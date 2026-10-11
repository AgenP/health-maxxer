from estimate import map_extraction


def ext(**kw):
    base = {"subject_type": "prepared_food", "brand": "unknown", "product_name": "unknown", "food_category": "unknown",
            "packaging_material": [], "heated": "unknown", "machine_type": "not_a_machine", "jug_material": "none",
            "certification_marks": [], "vessel": "none",
            "confidence": {"subject_type": "high", "brand": "high", "packaging_material": "high", "heated": "high", "machine_type": "high"},
            "notes": ""}
    base.update(kw)
    return base


def test_starbucks_wrap_heated_maps_to_lab_measured_wrap():
    r = map_extraction(ext(brand="Starbucks", product_name="Spinach & Feta Wrap", heated="hot", packaging_material=["paper"]))
    assert r["estimate_key"] == "wrap"


def test_starbucks_wrap_cold_maps_to_unheated_wrap():
    r = map_extraction(ext(brand="Starbucks", product_name="Spinach Feta Wrap", heated="cold"))
    assert r["estimate_key"] == "wrapCold"


def test_water_machine_and_water_drinks_map_to_water():
    assert map_extraction(ext(subject_type="water_machine", machine_type="bottle_filling_station"))["estimate_key"] == "water"
    assert map_extraction(ext(subject_type="packaged_product", food_category="water", packaging_material=["pet_plastic"]))["estimate_key"] == "water"


def test_unrecognised_food_falls_back_to_unknown():
    assert map_extraction(ext(subject_type="not_food"))["estimate_key"] == "unknown"


def test_chips_mark_low_confidence_fields_as_inferred_and_skip_unknowns():
    r = map_extraction(ext(brand="Starbucks", product_name="Spinach Feta Wrap", heated="hot", packaging_material=["paper"],
                           confidence={"subject_type": "high", "brand": "high", "packaging_material": "low", "heated": "high", "machine_type": "high"}))
    assert ["Starbucks", 0] in r["chips"]
    assert ["Paper", 1] in r["chips"]
    assert ["Heated", 0, "heated"] in r["chips"]
    assert not any(c[0].lower() == "unknown" for c in r["chips"])
