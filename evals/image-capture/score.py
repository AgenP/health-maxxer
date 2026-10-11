"""Score predictions against golden labels. Usage: .venv/bin/python evals/image-capture/score.py preds/<file>.jsonl"""
import json, pathlib, statistics, sys
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
EXACT = ["subject_type", "food_category", "heated", "machine_type", "jug_material", "vessel"]
FAMILY = {"pet_plastic": "plastic", "other_plastic": "plastic", "paper_cup_plastic_lid": "paper+plastic", "glass": "glass",
          "metal_can": "metal", "foil": "metal", "paper": "paper", "paper_carton": "paper", "none_visible": "none"}
UNK = {"unknown", "", None}


def norm(s):
    return "".join(c for c in (s or "").lower() if c.isalnum())


def fam(xs):
    out = set()
    for x in xs or []:
        out |= set(FAMILY.get(x, x).split("+")) if x not in UNK else set()
    return out


def main():
    preds = {r["id"]: r for r in map(json.loads, open(sys.argv[1]))}
    gold = []
    for f in ROOT.glob("labels-*.jsonl"):
        gold += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    stats = defaultdict(lambda: defaultdict(lambda: {"right": 0, "wrong": 0, "abstain": 0}))
    wrongs, lat = [], []
    for g in gold:
        p = preds.get(g["id"])
        if not p or p.get("error"):
            continue
        lat.append(p.get("latency_s", 0))
        s = g["set"]
        fields = [k for k in EXACT if g.get(k) not in UNK and k in g]
        for k in fields:
            if p.get(k) in UNK:
                stats[s][k]["abstain"] += 1
            elif p.get(k) == g[k]:
                stats[s][k]["right"] += 1
            else:
                stats[s][k]["wrong"] += 1
                wrongs.append((g["id"], k, g[k], p.get(k), p.get("confidence", {}).get(k)))
        if g.get("brand") not in UNK:
            pb, gb = norm(p.get("brand")), norm(g["brand"])
            key = "abstain" if p.get("brand") in UNK else ("right" if pb and (pb in gb or gb in pb) else "wrong")
            stats[s]["brand"][key] += 1
            if key == "wrong":
                wrongs.append((g["id"], "brand", g["brand"], p.get("brand"), p.get("confidence", {}).get("brand")))
        gm = fam(g.get("packaging_material"))
        if gm:
            pm = fam(p.get("packaging_material"))
            if not pm:
                stats[s]["packaging_family"]["abstain"] += 1
            elif gm & pm and not (pm - gm):
                stats[s]["packaging_family"]["right"] += 1
            elif gm & pm:
                stats[s]["packaging_family"]["right"] += 1
                stats[s]["packaging_extra_material"]["wrong"] += 1
            else:
                stats[s]["packaging_family"]["wrong"] += 1
                wrongs.append((g["id"], "packaging", sorted(gm), sorted(pm), p.get("confidence", {}).get("packaging_material")))
    print(f"# {pathlib.Path(sys.argv[1]).name}")
    errs = [p for p in preds.values() if p.get("error")]
    print(f"n_pred={len(preds)} errors={len(errs)} latency median={statistics.median(lat) if lat else 0:.1f}s p90={sorted(lat)[int(.9*len(lat))-1] if lat else 0:.1f}s")
    served = defaultdict(int)
    for p in preds.values():
        served[p.get("served_model")] += 1
    print("served_by:", dict(served))
    print("\n| set | field | n | right | wrong | abstain | accuracy (excl. abstain) |\n|---|---|---|---|---|---|---|")
    for s in sorted(stats):
        for k, v in sorted(stats[s].items()):
            n = v["right"] + v["wrong"] + v["abstain"]
            dec = v["right"] + v["wrong"]
            print(f"| {s} | {k} | {n} | {v['right']} | {v['wrong']} | {v['abstain']} | {v['right']/dec:.0%} |" if dec else f"| {s} | {k} | {n} | 0 | 0 | {v['abstain']} | - |")
    print("\n## Wrong answers (id, field, gold, pred, model confidence)")
    for w in wrongs:
        print("-", *w)


if __name__ == "__main__":
    main()
