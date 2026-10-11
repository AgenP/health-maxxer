# Image-capture eval schema

One JSON object per image. Golden labels (`labels.jsonl`) and model predictions (`preds/<model>.jsonl`) use the same fields. Use `"unknown"` when the image does not show it. Never guess for a golden label.

```json
{
  "id": "off-0001",
  "set": "off-packaging | snaps | machines",
  "file": "images/off/off-0001.jpg",
  "subject_type": "packaged_product | prepared_food | drink_in_vessel | water_machine | not_food",
  "brand": "string | unknown",
  "product_name": "string | unknown",
  "food_category": "water | soda | coffee_tea | dairy | canned | snack | prepared_meal | fast_food | produce | other | unknown",
  "packaging_material": ["pet_plastic", "other_plastic", "glass", "metal_can", "paper_carton", "paper_cup_plastic_lid", "paper", "foil", "none_visible", "unknown"],
  "heated": "hot | cold | ambient | unknown",
  "machine_type": "bottle_top_cooler_with_jug | bottom_load_cooler | plumbed_point_of_use | bottle_filling_station | drinking_fountain | fridge_dispenser | countertop_filter | not_a_machine | unknown",
  "jug_material": "polycarbonate | pet | other_plastic | glass | none | unknown",
  "certification_marks": ["e.g. NSF/ANSI 53", "none_visible"],
  "vessel": "plastic_bottle | plastic_cup | paper_cup | metal | glass | ceramic | none | unknown",
  "label_source": "where the golden label came from (OFF tags, Commons description, manual)",
  "notes": "free text"
}
```

Scoring (code-based, no LLM judge needed):
- **Exact match**: subject_type, food_category, heated, machine_type, jug_material, vessel.
- **Set F1**: packaging_material, certification_marks.
- **Fuzzy match**: brand (case-insensitive, normalised).
- **Abstention**: a prediction of `unknown` where the label is known counts as a miss but is tracked separately from a wrong answer. Wrong-and-confident is the failure that matters most for the product (decision 5: chips must be trustworthy).
