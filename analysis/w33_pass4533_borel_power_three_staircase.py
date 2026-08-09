#!/usr/bin/env python3
"""Pass 4533 (outside the box) -- Borel power-of-three orbit staircase.

The Pass-4532 decomposition has a rigid arithmetic shape not used in its proof:
line vertices split 1,3,9,27 and protected edges split into two copies of
3,9,27,81.  This pass freezes that exact power-of-three staircase together
with stabilizer orders 54,18,6,2.

The result is presented as an orbit-filtration fact.  We do not identify the
exponent with physical scale, energy, time, or a Bruhat length without an
additional theorem.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4533_BOREL_POWER_THREE_STAIRCASE.json"


def main() -> int:
    c = json.loads((ROOT / "data/PART_W33_PASS4532_BOREL_EDGE_LOCAL_CELL_FUSION.json").read_text())
    v = c["line_vertex_orbit_sizes"]
    e = [r["orbit_size"] for r in c["protected_edge_orbits"]]
    st = [r["stabilizer_order_in_Borel"] for r in c["protected_edge_orbits"]]
    assert v == [1,3,9,27]
    assert e == [3,3,9,9,27,27,81,81]
    assert st == [54,54,18,18,6,6,2,2]
    powers = {1:0,3:1,9:2,27:3,81:4}
    assert all(x in powers for x in v+e)
    edge_exponents = [powers[x] for x in e]
    assert Counter(edge_exponents) == {1:2,2:2,3:2,4:2}

    shells = []
    for k in range(1,5):
        rows = [r for r in c["protected_edge_orbits"] if r["orbit_size"] == 3**k]
        shells.append({
            "exponent": k,
            "orbit_size": 3**k,
            "number_of_edge_orbits": len(rows),
            "Borel_stabilizer_order": 162 // (3**k),
            "cell_locations": sorted(r["cell_location"] for r in rows),
            "representatives": [r["representative"] for r in rows],
        })

    out = {
        "pass": 4533,
        "vertex_staircase": {"orbit_sizes": v, "identity": "1+3+9+27=40"},
        "edge_staircase": {"orbit_sizes": e, "identity": "2*(3+9+27+81)=240", "shells": shells},
        "stabilizer_staircase": [54,18,6,2],
        "theorem": "The canonical Borel action organizes all 40 line vertices into one orbit of each size 3^0..3^3 and all 240 protected edges into exactly two orbits of each size 3^1..3^4, with stabilizers dropping by a factor three at every edge shell.",
        "interpretation": "This is an exact finite orbit filtration naturally aligned with the order-81 unipotent core of the Borel; the certificate records the arithmetic hierarchy without assigning it a physical scale variable.",
        "boundary": "Power-of-three orbit sizes are exact. A Bruhat-length, renormalization, causal-depth, or energy-scale interpretation would require a separate intertwiner/dynamics theorem."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
