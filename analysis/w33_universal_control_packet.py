#!/usr/bin/env python3
"""Proof-carrying finite control packet for the W33 universal VM.

This is the concrete transaction that joins the current architecture pieces.
A guest semantic transition is compiled into a packet containing:

  * a semantic transition digest (what computation means),
  * source/target W33 portals and the deterministic diameter-two route,
  * an Sp(4,3) qutrit-transvection micro-word of length <= 5,
  * the induced projective PSp target digest,
  * the central-lift bit selecting which {g,-g} matrix is intended,
  * an optional 1296-state fibre-hypervisor address,
  * physical phase/calibration/non-Clifford evidence when the requested stage
    crosses those boundaries.

The packet verifier recomputes the route and multiplies the transvection word; it
does not trust either target field supplied by the compiler.  Thus the guest
semantic identity remains independent of placement, while the finite-control
proof binds exactly how the requested operation is to be transported/executed.

Important scope: the <=5 word bound is an imported exhaustive theorem for the
Holotrade Sp(4,3) compiler.  This packet verifier only checks that a supplied
word is valid and within that certified envelope; it is not itself the compiler
or a proof that the supplied word is minimal.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
import json
import os
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from w33_typed_universal_microvm import GEOMETRY  # noqa: E402
from w33_projective_symplectic_lift_control_abi import (  # noqa: E402
    IDENTITY,
    Matrix,
    central_lift_bit,
    matmul,
    projective_action,
    transvection,
)

MAX_TRANSVECTION_WORD = 5
HYPERVISOR_STATES = 1296
BASE_STATES = 36
FIBRE = 6


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def is_digest(value: str | None) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


class Stage(str, Enum):
    PROJECTIVE_SCHEDULE = "projective-schedule"
    SYMPLECTIC_EXECUTE = "symplectic-execute"
    CALIBRATED_OPTICAL = "calibrated-optical"
    NONCLIFFORD = "nonclifford"


@dataclass(frozen=True)
class MicroOp:
    axis: int
    lam: int

    def validate(self) -> None:
        if not 0 <= self.axis < 40:
            raise ValueError("transvection axis must be a W33 projective point 0..39")
        if self.lam not in (1, 2):
            raise ValueError("qutrit transvection lambda must be 1 or 2")


@dataclass(frozen=True)
class HypervisorAddress:
    base: int
    circuit_tag: int
    pair_tag: int

    def validate(self) -> None:
        if not 0 <= self.base < BASE_STATES:
            raise ValueError("base outside 36-state quotient")
        if not 0 <= self.circuit_tag < FIBRE or not 0 <= self.pair_tag < FIBRE:
            raise ValueError("fibre tag outside 0..5")

    @property
    def packed(self) -> int:
        self.validate()
        return self.base + BASE_STATES * (self.circuit_tag + FIBRE * self.pair_tag)

    @property
    def circuit216(self) -> int:
        self.validate()
        return FIBRE * self.base + self.circuit_tag

    @property
    def pair216(self) -> int:
        self.validate()
        return FIBRE * self.base + self.pair_tag


@dataclass(frozen=True)
class ControlPacket:
    schema: str
    semantic_transition_digest: str
    source_portal: int
    target_portal: int
    route: tuple[int, ...]
    microcode: tuple[MicroOp, ...]
    projective_target_digest: str
    sp_central_lift_bit: int
    requested_stage: str
    execution_passport_id: str
    hypervisor: HypervisorAddress | None = None
    clifford_phase_frame_digest: str | None = None
    calibration_digest: str | None = None
    nonclifford_resource_digest: str | None = None

    def body(self) -> dict[str, Any]:
        row = asdict(self)
        return row

    @property
    def packet_id(self) -> str:
        return digest(self.body())


def word_matrix(word: tuple[MicroOp, ...]) -> Matrix:
    cur = IDENTITY
    for op in word:
        op.validate()
        # Program order: apply each next transvection on the right, matching the
        # current Holotrade compiler's g.T(...) peeling convention.
        cur = matmul(cur, transvection(GEOMETRY.points[op.axis], op.lam))
    return cur


def target_digest(matrix: Matrix) -> str:
    return digest({"projective_action": projective_action(matrix)})


def validate_packet(packet: ControlPacket) -> dict[str, Any]:
    try:
        stage = Stage(packet.requested_stage)
    except ValueError:
        return {"ok": False, "checks": {"known_stage": False}}

    checks: dict[str, bool] = {
        "schema": packet.schema == "w33.universal-control-packet.v1",
        "semantic_transition_committed": is_digest(packet.semantic_transition_digest),
        "passport_committed": is_digest(packet.execution_passport_id),
        "known_stage": True,
        "source_portal_valid": 0 <= packet.source_portal < 40,
        "target_portal_valid": 0 <= packet.target_portal < 40,
        "word_length_within_certified_envelope": len(packet.microcode) <= MAX_TRANSVECTION_WORD,
        "word_nonempty_for_execution": stage is Stage.PROJECTIVE_SCHEDULE or len(packet.microcode) > 0,
        "central_lift_bit_typed": packet.sp_central_lift_bit in (0, 1),
    }

    try:
        expected_route = GEOMETRY.route(packet.source_portal, packet.target_portal)
        checks["route_is_canonical"] = packet.route == expected_route
        checks["route_diameter_at_most_two"] = len(expected_route) - 1 <= 2
    except Exception:
        checks["route_is_canonical"] = False
        checks["route_diameter_at_most_two"] = False

    try:
        matrix = word_matrix(packet.microcode)
        checks["microcode_reconstructs_projective_target"] = target_digest(matrix) == packet.projective_target_digest
        checks["microcode_reconstructs_central_lift"] = central_lift_bit(matrix) == packet.sp_central_lift_bit
    except Exception:
        checks["microcode_reconstructs_projective_target"] = False
        checks["microcode_reconstructs_central_lift"] = False

    if packet.hypervisor is not None:
        try:
            packet.hypervisor.validate()
            checks["hypervisor_address_valid"] = 0 <= packet.hypervisor.packed < HYPERVISOR_STATES
            checks["hypervisor_projections_valid"] = (
                0 <= packet.hypervisor.circuit216 < 216
                and 0 <= packet.hypervisor.pair216 < 216
            )
        except Exception:
            checks["hypervisor_address_valid"] = False
            checks["hypervisor_projections_valid"] = False

    if stage in {Stage.CALIBRATED_OPTICAL, Stage.NONCLIFFORD}:
        checks["clifford_phase_frame_committed"] = is_digest(packet.clifford_phase_frame_digest)
        checks["measured_calibration_committed"] = is_digest(packet.calibration_digest)
    if stage is Stage.NONCLIFFORD:
        checks["nonclifford_resource_committed"] = is_digest(packet.nonclifford_resource_digest)

    return {"ok": all(checks.values()), "checks": checks}


def make_packet(
    semantic: object,
    source: int,
    target: int,
    word: tuple[MicroOp, ...],
    stage: Stage,
    hypervisor: HypervisorAddress | None = None,
    with_physical_evidence: bool = False,
    with_nonclifford: bool = False,
) -> ControlPacket:
    matrix = word_matrix(word)
    kwargs: dict[str, Any] = {}
    if with_physical_evidence:
        kwargs["clifford_phase_frame_digest"] = digest({"phase_frame": "demo"})
        kwargs["calibration_digest"] = digest({"measured_calibration": "demo"})
    if with_nonclifford:
        kwargs["nonclifford_resource_digest"] = digest({"nonclifford": "demo"})
    return ControlPacket(
        schema="w33.universal-control-packet.v1",
        semantic_transition_digest=digest(semantic),
        source_portal=source,
        target_portal=target,
        route=GEOMETRY.route(source, target),
        microcode=word,
        projective_target_digest=target_digest(matrix),
        sp_central_lift_bit=central_lift_bit(matrix),
        requested_stage=stage.value,
        execution_passport_id=digest({"passport": "demo-v4"}),
        hypervisor=hypervisor,
        **kwargs,
    )


def verify() -> dict[str, Any]:
    word = (MicroOp(0, 1), MicroOp(7, 2), MicroOp(13, 1))
    semantic = {"guest": "DECJZ", "pc": 11, "before": [5, 7], "after": [5, 6]}
    hyper = HypervisorAddress(11, 2, 5)
    packet = make_packet(semantic, 3, 37, word, Stage.SYMPLECTIC_EXECUTE, hyper)
    good = validate_packet(packet)

    tampered_route = ControlPacket(**{**packet.body(), "route": (3, 37)})
    tampered_target = ControlPacket(**{
        **packet.body(),
        "projective_target_digest": digest({"projective_action": "wrong"}),
    })
    tampered_lift = ControlPacket(**{
        **packet.body(),
        "sp_central_lift_bit": 1 - packet.sp_central_lift_bit,
    })
    optical_missing = ControlPacket(**{
        **packet.body(),
        "requested_stage": Stage.CALIBRATED_OPTICAL.value,
    })
    optical_good = make_packet(
        semantic, 3, 37, word, Stage.CALIBRATED_OPTICAL, hyper, with_physical_evidence=True
    )
    nonclifford_missing = ControlPacket(**{
        **optical_good.body(),
        "requested_stage": Stage.NONCLIFFORD.value,
    })
    nonclifford_good = make_packet(
        semantic,
        3,
        37,
        word,
        Stage.NONCLIFFORD,
        hyper,
        with_physical_evidence=True,
        with_nonclifford=True,
    )

    # The semantic transition digest intentionally does not depend on route or
    # microcode: multiple verified backends may realize the same guest step.
    same_semantics_other_route_target = make_packet(
        semantic, 9, 22, (MicroOp(4, 1),), Stage.SYMPLECTIC_EXECUTE, hyper
    )

    checks = {
        "valid_packet_admitted": good["ok"],
        "route_tamper_refused": not validate_packet(tampered_route)["ok"],
        "projective_target_tamper_refused": not validate_packet(tampered_target)["ok"],
        "central_lift_tamper_refused": not validate_packet(tampered_lift)["ok"],
        "optical_stage_refuses_missing_evidence": not validate_packet(optical_missing)["ok"],
        "optical_stage_accepts_evidence": validate_packet(optical_good)["ok"],
        "nonclifford_stage_refuses_missing_resource": not validate_packet(nonclifford_missing)["ok"],
        "nonclifford_stage_accepts_resource": validate_packet(nonclifford_good)["ok"],
        "semantic_identity_independent_of_backend_path": (
            packet.semantic_transition_digest == same_semantics_other_route_target.semantic_transition_digest
            and packet.packet_id != same_semantics_other_route_target.packet_id
        ),
        "hypervisor_address_uses_1296_space": hyper.packed < 1296,
    }
    return {
        "schema": "w33.universal-control-packet-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "sample": {
            "packet_id": packet.packet_id,
            "route": list(packet.route),
            "word": [asdict(op) for op in packet.microcode],
            "word_length": len(packet.microcode),
            "hypervisor": {
                "packed": hyper.packed,
                "base": hyper.base,
                "circuit216": hyper.circuit216,
                "pair216": hyper.pair216,
            },
        },
        "interpretation": (
            "A guest transition is a backend-independent semantic object. A control packet "
            "is the proof-carrying finite realization of that transition: route, microcode, "
            "PSp target, Sp lift, hypervisor placement and physical evidence all verify separately."
        ),
        "boundary": (
            "Word length <=5 is checked against the imported exhaustive Sp(4,3) envelope, "
            "but this verifier does not prove that a supplied word is minimal. Physical and "
            "non-Clifford evidence fields are integrity commitments, not measurements created here."
        ),
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["status"] == "PASS" else 1)
