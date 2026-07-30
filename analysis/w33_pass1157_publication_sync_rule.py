#!/usr/bin/env python3
"""Pass 1157: publication sync rule for all 432-carrier claims."""
from __future__ import annotations
import json
from pathlib import Path

REQUIRED_TAGS = [
    "acting_group",
    "stabilizer_label_or_order",
    "color_retained_or_forgotten",
]

def main() -> dict:
    result = {
        "schema": "w33.pass1157.publication_sync_rule.v1",
        "status": "PASS",
        "required_tags": REQUIRED_TAGS,
        "applies_to": [
            "432 orbit",
            "Steinberg bridge",
            "stabilizer statements",
            "colored/uncolored target claims",
        ],
        "policy": "Any publication claim about a 432-carrier must specify acting group, stabilizer label/order, and whether color is retained or forgotten."
    }
    out = Path("data/w33_pass1157_publication_sync_rule.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1157 tags", len(REQUIRED_TAGS))
    return result

if __name__ == "__main__":
    main()
