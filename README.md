# Health-maxxer

NY hackathon, submission 5pm ET, 2026-10-11.

**Challenge:** Health-maxxing. Tap into supply chain and estimate microplastic and other negative materials/chemicals/processes.

**Pitch:** scan a food product, infer its supply chain (ingredients, packaging, processing, origin), and return a **relative risk tier with an uncertainty band and provenance**, plus a lower-risk swap.

Docs:
- [docs/methods.md](docs/methods.md): estimation methods and why they hold up
- [docs/data-check.md](docs/data-check.md): falsify-first data coverage results (2026-10-11)
- [docs/demo-and-fallbacks.md](docs/demo-and-fallbacks.md): demo location/product, offline fallback, sparse-data tier plan

Layout:

| Path | What |
|---|---|
| `data/plasticlist/plasticlist.tsv` | PlasticList lab results: 618 samples, 236 US products, 173 cols |
| `data/fccmigex/S112_FCCMIGEX.csv` | FCCmigex chemical list (NORMAN S112): 5,063 food-contact migrants |
| `data/off-samples/*.json` | Open Food Facts top-100 samples: waters, canned-foods, coffees, teas |
| `scripts/off_cov.py` | OFF field-coverage sampler |

Running the OFF script on this Mac needs the certifi CA bundle:

```sh
export SSL_CERT_FILE=$(python3 -c "import certifi;print(certifi.where())")
python3 scripts/off_cov.py waters coffees
```

OFF API etiquette: send a User-Agent, keep search calls to about 10/min (it rate-limits and returns non-JSON).
