#!/usr/bin/env python3
"""Zero-copy immutable Merkle subtree sharing over the common 36-state ABI.

The existing heterogeneous kernel sends content-addressed JSON objects.  This
module tightens the memory/data-plane connection: a carrier-bound W33 Merkle
memory may publish an immutable subtree digest to the neutral 36-state fabric.
Publishing/delegating a handle creates no new content blobs; receivers read the
same immutable subtree by digest with endpoint-bound authority.

"Zero-copy" is meant in this software/content-store sense: no payload bytes are
re-serialized into a second logical object on delegation.  It is not a claim
about DMA, cache coherence, optical hardware, or physical copy energy.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any, Sequence

from w33_heterogeneous_36_ipc import FiberEndpoint
from w33_merkle_capability_memory import ContentStore, MemoryCapability, PersistentMemory, validate_address
from w33_typed_universal_microvm import Carrier


@dataclass(frozen=True)
class MerkleSubtreeHandle36:
    subtree_root: str
    destination_carrier: str
    destination_base36: int
    source_snapshot_root: str
    rights: tuple[str, ...] = ("read",)

    def __post_init__(self) -> None:
        if not 0 <= self.destination_base36 < 36:
            raise ValueError("destination base must lie in 0..35")
        if self.rights != ("read",):
            raise ValueError("shared Merkle subtree handles are immutable/read-only")

    def descriptor(self) -> dict[str, Any]:
        return {
            "subtree_root": self.subtree_root,
            "destination_carrier": self.destination_carrier,
            "destination_base36": self.destination_base36,
            "source_snapshot_root": self.source_snapshot_root,
            "rights": list(self.rights),
        }


class MerkleObjectPlane36:
    def __init__(self, store: ContentStore) -> None:
        self.store = store

    def publish(self, memory: PersistentMemory, cap: MemoryCapability, prefix: Sequence[int],
                destination_carrier: Carrier, destination_base36: int) -> MerkleSubtreeHandle36:
        p = validate_address(prefix)
        if memory.store is not self.store:
            raise ValueError("zero-copy publication requires the shared content store")
        if cap.carrier != memory.machine_type or not cap.authorizes(p, "read"):
            raise PermissionError("memory capability does not authorize subtree publication")
        subtree = self.store.subtree(memory.root, p)
        if subtree is None:
            raise KeyError("cannot publish absent subtree")
        return MerkleSubtreeHandle36(
            subtree_root=subtree,
            destination_carrier=destination_carrier.value,
            destination_base36=int(destination_base36),
            source_snapshot_root=memory.root,
        )

    def delegate(self, handle: MerkleSubtreeHandle36, destination_carrier: Carrier,
                 destination_base36: int) -> MerkleSubtreeHandle36:
        if handle.subtree_root not in self.store.blobs:
            raise KeyError("subtree root is absent")
        return MerkleSubtreeHandle36(
            subtree_root=handle.subtree_root,
            destination_carrier=destination_carrier.value,
            destination_base36=int(destination_base36),
            source_snapshot_root=handle.source_snapshot_root,
        )

    def read(self, receiver: FiberEndpoint, handle: MerkleSubtreeHandle36,
             relative_address: Sequence[int] = ()) -> Any:
        if receiver.carrier.value != handle.destination_carrier or receiver.base36 != handle.destination_base36:
            raise PermissionError("Merkle handle is not delegated to this endpoint")
        return self.store.read(handle.subtree_root, validate_address(relative_address))


def root_cap(carrier: Carrier) -> MemoryCapability:
    return MemoryCapability(carrier)


def verify() -> dict[str, Any]:
    store = ContentStore()
    cap81 = root_cap(Carrier.CIRCUIT_ST81)
    mem = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
    mem = mem.write(cap81, (7, 1, 2), {"tensor": [3, 6, 9]})
    mem = mem.write(cap81, (7, 4, 5), {"tensor": [12, 15]})
    old_root = mem.root
    blobs_before_publish = len(store.blobs)

    plane = MerkleObjectPlane36(store)
    h64 = plane.publish(mem, cap81, (7,), Carrier.PAIR_ST64, 7)
    blobs_after_publish = len(store.blobs)
    h81 = plane.delegate(h64, Carrier.CIRCUIT_ST81, 9)
    blobs_after_delegate = len(store.blobs)

    receiver64 = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 5)
    receiver81 = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 9 + 1)
    value64 = plane.read(receiver64, h64, (1, 2))
    value81 = plane.read(receiver81, h81, (4, 5))

    wrong_endpoint_blocked = False
    try:
        plane.read(FiberEndpoint(Carrier.PAIR_ST64, 6 * 8 + 0), h64, (1, 2))
    except PermissionError:
        wrong_endpoint_blocked = True

    # Copy-on-write source update must not mutate the previously published view.
    mem2 = mem.write(cap81, (7, 1, 2), {"tensor": [99]})
    old_view = plane.read(receiver64, h64, (1, 2))
    new_subtree = store.subtree(mem2.root, (7,))

    public = json.dumps({"h64": h64.descriptor(), "h81": h81.descriptor()}, sort_keys=True)
    checks = {
        "publish_allocates_zero_blobs": blobs_after_publish == blobs_before_publish,
        "delegation_allocates_zero_blobs": blobs_after_delegate == blobs_after_publish,
        "cross_carrier_relative_read": value64 == {"tensor": [3, 6, 9]},
        "same_digest_can_be_delegated_elsewhere": h64.subtree_root == h81.subtree_root and value81 == {"tensor": [12, 15]},
        "endpoint_authority_enforced": wrong_endpoint_blocked,
        "published_snapshot_is_immutable": old_view == {"tensor": [3, 6, 9]} and new_subtree != h64.subtree_root,
        "source_snapshot_bound": h64.source_snapshot_root == old_root,
        "private_fibre_absent": "private_tag6" not in public and "state216" not in public,
    }
    return {
        "schema": "w33.zero-copy-merkle36.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "shared_subtree_root": h64.subtree_root,
        "checks": checks,
        "honesty_boundary": "Zero-copy means content-address reuse in one logical immutable store; no physical zero-copy/DMA/optical claim is made.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
