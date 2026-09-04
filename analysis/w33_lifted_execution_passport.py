#!/usr/bin/env python3
"""Execution-passport v4 control-lift extension for the W33 runtime.

Version 3 of the passport already commits the guest image, immutable carrier,
logical dimension, Merkle memory/capability roots, component link, distinct
Clifford/projective namespaces, magic budget, reversible history, authority
epoch/revocation, concurrency schedule, cancellation and GC reachability.

The current VM frontier exposes one remaining identity gap: a projective PSp
operation does not determine which Sp lift {g,-g} is intended, and an Sp lift
still does not determine a calibrated optical Clifford realization.  This file
adds those distinctions without mutating the established v3 object.

The v4 envelope commits:
  * the exact v3 passport digest,
  * deployment mode: one immutable 216 guest OR the 1296 fibre hypervisor,
  * projective-control target digest,
  * explicit Sp central-lift bit,
  * optional Clifford phase-frame digest,
  * optional measured-calibration digest,
  * optional non-Clifford resource digest,
  * a requested execution stage.

Admission is monotone/fail-closed:
  PROJECTIVE_SCHEDULE requires only the projective target;
  SYMPLECTIC_EXECUTE additionally requires the central-lift bit;
  CALIBRATED_OPTICAL additionally requires phase-frame + calibration evidence;
  NONCLIFFORD additionally requires an explicit non-Clifford resource.

The 1296 machine is deliberately a hypervisor deployment mode, not a third
Carrier value.  A hypervisor envelope therefore binds the two child guest
profile/passport identities separately and forbids carrier conversion.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
from typing import Any


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def is_digest(value: str | None) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


class ExecutionStage(str, Enum):
    PROJECTIVE_SCHEDULE = "projective-schedule"
    SYMPLECTIC_EXECUTE = "symplectic-execute"
    CALIBRATED_OPTICAL = "calibrated-optical"
    NONCLIFFORD = "nonclifford"


class DeploymentRole(str, Enum):
    GUEST_CIRCUIT_ST81 = "w33.circuit216.steinberg81"
    GUEST_PAIR_ST64 = "w33.paired-hemisystem216.steinberg64"
    FIBRE1296_HYPERVISOR = "w33.fibre1296.steinberg81+64"


@dataclass(frozen=True)
class HypervisorBinding:
    """Identity of the two immutable guest children hosted by the fibre product."""
    circuit_guest_digest: str
    pair_guest_digest: str
    base_states: int = 36
    fibre_degree: int = 6
    hypervisor_states: int = 1296
    carrier_conversion: str = "FORBIDDEN"


@dataclass(frozen=True)
class LiftedExecutionPassport:
    schema: str
    base_passport_id: str
    deployment_role: str
    projective_target_digest: str
    requested_stage: str
    sp_central_lift_bit: int | None = None
    clifford_phase_frame_digest: str | None = None
    calibration_digest: str | None = None
    nonclifford_resource_digest: str | None = None
    hypervisor: HypervisorBinding | None = None

    def body(self) -> dict[str, Any]:
        row = asdict(self)
        return row

    @property
    def passport_id(self) -> str:
        return digest(self.body())


def validate(passport: LiftedExecutionPassport) -> dict[str, Any]:
    try:
        stage = ExecutionStage(passport.requested_stage)
        role = DeploymentRole(passport.deployment_role)
    except ValueError:
        return {"ok": False, "checks": {"known_stage_and_role": False}}

    checks: dict[str, bool] = {
        "schema_v4": passport.schema == "w33.execution-passport.v4",
        "base_passport_committed": is_digest(passport.base_passport_id),
        "projective_target_committed": is_digest(passport.projective_target_digest),
        "known_stage_and_role": True,
        "central_bit_well_typed": passport.sp_central_lift_bit in (None, 0, 1),
    }

    if stage in {
        ExecutionStage.SYMPLECTIC_EXECUTE,
        ExecutionStage.CALIBRATED_OPTICAL,
        ExecutionStage.NONCLIFFORD,
    }:
        checks["sp_lift_explicit"] = passport.sp_central_lift_bit in (0, 1)

    if stage in {ExecutionStage.CALIBRATED_OPTICAL, ExecutionStage.NONCLIFFORD}:
        checks["clifford_phase_frame_committed"] = is_digest(passport.clifford_phase_frame_digest)
        checks["measured_calibration_committed"] = is_digest(passport.calibration_digest)

    if stage is ExecutionStage.NONCLIFFORD:
        checks["nonclifford_resource_committed"] = is_digest(passport.nonclifford_resource_digest)

    if role is DeploymentRole.FIBRE1296_HYPERVISOR:
        h = passport.hypervisor
        checks.update({
            "hypervisor_binding_present": h is not None,
            "hypervisor_children_committed": bool(
                h and is_digest(h.circuit_guest_digest) and is_digest(h.pair_guest_digest)
            ),
            "hypervisor_children_distinct": bool(
                h and h.circuit_guest_digest != h.pair_guest_digest
            ),
            "hypervisor_geometry_exact": bool(
                h
                and h.base_states == 36
                and h.fibre_degree == 6
                and h.hypervisor_states == 1296
            ),
            "carrier_conversion_forbidden": bool(h and h.carrier_conversion == "FORBIDDEN"),
        })
    else:
        checks["guest_has_no_hypervisor_binding"] = passport.hypervisor is None

    return {"ok": all(checks.values()), "checks": checks}


def demo(stage: ExecutionStage, role: DeploymentRole) -> LiftedExecutionPassport:
    common = dict(
        schema="w33.execution-passport.v4",
        base_passport_id=digest({"v3": "demo-passport"}),
        deployment_role=role.value,
        projective_target_digest=digest({"PSp": "demo-target"}),
        requested_stage=stage.value,
    )
    if stage is not ExecutionStage.PROJECTIVE_SCHEDULE:
        common["sp_central_lift_bit"] = 1
    if stage in {ExecutionStage.CALIBRATED_OPTICAL, ExecutionStage.NONCLIFFORD}:
        common["clifford_phase_frame_digest"] = digest({"phase": "demo"})
        common["calibration_digest"] = digest({"calibration": "measured-demo"})
    if stage is ExecutionStage.NONCLIFFORD:
        common["nonclifford_resource_digest"] = digest({"resource": "validated-demo"})
    if role is DeploymentRole.FIBRE1296_HYPERVISOR:
        common["hypervisor"] = HypervisorBinding(
            circuit_guest_digest=digest({"guest": "ST81"}),
            pair_guest_digest=digest({"guest": "ST64"}),
        )
    return LiftedExecutionPassport(**common)


def verify() -> dict[str, Any]:
    stage_ok = {
        stage.value: validate(demo(stage, DeploymentRole.GUEST_CIRCUIT_ST81))["ok"]
        for stage in ExecutionStage
    }
    hypervisor = demo(ExecutionStage.SYMPLECTIC_EXECUTE, DeploymentRole.FIBRE1296_HYPERVISOR)
    hv = validate(hypervisor)

    projective = demo(ExecutionStage.PROJECTIVE_SCHEDULE, DeploymentRole.GUEST_CIRCUIT_ST81)
    missing_lift = LiftedExecutionPassport(
        schema=projective.schema,
        base_passport_id=projective.base_passport_id,
        deployment_role=projective.deployment_role,
        projective_target_digest=projective.projective_target_digest,
        requested_stage=ExecutionStage.SYMPLECTIC_EXECUTE.value,
    )
    missing_phase = demo(ExecutionStage.SYMPLECTIC_EXECUTE, DeploymentRole.GUEST_CIRCUIT_ST81)
    missing_phase = LiftedExecutionPassport(
        **{**missing_phase.body(), "requested_stage": ExecutionStage.CALIBRATED_OPTICAL.value}
    )
    optical = demo(ExecutionStage.CALIBRATED_OPTICAL, DeploymentRole.GUEST_CIRCUIT_ST81)
    missing_magic = LiftedExecutionPassport(
        **{**optical.body(), "requested_stage": ExecutionStage.NONCLIFFORD.value}
    )
    bad_hyper = LiftedExecutionPassport(
        **{
            **hypervisor.body(),
            "hypervisor": HypervisorBinding(
                circuit_guest_digest=digest({"guest": "same"}),
                pair_guest_digest=digest({"guest": "same"}),
            ),
        }
    )

    checks = {
        "all_complete_stage_examples_admit": all(stage_ok.values()),
        "hypervisor_admits_with_two_children": hv["ok"],
        "symplectic_refuses_missing_central_lift": not validate(missing_lift)["ok"],
        "optical_refuses_missing_phase_calibration": not validate(missing_phase)["ok"],
        "nonclifford_refuses_missing_resource": not validate(missing_magic)["ok"],
        "hypervisor_refuses_aliased_children": not validate(bad_hyper)["ok"],
        "passport_identity_changes_with_stage": len({
            demo(stage, DeploymentRole.GUEST_CIRCUIT_ST81).passport_id
            for stage in ExecutionStage
        }) == 4,
    }
    return {
        "schema": "w33.execution-passport-v4-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "stage_examples": stage_ok,
        "hypervisor_checks": hv["checks"],
        "interpretation": (
            "Execution identity now separates projective scheduling, Sp matrix lift, "
            "calibrated Clifford realization and non-Clifford resource admission while "
            "keeping the 1296 fibre product above, rather than inside, the immutable guest carrier type."
        ),
        "boundary": (
            "The central lift bit is only the twofold PSp-to-Sp choice. A full qutrit Clifford "
            "phase frame, measured optical calibration and non-Clifford resource remain separate evidence."
        ),
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
