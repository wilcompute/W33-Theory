"""Cycle Clock Theory crosswalk for the W(3,3) paper.

This module does not try to certify Cycle Clock Theory.  It records the
finite mathematical overlap between the paper's W(3,3) kernel and the
structural desiderata that CCT emphasizes: finite symbolic language,
trit-level efficiency, Clifford/root-system process objects, E8/H4
quasicrystal projection data, and closed feedback loops.
"""
from __future__ import annotations

from typing import Any


Q = 3
LAMBDA = 2
MU = 4
K = 12
V = 40
E = V * K // 2
PHI3 = 13
PHI4 = 10
PHI6 = 7
F = 24


def q_factorial_equals_two_q_only_at_three(limit: int = 12) -> list[int]:
    """Return positive q <= limit satisfying q! = 2q."""
    hits: list[int] = []
    fact = 1
    for q in range(1, limit + 1):
        fact *= q
        if fact == 2 * q:
            hits.append(q)
    return hits


def projective_qutrit_phase_space_counts() -> dict[str, int]:
    """Counts for nonzero F_3^4 vectors modulo scalar multiplication."""
    affine_vectors = Q**MU
    nonzero_vectors = affine_vectors - 1
    nonzero_scalars = Q - 1
    projective_points = nonzero_vectors // nonzero_scalars
    return {
        "q": Q,
        "dimension": MU,
        "affine_vectors": affine_vectors,
        "nonzero_vectors": nonzero_vectors,
        "nonzero_scalars": nonzero_scalars,
        "projective_points": projective_points,
        "w33_vertices": V,
    }


def w33_clock_language_summary() -> dict[str, Any]:
    """Finite code-language invariants of the two-qutrit W(3,3) kernel."""
    points = projective_qutrit_phase_space_counts()
    line_count = V
    matchings_per_line = Q
    line_clock_states = line_count * matchings_per_line
    return {
        "symbols": {
            "trit_alphabet_size": Q,
            "q_factorial_equals_two_q_hits": q_factorial_equals_two_q_only_at_three(),
            "two_qutrit_exponent_vectors": points["affine_vectors"],
            "nonidentity_exponent_vectors": points["nonzero_vectors"],
            "projective_symbols": points["projective_points"],
        },
        "relational_rules": {
            "srg_parameters": (V, K, LAMBDA, MU),
            "master_equation_left": K * (K - LAMBDA - 1),
            "master_equation_right": (V - K - 1) * MU,
            "edge_relations": E,
            "symplectic_commutation_rule": "B(x,y)=0 over F_3",
        },
        "syntactical_freedom": {
            "line_count": line_count,
            "matchings_per_line": matchings_per_line,
            "line_clock_states": line_clock_states,
            "line_clock_edge_cover": 2 * line_clock_states,
            "cycle_rank": E - V + 1,
        },
    }


def e8_h4_projection_summary() -> dict[str, Any]:
    """E8/H4 projection arithmetic already forced by W(3,3)."""
    h = Q * PHI4
    rank_e8 = K - MU
    rank_h4 = MU
    e8_degrees = (
        LAMBDA,
        K - MU,
        K,
        PHI3 + 1,
        K + MU + LAMBDA,
        E // K,
        F,
        h,
    )
    h4_degrees = (LAMBDA, K, E // K, h)
    return {
        "w33_edges": E,
        "e8_roots": rank_e8 * h,
        "h4_roots": rank_h4 * h,
        "e8_rank": rank_e8,
        "h4_rank": rank_h4,
        "coxeter_number": h,
        "e8_dimension": E + LAMBDA**Q,
        "e8_degrees": e8_degrees,
        "h4_degrees": h4_degrees,
        "h4_degrees_embed_in_e8": set(h4_degrees).issubset(set(e8_degrees)),
    }


def full_symmetry_no_go_summary() -> dict[str, Any]:
    """The finite counterpart of choosing an H4 projection plane."""
    orbital_degrees = (2, 27, 36, 54)
    possible_degrees = sorted(
        {
            sum(deg for bit, deg in enumerate(orbital_degrees) if mask & (1 << bit))
            for mask in range(1 << len(orbital_degrees))
        }
    )
    return {
        "m120_states": 120,
        "six_hundred_cell_degree": K,
        "full_psp43_orbital_degrees": orbital_degrees,
        "possible_invariant_degrees": possible_degrees,
        "full_symmetry_can_make_600_cell_graph": K in possible_degrees,
        "required_selector": "golden/icosahedral H4 projection data",
    }


def build_cct_crosswalk() -> dict[str, Any]:
    """Side-by-side CCT desiderata and W(3,3) finite witnesses."""
    language = w33_clock_language_summary()
    projection = e8_h4_projection_summary()
    no_go = full_symmetry_no_go_summary()
    rows = [
        {
            "cct_desideratum": "finite code/language",
            "w33_witness": "F_3^4 projective two-qutrit Pauli symbols",
            "integer_certificate": language["symbols"]["projective_symbols"],
        },
        {
            "cct_desideratum": "principle of efficient language",
            "w33_witness": "q=3 is the unique q<=12 solution of q! = 2q",
            "integer_certificate": Q,
        },
        {
            "cct_desideratum": "trit savings",
            "w33_witness": "81 two-qutrit exponent vectors collapse to 40 projective nonidentity observables",
            "integer_certificate": language["symbols"]["two_qutrit_exponent_vectors"],
        },
        {
            "cct_desideratum": "Clifford/root-system process objects",
            "w33_witness": "Aut(W(3,3)) = Sp(4,3), the two-qutrit Clifford symplectic group",
            "integer_certificate": 51_840,
        },
        {
            "cct_desideratum": "E8 to H4 quasicrystal pathway",
            "w33_witness": "240 W(3,3) edges, 120 internal line-matching states",
            "integer_certificate": projection["w33_edges"],
        },
        {
            "cct_desideratum": "feedback loop / cycle-clock dynamics",
            "w33_witness": "finite graph cycle rank and three-state line clocks",
            "integer_certificate": language["syntactical_freedom"]["cycle_rank"],
        },
        {
            "cct_desideratum": "non-arbitrary H4 emergence",
            "w33_witness": "full PSp(4,3) symmetry cannot produce a 12-regular 600-cell skeleton",
            "integer_certificate": no_go["full_psp43_orbital_degrees"],
        },
    ]
    return {
        "language": language,
        "projection": projection,
        "no_go": no_go,
        "crosswalk_rows": rows,
        "theorem": {
            "w33_realizes_cct_finite_language_template": all(
                [
                    language["symbols"]["q_factorial_equals_two_q_hits"] == [Q],
                    language["symbols"]["projective_symbols"] == V,
                    language["relational_rules"]["master_equation_left"]
                    == language["relational_rules"]["master_equation_right"],
                    language["syntactical_freedom"]["line_clock_states"] == 120,
                    projection["e8_roots"] == E,
                    projection["h4_roots"] == 120,
                    projection["h4_degrees_embed_in_e8"],
                    not no_go["full_symmetry_can_make_600_cell_graph"],
                ]
            ),
            "interpretation": (
                "W(3,3) is an executable finite instance of the CCT code-language "
                "template; the H4/quasicrystal step still requires an extra "
                "golden/icosahedral selector."
            ),
        },
    }


if __name__ == "__main__":
    import json

    print(json.dumps(build_cct_crosswalk(), indent=2))
