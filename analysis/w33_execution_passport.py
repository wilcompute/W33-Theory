#!/usr/bin/env python3
"""Proof-carrying execution passport for the W33/Holonet runtime stack.

Version 2 promotes three previously separate runtime control planes into the
packet identity itself:
  * capability authority epoch + selective revocation root,
  * deterministic asynchronous schedule root,
  * temporal Merkle root-registry identity.

The passport already binds guest validation, component link, memory capability
and snapshot, packet refinement, immutable machine carrier, the two distinct
order-51840 symmetry namespaces, magic budget, and reversible-history policy.
A packet is admitted only against the exact passport, current capability epoch,
and current revocation root.

The passport digest is an integrity commitment, not a digital signature or a
remote-attestation certificate. Production authorization remains the signed /
hardware-root layer (the sibling Holotrade runtime binds passports into signed
receipt metadata).
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
    capability_epoch: int
    revocation_root: str
    schedule_root: str
    gc_registry_root: str
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
    capability_epoch: int
    revocation_root: str


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
        "schema_v2": passport.schema == "w33.execution-passport.v2",
        "known_carrier": expected_dim is not None,
        "logical_dimension_matches_carrier": expected_dim == passport.logical_dimension,
        "memory_is_content_addressed": is_digest(passport.memory_root),
        "memory_capability_is_committed": is_digest(passport.memory_capability_digest),
        "component_link_is_committed": is_digest(passport.component_link_digest),
        "symmetry_namespaces_do_not_alias": passport.clifford_namespace != passport.projective_weyl_namespace,
        "magic_budget_nonnegative": isinstance(passport.magic_budget, int) and passport.magic_budget >= 0,
        "history_root_is_committed": is_digest(passport.history_root),
        "erasure_policy_typed": passport.erasure_policy in {"RETAIN_OR_UNCOMPUTE", "EXPLICIT_DISCARD_ONLY"},
        "capability_epoch_nonnegative": isinstance(passport.capability_epoch, int) and passport.capability_epoch >= 0,
        "revocation_root_committed": is_digest(passport.revocation_root),
        "async_schedule_committed": is_digest(passport.schedule_root),
        "gc_registry_committed": is_digest(passport.gc_registry_root),
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
        "capability_epoch_current": packet.capability_epoch == passport.capability_epoch,
        "revocation_root_current": packet.revocation_root == passport.revocation_root,
    }
    return {"ok": all(checks.values()), "checks": checks, "passport_checks": pv["checks"]}


def verify() -> dict[str, Any]:
    from w33_capability_epoch_revocation import RevocationAuthority
    from w33_temporal_merkle_gc import RootRegistry

    interface = Interface("w33:ipc36", (("send", FuncSig(("u32", "u32", "handle36"), ("future<u32>",), True)),))
    link = ComponentLinker().link(
        ComponentDecl("guest", Carrier.CIRCUIT_ST81, imports=(interface,)),
        ComponentDecl("kernel", Carrier.PAIR_ST64, exports=(interface,)),
        "w33:ipc36",
    )

    store = ContentStore()
    cap = MemoryCapability(Carrier.CIRCUIT_ST81)
    memory = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81).write(cap, (3, 1), {"passport": "state"})

    authority = RevocationAuthority("passport-demo-authority")
    registry = RootRegistry()
    registry.pin("LIVE_VM", "passport-demo", memory.root, "STRONG")
    schedule_root = digest({
        "scheduler": "record-replay",
        "operations": ["send:first", "recv:first", "pump"],
    })

    evidence = (
        Evidence("guest-validator", "VALIDATED", file_digest("analysis/w33_wasm3_capability_runtime.py")),
        Evidence("component-linker", "PASS", file_digest("analysis/w33_component_async36.py")),
        Evidence("packet-refinement", "PASS", file_digest("rtl/w33_universal_packet_microsequencer.v")),
        Evidence("magic-port-abi", "VERIFIED", file_digest("data/bt1385_hesse_sic_t_port_abi.json")),
    )
    passport = ExecutionPassport(
        schema="w33.execution-passport.v2",
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
        capability_epoch=authority.epoch,
        revocation_root=authority.root,
        schedule_root=schedule_root,
        gc_registry_root=registry.registry_root,
        evidence=evidence,
    )
    packet = PacketRequest(
        passport.passport_id,
        passport.carrier,
        1,
        digest({"payload": [1, 2, 3]}),
        passport.capability_epoch,
        passport.revocation_root,
    )
    admitted = admit_packet(packet, passport)

    over_budget = admit_packet(replace(packet, required_magic=3), passport)
    wrong_carrier = admit_packet(replace(packet, carrier=Carrier.PAIR_ST64.value), passport)
    stale_epoch = admit_packet(replace(packet, capability_epoch=passport.capability_epoch + 1), passport)
    wrong_revocation = admit_packet(replace(packet, revocation_root=digest({"revoked": True})), passport)
    tampered_passport = replace(passport, schedule_root=digest({"schedule": "tampered"}))
    stale_id = admit_packet(packet, tampered_passport)
    aliased = validate_passport(replace(passport, projective_weyl_namespace=passport.clifford_namespace))

    checks = {
        "valid_packet_admitted": admitted["ok"],
        "magic_overdraft_refused": not over_budget["ok"],
        "carrier_relabel_refused": not wrong_carrier["ok"],
        "stale_capability_epoch_refused": not stale_epoch["ok"],
        "wrong_revocation_root_refused": not wrong_revocation["ok"],
        "schedule_mutation_changes_identity": tampered_passport.passport_id != passport.passport_id and not stale_id["ok"],
        "equal_order_namespace_alias_refused": not aliased["ok"],
        "control_planes_are_content_addressed": all(is_digest(x) for x in (passport.revocation_root, passport.schedule_root, passport.gc_registry_root)),
        "evidence_spans_guest_component_packet_magic": REQUIRED_EVIDENCE == {e.name for e in evidence},
    }
    return {
        "schema": "w33.execution-passport-certificate.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passport_id": passport.passport_id,
        "control_plane": {
            "capability_epoch": passport.capability_epoch,
            "revocation_root": passport.revocation_root,
            "schedule_root": passport.schedule_root,
            "gc_registry_root": passport.gc_registry_root,
        },
        "checks": checks,
        "interpretation": "Packet identity now commits authority epoch/revocation, asynchronous wake schedule, and retained-state reachability in addition to guest, memory, carrier, packet, magic, and history semantics.",
        "honesty_boundary": "The SHA-256 passport is an integrity commitment, not cryptographic authorization, distributed revocation consensus, or remote attestation.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
