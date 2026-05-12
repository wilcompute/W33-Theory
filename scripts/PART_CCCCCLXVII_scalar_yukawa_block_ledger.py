#!/usr/bin/env python3
"""
PART_CCCCCLXVII_scalar_yukawa_block_ledger.py

Executable symbolic ledger for scalar/Yukawa blocks on the W(3,3)
240-dimensional 1-chain carrier.

The carrier decomposes by the 1-Hodge spectrum:

    K: 81, eigenvalue 0
    B: 120, eigenvalue 4
    R: 24, eigenvalue 10
    S: 15, eigenvalue 16

A finite scalar Phi is treated as a self-adjoint block operator over
K+B+R+S.  This script computes the exact sector weights in:

    Tr(Phi^2)
    Tr(Delta_1 Phi^2)
    Tr([Delta_1,Phi]^*[Delta_1,Phi])

and records the minimal K-B scalar/Yukawa ansatz.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

SECTORS = {
    "K": {"dim": 81, "lambda": 0, "meaning": "cellular H1 / massless matter kernel"},
    "B": {"dim": 120, "lambda": 4, "meaning": "triangle-boundary / gauge-local sector"},
    "R": {"dim": 24, "lambda": 10, "meaning": "r-sector heavy correction"},
    "S": {"dim": 15, "lambda": 16, "meaning": "s-sector heavy correction"},
}
ORDER = ["K", "B", "R", "S"]


@dataclass(frozen=True)
class ScalarYukawaBlockLedger:
    part: str
    title: str
    sector_decomposition: dict[str, dict[str, Any]]
    quadratic_trace_weights: dict[str, Any]
    delta_phi_squared_weights: dict[str, Any]
    commutator_gap_penalty: dict[str, Any]
    minimal_KB_ansatz: dict[str, Any]
    quartic_block_rules: dict[str, Any]
    effective_fermion_mass: dict[str, Any]
    checks: dict[str, bool]
    all_checks_pass: bool


def pairs() -> list[tuple[str, str]]:
    return [(ORDER[i], ORDER[j]) for i in range(len(ORDER)) for j in range(i + 1, len(ORDER))]


def lam(s: str) -> int:
    return int(SECTORS[s]["lambda"])


def dim(s: str) -> int:
    return int(SECTORS[s]["dim"])


def build_quadratic_weights() -> dict[str, Any]:
    return {
        "diagonal_coefficients_Tr_Phi_ii_squared": {s: 1 for s in ORDER},
        "offdiag_coefficients_norm_Phi_ij_squared": {f"{a}{b}": 2 for a, b in pairs()},
        "formula": "Tr(Phi^2)=sum_i Tr(Phi_ii^2)+2 sum_{i<j} ||Phi_ij||^2",
    }


def build_delta_phi_weights() -> dict[str, Any]:
    return {
        "diagonal_coefficients_Tr_Phi_ii_squared": {s: lam(s) for s in ORDER},
        "offdiag_coefficients_norm_Phi_ij_squared": {f"{a}{b}": lam(a) + lam(b) for a, b in pairs()},
        "formula": "Tr(Delta_1 Phi^2)=sum_i lambda_i Tr(Phi_ii^2)+sum_{i<j}(lambda_i+lambda_j)||Phi_ij||^2",
    }


def build_commutator_penalty() -> dict[str, Any]:
    weights = {f"{a}{b}": 2 * (lam(a) - lam(b)) ** 2 for a, b in pairs()}
    return {
        "offdiag_coefficients_norm_Phi_ij_squared": weights,
        "formula": "Tr([Delta_1,Phi]^*[Delta_1,Phi])=2 sum_{i<j}(lambda_i-lambda_j)^2||Phi_ij||^2",
        "ordered_by_cost": sorted(weights.items(), key=lambda item: item[1]),
    }


def build_minimal_ansatz() -> dict[str, Any]:
    return {
        "name": "minimal K-B Higgs/Yukawa interface",
        "nonzero_blocks": {
            "Phi_KB": "Y : B -> K",
            "Phi_BK": "Y* : K -> B",
            "Phi_BB": "H : B -> B",
        },
        "trace_Phi_squared": "2||Y||^2 + Tr(H^2)",
        "trace_Delta_Phi_squared": "4||Y||^2 + 4Tr(H^2)",
        "commutator_penalty": "32||Y||^2",
        "quartic_trace": "2Tr((Y Y*)^2)+4Tr(Y H^2 Y*)+Tr(H^4)",
        "why_minimal": "K-B is the cheapest nonzero bridge from the 81-dimensional kernel into massive sectors.",
    }


def build_quartic_rules() -> dict[str, Any]:
    return {
        "general_block_path_formula": "Tr(Phi^4)=sum_{i,j,k,l} Tr(Phi_ij Phi_jk Phi_kl Phi_li)",
        "path_condition": "only sector-compatible closed length-4 block paths contribute",
        "minimal_KB_formula": "2Tr((Y Y*)^2)+4Tr(Y H^2 Y*)+Tr(H^4)",
    }


def build_effective_fermion_mass() -> dict[str, Any]:
    return {
        "fermion_kernel": "K^+ direct_sum K^-",
        "dimension": 2 * dim("K"),
        "direct_kernel_dimension": dim("K"),
        "boundary_scale": "4 M_F^2",
        "algebraic_composite": "M_eff ~ Y H Y*",
        "integrated_boundary_composite": "M_eff ~ Y (4 M_F^2 + H)^(-1) Y*",
        "interpretation": "massless H1 modes acquire effective mass through the massive boundary/gauge sector",
    }


def build_result() -> ScalarYukawaBlockLedger:
    quad = build_quadratic_weights()
    delta = build_delta_phi_weights()
    comm = build_commutator_penalty()
    checks = {
        "total_dimension_240": sum(dim(s) for s in ORDER) == 240,
        "kernel_dimension_81": dim("K") == 81,
        "boundary_dimension_120": dim("B") == 120,
        "eigenvalues": [lam(s) for s in ORDER] == [0, 4, 10, 16],
        "KB_delta_weight_4": delta["offdiag_coefficients_norm_Phi_ij_squared"]["KB"] == 4,
        "KR_delta_weight_10": delta["offdiag_coefficients_norm_Phi_ij_squared"]["KR"] == 10,
        "KS_delta_weight_16": delta["offdiag_coefficients_norm_Phi_ij_squared"]["KS"] == 16,
        "KB_commutator_cost_32": comm["offdiag_coefficients_norm_Phi_ij_squared"]["KB"] == 32,
        "KR_commutator_cost_200": comm["offdiag_coefficients_norm_Phi_ij_squared"]["KR"] == 200,
        "KS_commutator_cost_512": comm["offdiag_coefficients_norm_Phi_ij_squared"]["KS"] == 512,
        "KB_cheapest_from_kernel": min(
            (comm["offdiag_coefficients_norm_Phi_ij_squared"][key], key)
            for key in ["KB", "KR", "KS"]
        )[1] == "KB",
        "fermion_double_162": 2 * dim("K") == 162,
    }
    return ScalarYukawaBlockLedger(
        part="CCCCCLXVII",
        title="Scalar/Yukawa Block Ledger on the W(3,3) 240-Carrier",
        sector_decomposition=SECTORS,
        quadratic_trace_weights=quad,
        delta_phi_squared_weights=delta,
        commutator_gap_penalty=comm,
        minimal_KB_ansatz=build_minimal_ansatz(),
        quartic_block_rules=build_quartic_rules(),
        effective_fermion_mass=build_effective_fermion_mass(),
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "scalar/Yukawa block checks failed"
    out = Path("data/PART_CCCCCLXVII_scalar_yukawa_block_ledger_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
