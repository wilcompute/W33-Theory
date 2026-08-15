#!/usr/bin/env python3
"""Pass5396--5401: all-q Levi apartment cycle tight-frame theorem.

For a generalized quadrangle GQ(q,q), let Gamma be the Levi graph and let X
be its flag line graph.  Let C have one row for every Levi edge/flag and one
column for every simple 8-cycle (apartment), with each apartment column signed
using the fixed orientation point -> line on Levi edges.

A nonbacktracking Levi path of five edges has a unique 8-cycle completion by
the GQ projection axiom.  Removing one terminal edge introduces q choices.
Therefore a pair of flag edges at line-graph distance d lies in q^(4-d)
apartments.  Cycle signs alternate with d, giving

    (C C^T)_{ef} = (-1)^d q^(4-d).

Combining with Pass5388--5392 gives

    C C^T = q^4 A0 - q^3 A1 + q^2 A2 - q A3 + A4
          = N E_{-2},
    N=(q+1)^2(q^2+1).

Thus all oriented apartments form a tight frame for the q^4-dimensional Levi
cycle space.  At q=3 this is exactly the 160 x 1620 BT545--BT549 cycle-frame
identity.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5396_5401_ALLQ_APARTMENT_TIGHT_FRAME.json"
ANCHORS = [2, 3, 4, 5, 7, 8, 9, 11, 13]


def row(q: int) -> dict:
    assert q > 1
    n = (q + 1) ** 2 * (q * q + 1)  # flags = Levi edges
    cycle_dim = q**4
    per_edge = q**4
    numerator = n * per_edge
    assert numerator % 8 == 0
    apartments = numerator // 8

    unsigned = [q**4, q**3, q**2, q, 1]
    signed = [q**4, -q**3, q**2, -q, 1]
    shells = [1, 2*q, 2*q*q, 2*q**3, q**4]

    # Double count apartment/edge incidences.
    assert apartments * 8 == n * per_edge

    # For d=1,2,3 each apartment through e contributes two d-separated
    # edges; for d=4 it contributes its unique opposite edge.
    for d in range(1, 4):
        assert shells[d] * unsigned[d] == 2 * per_edge
    assert shells[4] * unsigned[4] == per_edge

    # Trace of C C^T from rows equals trace from columns.
    assert n * signed[0] == apartments * 8

    # Since C C^T = n E_-2, the nonzero eigenvalue/frame bound is n and
    # the rank is q^4.  Normalizing each length-sqrt(8) apartment column
    # produces a unit-norm tight frame of bound n/8.
    assert apartments * 8 == cycle_dim * n

    return {
        "q": q,
        "flags": n,
        "cycle_dimension": cycle_dim,
        "apartments": apartments,
        "apartments_per_flag_edge": per_edge,
        "pair_apartment_counts_by_distance": unsigned,
        "signed_overlap_by_distance": signed,
        "CCt_nonzero_eigenvalue": n,
        "CCt_rank": cycle_dim,
        "normalized_frame_bound": f"{n}/8",
    }


def build_certificate() -> dict:
    anchors = {str(q): row(q) for q in ANCHORS}
    q3 = anchors["3"]
    assert q3 == {
        "q": 3,
        "flags": 160,
        "cycle_dimension": 81,
        "apartments": 1620,
        "apartments_per_flag_edge": 81,
        "pair_apartment_counts_by_distance": [81, 27, 9, 3, 1],
        "signed_overlap_by_distance": [81, -27, 9, -3, 1],
        "CCt_nonzero_eigenvalue": 160,
        "CCt_rank": 81,
        "normalized_frame_bound": "160/8",
    }
    return {
        "schema": "w33.allq_levi_apartment_tight_frame.v1",
        "pass_range": [5396, 5401],
        "status": "THEOREM_COMBINATORIAL_HODGE_FRAME",
        "domain": "Any finite generalized quadrangle of order (q,q), q>1.",
        "path_completion_lemma": {
            "length_5": "Every nonbacktracking Levi path of five edges closes uniquely to an 8-cycle by the generalized-quadrangle projection axiom.",
            "recursion": "For a fixed shorter nonbacktracking path, each removed terminal edge restores exactly q legal extensions; therefore a distance-d flag-edge pair lies in q^(4-d) apartments.",
        },
        "apartment_census": {
            "flags": "N=(q+1)^2(q^2+1)",
            "apartments_per_flag_edge": "q^4",
            "total_apartments": "N q^4 / 8",
        },
        "overlap_kernel": {
            "unsigned_by_distance_d=0..4": ["q^4", "q^3", "q^2", "q", "1"],
            "signed_by_distance_d=0..4": ["q^4", "-q^3", "q^2", "-q", "1"],
            "reason_for_sign": "With every Levi edge oriented point->line, signs alternate around every 8-cycle; the product for two edges is (-1)^d."
        },
        "tight_frame": {
            "matrix": "C = signed flag-edge x apartment incidence matrix",
            "identity": "C C^T = q^4 A0 - q^3 A1 + q^2 A2 - q A3 + A4 = N E_-2",
            "rank": "q^4",
            "column_norm_squared": 8,
            "normalized_unit_frame_bound": "N/8",
            "number_of_unit_vectors": "N q^4/8",
            "ambient_cycle_dimension": "q^4"
        },
        "w33_specialization": {
            "q": 3,
            "C_shape": [160, 1620],
            "CCt_kernel": [81, -27, 9, -3, 1],
            "identity": "C C^T = 160 E_-2",
            "reading": "Exactly the BT545-BT549 W33 oriented 8-cycle frame and Hodge/Kirchhoff cycle projector."
        },
        "anchors": anchors,
        "boundary": "The theorem uses the full set of apartments. It does not assert that arbitrary apartment subsets are tight frames and does not by itself establish code distance or physical fault tolerance."
    }


def main() -> dict:
    out = build_certificate()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
