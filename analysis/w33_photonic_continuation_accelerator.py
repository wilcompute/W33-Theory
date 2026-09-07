#!/usr/bin/env python3
"""Finite photonic control-plane adapter for one HoloVM continuation step.

The durable VM remains the immutable software continuation graph.  This module
asks a narrower hardware question: what is the smallest *current lowering
primitive grammar* needed to accelerate one already-defined guest transition?

For one authenticated guest step we:
  1. independently execute/verify the process-kernel transition;
  2. bind its exact receipt and parent continuation to one valid W33 control
     packet containing a single qutrit transvection;
  3. lower that transvection to the existing three-stage photonic grammar
     (eigenmode analyse -> quadratic phase -> eigenmode synthesize);
  4. commit the predicted child continuation root; and
  5. expose a measurement-receipt port that remains fail-closed until the
     repository has accepted W33 device calibration covering the required
     primitive classes.

Thus a continuation root is classical authenticated state; it is never encoded
as an optical amplitude.  The optical device is a finite control accelerator,
not the unbounded guest memory.

"Smallest" below means smallest within the repository's present transvection
lowering grammar: one transvection is exactly three optical operations.  It is
not a proof of global physical circuit minimality.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Any

from w33_authenticated_counter_machine import BitStore, Receipt, genesis
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_holovm_process_kernel import (
    ProcessContinuation,
    advance,
    prepare_process,
    spawn,
)
from w33_merkle_capability_memory import digest
from w33_projective_symplectic_lift_control_abi import central_lift_bit
from w33_qutrit_clifford_phase_displacement_lift import (
    CliffordPhaseFrame,
    REQUIRED_CALIBRATION_PRIMITIVES,
)
from w33_qutrit_clifford_photonic_lowering import lower_frame
import w33_qutrit_optical_calibration_ingest as calibration
from w33_typed_universal_microvm import Carrier, Program, add_r1_into_r0_program
from w33_universal_control_packet import (
    ControlPacket,
    MicroOp,
    Stage,
    target_digest,
    validate_packet,
    word_matrix,
)

PLAN_SCHEMA = "w33.photonic-continuation-accelerator-plan.v1"
RECEIPT_SCHEMA = "w33.photonic-continuation-accelerator-receipt.v1"
MEASUREMENT_SCHEMA = "w33.photonic-continuation-measurement.v1"


@dataclass(frozen=True)
class AcceleratorPlan:
    parent_continuation: str
    predicted_child_continuation: str
    process_id: str
    generation_before: int
    generation_after: int
    guest_receipt_id: str
    control_packet_id: str
    phase_frame_digest: str
    photonic_plan_digest: str
    axis: int
    lam: int
    route: tuple[int, ...]
    optical_operations: int
    required_calibration_primitives: tuple[str, ...]
    calibrated_device: bool

    @property
    def plan_id(self) -> str:
        return digest({"schema": PLAN_SCHEMA, **asdict(self)})


@dataclass(frozen=True)
class AcceleratorReceipt:
    plan_id: str
    parent_continuation: str
    child_continuation: str
    process_id: str
    guest_receipt_id: str
    control_packet_id: str
    photonic_plan_digest: str
    execution_mode: str
    measurement_digest: str | None

    @property
    def receipt_id(self) -> str:
        return digest({"schema": RECEIPT_SCHEMA, **asdict(self)})


def _device_status() -> tuple[bool, tuple[str, ...], dict[str, Any]]:
    device = calibration.device_calibration()
    packet = device.get("packet") if isinstance(device.get("packet"), dict) else {}
    coverage = tuple(sorted(packet.get("primitive_coverage", []))) if isinstance(packet.get("primitive_coverage"), list) else ()
    calibrated = bool(device.get("accepted")) and REQUIRED_CALIBRATION_PRIMITIVES <= set(coverage)
    return calibrated, coverage, device


def compile_one_step(
    program: Program,
    process: ProcessContinuation,
    memory: BitStore,
    *,
    lam: int = 1,
) -> tuple[AcceleratorPlan, ProcessContinuation, Receipt, ControlPacket, dict[str, Any]]:
    """Compile one verified software transition into one optical control plan."""
    if lam not in (1, 2):
        raise ValueError("transvection lambda must be 1 or 2")
    child, guest_receipt = advance(program, process, memory)
    axis = int(guest_receipt.route[-1])
    word = (MicroOp(axis, lam),)
    matrix = word_matrix(word)
    frame = CliffordPhaseFrame(((axis, lam),))
    packet = ControlPacket(
        schema="w33.universal-control-packet.v1",
        semantic_transition_digest=guest_receipt.receipt_id,
        source_portal=int(guest_receipt.route[0]),
        target_portal=axis,
        route=guest_receipt.route,
        microcode=word,
        projective_target_digest=target_digest(matrix),
        sp_central_lift_bit=central_lift_bit(matrix),
        requested_stage=Stage.SYMPLECTIC_EXECUTE.value,
        execution_passport_id=process.passport_id,
        clifford_phase_frame_digest=frame.phase_frame_digest,
    )
    verdict = validate_packet(packet)
    if not verdict["ok"]:
        raise ValueError(f"generated continuation control packet failed verification: {verdict['checks']}")
    optical = lower_frame(frame)
    operations = optical["operations"]
    # No displacement is present in this one-transvection frame, so the current
    # lowering grammar must be exactly analyse/phase/synthesize.
    if len(operations) != 3:
        raise AssertionError("one transvection no longer lowers to exactly three optical operations")
    prepared_child = prepare_process(child, memory)
    calibrated, _, _ = _device_status()
    plan = AcceleratorPlan(
        parent_continuation=process.continuation_id,
        predicted_child_continuation=prepared_child.root,
        process_id=process.process_id,
        generation_before=process.generation,
        generation_after=child.generation,
        guest_receipt_id=guest_receipt.receipt_id,
        control_packet_id=packet.packet_id,
        phase_frame_digest=frame.phase_frame_digest,
        photonic_plan_digest=optical["plan_digest"],
        axis=axis,
        lam=lam,
        route=guest_receipt.route,
        optical_operations=len(operations),
        required_calibration_primitives=tuple(sorted(REQUIRED_CALIBRATION_PRIMITIVES)),
        calibrated_device=calibrated,
    )
    return plan, child, guest_receipt, packet, optical


def software_receipt(plan: AcceleratorPlan) -> AcceleratorReceipt:
    """Commit the exact software prediction without claiming physical execution."""
    return AcceleratorReceipt(
        plan_id=plan.plan_id,
        parent_continuation=plan.parent_continuation,
        child_continuation=plan.predicted_child_continuation,
        process_id=plan.process_id,
        guest_receipt_id=plan.guest_receipt_id,
        control_packet_id=plan.control_packet_id,
        photonic_plan_digest=plan.photonic_plan_digest,
        execution_mode="VERIFIED_SOFTWARE_PLAN",
        measurement_digest=None,
    )


def bind_physical_measurement(
    plan: AcceleratorPlan,
    *,
    measurement_digest: str,
    observed_child_continuation: str,
) -> AcceleratorReceipt:
    """Bind a real measurement only after accepted device calibration.

    A caller cannot turn a software plan into "hardware evidence" by supplying a
    hash.  The repository's calibration ingest must already accept the exact
    primitive coverage, and the measured child must match the predicted root.
    """
    calibrated, coverage, _ = _device_status()
    if not calibrated or not plan.calibrated_device:
        raise PermissionError("physical continuation acceleration requires accepted W33 device calibration")
    if not isinstance(measurement_digest, str) or not measurement_digest.startswith("sha256:"):
        raise ValueError("measurement must be content addressed")
    if observed_child_continuation != plan.predicted_child_continuation:
        raise ValueError("measured child continuation disagrees with verified software prediction")
    if not REQUIRED_CALIBRATION_PRIMITIVES <= set(coverage):
        raise PermissionError("device calibration does not cover accelerator primitive set")
    return AcceleratorReceipt(
        plan_id=plan.plan_id,
        parent_continuation=plan.parent_continuation,
        child_continuation=observed_child_continuation,
        process_id=plan.process_id,
        guest_receipt_id=plan.guest_receipt_id,
        control_packet_id=plan.control_packet_id,
        photonic_plan_digest=plan.photonic_plan_digest,
        execution_mode="CALIBRATED_PHYSICAL_MEASUREMENT",
        measurement_digest=measurement_digest,
    )


def verify() -> dict[str, Any]:
    program = add_r1_into_r0_program()
    memory = BitStore()
    state = genesis(program, memory, (7, 1), session="photonic-continuation")
    passport = digest({
        "schema": "w33.photonic-continuation-demo-passport.v1",
        "image": program.image_id,
        "carrier": Carrier.CIRCUIT_ST81.value,
    })
    process = spawn(state, FibreProductAddress(5, 2, 4), passport)
    plan, child, guest_receipt, packet, optical = compile_one_step(program, process, memory)
    soft = software_receipt(plan)
    calibrated, coverage, device = _device_status()

    blocked_without_calibration = False
    if not calibrated:
        try:
            bind_physical_measurement(
                plan,
                measurement_digest=digest({"synthetic": "not-a-device-measurement"}),
                observed_child_continuation=plan.predicted_child_continuation,
            )
        except PermissionError:
            blocked_without_calibration = True

    operations = optical["operations"]
    checks = {
        "authenticated_guest_step_advances_generation": child.generation == process.generation + 1,
        "process_identity_is_stable_across_accelerated_step": child.process_id == process.process_id,
        "control_packet_binds_exact_guest_receipt": packet.semantic_transition_digest == guest_receipt.receipt_id,
        "control_packet_revalidates": validate_packet(packet)["ok"],
        "one_transvection_uses_exact_three_stage_current_optical_grammar": (
            len(operations) == 3
            and [row["operation"] for row in operations] == [
                "WEYL_EIGENMODE_ANALYZE",
                "QUTRIT_QUADRATIC_PHASE_MASK",
                "WEYL_EIGENMODE_SYNTHESIZE",
            ]
        ),
        "route_stays_inside_W33_diameter_two": len(plan.route) - 1 <= 2,
        "predicted_child_is_content_addressed_process_snapshot": plan.predicted_child_continuation.startswith("sha256:"),
        "software_receipt_never_claims_measurement": soft.execution_mode == "VERIFIED_SOFTWARE_PLAN" and soft.measurement_digest is None,
        "physical_path_is_fail_closed_when_device_packet_missing": calibrated or blocked_without_calibration,
        "calibration_coverage_rule_is_exact": calibrated == (bool(device.get("accepted")) and REQUIRED_CALIBRATION_PRIMITIVES <= set(coverage)),
    }
    return {
        "schema": "w33.photonic-continuation-accelerator-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "plan": {
            **asdict(plan),
            "plan_id": plan.plan_id,
            "software_receipt_id": soft.receipt_id,
        },
        "finite_control_plane": {
            "classical_input": ["parent_continuation_root", "process_id", "guest_receipt_id", "passport_id"],
            "finite_W33_control": {"axis": plan.axis, "lambda": plan.lam, "route_hops": len(plan.route) - 1},
            "optical_operations_in_current_grammar": plan.optical_operations,
            "optical_sequence": [row["operation"] for row in operations],
            "classical_output": ["predicted_child_continuation_root", "control_packet_id", "photonic_plan_digest", "optional_measurement_digest"],
        },
        "device_calibration": {
            "present": bool(device.get("present")),
            "accepted": bool(device.get("accepted")),
            "coverage": list(coverage),
            "physical_acceleration_admitted": calibrated,
        },
        "boundary": (
            "The exact three-operation count is minimal only inside the repository's current one-transvection lowering grammar. "
            "No optical hardware execution or measurement is claimed unless the external W33 device calibration ingest accepts the required primitive coverage."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(out["status"] != "PASS")
