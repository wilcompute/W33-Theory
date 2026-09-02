#!/usr/bin/env python3
"""Deterministic record/replay for W33 asynchronous component scheduling.

Once futures and streams exist, guest results can depend on wakeup order even
when every individual component is deterministic.  This module records the
external scheduling decisions (send, receive, pump/wake) into a content-addressed
schedule trace and demonstrates exact replay on a fresh runtime.

A deliberately mutated wake order produces a different schedule root and a
different final liveness state.  The trace therefore becomes part of the
reproducibility/audit surface rather than an invisible property of the host event
loop.  This is a software scheduler theorem, not a claim about physical clock
jitter or distributed consensus.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

from w33_component_async36 import Async36Runtime, StreamU32
from w33_heterogeneous_36_ipc import FiberEndpoint, IPCCapability
from w33_heterogeneous_36_kernel import HeterogeneousKernel36, SharedObjectStore36
from w33_typed_universal_microvm import Carrier


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


def cap(carrier: Carrier) -> IPCCapability:
    return IPCCapability(carrier, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))


class Scenario:
    def __init__(self) -> None:
        self.store = SharedObjectStore36()
        self.kernel = HeterogeneousKernel36(queue_depth=1, object_store=self.store)
        self.runtime = Async36Runtime(self.kernel)
        self.sender = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 2)
        self.receiver = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 5)
        self.sender_cap = cap(self.sender.carrier)
        self.receiver_cap = cap(self.receiver.carrier)
        self.handle = self.store.put({"payload": "record-replay"}, self.receiver.carrier, self.receiver.base36)
        self.futures: dict[str, Any] = {}
        self.streams: dict[str, StreamU32] = {}

    @staticmethod
    def key(k: tuple[str, int, str, int]) -> str:
        return "|".join(map(str, k))

    def snapshot(self) -> dict[str, Any]:
        queues = {
            self.key(k): [m.public_descriptor() for m in q]
            for k, q in sorted(self.kernel.queues.items(), key=lambda x: self.key(x[0]))
            if q
        }
        return {
            "queues": queues,
            "next_send": {self.key(k): v for k, v in sorted(self.kernel.next_send.items(), key=lambda x: self.key(x[0]))},
            "next_recv": {self.key(k): v for k, v in sorted(self.kernel.next_recv.items(), key=lambda x: self.key(x[0]))},
            "delivered": sorted(self.kernel.delivered),
            "pending_nonces": [p.nonce for p in self.runtime.pending],
            "futures": {k: {"state": v.state, "value": v.value} for k, v in sorted(self.futures.items())},
            "streams": {k: list(v.items) for k, v in sorted(self.streams.items())},
        }

    def apply(self, op: str) -> dict[str, Any]:
        if op.startswith("send:"):
            label = op.split(":", 1)[1]
            nonce = f"schedule-{label}"
            fut = self.runtime.send_async(
                self.sender, self.sender_cap, self.receiver.carrier,
                self.receiver.base36, self.handle, nonce,
            )
            self.futures[label] = fut
            result: Any = {"future": label, "state": fut.state, "value": fut.value}
        elif op.startswith("recv:"):
            label = op.split(":", 1)[1]
            stream = StreamU32(capacity=1)
            pushed = self.runtime.recv_stream(self.receiver, self.receiver_cap, stream)
            self.streams[label] = stream
            result = {"stream": label, "pushed": pushed, "items": list(stream.items)}
        elif op == "pump":
            result = {"woken": self.runtime.pump()}
        else:
            raise ValueError(f"unknown schedule operation {op}")
        return {"op": op, "result": result, "state": self.snapshot()}


def run_schedule(schedule: list[str]) -> dict[str, Any]:
    scenario = Scenario()
    events = [scenario.apply(op) for op in schedule]
    payload = {
        "schedule": list(schedule),
        "events": events,
        "final": scenario.snapshot(),
    }
    return {
        **payload,
        "schedule_root": digest(payload),
    }


def verify() -> dict[str, Any]:
    canonical_schedule = ["send:first", "send:second", "recv:first", "pump", "recv:second"]
    replay_a = run_schedule(canonical_schedule)
    replay_b = run_schedule(canonical_schedule)

    wrong_order = ["send:first", "send:second", "pump", "recv:first", "recv:second"]
    mutated = run_schedule(wrong_order)

    public = json.dumps(replay_a, sort_keys=True)
    checks = {
        "fresh_runtime_replays_exact_schedule_root": replay_a["schedule_root"] == replay_b["schedule_root"],
        "fresh_runtime_replays_exact_final_state": replay_a["final"] == replay_b["final"],
        "canonical_schedule_delivers_two_messages": len(replay_a["final"]["delivered"]) == 2,
        "canonical_schedule_leaves_no_pending_send": replay_a["final"]["pending_nonces"] == [],
        "wake_order_is_committed": mutated["schedule_root"] != replay_a["schedule_root"],
        "wrong_wake_order_changes_liveness_state": len(mutated["final"]["delivered"]) == 1 and len(mutated["final"]["pending_nonces"]) == 1,
        "trace_is_carrier_neutral": "private_tag6" not in public and "state216" not in public,
    }
    return {
        "schema": "w33.async-schedule-replay.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "schedule_root": replay_a["schedule_root"],
        "mutated_schedule_root": mutated["schedule_root"],
        "checks": checks,
        "interpretation": "Async wake order is promoted to content-addressed execution evidence. Equal input plus equal recorded schedule replays exactly; a different wake order is a different certified execution.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
