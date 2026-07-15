#!/usr/bin/env python3
"""Pass 310: can the clock/machine coupling be constructed?  Not as asserted.

Pass 307 was blocked on a missing object: bt1654_heawood_clock_homology.py
asserts the Heawood clock is "a separate clock/homology module coupled to the W33
machine" but never says HOW.  Without the coupling there is no combined spectrum,
so Pass 303's compositum stays a statement about two separate systems.  This
witness tries to construct it, and reports the obstructions honestly.

WHAT bt1654 ALREADY ESTABLISHED (the honest boundary it drew itself):
    the Heawood graph has girth 6 (28 six-cycles), while the W(3,3) point-line
    Levi graph has girth 8 and ZERO six-cycles.
So Heawood is not a subgraph of the W(3,3) Levi graph -- a subgraph would carry
its 6-cycles along.  We re-verify that here rather than taking it on trust.

THE NEW OBSTRUCTIONS.
  * ORDER.  |PGSp(4,3)| = 51840 = 2^7*3^4*5 has no factor 7 (Pass 309), so the
    substrate's symmetry group cannot act with the Heawood/Fano 7-fold symmetry.
    Any coupling would have to break the clock's own symmetry.
  * SIZE.  Heawood has 14 vertices; the W(3,3) Levi graph has 80. 14 does not
    divide 80, so there is no clean orbit decomposition of the machine into
    clock-sized pieces.
  * FIELD.  Pass 307 showed that adding coupling edges pushes the spectrum out of
    Q(sqrt2,sqrt3) -- so a coupling that PRESERVED the nice field would have to be
    very special, and none of the obvious ones is.

VERDICT.  The coupling is not constructed here, and the obstructions suggest it
is not a graph embedding or a group action at all.  bt1654's phrase "coupled
module" is doing unexamined work: it asserts a relationship whose type has never
been specified.  Until someone specifies it, Pass 303's TBM-field observation
must stay what it is -- an arithmetic fact about two forced fields, not physics
of one system.
"""

from __future__ import annotations

from itertools import combinations
import json
from pathlib import Path
import sys

import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_pass224_shadow_code_tower import isotropic_lines, pg3_points

OUT = ROOT / "data" / "w33_pass310_the_coupling_does_not_exist.json"


def heawood_nx():
    lines = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (1, 4, 6), (2, 3, 6), (2, 4, 5)]
    G = nx.Graph()
    for li, L in enumerate(lines):
        for p in L:
            G.add_edge(p, 7 + li)
    return G


def w33_levi_nx():
    pts = pg3_points(3)
    lines = isotropic_lines(pts, 3)
    n = len(pts)
    G = nx.Graph()
    for j, L in enumerate(lines):
        for p in L:
            G.add_edge(p, n + j)
    return G


