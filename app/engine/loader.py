import csv
from collections import defaultdict

from engine.core import Product, Sample


def _num(raw):
    raw = (raw or "").strip()
    if not raw or raw.startswith("<"):
        return None
    return float(raw)


def load_products(path):
    grouped = defaultdict(list)
    meta = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pid = row["product_id"]
            meta[pid] = (row["product"], tuple(t.strip() for t in row["tags"].split(",") if t.strip()))
            raw = row["DEHP_equivalents_ng_g"].strip()
            grouped[pid].append(Sample(
                ng_g=_num(raw),
                censored=raw.startswith("<"),
                pct_tdi=_num(row["DEHP_equivalents_percent_tdi_70_kg_efsa"]),
                serving_g=_num(row["serving_size_g"]),
            ))
    return {pid: Product(pid, meta[pid][0], meta[pid][1], tuple(s)) for pid, s in grouped.items()}
