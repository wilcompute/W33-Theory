#!/usr/bin/env python3
"""Pass 4534 (outside the box) -- local edge tomography saturates the unique 9-layer.

Pass 4513 identifies the protected 240-set with vectors A_*(e_i+e_j) for
adjacent dual-W33 line pairs.  Their full span has dimension 9, not 10.  By
Pass 4496 the protected H10 module has unique invariant-submodule lattice
0<1<9<10, so this PSp-invariant edge-image span is exactly the unique
9-dimensional submodule.

The striking local result is stronger: the 24 protected edges entirely inside
the 13-line Borel gauge cell already span this full 9-space, and even the 12
spokes from the fixed center line do so.  Nine explicitly listed spokes are a
basis.  Therefore the local cell is information-complete for the protected
edge orbit, while the edge orbit itself provably misses the final 1D quotient
of H10.
"""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import numpy as np

from w33_apartment_section_core import build_geometry, rank2

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS4534_LOCAL_EDGE_TOMOGRAPHY_NINE_LAYER.json"


def main() -> int:
    _pts, _pidx, _lines, _lidx, _Ap, Astar, *_ = build_geometry()
    assert rank2(Astar) == 10
    center = 0
    S = {center} | set(int(x) for x in np.flatnonzero(Astar[center]))
    assert len(S) == 13

    edges = [(i,j) for i in range(40) for j in range(i+1,40) if Astar[i,j]]
    assert len(edges) == 240
    def image(e):
        return (Astar[:,e[0]] ^ Astar[:,e[1]]).astype(np.uint8)
    def erank(es):
        return rank2(np.asarray([image(e) for e in es], dtype=np.uint8)) if es else 0

    internal = [e for e in edges if e[0] in S and e[1] in S]
    boundary = [e for e in edges if (e[0] in S) ^ (e[1] in S)]
    exterior = [e for e in edges if e[0] not in S and e[1] not in S]
    spokes = [e for e in internal if center in e]
    tangential = [e for e in internal if center not in e]
    assert (len(internal),len(boundary),len(exterior),len(spokes),len(tangential)) == (24,108,108,12,12)

    ranks = {
        "all_240_edges": erank(edges),
        "internal_24": erank(internal),
        "boundary_108": erank(boundary),
        "exterior_108": erank(exterior),
        "center_spokes_12": erank(spokes),
        "internal_tangential_12": erank(tangential),
    }
    assert ranks == {
        "all_240_edges": 9, "internal_24": 9, "boundary_108": 9,
        "exterior_108": 8, "center_spokes_12": 9, "internal_tangential_12": 8,
    }

    basis = None
    for comb in itertools.combinations(spokes, 9):
        if erank(comb) == 9:
            basis = comb; break
    assert basis is not None
    # No set of fewer than 9 vectors can span a 9-space; the explicit 9-set is minimal.

    c4496 = json.loads((ROOT / "data/PART_W33_PASS4496_H10_EXTENSION_COHOMOLOGY.json").read_text())
    assert c4496["module"]["dimension"] == 10
    assert c4496["module"]["invariant_submodule_lattice"] == "0 < 1 < 9 < 10"
    assert c4496["module"]["uniserial"] is True

    out = {
        "pass": 4534,
        "protected_H10_dimension": 10,
        "edge_image_span_dimension": 9,
        "module_identification": "The PSp-invariant span of all 240 edge images is the unique 9-dimensional invariant submodule in H10=1|8|1.",
        "local_ranks": ranks,
        "minimal_local_spoke_basis_size": 9,
        "one_nine_spoke_basis": [list(map(int,e)) for e in basis],
        "local_completeness": "The 13-line Borel cell, and already its 12 center spokes, span every vector obtainable from the protected 240-edge orbit.",
        "missing_direction": "The edge-image family is codimension one in H10, so no combination of protected edge vectors reaches the top 1D quotient H10/V9.",
        "theorem": "Protected edge tomography is completely local to one Borel cell but intrinsically 9-dimensional: nine local spokes generate the unique 9-layer of H10, while the tenth protected direction lies outside the entire 240-edge carrier.",
        "boundary": "This is linear-algebraic information completeness for the finite protected edge family, not physical state tomography, a measurement protocol, or a fault-tolerance claim."
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
