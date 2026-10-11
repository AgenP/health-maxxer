from pathlib import Path

import pytest

from engine.core import SOURCES, Product, Sample, estimate, find_swap, match_product, product_median
from engine.loader import load_products

TSV = Path(__file__).resolve().parents[3] / "data" / "plasticlist" / "plasticlist.tsv"


@pytest.fixture(scope="module")
def products():
    return load_products(TSV)


def test_loader_groups_samples_by_product(products):
    assert sum(len(p.samples) for p in products.values()) == 618
    wrap = products["170"]
    assert wrap.name == "Starbucks Spinach Feta Wrap Warmed"
    assert "prepared_meals" in wrap.tags
    assert sorted(s.ng_g for s in wrap.samples) == [22.0, 76.0, 149.0]


def test_loader_marks_loq_as_censored(products):
    tea = products["79"]
    assert all(s.censored and s.ng_g is None for s in tea.samples)


def test_match_product_fuzzy(products):
    assert match_product("Starbucks spinach feta wrap warmed", products).product_id == "170"
    assert match_product("mystery snack", products) is None


def test_t1_estimate_for_wrap(products):
    e = estimate({"brand": "Starbucks", "product_name": "Spinach Feta Wrap", "heated": "hot",
                  "food_category": "prepared_meal", "packaging_material": ["paper"]}, products)
    assert e["evidence_tier"] == "T1"
    assert e["tier"] in ("lo", "med", "hi")
    assert e["band"][0] <= e["percentile"] <= e["band"][1]
    assert e["reference_level"]["min_pct_tdi"] == 0.1
    assert e["reference_level"]["max_pct_tdi"] == 0.7
    assert set(e["sources"]) <= set(SOURCES)
    assert e["swap"]["evidence"] == "lab-backed"


def test_t3_category_prior_has_no_point_estimate(products):
    e = estimate({"food_category": "coffee_tea", "packaging_material": ["paper_cup_plastic_lid"], "heated": "hot"},
                 products)
    assert e["evidence_tier"] == "T3"
    assert e["point"] is None
    assert e["reference_level"] is None and e["reference_reason"]
    assert "brand" in e["missing"]


def test_unknown_is_t5(products):
    e = estimate({"product_name": "mystery snack", "food_category": "unknown"}, products)
    assert e["evidence_tier"] == "T5"
    assert e["tier"] == "unk" and e["point"] is None


def test_water_is_comparison_card(products):
    e = estimate({"food_category": "water"}, products)
    assert e["kind"] == "water" and e["evidence_tier"] == "T3"
    assert e["sources"] == ["dep", "mason"]


def test_swap_for_wrap_is_lower_and_overlapping(products):
    s = find_swap(products["170"], products)
    assert s["product"].startswith("Starbucks")
    assert s["ratio"] > 1
    assert s["evidence"] == "lab-backed"


def test_swap_wrap_vs_egg_bites_overlaps(products):
    s = find_swap(products["170"], products, candidates=[products["172"]])
    assert s["product"] == "Starbucks Bacon Gruyere Egg Bites Warmed"
    assert s["ranges_overlap"] is True
    assert s["ratio"] == pytest.approx(76 / 17, rel=0.01)


def test_censored_samples_use_half_loq_in_median():
    p = Product("x", "x", ("t",), (Sample(None, True, None, None), Sample(10.0, False, None, None)))
    assert product_median(p, loq=2.0) == pytest.approx((1.0 + 10.0) / 2)


def test_generic_latte_does_not_t1_match_matcha_latte(products):
    e = estimate({"brand": "Starbucks", "product_name": "Latte", "food_category": "coffee_tea", "heated": "hot"}, products)
    assert e["evidence_tier"] == "T2" and e["point"] is not None
