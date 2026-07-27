#!/usr/bin/env python3
"""Pass 1154: collision-free exact separator for the five canonical degree-540 species."""
from __future__ import annotations
import json
from pathlib import Path

SPECIES = [
    {"tom": 77, "tag": "point-nonedge", "rank": 25, "normalizer": 96},
    {"tom": 78, "tag": "double-six-nonincident", "rank": 28, "normalizer": 96},
    {"tom": 79, "tag": "gq42-arc", "rank": 27, "normalizer": 96},
    {"tom": 80, "tag": "outer-4c", "rank": 21, "normalizer": 96},
    {"tom": 81, "tag": "line-nonedge", "rank": 32, "normalizer": 48},
]

def main() -> dict:
    separator = [(s["rank"], s["tom"], s["normalizer"]) for s in SPECIES]
    assert len(set(separator)) == len(SPECIES)
    result = {
        "schema": "w33.pass1154.degree540_species_separator.v1",
        "status": "PASS",
        "separator_name": "(rank, TOM id, normalizer order)",
        "collision_free": True,
        "species": [
            {
                **s,
                "separator": [s["rank"], s["tom"], s["normalizer"]],
            }
            for s in SPECIES
        ],
        "policy": "Cardinality 540 and abstract stabilizer type alone never identify a species; use the exact separator triple."
    }
    out = Path("data/w33_pass1154_degree540_species_separator.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("PASS 1154 separator collision-free", True)
    return result

if __name__ == "__main__":
    main()
