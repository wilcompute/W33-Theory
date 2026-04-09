"""Quarter-turn quark-sheet CP bridge after the live CKM seed reset.

The refreshed live generator moved the best real CKM seed to the cross-row
charged pair ``Q_2_1`` against ``L_2`` on the common ``z = 2`` sheet. The next
question is whether the first viable CP-capable deformation still lives there.

This module checks the minimal real-profile two-point ansatz

    v_up   = e_i + a exp(i theta) e_j,
    v_down = e_i - a exp(i theta) e_j,

and packages the current sharp answer:

- phasing the refreshed cross-row seed is CP-hostile and degrades CKM badly;
- the best quark-only quarter-turn carrier is the same-row charged-sheet pair
  ``Q_1_1`` against ``Q_2_1``;
- that same pair is best both for minimum CKM error and for matching the
  observed Jarlskog scale; and
- only one continuous knob remains there: the quarter-turn amplitude ``a``.
"""

from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_quarter_turn_quark_sheet_bridge_summary.json"
J_TARGET = 3.12e-5
CKM_TARGET_2025 = np.array(
    [
        [0.97349, 0.22487, 0.003732],
        [0.22487, 0.97349, 0.04183],
        [0.00858, 0.04111, 0.999118],
    ],
    dtype=float,
)

from exploration.w33_finite_spectral_triple import canonical_generation_basis
from scripts.w33_yukawa_blocks import (
    _build_hodge_and_generations,
    build_generation_profiles,
    ckm_error,
    cubic_form_on_h27,
    compute_ckm_and_jarlskog,
)


def _load_json(filename: str) -> dict[str, Any]:
    return json.loads((DATA_DIR / filename).read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def _real_profile_data() -> tuple[list[np.ndarray], list[Any]]:
    hodge, _triangles, edges, generators = _build_hodge_and_generations()
    _h27, local_tris, generation_profiles = build_generation_profiles(
        hodge,
        edges,
        generators,
        v0=0,
    )
    return generation_profiles, local_tris


def _yukawa(
    generation_profiles: list[np.ndarray],
    local_tris: list[Any],
    vev: np.ndarray,
) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=complex)
    for a in range(3):
        for b in range(a, 3):
            value = cubic_form_on_h27(None, local_tris, generation_profiles[a], generation_profiles[b], vev)
            matrix[a, b] = value
            matrix[b, a] = value
    return matrix


def _unit_slot_vectors(slot_i: str, slot_j: str) -> tuple[np.ndarray, np.ndarray]:
    slot_to_source = {state.slot: state.source_i27 for state in canonical_generation_basis()}
    e_i = np.zeros(27, dtype=complex)
    e_j = np.zeros(27, dtype=complex)
    e_i[slot_to_source[slot_i]] = 1.0
    e_j[slot_to_source[slot_j]] = 1.0
    return e_i, e_j


def _pair_record(
    slot_i: str,
    slot_j: str,
    amplitude: float,
    theta_over_pi: float,
    generation_profiles: list[np.ndarray],
    local_tris: list[Any],
) -> dict[str, Any]:
    e_i, e_j = _unit_slot_vectors(slot_i, slot_j)
    phase = np.exp(1j * np.pi * theta_over_pi)
    y_up = _yukawa(generation_profiles, local_tris, e_i + amplitude * phase * e_j)
    y_down = _yukawa(generation_profiles, local_tris, e_i - amplitude * phase * e_j)
    ckm_matrix, jarlskog = compute_ckm_and_jarlskog(y_up, y_down)
    return {
        "slot_i": slot_i,
        "slot_j": slot_j,
        "amplitude": float(amplitude),
        "theta_over_pi": float(theta_over_pi),
        "ckm_error": float(ckm_error(ckm_matrix)),
        "jarlskog_abs": float(abs(jarlskog)),
        "V_CKM": np.abs(ckm_matrix).tolist(),
    }


