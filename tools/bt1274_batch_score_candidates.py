#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GLOB = "examples/bt1269_*candidate.json"


def score_one(path: Path):
    out = subprocess.check_output([sys.executable, str(ROOT / "tools" / "bt1272_score_candidate.py"), str(path)], cwd=ROOT, text=True)
    return json.loads(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pattern", default=DEFAULT_GLOB)
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1274_batch_candidate_scores_summary.json")
    ns = ap.parse_args()
    paths = sorted(ROOT.glob(ns.pattern))
    rows = [score_one(p) for p in paths]
    counts = {}
    for row in rows:
        counts[row["band"]] = counts.get(row["band"], 0) + 1
    result = {
        "bt": 1274,
        "title": "Batch candidate scoring",
        "pattern": ns.pattern,
        "candidate_count": len(rows),
        "band_counts": counts,
        "rows": rows
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt":1274, "candidate_count":len(rows), "band_counts":counts, "out":str(ns.out)}, indent=2))


if __name__ == "__main__":
    main()
