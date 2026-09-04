#!/usr/bin/env python3
"""First-class bounded capability pointers for W33 Merkle memory.

This turns the existing memory-capability and epoch-revocation objects into an
actual virtual-memory ISA.  A pointer commits

    (Merkle root, fixed-depth base-40 address, bounds, cursor, rights,
     authority epoch, carrier/module, evidence floor, seal state).

The design follows the capability-machine discipline used by CHERI -- authority
travels with a pointer and can only be narrowed -- while preserving this repo's
native W33 details: addresses are base-40 Merkle coordinates, carrier type is
construction-time, epochs/revocation live in a separate authority plane, and a
physical backend may require a stronger evidence tier than a software model.

Important differences from hardware CHERI are explicit.  There is no hidden tag
bit in Python and no claim of hardware unforgeability.  A pointer is admitted
only when its EpochCapability validates against the current authority, its
snapshot root matches the memory object being accessed, and all monotone bounds,
rights, carrier and evidence checks pass.

Literature anchor: CHERI ISA v9 (UCAM-CL-TR-987) describes bounded, permissioned,
provenance-carrying capabilities and discusses epoch/revocation mechanisms.  The
specific base-40 address encoding and evidence-tier field here are W33 project
constructions, not CHERI claims.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import IntEnum
import hashlib
import json
from typing import Any, Iterable, Sequence

from w33_capability_epoch_revocation import EpochCapability, RevocationAuthority
from w33_merkle_capability_memory import PersistentMemory, validate_address
from w33_typed_universal_microvm import Carrier


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


class EvidenceTier(IntEnum):
    MODEL = 0
    VERIFIED_SOFTWARE = 1
    CALIBRATED_DEVICE = 2
    ATTESTED_DEVICE = 3

    @classmethod
    def parse(cls, value: "EvidenceTier | int | str") -> "EvidenceTier":
        if isinstance(value, cls):
            return value
        if isinstance(value, int):
            return cls(value)
        return cls[str(value).upper()]


def address_index(address: Sequence[int]) -> int:
    """Interpret a fixed-depth W33 tuple as one base-40 integer."""
    row = validate_address(address)
    out = 0
    for digit in row:
        out = 40 * out + digit
    return out


def index_address(value: int, depth: int) -> tuple[int, ...]:
    if depth < 0 or value < 0 or value >= 40 ** depth:
        raise ValueError("index does not fit fixed W33 address depth")
    out = [0] * depth
    x = int(value)
    for i in range(depth - 1, -1, -1):
        out[i] = x % 40
        x //= 40
    return tuple(out)


def prefix_interval(prefix: Sequence[int], depth: int) -> tuple[int, int]:
    p = validate_address(prefix)
    if len(p) > depth:
        raise ValueError("capability prefix is deeper than pointer address")
    scale = 40 ** (depth - len(p))
    start = address_index(p) * scale
    return start, start + scale


@dataclass(frozen=True)
class CapabilityPointer:
    epoch_cap: EpochCapability
    memory_root: str
    depth: int
    base: int
    length: int
    cursor: int
    rights: frozenset[str]
    evidence_floor: EvidenceTier = EvidenceTier.MODEL
    sealed: bool = False

    def __post_init__(self) -> None:
        if not (isinstance(self.memory_root, str) and self.memory_root.startswith("sha256:") and len(self.memory_root) == 71):
            raise ValueError("pointer must commit a SHA-256 Merkle root")
        if self.depth < 0:
            raise ValueError("depth must be nonnegative")
        limit = 40 ** self.depth
        if self.length <= 0 or self.base < 0 or self.base + self.length > limit:
            raise ValueError("capability bounds exceed fixed-depth W33 address space")
        if not self.base <= self.cursor < self.base + self.length:
            raise ValueError("cursor is outside capability bounds")
        allowed = frozenset({"read", "write", "derive"})
        if not self.rights or not self.rights <= allowed:
            raise ValueError("unknown or empty pointer rights")
        if not self.rights <= self.epoch_cap.base.rights:
            raise PermissionError("pointer rights exceed authority token")
        p0, p1 = prefix_interval(self.epoch_cap.base.prefix, self.depth)
        if self.base < p0 or self.base + self.length > p1:
            raise PermissionError("pointer bounds escape authority prefix")
        EvidenceTier.parse(self.evidence_floor)

    @property
    def carrier(self) -> Carrier:
        return self.epoch_cap.base.carrier

    @property
    def address(self) -> tuple[int, ...]:
        return index_address(self.cursor, self.depth)

    @property
    def end(self) -> int:
        return self.base + self.length

    @property
    def pointer_id(self) -> str:
        return digest(self.descriptor())

    def descriptor(self) -> dict[str, Any]:
        return {
            "schema": "w33.capability-pointer.v1",
            "epoch_cap_id": self.epoch_cap.cap_id,
            "issuer": self.epoch_cap.issuer,
            "epoch": self.epoch_cap.epoch,
            "memory_root": self.memory_root,
            "depth": self.depth,
            "base": self.base,
            "length": self.length,
            "cursor": self.cursor,
            "address": list(self.address),
            "rights": sorted(self.rights),
            "carrier": self.carrier.value,
            "evidence_floor": EvidenceTier.parse(self.evidence_floor).name,
            "sealed": self.sealed,
        }

    @classmethod
    def from_epoch_cap(
        cls,
        cap: EpochCapability,
        memory: PersistentMemory,
        depth: int,
        *,
        cursor: Sequence[int] | None = None,
        rights: Iterable[str] | None = None,
        evidence_floor: EvidenceTier = EvidenceTier.MODEL,
    ) -> "CapabilityPointer":
        p0, p1 = prefix_interval(cap.base.prefix, depth)
        cur = p0 if cursor is None else address_index(cursor)
        selected = frozenset(cap.base.rights if rights is None else rights)
        return cls(cap, memory.root, depth, p0, p1 - p0, cur, selected, evidence_floor)

    def offset(self, delta: int) -> "CapabilityPointer":
        nxt = self.cursor + int(delta)
        if not self.base <= nxt < self.end:
            raise PermissionError("capability pointer arithmetic crossed bounds")
        return replace(self, cursor=nxt)

    def set_bounds(self, base: int, length: int) -> "CapabilityPointer":
        base, length = int(base), int(length)
        if length <= 0 or base < self.base or base + length > self.end:
            raise PermissionError("CSETBOUNDS may only narrow the current region")
        if not base <= self.cursor < base + length:
            raise PermissionError("new bounds would exclude the current cursor")
        return replace(self, base=base, length=length)

    def restrict_rights(self, rights: Iterable[str]) -> "CapabilityPointer":
        narrowed = frozenset(rights)
        if not narrowed or not narrowed <= self.rights:
            raise PermissionError("CANDPERM may only remove rights")
        return replace(self, rights=narrowed)

    def require_evidence(self, tier: EvidenceTier | int | str) -> "CapabilityPointer":
        target = EvidenceTier.parse(tier)
        current = EvidenceTier.parse(self.evidence_floor)
        if target < current:
            raise PermissionError("evidence requirement may only become stricter")
        return replace(self, evidence_floor=target)

    def seal(self) -> "CapabilityPointer":
        return replace(self, sealed=True)

    def _admit(
        self,
        memory: PersistentMemory,
        authority: RevocationAuthority,
        right: str,
        evidence: EvidenceTier | int | str,
    ) -> tuple[int, ...]:
        if self.sealed:
            raise PermissionError("sealed capability is not dereferenceable")
        if memory.root != self.memory_root:
            raise PermissionError("capability is bound to a different Merkle snapshot")
        if memory.machine_type != self.carrier:
            raise PermissionError("capability carrier does not match memory machine type")
        if not authority.validate(self.epoch_cap):
            raise PermissionError("capability revoked or stale epoch")
        if right not in self.rights:
            raise PermissionError(f"capability lacks {right} right")
        if EvidenceTier.parse(evidence) < EvidenceTier.parse(self.evidence_floor):
            raise PermissionError("backend evidence tier is below capability requirement")
        address = self.address
        if not self.epoch_cap.base.authorizes(address, right):
            raise PermissionError("underlying authority token rejects address/right")
        return address

    def load(
        self,
        memory: PersistentMemory,
        authority: RevocationAuthority,
        evidence: EvidenceTier | int | str = EvidenceTier.MODEL,
    ) -> Any:
        address = self._admit(memory, authority, "read", evidence)
        return memory.read(self.epoch_cap.base, address)

    def store(
        self,
        memory: PersistentMemory,
        authority: RevocationAuthority,
        value: Any,
        evidence: EvidenceTier | int | str = EvidenceTier.MODEL,
    ) -> tuple[PersistentMemory, "CapabilityPointer"]:
        address = self._admit(memory, authority, "write", evidence)
        updated = memory.write(self.epoch_cap.base, address, value)
        return updated, replace(self, memory_root=updated.root)


class CapabilityAddressISA:
    """Tiny reference instruction machine for first-class capability words."""

    def __init__(self) -> None:
        self.caps: dict[str, CapabilityPointer] = {}
        self.values: dict[str, Any] = {}

    def bind(self, register: str, pointer: CapabilityPointer) -> None:
        self.caps[str(register)] = pointer

    def execute(
        self,
        instruction: dict[str, Any],
        memory: PersistentMemory,
        authority: RevocationAuthority,
        evidence: EvidenceTier | int | str = EvidenceTier.MODEL,
    ) -> PersistentMemory:
        op = str(instruction["op"]).upper()
        rd = str(instruction.get("rd", ""))
        rs = str(instruction.get("rs", ""))
        if op == "CINC":
            self.caps[rd] = self.caps[rs].offset(int(instruction["delta"]))
        elif op == "CSETBOUNDS":
            self.caps[rd] = self.caps[rs].set_bounds(int(instruction["base"]), int(instruction["length"]))
        elif op == "CANDPERM":
            self.caps[rd] = self.caps[rs].restrict_rights(instruction["rights"])
        elif op == "CREQUIRE":
            self.caps[rd] = self.caps[rs].require_evidence(instruction["tier"])
        elif op == "CSEAL":
            self.caps[rd] = self.caps[rs].seal()
        elif op == "CLOAD":
            self.values[rd] = self.caps[rs].load(memory, authority, evidence)
        elif op == "CSTORE":
            source = self.caps[rs]
            value = self.values[str(instruction["value_reg"])] if "value_reg" in instruction else instruction.get("value")
            memory, fresh = source.store(memory, authority, value, evidence)
            self.caps[rs] = fresh
        else:
            raise ValueError(f"unknown capability opcode {op}")
        return memory


def verify() -> dict[str, Any]:
    from w33_capability_epoch_revocation import RevocationAuthority
    from w33_merkle_capability_memory import ContentStore, MemoryCapability, PersistentMemory

    store = ContentStore()
    memory = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
    authority = RevocationAuthority("w33-capability-address-root")
    epoch_cap = authority.mint(MemoryCapability(Carrier.CIRCUIT_ST81, prefix=(7,)))
    ptr = CapabilityPointer.from_epoch_cap(
        epoch_cap,
        memory,
        depth=3,
        cursor=(7, 1, 2),
        evidence_floor=EvidenceTier.VERIFIED_SOFTWARE,
    )

    roundtrip = all(index_address(address_index(a), len(a)) == a for a in ((0,), (7, 1, 2), (39, 39, 39)))
    prefix_lo, prefix_hi = prefix_interval((7,), 3)
    ptr = ptr.set_bounds(prefix_lo + 40, 80)  # addresses 7,1,0 through 7,2,39
    ptr = ptr.offset(address_index((7, 1, 2)) - ptr.cursor)

    weak_evidence_blocked = False
    try:
        ptr.load(memory, authority, EvidenceTier.MODEL)
    except PermissionError:
        weak_evidence_blocked = True

    # Store through the software-verified pointer; persistent memory returns a
    # new root and the pointer returned by CSTORE follows that new snapshot.
    memory, current = ptr.store(memory, authority, {"word": 137}, EvidenceTier.VERIFIED_SOFTWARE)
    stored = current.load(memory, authority, EvidenceTier.VERIFIED_SOFTWARE)

    stale_snapshot_blocked = False
    try:
        ptr.load(memory, authority, EvidenceTier.VERIFIED_SOFTWARE)
    except PermissionError:
        stale_snapshot_blocked = True

    read_only = current.restrict_rights({"read"})
    write_blocked = False
    try:
        read_only.store(memory, authority, 999, EvidenceTier.VERIFIED_SOFTWARE)
    except PermissionError:
        write_blocked = True

    bounds_blocked = False
    try:
        current.offset(current.length + 1)
    except PermissionError:
        bounds_blocked = True

    rights_escalation_blocked = False
    try:
        read_only.restrict_rights({"read", "write"})
    except PermissionError:
        rights_escalation_blocked = True

    evidence_downgrade_blocked = False
    calibrated = current.require_evidence(EvidenceTier.CALIBRATED_DEVICE)
    try:
        calibrated.require_evidence(EvidenceTier.MODEL)
    except PermissionError:
        evidence_downgrade_blocked = True

    calibrated_gate_blocks_software = False
    try:
        calibrated.load(memory, authority, EvidenceTier.VERIFIED_SOFTWARE)
    except PermissionError:
        calibrated_gate_blocks_software = True
    calibrated_reads = calibrated.load(memory, authority, EvidenceTier.CALIBRATED_DEVICE)

    sealed_blocked = False
    try:
        current.seal().load(memory, authority, EvidenceTier.ATTESTED_DEVICE)
    except PermissionError:
        sealed_blocked = True

    authority.rotate_epoch()
    stale_epoch_blocked = False
    try:
        current.load(memory, authority, EvidenceTier.ATTESTED_DEVICE)
    except PermissionError:
        stale_epoch_blocked = True

    # ISA path: mint a fresh pointer against the current snapshot and exercise
    # pointer arithmetic + load through architectural registers.
    fresh_cap = authority.mint(MemoryCapability(Carrier.CIRCUIT_ST81, prefix=(7,)))
    fresh = CapabilityPointer.from_epoch_cap(
        fresh_cap, memory, 3, cursor=(7, 1, 2), evidence_floor=EvidenceTier.VERIFIED_SOFTWARE
    ).set_bounds(prefix_lo + 40, 80)
    isa = CapabilityAddressISA()
    isa.bind("c0", fresh)
    memory = isa.execute({"op": "CINC", "rd": "c1", "rs": "c0", "delta": 0}, memory, authority)
    memory = isa.execute({"op": "CLOAD", "rd": "v0", "rs": "c1"}, memory, authority, EvidenceTier.VERIFIED_SOFTWARE)

    checks = {
        "base40_address_roundtrip": roundtrip,
        "prefix_interval_is_contiguous": prefix_hi - prefix_lo == 40 ** 2,
        "pointer_is_inside_authority_prefix": current.base >= prefix_lo and current.end <= prefix_hi,
        "weak_evidence_refused": weak_evidence_blocked,
        "store_and_load_succeed": stored == {"word": 137},
        "persistent_snapshot_binding_refuses_stale_pointer": stale_snapshot_blocked,
        "write_permission_is_monotone": write_blocked,
        "bounds_are_monotone": bounds_blocked,
        "rights_cannot_reexpand": rights_escalation_blocked,
        "evidence_floor_cannot_weaken": evidence_downgrade_blocked,
        "calibration_floor_is_enforced": calibrated_gate_blocks_software and calibrated_reads == {"word": 137},
        "sealed_pointer_is_not_dereferenceable": sealed_blocked,
        "epoch_rotation_revokes_old_pointer": stale_epoch_blocked,
        "isa_register_load_matches_direct_load": isa.values.get("v0") == {"word": 137},
        "pointer_identity_is_content_addressed": current.pointer_id.startswith("sha256:"),
    }
    return {
        "schema": "w33.capability-address-isa-certificate.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "opcodes": ["CINC", "CSETBOUNDS", "CANDPERM", "CREQUIRE", "CSEAL", "CLOAD", "CSTORE"],
        "pointer_fields": [
            "merkle_root", "base40_address", "bounds", "rights", "epoch",
            "carrier", "evidence_floor", "seal_state",
        ],
        "sample_pointer": current.descriptor(),
        "checks": checks,
        "interpretation": (
            "W33 Merkle addresses are now first-class authority-bearing machine words: "
            "pointer arithmetic, bounds, permissions, revocation epochs, carrier type and "
            "evidence admission are checked at the dereference boundary."
        ),
        "honesty_boundary": (
            "Software validation is exact for this model, but Python objects do not provide "
            "CHERI-style hidden hardware tags. Hardware unforgeability remains a separate implementation step."
        ),
    }


if __name__ == "__main__":
    out = verify()
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if out["status"] == "PASS" else 1)
