#!/usr/bin/env python3
"""Execute pending BT1208--BT1210 materialization scripts.

This runner is meant for a real repository checkout with archive/bundle files
available. It materializes:
  * BT1208 raw/canonical Z2 vs packet-local S3 contingency table;
  * BT1209 isomorphism-dependence sample;
  * BT1210 half-fiber table schema file.

The full BT748 51840-row presentation-pair table still requires instrumenting
BT748 with the snippet emitted by BT1210; this runner records the schema and
status, not the full table.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT1211_EXECUTION_SUMMARY.json"

COMMANDS = [
    [sys.executable, "analysis/bt1208_raw_z2_s3_contingency_table_writer.py"],
    [sys.executable, "analysis/bt1209_isomorphism_dependence_sampler.py", "--max-isomorphisms", "64"],
    [sys.executable, "analysis/bt1210_bt748_half_fiber_table_generator.py"],
]


def main() -> int:
    results = []
    for cmd in COMMANDS:
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        results.append({
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        })
        if proc.returncode != 0:
            break
    payload = {
        "bt": 1211,
        "title": "BT1208-BT1210 execution summary",
        "results": results,
        "all_returncodes_zero": all(r["returncode"] == 0 for r in results) and len(results) == len(COMMANDS),
        "expected_outputs": [
            "data/PART_BT1208_RAW_Z2_S3_CONTINGENCY_TABLE_results.json",
            "data/PART_BT1209_ISOMORPHISM_DEPENDENCE_SAMPLE_results.json",
            "data/PART_BT1210_BT748_HALF_FIBER_TABLE_SCHEMA.json",
        ],
        "bt748_full_table_boundary": "full 51840-row presentation-pair table still requires instrumented BT748 run",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["all_returncodes_zero"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
