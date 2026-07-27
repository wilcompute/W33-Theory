#!/usr/bin/env python3
"""RETRACTED shifted-adjacency synthesis descendant.

The exact historical source remains recoverable from Git blob
0412d1344d92eb0a92b030ff8ed8bf94a1d5ab35.
"""
from __future__ import annotations
import json

RETRACTION = {
    "audit_tag": "{shifted-adjacency:retracted}",
    "status": "RETRACTED",
    "historical_blob_sha": "0412d1344d92eb0a92b030ff8ed8bf94a1d5ab35",
    "false_spectrum": {"-7": 6, "-1": 16, "5": 10},
    "correct_spectrum": {"11": 1, "1": 24, "-5": 15},
    "correction": "analysis/2026-07-27_shifted_adjacency_spectral_erratum.md",
    "verifier": "analysis/w33_shifted_adjacency_spectral_audit.py"
}


def main() -> None:
    print(json.dumps(RETRACTION, indent=2))
    raise SystemExit("RETRACTED: shifted-adjacency sections MLXXII-MLXXV and MLXXX are invalid")


if __name__ == "__main__":
    main()
