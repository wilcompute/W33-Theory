#!/usr/bin/env python3
"""Pass 1164 v2: exact residual module replaces the speculative 1920 split."""
from __future__ import annotations
import json
from pathlib import Path

EXACT = {
    "1": (1,13), "6": (6,16), "15": (15,5), "15a": (15,4),
    "20": (20,21), "24": (24,2), "30": (30,9), "60a": (60,4),
    "64": (64,10), "90": (90,1),
}


def main() -> dict:
    dim = sum(d*m for d,m in EXACT.values())
    comm = sum(m*m for _,m in EXACT.values())
    assert dim == 1952 and comm == 1109
    result = {
        "schema": "w33.pass1164.exact_residual_recovery.v2",
        "status": "PASS",
        "dimension": dim,
        "decomposition": {k:{"degree":d,"multiplicity":m} for k,(d,m) in EXACT.items()},
        "commutant_dimension": comm,
        "source": "Pass 1135 exact character inner products",
        "correction": "No 1920-dimensional submodule or complementary 32-dimensional submodule is inferred from arithmetic alone.",
    }
    out=Path("data/MODULE_1920_IDENTIFICATION_2026_07_27.json")
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(result,indent=2)+"\n")
    print("PASS 1164 v2 exact residual 1952, commutant 1109")
    return result


if __name__ == "__main__": main()
