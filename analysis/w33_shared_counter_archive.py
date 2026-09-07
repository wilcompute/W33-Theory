#!/usr/bin/env python3
"""Collector-visible shared counter snapshots with exact payload admission.

Prior art: w33_zero_copy_merkle36.py, w33_lossless_counter_suspension.py,
w33_temporal_merkle_gc.py; Venti (Quinlan and Dorward, FAST 2002).
Each binary node becomes one generic collector-visible node. Snapshot metadata
keeps both fibre tags and guest control state private to that snapshot root.
Admission prices the weighted union of ALL strong-root closures, not a guessed
deduplication percentage. Costs are canonical JSON blob payload bytes only:
registry records, hash-index keys, Python objects, I/O and CPU are excluded.
This in-memory reference implementation requires serialized owner operations;
it supplies no concurrent transaction, authority, lease or durability service.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from w33_authenticated_counter_machine import Bit, BitStore, State, ZERO
from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
from w33_lossless_counter_suspension import SuspensionHandle, _address, _state, reachable
from w33_merkle_capability_memory import ContentStore, canonical_json, digest
from w33_temporal_merkle_gc import RootRegistry, TemporalMerkleGC

SCHEMA = "w33.shared-counter-snapshot.v1"
BIT_SCHEMA = "w33.shared-counter-bit.v1"
KIND = "SHARED_COUNTER_SNAPSHOT"


@dataclass(frozen=True)
class PreparedSnapshot:
    root: str
    # Serialized immutable descriptors prevent a caller mutating a quoted row.
    blobs: tuple[tuple[str, str], ...]


def prepare(state: State, address: FibreProductAddress, memory: BitStore, *,
            max_nodes: int = 100_000) -> PreparedSnapshot:
    state, address = _state(asdict(state)), _address(asdict(address))
    nodes = reachable(memory, state.roots, max_nodes)
    encoded = ContentStore()
    mapping = {ZERO: encoded.empty}
    for start in state.roots:
        path = []
        cursor = start
        while cursor not in mapping:
            path.append(cursor)
            cursor = nodes[cursor].tail
        for key in reversed(path):
            node = nodes[key]
            mapping[key] = encoded.put({
                "kind": "node",
                "value": {"schema": BIT_SCHEMA, "counter_root": key, "bit": node.bit},
                "children": [[0, mapping[node.tail]]],
            })
    root = encoded.put({
        "kind": "node",
        "value": {"schema": SCHEMA, "state": {**asdict(state), "roots": list(state.roots)},
                  "fibre": asdict(address)},
        "children": [[i, mapping[key]] for i, key in enumerate(state.roots)],
    })
    return PreparedSnapshot(root, tuple((key, canonical_json(row).decode())
                                        for key, row in sorted(encoded.blobs.items())))


def _read(store: ContentStore, key: str) -> dict:
    row = store.get(key)
    if type(row) is not dict or digest(row) != key:
        raise ValueError("corrupt archived content")
    return row


def _restore(root: str, store: ContentStore, max_nodes: int
             ) -> tuple[State, FibreProductAddress, BitStore, set[str]]:
    if type(max_nodes) is not int or max_nodes < 0:
        raise ValueError("invalid node budget")
    row = _read(store, root)
    if set(row) != {"kind", "value", "children"} or row["kind"] != "node":
        raise ValueError("invalid snapshot node")
    value = row["value"]
    if type(value) is not dict or set(value) != {"schema", "state", "fibre"} or value["schema"] != SCHEMA:
        raise ValueError("invalid snapshot metadata")
    state, address = _state(value["state"]), _address(value["fibre"])
    children = row["children"]
    if (type(children) is not list or len(children) != 2
            or any(type(p) is not list or len(p) != 2 or type(p[0]) is not int
                   or p[0] != i or type(p[1]) is not str for i, p in enumerate(children))):
        raise ValueError("invalid counter root edges")
    memory = BitStore()
    seen = {root, store.empty}
    decoded = {store.empty: ZERO}
    if _read(store, store.empty) != {"kind": "node", "value": None, "children": []}:
        raise ValueError("invalid empty archive node")
    for i, start in children:
        cursor, path, active = start, [], set()
        while cursor not in decoded:
            if cursor in active:
                raise ValueError("cyclic archived counter")
            if len(memory.nodes) + len(path) >= max_nodes:
                raise TimeoutError("restore node budget exhausted")
            active.add(cursor)
            node = _read(store, cursor)
            if set(node) != {"kind", "value", "children"} or node["kind"] != "node":
                raise ValueError("invalid archived bit node")
            val, edges = node["value"], node["children"]
            if (type(val) is not dict or set(val) != {"schema", "counter_root", "bit"}
                    or val["schema"] != BIT_SCHEMA or type(edges) is not list
                    or len(edges) != 1 or type(edges[0]) is not list or len(edges[0]) != 2
                    or type(edges[0][0]) is not int or edges[0][0] != 0
                    or type(edges[0][1]) is not str):
                raise ValueError("invalid archived bit descriptor")
            path.append((cursor, val))
            cursor = edges[0][1]
        for key, val in reversed(path):
            bit = Bit(val["bit"], decoded[cursor])
            if bit.root != val["counter_root"]:
                raise ValueError("counter identity does not match archived tail")
            memory.put(bit)
            decoded[key] = bit.root
            seen.add(key)
            cursor = key
        if decoded[start] != state.roots[i]:
            raise ValueError("snapshot counter root mismatch")
    return state, address, memory, seen


def _overlay(proposal: PreparedSnapshot, archive: ContentStore, max_nodes: int) -> ContentStore:
    view = ContentStore()
    view.blobs = dict(archive.blobs)
    keys = set()
    for key, wire in proposal.blobs:
        row = json.loads(wire)
        if key in keys or digest(row) != key:
            raise ValueError("duplicate or corrupt proposed blob")
        if key in view.blobs and view.blobs[key] != row:
            raise ValueError("content collision or corrupt existing blob")
        keys.add(key)
        view.blobs[key] = row
    _, _, _, closure = _restore(proposal.root, view, max_nodes)
    if keys != closure:
        raise ValueError("proposal must contain exactly its reachable closure")
    return view


def _retained(store: ContentStore, registry: RootRegistry) -> set[str]:
    marked = set(TemporalMerkleGC(store, registry).plan()["marked"])
    for key in marked:
        _read(store, key)
    return marked


def _bytes(store: ContentStore, keys: set[str]) -> int:
    return sum(len(canonical_json(store.blobs[key])) for key in keys)


def quote(proposal: PreparedSnapshot, archive: ContentStore, registry: RootRegistry, *,
          max_nodes: int = 100_000) -> dict:
    """Exact point-in-time retained payload quote; publishing always rechecks."""
    view = _overlay(proposal, archive, max_nodes)
    current = _retained(archive, registry)
    future = RootRegistry()
    future.references = dict(registry.references)
    future.pin(KIND, "quote-only", proposal.root, "STRONG")
    union = _retained(view, future)
    return {
        "current_payload_bytes": _bytes(archive, current),
        "prospective_payload_bytes": _bytes(view, union),
        "marginal_payload_bytes": _bytes(view, union - current),
        "prospective_blobs": len(union),
        "registry_root": registry.registry_root,
    }


def publish(owner: str, proposal: PreparedSnapshot, archive: ContentStore,
            registry: RootRegistry, *, max_payload_bytes: int,
            max_nodes: int = 100_000) -> SuspensionHandle:
    """Recheck, budget, then install and sweep; validation rejection is atomic.

    Crash recovery and allocation failure during installation are outside this
    owner-serialized in-memory model.
    """
    if type(owner) is not str or not owner:
        raise ValueError("explicit owner required")
    if type(max_payload_bytes) is not int or max_payload_bytes < 0:
        raise ValueError("invalid payload budget")
    view = _overlay(proposal, archive, max_nodes)
    future = RootRegistry()
    future.references = dict(registry.references)
    ref = future.pin(KIND, owner, proposal.root, "STRONG")
    marked = _retained(view, future)
    if _bytes(view, marked) > max_payload_bytes:
        raise MemoryError("retained snapshot union exceeds payload budget")
    retained = {key: view.blobs[key] for key in marked}
    # The owner serializes operations; validation precedes mutation.
    archive.blobs.clear()
    archive.blobs.update(retained)
    registry.references[ref.reference_id] = ref
    return SuspensionHandle(ref.reference_id, proposal.root)


def resume(handle: SuspensionHandle, expected_root: str, archive: ContentStore,
           registry: RootRegistry, *, max_nodes: int = 100_000
           ) -> tuple[State, FibreProductAddress, BitStore]:
    if handle.root != expected_root:
        raise ValueError("wrong trusted snapshot root")
    ref = registry.references.get(handle.reference_id)
    if ref is None or (ref.root, ref.kind, ref.strength) != (expected_root, KIND, "STRONG"):
        raise PermissionError("a live strong snapshot reference is required")
    state, address, memory, _ = _restore(expected_root, archive, max_nodes)
    return state, address, memory


def verify() -> dict:
    """Measure explicit workloads; no timing or machine-RAM estimate is used."""
    from w33_authenticated_counter_machine import genesis
    from w33_lossless_counter_suspension import suspend as monolithic_suspend
    from w33_typed_universal_microvm import add_r1_into_r0_program

    program, memory = add_r1_into_r0_program(), BitStore()
    fibre = FibreProductAddress(0, 0, 0)
    archive, registry = ContentStore(), RootRegistry()
    old_archive, old_registry = ContentStore(), RootRegistry()
    all_restored = True
    first_shared = first_monolithic = None
    for n in range(256):
        state = genesis(program, memory, (n, 0), session="archive-economics")
        proposal = prepare(state, fibre, memory)
        handle = publish(str(n), proposal, archive, registry, max_payload_bytes=10**9)
        monolithic_suspend(str(n), state, fibre, memory, old_archive, old_registry)
        restored, _, store = resume(handle, handle.root, archive, registry)
        all_restored &= restored == state and [store.decode(r) for r in restored.roots] == [n, 0]
        if n == 0:
            first_shared = _bytes(archive, set(archive.blobs))
            first_monolithic = _bytes(old_archive, set(old_archive.blobs))
    shared_bytes = _bytes(archive, set(archive.blobs))
    old_bytes = _bytes(old_archive, set(old_archive.blobs))

    # Same bit length, different overlap with a retained snapshot.
    pool, pins = ContentStore(), RootRegistry()
    def candidate(n):
        return prepare(genesis(program, memory, (n, 0), session="cost"), fibre, memory)
    publish("base", candidate(255), pool, pins, max_payload_bytes=10**9)
    costs = {str(n): quote(candidate(n), pool, pins)["marginal_payload_bytes"] for n in (254, 128)}

    # The retained-byte function is weighted set coverage. Check diminishing
    # marginal costs for all A subset B and x outside B on six actual snapshots.
    proposals = [candidate(n) for n in (0, 1, 2, 3, 7, 8)]
    sets = [{key for key, _ in p.blobs} for p in proposals]
    weights = {key: len(wire.encode()) for p in proposals for key, wire in p.blobs}
    empty = pool.empty
    closures = []
    for mask in range(64):
        union = {empty}
        for i, keys in enumerate(sets):
            if mask & (1 << i):
                union |= keys
        closures.append(union)
    f = [sum(weights[key] for key in union) for union in closures]
    comparisons = 0
    diminishing = True
    for a in range(64):
        for b in range(64):
            if a & ~b:
                continue
            for x in range(6):
                if not b & (1 << x):
                    comparisons += 1
                    diminishing &= f[a | (1 << x)] - f[a] >= f[b | (1 << x)] - f[b]
    checks = {
        "all_256_snapshots_restore": all_restored,
        "exactly_255_shared_binary_nodes": len(archive.blobs) == 256 + 255 + 1,
        "shared_population_uses_fewer_payload_bytes": shared_bytes < old_bytes,
        "same_width_candidates_have_different_marginal_cost": costs["254"] < costs["128"],
        "coverage_marginals_diminish_on_all_six_snapshot_subsets": diminishing,
    }
    return {
        "schema": "w33.shared-counter-archive-economics.v1",
        "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
        "population": {"snapshots": 256, "shared_binary_nodes": 255,
                       "shared_blobs": len(archive.blobs), "shared_payload_bytes": shared_bytes,
                       "monolithic_payload_bytes": old_bytes},
        "zero_counter_single_snapshot": {"shared_payload_bytes": first_shared,
                                         "monolithic_payload_bytes": first_monolithic},
        "marginal_bytes_with_255_retained": costs,
        "diminishing_return_comparisons": comparisons,
        "scope": "Canonical JSON blob payloads only; excludes registry/index/RAM/CPU/I/O. Weighted coverage is standard set algebra, not a new mathematical theorem. No scheduling optimality claim.",
    }


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
