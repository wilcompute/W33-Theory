#!/usr/bin/env python3
"""Fail-closed compatibility shim for the retracted k=9 A5/Hecke chain."""
from __future__ import annotations

import json
from pathlib import Path

REPLACEMENT_SCRIPT = "analysis/w33_pass1315_1319_exact_frontiers.py"
REPLACEMENT_CERTIFICATE = "data/w33_pass1315_1319_exact_frontiers.json"


def emit_retraction(old_artifact: str, out: Path) -> dict:
    result = {
        "schema": "w33.k9_retraction.v1",
        "status": "RETRACTED",
        "old_artifact": old_artifact,
        "reason": "The proposed fixed-point vector (432,4,0,1,1) has Burnside value 43/5, not 9. The literal carrier has 26 A5/S5 orbitals.",
        "replacement": {
            "orbit_count": 26,
            "script": REPLACEMENT_SCRIPT,
            "certificate": REPLACEMENT_CERTIFICATE,
            "exact_hecke_release": "analysis/w33_pass1302_a5_s5_hecke_equality.py",
        },
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"RETRACTED {old_artifact}: use Passes 1302 and 1315-1319")
    return result
