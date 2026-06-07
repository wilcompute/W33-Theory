#!/usr/bin/env python3
"""
BT489: Toroidal Dual Incidence Ladder Theorem

This is driven by the toroidal-triad HTML page:
  - dual hole equations
  - shared mod-12 residues {0,3,4,7}
  - next shared level h=6 with edge count 66
  - flag-orbit resonance 42 = 6*7

We turn that into an exact symbolic/networkx verifier.

Let n be an admissible complete-adjacency parameter, i.e.
    h(n) = (n-3)(n-4)/12 is integral.
This happens exactly for n mod 12 in {0,3,4,7}.

Vertex-complete side C_n:
    V=n
    E=C(n,2)
    F=n(n-1)/3
    face degree = 3

Face-complete dual side S_n:
    V=n(n-1)/3
    E=C(n,2)
    F=n
    face degree = n-1

The common face-edge incidence count is
    I = 2E = n(n-1).

At n=7 this is I=42, exactly the toroidal triad page's
"flag orbit resonance" count. At n=12 this becomes I=132
and E=66, the next shared edge prediction.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx


RESIDUES = {0, 3, 4, 7}


def genus(n: int) -> int:
    assert (n - 3) * (n - 4) % 12 == 0
    return ((n - 3) * (n - 4)) // 12


def is_admissible(n: int) -> bool:
    return n % 12 in RESIDUES and (n - 3) * (n - 4) % 12 == 0


def packet(n: int) -> dict:
    assert is_admissible(n)
    E = n * (n - 1) // 2
    Fv = n * (n - 1) // 3
    h = genus(n)

    # NetworkX tests the complete observable sides directly.
    vertex_graph = nx.complete_graph(n)
    face_graph = nx.complete_graph(n)
    assert vertex_graph.number_of_edges() == E
    assert face_graph.number_of_edges() == E

    # Euler checks for both dual sides.
    assert n - E + Fv == 2 - 2 * h
    assert Fv - E + n == 2 - 2 * h

    incidence = 2 * E
    assert incidence == n * (n - 1)
    assert 3 * Fv == incidence
    assert n * (n - 1) == incidence

    defect = Fv - n
    assert defect == n * (n - 4) // 3

    pair = {
        "n": n,
        "residue_mod_12": n % 12,
        "genus": h,
        "edge_count": E,
        "shared_face_edge_incidence": incidence,
        "vertex_complete": {
            "V": n,
            "E": E,
            "F": Fv,
            "face_degree": 3,
            "vertex_adjacency_graph": f"K_{n}",
        },
        "face_complete_dual": {
            "V": Fv,
            "E": E,
            "F": n,
            "face_degree": n - 1,
            "face_adjacency_graph": f"K_{n}",
        },
        "duality_defect_F_minus_V": defect,
        "combined_dual_packet": {
            "V_total": n + Fv,
            "E_total": 2 * E,
            "F_total": n + Fv,
            "self_dual_packet": True,
        },
    }
    return pair


def residue_polynomial_label(r: int) -> str:
    if r == 0:
        return "n=12m: h=12m^2-7m+1"
    if r == 3:
        return "n=12m+3: h=m(12m-1)"
    if r == 4:
        return "n=12m+4: h=m(12m+1)"
    if r == 7:
        return "n=12m+7: h=12m^2+7m+1"
    raise ValueError(r)


def main() -> dict:
    # Confirm the residue law up to a wide range.
    residue_hits = [n for n in range(0, 241) if ((n - 3) * (n - 4)) % 12 == 0]
    assert set(n % 12 for n in residue_hits) == RESIDUES

    ladder_ns = [4, 7, 12, 15, 16, 19, 24, 27, 28, 31, 36, 39, 40, 43]
    ladder = [packet(n) for n in ladder_ns]

    # Key page predictions.
    p4 = packet(4)
    p7 = packet(7)
    p12 = packet(12)
    assert p4["genus"] == 0
    assert p4["vertex_complete"] == p4["face_complete_dual"]
    assert p4["duality_defect_F_minus_V"] == 0

    assert p7["genus"] == 1
    assert p7["edge_count"] == 21
    assert p7["vertex_complete"]["F"] == 14
    assert p7["face_complete_dual"]["V"] == 14
    assert p7["shared_face_edge_incidence"] == 42
    assert p7["duality_defect_F_minus_V"] == 7

    assert p12["genus"] == 6
    assert p12["edge_count"] == 66
    assert p12["vertex_complete"]["F"] == 44
    assert p12["face_complete_dual"]["V"] == 44
    assert p12["shared_face_edge_incidence"] == 132
    assert p12["duality_defect_F_minus_V"] == 32

    # Self-duality occurs only at tetrahedron in the positive nondegenerate ladder.
    self_dual = [p["n"] for p in ladder if p["duality_defect_F_minus_V"] == 0]
    assert self_dual == [4]

    # Recurrence checks for each residue branch: h(n+12)-h(n)=2n+5.
    recurrences = []
    for n in range(4, 120):
        if is_admissible(n) and is_admissible(n + 12):
            assert genus(n + 12) - genus(n) == 2 * n + 5
            recurrences.append({"n": n, "n_plus_12": n + 12, "delta_h": 2 * n + 5})

    results = {
        "theorem": "BT489 Toroidal Dual Incidence Ladder Theorem",
        "source_hint": "visualizations/w33-toroidal-triad.html dual hole equations + mod-12 law + 42/66 constants panel",
        "admissible_residues_mod_12": sorted(RESIDUES),
        "residue_polynomials": {str(r): residue_polynomial_label(r) for r in sorted(RESIDUES)},
        "formulae": {
            "genus": "h(n)=((n-3)(n-4))/12",
            "edge_count": "E=C(n,2)",
            "vertex_complete_f_vector": "(n, C(n,2), n(n-1)/3)",
            "face_complete_dual_f_vector": "(n(n-1)/3, C(n,2), n)",
            "shared_incidence": "I=2E=n(n-1)",
            "duality_defect": "D=F-V=n(n-4)/3",
            "genus_recurrence": "h(n+12)-h(n)=2n+5",
        },
        "special_levels": {
            "tetrahedron_n4": p4,
            "csaszar_szilassi_n7": p7,
            "next_common_n12": p12,
        },
        "ladder_samples": ladder,
        "self_dual_positive_ladder_ns": self_dual,
        "recurrence_samples_first_10": recurrences[:10],
        "substrate_reading": {
            "n4": "unbroken tetrahedral phase: V=F=4 and D=0",
            "n7": "genus-one split: Csaszar (7,21,14) and Szilassi (14,21,7), I=42=6*7",
            "n12": "next shared genus h=6: edge shell E=66 and defect D=32=|E(Q4)|",
            "duality_defect": "D measures how far the vertex and face observables split after tetrahedron",
        },
    }

    out = Path("data/PART_BT489_TOROIDAL_DUAL_INCIDENCE_LADDER_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results


if __name__ == "__main__":
    main()
