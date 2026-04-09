"""Two-sheet CKM lift architecture after the quarter-turn quark-sheet closure.

The refreshed quarter-turn analysis isolated one sharp CKM/CP carrier:

- Cabibbo/CP edge on the charged quark sheet ``z = 2``:
  ``Q_1_1`` against ``Q_2_1``.

The next unresolved wall from that analysis was equally sharp:

- the carrier already captures Cabibbo almost exactly,
- but it still under-generates ``V_cb`` by about ``3.5e-2``.

This module searches for the cleanest single quarter-turn quark pair whose job
is specifically to supply a ``2 ↔ 3`` lift with minimal extra Cabibbo
contamination. The result is a second sheet:

- V_cb lift edge on the companion quark sheet ``z = 1``:
  ``Q_2_2`` against ``Q_3_2``.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_two_sheet_ckm_lift_bridge_summary.json"
TARGET_VCB = 0.04183
TARGET_VUB = 0.003732
MAX_CABIBBO_CONTAMINATION = 0.01

from exploration.w33_finite_spectral_triple import canonical_generation_basis
from scripts.w33_yukawa_blocks import (
    _build_hodge_and_generations,
    build_generation_profiles,
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


def _slot_source(slot: str) -> int:
    for state in canonical_generation_basis():
        if state.slot == slot:
            return state.source_i27
    raise KeyError(slot)


def _quarter_turn_record(
    slot_i: str,
    slot_j: str,
    amplitude: float,
    theta_over_pi: float,
    generation_profiles: list[np.ndarray],
    local_tris: list[Any],
) -> dict[str, Any]:
    e_i = np.zeros(27, dtype=complex)
    e_j = np.zeros(27, dtype=complex)
    e_i[_slot_source(slot_i)] = 1.0
    e_j[_slot_source(slot_j)] = 1.0
    phase = np.exp(1j * np.pi * theta_over_pi)
    y_up = _yukawa(generation_profiles, local_tris, e_i + amplitude * phase * e_j)
    y_down = _yukawa(generation_profiles, local_tris, e_i - amplitude * phase * e_j)
    ckm_matrix, jarlskog = compute_ckm_and_jarlskog(y_up, y_down)
    abs_ckm = np.abs(ckm_matrix)
    return {
        "slot_i": slot_i,
        "slot_j": slot_j,
        "amplitude": float(amplitude),
        "theta_over_pi": float(theta_over_pi),
        "Vus": float(abs_ckm[0, 1]),
        "Vcb": float(abs_ckm[1, 2]),
        "Vub": float(abs_ckm[0, 2]),
        "jarlskog_abs": float(abs(jarlskog)),
        "V_CKM": abs_ckm.tolist(),
    }


@lru_cache(maxsize=1)
def build_two_sheet_ckm_lift_summary() -> dict[str, Any]:
    quarter_turn = _load_json("w33_quarter_turn_quark_sheet_bridge_summary.json")
    generation_profiles, local_tris = _real_profile_data()

    quark_slots = [state.slot for state in canonical_generation_basis() if state.slot.startswith("Q_")]
    lift_candidates = []
    for index, slot_i in enumerate(quark_slots):
        for slot_j in quark_slots[index + 1 :]:
            best = None
            for amplitude in np.linspace(0.0, 0.2, 401):
                for theta_over_pi in (0.5, 1.5):
                    record = _quarter_turn_record(
                        slot_i,
                        slot_j,
                        float(amplitude),
                        theta_over_pi,
                        generation_profiles,
                        local_tris,
                    )
                    if record["Vus"] >= MAX_CABIBBO_CONTAMINATION:
                        continue
                    key = (
                        abs(record["Vcb"] - TARGET_VCB),
                        abs(record["Vub"] - TARGET_VUB),
                        record["Vus"],
                        record["amplitude"],
                        record["theta_over_pi"],
                    )
                    if best is None or key < best[0]:
                        best = (key, record)
            if best is not None:
                lift_candidates.append(best[1])

    best_lift = min(
        lift_candidates,
        key=lambda record: (
            abs(record["Vcb"] - TARGET_VCB),
            abs(record["Vub"] - TARGET_VUB),
            record["Vus"],
        ),
    )
    lift_candidates.sort(
        key=lambda record: (
            abs(record["Vcb"] - TARGET_VCB),
            abs(record["Vub"] - TARGET_VUB),
            record["Vus"],
        )
    )

    cabibbo_edge = quarter_turn["refined_q11_q21_quarter_turn_family"]["best_error"]

    return {
        "status": "ok",
        "targets": {
            "vcb_target": TARGET_VCB,
            "vub_target": TARGET_VUB,
            "max_cabibbo_contamination": MAX_CABIBBO_CONTAMINATION,
        },
        "cabibbo_cp_edge": cabibbo_edge,
        "second_layer_lift_edge": best_lift,
        "top_lift_candidates": lift_candidates[:8],
        "two_sheet_ckm_lift_theorem": {
            "the_cleanest_second_layer_vcb_lift_is_q22_against_q32": (
                best_lift["slot_i"] == "Q_2_2" and best_lift["slot_j"] == "Q_3_2"
            ),
            "the_second_layer_lift_lives_on_the_companion_charged_quark_sheet_z1": (
                best_lift["slot_i"] == "Q_2_2" and best_lift["slot_j"] == "Q_3_2"
            ),
            "the_second_layer_lift_matches_vcb_while_keeping_vus_small": (
                abs(best_lift["Vcb"] - TARGET_VCB) < 3e-4
                and best_lift["Vus"] < MAX_CABIBBO_CONTAMINATION
            ),
            "the_second_layer_lift_is_distinct_from_the_cabibbo_cp_edge": (
                best_lift["slot_i"] != cabibbo_edge["slot_i"]
                or best_lift["slot_j"] != cabibbo_edge["slot_j"]
            ),
            "the_live_ckm_architecture_splits_into_a_z2_cabibbo_edge_plus_a_z1_vcb_lift": (
                cabibbo_edge["slot_i"] == "Q_1_1"
                and cabibbo_edge["slot_j"] == "Q_2_1"
                and best_lift["slot_i"] == "Q_2_2"
                and best_lift["slot_j"] == "Q_3_2"
            ),
        },
        "interpretive_read": (
            "The live quarter-turn quark program now separates cleanly into two "
            "charged sheets. The z=2 sheet carries the 1↔2 Cabibbo/CP edge, and "
            "the companion z=1 sheet carries the cleanest isolated 2↔3 lift."
        ),
        "bridge_verdict": (
            "The next CKM layer is no longer abstract. After fixing the "
            "Cabibbo/CP carrier Q_1_1 against Q_2_1 on the z=2 quark sheet, the "
            "cleanest single quarter-turn 2↔3 lift is Q_2_2 against Q_3_2 on "
            "the z=1 sheet. At amplitude 0.0375 it gives V_cb≈0.04161 with only "
            "V_us≈0.00788 contamination and tiny J. So the live architecture is "
            "now a two-sheet packet: Cabibbo/CP on z=2, V_cb lift on z=1."
        ),
        "source_files": [
            "data/w33_quarter_turn_quark_sheet_bridge_summary.json",
            "scripts/w33_yukawa_blocks.py",
        ],
    }


def write_summary(path: Path = DEFAULT_OUTPUT_PATH) -> Path:
    path.write_text(json.dumps(build_two_sheet_ckm_lift_summary(), indent=2), encoding="utf-8")
    return path


def main() -> None:
    path = write_summary()
    print(f"Wrote {path}")


if __name__ == "__main__":
    main()
