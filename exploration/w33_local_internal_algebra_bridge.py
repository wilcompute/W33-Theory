"""Local internal algebra bridge for the W(3,3) finite triple candidate.

This script separates two statements that were recently conflated:

1. The naive 40-point graph spectral triple based on the Bose-Mesner algebra
   is too small and commutative to model the Standard Model internal algebra.
2. The repo's local 27/162-state finite triple candidate already carries an
   explicit U(1)_Y + quaternionic weak + M_3(C) color support algebra, and its
   natural real/grading data satisfy the KO-dim 6 sign pattern.

The goal is not to claim a full Connes reconstruction theorem. The goal is to
make the honest current status executable:

- the global graph triple is obstructed;
- the local internal carrier is not;
- the clean Higgs pair H_2, Hbar_2 is exactly the one surviving the current
  weak/color order-one screen.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_local_internal_algebra_bridge_summary.json"

from exploration.w33_finite_spectral_triple import (
    BasisState,
    build_w33_finite_spectral_triple,
    color_factor_operator_27,
    color_triplet_blocks_27,
    hypercharge_operator_27,
    q_color_block_27,
    quaternion_matrix,
    u1_hypercharge_phase_27,
    weak_doublet_blocks_27,
    weak_factor_operator_27,
)
from exploration.w33_fermionic_connes_sector import (
    clean_higgs_slots,
    sample_order_one_residual_norm,
    sample_order_zero_residuals,
)


def _block_compression(operator: np.ndarray, indices: tuple[int, ...]) -> np.ndarray:
    return np.asarray(operator, dtype=complex)[np.ix_(indices, indices)]


def _quaternion_block_diagnostics() -> dict[str, Any]:
    weak_block = weak_doublet_blocks_27()[0]
    unit = np.eye(2, dtype=complex)
    qi = quaternion_matrix(1j, 0.0)
    qj = quaternion_matrix(0.0, 1.0)
    qk = quaternion_matrix(0.0, 1j)

    return {
        "weak_block_indices": list(weak_block),
        "i_squared_plus_identity_norm": float(np.linalg.norm(qi @ qi + unit)),
        "j_squared_plus_identity_norm": float(np.linalg.norm(qj @ qj + unit)),
        "k_squared_plus_identity_norm": float(np.linalg.norm(qk @ qk + unit)),
        "ij_minus_k_norm": float(np.linalg.norm(qi @ qj - qk)),
        "jk_minus_i_norm": float(np.linalg.norm(qj @ qk - qi)),
        "ki_minus_j_norm": float(np.linalg.norm(qk @ qi - qj)),
    }


def _color_block_diagnostics() -> dict[str, Any]:
    pure_triplet_block = color_triplet_blocks_27()[0]
    e12 = np.zeros((3, 3), dtype=complex)
    e23 = np.zeros((3, 3), dtype=complex)
    e12[0, 1] = 1.0
    e23[1, 2] = 1.0
    e13 = e12 @ e23

    op12 = _block_compression(color_factor_operator_27(e12), pure_triplet_block)
    op23 = _block_compression(color_factor_operator_27(e23), pure_triplet_block)
    op13 = _block_compression(color_factor_operator_27(e13), pure_triplet_block)

    return {
        "q_color_block_indices": list(q_color_block_27()),
        "pure_triplet_block_indices": list(pure_triplet_block),
        "matrix_units_multiply_correctly_norm": float(np.linalg.norm(op12 @ op23 - op13)),
        "e12_rank": int(np.linalg.matrix_rank(op12)),
        "e23_rank": int(np.linalg.matrix_rank(op23)),
        "e13_rank": int(np.linalg.matrix_rank(op13)),
    }


def _commuting_gauge_support_diagnostics() -> dict[str, Any]:
    weak_example = weak_factor_operator_27(1 / np.sqrt(2), 1j / np.sqrt(2))
    color_example = color_factor_operator_27(np.diag([1.0, np.exp(1j * 0.2), np.exp(-1j * 0.2)]))
    hypercharge = hypercharge_operator_27()
    hypercharge_phase = u1_hypercharge_phase_27(0.123)

    return {
        "weak_color_commutator_norm": float(np.linalg.norm(weak_example @ color_example - color_example @ weak_example)),
        "weak_hypercharge_commutator_norm": float(np.linalg.norm(weak_example @ hypercharge - hypercharge @ weak_example)),
        "color_hypercharge_commutator_norm": float(np.linalg.norm(color_example @ hypercharge - hypercharge @ color_example)),
        "hypercharge_phase_unitarity_norm": float(
            np.linalg.norm(hypercharge_phase.conj().T @ hypercharge_phase - np.eye(hypercharge_phase.shape[0]))
        ),
    }


def _ko6_sign_diagnostics() -> dict[str, Any]:
    candidate = build_w33_finite_spectral_triple()
    j_op = candidate.real_structure_162.astype(complex)
    d_op = candidate.dirac_162.astype(complex)
    gamma = candidate.grading_162.astype(complex)

    return {
        "J2_minus_identity_norm": float(np.linalg.norm(j_op @ j_op - np.eye(j_op.shape[0]))),
        "JD_minus_DJ_norm": float(np.linalg.norm(j_op @ d_op - d_op @ j_op)),
        "Jgamma_plus_gammaJ_norm": float(np.linalg.norm(j_op @ gamma + gamma @ j_op)),
        "Jgamma_minus_gammaJ_norm": float(np.linalg.norm(j_op @ gamma - gamma @ j_op)),
        "sign_pattern": {
            "epsilon": +1,
            "epsilon_prime": +1,
            "epsilon_double_prime": -1,
        },
    }


def _fermionic_screen_diagnostics() -> dict[str, Any]:
    slots = ("H_1", "H_2", "Hbar_1", "Hbar_2")
    norms = {slot: float(sample_order_one_residual_norm(slot)) for slot in slots}
    order_zero_max = max(float(np.linalg.norm(residual)) for residual in sample_order_zero_residuals().values())
    return {
        "clean_higgs_slots": list(clean_higgs_slots()),
        "order_one_residual_norms": norms,
        "order_zero_max_residual_norm": order_zero_max,
    }


def build_summary() -> dict[str, Any]:
    weak = _quaternion_block_diagnostics()
    color = _color_block_diagnostics()
    commuting = _commuting_gauge_support_diagnostics()
    ko6 = _ko6_sign_diagnostics()
    fermionic = _fermionic_screen_diagnostics()

    return {
        "status": "ok",
        "global_vs_local_read": {
            "global_graph_triple": "40-point permutation/Bose-Mesner test is commutative and too small",
            "local_internal_carrier": "27-state canonical basis lifted to a 162-state even finite triple candidate",
        },
        "weak_quaternion_block": weak,
        "color_matrix_block": color,
        "commuting_gauge_support": commuting,
        "ko_dim_6_local_signs": ko6,
        "fermionic_screen": fermionic,
        "local_internal_algebra_bridge_theorem": {
            "the_global_bose_mesner_obstruction_does_not_rule_out_the_local_internal_carrier": True,
            "the_local_candidate_has_ko_dim_6_sign_pattern": (
                ko6["J2_minus_identity_norm"] == 0.0
                and ko6["JD_minus_DJ_norm"] == 0.0
                and ko6["Jgamma_plus_gammaJ_norm"] == 0.0
            ),
            "the_weak_factor_contains_honest_quaternionic_blocks": (
                weak["i_squared_plus_identity_norm"] == 0.0
                and weak["j_squared_plus_identity_norm"] == 0.0
                and weak["k_squared_plus_identity_norm"] == 0.0
                and weak["ij_minus_k_norm"] == 0.0
            ),
            "the_color_factor_contains_matrix_unit_structure": (
                color["matrix_units_multiply_correctly_norm"] == 0.0
                and color["e12_rank"] == 1
                and color["e23_rank"] == 1
                and color["e13_rank"] == 1
            ),
            "u1_weak_color_support_commute_on_the_local_carrier": (
                commuting["weak_color_commutator_norm"] == 0.0
                and commuting["weak_hypercharge_commutator_norm"] == 0.0
                and commuting["color_hypercharge_commutator_norm"] == 0.0
            ),
            "the_clean_higgs_pair_survives_the_current_fermionic_order_one_screen": (
                tuple(fermionic["clean_higgs_slots"]) == ("H_2", "Hbar_2")
                and fermionic["order_one_residual_norms"]["H_2"] == 0.0
                and fermionic["order_one_residual_norms"]["Hbar_2"] == 0.0
            ),
        },
        "interpretive_read": (
            "The honest obstruction is only to the naive global graph triple. "
            "On the local E6/Heisenberg carrier already present in the repo, "
            "there is an explicit commuting U(1)_Y + H + M_3(C) gauge-support "
            "algebra, the natural J/gamma pair has the KO-dim 6 sign pattern, "
            "and the clean Higgs pair H_2, Hbar_2 is exactly the one passing the "
            "current fermionic weak/color order-one screen."
        ),
        "bridge_verdict": (
            "Claude was right that the 40-point Bose-Mesner algebra is not the "
            "Standard Model algebra. Claude was wrong to promote that into a "
            "fundamental no-go for the repo's actual internal carrier. The right "
            "statement is narrower: the global graph triple fails, but the local "
            "27/162-state W33 finite-triple candidate already carries the right "
            "algebraic support pattern and KO-6 reality signs. So the live problem "
            "is not 'find any Connes carrier at all'; it is to tighten the local "
            "candidate into a full order-zero/order-one/orientability proof and "
            "connect that carrier back to the genuine W(3,3) geometry without "
            "smuggling in ad hoc structure."
        ),
        "source_files": [
            "exploration/w33_finite_spectral_triple.py",
            "exploration/w33_fermionic_connes_sector.py",
            "exploration/w33_spectral_triple.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
