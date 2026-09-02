#!/usr/bin/env python3
"""Temporal garbage collection for persistent W33 Merkle state.

Persistent copy-on-write memory deliberately retains old snapshots.  That is
necessary for checkpoints/reversible history, but a real runtime also needs a
precise rule for when unreachable blobs may be reclaimed.

This module separates two reference classes:
  * STRONG roots require the referenced Merkle bytes to remain readable
    (live VM, checkpoint, retained history, delegated shared subtree);
  * HASH_ONLY roots preserve only content identity for an audit/receipt. They do
    not force the runtime to retain the underlying bytes forever.

The collector marks all blobs reachable from STRONG roots (plus the canonical
empty node) and sweeps the rest. A DISCARD_HISTORY-style policy must release its
strong root before collection.  Sweeping logical content-addressed blobs is not
a claim about physical media sanitization or Landauer dissipation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from w33_merkle_capability_memory import ContentStore, MemoryCapability, PersistentMemory
from w33_typed_universal_microvm import Carrier


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class RootReference:
    reference_id: str
    kind: str
    owner: str
    root: str
    strength: str


class RootRegistry:
    VALID_STRENGTH = {"STRONG", "HASH_ONLY"}

    def __init__(self) -> None:
        self.references: dict[str, RootReference] = {}

    def pin(self, kind: str, owner: str, root: str, strength: str = "STRONG") -> RootReference:
        if strength not in self.VALID_STRENGTH:
            raise ValueError("unknown root strength")
        if not root.startswith("sha256:"):
            raise ValueError("root must be content addressed")
        rid = digest({"kind": kind, "owner": owner, "root": root, "strength": strength})
        ref = RootReference(rid, kind, owner, root, strength)
        self.references[rid] = ref
        return ref

    def release(self, reference_id: str) -> RootReference:
        if reference_id not in self.references:
            raise KeyError("unknown root reference")
        return self.references.pop(reference_id)

    def strong_roots(self) -> set[str]:
        return {r.root for r in self.references.values() if r.strength == "STRONG"}

    def audit_roots(self) -> set[str]:
        return {r.root for r in self.references.values() if r.strength == "HASH_ONLY"}

    @property
    def registry_root(self) -> str:
        return digest({
            "references": [
                {"id": r.reference_id, "kind": r.kind, "owner": r.owner, "root": r.root, "strength": r.strength}
                for r in sorted(self.references.values(), key=lambda x: x.reference_id)
            ]
        })


class TemporalMerkleGC:
    def __init__(self, store: ContentStore, registry: RootRegistry) -> None:
        self.store = store
        self.registry = registry

    def _mark(self, root: str, marked: set[str]) -> None:
        if root in marked:
            return
        row = self.store.blobs.get(root)
        if row is None:
            raise KeyError(f"strong Merkle root/blob is missing: {root}")
        marked.add(root)
        if row.get("kind") != "node":
            return
        for _, child in row.get("children", []):
            self._mark(child, marked)

    def plan(self) -> dict[str, Any]:
        marked: set[str] = {self.store.empty}
        for root in sorted(self.registry.strong_roots()):
            self._mark(root, marked)
        all_blobs = set(self.store.blobs)
        sweep = sorted(all_blobs - marked)
        return {
            "strong_roots": sorted(self.registry.strong_roots()),
            "hash_only_roots": sorted(self.registry.audit_roots()),
            "marked": sorted(marked),
            "sweep": sweep,
            "before": len(all_blobs),
            "after": len(marked),
            "registry_root": self.registry.registry_root,
        }

    def collect(self) -> dict[str, Any]:
        plan = self.plan()
        for key in plan["sweep"]:
            self.store.blobs.pop(key, None)
        plan["collected"] = len(plan["sweep"])
        return plan


def verify() -> dict[str, Any]:
    store = ContentStore()
    cap = MemoryCapability(Carrier.CIRCUIT_ST81)
    mem0 = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
    mem1 = mem0.write(cap, (7, 1, 2), {"version": 1})
    mem1 = mem1.write(cap, (9, 4, 5), {"shared": "stable"})
    old_value = mem1.read(cap, (7, 1, 2))
    mem2 = mem1.write(cap, (7, 1, 2), {"version": 2})
    new_value = mem2.read(cap, (7, 1, 2))

    registry = RootRegistry()
    live = registry.pin("LIVE_VM", "vm-81", mem2.root, "STRONG")
    checkpoint = registry.pin("CHECKPOINT", "checkpoint-old", mem1.root, "STRONG")
    receipt = registry.pin("SIGNED_RECEIPT", "receipt-old", mem1.root, "HASH_ONLY")

    gc = TemporalMerkleGC(store, registry)
    before_first = len(store.blobs)
    first = gc.collect()
    checkpoint_still_reads = store.read(mem1.root, (7, 1, 2))

    registry.release(checkpoint.reference_id)
    second = gc.collect()
    old_snapshot_bytes_gone = mem1.root not in store.blobs
    live_still_reads = store.read(mem2.root, (7, 1, 2))
    receipt_hash_retained = receipt.root in registry.audit_roots()

    # Releasing the live VM is equivalent to relinquishing the final strong
    # memory authority; only the canonical empty node must remain after sweep.
    registry.release(live.reference_id)
    third = gc.collect()

    checks = {
        "copy_on_write_versions_differ": old_value == {"version": 1} and new_value == {"version": 2} and mem1.root != mem2.root,
        "strong_checkpoint_protects_old_snapshot": checkpoint_still_reads == {"version": 1} and mem1.root in first["marked"],
        "hash_only_receipt_does_not_prevent_sweep": old_snapshot_bytes_gone and receipt_hash_retained,
        "live_root_survives_old_checkpoint_release": live_still_reads == {"version": 2} and mem2.root in second["marked"],
        "collector_never_sweeps_canonical_empty": store.empty in store.blobs,
        "final_release_leaves_only_empty_reachable": third["after"] == 1 and set(store.blobs) == {store.empty},
        "registry_is_content_addressed": registry.registry_root.startswith("sha256:"),
    }
    return {
        "schema": "w33.temporal-merkle-gc.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "first_collection": {k: first[k] for k in ("before", "after", "collected")},
        "second_collection": {k: second[k] for k in ("before", "after", "collected")},
        "third_collection": {k: third[k] for k in ("before", "after", "collected")},
        "checks": checks,
        "interpretation": "Persistent memory remains readable exactly while a strong runtime reference exists. Audit hashes may outlive bytes. Logical discard/release changes reachability; collection then reclaims only unreachable blobs.",
        "honesty_boundary": "Logical blob reclamation is not proof of physical media erasure, secure deletion, or thermodynamic cost.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
