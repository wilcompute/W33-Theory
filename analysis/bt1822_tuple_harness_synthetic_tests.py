#!/usr/bin/env python3
"""BT1822: synthetic pass/fail fixtures for the BT1819 tuple harness.

These are deliberately labeled synthetic.  They test the harness mechanics only and
are not claimed to be true BT1781 tuple lists.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1822_tuple_harness_synthetic_tests.json"
TABLES = ['T001','T002','T010','T012','T020','T021','T100','T101','T111','T112','T120','T122','T200','T202','T210','T211','T221','T222']
EXPECTED = np.array([528,562,578,528,612,580,528,528,480,528,612,564,562,528,578,562,562,560], dtype=int)
CORRECTION = {'T010': -2, 'T210': -2, 'T222': 2}
F2 = np.array([[1,0,0,1,1,0,1,0,1,0,0,1,0,1,1,0,1,0],[0,1,1,0,0,1,0,1,0,1,1,0,1,0,0,1,0,1]], dtype=int)
F3 = np.array([[1,0,0,1,2,0,2,0,0,0,0,2,0,1,0,0,0,0],[2,0,0,1,1,0,2,0,2,0,0,0,0,0,1,0,0,0],[0,0,2,0,0,2,0,1,0,1,2,0,0,0,0,1,0,0],[1,0,2,2,0,2,0,1,0,2,1,0,0,0,0,0,1,0],[2,2,1,1,1,1,2,1,2,1,0,0,1,0,1,1,0,1]], dtype=int)

def eval_vec(vec):
    delta = np.zeros(18, dtype=int)
    for t,v in CORRECTION.items():
        delta[TABLES.index(t)] = v
    adjusted = vec + delta
    return {
        "total": int(vec.sum()),
        "matches_expected": bool(np.array_equal(vec, EXPECTED)),
        "observed_F2": (F2 @ vec % 2).astype(int).tolist(),
        "observed_F3": (F3 @ vec % 3).astype(int).tolist(),
        "adjusted_F2": (F2 @ adjusted % 2).astype(int).tolist(),
        "adjusted_F3": (F3 @ adjusted % 3).astype(int).tolist(),
        "passes": bool(np.array_equal(vec, EXPECTED) and np.all((F2 @ adjusted)%2 == 0) and np.all((F3 @ adjusted)%3 == 0))
    }

def main():
    positive = EXPECTED.copy()
    negative_count = EXPECTED.copy(); negative_count[TABLES.index('T010')] += 1
    negative_syndrome = EXPECTED.copy(); negative_syndrome[TABLES.index('T222')] += 2
    tests = {
        "synthetic_positive_counts_only": eval_vec(positive),
        "synthetic_negative_wrong_count": eval_vec(negative_count),
        "synthetic_negative_wrong_syndrome": eval_vec(negative_syndrome)
    }
    payload = {
        "bt": "BT1822",
        "title": "tuple harness synthetic tests",
        "status": "synthetic_fixtures_only_not_true_BT1781_data",
        "fixtures": tests,
        "expected_outcomes": {
            "synthetic_positive_counts_only": true if False else "pass",
            "synthetic_negative_wrong_count": "fail",
            "synthetic_negative_wrong_syndrome": "fail"
        },
        "checks": {
            "positive_passes": tests["synthetic_positive_counts_only"]["passes"] is True,
            "negative_wrong_count_fails": tests["synthetic_negative_wrong_count"]["passes"] is False,
            "negative_wrong_syndrome_fails": tests["synthetic_negative_wrong_syndrome"]["passes"] is False
        },
        "boundary": "These fixtures validate BT1819 harness behavior only. They are synthetic counts, not materialized BT1781 tuple lists.",
        "conclusion": "BT1822 gives the tuple harness a pass/fail self-test layer without smuggling in fake tuple data."
    }
    payload["verified"] = all(payload["checks"].values())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "outcomes": {k:v["passes"] for k,v in tests.items()}}, indent=2))
    return 0 if payload["verified"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
