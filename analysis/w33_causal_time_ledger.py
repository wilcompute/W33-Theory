#!/usr/bin/env python3
"""Causal/reversible time ledger for W33 virtual-machine state.

This makes the project's "time as memory/history" idea operational without
claiming a new law of physics.  Logical time is the depth of an append-only
causal DAG.  Reversible computation may return to an earlier *semantic state*
while causal time continues to increase because the history is retained.
Branches from one snapshot are incomparable.  A DISCARD_HISTORY event creates
an explicit non-reversible cut: later execution cannot traverse backward across
that edge using the runtime's retained undo authority.

The ledger itself still records hashes for auditability; therefore DISCARD is a
logical recoverability/authority cut, not evidence of physical data erasure or
thermodynamic dissipation.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class Event:
    event_id: str
    kind: str
    parents: tuple[str, ...]
    semantic_state: str
    logical_time: int
    reversible_to: str | None
    metadata_digest: str


class CausalTimeLedger:
    def __init__(self, initial_state: Any) -> None:
        state = digest(initial_state)
        genesis_body = {
            "kind": "GENESIS",
            "parents": [],
            "semantic_state": state,
            "logical_time": 0,
            "reversible_to": None,
            "metadata_digest": digest({}),
        }
        gid = digest(genesis_body)
        self.events: dict[str, Event] = {
            gid: Event(gid, "GENESIS", (), state, 0, None, digest({}))
        }
        self.genesis = gid

    def _event(self, kind: str, parents: tuple[str, ...], semantic_state: str,
               reversible_to: str | None, metadata: Any = None) -> str:
        if not parents or any(p not in self.events for p in parents):
            raise ValueError("event parents must exist")
        t = max(self.events[p].logical_time for p in parents) + 1
        md = digest({} if metadata is None else metadata)
        body = {
            "kind": kind,
            "parents": list(parents),
            "semantic_state": semantic_state,
            "logical_time": t,
            "reversible_to": reversible_to,
            "metadata_digest": md,
        }
        eid = digest(body)
        self.events[eid] = Event(eid, kind, parents, semantic_state, t, reversible_to, md)
        return eid

    def step(self, parent: str, new_state: Any, metadata: Any = None) -> str:
        if parent not in self.events:
            raise KeyError(parent)
        return self._event("REVERSIBLE_STEP", (parent,), digest(new_state), parent, metadata)

    def reverse(self, head: str) -> str:
        event = self.events[head]
        if event.reversible_to is None:
            raise PermissionError("history edge is not reversible")
        target = self.events[event.reversible_to]
        return self._event(
            "UNCOMPUTE",
            (head,),
            target.semantic_state,
            head,
            {"restores_event": target.event_id},
        )

    def discard_history(self, head: str, metadata: Any = None) -> str:
        event = self.events[head]
        return self._event("DISCARD_HISTORY", (head,), event.semantic_state, None, metadata)

    def branch(self, snapshot: str, branch_state: Any, label: str) -> str:
        return self._event("BRANCH_STEP", (snapshot,), digest(branch_state), snapshot, {"label": label})

    def merge_equal_state(self, left: str, right: str, metadata: Any = None) -> str:
        if left == right:
            raise ValueError("merge requires distinct heads")
        le, ri = self.events[left], self.events[right]
        if le.semantic_state != ri.semantic_state:
            raise ValueError("only equal semantic states may be merged without a reconciliation function")
        return self._event("JOIN_EQUAL_STATE", (left, right), le.semantic_state, None, metadata)

    def happens_before(self, ancestor: str, descendant: str) -> bool:
        if ancestor == descendant:
            return True
        seen: set[str] = set()
        stack = [descendant]
        while stack:
            cur = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            for parent in self.events[cur].parents:
                if parent == ancestor:
                    return True
                stack.append(parent)
        return False

    def descriptor(self, event_id: str) -> dict[str, Any]:
        return asdict(self.events[event_id])


def verify() -> dict[str, Any]:
    ledger = CausalTimeLedger({"counter": 0})
    g = ledger.genesis
    e1 = ledger.step(g, {"counter": 1}, {"op": "INC"})
    e2 = ledger.step(e1, {"counter": 2}, {"op": "INC"})
    u1 = ledger.reverse(e2)  # semantic state returns to e1
    u2 = ledger.reverse(u1)  # semantic state returns to e2 because UNCOMPUTE itself is reversible

    # A separate exact inverse of e1 demonstrates same semantic state at later time.
    back_to_g = ledger._event("EXACT_INVERSE", (e1,), ledger.events[g].semantic_state, e1, {"inverse": "INC"})

    left = ledger.branch(e1, {"counter": 7}, "left")
    right = ledger.branch(e1, {"counter": 7}, "right")
    joined = ledger.merge_equal_state(left, right, {"reason": "content-equal convergence"})

    cut = ledger.discard_history(e2, {"discarded_undo_records": 2})
    reverse_cut_blocked = False
    try:
        ledger.reverse(cut)
    except PermissionError:
        reverse_cut_blocked = True

    checks = {
        "reversible_step_has_back_edge": ledger.events[e2].reversible_to == e1,
        "uncompute_restores_prior_semantic_state": ledger.events[u1].semantic_state == ledger.events[e1].semantic_state,
        "same_semantic_state_can_have_later_time": ledger.events[back_to_g].semantic_state == ledger.events[g].semantic_state and ledger.events[back_to_g].logical_time > ledger.events[g].logical_time,
        "causal_time_monotone": ledger.events[e2].logical_time > ledger.events[e1].logical_time > ledger.events[g].logical_time,
        "branches_are_incomparable": not ledger.happens_before(left, right) and not ledger.happens_before(right, left),
        "common_snapshot_precedes_both_branches": ledger.happens_before(e1, left) and ledger.happens_before(e1, right),
        "equal_state_join_has_two_parents": set(ledger.events[joined].parents) == {left, right},
        "discard_history_is_irreversible_cut": ledger.events[cut].reversible_to is None and reverse_cut_blocked,
    }
    return {
        "schema": "w33.causal-time-ledger.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "event_count": len(ledger.events),
        "checks": checks,
        "interpretation": "In the VM, semantic state and causal time are distinct: reversible execution can revisit a state while retained history makes the causal clock advance. Explicit discard removes reverse authority across one edge.",
        "honesty_boundary": "This is an append-only software causal model. It does not prove that physical time emerges from computation, nor that logical discard physically erases bits.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
