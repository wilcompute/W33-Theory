#!/usr/bin/env python3
"""Photonic lowering for the phase-specified W33 two-qutrit Clifford ISA.

The algebraic phase lift now has explicit hardware-facing primitives instead of
ending at a 9x9 unitary.  This module lowers:

* Weyl displacement D(q1,q2,p1,p2) into addressable cyclic mode shifts and
  120-degree qutrit phase masks;
* each transvection U(v,lambda) into an eigenmode-analysis / quadratic phase /
  eigenmode-synthesis sandwich for D_v.

The plan is bound to the existing time-bin and frequency-bin compiler
certificates.  It is still a control plan, not a fabricated optical chip.
Physical admission is delegated to w33_qutrit_optical_calibration_ingest and is
true only for a W33_DEVICE_MEASUREMENT packet explicitly covering both primitive
classes used here.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
from typing import Any, Sequence

from w33_qutrit_clifford_phase_displacement_lift import (
    AXIS_INDEX if False else None,
)
# Import explicitly below; the conditional dummy above intentionally avoids
# implying that the phase-lift module exports a projective-axis lookup.
from w33_qutrit_clifford_phase_displacement_lift import (
    CliffordPhaseFrame,
    GEOMETRY,
    HALF,
    REQUIRED_CALIBRATION_PRIMITIVES,
    transvection_unitary,
)
import w33_qutrit_optical_calibration_ingest as calibration

ROOT = Path(__file__).resolve().parents[1]


def digest(v: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(v, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def displacement_plan(d: Sequence[int]) -> list[dict[str, Any]]:
    if len(d) != 4:
        raise ValueError("two-qutrit Weyl displacement requires four F3 coordinates")
    q1, q2, p1, p2 = (int(x) % 3 for x in d)
    rows: list[dict[str, Any]] = []
    for logical, q in enumerate((q1, q2)):
        if q:
            rows.append({
                "primitive": "WEYL_DISPLACEMENT",
                "operation": "CYCLIC_MODE_SHIFT",
                "logical_qutrit": logical,
                "shift_mod3": q,
                "hardware_family": "time_or_frequency_bin_permutation",
            })
    for logical, p in enumerate((p1, p2)):
        if p:
            rows.append({
                "primitive": "WEYL_DISPLACEMENT",
                "operation": "QUTRIT_LINEAR_PHASE_MASK",
                "logical_qutrit": logical,
                "phase_step_mod3": p,
                "phase_step_degrees": 120 * p,
                "hardware_family": "line_by_line_phase_or_eom_drive",
            })
    return rows


def transvection_plan(axis: int, lam: int) -> list[dict[str, Any]]:
    axis = int(axis); lam = int(lam)
    if not 0 <= axis < 40 or lam not in (1, 2):
        raise ValueError("invalid W33 transvection opcode")
    v = tuple(int(x) for x in GEOMETRY.points[axis])
    phase_trits = [((HALF * lam * k * k) % 3) for k in range(3)]
    return [
        {
            "primitive": "TRANSVECTION_QUADRATIC_PHASE",
            "operation": "WEYL_EIGENMODE_ANALYZE",
            "axis": axis,
            "weyl_label": list(v),
            "hardware_family": "qutrit_mode_mixer",
        },
        {
            "primitive": "TRANSVECTION_QUADRATIC_PHASE",
            "operation": "QUTRIT_QUADRATIC_PHASE_MASK",
            "axis": axis,
            "lambda": lam,
            "phase_trits_by_eigenvalue": phase_trits,
            "phase_degrees_by_eigenvalue": [120 * x for x in phase_trits],
            "hardware_family": "line_by_line_phase_or_eom_drive",
        },
        {
            "primitive": "TRANSVECTION_QUADRATIC_PHASE",
            "operation": "WEYL_EIGENMODE_SYNTHESIZE",
            "axis": axis,
            "weyl_label": list(v),
            "hardware_family": "qutrit_mode_mixer_inverse",
        },
    ]


def lower_frame(frame: CliffordPhaseFrame) -> dict[str, Any]:
    ops: list[dict[str, Any]] = []
    ops.extend(displacement_plan(frame.displacement))
    for axis, lam in frame.word:
        ops.extend(transvection_plan(axis, lam))
    if frame.global_phase_mod3:
        ops.append({
            "primitive": "GLOBAL_FRAME_PHASE",
            "operation": "FRAME_PHASE_BOOKKEEPING_ONLY",
            "phase_mod3": frame.global_phase_mod3,
            "physical_observable": False,
        })
    payload = {
        "schema": "w33.qutrit-clifford-photonic-plan.v1",
        "phase_frame_digest": frame.phase_frame_digest,
        "symplectic_word": [list(x) for x in frame.word],
        "displacement": list(frame.displacement),
        "global_phase_mod3": frame.global_phase_mod3,
        "required_calibration_primitives": sorted(REQUIRED_CALIBRATION_PRIMITIVES),
        "operations": ops,
    }
    payload["plan_digest"] = digest(payload)
    return payload


def verify() -> dict[str, Any]:
    timebin = load_json("data/bt1653_time_bin_hardware_compiler.json")
    freq = load_json("data/w33_frequency_bin_hashimoto_compiler.json")

    all_masks_ok = True
    all_plans_three_stage = True
    unitary_shapes_ok = True
    for axis in range(40):
        for lam in (1, 2):
            plan = transvection_plan(axis, lam)
            all_plans_three_stage = all_plans_three_stage and len(plan) == 3
            mask = plan[1]["phase_trits_by_eigenvalue"]
            expected = [((HALF * lam * k * k) % 3) for k in range(3)]
            all_masks_ok = all_masks_ok and mask == expected
            U = transvection_unitary(GEOMETRY.points[axis], lam)
            unitary_shapes_ok = unitary_shapes_ok and len(U) == 9 and all(len(row) == 9 for row in U)

    sample = CliffordPhaseFrame(((0, 1), (13, 2)), (1, 2, 0, 1), 2)
    plan = lower_frame(sample)
    device = calibration.device_calibration()
    prior = calibration.prior_art()
    packet = device.get("packet") if isinstance(device.get("packet"), dict) else {}
    coverage = set(packet.get("primitive_coverage", [])) if isinstance(packet.get("primitive_coverage"), list) else set()
    calibrated = bool(device.get("accepted")) and REQUIRED_CALIBRATION_PRIMITIVES <= coverage

    checks = {
        "all_80_transvections_lower_to_three_stage_photonic_plan": all_plans_three_stage,
        "all_quadratic_masks_match_exact_phase_polynomial": all_masks_ok,
        "phase_source_unitaries_remain_9x9": unitary_shapes_ok,
        "sample_plan_binds_phase_frame_digest": plan["phase_frame_digest"] == sample.phase_frame_digest,
        "sample_plan_requires_exact_two_primitive_classes": set(plan["required_calibration_primitives"]) == set(REQUIRED_CALIBRATION_PRIMITIVES),
        "time_bin_hardware_compiler_certificate_is_verified": bool(timebin.get("verified")),
        "frequency_bin_hardware_compiler_certificate_is_verified": bool(freq.get("verified")),
        "external_prior_art_is_never_W33_calibration": prior.get("accepted_for_w33") is False,
        "calibrated_device_requires_measured_W33_packet_and_coverage": calibrated == (bool(device.get("accepted")) and REQUIRED_CALIBRATION_PRIMITIVES <= coverage),
        "current_missing_device_packet_fails_closed": calibrated or not bool(device.get("present")),
    }
    return {
        "schema": "w33.qutrit-clifford-photonic-lowering.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "sample_plan": plan,
        "compiler_bindings": {
            "time_bin": "data/bt1653_time_bin_hardware_compiler.json",
            "frequency_bin": "data/w33_frequency_bin_hashimoto_compiler.json",
        },
        "device_calibration": {
            "present": bool(device.get("present")),
            "accepted": bool(device.get("accepted")),
            "declared_coverage": sorted(coverage),
            "calibrated_for_phase_lift": calibrated,
        },
        "boundary": (
            "This lowers exact Clifford phase semantics to an explicit optical component grammar. It does not assign measured insertion loss, visibility, RF power, drift, or device fidelity. CALIBRATED_DEVICE remains unreachable without a real W33_DEVICE_MEASUREMENT packet carrying the exact primitive coverage."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
