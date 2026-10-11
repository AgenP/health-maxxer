"""Run a Claude vision model over the labelled image sets and write predictions.

Usage: .venv/bin/python evals/image-capture/run_eval.py [--model claude-opus-5-5] [--effort medium] [--sets off,snaps,machines] [--limit N]
Reads ANTHROPIC_API_KEY from $HM_ENV_FILE, the repo-root .env, or AIOS/secrets/hackathon.env (all git-ignored).
"""
import argparse, base64, json, mimetypes, os, pathlib, time
from concurrent.futures import ThreadPoolExecutor

import anthropic

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[1]

PACKAGING = ["pet_plastic", "other_plastic", "glass", "metal_can", "paper_carton", "paper_cup_plastic_lid", "paper", "foil", "none_visible", "unknown"]
SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["subject_type", "brand", "product_name", "food_category", "packaging_material", "heated", "machine_type",
                 "jug_material", "certification_marks", "vessel", "confidence", "notes"],
    "properties": {
        "subject_type": {"type": "string", "enum": ["packaged_product", "prepared_food", "drink_in_vessel", "water_machine", "not_food"]},
        "brand": {"type": "string"},
        "product_name": {"type": "string"},
        "food_category": {"type": "string", "enum": ["water", "soda", "coffee_tea", "dairy", "canned", "snack", "prepared_meal", "fast_food", "produce", "other", "unknown"]},
        "packaging_material": {"type": "array", "items": {"type": "string", "enum": PACKAGING}},
        "heated": {"type": "string", "enum": ["hot", "cold", "ambient", "unknown"]},
        "machine_type": {"type": "string", "enum": ["bottle_top_cooler_with_jug", "bottom_load_cooler", "plumbed_point_of_use", "bottle_filling_station", "drinking_fountain", "fridge_dispenser", "countertop_filter", "not_a_machine", "unknown"]},
        "jug_material": {"type": "string", "enum": ["polycarbonate", "pet", "other_plastic", "glass", "none", "unknown"]},
        "certification_marks": {"type": "array", "items": {"type": "string"}},
        "vessel": {"type": "string", "enum": ["plastic_bottle", "plastic_cup", "paper_cup", "metal", "glass", "ceramic", "none", "unknown"]},
        "confidence": {
            "type": "object", "additionalProperties": False,
            "required": ["subject_type", "brand", "packaging_material", "heated", "machine_type"],
            "properties": {k: {"type": "string", "enum": ["high", "medium", "low"]} for k in ["subject_type", "brand", "packaging_material", "heated", "machine_type"]},
        },
        "notes": {"type": "string"},
    },
}

SYSTEM = """You extract structured facts from a photo a person took of food, drink, or a water machine. The facts feed an estimate of exposure to microplastics and plastic-associated chemicals, and the person sees each fact as an editable chip, so a confident wrong answer is worse than "unknown".

Report only what the photo shows or what printed text on it states. Use "unknown" (or an empty list) whenever you cannot see it. Do not infer a brand from style alone.
- brand / product_name: as printed; "unknown" if not legible.
- packaging_material: every material in direct contact with the food or drink that you can see (e.g. a coffee cup is paper_cup_plastic_lid; a can is metal_can; a clear water bottle is pet_plastic only if marked or clearly a standard PET bottle, otherwise other_plastic). none_visible for unpackaged food.
- heated: hot if steam, a hot drink, or freshly heated food is evident; cold if iced or chilled; ambient for shelf-stable products at room temperature.
- machine_type and jug_material only for water machines; otherwise not_a_machine and none.
- certification_marks: certification text you can actually read (e.g. "NSF/ANSI 53"); empty list if none.
- vessel: what the person would drink from, if visible.
- confidence: your confidence in each listed field."""


def load_env():
    for env in [pathlib.Path(os.environ.get("HM_ENV_FILE", REPO / ".env")), REPO.parents[1] / "secrets" / "hackathon.env"]:
        if not env.exists():
            continue
        for line in env.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def predict(client, model, effort, row):
    path = ROOT / row["file"]
    media = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    data = base64.standard_b64encode(path.read_bytes()).decode()
    t0 = time.time()
    resp = client.beta.messages.create(
        model=model,
        max_tokens=4000,
        system=SYSTEM,
        output_config={"effort": effort, "format": {"type": "json_schema", "schema": SCHEMA}},
        betas=["server-side-fallback-2026-07-01"],
        extra_body={"fallbacks": "default"},
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
            {"type": "text", "text": "Extract the facts from this photo."},
        ]}],
    )
    latency = time.time() - t0
    out = {"id": row["id"], "set": row["set"], "served_model": resp.model, "stop_reason": resp.stop_reason,
           "latency_s": round(latency, 2), "input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens}
    if resp.stop_reason == "refusal":
        out["error"] = "refusal"
        return out
    text = next(b.text for b in resp.content if b.type == "text")
    out.update(json.loads(text))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5-5")
    ap.add_argument("--effort", default="medium")
    ap.add_argument("--sets", default="off,snaps,machines")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    load_env()
    client = anthropic.Anthropic()
    rows = []
    for s in a.sets.split(","):
        f = ROOT / f"labels-{s}.jsonl"
        if f.exists():
            rows += [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
    if a.limit:
        rows = rows[: a.limit]
    outdir = ROOT / "preds"
    outdir.mkdir(exist_ok=True)
    outfile = outdir / f"{a.model}__{a.effort}.jsonl"

    def safe(row):
        try:
            return predict(client, a.model, a.effort, row)
        except anthropic.APIStatusError as e:
            return {"id": row["id"], "set": row["set"], "error": f"{e.status_code}: {e.message}"}
        except anthropic.APIConnectionError as e:
            return {"id": row["id"], "set": row["set"], "error": f"connection: {e}"}

    with ThreadPoolExecutor(a.workers) as ex, outfile.open("w") as f:
        for r in ex.map(safe, rows):
            f.write(json.dumps(r) + "\n")
            print(r["id"], r.get("error") or f"{r.get('latency_s')}s {r.get('served_model')}")
    print("wrote", outfile)


if __name__ == "__main__":
    main()
