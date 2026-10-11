# Estimation methods

Core stance: estimate **relative risk with an uncertainty band and per-factor citations**, not absolute particle counts. Microplastic measurement methods disagree by orders of magnitude, so a precise number reads as fake; a ranked tier with a "why" reads as rigorous.

## Methods

| # | Method | What it is | Data |
|---|---|---|---|
| 1 | Composition graph (LCA-style) | Product → ingredients, packaging, processing steps, contact materials. Each node gets a hazard/emission factor; sum. Same structure as life-cycle assessment. | Open Food Facts API (ingredients, packaging materials, NOVA), Agribalyse, EPA USEEIO |
| 2 | Migration physics | Regulatory diffusion modelling (Piringer approach) for packaging → food migration. Drivers: polymer, temperature, contact time, fat content, surface-to-volume ratio. Encode as multipliers (heat, fatty, long shelf life). Strongest "derivation" story. | EU food-contact migration modelling literature |
| 3 | Measured lookup + nearest-neighbour fill | Use lab values where they exist; borrow from similar products (same category + packaging) where they don't. | PlasticList, FCCmigex (chemical list only), USDA PDP, FDA Total Diet Study, EPA CPDat/CompTox |
| 4 | Literature emission factors | A 15–20 paper factor table. Anchors: PET bottled water ~240k particles/L (Qian 2024, PNAS); plastic tea bags, billions of particles per cup (Hernandez 2019); microwaving PP containers (Hussain 2023). **Check exact figures before putting them on a slide.** | Papers |
| 5 | Bayesian / Monte Carlo | Category prior, updated with product features, uncertainty propagated. Output e.g. "Tier 4/5, 80% interval". | numpy |
| 6 | LLM gap-filling | Infer missing packaging/process from name, description, photo. Badge those nodes "inferred", lower confidence. | Claude API |

## Framing

- **Hazard ≠ exposure.** Score = hazard of inputs × migration conditions × consumption frequency. Frequency is the personal health-maxxing angle.
- **Validate against held-out data.** Predict PlasticList rank from composition alone (leave-one-out), report Spearman ρ. Answers the feasibility question directly.
- **Every score expands to provenance:** measured / derived / inferred.
