PACKAGING_LABELS = {
    "pet_plastic": "PET plastic", "other_plastic": "Plastic", "glass": "Glass", "metal_can": "Can",
    "paper_carton": "Carton", "paper_cup_plastic_lid": "Paper cup + plastic lid", "paper": "Paper",
    "foil": "Foil", "none_visible": "No packaging",
}
HEAT_LABELS = {"hot": "Heated", "cold": "Not heated", "ambient": "Room temp"}
PLASTIC = {"pet_plastic", "other_plastic", "paper_cup_plastic_lid"}


def _inferred(conf, field):
    return 0 if conf.get(field) == "high" else 1


def _chips(e):
    conf = e.get("confidence", {})
    chips = []
    if e.get("brand", "unknown") != "unknown":
        chips.append([e["brand"], _inferred(conf, "brand")])
    for m in e.get("packaging_material", []):
        if m in PACKAGING_LABELS:
            chips.append([PACKAGING_LABELS[m], _inferred(conf, "packaging_material")])
    if e.get("heated") in HEAT_LABELS:
        chips.append([HEAT_LABELS[e["heated"]], _inferred(conf, "heated"), "heated"])
    if e.get("machine_type") not in (None, "not_a_machine", "unknown"):
        chips.append([e["machine_type"].replace("_", " ").capitalize(), _inferred(conf, "machine_type")])
    return chips


def _packaging_hint(materials):
    if set(materials) & PLASTIC:
        return "plastic"
    if "metal_can" in materials:
        return "can"
    if set(materials) & {"glass", "none_visible"}:
        return "glass"
    return None


def map_extraction(e):
    name = f'{e.get("brand", "")} {e.get("product_name", "")}'.lower()
    if e.get("subject_type") == "water_machine" or e.get("food_category") == "water":
        key = "water"
    elif "starbucks" in name and "wrap" in name:
        key = "wrapCold" if e.get("heated") in ("cold", "ambient") else "wrap"
    else:
        key = "unknown"
    out = {"estimate_key": key, "chips": _chips(e), "extraction": e}
    if key == "unknown" and e.get("subject_type") != "not_food":
        out["packaging_hint"] = _packaging_hint(e.get("packaging_material", []))
    return out
