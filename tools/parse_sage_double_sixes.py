#!/usr/bin/env python3
"""Parse and summarize `artifacts/sage_double_sixes.json` produced by `tools/sage_double_sixes.py`.

Writes `artifacts/sage_double_sixes_summary.json` with line-count and sample lines.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "artifacts" / "sage_double_sixes.json"
OUT = ROOT / "artifacts" / "sage_double_sixes_summary.json"

if not P.exists():
    print("No sage_double_sixes.json found; nothing to parse")
    raise SystemExit(1)

data = json.loads(P.read_text(encoding="utf-8"))
lines = data.get("lines") or []
summary = {
    "n_lines": len(lines),
    "sample_lines": [l.get("repr")[:200] for l in lines[:20]],
}
OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("Wrote", OUT)
