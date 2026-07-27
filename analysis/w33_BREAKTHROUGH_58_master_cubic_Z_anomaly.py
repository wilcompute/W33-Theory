#!/usr/bin/env python3
"""RETRACTED shifted-adjacency descendant.

The exact historical source remains recoverable from Git blob
957d0d2134cf1a057d165c199a91644d2ff5b5a5 and the pre-retraction history.
"""
from __future__ import annotations
import json

RETRACTION = {
    "audit_tag": "{shifted-adjacency:retracted}",
    "status": "RETRACTED",
    "historical_blob_sha": "957d0d2134cf1a057d165c199a91644d2ff5b5a5",
    "false_spectrum": {"-7": 6, "-1": 16, "5": 10},
    "correct_spectrum": {"11": 1, "1": 24, "-5": 15},
    "correction": "analysis/2026-07-27_shifted_adjacency_spectral_erratum.md",
    "verifier": "analysis/w33_shifted_adjacency_spectral_audit.py",
}


def main() -> None:
    print(json.dumps(RETRACTION, indent=2))
    raise SystemExit("RETRACTED: run analysis/w33_shifted_adjacency_spectral_audit.py")


if __name__ == "__main__":
    main()
