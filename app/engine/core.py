import math
import re
from bisect import bisect_right
from dataclasses import dataclass
from statistics import median

SOURCES = {
    "plasticlist": {"label": "PlasticList report", "url": "https://www.plasticlist.org/report"},
    "efsa": {"label": "EFSA 2019 phthalates TDI", "url": "https://doi.org/10.2903/j.efsa.2019.5838"},
    "dep": {"label": "NYC DEP 2025 Drinking Water Supply and Quality Report",
            "url": "https://www.nyc.gov/assets/dep/downloads/pdf/water/drinking-water/drinking-water-supply-quality-report/2025-drinking-water-supply-quality-report.pdf"},
    "epa": {"label": "EPA PFAS drinking water", "url": "https://www.epa.gov/sdwa/and-polyfluoroalkyl-substances-pfas"},
    "mason": {"label": "Mason et al. 2018, microplastics in bottled water", "url": "https://doi.org/10.3389/fchem.2018.00407"},
}

CATEGORY_TAGS = {
    "coffee_tea": ("coffee", "tea"),
    "fast_food": ("fast_food",),
    "prepared_meal": ("prepared_meals",),
    "dairy": ("dairy",),
    "soda": ("sodas",),
    "snack": ("snacks",),
    "water": ("water",),
}

# PlasticList reports censored values only as "<LOQ" with no numeric limit, so the
# smallest detected value in the dataset (0.8 ng/g) stands in for the LOQ.
DEFAULT_LOQ = 0.8
MATCH_THRESHOLD = 0.6
WIDEN = {"T2": 2.0, "T3": 3.0}
STOPWORDS = {"and", "the", "a", "of", "with", "unknown"}


@dataclass(frozen=True)
class Sample:
    ng_g: float | None
    censored: bool
    pct_tdi: float | None
    serving_g: float | None


@dataclass(frozen=True)
class Product:
    product_id: str
    name: str
    tags: tuple
    samples: tuple


def _value(s, loq):
    return loq / 2 if s.censored else s.ng_g


def product_median(p, loq=DEFAULT_LOQ):
    return median(_value(s, loq) for s in p.samples)


def _range(p, loq=DEFAULT_LOQ):
    vals = [_value(s, loq) for s in p.samples]
    return min(vals), max(vals)


def _tokens(text):
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if t not in STOPWORDS}


def match_product(query, products, threshold=MATCH_THRESHOLD):
    q = _tokens(query)
    if not q:
        return None
    best, best_score = None, 0.0
    for p in products.values():
        t = _tokens(p.name)
        score = len(q & t) / len(q | t)
        if score > best_score:
            best, best_score = p, score
    return best if best_score >= threshold else None


def _percentile(x, sorted_medians):
    return round(100 * bisect_right(sorted_medians, x) / len(sorted_medians))


def _tier(pct):
    return "lo" if pct < 33 else "med" if pct < 67 else "hi"


def _brand_of(p):
    return p.name.split()[0].lower()


def find_swap(product, products, candidates=None):
    if candidates is None:
        candidates = [c for c in products.values() if c.product_id != product.product_id and set(c.tags) & set(product.tags)]
    m = product_median(product)
    lower = [c for c in candidates if product_median(c) < m and any(not s.censored for s in c.samples)]
    if not lower:
        return None
    brand = _brand_of(product)
    pick = min(lower, key=lambda c: (_brand_of(c) != brand, -product_median(c)))
    (a_lo, a_hi), (b_lo, b_hi) = _range(product), _range(pick)
    return {
        "product": pick.name,
        "product_id": pick.product_id,
        "ratio": round(m / product_median(pick), 2),
        "ranges_overlap": a_lo <= b_hi and b_lo <= a_hi,
        "evidence": "lab-backed",
        "sources": ["plasticlist"],
    }


def _query(attrs):
    parts = [attrs.get("brand"), attrs.get("product_name")]
    text = " ".join(p for p in parts if p and p != "unknown")
    if text and attrs.get("heated") == "hot":
        text += " warmed"
    return text


def _missing(attrs):
    return [k for k in ("brand", "product_name", "packaging_material", "heated")
            if attrs.get(k) in (None, "", "unknown", [])]


def estimate(attrs, products):
    if attrs.get("food_category") == "water" or attrs.get("subject_type") == "water_machine":
        return {"kind": "water", "evidence_tier": "T3", "tier": "unk", "point": None, "band": None,
                "reference_level": None, "reference_reason": "compared against NYC tap and bottled-water literature",
                "sources": ["dep", "mason"], "missing": _missing(attrs), "swap": None}
    medians = sorted(product_median(p) for p in products.values())
    out = {"kind": "food", "missing": _missing(attrs), "swap": None,
           "reference_level": None, "reference_reason": None}

    hit = match_product(_query(attrs), products)
    if hit:
        lo, hi = _range(hit)
        m = product_median(hit)
        tdi = [s.pct_tdi for s in hit.samples if s.pct_tdi is not None]
        pct = _percentile(m, medians)
        out.update(evidence_tier="T1", matched_product=hit.name, point=m, percentile=pct, tier=_tier(pct),
                   band=[_percentile(lo, medians), _percentile(hi, medians)], sources=["plasticlist"],
                   swap=find_swap(hit, products))
        if tdi:
            out["reference_level"] = {"source": "efsa", "type": "EFSA tolerable daily intake, 70 kg adult, per serving",
                                      "min_pct_tdi": min(tdi), "max_pct_tdi": max(tdi)}
            out["sources"].append("efsa")
        else:
            out["reference_reason"] = "all samples below the limit of quantification"
        return out

    tags = set(CATEGORY_TAGS.get(attrs.get("food_category"), ()))
    group = [p for p in products.values() if tags & set(p.tags)]
    brand = (attrs.get("brand") or "").lower()
    branded = [p for p in group if brand and brand != "unknown" and _brand_of(p) == brand.split()[0]]
    if branded:
        tier_name, pool = "T2", branded
    elif group:
        tier_name, pool = "T3", group
    else:
        out.update(evidence_tier="T5", tier="unk", point=None, percentile=None, band=None, sources=["plasticlist"],
                   reference_reason="no comparable lab measurement")
        return out
    m = median(product_median(p) for p in pool)
    f = WIDEN[tier_name]
    pct = _percentile(m, medians)
    out.update(evidence_tier=tier_name, point=m if tier_name == "T2" else None, percentile=pct, tier=_tier(pct),
               band=[_percentile(m / f, medians), _percentile(m * f, medians)], sources=["plasticlist"],
               prior_products=len(pool),
               reference_reason="reference levels are only shown for lab-measured products")
    return out
