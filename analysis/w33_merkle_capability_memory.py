#!/usr/bin/env python3
"""Persistent W33-addressed Merkle memory with monotone capabilities.

This closes a specific boundary in the typed universal microVM: abstract
counter-machine semantics may use unbounded natural numbers, but one finite
40-point W33 cell is not infinite memory.  The implementation model is instead
a scalable family of sparse 40-ary Merkle tries.  An address is a tuple of W33
point labels.  Depth d exposes 40**d possible leaf addresses, while only written
paths consume blobs.

The memory is persistent: writes return a new root, old roots remain readable,
and unchanged subtrees are shared by digest.  Capabilities bind a construction-
time carrier, an address prefix, and a monotone rights set.  Derived
capabilities may narrow rights and extend the prefix; they cannot widen rights,
escape the prefix, or change carrier type.

For equal-depth placements, address transport is the Cartesian product of W33:
each coordinate moves along a W33 route of at most two hops, so total virtual
routing cost is at most 2*d.

Honesty boundary: this is a software memory model and scalable address family,
not a claim that one finite device has literally infinite storage.  Any finite
execution uses finite depth and finitely many content-addressed blobs.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable, Sequence

from w33_typed_universal_microvm import Carrier, GEOMETRY


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def validate_address(address: Sequence[int]) -> tuple[int, ...]:
    row = tuple(int(x) for x in address)
    if any(x < 0 or x >= 40 for x in row):
        raise ValueError("W33 address digits must lie in 0..39")
    return row


class ContentStore:
    """Immutable descriptor store keyed by SHA-256 content identity."""

    def __init__(self) -> None:
        self.blobs: dict[str, dict[str, Any]] = {}
        self.empty = self.put({"kind": "node", "value": None, "children": []})

    def put(self, row: dict[str, Any]) -> str:
        key = digest(row)
        self.blobs.setdefault(key, row)
        return key

    def get(self, key: str) -> dict[str, Any]:
        if key not in self.blobs:
            raise KeyError(key)
        return self.blobs[key]

    def read(self, root: str, address: Sequence[int]) -> Any:
        addr = validate_address(address)
        key = root
        for slot in addr:
            row = self.get(key)
            children = dict(row["children"])
            key = children.get(slot)
            if key is None:
                return None
        return self.get(key)["value"]

    def subtree(self, root: str, prefix: Sequence[int]) -> str | None:
        addr = validate_address(prefix)
        key = root
        for slot in addr:
            children = dict(self.get(key)["children"])
            key = children.get(slot)
            if key is None:
                return None
        return key

    def write(self, root: str, address: Sequence[int], value: Any) -> str:
        addr = validate_address(address)

        def rec(key: str, pos: int) -> str:
            row = self.get(key)
            if row.get("kind") != "node":
                raise ValueError("corrupt Merkle node")
            children = dict(row["children"])
            if pos == len(addr):
                return self.put({
                    "kind": "node",
                    "value": value,
                    "children": sorted(children.items()),
                })
            slot = addr[pos]
            child = children.get(slot, self.empty)
            children[slot] = rec(child, pos + 1)
            return self.put({
                "kind": "node",
                "value": row["value"],
                "children": sorted(children.items()),
            })

        return rec(root, 0)


@dataclass(frozen=True)
class MemoryCapability:
    carrier: Carrier
    prefix: tuple[int, ...] = ()
    rights: frozenset[str] = frozenset({"read", "write", "derive"})

    def __post_init__(self) -> None:
        validate_address(self.prefix)
        allowed = {"read", "write", "derive"}
        if not self.rights or not set(self.rights) <= allowed:
            raise ValueError("unknown or empty capability rights")

    def authorizes(self, address: Sequence[int], right: str) -> bool:
        addr = validate_address(address)
        return (
            right in self.rights
            and len(addr) >= len(self.prefix)
            and addr[: len(self.prefix)] == self.prefix
        )

    def derive(self, suffix: Sequence[int], rights: Iterable[str]) -> "MemoryCapability":
        if "derive" not in self.rights:
            raise PermissionError("capability lacks derive right")
        narrowed = frozenset(rights)
        if not narrowed or not narrowed <= self.rights:
            raise PermissionError("derived rights must be a nonempty subset")
        return MemoryCapability(
            carrier=self.carrier,
            prefix=self.prefix + validate_address(suffix),
            rights=narrowed,
        )

    def descriptor(self) -> dict[str, Any]:
        return {
            "carrier": self.carrier.value,
            "prefix": list(self.prefix),
            "rights": sorted(self.rights),
        }


@dataclass(frozen=True)
class PersistentMemory:
    store: ContentStore
    root: str
    machine_type: Carrier

    @classmethod
    def empty(cls, store: ContentStore, machine_type: Carrier) -> "PersistentMemory":
        return cls(store=store, root=store.empty, machine_type=machine_type)

    def _check(self, cap: MemoryCapability, address: Sequence[int], right: str) -> tuple[int, ...]:
        addr = validate_address(address)
        if cap.carrier != self.machine_type:
            raise PermissionError("capability carrier does not match memory machine type")
        if not cap.authorizes(addr, right):
            raise PermissionError(f"capability does not authorize {right} at {addr}")
        return addr

    def read(self, cap: MemoryCapability, address: Sequence[int]) -> Any:
        addr = self._check(cap, address, "read")
        return self.store.read(self.root, addr)

    def write(self, cap: MemoryCapability, address: Sequence[int], value: Any) -> "PersistentMemory":
        addr = self._check(cap, address, "write")
        return PersistentMemory(
            store=self.store,
            root=self.store.write(self.root, addr, value),
            machine_type=self.machine_type,
        )

    def snapshot(self, cap: MemoryCapability) -> str:
        if cap.carrier != self.machine_type:
            raise PermissionError("wrong machine type")
        return digest({
            "mediaType": "application/vnd.w33.merkle-memory.v1+json",
            "root": self.root,
            "machineType": self.machine_type.value,
            "capability": cap.descriptor(),
        })


def capacity(depth: int) -> int:
    if depth < 0:
        raise ValueError("depth must be nonnegative")
    return 40 ** depth


def route_address(source: Sequence[int], target: Sequence[int]) -> list[dict[str, Any]]:
    """Route equal-depth W33 addresses coordinate by coordinate."""

    left = validate_address(source)
    right = validate_address(target)
    if len(left) != len(right):
        raise ValueError("routing requires equal-depth addresses")
    current = list(left)
    events: list[dict[str, Any]] = []
    for level, destination in enumerate(right):
        path = GEOMETRY.route(current[level], destination)
        for a, b in zip(path, path[1:]):
            before = tuple(current)
            current[level] = b
            events.append({
                "level": level,
                "from": list(before),
                "to": list(current),
                "point_hop": [a, b],
                "line_bus": GEOMETRY.line_by_pair[(a, b)],
            })
    if tuple(current) != right:
        raise AssertionError("route did not reach target")
    if len(events) > 2 * len(left):
        raise AssertionError("Cartesian W33 route exceeded 2d bound")
    return events


def verify() -> dict[str, Any]:
    store = ContentStore()
    rootcap81 = MemoryCapability(Carrier.CIRCUIT_ST81)
    mem0 = PersistentMemory.empty(store, Carrier.CIRCUIT_ST81)
    before_blobs = len(store.blobs)
    mem1 = mem0.write(rootcap81, (1, 2, 3), {"word": "alpha"})
    first_write_blobs = len(store.blobs) - before_blobs
    mem2 = mem1.write(rootcap81, (9, 8, 7), {"word": "beta"})
    beta_subtree_before = store.subtree(mem2.root, (9,))
    mem3 = mem2.write(rootcap81, (1, 2, 3), {"word": "ALPHA"})
    beta_subtree_after = store.subtree(mem3.root, (9,))

    before_repeat = len(store.blobs)
    mem3_repeat = mem3.write(rootcap81, (1, 2, 3), {"word": "ALPHA"})
    repeat_added = len(store.blobs) - before_repeat

    read_only = rootcap81.derive((1, 2), {"read"})
    blocked_write = False
    try:
        mem3.write(read_only, (1, 2, 4), "forbidden")
    except PermissionError:
        blocked_write = True

    escalation_blocked = False
    try:
        read_only.derive((3,), {"read", "write"})
    except PermissionError:
        escalation_blocked = True

    wrong_carrier_blocked = False
    cap64 = MemoryCapability(Carrier.PAIR_ST64)
    try:
        mem3.read(cap64, (1, 2, 3))
    except PermissionError:
        wrong_carrier_blocked = True

    sample_source = (0, 1, 2, 3, 4)
    sample_target = (39, 38, 37, 36, 35)
    events = route_address(sample_source, sample_target)

    checks = {
        "old_snapshot_unchanged": mem0.read(rootcap81, (1, 2, 3)) is None,
        "new_snapshot_reads_value": mem1.read(rootcap81, (1, 2, 3)) == {"word": "alpha"},
        "path_write_creates_depth_plus_one_nodes": first_write_blobs == 4,
        "unrelated_subtree_shared": beta_subtree_before == beta_subtree_after,
        "identical_write_is_deduplicated": mem3_repeat.root == mem3.root and repeat_added == 0,
        "read_only_write_blocked": blocked_write,
        "rights_escalation_blocked": escalation_blocked,
        "wrong_carrier_blocked": wrong_carrier_blocked,
        "capacity_depth5": capacity(5) == 102_400_000,
        "route_bound_2d": len(events) <= 2 * len(sample_source),
        "snapshot_content_addressed": mem3.snapshot(rootcap81).startswith("sha256:"),
    }
    return {
        "schema": "w33.merkle-capability-memory.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": (
            "Sparse 40-ary content-addressed memory has persistent copy-on-write semantics, "
            "monotone carrier-bound capabilities, and equal-depth address routing bounded by 2d W33 hops."
        ),
        "capacity": {str(d): capacity(d) for d in range(1, 8)},
        "sample": {
            "depth": len(sample_source),
            "route_hops": len(events),
            "route_bound": 2 * len(sample_source),
            "root_before": mem2.root,
            "root_after": mem3.root,
            "shared_beta_subtree": beta_subtree_before,
            "snapshot": mem3.snapshot(rootcap81),
            "blob_count": len(store.blobs),
        },
        "checks": checks,
        "honesty_boundary": (
            "The family scales without a fixed depth ceiling in the abstract model, but every concrete snapshot "
            "uses finite depth and finite blobs. This is not literal infinite storage in one W33 cell."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
