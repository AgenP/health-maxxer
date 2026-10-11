import json, glob, time, urllib.request, random, sys
UA = {"User-Agent": "HealthMaxxerHackathon/0.1 (philip@pinnacleprompts.com)"}
FAM = {"plastic": "other_plastic", "pet-1-polyethylene-terephthalate": "pet_plastic", "pet": "pet_plastic",
       "glass": "glass", "brown-glass": "glass", "metal": "metal_can", "aluminium": "metal_can", "steel": "metal_can",
       "paper": "paper", "cardboard": "paper", "paperboard": "paper", "tetra-pak": "paper_carton"}
CAT = {"waters": "water", "canned-foods": "canned", "coffees": "coffee_tea", "teas": "coffee_tea"}
random.seed(7)
out, n = [], 0
for path in sorted(glob.glob("data/off-samples/*.json")):
    cat = CAT[path.split("/")[-1][:-5]]
    prods = [p for p in json.load(open(path)) if p.get("packaging_materials_tags")]
    random.shuffle(prods)
    taken = 0
    for p in prods:
        mats = sorted({FAM[t.split(":")[1]] for t in p["packaging_materials_tags"] if t.split(":")[1] in FAM})
        if not mats or taken >= 10:
            continue
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(
                f"https://world.openfoodfacts.org/api/v2/product/{p['code']}?fields=image_front_url,brands,product_name", headers=UA), timeout=30))
            url = (d["product"].get("image_front_url") or "").replace(".400.jpg", ".full.jpg")
            if not url:
                continue
            n += 1
            fid = f"off-{n:04d}"
            fn = f"evals/image-capture/images/off/{fid}.jpg"
            open(fn, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
        except Exception as e:
            print("skip", p["code"], e, file=sys.stderr); continue
        out.append({"id": fid, "set": "off-packaging", "file": fn.replace("evals/image-capture/", ""),
                    "subject_type": "packaged_product", "brand": (d["product"].get("brands") or "unknown").split(",")[0].strip() or "unknown",
                    "product_name": d["product"].get("product_name") or "unknown", "food_category": cat,
                    "packaging_material": mats, "label_source": f"https://world.openfoodfacts.org/product/{p['code']} packaging_materials_tags={p['packaging_materials_tags']}",
                    "notes": "multi-material tags describe the whole pack (incl. caps/labels); score at material-family level"})
        taken += 1
        time.sleep(0.7)
with open("evals/image-capture/labels-off.jsonl", "w") as f:
    for r in out: f.write(json.dumps(r) + "\n")
print(len(out), "images")
