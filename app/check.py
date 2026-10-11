import re

from engine.core import estimate
from estimate import HEAT_LABELS, map_extraction

CATEGORY_WORDS = [
    ("water", r"\b(water|tap|fountain|bottled)\b"),
    ("coffee_tea", r"\b(coffee|latte|espresso|cappuccino|tea|matcha|cold brew|frappuccino)\b"),
    ("soda", r"\b(soda|coke|cola|pepsi|sprite)\b"),
    ("dairy", r"\b(milk|yogurt|yoghurt|cheese)\b"),
    ("fast_food", r"\b(burger|fries|nuggets|mcdonald'?s|in-n-out|chipotle|taco bell)\b"),
    ("prepared_meal", r"\b(wrap|sandwich|salad|bowl|egg bites|meal)\b"),
]
CATEGORY_LABELS = {"water": "Water", "coffee_tea": "Coffee or tea", "soda": "Soda", "dairy": "Dairy",
                   "fast_food": "Fast food", "prepared_meal": "Prepared meal"}


def text_attrs(text):
    t = (text or "").lower()
    category = next((c for c, pat in CATEGORY_WORDS if re.search(pat, t)), "unknown")
    heated = "hot" if re.search(r"\b(hot|warm|warmed|heated|microwaved)\b", t) else \
        "cold" if re.search(r"\b(iced|cold|unheated|not heated)\b", t) else "unknown"
    return {"subject_type": "unknown", "brand": "unknown", "product_name": text or "unknown",
            "food_category": category, "packaging_material": [], "heated": heated}


def _text_chips(a):
    chips = []
    if a.get("food_category") in CATEGORY_LABELS:
        chips.append([CATEGORY_LABELS[a["food_category"]], 1])
    if a.get("heated") in HEAT_LABELS:
        chips.append([HEAT_LABELS[a["heated"]], 1, "heated"])
    return chips


def run_check(payload, extract, products):
    if payload.get("attrs"):
        attrs = payload["attrs"]
        chips = map_extraction(attrs)["chips"] if attrs.get("confidence") else _text_chips(attrs)
    elif payload.get("image"):
        attrs = extract(payload["image"], payload.get("text", ""))
        if payload.get("text"):
            attrs = {**attrs, "product_name": f'{attrs.get("product_name", "")} {payload["text"]}'.strip()}
        chips = map_extraction(attrs)["chips"]
    else:
        attrs = text_attrs(payload.get("text", ""))
        chips = _text_chips(attrs)
    return {"estimate": estimate(attrs, products), "attrs": attrs, "chips": chips}
