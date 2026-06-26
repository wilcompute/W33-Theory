#!/usr/bin/env python3
"""BT1819: tuple-list pass/fail harness for the quartet fibre law.

Usage:
  python analysis/bt1819_tuple_list_pass_fail_harness.py path/to/tuple_rows.json

Accepted input formats:
  1. JSON list of records with a table/label field such as {"table":"T010"}.
  2. JSON object containing a "rows" list in the same format.
  3. JSON object containing explicit "counts" keyed by table labels.

The harness does not fabricate tuple rows.  It checks whether future true BT1781
materialized tuple lists satisfy the BT1817 contract.
"""
from __future__ import annotations
import argparse, json
from collections import Counter
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "bt1819_tuple_list_pass_fail_harness_schema.json"
TABLES = ['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
EXPECTED = np.array([528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560], dtype=int)
CORRECTION = {'T010': -2, 'T210': -2, 'T222': 2}
F2 = np.array([[1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1]], dtype=int)
F3 = np.array([[1,0,0,1,2,0,2,0,0,0,0,2,0,1,0,0,0,0],[2,0,0,1,1,0,2,0,2,0,0,0,0,0,1,0,0,0],[0,0,2,0,0,2,0,1,0,1,2,0,0,0,0,1,0,0],[1,0,2,2,0,2,0,1,0,2,1,0,0,0,0,0,1,0],[2,2,1,1,1,1,2,1,2,1,0,0,1,0,1,1,0,1]], dtype=int)

def extract_counts(obj):
    if isinstance(obj, dict) and "counts" in obj:
        counts_obj = obj["counts"]
        if isinstance(counts_obj, dict):
            return Counter({t: int(counts_obj.get(t,0)) for t in TABLES})
        if isinstance(counts_obj, list):
            return Counter({t: int(v) for t,v in zip(TABLES, counts_obj)})
    rows = obj.get("rows", obj) if isinstance(obj, dict) else obj
    if not isinstance(rows, list):
        raise ValueError("expected list of rows, object with rows, or object with counts")
    c = Counter()
    for row in rows:
        if isinstance(row, str):
            lab = row
        elif isinstance(row, dict):
            lab = row.get("table") or row.get("label") or row.get("table_label")
        else:
            lab = None
        if lab not in TABLES:
            raise ValueError(f"missing/unknown table label in row: {row!r}")
        c[lab] += 1
    return c

def evaluate(counts):
    vec = np.array([counts.get(t,0) for t in TABLES], dtype=int)
    delta = np.zeros(len(TABLES), dtype=int)
    for t,v in CORRECTION.items():
        delta[TABLES.index(t)] = v
    adjusted = vec + delta
    return {
        "input_total": int(vec.sum()),
        "counts_vector": vec.tolist(),
        "matches_expected_9980_vector": bool(np.array_equal(vec, EXPECTED)),
        "observed_syndromes": {"F2": (F2 @ vec % 2).astype(int).tolist(), "F3": (F3 @ vec % 3).astype(int).tolist()},
        "correction_vector": delta.tolist(),
        "correction_syndromes": {"F2": (F2 @ delta % 2).astype(int).tolist(), "F3": (F3 @ delta % 3).astype(int).tolist()},
        "adjusted_total": int(adjusted.sum()),
        "adjusted_syndromes": {"F2": (F2 @ adjusted % 2).astype(int).tolist(), "F3": (F3 @ adjusted % 3).astype(int).tolist()},
        "passes_BT1817_contract": bool(np.array_equal(vec, EXPECTED) and np.all((F2 @ adjusted) % 2 == 0) and np.all((F3 @ adjusted) % 3 == 0))
    }

def write_schema():
    payload = {
        "bt": "BT1819",
        "title": "tuple-list pass/fail harness",
        "status": "harness_ready_no_true_tuple_list_embedded",
        "expected_tables": TABLES,
        "expected_counts": {t: int(v) for t,v in zip(TABLES, EXPECTED)},
        "expected_total": int(EXPECTED.sum()),
        "oriented_quartet_correction": CORRECTION,
        "pass_contract": [
            "input tuple rows/counts reproduce the 9980 vector exactly",
            "apply the oriented quartet correction T010=-2, T210=-2, T222=+2",
            "F2 left-kernel evaluations vanish after correction",
            "F3 left-kernel evaluations vanish after correction"
        ],
        "accepted_input_formats": [
            "list of records with table/label/table_label",
            "object with rows list",
            "object with counts dict or counts list in TABLES order"
        ],
        "boundary": "The harness is committed without true BT1781 tuple rows. It must be run on real materialized tuple data, not on fabricated counts."
    }
    DEFAULT_OUT.parent.mkdir(parents=True, exist_ok=True)
    DEFAULT_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    return payload

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="tuple-list/count JSON to validate")
    ap.add_argument("--out", help="optional output JSON path")
    args = ap.parse_args()
    if not args.input:
        payload = write_schema()
        print(json.dumps({"status": payload["status"], "schema": str(DEFAULT_OUT)}, indent=2))
        return 0
    obj = json.loads(Path(args.input).read_text())
    result = evaluate(extract_counts(obj))
    if args.out:
        Path(args.out).write_text(json.dumps(result, indent=2, sort_keys=True))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passes_BT1817_contract"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
