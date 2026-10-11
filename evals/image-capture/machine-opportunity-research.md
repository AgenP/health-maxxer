# Office water machine: research notes (2026-10-11, quick pass)

## (a) NSF/ANSI microplastics claims
- The microplastics claim lives in **NSF/ANSI 401**, which reuses the **NSF/ANSI 42 Class I particulate** test method. Credit is based on **0.5-1 µm** particles, with roughly 85%+ reduction required (the threshold is UNVERIFIED). Your belief checks out. https://wcponline.com/2022/01/14/update-on-microplastics-reduction-claims/
- An example A.O. Smith sheet shows "microplastics 0.5-<1 µm, 97.3% min". https://www.aosmithatlowes.com/media/1763/ao-mf-pds-2023.pdf
- **53** covers health contaminants such as lead and cysts. **58** covers RO. Whether either standard carries a microplastics claim of its own is UNVERIFIED (probably not). RO is physically finer than 0.5 µm.
- Gap: microplastics are usually defined as 1 µm-5 mm. Nanoplastics below 0.5 µm are not tested.

## (b) Evidence
- **PC 5-gal jugs:** in a UAE study (40 jugs), BPA rose over 30 days and was highest outdoors and in heat (about 9 µg/L). https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11396560/
- A Turkish carboy study found migration rose with temperature (5-40 °C), time (60 d) and sunlight, but stayed under the SML. https://akademikarsiv.cbu.edu.tr/items/32edd3de-0f28-45d1-9420-f564f412d865
- **Mason et al. 2018 (Orb/Fredonia):** 259 bottles, 93% contaminated. About 10.4 particles/L were >100 µm, and the mean including smaller particles was about 325/L. https://www.smithsonianmag.com/smart-news/study-finds-microplastics-more-90-percent-tested-water-bottles-2-180968507/
- **Qian et al. 2024 PNAS:** about 2.4e5 particles/L in bottled water, about 90% of them nanoplastics. These figures are from memory, not fetched: UNVERIFIED.
- **No dispenser- or office-cooler-specific study was found.** A ConsumerLab test found one pitcher filter *added* particles. https://consumerlab.com/answers/water-filters-for-microplastics/water-filters

## (c) Spec sheets
- **Elkay: yes.** WaterSentry 51300C, 51600C and 71300C are NSF 42/53/401 (microplastics), and model-number spec PDFs exist. https://www.elkay.com/content/dam/elkayv2/project-types/education/michigan-legislation/filter-first-compliant-filters.pdf
- **Primo, Culligan, Brita/Zip and Waterlogic:** not checked; UNVERIFIED. Expect POU units to list filter stages, but certifications may sit on the cartridge rather than the machine.

## (d) NYC DEP report
The annual report is usable for the regulated baseline: lead, DBPs and the rest. A microplastics test was not found; it is probably absent (UNVERIFIED, so grep the PDF). Building plumbing is not covered. https://a860-gpp.nyc.gov/concern/nyc_government_publications/qv33rx85v?locale=en

## (e) Proposed rule table (relative tier)
| machine_type | filtration | jug_material | tier |
|---|---|---|---|
| bottle_top_cooler_with_jug | none | polycarbonate | high (BPA + MP; worse if sunlit/warm) |
| bottle_top / bottom_load | none | pet / other_plastic | med-high |
| bottle_top / bottom_load | none | glass | med (plastic reservoir/lines remain) |
| plumbed_point_of_use | RO (58) | none | low |
| plumbed_point_of_use / bottle_filling_station | 401-certified carbon | none | low-med |
| plumbed_point_of_use / bottle_filling_station / fridge_dispenser | unknown or expired | none | med (tap baseline) |
| drinking_fountain | none | none | med (tap baseline) |
| countertop_filter | 401 | none | low-med (plastic housing) |

**A photo can tell:** machine type, jug presence, jug colour and tint (blue rigid = likely PC; the resin code #7 is visible only up close), brand/model badge, a filter-status light, and sun exposure or a nearby heater.

**A photo cannot tell:** filter age or certification, internal tubing and reservoir material, the jug's reuse count, water temperature history, or the actual particle load.
