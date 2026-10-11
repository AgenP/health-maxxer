# claude-opus-5-5__medium.jsonl
n_pred=71 errors=0 latency median=4.5s p90=7.8s
served_by: {'claude-opus-5-5': 71}

| set | field | n | right | wrong | abstain | accuracy (excl. abstain) |
|---|---|---|---|---|---|---|
| machines | brand | 11 | 9 | 1 | 1 | 90% |
| machines | food_category | 23 | 23 | 0 | 0 | 100% |
| machines | jug_material | 14 | 14 | 0 | 0 | 100% |
| machines | machine_type | 23 | 23 | 0 | 0 | 100% |
| machines | packaging_family | 14 | 11 | 1 | 2 | 92% |
| machines | subject_type | 23 | 23 | 0 | 0 | 100% |
| machines | vessel | 22 | 17 | 2 | 3 | 89% |
| off-packaging | brand | 17 | 15 | 2 | 0 | 88% |
| off-packaging | food_category | 18 | 16 | 2 | 0 | 89% |
| off-packaging | packaging_extra_material | 1 | 0 | 1 | 0 | 0% |
| off-packaging | packaging_family | 18 | 17 | 1 | 0 | 94% |
| off-packaging | subject_type | 18 | 18 | 0 | 0 | 100% |
| snaps | brand | 13 | 11 | 1 | 1 | 92% |
| snaps | food_category | 27 | 24 | 2 | 1 | 92% |
| snaps | heated | 9 | 7 | 0 | 2 | 100% |
| snaps | jug_material | 30 | 30 | 0 | 0 | 100% |
| snaps | machine_type | 30 | 30 | 0 | 0 | 100% |
| snaps | packaging_extra_material | 2 | 0 | 2 | 0 | 0% |
| snaps | packaging_family | 29 | 23 | 3 | 3 | 88% |
| snaps | subject_type | 30 | 25 | 5 | 0 | 83% |
| snaps | vessel | 30 | 29 | 1 | 0 | 97% |

## Wrong answers (id, field, gold, pred, model confidence)
- mach-002 brand Clickon Clikon high
- mach-003 vessel none plastic_cup None
- mach-013 packaging ['none'] ['plastic'] medium
- mach-020 vessel none paper_cup None
- off-0005 food_category canned other None
- off-0007 packaging ['paper'] ['metal'] high
- off-0009 brand Macarico Maçarico high
- off-0014 brand Hellmann's Poland Spring high
- off-0016 food_category water other None
- snap-007 subject_type drink_in_vessel prepared_food medium
- snap-007 food_category coffee_tea produce None
- snap-013 vessel glass plastic_bottle None
- snap-013 packaging ['glass'] ['plastic'] medium
- snap-016 subject_type packaged_product prepared_food medium
- snap-020 subject_type packaged_product not_food medium
- snap-021 packaging ['glass'] ['none'] medium
- snap-022 food_category prepared_meal fast_food None
- snap-022 brand Lipton Grill'd high
- snap-024 subject_type packaged_product prepared_food high
- snap-025 subject_type packaged_product prepared_food high
- snap-027 packaging ['none'] ['paper'] medium

## Review of misses (2026-10-11, manual)

**Label errors (model was right):**
- off-0007: OFF tags the can as `paper` (likely its paper label); model said `metal_can`. Gold is wrong.
- off-0014: the OFF front image is a Poland Spring water bottle filed under a Hellmann's product. Model read the photo correctly. Gold is wrong.
- mach-002 (Clickon vs Clikon) and off-0009 (Macarico vs Maçarico): spelling/accent normalisation in the scorer, not model errors.

**Taxonomy ambiguity (fix the schema, not the model):**
- subject_type packaged_product vs prepared_food for deli salads in clamshells (snap-024, snap-025) and microwave meals (snap-016). Needs a rule: "sold sealed = packaged_product".
- Multi-item scenes: snap-022 brand Lipton (drink) vs Grill'd (restaurant); snap-007 iced latte vs fruit salad. Needs a "primary item" rule or a multi-item output.
- snap-021 / mach-013 / snap-027: "none" vs incidental glassware or paper liners.

**Plausible real errors:**
- snap-013: Coca-Cola contour bottle predicted PET, gold glass (medium confidence). Contour bottles exist in both; ambiguous from this photo.
- off-0005, off-0016: food_category `other` for canned/water items (low stakes).

**Trivially-satisfied fields:** jug_material and machine_type on snaps (all `none`/`not_a_machine`), and jug_material on machines (golden jug resin is never labelled). These 100% rows say nothing about polycarbonate detection.

**Bottom line:** after removing label errors, packaging family is roughly 17/17 on OFF and 23/26 on snaps where decided; no high-confidence wrong packaging calls remain. Brand reading from legible labels is strong; the model abstains on logo-less cups as instructed (snap-001). Latency median 4.5 s, p90 7.8 s at medium effort; ~$0.03/image.
