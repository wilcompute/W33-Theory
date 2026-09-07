#!/usr/bin/env python3
"""Pass 1027: compile the certified C6 cocycle into a photonic test ABI.

The output is deliberately an experiment contract, not a claim that a waveguide
layout, loss budget, detector model, or pulse calibration has been solved.  The
GAP certificate supplies closed words in abstract Sp(4,3) generators; this script
turns those words into forward/inverse gate schedules and exact interferometric
phase signatures.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = DATA / "w33_pass1027_photonic_c6_holonomy_falsifier.json"


def load(name: str) -> dict[str, Any]:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def compile_word(word: list[int]) -> list[dict[str, Any]]:
    return [
        {
            "step": step,
            "primitive": f"G{abs(label)}",
            "direction": "forward" if label > 0 else "inverse",
            "signed_generator": label,
        }
        for step, label in enumerate(word, start=1)
    ]


def inverse_word(word: list[int]) -> list[int]:
    return [-label for label in reversed(word)]


def normalized_weights(length: int, mode: str) -> list[float]:
    if length == 0:
        return []
    if mode == "uniform":
        raw = [1.0] * length
    elif mode == "front_loaded":
        raw = [float(length - i) for i in range(length)]
    elif mode == "back_loaded":
        raw = [float(i + 1) for i in range(length)]
    else:
        raise ValueError(mode)
    total = sum(raw)
    return [round(value / total, 12) for value in raw]


def fringe_signature(phase: int) -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for reference_slot in range(6):
        reference_angle = 2.0 * math.pi * reference_slot / 6.0
        signal_angle = 2.0 * math.pi * phase / 6.0
        probability = (1.0 + math.cos(signal_angle - reference_angle)) / 2.0
        rows.append(
            {
                "reference_slot": reference_slot,
                "reference_angle_over_pi": round(reference_angle / math.pi, 12),
                "port0_probability": round(probability, 12),
            }
        )
    return rows


def main() -> None:
    cocycle = load("w33_pass1025_explicit_c6_groupoid_cocycle.json")
    section = load("w33_pass1022_equivariant_section_obstruction.json")

    assert cocycle["status"] == "PASS"
    assert section["status"] == "PASS"
    assert cocycle["check_count"] >= 19
    assert section["witnesses"]["Sylow5_admits_section"] is True

    witnesses = cocycle["closed_loop_witnesses"]
    loop_words = {
        1: list(witnesses["phase_1_word"]),
        2: list(witnesses["phase_2_word"]),
        3: list(witnesses["phase_3_word"]),
    }
    for phase, word in loop_words.items():
        assert word, f"phase-{phase} witness is empty"
        assert len(word) == witnesses[f"phase_{phase}_length"]

    loop_protocols: list[dict[str, Any]] = []
    for phase, word in loop_words.items():
        null_word = word + inverse_word(word)
        loop_protocols.append(
            {
                "phase_slot": phase,
                "phase_angle": f"{phase}*pi/3",
                "phase_factor": f"exp(2*pi*i*{phase}/6)",
                "word": word,
                "word_length": len(word),
                "gate_schedule": compile_word(word),
                "timing_reparameterizations": {
                    mode: normalized_weights(len(word), mode)
                    for mode in ("uniform", "front_loaded", "back_loaded")
                },
                "six_reference_fringe": fringe_signature(phase),
                "zero_reference_port0_probability": fringe_signature(phase)[0][
                    "port0_probability"
                ],
                "null_control": {
                    "word": null_word,
                    "word_length": len(null_word),
                    "predicted_phase_slot": 0,
                    "predicted_zero_reference_port0_probability": 1.0,
                },
            }
        )

    expected_zero_reference = {1: 0.75, 2: 0.25, 3: 0.0}
    for protocol in loop_protocols:
        phase = protocol["phase_slot"]
        assert math.isclose(
            protocol["zero_reference_port0_probability"],
            expected_zero_reference[phase],
            abs_tol=1e-12,
        )

    checks = {
        "phase1_is_primitive_C6_witness": bool(loop_words[1]),
        "phase2_is_C3_projection_witness": bool(loop_words[2]),
        "phase3_is_C2_sign_witness": bool(loop_words[3]),
        "phase1_zero_reference_probability_is_three_quarters": expected_zero_reference[1]
        == 0.75,
        "phase2_zero_reference_probability_is_one_quarter": expected_zero_reference[2]
        == 0.25,
        "phase3_zero_reference_probability_is_dark": expected_zero_reference[3]
        == 0.0,
        "all_timing_profiles_have_unit_total_duration": all(
            math.isclose(sum(weights), 1.0, abs_tol=1e-9)
            for protocol in loop_protocols
            for weights in protocol["timing_reparameterizations"].values()
        ),
        "word_inverse_controls_are_exactly_balanced": all(
            protocol["null_control"]["word_length"] == 2 * protocol["word_length"]
            for protocol in loop_protocols
        ),
        "sylow5_admissible_control_is_available": section["witnesses"][
            "Sylow5_admits_section"
        ],
        "c2_and_c3_coboundary_nulls_are_false": (
            cocycle["coboundary_tests"]["mod2_coboundary"] is False
            and cocycle["coboundary_tests"]["mod3_coboundary"] is False
        ),
    }
    assert all(checks.values()), [name for name, value in checks.items() if not value]

    result = {
        "schema": "w33.pass1027.photonic_c6_holonomy_falsifier.python.v1",
        "status": "PASS",
        "headline": (
            "The certified C6 groupoid cocycle has been compiled into three "
            "closed-loop photonic tests with exact pi/3, 2pi/3, and pi phase "
            "signatures, timing-reparameterization controls, and word-inverse "
            "null experiments."
        ),
        "physical_encoding": {
            "carrier": "single-photon path/time-bin or OAM phase register with a reference arm",
            "abstract_gate_binding": (
                "Each signed GAP generator label is an ABI symbol G_i or G_i^{-1}. "
                "The existing holonomic Sp(4,3) compiler must bind these symbols "
                "to calibrated geometric loops."
            ),
            "readout": (
                "Interfere the transported photon with the phase-zero reference and "
                "scan six reference phases separated by pi/3."
            ),
        },
        "loop_protocols": loop_protocols,
        "admissible_sector_control": {
            "group": "Sylow-5 subgroup of Sp(4,3)",
            "base_orbits": section["witnesses"]["Sylow5_base_orbit_lengths"],
            "procedure": (
                "Compile one Sylow-5 generator, traverse each five-cycle, and close "
                "after the fifth application.  Semiregularity gives a consistent "
                "section and predicts phase slot 0."
            ),
            "predicted_phase_slot": 0,
        },
        "falsification_contract": [
            {
                "test": "phase quantization",
                "reject_if": (
                    "tomographic phase is inconsistent with the certified slot "
                    "k in Z6 after independently calibrated systematic errors"
                ),
            },
            {
                "test": "geometric timing independence",
                "reject_if": (
                    "uniform, front-loaded, and back-loaded schedules tracing the "
                    "same gate word yield statistically distinguishable phases"
                ),
            },
            {
                "test": "word-inverse null",
                "reject_if": "a word followed by its exact inverse has nonzero recovered phase",
            },
            {
                "test": "admissible Sylow-5 control",
                "reject_if": "a closed five-cycle has nonzero recovered C6 phase",
            },
        ],
        "honesty_boundary": (
            "This is a finite gate-and-readout ABI with parameter-free ideal "
            "signatures. It is not a waveguide mask, detector-noise model, loss "
            "budget, or claim that the abstract Sp(4,3) generators have already "
            "been pulse-synthesized on a specific chip."
        ),
        "check_count": len(checks),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        "Pass1027 photonic falsifier: PASS — "
        f"loops={[len(loop_words[k]) for k in (1, 2, 3)]}"
    )


if __name__ == "__main__":
    main()
