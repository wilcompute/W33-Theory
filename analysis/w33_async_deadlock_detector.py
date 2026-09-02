#!/usr/bin/env python3
"""Deadlock detection and typed cancellation for W33 async components.

Future/stream backpressure makes waiting explicit, but explicit waiting can form a
cycle.  This module builds a wait-for graph from neutral component task IDs and
resource ownership, detects strongly connected deadlock components, and permits
cycle breaking only through an explicit cancellation capability.

The detector sees scheduling identities and neutral resource IDs only. It does
not inspect or serialize the private six-state fibre coordinate.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class CancelCapability:
    tasks: frozenset[str]
    rights: frozenset[str] = frozenset({"cancel"})

    def derive(self, tasks: Iterable[str], rights: Iterable[str]) -> "CancelCapability":
        tt, rr = frozenset(tasks), frozenset(rights)
        if "derive" not in self.rights:
            raise PermissionError("capability lacks derive right")
        if not tt or not tt <= self.tasks or not rr or not rr <= self.rights:
            raise PermissionError("derived cancellation authority must narrow")
        return CancelCapability(tt, rr)

    def authorizes(self, task: str) -> bool:
        return "cancel" in self.rights and task in self.tasks


class WaitForGraph:
    def __init__(self) -> None:
        self.owners: dict[str, str] = {}
        self.waits: dict[str, set[str]] = {}
        self.cancelled: set[str] = set()

    def own(self, task: str, resource: str) -> None:
        if resource in self.owners and self.owners[resource] != task:
            raise ValueError("resource already has an owner")
        self.owners[resource] = task

    def wait(self, task: str, resource: str) -> None:
        self.waits.setdefault(task, set()).add(resource)

    def release(self, task: str, resource: str) -> None:
        if self.owners.get(resource) == task:
            del self.owners[resource]

    def edges(self) -> dict[str, set[str]]:
        out: dict[str, set[str]] = {}
        for waiter, resources in self.waits.items():
            if waiter in self.cancelled:
                continue
            for resource in resources:
                owner = self.owners.get(resource)
                if owner is not None and owner != waiter and owner not in self.cancelled:
                    out.setdefault(waiter, set()).add(owner)
        for owner in self.owners.values():
            if owner not in self.cancelled:
                out.setdefault(owner, set())
        return out

    def strongly_connected(self) -> list[tuple[str, ...]]:
        graph = self.edges()
        index = 0
        indices: dict[str, int] = {}
        low: dict[str, int] = {}
        stack: list[str] = []
        onstack: set[str] = set()
        out: list[tuple[str, ...]] = []

        def visit(v: str) -> None:
            nonlocal index
            indices[v] = low[v] = index
            index += 1
            stack.append(v); onstack.add(v)
            for w in sorted(graph.get(v, ())):
                if w not in indices:
                    visit(w); low[v] = min(low[v], low[w])
                elif w in onstack:
                    low[v] = min(low[v], indices[w])
            if low[v] == indices[v]:
                comp: list[str] = []
                while True:
                    w = stack.pop(); onstack.remove(w); comp.append(w)
                    if w == v:
                        break
                out.append(tuple(sorted(comp)))

        for v in sorted(graph):
            if v not in indices:
                visit(v)
        return sorted(out)

    def deadlocks(self) -> list[tuple[str, ...]]:
        graph = self.edges()
        cycles: list[tuple[str, ...]] = []
        for comp in self.strongly_connected():
            if len(comp) > 1:
                cycles.append(comp)
            elif comp and comp[0] in graph.get(comp[0], set()):
                cycles.append(comp)
        return cycles

    def cancel(self, task: str, cap: CancelCapability) -> str:
        if not cap.authorizes(task):
            raise PermissionError("cancellation capability does not authorize task")
        self.cancelled.add(task)
        # Cancellation drops waits and releases every resource owned by victim.
        self.waits.pop(task, None)
        for resource, owner in list(self.owners.items()):
            if owner == task:
                del self.owners[resource]
        return digest({"cancelled": task, "remaining_edges": {k: sorted(v) for k, v in self.edges().items()}})

    def choose_victim(self, cycle: tuple[str, ...], priorities: dict[str, int] | None = None) -> str:
        if not cycle:
            raise ValueError("cycle required")
        priorities = priorities or {}
        # Higher numeric priority is more important, so cancel lowest priority;
        # lexical order makes the result deterministic.
        return min(cycle, key=lambda t: (priorities.get(t, 0), t))


def verify() -> dict[str, Any]:
    g = WaitForGraph()
    # A owns rA and waits on rB; B owns rB and waits on rC; C owns rC and waits on rA.
    for task, resource in [("component-A", "future-A"), ("component-B", "stream-B"), ("component-C", "mailbox-C")]:
        g.own(task, resource)
    g.wait("component-A", "stream-B")
    g.wait("component-B", "mailbox-C")
    g.wait("component-C", "future-A")
    cycles = g.deadlocks()
    cycle = cycles[0]
    victim = g.choose_victim(cycle, {"component-A": 10, "component-B": 1, "component-C": 5})

    unauthorized_blocked = False
    try:
        g.cancel(victim, CancelCapability(frozenset({"component-A"})))
    except PermissionError:
        unauthorized_blocked = True

    rootcap = CancelCapability(frozenset(cycle), frozenset({"cancel", "derive"}))
    narrow = rootcap.derive({victim}, {"cancel"})
    cancellation_record = g.cancel(victim, narrow)
    after = g.deadlocks()

    chain = WaitForGraph()
    chain.own("provider", "r")
    chain.wait("consumer", "r")

    serialized = json.dumps({"edges": {k: sorted(v) for k, v in g.edges().items()}}, sort_keys=True)
    checks = {
        "three_component_cycle_detected": len(cycles) == 1 and set(cycle) == {"component-A", "component-B", "component-C"},
        "deterministic_low_priority_victim": victim == "component-B",
        "unauthorized_cancellation_blocked": unauthorized_blocked,
        "narrow_capability_breaks_cycle": cancellation_record.startswith("sha256:") and after == [],
        "ordinary_wait_chain_not_deadlock": chain.deadlocks() == [],
        "detector_state_is_carrier_neutral": "private_tag6" not in serialized and "state216" not in serialized,
    }
    return {
        "schema": "w33.async-deadlock-detector.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "cycle": list(cycle),
        "victim": victim,
        "checks": checks,
        "interpretation": "Async futures/streams acquire an explicit neutral wait-for graph. Cyclic waits are detected and may be broken only by scoped cancellation authority.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
