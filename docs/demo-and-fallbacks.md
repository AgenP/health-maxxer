# Demo, fallbacks, sparse-data plan

## Demo location: NYC / US

The judges are in NY, and the measured datasets (PlasticList, USDA PDP, FDA PFAS) are US. Backup: France/EU, which has the densest Open Food Facts packaging data.

## Demo product: a Starbucks order

Recognisable, in PlasticList, with real spread (DEHP-equivalents, ng/serving):

| Item | Samples |
|---|---|
| Nescafé instant coffee powder | ~195 (lowest coffee) |
| Birthday Cake Pop | 646, 798, 798 |
| Chocolate Croissant (warmed) | 1,840 to 2,560 |
| Spinach Feta Wrap (warmed) | 3,498 / 12,084 / 23,691 (7× spread: heat + plastic story) |
| Caramel Frappuccino, Nitro Cold Brew, Matcha Latte | ~32k to 55k (**check the LOQ artifact first**, see data-check.md) |

Script:
1. Scan a measured item: T1, lab data, tight band.
2. Scan an unmeasured item: T2/T3 inference from category + packaging + heated, wider band, provenance shown.
3. "Swap to X" suggestion.

## Offline fallback

Cache about 20 demo products (OFF records + PlasticList rows) as JSON in the repo, so the demo runs with no API or wifi.

## Sparse-data tier plan

Each step down uses a broader estimate and widens the band.

| Tier | Source | Band | UI badge |
|---|---|---|---|
| T1 | Lab-measured (PlasticList barcode/name match) | Lab range | Lab-measured |
| T2 | Similar product (category + packaging + heated?) | ~2× | Inferred: similar products |
| T3 | Category prior (PlasticList category median, NOVA, packaging migration multiplier) | ~3× | Inferred: category |
| T4 | Country adjustment (OWID pesticide use/ha, mismanaged plastic per capita, FDA import refusals) | Shifts tier by at most ±1 | Origin estimate |
| T5 | Global prior | Wide | "Unknown: here's what would tell us" |

Rules:
- LLM fills missing packaging/origin from name or photo; those fields are badged "inferred".
- Combine evidence on a log scale (log-normal intervals); when tiers disagree, take the wider interval.
- Never show a point estimate below T2.
- Always list the missing inputs.
- State it is relative risk, not a safety or toxicity verdict.

## Validation slide

Predict PlasticList rank (ng/g) from category + packaging + heated only, leave-one-out, report Spearman ρ.
