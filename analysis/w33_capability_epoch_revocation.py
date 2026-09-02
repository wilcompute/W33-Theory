#!/usr/bin/env python3
"""Revocation epochs for otherwise monotone immutable W33 capabilities.

The existing Merkle memory capabilities are intentionally monotone: derived
capabilities can only narrow prefix/rights/carrier.  Pure monotonicity does not
answer operational revocation after a guest, component, or deployment is
compromised.

This module adds a separate authority plane:
  * immutable capability tokens remain content-addressed;
  * an issuer publishes a current epoch + selective revocation root;
  * every memory use validates the token against that root;
  * selective revocation kills one token and all descendants carrying its
    ancestry marker;
  * epoch rotation invalidates every token from the prior epoch at once.

Revocation therefore does not require mutating a capability in place and cannot
be used to widen rights.  This is a software authority model, not a hardware
capability-tag implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Sequence

from w33_merkle_capability_memory import (
    ContentStore,
    MemoryCapability,
    PersistentMemory,
    validate_address,
)
from w33_typed_universal_microvm import Carrier


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class EpochCapability:
    issuer: str
    epoch: int
    base: MemoryCapability
    ancestry: tuple[str, ...] = ()

    @property
    def cap_id(self) -> str:
        return digest({
            "issuer": self.issuer,
            "epoch": self.epoch,
            "base": self.base.descriptor(),
            "ancestry": list(self.ancestry),
        })

    def derive(self, suffix: Sequence[int], rights: Iterable[str]) -> "EpochCapability":
        child_base = self.base.derive(suffix, rights)
        return EpochCapability(
            issuer=self.issuer,
            epoch=self.epoch,
            base=child_base,
            ancestry=self.ancestry + (self.cap_id,),
        )


class RevocationAuthority:
    def __init__(self, issuer: str) -> None:
        if not issuer:
            raise ValueError("issuer required")
        self.issuer = issuer
        self.epoch = 0
        self.revoked: set[str] = set()

    @property
    def root(self) -> str:
        return digest({"issuer": self.issuer, "epoch": self.epoch, "revoked": sorted(self.revoked)})

    def mint(self, base: MemoryCapability) -> EpochCapability:
        return EpochCapability(self.issuer, self.epoch, base)

    def revoke(self, capability: EpochCapability) -> str:
        if capability.issuer != self.issuer:
            raise PermissionError("cannot revoke capability from another issuer")
        self.revoked.add(capability.cap_id)
        return self.root

    def rotate_epoch(self) -> str:
        self.epoch += 1
        self.revoked.clear()
        return self.root

    def validate(self, capability: EpochCapability) -> bool:
        if capability.issuer != self.issuer or capability.epoch != self.epoch:
            return False
        ids = set(capability.ancestry) | {capability.cap_id}
        return not bool(ids & self.revoked)


@dataclass(frozen=True)
class RevocableMemory:
    memory: PersistentMemory
    authority: RevocationAuthority

    def _base(self, cap: EpochCapability, address: Sequence[int], right: str) -> MemoryCapability:
        if not self.authority.validate(cap):
            raise PermissionError("capability revoked or stale epoch")
        addr = validate_address(address)
        if not cap.base.authorizes(addr, right):
            raise PermissionError(f"capability does not authorize {right} at {addr}")
        if cap.base.carrier != self.memory.machine_type:
            raise PermissionError("capability carrier does not match memory")
        return cap.base

    def read(self, cap: EpochCapability, address: Sequence[int]) -> Any:
        base = self._base(cap, address, "read")
        return self.memory.read(base, address)

    def write(self, cap: EpochCapability, address: Sequence[int], value: Any) -> "RevocableMemory":
        base = self._base(cap, address, "write")
        return RevocableMemory(self.memory.write(base, address, value), self.authority)


def verify() -> dict[str, Any]:
    store = ContentStore()
    base = MemoryCapability(Carrier.CIRCUIT_ST81)
    mem = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
    auth = RevocationAuthority("w33-runtime-root")
    root = auth.mint(base)
    child = root.derive((7,), {"read", "write", "derive"})
    grandchild = child.derive((1,), {"read"})

    rmem = RevocableMemory(mem, auth)
    rmem = rmem.write(child, (7, 1), {"secret": 36})
    before = rmem.read(grandchild, (7, 1))
    root_before_revoke = auth.root
    root_after_revoke = auth.revoke(child)

    descendant_revoked = False
    try:
        rmem.read(grandchild, (7, 1))
    except PermissionError:
        descendant_revoked = True

    sibling = root.derive((9,), {"read", "write"})
    sibling_alive = auth.validate(sibling)

    old_root_stale = False
    auth.rotate_epoch()
    try:
        rmem.read(root, (7, 1))
    except PermissionError:
        old_root_stale = True

    fresh = auth.mint(base).derive((7,), {"read"})
    fresh_reads = rmem.read(fresh, (7, 1))

    escalation_blocked = False
    try:
        fresh.derive((), {"read", "write"})
    except PermissionError:
        escalation_blocked = True

    checks = {
        "capability_works_before_revocation": before == {"secret": 36},
        "revocation_root_changes": root_after_revoke != root_before_revoke,
        "ancestor_revocation_kills_descendant": descendant_revoked,
        "unrelated_sibling_survives_selective_revocation": sibling_alive,
        "epoch_rotation_invalidates_all_old_tokens": old_root_stale,
        "fresh_epoch_token_can_recover_authorized_access": fresh_reads == {"secret": 36},
        "revocation_layer_does_not_enable_rights_escalation": escalation_blocked,
        "token_identity_is_content_addressed": fresh.cap_id.startswith("sha256:"),
    }
    return {
        "schema": "w33.capability-epoch-revocation.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "current_revocation_root": auth.root,
        "current_epoch": auth.epoch,
        "checks": checks,
        "interpretation": "Immutable monotone capabilities gain operational revocation through a separately authenticated epoch/root plane; selective revocation and global rotation do not mutate or widen the capability itself.",
        "honesty_boundary": "This is a software authority model. It does not provide CHERI-style hardware tags, TPM attestation, or distributed consensus on revocation roots.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
