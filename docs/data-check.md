# Data check (falsify-first), 2026-10-11

Question: is there enough product-level data for a composition-based estimator, and enough measured data to validate it?

**Verdict: yes, with a fallback required for about half of products.**

## Open Food Facts: works, with gaps

Total products: ~984k tagged US, ~1.27M France (search API count, 2026-10-11).

Field fill rates, top-100 most-scanned per category (`data/off-samples/`):

| Category | Total | Packaging material | Any packaging | Origin | Ingredients | NOVA |
|---|---|---|---|---|---|---|
| Waters | 5,212 | 55% | 65% | 30% | 95% | 83% |
| Canned foods | 12,779 | 52% | 64% | 39% | 97% | 95% |
| Teas | 3,335 | 26% | 31% | 13% | 92% | 81% |
| Coffees | 1,058 | 14% | 20% | 12% | 75% | 56% |

Caveat: the `countries_tags_en=united-states` filter did not apply (Moroccan and French products came back), so these rates are roughly **global, not US-specific**. US packaging coverage is UNVERIFIED.

## PlasticList: downloaded, best validation set

- Source: https://www.plasticlist.org/ ("Download TSV", behind a disclaimer modal; curl gets only a JS shell, needed Playwright).
- 618 samples, 236 products, 173 columns. US, collected around the Bay Area (Whole Foods, Target, Safeway, Palo Alto).
- Chemicals: 13 phthalates incl. `DEHP_equivalents`; BPA, BPS, BPF; substitutes DEHT, DEHA, DINCH, DIDA.
- Units per chemical: ng/g, ng/serving, percentiles, %TDI (EPA and EFSA, 14 kg and 70 kg). Non-detects are strings like `<370` or `<LOQ`, so parse as censored values.
- Features: `tags` (comma list: groceries 180, beverages 135, fast_food 86, water 80, ... glass 21, plastic 14), `serving_size_g`, collection notes. `shipped_in` is how the sample travelled to the lab, not the product's packaging.
- **No packaging-type column:** hand-label about 50 products from names.

### Traps

1. **Same-product variance is huge.** Diet Coke: `<LOQ`, `<LOQ`, 292, 39,590 ng/serving DEHP-eq. Supports ranges over point estimates.
2. **Likely detection-limit artifact (inference, UNVERIFIED against their methods notes).** Many beverage values cluster at 35k–45k ng/serving, about 100 ng/g × a ~370 g serving. Rank on **ng/g** and treat near-LOQ values as censored, or the validation learns serving size, not contamination.

## FCCmigex: partial

- Downloadable: chemical list only (NORMAN S112, https://zenodo.org/records/15852269): 5,063 chemicals with name, CAS, DTXSID, SMILES, InChIKey. Saved to `data/fccmigex/`.
- The ~35,500 migration measurements (material, food type, amount) are in a Power BI dashboard (https://www.foodpackagingforum.org/fccmigex) with no export.
- Use as a "known food-contact migrant" flag, not for amounts.

## Other sources (from research agent, mostly UNVERIFIED)

- USDA Pesticide Data Program: https://www.ams.usda.gov/datasets/pdp (raw format unverified)
- FDA PFAS in food: https://www.fda.gov/food/chemicals/analytical-results-testing-food-pfas-environmental-contamination (~90 samples/dataset, mostly non-detects, seafood the main hit)
- OWID pesticide use per hectare: https://ourworldindata.org/grapher/pesticide-use-per-hectare-of-cropland (CSV export untested)
- OWID mismanaged plastic waste per capita: https://ourworldindata.org/grapher/mismanaged-plastic-waste-per-capita (ZIP with CSV)
- FDA import refusals: https://www.accessdata.fda.gov/scripts/importrefusals/ (no official bulk CSV)
- EFSA pesticide monitoring on Zenodo, e.g. https://zenodo.org/records/3254912 (origin column unverified)
- Not checked: Consumer Reports 2024 phthalate tests, bottled-water microplastic tables, PAN banned-pesticide list, Agribalyse.