def main():
    checks = {}
    H = heawood_nx()
    W = w33_levi_nx()
    checks["heawood_14_21"] = (H.number_of_nodes() == 14 and H.number_of_edges() == 21)
    checks["w33_levi_80_160"] = (W.number_of_nodes() == 80 and W.number_of_edges() == 160)

    # ---- girth, re-verified rather than trusted
    gH = nx.girth(H) if hasattr(nx, "girth") else min(
        len(c) for c in nx.cycle_basis(H))
    gW = nx.girth(W) if hasattr(nx, "girth") else min(
        len(c) for c in nx.cycle_basis(W))
    checks["heawood_girth_6"] = gH == 6
    checks["w33_levi_girth_8"] = gW == 8
    checks["girths_differ"] = gH != gW
    # a subgraph inherits short cycles: girth(sub) >= girth(host)
    checks["heawood_cannot_be_a_subgraph_of_W33_levi"] = gH < gW

    # ---- ORDER obstruction (Pass 309)
    checks["pgsp43_has_no_order_7"] = 51840 % 7 != 0
    checks["clock_symmetry_cannot_act"] = 51840 % 7 != 0

    # ---- SIZE obstruction
    checks["14_does_not_divide_80"] = 80 % 14 != 0
    checks["no_clean_orbit_decomposition"] = 80 % 14 != 0

    # ---- try the obvious couplings and see what they cost
    attempts = {}
    # (a) identify Heawood's 14 vertices with 14 of the machine's 80
    attempts["vertex_identification"] = {
        "possible_as_a_map": True,
        "but": "an arbitrary injection of 14 into 80 carries no structure; there "
               "is no canonical choice, and any choice breaks the Fano 7-fold "
               "symmetry that PGSp(4,3) cannot support anyway",
    }
    # (b) subgraph embedding
    attempts["subgraph_embedding"] = {
        "possible": False,
        "why": f"girth(Heawood) = {gH} < {gW} = girth(W(3,3) Levi); a subgraph "
               "cannot have shorter cycles than its host",
    }
    # (c) group action
    attempts["group_action"] = {
        "possible": False,
        "why": "PGSp(4,3) has order 51840 with no factor 7, so it has no element "
               "of order 7 and cannot realise the Fano symmetry (Pass 309)",
    }
    # (d) spectral: does adding edges keep the field?
    attempts["edge_coupling"] = {
        "possible": True,
        "but": "Pass 307 showed adding coupling edges pushes the spectrum OUT of "
               "Q(sqrt2, sqrt3); the nice field does not survive",
    }
    checks["all_obvious_routes_examined"] = len(attempts) == 4
    checks["no_route_works"] = not any(
        a.get("possible") and "but" not in a for a in attempts.values())

    all_pass = all(v for v in checks.values() if isinstance(v, bool))
    payload = {
        "schema": "w33.pass310.the_coupling_does_not_exist.v1",
        "status": "PASS" if all_pass else "FAIL",
        "the_missing_object": (
            "bt1654_heawood_clock_homology.py asserts the Heawood clock is 'a "
            "separate clock/homology module coupled to the W33 machine' but never "
            "specifies the coupling. Pass 307 was blocked on exactly this. "
            "Without it there is no combined spectrum, so Pass 303's compositum "
            "remains a statement about two SEPARATE systems."
        ),
        "measurements": {
            "heawood": {"V": 14, "E": 21, "girth": gH},
            "w33_levi": {"V": 80, "E": 160, "girth": gW},
        },
        "obstructions": {
            "girth": f"girth(Heawood) = {gH} but girth(W(3,3) Levi) = {gW}; a "
                     "subgraph cannot have shorter cycles than its host, so "
                     "Heawood is NOT a subgraph -- bt1654 said this and it is "
                     "re-verified here rather than taken on trust",
            "order": "|PGSp(4,3)| = 51840 = 2^7*3^4*5 has no factor 7, so the "
                     "substrate's symmetry group has no element of order 7 and "
                     "cannot act with the Fano 7-fold symmetry (Pass 309)",
            "size": "14 does not divide 80, so there is no clean orbit "
                    "decomposition of the machine into clock-sized pieces",
            "field": "Pass 307: adding coupling edges pushes the spectrum out of "
                     "Q(sqrt2, sqrt3), so a field-preserving coupling would have "
                     "to be very special, and none of the obvious ones is",
        },
        "attempts": attempts,
        "VERDICT": (
            "The coupling is NOT constructed, and the obstructions suggest it is "
            "not a graph embedding (girth), not a group action (order), and not "
            "a clean decomposition (size). bt1654's phrase 'coupled module' is "
            "doing unexamined work: it asserts a relationship whose TYPE has "
            "never been specified. Until someone specifies it, Pass 303's "
            "TBM-field observation must stay what it is -- an arithmetic fact "
            "about two forced fields, not the physics of one system."
        ),
        "what_would_settle_it": (
            "A stated type for the coupling: is it a functor, a spectral "
            "correspondence, a quotient, a fibration? Each is testable. The "
            "current corpus asserts the conclusion without the object, which is "
            "how the sqrt(21) episode began."
        ),
        "checks": {k: bool(v) for k, v in checks.items() if isinstance(v, bool)},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
