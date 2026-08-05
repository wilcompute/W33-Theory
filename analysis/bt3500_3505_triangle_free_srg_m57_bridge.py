#!/usr/bin/env python3
"""Passes 3500-3505: exact triangle-free SRG / W33 / missing-Moore bridge.

This module deliberately separates:
  * exact parameter and spectral arithmetic;
  * necessary local structure for a hypothetical Moore(57,2) graph;
  * literature-status flags, which are data and not re-proved here.

It uses only the Python standard library and writes a deterministic JSON
certificate when executed as a script.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


KNOWN_TRIANGLE_FREE_SRGS = [
    {"name": "C5", "parameters": [5, 2, 0, 1]},
    {"name": "Petersen", "parameters": [10, 3, 0, 1]},
    {"name": "Clebsch", "parameters": [16, 5, 0, 2]},
    {"name": "Hoffman-Singleton", "parameters": [50, 7, 0, 1]},
    {"name": "Gewirtz", "parameters": [56, 10, 0, 2]},
    {"name": "M22", "parameters": [77, 16, 0, 4]},
    {"name": "Higman-Sims", "parameters": [100, 22, 0, 6]},
]

MU4_R2_LABELS = {
    0: {"name": "M22", "status": "exists_unique"},
    1: {"name": "57-vertex hole", "status": "nonexistent_Wilbrink_Brouwer_1983"},
    2: {"name": "W33 parameter class", "status": "exists_28_isomorphism_classes"},
    3: {"name": "Paulus parameter class", "status": "exists_10_isomorphism_classes"},
    4: {"name": "T(6)", "status": "exists_unique"},
}


def srg_feasible(v: int, k: int, lam: int, mu: int) -> bool:
    return (v - k - 1) * mu == k * (k - lam - 1)


def srg_spectrum(v: int, k: int, lam: int, mu: int) -> dict[str, Any]:
    """Return exact SRG spectral data, retaining a quadratic radical if needed."""
    disc = (lam - mu) ** 2 + 4 * (k - mu)
    root = int(disc**0.5)
    if root * root == disc:
        r = Fraction(lam - mu + root, 2)
        s = Fraction(lam - mu - root, 2)
        f = Fraction(-k - s * (v - 1), r - s)
        g = Fraction(v - 1) - f
        if any(x.denominator != 1 for x in (r, s, f, g)):
            raise ValueError("non-integral spectrum/multiplicity")
        return {
            "eigenvalues": [k, int(r), int(s)],
            "multiplicities": [1, int(f), int(g)],
            "discriminant": disc,
        }

    # The only nonsquare case used in this packet is C5.  The multiplicities
    # can be checked directly from trace and dimension.
    if [v, k, lam, mu] == [5, 2, 0, 1]:
        return {
            "eigenvalues": ["2", "(-1+sqrt(5))/2", "(-1-sqrt(5))/2"],
            "multiplicities": [1, 2, 2],
            "discriminant": 5,
        }
    raise ValueError(f"unsupported non-square SRG discriminant {disc}")


def srg_spectrum_integral(v: int, k: int, lam: int, mu: int) -> dict[str, Any]:
    out = srg_spectrum(v, k, lam, mu)
    if not all(isinstance(x, int) for x in out["eigenvalues"]):
        raise ValueError("spectrum is not integral")
    return {"eigenvalues": out["eigenvalues"], "multiplicities": out["multiplicities"]}


def mu4_r2_member(lam: int) -> dict[str, Any]:
    """The exact fixed-mu=4, positive-eigenvalue r=2 ladder."""
    mu = 4
    r = 2
    s = lam - 6
    k = 16 - 2 * lam
    v = (lam - 7) * (3 * lam - 22) // 2
    f_r = (lam - 5) * (3 * lam - 22) // 2
    f_s = -3 * (lam - 7)
    item = {
        "lambda": lam,
        "parameters": [v, k, lam, mu],
        "spectrum": {
            "eigenvalues": [k, r, s],
            "multiplicities": [1, f_r, f_s],
        },
        **MU4_R2_LABELS[lam],
    }
    assert srg_feasible(v, k, lam, mu)
    assert srg_spectrum_integral(v, k, lam, mu) == item["spectrum"]
    return item


def shared_w33_gewirtz_kernel() -> dict[str, Any]:
    w33 = srg_spectrum_integral(40, 12, 2, 4)
    gewirtz = srg_spectrum_integral(56, 10, 0, 2)
    assert w33["eigenvalues"][1:] == [2, -4]
    assert gewirtz["eigenvalues"][1:] == [2, -4]
    # On the augmentation module, both adjacency operators obey
    # (A - 2I)(A + 4I) = A^2 + 2A - 8I = 0.
    # Their complements have nonprincipal eigenvalues -3 and +3.
    return {
        "W33": w33,
        "Gewirtz": gewirtz,
        "common_nonprincipal_minimal_polynomial": "x^2 + 2*x - 8",
        "complement_nonprincipal_eigenvalues": [-3, 3],
        "centered_complement_square": "9*I_on_augmentation",
        "boundary": "shared_functional_calculus_not_a_canonical_module_isomorphism",
    }


def missing_moore_edge_chart() -> dict[str, Any]:
    """Necessary edge-rooted structure for an SRG(3250,57,0,1)."""
    degree = 57
    vertices = degree * degree + 1
    edges = vertices * degree // 2
    branch = degree - 1
    core = branch * branch

    assert vertices == 3250
    assert edges == 92625
    assert 2 + 2 * branch + core == vertices

    # Fix an edge a--b.  The two punctured neighborhoods have size 56.
    # The residual vertices are forced bijectively onto A x B.
    # Each residual vertex has 2 branch neighbors and 55 residual neighbors.
    residual_degree = degree - 2
    assert residual_degree == branch - 1 == 55

    return {
        "parameters": [vertices, degree, 0, 1],
        "spectrum": {
            "eigenvalues": [57, 7, -8],
            "multiplicities": [1, 1729, 1520],
        },
        "edge_count": edges,
        "edge_rooted_partition": [2, branch, branch, core],
        "residual_grid": [branch, branch],
        "residual_degree": residual_degree,
        "row_fibration": {
            "fibres": branch,
            "fibre_size": branch,
            "between_distinct_fibres": "perfect_matching",
        },
        "column_fibration": {
            "fibres": branch,
            "fibre_size": branch,
            "between_distinct_fibres": "perfect_matching",
        },
        "permutation_constraints": [
            "sigma_ji = inverse(sigma_ij)",
            "sigma_ij has no fixed point",
            "for distinct i,j,k: sigma_ki*sigma_jk*sigma_ij has no fixed point",
        ],
        "boundary": (
            "These are necessary local constraints. Row/column relabellings are "
            "coordinate gauge, not automorphisms of a fixed graph."
        ),
    }


def fifty_seven_firewall() -> dict[str, Any]:
    psl2_19 = 19 * (19 * 19 - 1) // 2
    assert psl2_19 == 3420
    return {
        "objects": {
            "missing_M57": {
                "meaning": "degree_57_Moore_graph",
                "vertices": 3250,
                "degree": 57,
                "status": "existence_open",
            },
            "lambda1_hole": {
                "meaning": "57_vertex_SRG_in_mu4_r2_ladder",
                "parameters": [57, 14, 1, 4],
                "status": "proved_nonexistent_1983",
            },
            "Perkel": {
                "meaning": "57_vertex_distance_regular_graph",
                "vertices": 57,
                "degree": 6,
                "status": "exists",
            },
            "regular_57_cell": {
                "meaning": "abstract_regular_polytope_with_57_cells",
                "symmetry_order": psl2_19,
                "status": "exists",
            },
        },
        "psl2_19_order": psl2_19,
        "psl2_19_even": psl2_19 % 2 == 0,
        "conditional_no_embedding": (
            "If the 2026 no-involution preprint is correct, Aut(M57) has odd "
            "order, so PSL(2,19) cannot embed in Aut(M57)."
        ),
    }


def build_certificate() -> dict[str, Any]:
    known = []
    for graph in KNOWN_TRIANGLE_FREE_SRGS:
        v, k, lam, mu = graph["parameters"]
        assert lam == 0
        assert srg_feasible(v, k, lam, mu)
        known.append({**graph, "spectrum": srg_spectrum(v, k, lam, mu)})

    ladder = [mu4_r2_member(lam) for lam in range(5)]
    assert ladder[0]["parameters"] == [77, 16, 0, 4]
    assert ladder[1]["parameters"] == [57, 14, 1, 4]
    assert ladder[2]["parameters"] == [40, 12, 2, 4]
    assert ladder[3]["parameters"] == [26, 10, 3, 4]
    assert ladder[4]["parameters"] == [15, 8, 4, 4]

    result: dict[str, Any] = {
        "status": "PASS_6_FRONTS",
        "passes": [3500, 3501, 3502, 3503, 3504, 3505],
        "known_triangle_free_srgs": known,
        "mu4_r2_ladder": ladder,
        "w33_gewirtz_kernel": shared_w33_gewirtz_kernel(),
        "missing_moore_edge_chart": missing_moore_edge_chart(),
        "fifty_seven_firewall": fifty_seven_firewall(),
        "claim_audit": {
            "edge_count_is_not_automorphism_count": True,
            "factorial_relabelling_is_not_fixed_graph_automorphism_group": True,
            "regular_bipartite_does_not_imply_complete_bipartite": True,
            "safe_edge_transitivity_boundary": (
                "A connected regular edge-transitive non-vertex-transitive graph "
                "is bipartite; an M57 graph has girth five, hence is not bipartite."
            ),
        },
        "evidence_boundary": [
            "No M57 existence or nonexistence claim is proved here.",
            "The 2026 no-involution result is treated as a recent preprint.",
            "No Perkel/57-cell/M57 graph identification is asserted.",
            "The W33-Gewirtz bridge is spectral, not an objectwise intertwiner.",
        ],
    }
    payload = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["semantic_sha256"] = hashlib.sha256(payload).hexdigest()
    return result


def main() -> None:
    result = build_certificate()
    output = Path("data/PART_BT3500_BT3505_TRIANGLE_FREE_SRG_M57_BRIDGE_results.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(result["status"], result["semantic_sha256"])


if __name__ == "__main__":
    main()
