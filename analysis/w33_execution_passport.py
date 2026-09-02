#!/usr/bin/env python3
"""Proof-carrying execution passport for the W33/Holonet runtime stack.

A packet should not need to rediscover its execution authority from loose runtime
state.  This module packages content identities for the guest validator,
component link, memory capability/snapshot, packet refinement, machine carrier,
symmetry namespaces, magic budget, and reversible-history policy into one
content-addressed passport.  Packet admission is fail closed against that
passport.

The passport digest is an integrity commitment, not a digital signature or a
remote-attestation certificate.  Production authorization still needs a signing
key / hardware root of trust (Holotrade has a separate signed-receipt layer).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import hashlib
import json
from pathlib import Path
from typing import Any

from w33_component_async36 import ComponentDecl, ComponentLinker, FuncSig, Interface
from w33_merkle_capability_memory import ContentStore, MemoryCapability, PersistentMemory
from w33_typed_universal_microvm import Carrier

ROOT = Path(__file__).resolve().parents[1]


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def file_digest(path: str) -> str:
    return "sha256:" + hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def is_digest(value: str) -> bool:
    return isinstance(value, str) and value.startswith("sha256:") and len(value) == 71


def logical_dim(carrier: Carrier) -> int:
    return 81 if carrier == Carrier.CIRCUIT_ST81 else 64


@dataclass(frozen=True)
class Evidence:
    name: str
    status: str
    artifact_digest: str


@dataclass(frozen=True)
class ExecutionPassport:
    schema: str
    guest_image: str
    carrier: str
    logical_dimension: int
    memory_root: str
    memory_capability_digest: str
    component_link_digest: str
    clifford_namespace: str
    projective_weyl_namespace: str
    magic_resource: str
    magic_budget: int
    history_root: str
    erasure_policy: str
    evidence: tuple[Evidence, ...]
    runtime_retype: str = "FORBIDDEN"

    def body(self) -> dict[str, Any]:
        row = asdict(self)
        row["evidence"] = [asdict(e) for e in self.evidence]
        return row

    @property
    def passport_id(self) -> str:
        return digest(self.body())


@dataclass(frozen=True)
class PacketRequest:
    passport_id: str
    carrier: str
    required_magic: int
    payload_digest: str


REQUIRED_EVIDENCE = {
    "guest-validator",
    "component-linker",
    "packet-refinement",
    "magic-port-abi",
}


def validate_passport(passport: ExecutionPassport) -> dict[str, Any]:
    expected_dim = 81 if passport.carrier == Carrier.CIRCUIT_ST81.value else 64 if passport.carrier == Carrier.PAIR_ST64.value else None
    evidence_names = {e.name for e in passport.evidence if e.status in {"PASS", "VALIDATED", "VERIFIED"}}
    checks = {
        "known_carrier": expected_dim is not None,
        "logical_dimension_matches_carrier": expected_dim == passport.logical_dimension,
        "memory_is_content_addressed": is_digest(passport.memory_root),
        "memory_capability_is_committed": is_digest(passport.memory_capability_digest),
        "component_link_is_committed": is_digest(passport.component_link_digest),
        "symmetry_namespaces_do_not_alias": passport.clifford_namespace != passport.projective_weyl_namespace,
        "magic_budget_nonnegative": passport.magic_budget >= 0,
        "history_root_is_committed": is_digest(passport.history_root),
        "erasure_policy_typed": passport.erasure_policy in {"RETAIN_OR_UNCOMPUTE", "EXPLICIT_DISCARD_ONLY"},
        "runtime_retype_forbidden": passport.runtime_retype == "FORBIDDEN",
        "required_evidence_present": REQUIRED_EVIDENCE <= evidence_names,
        "all_evidence_content_addressed": all(is_digest(e.artifact_digest) for e in passport.evidence),
    }
    return {"ok": all(checks.values()), "checks": checks}


def admit_packet(packet: PacketRequest, passport: ExecutionPassport) -> dict[str, Any]:
    pv = validate_passport(passport)
    checks = {
        "passport_valid": pv["ok"],
        "packet_binds_exact_passport": packet.passport_id == passport.passport_id,
        "carrier_matches": packet.carrier == passport.carrier,
        "magic_budget_sufficient": 0 <= packet.required_magic <= passport.magic_budget,
        "payload_content_addressed": is_digest(packet.payload_digest),
    }
    return {"ok": all(checks.values()), "checks": checks, "passport_checks": pv["checks"]}


def verify() -> dict[str, Any]:
    interface = Interface("w33:ipc36", (("send", FuncSig(("u32", "u32", "handle36"), ("future<u32>",), True)),))
    link = ComponentLinker().link(
        ComponentDecl("guest", Carrier.CIRCUIT_ST81, imports=(interface,)),
        ComponentDecl("kernel", Carrier.PAIR_ST64, exports=(interface,)),
        "w33:ipc36",
    )

    store = ContentStore()
    cap = MemoryCapability(Carrier.CIRCUIT_ST81)
    memory = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81).write(cap, (3, 1), {"passport": "state"})

    evidence = (
        Evidence("guest-validator", "VALIDATED", file_digest("analysis/w33_wasm3_capability_runtime.py")),
        Evidence("component-linker", "PASS", file_digest("analysis/w33_component_async36.py")),
        Evidence("packet-refinement", "PASS", file_digest("rtl/w33_universal_packet_microsequencer.v")),
        Evidence("magic-port-abi", "VERIFIED", file_digest("data/bt1385_hesse_sic_t_port_abi.json")),
    )
    passport = ExecutionPassport(
        schema="w33.execution-passport.v1",
        guest_image=digest({"guest": "demo-component"}),
        carrier=Carrier.CIRCUIT_ST81.value,
        logical_dimension=81,
        memory_root=memory.root,
        memory_capability_digest=digest(cap.descriptor()),
        component_link_digest=link["link_digest"],
        clifford_namespace="Sp(4,3)-clifford-lift",
        projective_weyl_namespace="PGSp(4,3)-projective-weyl",
        magic_resource="hesse_sic_t_token",
        magic_budget=2,
        history_root=digest({"history": []}),
        erasure_policy="EXPLICIT_DISCARD_ONLY",
        evidence=evidence,
    )
    packet = PacketRequest(passport.passport_id, passport.carrier, 1, digest({"payload": [1, 2, 3]}))
    admitted = admit_packet(packet, passport)

    over_budget = admit_packet(replace(packet, required_magic=3), passport)
    wrong_carrier = admit_packet(replace(packet, carrier=Carrier.PAIR_ST64.value), passport)
    tampered_passport = replace(passport, magic_budget=99)
    stale_id = admit_packet(packet, tampered_passport)
    aliased = validate_passport(replace(passport, projective_weyl_namespace=passport.clifford_namespace))

    checks = {
        "valid_packet_admitted": admitted["ok"],
        "magic_overdraft_refused": not over_budget["ok"],
        "carrier_relabel_refused": not wrong_carrier["ok"],
        "passport_mutation_changes_identity": tampered_passport.passport_id != passport.passport_id and not stale_id["ok"],
        "equal_order_namespace_alias_refused": not aliased["ok"],
        "evidence_spans_guest_component_packet_magic": REQUIRED_EVIDENCE == {e.name for e in evidence},
    }
    return {
        "schema": "w33.execution-passport-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passport_id": passport.passport_id,
        "checks": checks,
        "interpretation": "Packet admission can be reduced to one immutable passport identity spanning guest validation, component linking, memory authority, carrier typing, packet refinement, magic budget, and reversible-history policy.",
        "honesty_boundary": "The SHA-256 passport is an integrity commitment, not cryptographic authorization or remote attestation.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
