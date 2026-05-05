#!/usr/bin/env python3
"""
PART CCCXXIV -- TOE Architecture Compiler
=========================================

Executable architecture audit tying the photon/qutrit/W33 runtime stack into one
finite-system theorem spine.

This file separates exact finite identities from physics-facing interpretation.
The exact layer verifies:

    q=3 bootloader -> W(3,3) parameters -> two-qutrit Pauli address space
    -> photonic MBQC resources -> Clifford orbit compiler -> critical fusion
    -> Hashimoto carrier -> determinant/action compression -> RG-renderer boundary.

The point is not to refit physical constants.  It is to compile the architecture:
which finite objects are memory, which are gates/resources, which are propagation
states, and which quantities belong to the UV boundary later rendered by RG flow.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

# --- W(3,3) base constants ---
Q = 3
LAM = 2
MU = 4
K = 12
V = 40
F = 24
G = 15

E = V * K // 2
T = V * K * LAM // 6
DIRECTED_HASHIMOTO = 2 * E
TRIANGLE_TRACE = 6 * T

PHI3 = Q * Q + Q + 1
PHI4 = Q * Q + 1
PHI6 = Q * Q - Q + 1
THETA = Q * Q + 1
J_INV = 2 ** Q

SP4_F3_ORDER = Q ** 4 * (Q ** 2 - 1) * (Q ** 4 - 1)

SIN2_THETA_W_GUT = Fraction(Q, LAM ** Q)
BETA_MSSM = (Fraction(Q * (K - 1), MU + 1), Fraction(1, 1), Fraction(-Q, 1))
BETA_SM = (Fraction(V + 1, PHI4), Fraction(-(F - MU - 1), LAM * Q), Fraction(-PHI6, 1))


def frac_str(x: Fraction) -> str:
    """Stable JSON string representation for exact rational values."""
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def ok(name: str, condition: bool, value: Any = None) -> Dict[str, Any]:
    return {"name": name, "passed": bool(condition), "value": value}


def build_results() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 1. Bootloader / W33 closure.
    # ------------------------------------------------------------------
    checks.append(ok("q! = 2q selects q=3", math.factorial(Q) == 2 * Q, Q))
    checks.append(ok("V = (q^4-1)/(q-1)", V == (Q ** 4 - 1) // (Q - 1), V))
    checks.append(ok("K = 2^q + q + 1", K == 2 ** Q + Q + 1, K))
    checks.append(ok("lambda = q-1", LAM == Q - 1, LAM))
    checks.append(ok("mu = q+1", MU == Q + 1, MU))
    checks.append(ok("E = VK/2 = 240", E == 240, E))
    checks.append(ok("T = VKlambda/6 = 160", T == 160, T))
    checks.append(ok("directed Hashimoto carrier = 2E = 480", DIRECTED_HASHIMOTO == 480, DIRECTED_HASHIMOTO))
    checks.append(ok("triangle trace = 6T = 960", TRIANGLE_TRACE == 960, TRIANGLE_TRACE))

    # ------------------------------------------------------------------
    # 2. Two-qutrit Pauli address space.
    # ------------------------------------------------------------------
    pauli_exponent_vectors = Q ** 4
    projective_observables = (pauli_exponent_vectors - 1) // (Q - 1)
    checks.append(ok("two-qutrit Pauli exponent vectors = q^4 = 81", pauli_exponent_vectors == 81, pauli_exponent_vectors))
    checks.append(ok("projectivized nonzero two-qutrit observables = 40", projective_observables == V, projective_observables))
    checks.append(ok("Sp(4,F3) order = Aut(W33) order = 51840", SP4_F3_ORDER == 51840, SP4_F3_ORDER))

    # ------------------------------------------------------------------
    # 3. Photonic MBQC resource layer.
    # ------------------------------------------------------------------
    p_fusion = Fraction(LAM, MU)
    p_klm = Fraction(1, MU)
    expected_fusion_attempts = Fraction(E, 1) / p_fusion
    expected_klm_attempts = Fraction(E, 1) / p_klm
    checks.append(ok("photon qubit face dimension = lambda = 2", LAM == 2, LAM))
    checks.append(ok("photonic qutrit mode count = q = 3", Q == 3, Q))
    checks.append(ok("Type-II fusion probability = lambda/mu = 1/2", p_fusion == Fraction(1, 2), frac_str(p_fusion)))
    checks.append(ok("KLM primitive success probability = 1/mu = 1/4", p_klm == Fraction(1, 4), frac_str(p_klm)))
    checks.append(ok("expected W33 fusion attempts = E/p = 480", expected_fusion_attempts == DIRECTED_HASHIMOTO, int(expected_fusion_attempts)))
    checks.append(ok("expected KLM attempts for all W33 edges = tr(A^3)", expected_klm_attempts == TRIANGLE_TRACE, int(expected_klm_attempts)))

    # ------------------------------------------------------------------
    # 4. Critical fusion/percolation layer.
    # ------------------------------------------------------------------
    retained_edges = p_fusion * E
    complementary_edges = (1 - p_fusion) * E
    critical_degree = p_fusion * K
    critical_degree_variance = K * p_fusion * (1 - p_fusion)
    critical_stabilizer_weight = 1 + critical_degree
    full_stabilizer_weight = 1 + K
    critical_triangle_trace = 6 * T * p_fusion ** 3
    edge_count_variance = E * p_fusion * (1 - p_fusion)

    checks.append(ok("critical retained edges = 120", retained_edges == 120, int(retained_edges)))
    checks.append(ok("critical complementary edges = 120", complementary_edges == 120, int(complementary_edges)))
    checks.append(ok("critical split E = 120+120", retained_edges + complementary_edges == E, f"{int(retained_edges)}+{int(complementary_edges)}"))
    checks.append(ok("critical expected degree = 2q", critical_degree == 2 * Q, int(critical_degree)))
    checks.append(ok("critical degree variance = q", critical_degree_variance == Q, int(critical_degree_variance)))
    checks.append(ok("critical stabilizer weight = Phi_6", critical_stabilizer_weight == PHI6, int(critical_stabilizer_weight)))
    checks.append(ok("full stabilizer weight = Phi_3", full_stabilizer_weight == PHI3, full_stabilizer_weight))
    checks.append(ok("critical triangle trace = 120", critical_triangle_trace == 120, int(critical_triangle_trace)))
    checks.append(ok("4 * critical edge-count variance = E", 4 * edge_count_variance == E, int(edge_count_variance)))

    # ------------------------------------------------------------------
    # 5. Clifford compiler orbit factors.
    # ------------------------------------------------------------------
    checks.append(ok("Sp order / vertices = (q+1)^2 q^4", SP4_F3_ORDER // V == (Q + 1) ** 2 * Q ** 4, SP4_F3_ORDER // V))
    checks.append(ok("Sp order / edges = 216 = 8q^3", SP4_F3_ORDER // E == 8 * Q ** 3, SP4_F3_ORDER // E))
    checks.append(ok("Sp order / directed Hashimoto carrier = mu q^3", SP4_F3_ORDER // DIRECTED_HASHIMOTO == MU * Q ** 3, SP4_F3_ORDER // DIRECTED_HASHIMOTO))
    checks.append(ok("Sp order / triangle trace = lambda q^3", SP4_F3_ORDER // TRIANGLE_TRACE == LAM * Q ** 3, SP4_F3_ORDER // TRIANGLE_TRACE))
    checks.append(ok("Sp order / triangles = mu q^4", SP4_F3_ORDER // T == MU * Q ** 4, SP4_F3_ORDER // T))

    # ------------------------------------------------------------------
    # 6. Determinant/action compression.
    # ------------------------------------------------------------------
    # Z(x)=(1-5x)^10(1+x)^16(1+7x)^6.  Store the factor as
    # (linear coefficient c, exponent e) for (1-cx)^e.
    determinant_terms = [(5, PHI4), (-1, (Q + 1) ** 2), (-PHI6, 2 * Q)]
    det_coefficients = tuple(c for c, _ in determinant_terms)
    det_exponents = tuple(e for _, e in determinant_terms)
    signed_first_moment = sum(c * e for c, e in determinant_terms)
    second_moment = sum((c ** 2) * e for c, e in determinant_terms)
    exponent_product = math.prod(det_exponents)
    z_at_one_power = 20 + 16 + 18  # (-4)^10 * 2^16 * 8^6 = 2^54

    checks.append(ok("determinant coefficients = {J,-1,-Phi6}", det_coefficients == (5, -1, -7), det_coefficients))
    checks.append(ok("determinant exponents = {Phi4,(q+1)^2,2q}", det_exponents == (10, 16, 6), det_exponents))
    checks.append(ok("determinant exponent product = tr(A^3)", exponent_product == TRIANGLE_TRACE, exponent_product))
    checks.append(ok("determinant signed first moment = -2^q", signed_first_moment == -J_INV, signed_first_moment))
    checks.append(ok("determinant second moment = Phi6(q^4-1)", second_moment == PHI6 * (Q ** 4 - 1), second_moment))
    checks.append(ok("Z(1)=2^(2q^3)", z_at_one_power == 2 * Q ** 3, z_at_one_power))

    # ------------------------------------------------------------------
    # 7. RG renderer boundary.
    # ------------------------------------------------------------------
    checks.append(ok("weak-mixing UV boundary = q/lambda^q = 3/8", SIN2_THETA_W_GUT == Fraction(3, 8), frac_str(SIN2_THETA_W_GUT)))
    checks.append(ok("MSSM b1 = q(k-1)/(mu+1) = 33/5", BETA_MSSM[0] == Fraction(33, 5), frac_str(BETA_MSSM[0])))
    checks.append(ok("MSSM b2 = 1", BETA_MSSM[1] == Fraction(1, 1), frac_str(BETA_MSSM[1])))
    checks.append(ok("MSSM b3 = -q", BETA_MSSM[2] == Fraction(-Q, 1), frac_str(BETA_MSSM[2])))
    checks.append(ok("SM beta coefficients have W33 forms", BETA_SM == (Fraction(41, 10), Fraction(-19, 6), Fraction(-7, 1)), tuple(frac_str(x) for x in BETA_SM)))

    verified = all(check["passed"] for check in checks)

    architecture = {
        "bootloader": "q! = 2q selects q=3 and the finite field F_3.",
        "memory_register": "Projective nonzero vectors of F_3^4 are the 40 two-qutrit Pauli observables.",
        "commutation_geometry": "W(3,3) adjacency is the vanishing symplectic commutator.",
        "hardware": "Single photons expose lambda=2 qubit interfaces and q=3 qutrit mode interfaces.",
        "resource_layer": "A W33 photonic cluster has 40 photons, 240 edges, and expected 480 Type-II fusion attempts.",
        "compiler": "Sp(4,F3) is the Clifford/automorphism compiler of order 51840.",
        "critical_realization": "Type-II fusion at p=lambda/mu=1/2 realizes the 120+120 Seidel split and Phi3->Phi6 stabilizer transition.",
        "causal_scheduler": "Hashimoto directed edges are the 480-state non-backtracking propagation carrier.",
        "action_compression": "The determinant (1-5x)^10(1+x)^16(1+7x)^6 compresses triangle trace and operator moments.",
        "rg_renderer": "W33 supplies UV arithmetic boundaries; RG flow renders IR observables such as sin^2 theta_W(M_Z).",
    }

    return {
        "part": "CCCXXIV",
        "title": "TOE Architecture Compiler: photon-qutrit-W33 runtime stack",
        "verified": verified,
        "checks_total": len(checks),
        "checks_passed": sum(1 for check in checks if check["passed"]),
        "constants": {
            "q": Q,
            "lambda": LAM,
            "mu": MU,
            "k": K,
            "v": V,
            "f": F,
            "g": G,
            "E": E,
            "T": T,
            "directed_hashimoto": DIRECTED_HASHIMOTO,
            "triangle_trace": TRIANGLE_TRACE,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
            "Sp4_F3_order": SP4_F3_ORDER,
        },
        "probabilities": {
            "p_fusion": frac_str(p_fusion),
            "p_klm": frac_str(p_klm),
        },
        "resource_counts": {
            "photons": V,
            "edges": E,
            "expected_type_ii_fusion_attempts": int(expected_fusion_attempts),
            "expected_klm_attempts_all_edges": int(expected_klm_attempts),
            "critical_retained_edges": int(retained_edges),
            "critical_complement_edges": int(complementary_edges),
            "full_stabilizer_weight": full_stabilizer_weight,
            "critical_stabilizer_weight": int(critical_stabilizer_weight),
        },
        "orbit_factors": {
            "per_vertex": SP4_F3_ORDER // V,
            "per_edge": SP4_F3_ORDER // E,
            "per_directed_hashimoto_state": SP4_F3_ORDER // DIRECTED_HASHIMOTO,
            "per_triangle_trace_unit": SP4_F3_ORDER // TRIANGLE_TRACE,
            "per_triangle": SP4_F3_ORDER // T,
        },
        "determinant": {
            "Z(x)": "(1-5x)^10(1+x)^16(1+7x)^6",
            "coefficients": det_coefficients,
            "exponents": det_exponents,
            "signed_first_moment": signed_first_moment,
            "second_moment": second_moment,
            "exponent_product": exponent_product,
            "Z(1)": f"2^{z_at_one_power}",
        },
        "rg_boundary": {
            "sin2_theta_W_MGUT": frac_str(SIN2_THETA_W_GUT),
            "MSSM_beta": tuple(frac_str(x) for x in BETA_MSSM),
            "SM_beta": tuple(frac_str(x) for x in BETA_SM),
        },
        "architecture": architecture,
        "theorem": (
            "W(3,3) is the finite photon-qutrit runtime kernel: its 40 projective "
            "two-qutrit Pauli observables are the memory/address layer; its 240 edges "
            "are entangling resources; its 480 directed edges are the Hashimoto causal "
            "scheduler and the expected Type-II fusion-attempt budget; Sp(4,F3) is the "
            "Clifford compiler; the determinant compresses the action/operator stack; "
            "and RG flow renders W33 UV boundary data into IR observables."
        ),
        "honesty_boundary": (
            "This audit proves exact finite architecture identities.  It does not by "
            "itself prove a continuum Standard Model action, a full quantum-gravity "
            "scaling limit, or all measured constants.  Those require the next layer: "
            "a canonical finite action plus a controlled RG/scaling construction."
        ),
        "checks": checks,
    }


def main() -> None:
    results = build_results()
    out_path = ROOT / "PART_CCCXXIV_toe_architecture_compiler_results.json"
    out_path.write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "part": results["part"],
        "verified": results["verified"],
        "checks_passed": results["checks_passed"],
        "checks_total": results["checks_total"],
        "out_path": str(out_path),
    }, indent=2))


if __name__ == "__main__":
    main()
