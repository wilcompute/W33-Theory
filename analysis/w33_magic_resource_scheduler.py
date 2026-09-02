#!/usr/bin/env python3
"""Typed non-Clifford resource scheduler for the W33/Holonet packet machine.

The runtime previously had a scalar magic budget.  This module turns it into a
scarce typed resource with reservations, packet-slot allocation, audit status,
and an explicit fault-tolerance adapter gate.

Two layers are kept separate:
  * HESSE_T_RAW: repository-local exact qutrit T teleportation/ABI witness.
    It is usable for logical simulation/refinement but is NOT fault tolerant.
  * external qutrit MSD/code candidates: may be registered as prior-art
    adapters, but the scheduler refuses to label their output fault tolerant
    until a W33 encoding map AND threshold/noise certificate are supplied.

This prevents a scheduler from converting "magic-capable" into an unjustified
physical-universality claim.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any

import w33_qutrit_t_teleportation_port as tport


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value)).hexdigest()


@dataclass(frozen=True)
class MagicResourceType:
    name: str
    dimension: int
    logical_gate: str
    fault_tolerant: bool
    evidence_class: str


HESSE_T_RAW = MagicResourceType(
    "HESSE_T_RAW", 3, "qutrit-T", False, "EXACT_STATEVECTOR_AND_PACKET_ABI",
)


@dataclass(frozen=True)
class FTAdapter:
    name: str
    code_parameters: str
    encoding_map_verified: bool
    threshold_certificate_verified: bool
    source_class: str = "EXTERNAL_PRIOR_ART_CANDIDATE"

    @property
    def enabled(self) -> bool:
        return self.encoding_map_verified and self.threshold_certificate_verified


@dataclass(frozen=True)
class MagicToken:
    token_id: str
    resource_type: str
    factory_batch: str
    audit_digest: str


@dataclass(frozen=True)
class Reservation:
    reservation_id: str
    token_id: str
    packet_index: int
    microframe_tick: int
    logical_gate: str
    assurance: str


class MagicFactoryScheduler:
    def __init__(self) -> None:
        self.inventory: dict[str, MagicToken] = {}
        self.reserved: set[str] = set()
        self.reservations: list[Reservation] = []
        self.adapters: dict[str, FTAdapter] = {}

    def register_adapter(self, adapter: FTAdapter) -> None:
        self.adapters[adapter.name] = adapter

    def mint_raw(self, count: int, factory_batch: str, audit_digest: str) -> list[MagicToken]:
        if count < 0 or not audit_digest.startswith("sha256:"):
            raise ValueError("invalid magic factory mint")
        out: list[MagicToken] = []
        for i in range(count):
            tid = digest({"resource": HESSE_T_RAW.name, "batch": factory_batch, "index": i, "audit": audit_digest})
            tok = MagicToken(tid, HESSE_T_RAW.name, factory_batch, audit_digest)
            self.inventory[tid] = tok
            out.append(tok)
        return out

    def _free_raw(self) -> MagicToken:
        free = sorted(k for k in self.inventory if k not in self.reserved)
        if not free:
            raise RuntimeError("no unreserved HESSE_T_RAW token available")
        return self.inventory[free[0]]

    def reserve_t(self, packet_index: int, assurance: str = "EXACT_LOGICAL") -> Reservation:
        if packet_index < 0:
            raise ValueError("packet index must be nonnegative")
        if assurance not in {"EXACT_LOGICAL", "FAULT_TOLERANT"}:
            raise ValueError("unknown assurance class")
        if assurance == "FAULT_TOLERANT":
            enabled = [a for a in self.adapters.values() if a.enabled]
            if not enabled:
                raise PermissionError("fault-tolerant T reservation refused: no verified W33 FT adapter")
        token = self._free_raw()
        self.reserved.add(token.token_id)
        # Architecture policy: one typed injection point in the first epilogue
        # word of each 72-tick microframe.  This is a scheduler slot, not a
        # measured hardware latency.
        tick = packet_index * 72 + 48
        body = {
            "token": token.token_id,
            "packet_index": packet_index,
            "microframe_tick": tick,
            "logical_gate": "qutrit-T",
            "assurance": assurance,
        }
        row = Reservation(digest(body), token.token_id, packet_index, tick, "qutrit-T", assurance)
        self.reservations.append(row)
        return row

    def consume(self, reservation_id: str) -> MagicToken:
        row = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if row is None:
            raise KeyError("unknown reservation")
        token = self.inventory.pop(row.token_id, None)
        if token is None:
            raise PermissionError("magic token already consumed")
        self.reserved.discard(row.token_id)
        return token

    def cancel(self, reservation_id: str) -> None:
        row = next((r for r in self.reservations if r.reservation_id == reservation_id), None)
        if row is None:
            raise KeyError("unknown reservation")
        self.reserved.discard(row.token_id)
        self.reservations = [r for r in self.reservations if r.reservation_id != reservation_id]

    def snapshot(self) -> dict[str, Any]:
        return {
            "inventory": sorted(self.inventory),
            "reserved": sorted(self.reserved),
            "reservations": [asdict(r) for r in self.reservations],
            "adapters": {k: asdict(v) | {"enabled": v.enabled} for k, v in sorted(self.adapters.items())},
        }


def verify() -> dict[str, Any]:
    teleport = tport.verify()
    audit_digest = digest({"tport_status": teleport.get("status"), "checks": teleport.get("checks", {})})
    sched = MagicFactoryScheduler()
    tokens = sched.mint_raw(2, "batch-demo", audit_digest)

    r0 = sched.reserve_t(0, "EXACT_LOGICAL")
    r1 = sched.reserve_t(1, "EXACT_LOGICAL")
    overbook_blocked = False
    try:
        sched.reserve_t(2, "EXACT_LOGICAL")
    except RuntimeError:
        overbook_blocked = True

    # Prior-art adapter metadata alone is intentionally insufficient.
    candidate = FTAdapter(
        name="QUTRIT_TRIORTHOGONAL_20_7_2",
        code_parameters="[[20,7,2]]_3",
        encoding_map_verified=False,
        threshold_certificate_verified=False,
    )
    sched.register_adapter(candidate)
    ft_refused = False
    try:
        # Cancel one logical reservation so inventory is not the reason for refusal.
        sched.cancel(r1.reservation_id)
        sched.reserve_t(2, "FAULT_TOLERANT")
    except PermissionError:
        ft_refused = True

    consumed = sched.consume(r0.reservation_id)
    consume_twice_blocked = False
    try:
        sched.consume(r0.reservation_id)
    except PermissionError:
        consume_twice_blocked = True

    snap = sched.snapshot()
    checks = {
        "exact_t_port_certificate_passes": teleport.get("status") == "PASS",
        "raw_tokens_content_addressed": len(tokens) == 2 and all(t.token_id.startswith("sha256:") for t in tokens),
        "packet_slots_are_72_tick_aligned": r0.microframe_tick == 48 and r1.microframe_tick == 120,
        "inventory_cannot_be_overbooked": overbook_blocked,
        "ft_candidate_is_fail_closed_without_w33_adapter": ft_refused and not candidate.enabled,
        "reservation_consumes_exact_token": consumed.token_id == r0.token_id,
        "token_double_spend_blocked": consume_twice_blocked,
        "scheduler_keeps_assurance_explicit": all(r["assurance"] in {"EXACT_LOGICAL", "FAULT_TOLERANT"} for r in snap["reservations"]),
    }
    return {
        "schema": "w33.magic-resource-scheduler.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "candidate_adapter": asdict(candidate) | {"enabled": candidate.enabled},
        "interpretation": "Non-Clifford resources are reserved/consumed like typed accelerator tokens. Exact logical T and fault-tolerant T are distinct assurance classes; the latter remains refused until W33-specific encoding and threshold evidence exists.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
