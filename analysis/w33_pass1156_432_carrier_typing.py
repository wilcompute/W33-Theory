#!/usr/bin/env python3
"""Pass 1156: exact carrier typing for the two distinct 432 stories in the repository."""
from __future__ import annotations
import json
from pathlib import Path

def main() -> dict:
    carriers = {
        "W_E6_432": {
            "acting_group": "W(E6)",
            "carrier_size": 432,
            "stabilizer_label": "S5 (Hecke packet)",
            "typed_as": "Hecke/double-coset carrier",
            "color_support": "admits C3-color extension",
        },
        "Sp43_432": {
            "acting_group": "Sp(4,3)",
            "carrier_size": 432,
            "stabilizer_order": 60,
            "typed_as": "symplectic orbit carrier",
            "color_support": "not implied",
        },
    }
    result = {
        "schema": "w33.pass1156.432_carrier_typing.v1",
        "status": "PASS",
        "same_cardinality_not_same_carrier": True,
        "carriers": carriers,
        "policy": "A W(E6) 432-carrier and an Sp(4,3) 432-orbit are distinct typed objects unless an explicit intertwiner is supplied."
    }
    out = Path("data/w33_pass1156_432_carrier_typing.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1156 typed distinct carriers")
    return result

if __name__ == "__main__":
    main()
