#!/usr/bin/env python3
"""
PART_CCCCCLXVIII_minimal_kb_seesaw_singular_values.py

Executable symbolic artifact for the minimal K-B Higgs/Yukawa ansatz.

The ansatz is

    Phi_min = [[0, Y], [Y*, h I_B]]

on K + B with dim K = 81 and dim B = 120.  The bridge
Y : B -> K has rank at most 81, forcing a residual 39-dimensional
boundary sector at maximal rank.

This script records the singular-value reduction:

    S2 = sum sigma_i^2
    S4 = sum sigma_i^4

and the exact W(3,3) trace/seesaw formulas.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any

DIM_K = 81
DIM_B = 120
LAMBDA_K = 0
LAMBDA_B = 4
RANK_D1 = 39


@dataclass(frozen=True)
class MinimalKBSeesaw:
    part: str
    title: str
    ansatz: dict[str, Any]
    rank_lock: dict[str, Any]
    singular_value_invariants: dict[str, str]
    trace_formulas: dict[str, str]
    effective_mass_formulas: dict[str, str]
    potential_ledger: dict[str, str]
    checks: dict[str, bool]
    all_checks_pass: bool


def build_result() -> MinimalKBSeesaw:
    max_rank = min(DIM_K, DIM_B)
    residual_B = DIM_B - max_rank
    commutator_cost_KB = 2 * (LAMBDA_B - LAMBDA_K) ** 2
    delta_phi_weight_KB = LAMBDA_K + LAMBDA_B

    checks = {
        "max_rank_81": max_rank == 81,
        "forced_residual_B_39": residual_B == 39,
        "residual_matches_rank_d1": residual_B == RANK_D1,
        "dimension_split_120_81_39": DIM_B == DIM_K + RANK_D1,
        "delta_phi_KB_weight_4": delta_phi_weight_KB == 4,
        "commutator_KB_cost_32": commutator_cost_KB == 32,
        "fermion_double_162": 2 * DIM_K == 162,
    }

    return MinimalKBSeesaw(
        part="CCCCCLXVIII",
        title="Minimal K-B Seesaw and Singular-Value Reduction",
        ansatz={
            "carrier": "K direct_sum B",
            "dim_K": DIM_K,
            "dim_B": DIM_B,
            "Phi_min": "[[0,Y],[Y*,h I_B]]",
            "Y": "B_120 -> K_81",
            "H": "h I_B",
            "boundary_eigenvalue": LAMBDA_B,
            "kernel_eigenvalue": LAMBDA_K,
        },
        rank_lock={
            "rank_Y_bound": "rank(Y) <= min(81,120) = 81",
            "max_rank": max_rank,
            "forced_boundary_nullity": residual_B,
            "identity": "120 = 81 + 39",
            "rank_d1": RANK_D1,
            "interpretation": "maximal K-B Yukawa bridge leaves a 39-dimensional residual boundary sector matching rank(d1)=|V|-1",
        },
        singular_value_invariants={
            "sigma_i": "nonzero singular values of Y",
            "S2": "sum_i sigma_i^2 = ||Y||^2",
            "S4": "sum_i sigma_i^4 = Tr((Y Y*)^2)",
            "rank": "number of nonzero sigma_i",
        },
        trace_formulas={
            "Tr_Phi_min_squared": "2 S2 + 120 h^2",
            "Tr_Delta_Phi_min_squared": "4 S2 + 480 h^2",
            "commutator_penalty": "32 S2",
            "Tr_Phi_min_fourth": "2 S4 + 4 h^2 S2 + 120 h^4",
        },
        effective_mass_formulas={
            "fermion_carrier": "K^+ direct_sum K^-",
            "fermion_dimension": str(2 * DIM_K),
            "algebraic_mass_operator": "M_alg = h Y Y*",
            "algebraic_mass_eigenvalues": "h sigma_i^2",
            "integrated_boundary_operator": "M_eff = (4 M_F^2 + h)^(-1) Y Y*",
            "integrated_boundary_eigenvalues": "sigma_i^2/(4 M_F^2 + h)",
            "heavy_boundary_limit": "sigma_i^2/(4 M_F^2)",
            "massive_kernel_modes": "rank(Y)",
            "residual_massless_kernel_modes": "81 - rank(Y)",
        },
        potential_ledger={
            "V_hY": "alpha(2S2+120h^2)+beta(2S4+4h^2S2+120h^4)+gamma(32S2)+delta(4S2+480h^2)",
            "free_invariants": "h, S2, S4, rank(Y), singular-value distribution of Y",
            "next_required_structure": "choose a canonical W(3,3)-equivariant or incidence-derived Y",
        },
        checks=checks,
        all_checks_pass=all(checks.values()),
    )


def main() -> None:
    result = build_result()
    payload = asdict(result)
    print(json.dumps(payload, indent=2))
    assert result.all_checks_pass, "minimal K-B seesaw checks failed"
    out = Path("data/PART_CCCCCLXVIII_minimal_kb_seesaw_singular_values_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
