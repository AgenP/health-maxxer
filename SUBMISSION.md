# Health-Maxxing (Health OS): AI Engineer NYC 2026 submission

**Repo:** https://github.com/AgenP/health-maxxer

## What it does
Plastic and chemical exposure can damage our health. Snap a quick pic of what you're eating or drinking and in about 5 seconds get an estimate of plastic-chemical exposure, how strong the evidence is, how it compares to official reference levels, and a lower-exposure alternative where the data supports one. It's the first live module of a personal Health OS (bloodwork, sleep, and gym & nutrition are on the roadmap).

## How it works
1. **See:** Claude Opus 5.5 reads the photo into structured facts (brand, packaging, heated or not), shown as editable chips.
2. **Match:** an estimate engine matches it against 618 lab samples from 236 products (PlasticList), falling back to similar products, then the category.
3. **Estimate:** a relative tier with an uncertainty band and an evidence tier (T1 lab-measured, T2 similar products, T3 category, T5 unknown), compared against reference levels (EFSA, EPA, NYC DEP).
4. **Swap:** a lower-exposure option with its impact and evidence label.

## How we checked it
- Photo extraction eval on 71 labelled images: packaging read correctly on 17/17 product photos and 23/26 real-world snaps after correcting label errors; no confident wrong packaging calls. About 5 s and $0.03 per photo.
- 21 automated tests on the estimate engine and request handling.
- Every cited figure in the app links to its primary source.

## Known limitations
- Estimates are relative, not safety verdicts. A "higher" food can still be well under 1% of the EU tolerable daily intake; the card says so.
- Lab data is US-only (PlasticList, Bay Area samples). No lab data for NYC tap water, and microplastics have no official reference level.
- Product-name matching can produce false lab matches on short names (e.g. "Starbucks latte" matching "Starbucks Matcha Latte"). Fix: require all distinguishing words to match.
- User research so far is a self-interview only; all user needs are labelled as assumptions.
- Next: run our own lab studies, then add bloodwork to see whether swaps change what's in your body.

## AI tools used
- **Claude Code** (Claude Opus 5.5): research, design, code, tests, evals, pitch deck and video edit.
- **Claude Opus 5.5 via the Anthropic API:** live photo understanding in the app.
- **Whisper (mlx-whisper large-v3-turbo):** transcribing the demo video for editing.

## Data and image credits
- Lab data: PlasticList, https://www.plasticlist.org/report
- Reference levels: EFSA 2019 (https://doi.org/10.2903/j.efsa.2019.5838), US EPA PFAS rule, NYC DEP 2025 Drinking Water Supply and Quality Report; bottled vs tap: Mason et al. 2018 (https://doi.org/10.3389/fchem.2018.00407)
- Demo photo 1: "Starbucks Grande Iced Pumpkin Spice Latte" by JimmyStardust, CC BY-SA 4.0, https://commons.wikimedia.org/wiki/File:Starbucks_Grande_Iced_Pumpkin_Spice_Latte.jpg
- Demo photo 2: "New BPC Gym water filtration system" by Airman 1st Class Kylie Barrow, public domain, https://commons.wikimedia.org/wiki/File:New_BPC_Gym_water_filtration_system_(1).jpg
- Eval photos: Wikimedia Commons and Open Food Facts; per-image credits in `evals/image-capture/images/*/ATTRIBUTION.md`.
