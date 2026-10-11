import pathlib

from check import run_check, text_attrs
from engine.loader import load_products

PRODUCTS = load_products(pathlib.Path(__file__).resolve().parents[1] / "data" / "plasticlist" / "plasticlist.tsv")


def no_extract(*_):
    raise AssertionError("extract should not be called without an image")


def test_text_attrs_detects_category_and_heat():
    a = text_attrs("hot latte from a cafe")
    assert a["food_category"] == "coffee_tea"
    assert a["heated"] == "hot"
    assert text_attrs("tap water in my hotel room")["food_category"] == "water"


def test_text_only_wrap_reaches_t1_with_swap():
    r = run_check({"text": "Starbucks spinach feta wrap warmed"}, no_extract, PRODUCTS)
    assert r["estimate"]["evidence_tier"] == "T1"
    assert r["estimate"]["swap"]["ratio"] > 1


def test_photo_path_uses_extraction_and_appends_chips():
    def fake_extract(image, text):
        return {"subject_type": "drink_in_vessel", "brand": "unknown", "product_name": "unknown", "food_category": "coffee_tea",
                "packaging_material": ["paper_cup_plastic_lid"], "heated": "hot", "machine_type": "not_a_machine",
                "jug_material": "none", "certification_marks": [], "vessel": "paper_cup",
                "confidence": {"subject_type": "high", "brand": "high", "packaging_material": "high", "heated": "high", "machine_type": "high"},
                "notes": ""}
    r = run_check({"image": "data:image/jpeg;base64,xx", "text": ""}, fake_extract, PRODUCTS)
    assert r["estimate"]["evidence_tier"] == "T3"
    assert ["Paper cup + plastic lid", 0] in r["chips"]


def test_attrs_override_reruns_without_extraction():
    r = run_check({"attrs": {"brand": "Starbucks", "product_name": "Spinach Feta Wrap", "heated": "hot"}}, no_extract, PRODUCTS)
    assert r["estimate"]["evidence_tier"] == "T1"
    assert r["attrs"]["heated"] == "hot"


def test_unheated_never_claims_lab_data_from_a_warmed_sample():
    r = run_check({"attrs": {"brand": "Starbucks", "product_name": "Spinach Feta Wrap", "heated": "cold",
                             "food_category": "prepared_meal"}}, no_extract, PRODUCTS)
    assert r["estimate"]["evidence_tier"] != "T1"
