#!/usr/bin/env python3
"""Exact, bounded set-union admission for recoverable counter snapshots.

This is retention scheduling, not CPU scheduling or a reversible pebble schedule.
Prior work: w33_shared_counter_archive.py, w33_adaptive_reversible_scheduler.py;
Goldschmidt, Nehme and Yu, Note: On the set-union knapsack problem (1994).
Maximize caller-supplied nonnegative integer utility subject to canonical blob
payload bytes. All existing STRONG roots are mandatory. At most 16 pending
requests are accepted; there is no heuristic fallback masquerading as optimal.
Owner operations must be serialized. Plans are advisory, not authority tokens.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import json

from w33_merkle_capability_memory import ContentStore, canonical_json, digest
from w33_shared_counter_archive import (
    PreparedSnapshot, _overlay, _retained, publish,
)
from w33_temporal_merkle_gc import RootRegistry

MAX_CANDIDATES = 16


@dataclass(frozen=True)
class Request:
    request_id: str
    utility: int
    snapshot: PreparedSnapshot


@dataclass(frozen=True)
class AdmissionPlan:
    problem_root: str
    registry_root: str
    selected: tuple[str, ...]
    utility: int
    payload_bytes: int
    feasible: bool
    subsets_examined: int
    feasible_subsets: int

    def descriptor(self) -> dict:
        return {**asdict(self), "selected": list(self.selected)}


def _problem(requests, archive, registry, max_payload_bytes, max_nodes):
    if type(max_payload_bytes) is not int or max_payload_bytes < 0:
        raise ValueError("invalid payload budget")
    if type(max_nodes) is not int or max_nodes < 0:
        raise ValueError("invalid node budget")
    if not isinstance(requests, (tuple, list)) or len(requests) > MAX_CANDIDATES:
        raise ValueError("exact admission accepts at most 16 requests in a list or tuple")
    ids = set()
    for r in requests:
        if (type(r) is not Request or type(r.request_id) is not str or not r.request_id
                or type(r.utility) is not int or r.utility < 0):
            raise ValueError("request needs a nonempty id and nonnegative integer utility")
        if r.request_id in ids:
            raise ValueError("duplicate request id")
        ids.add(r.request_id)
    requests = tuple(sorted(requests, key=lambda r: r.request_id))
    base = _retained(archive, registry)
    view = ContentStore()
    view.blobs = dict(archive.blobs)
    closures = []
    for r in requests:
        # Validate every request, even one that the eventual optimum excludes.
        view = _overlay(r.snapshot, view, max_nodes)
        closures.append(frozenset(key for key, _ in r.snapshot.blobs))
    weights = {key: len(canonical_json(view.blobs[key]))
               for key in base.union(*closures)}
    problem_root = digest({
        "schema": "w33.snapshot-admission-problem.v1",
        "registry_root": registry.registry_root,
        "requests": [(r.request_id, r.utility, r.snapshot.root) for r in requests],
        "max_payload_bytes": max_payload_bytes,
    })
    return requests, base, closures, weights, problem_root


def plan(requests, archive: ContentStore, registry: RootRegistry, *,
         max_payload_bytes: int, max_nodes: int = 100_000) -> AdmissionPlan:
    """Exhaust all subsets; ties prefer fewer bytes, then lexicographic ids.

    Existing retention over budget returns infeasible, without evicting anything.
    Optimality is only for the supplied request set, utility and payload metric.
    """
    rows, base, closures, weights, root = _problem(
        requests, archive, registry, max_payload_bytes, max_nodes)
    best = None
    feasible_subsets = 0
    for mask in range(1 << len(rows)):
        selected = tuple(i for i in range(len(rows)) if mask & (1 << i))
        union = base.union(*(closures[i] for i in selected))
        cost = sum(weights[key] for key in union)
        if cost > max_payload_bytes:
            continue
        feasible_subsets += 1
        ids = tuple(rows[i].request_id for i in selected)
        value = sum(rows[i].utility for i in selected)
        objective = (-value, cost, ids)
        if best is None or objective < best[0]:
            best = (objective, ids, value, cost)
    if best is None:
        ids, value, cost = (), 0, sum(weights[key] for key in base)
    else:
        _, ids, value, cost = best
    return AdmissionPlan(root, registry.registry_root, ids, value, cost,
                         best is not None, 1 << len(rows), feasible_subsets)


def admit(expected: AdmissionPlan, requests, archive: ContentStore,
          registry: RootRegistry, *, max_payload_bytes: int,
          max_nodes: int = 100_000) -> dict:
    """Recompute the exact plan, then publish into private staging stores.

    Rejection before installation leaves public archive and registry unchanged.
    Requires serialized owner operations; crash/allocation failure during final
    installation is outside this in-memory model. The caller supplies the budget
    again: changing a plan cannot raise the authoritative budget.
    """
    actual = plan(requests, archive, registry,
                  max_payload_bytes=max_payload_bytes, max_nodes=max_nodes)
    if actual != expected:
        raise ValueError("stale or altered admission plan")
    if not actual.feasible:
        raise MemoryError("existing strong retention exceeds budget")
    staged_archive, staged_registry = ContentStore(), RootRegistry()
    staged_archive.blobs = dict(archive.blobs)
    staged_registry.references = dict(registry.references)
    by_id = {r.request_id: r for r in requests}
    handles = {}
    for key in actual.selected:
        handles[key] = publish(key, by_id[key].snapshot, staged_archive,
                               staged_registry, max_payload_bytes=max_payload_bytes,
                               max_nodes=max_nodes)
    # Empty selection is a no-op, not a request to collect or release anything.
    if handles:
        archive.blobs.clear()
        archive.blobs.update(staged_archive.blobs)
        registry.references.clear()
        registry.references.update(staged_registry.references)
    return handles


def witness_requests():
    from w33_authenticated_counter_machine import BitStore, genesis
    from w33_finite_control_unbounded_guest_hypervisor import FibreProductAddress
    from w33_shared_counter_archive import prepare
    from w33_typed_universal_microvm import add_r1_into_r0_program

    memory, program = BitStore(), add_r1_into_r0_program()
    return tuple(Request(str(n), 1, prepare(
        genesis(program, memory, (n, 0), session="set-union-demo"),
        FibreProductAddress(0, 0, 0), memory)) for n in (128, 254, 255))


def verify() -> dict:
    from w33_shared_counter_archive import quote, resume
    from w33_authenticated_counter_machine import prove_step, verify_step
    from w33_typed_universal_microvm import add_r1_into_r0_program

    requests = witness_requests()
    archive, registry = ContentStore(), RootRegistry()
    costs = {}
    for mask in range(1, 8):
        group = [r for i, r in enumerate(requests) if mask & (1 << i)]
        blobs = {k: v for r in group for k, v in r.snapshot.blobs}
        costs[",".join(r.request_id for r in group)] = sum(len(v.encode()) for v in blobs.values())
    budget = costs["254,255"]
    exact = plan(requests, archive, registry, max_payload_bytes=budget)
    # Explicit comparator: repeatedly take smallest current marginal cost,
    # tie by id, among requests that fit; all three utilities equal one.
    greedy_archive, greedy_registry = ContentStore(), RootRegistry()
    remaining, greedy = list(requests), []
    while remaining:
        fits = [(quote(r.snapshot, greedy_archive, greedy_registry), r) for r in remaining]
        fits = [(q, r) for q, r in fits if q["prospective_payload_bytes"] <= budget]
        if not fits:
            break
        _, r = min(fits, key=lambda qr: (qr[0]["marginal_payload_bytes"], qr[1].request_id))
        publish(r.request_id, r.snapshot, greedy_archive, greedy_registry, max_payload_bytes=budget)
        greedy.append(r.request_id)
        remaining.remove(r)
    handles = admit(exact, requests, archive, registry, max_payload_bytes=budget)
    restored = {}
    program = add_r1_into_r0_program()
    for key, handle in handles.items():
        state, _, memory = resume(handle, handle.root, archive, registry)
        # Each archived input has counter1=0: execute its branch and halt after
        # recovery using the existing independent arithmetic receipt verifier.
        while not state.halted:
            state, _ = verify_step(program, state, prove_step(program, state, memory))
        restored[key] = [memory.decode(r) for r in state.roots]
    checks = {
        "equal_standalone_payloads": len({costs[str(n)] for n in (128, 254, 255)}) == 1,
        "joint_plan_selects_shared_pair": exact.selected == ("254", "255"),
        "all_eight_subsets_examined": exact.subsets_examined == 8,
        "greedy_admits_one_exact_admits_two": greedy == ["128"] and exact.utility == 2,
        "both_selected_guests_resume_and_halt": restored == {"254": [254, 0], "255": [255, 0]},
        "installed_payload_matches_plan": sum(len(canonical_json(v)) for v in archive.blobs.values()) == exact.payload_bytes,
    }
    return {"schema": "w33.snapshot-admission-witness.v1",
            "status": "PASS" if all(checks.values()) else "FAIL", "checks": checks,
            "subset_payload_bytes": costs, "budget": budget,
            "exact_plan": exact.descriptor(), "greedy_selected": greedy,
            "resumed_outputs": restored,
            "scope": "Exact at most 16 pending requests; caller utility and canonical payloads only. No CPU scheduling, peak RAM, eviction, authority or durable transaction claim."}


if __name__ == "__main__":
    result = verify()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(result["status"] != "PASS")
