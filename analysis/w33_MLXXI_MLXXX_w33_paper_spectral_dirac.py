#!/usr/bin/env python3
"""RETRACTED IN PART: mixed shifted-adjacency synthesis descendant.

The exact historical source remains recoverable from Git blob
0412d1344d92eb0a92b030ff8ed8bf94a1d5ab35.
Only MLXXII--MLXXV and MLXXX are retracted here.  The remaining sections are
quarantined from execution but not adjudicated by this spectral correction.
"""
from __future__ import annotations
import json

RETRACTION = {
    "audit_tag": "{shifted-adjacency:retracted}",
    "status": "RETRACTED_IN_PART",
    "historical_blob_sha": "0412d1344d92eb0a92b030ff8ed8bf94a1d5ab35",
    "false_spectrum": {"-7": 6, "-1": 16, "5": 10},
    "correct_spectrum": {"11": 1, "1": 24, "-5": 15},
    "retracted_sections": [
        "MLXXII_master_cubic",
        "MLXXIII_spectral_democracy",
        "MLXXIV_Z_taylor",
        "MLXXV_trace_tower",
        "MLXXX_meta",
    ],
    "not_adjudicated_here": [
        "MLXXI_equipartition",
        "MLXXVI_PMNS_sum_rule",
        "MLXXVII_jarlskog",
        "MLXXVIII_H0_simple",
        "MLXXIX_cosmology",
    ],
    "correction": "analysis/2026-07-27_shifted_adjacency_spectral_erratum.md",
    "verifier": "analysis/w33_shifted_adjacency_spectral_audit.py"
}


def main() -> None:
    print(json.dumps(RETRACTION, indent=2))
    raise SystemExit(
        "RETRACTED IN PART: shifted-adjacency sections "
        "MLXXII-MLXXV and MLXXX are invalid"
    )


if __name__ == "__main__":
    main()
