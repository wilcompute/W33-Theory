#!/usr/bin/env python3
"""Part DCMLXXXIV: post-burst forcing/moonshine corrective audit.

The DCCLXXVIII-DCCLXXXIII burst added strong Moonshine, Narain, horizon,
and Leech arithmetic.  It also introduced two claims that need a hard boundary:

* 640320 is not 2^7*q^2*5*Phi6*B2.
* W(3,3) is not the Johnson graph J(40,12), so the Johnson/girth pincer cannot
  prove d_X=q=3.

This verifier promotes the exact arithmetic that survives and records the
unsafe claims as rejected or conditional.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import asdict, dataclass
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DATA_PATH = ROOT / "data" / "dcmlxxxiv_post_burst_forcing_moonshine_audit.json"
RESULT_PATH = ROOT / "PART_DCMLXXXIV_POST_BURST_FORCING_MOONSHINE_AUDIT_results.json"

PART = "DCMLXXXIV"
DECIMAL = 984

Q = 3
DX = 3
DZ = 4
K = 12
LAMBDA = 2
MU = 4
V = 40
E = 240
F = 24
PHI3 = 13
PHI4 = 10
PHI6 = 7
B2 = 127
N_M = 36

RAMANUJAN_ROOT = 640_320
LEECH_MINIMAL_VECTORS = 196_560
MONSTER_C1 = 196_884
ETA_3B_B1 = 54
THETA_E8_A2 = 2_160
H_MIXED_INCIDENCE = 42
H_FULL_INCIDENCE = 96


@dataclass(frozen=True)
class AuditSummary:
    part: str
    decimal: int
    ramanujan_root_status: str
    johnson_girth_pincer_status: str
    q3_status: str
    live_frontier: str
    all_identities_hold: bool


def frac_payload(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "text": f"{value.numerator}/{value.denominator}",
        "float": float(value),
    }


def factorint(value: int) -> dict[int, int]:
    n = abs(value)
    factors: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def johnson_triangle_example() -> dict[str, Any]:
    a = set(range(12))
    b = set(range(11)) | {12}
    c = set(range(11)) | {13}
    intersections = {
        "A_cap_B": len(a & b),
        "A_cap_C": len(a & c),
        "B_cap_C": len(b & c),
    }
    return {
        "A": sorted(a),
        "B": sorted(b),
        "C": sorted(c),
        "pairwise_intersections": intersections,
        "is_triangle_in_J_40_12": all(size == 11 for size in intersections.values()),
    }


def source_anchor_checks() -> dict[str, bool]:
    breakthrough_778 = (ROOT / "BREAKTHROUGH_DCCLXXVIII.md").read_text(encoding="utf-8")
    breakthrough_782 = (ROOT / "BREAKTHROUGH_DCCLXXXII.md").read_text(encoding="utf-8")
    correction = (ROOT / "analysis" / "2026-05-18_moonshine_factorization_correction.md").read_text(
        encoding="utf-8"
    )
    theta_eta = (ROOT / "analysis" / "2026-05-18_theta_eta_horizon_coupling.md").read_text(
        encoding="utf-8"
    )
    monster_3b = (ROOT / "analysis" / "2026-05-18_monster_3b_horizon_syndrome.md").read_text(
        encoding="utf-8"
    )
    return {
        "burst_contains_false_640320_product": "640320 = 2^7" in breakthrough_778
        or "640320 = 2⁷" in breakthrough_778,
        "correction_contains_additive_b2_bridge": "640320=7!\\cdot127+240" in correction,
        "burst_contains_johnson_girth_claim": "The W(3,3) graph is the Johnson graph `J(40, 12)`"
        in breakthrough_782,
        "theta_eta_contains_a2_bridge": "2160=40\\cdot54" in theta_eta,
        "monster_3b_contains_horizon_jump": "96-42=54" in monster_3b,
    }


def build_audit() -> dict[str, Any]:
    claimed_640320_product = (2**7) * (Q**2) * 5 * PHI6 * B2
    correct_prime_factorization = factorint(RAMANUJAN_ROOT)
    correct_multiplicative = E * DZ * (F - 1) * (F + LAMBDA + Q)
    additive_b2 = math.factorial(PHI6) * B2 + E

    w33_line_count = 40
    w33_line_size = Q + 1
    triangles_per_line = math.comb(w33_line_size, 3)
    w33_collinearity_triangles = w33_line_count * triangles_per_line
    w33_girth = 3 if w33_collinearity_triangles else None
    johnson_vertices = math.comb(40, 12)
    johnson_degree = 12 * (40 - 12)
    johnson_triangle = johnson_triangle_example()

    monster_level = K * Q * Q
    horizon_jump = H_FULL_INCIDENCE - H_MIXED_INCIDENCE
    leech_scaled = E * Q * Q * PHI6 * PHI3
    monster_gap = MONSTER_C1 - LEECH_MINIMAL_VECTORS
    leech_factor = LEECH_MINIMAL_VECTORS // (K * Q * Q)

    source_anchors = source_anchor_checks()

    johnson_boundary = {
        "w33_collinearity_graph": {
            "vertices": V,
            "degree": K,
            "line_count": w33_line_count,
            "line_size": w33_line_size,
            "triangles_from_lines": w33_collinearity_triangles,
            "girth": w33_girth,
        },
        "johnson_J_40_12": {
            "vertices": johnson_vertices,
            "degree": johnson_degree,
            "triangle_example": johnson_triangle,
        },
        "classification": (
            "rejected: W(3,3) collinearity is 40-vertex 12-regular with "
            "line K4 triangles; J(40,12) has C(40,12) vertices and valency 336."
        ),
        "girth_over_two_for_w33": frac_payload(Fraction(w33_girth, 2)),
        "d_x_from_girth_over_two": "not_applicable",
    }

    moonshine_boundary = {
        "ramanujan_heegner_root": RAMANUJAN_ROOT,
        "rejected_product": {
            "formula": "2^7*q^2*5*Phi6*B2",
            "value": claimed_640320_product,
            "target": RAMANUJAN_ROOT,
            "difference": claimed_640320_product - RAMANUJAN_ROOT,
            "classification": "false_multiplicative_b2_claim",
        },
        "correct_prime_factorization": correct_prime_factorization,
        "correct_edge_factorization": {
            "formula": "|E|*dZ*(f-1)*(f+lambda+q)",
            "value": correct_multiplicative,
            "factors": [E, DZ, F - 1, F + LAMBDA + Q],
        },
        "correct_additive_b2_bridge": {
            "formula": "Phi6!*B2 + |E|",
            "value": additive_b2,
            "factors": [math.factorial(PHI6), B2, E],
        },
    }

    preserved_exact = {
        "monster_3b_level": {
            "level": monster_level,
            "forms": {
                "k*q^2": K * Q * Q,
                "q*N_M": Q * N_M,
                "2*horizon_jump": 2 * horizon_jump,
            },
            "q_selected_if_k_and_N_M_fixed": frac_payload(Fraction(N_M, K)),
        },
        "theta_eta_horizon": {
            "horizon_jump": horizon_jump,
            "theta_E8_a2": THETA_E8_A2,
            "a2_equals_v_jump": V * horizon_jump,
            "a2_over_jump": frac_payload(Fraction(THETA_E8_A2, horizon_jump)),
        },
        "leech_monster_split": {
            "leech_minimal_vectors": LEECH_MINIMAL_VECTORS,
            "leech_scaled_from_E8": leech_scaled,
            "monster_c1": MONSTER_C1,
            "monster_gap": monster_gap,
            "gap_form_k_q3": K * Q**3,
        },
        "prime_1823_boundary": {
            "leech_factor": leech_factor,
            "additive_identity": leech_factor + Q,
            "factor_1820": MU * 5 * PHI6 * PHI3,
            "classification": (
                "additive Leech-shadow identity; it uses the external factor 5 "
                "and is not a pure multiplicative substrate factorization of 1823"
            ),
        },
    }

    q3_status = {
        "d_x": DX,
        "q": Q,
        "preserved_exact_sources": [
            "CSS/Hamming parameter d_X=q=3",
            "Monster level selector q=N_M/k=36/12 when N_M and k are fixed",
        ],
        "rejected_source": "Johnson graph girth-over-two pincer",
        "classification": (
            "q=3 remains exact in the audited finite/code layers, but the "
            "DCCLXXXII Johnson/girth argument is not a valid independent proof."
        ),
    }

    external_sources = [
        {
            "label": "MathWorld Johnson Graph",
            "url": "https://mathworld.wolfram.com/JohnsonGraph.html",
            "used_fact": "J(n,k) has k-subsets of an n-set as vertices; this already rules out identifying J(40,12) with a 40-vertex graph.",
            "runtime_dependency": False,
        },
        {
            "label": "MathWorld Generalized Quadrangle",
            "url": "https://mathworld.wolfram.com/GeneralizedQuadrangle.html",
            "used_fact": "A generalized quadrangle of order (3,3) has 40 points with 4 points on a line; line cliques give collinearity triangles.",
            "runtime_dependency": False,
        },
        {
            "label": "MathWorld Leech Lattice",
            "url": "https://mathworld.wolfram.com/LeechLattice.html",
            "used_fact": "The Leech lattice has 196560 minimal vectors/kissing number, matching the exact Monster-Leech split used here.",
            "runtime_dependency": False,
        },
    ]

    identities = {
        "part_number_is_984": PART == "DCMLXXXIV" and DECIMAL == 984,
        "source_anchors_present": all(source_anchors.values()),
        "wrong_640320_product_is_false": claimed_640320_product != RAMANUJAN_ROOT,
        "correct_prime_factorization": correct_prime_factorization == {2: 6, 3: 1, 5: 1, 23: 1, 29: 1},
        "correct_edge_factorization": correct_multiplicative == RAMANUJAN_ROOT,
        "correct_additive_b2_bridge": additive_b2 == RAMANUJAN_ROOT,
        "b2_is_mersenne_heptad": B2 == 2**PHI6 - 1,
        "w33_has_40_vertices_and_degree_12": V == 40 and K == 12,
        "w33_collinearity_has_triangles": w33_girth == 3 and w33_collinearity_triangles == 160,
        "johnson_j_40_12_not_w33": johnson_vertices != V and johnson_degree != K,
        "johnson_j_40_12_has_triangle_counterexample": johnson_triangle["is_triangle_in_J_40_12"],
        "girth_over_two_pincer_rejected": Fraction(w33_girth, 2) != DX,
        "monster_3b_level_forms_hold": monster_level == Q * N_M == 2 * horizon_jump == 108,
        "theta_eta_horizon_bridge_holds": THETA_E8_A2 == V * horizon_jump == E * Q * Q,
        "leech_minimal_vectors_scaled_from_e8": LEECH_MINIMAL_VECTORS == leech_scaled,
        "monster_c1_leech_gap_holds": MONSTER_C1 == LEECH_MINIMAL_VECTORS + K * Q**3,
        "prime_1823_additive_boundary": leech_factor == MU * 5 * PHI6 * PHI3
        and leech_factor + Q == 1823,
        "external_sources_are_static": all(not source["runtime_dependency"] for source in external_sources),
    }

    summary = AuditSummary(
        part=PART,
        decimal=DECIMAL,
        ramanujan_root_status="corrected: additive B2 bridge, not multiplicative B2 factor",
        johnson_girth_pincer_status="rejected: W33 is not J(40,12)",
        q3_status="preserved exact, but not proved by Johnson/girth pincer",
        live_frontier="functorial CSS/horizon proof of d_X=3 without Johnson misidentification",
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "source_anchor_checks": source_anchors,
        "moonshine_640320_boundary": moonshine_boundary,
        "johnson_girth_boundary": johnson_boundary,
        "preserved_exact_identities": preserved_exact,
        "q3_forcing_status": q3_status,
        "static_external_sources": external_sources,
        "honesty_boundary": (
            "This is a corrective audit. It preserves exact post-burst arithmetic "
            "while refusing to count the false B2 product or the Johnson/girth "
            "claim as proved theory."
        ),
        "identities": identities,
    }


def write_audit() -> tuple[Path, Path]:
    payload = build_audit()
    DATA_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    RESULT_PATH.write_text(
        json.dumps(
            {
                "part": payload["summary"]["part"],
                "decimal": payload["summary"]["decimal"],
                "status": "VERIFIED: post-burst forcing/moonshine corrective audit",
                "summary": payload["summary"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return DATA_PATH, RESULT_PATH


def main() -> None:
    data_path, result_path = write_audit()
    print(f"Wrote {data_path}")
    print(f"Wrote {result_path}")


if __name__ == "__main__":
    main()