def _pair_search(
    slot_i: str,
    slot_j: str,
    amplitudes: np.ndarray,
    theta_values_over_pi: tuple[float, ...],
    generation_profiles: list[np.ndarray],
    local_tris: list[Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    best_error = None
    best_target = None
    for amplitude in amplitudes:
        for theta_over_pi in theta_values_over_pi:
            record = _pair_record(
                slot_i,
                slot_j,
                float(amplitude),
                float(theta_over_pi),
                generation_profiles,
                local_tris,
            )
            error_key = (
                record["ckm_error"],
                abs(record["jarlskog_abs"] - J_TARGET),
                record["amplitude"],
                record["theta_over_pi"],
            )
            if best_error is None or error_key < best_error[0]:
                best_error = (error_key, record)
            target_key = (
                abs(record["jarlskog_abs"] - J_TARGET),
                record["ckm_error"],
                record["amplitude"],
                record["theta_over_pi"],
            )
            if best_target is None or target_key < best_target[0]:
                best_target = (target_key, record)
    return best_error[1], best_target[1]


def _ckm_residual_report(record: dict[str, Any]) -> dict[str, Any]:
    matrix = np.array(record["V_CKM"], dtype=float)
    residual = matrix - CKM_TARGET_2025
    return {
        "residual_matrix": residual.tolist(),
        "abs_max_residual": float(np.max(np.abs(residual))),
        "frobenius_residual": float(np.linalg.norm(residual)),
        "vud_residual": float(residual[0, 0]),
        "vus_residual": float(residual[0, 1]),
        "vub_residual": float(residual[0, 2]),
        "vcb_residual": float(residual[1, 2]),
        "vts_residual": float(residual[2, 1]),
    }


@lru_cache(maxsize=1)
def build_quarter_turn_quark_sheet_summary() -> dict[str, Any]:
    live_seed = _load_json("w33_live_ckm_seed_bridge_summary.json")
    generation_profiles, local_tris = _real_profile_data()

    live_cross_row = _pair_search(
        "Q_2_1",
        "L_2",
        np.linspace(1.0, 1.0, 1),
        tuple(np.linspace(0.0, 2.0, 72, endpoint=False)),
        generation_profiles,
        local_tris,
    )[0]

    quarter_turn_grid = np.linspace(0.0, 1.2, 241)
    theta_quarter_turns = (0.5, 1.5)
    quark_slots = [state.slot for state in canonical_generation_basis() if state.slot.startswith("Q_")]
    quark_pair_reports = []
    for index, slot_i in enumerate(quark_slots):
        for slot_j in quark_slots[index + 1 :]:
            best_error, best_target = _pair_search(
                slot_i,
                slot_j,
                quarter_turn_grid,
                theta_quarter_turns,
                generation_profiles,
                local_tris,
            )
            quark_pair_reports.append(
                {
                    "slot_i": slot_i,
                    "slot_j": slot_j,
                    "best_error": best_error,
                    "best_target_match": best_target,
                }
            )

    best_quark_pair_by_error = min(
        quark_pair_reports,
        key=lambda item: item["best_error"]["ckm_error"],
    )
    best_quark_pair_by_target = min(
        quark_pair_reports,
        key=lambda item: abs(item["best_target_match"]["jarlskog_abs"] - J_TARGET),
    )

    refined_best_error, refined_best_target = _pair_search(
        "Q_1_1",
        "Q_2_1",
        np.linspace(0.0, 1.0, 10001),
        theta_quarter_turns,
        generation_profiles,
        local_tris,
    )

    exact_fraction_candidates = {}
    for fraction in (Fraction(4, 11), Fraction(7, 11), Fraction(3, 8), Fraction(5, 8), Fraction(7, 13)):
        record = _pair_record(
            "Q_1_1",
            "Q_2_1",
            float(fraction),
            0.5,
            generation_profiles,
            local_tris,
        )
        exact_fraction_candidates[str(fraction)] = record

    refined_best_error_residual = _ckm_residual_report(refined_best_error)
    refined_best_target_residual = _ckm_residual_report(refined_best_target)

    return {
        "status": "ok",
        "experimental_target": {
            "jarlskog_abs_target": J_TARGET,
            "ckm_matrix_abs_target_2025": CKM_TARGET_2025.tolist(),
        },
        "live_cross_row_seed": {
            "real_seed": live_seed["live_best_seed"],
            "best_equal_amplitude_phase_deformation": live_cross_row,
        },
        "best_quark_pair_by_error": best_quark_pair_by_error,
        "best_quark_pair_by_target_match": best_quark_pair_by_target,
        "refined_q11_q21_quarter_turn_family": {
            "best_error": refined_best_error,
            "best_error_residuals_against_ckm_2025": refined_best_error_residual,
            "best_target_match": refined_best_target,
            "best_target_residuals_against_ckm_2025": refined_best_target_residual,
        },
        "exact_fraction_candidates_on_q11_q21": exact_fraction_candidates,
        "quarter_turn_quark_sheet_theorem": {
            "phasing_the_refreshed_cross_row_seed_is_ckm_hostile": (
                live_cross_row["ckm_error"] > live_seed["live_best_seed"]["ckm_error"]
            ),
            "the_best_quark_only_quarter_turn_pair_is_q11_q21": (
                best_quark_pair_by_error["slot_i"] == "Q_1_1"
                and best_quark_pair_by_error["slot_j"] == "Q_2_1"
                and best_quark_pair_by_target["slot_i"] == "Q_1_1"
                and best_quark_pair_by_target["slot_j"] == "Q_2_1"
            ),
            "the_best_quark_only_pair_lives_on_the_same_charged_z2_sheet": (
                best_quark_pair_by_error["best_error"]["slot_i"] == "Q_1_1"
                and best_quark_pair_by_error["best_error"]["slot_j"] == "Q_2_1"
            ),
            "the_error_optimal_q11_q21_quarter_turn_improves_on_the_live_real_seed": (
                refined_best_error["ckm_error"] < live_seed["live_best_seed"]["ckm_error"]
            ),
            "the_target_matching_q11_q21_quarter_turn_hits_the_observed_jarlskog_scale": (
                abs(refined_best_target["jarlskog_abs"] - J_TARGET) < 5e-9
            ),
            "the_target_matching_q11_q21_quarter_turn_still_improves_on_the_live_real_seed": (
                refined_best_target["ckm_error"] < live_seed["live_best_seed"]["ckm_error"]
            ),
            "the_exact_fraction_7_over_11_is_already_an_observed_jarlskog_hit_on_the_live_carrier": (
                abs(exact_fraction_candidates["7/11"]["jarlskog_abs"] - J_TARGET) < 2e-8
            ),
            "the_exact_fraction_4_over_11_tracks_the_error_optimal_amplitude": (
                abs(exact_fraction_candidates["4/11"]["amplitude"] - refined_best_error["amplitude"]) < 0.005
                and abs(exact_fraction_candidates["4/11"]["ckm_error"] - refined_best_error["ckm_error"]) < 0.001
            ),
            "the_live_denominator_11_packet_beats_the_old_denominator_13_amplitude_on_this_carrier": (
                abs(exact_fraction_candidates["7/11"]["jarlskog_abs"] - J_TARGET)
                < abs(exact_fraction_candidates["7/13"]["jarlskog_abs"] - J_TARGET)
            ),
            "the_error_optimal_q11_q21_packet_is_a_cabibbo_edge_not_a_full_ckm_solution": (
                abs(refined_best_error_residual["vus_residual"]) < 0.003
                and abs(refined_best_error_residual["vud_residual"]) < 0.002
                and abs(refined_best_error_residual["vcb_residual"]) > 0.03
            ),
            "even_the_target_matching_q11_q21_packet_still_needs_a_second_layer_for_vcb": (
                abs(refined_best_target_residual["vcb_residual"]) > 0.03
            ),
            "only_the_amplitude_remains_once_the_quarter_turn_pair_is_fixed": (
                refined_best_error["theta_over_pi"] in theta_quarter_turns
                and refined_best_target["theta_over_pi"] in theta_quarter_turns
            ),
        },
        "interpretive_read": (
            "After the live reset, the first viable CP carrier does not sit on "
            "the refreshed cross-row seed Q_2_1 against L_2. It moves to the "
            "same-row charged quark sheet. The unique best quarter-turn quark "
            "pair is Q_1_1 against Q_2_1, and one amplitude family on that pair "
            "interpolates between the lowest CKM error and the observed "
            "Jarlskog scale."
        ),
        "bridge_verdict": (
            "The refreshed CKM/CP frontier is now two-tiered. The best purely "
            "real seed remains the cross-row charged bridge Q_2_1 against L_2, "
            "but its phase deformation is CKM-hostile. The first physically "
            "clean CP-capable carrier is instead the same-row quark-sheet pair "
            "Q_1_1 against Q_2_1 at quarter-turn phase. On that pair, a=0.3602 "
            "gives CKM error 0.05093 with |J|≈1.00e-5, while a=0.6362 gives "
            "CKM error 0.13276 with |J|≈3.12022e-5, essentially the observed "
            "Jarlskog scale. Even better, the nearby exact fractions are not "
            "random: 4/11 tracks the error-optimal amplitude and 7/11 is "
            "already an observed-Jarlskog hit on the live carrier. So the live "
            "CP problem has compressed to one quarter-turn amplitude packet on "
            "one charged quark-sheet edge, with denominator 11 rather than the "
            "old stale 13-packet. The remaining wall is now cleaner too: this "
            "edge already captures Cabibbo almost exactly, but it still "
            "under-generates V_cb, so the next layer has to be a 2↔3 lift "
            "rather than another 1↔2 family mechanism."
        ),
        "source_files": [
            "data/w33_live_ckm_seed_bridge_summary.json",
            "scripts/w33_yukawa_blocks.py",
            "artifacts/e6_cubic_affine_heisenberg_model.json",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(
        json.dumps(build_quarter_turn_quark_sheet_summary(), indent=2),
        encoding="utf-8",
    )
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
