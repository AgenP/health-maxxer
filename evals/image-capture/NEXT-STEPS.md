# Image capture: planned next steps

Status 2026-10-11: Opus 5.5 (medium) baseline run on 71 images, see `results-opus-5-5-medium.md`. Nothing below has been run yet.

## 1. Taxonomy catch-all and gradual expansion (decided, not built)

**Problem.** Fixed-choice fields force the model to pick the nearest wrong value or abstain. Known gaps in `packaging_material`: polystyrene foam (styrofoam clamshells and cups, high concern), bioplastic (PLA), silicone, moulded fibre (snap-018 had to be labelled `paper`).

**Decision.** Keep the constrained taxonomy (the estimate engine's factor lookups, editable chip dropdowns, Top Contributors grouping and eval scoring all need a fixed vocabulary). Do **not** switch to fully free text: it would need a second normalisation step anyway and loses consistency and scorability.

**Change to make:**
1. Add `other` to every fixed-choice field, with a required free-text partner (e.g. `packaging_other: "polystyrene foam clamshell"`).
2. Keep `unknown` (cannot see it, an information gap) separate from `other` (can see it, not in the list, a taxonomy gap).
3. Estimate behaviour:

| Extracted as | Estimate behaviour |
|---|---|
| Known value | Use its factor |
| `other` + text | Back off to the parent class (e.g. "plastic, unspecified") or the category prior; band widens (T2 to T3). Chip shows *Other: "<text>"*, editable |
| `unknown` | Same broad prior; result card lists it as missing ("would sharpen this: packaging") |

`other` costs precision but never correctness. A forced wrong value gives a confident wrong factor and a falsely narrow band.

**Expansion loop:**
- Log every `other` text; periodically cluster them (open coding to axial coding, as in Hamel's error-discovery skill).
- Promote a cluster to an enum value **only if it changes the estimate** (e.g. polystyrene gets its own migration factor). Otherwise map it onto an existing value.
- Trigger: `other` rate per field above roughly 5 to 10% (starting rule of thumb, unvalidated).

**Zero-cost first pass:** mine the free-text `notes` field of the 71 existing predictions (`preds/claude-opus-5-5__medium.jsonl`) for materials and categories that don't fit the current enums. That gives the first expansion list before any schema change.

## 2. Schema rules for ambiguous cases (from the miss review)

- **Sealed vs prepared:** "sold sealed = packaged_product" (deli salads in clamshells, microwave meals).
- **Multi-item scenes:** either a "primary item" rule or a list of items per photo (snap-022 burger + Lipton bottle + Grill'd branding; snap-007 iced latte + fruit salad).
- **Overlapping categories:** define `fast_food` vs `prepared_meal` boundaries (definitions, not new values).
- **Incidental materials:** whether plates, drinking glasses and paper liners count as packaging.

## 3. Label hygiene

- Fix the two known golden-label errors from Open Food Facts (off-0007 tagged paper, actually a can; off-0014 image is Poland Spring, product is Hellmann's).
- Add a sanity check before OFF data feeds estimates: OFF tags and images can disagree with the product.
- Normalise accents in the brand scorer (Maçarico vs Macarico) to match the review app.

## 4. Coverage gaps in the image sets

- **Polycarbonate jugs:** no golden jug-material labels exist, so the highest-value machine field is untested. Best single test image: the WeWork machine plus its model plate (Philip to snap).
- No blurry or dark snaps; hard cases are only clutter, distance and occlusion.
- No fridge-door dispensers.
- All images are Commons/OFF, not target-user photos. Results are indicative only.

## 5. Comparisons (when asked)

Same images, same scorer: Opus 5.5 at low effort, and Sonnet 5.5 or Haiku 5.5 (only if explicitly chosen), comparing accuracy, abstention, latency (baseline median 4.5 s, p90 7.8 s) and cost (baseline about $0.03/image).

## 6. Human review

Philip's labels from the review app (`serve_review.py`, saved to `review/labels-<run>.json`) feed the error analysis for steps 1 and 2.
