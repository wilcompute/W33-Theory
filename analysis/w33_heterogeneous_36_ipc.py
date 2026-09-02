#!/usr/bin/env python3
"""Typed heterogeneous IPC over the common 36-state carrier quotient.

The current carrier theorem says the two 216-state machines are inequivalent
and cannot be converted into one another by a substrate symmetry, but both are
principal six-fibrations over the same 36-state base.  That suggests a syscall
ABI, not a gauge transform.

A local carrier state is represented as
    state216 = 6 * base36 + private_tag6.
IPC exposes only ``base36``.  The private fibre tag is never translated across
carriers, and a received message does not manufacture a state in the sender's
fibre.  Therefore communication is possible while the construction-time fork
remains intact.

The neutral syscall surface is intentionally tiny:
    SEND36(destination_machine, destination_base, payload)
    RECV36()
    ACK36(message_id)

Capabilities restrict machine type, base addresses and rights.  Cross-carrier
messages are content-addressed and delivered through one of 36 neutral
mailboxes.  This is an executable typed message ABI; it does not claim an
isomorphism between the ST81 and ST64 modules.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Iterable

from w33_typed_universal_microvm import Carrier


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class FiberEndpoint:
    carrier: Carrier
    state216: int

    def __post_init__(self) -> None:
        if not 0 <= self.state216 < 216:
            raise ValueError("carrier state must lie in 0..215")

    @property
    def base36(self) -> int:
        return self.state216 // 6

    @property
    def private_tag6(self) -> int:
        return self.state216 % 6

    def public_descriptor(self) -> dict[str, Any]:
        return {"carrier": self.carrier.value, "base36": self.base36}


@dataclass(frozen=True)
class IPCCapability:
    carrier: Carrier
    bases: frozenset[int]
    rights: frozenset[str]

    def __post_init__(self) -> None:
        if not self.bases or any(not 0 <= b < 36 for b in self.bases):
            raise ValueError("IPC capability requires nonempty bases in 0..35")
        if not self.rights or not self.rights <= {"send", "recv", "ack", "derive"}:
            raise ValueError("unknown IPC rights")

    def derive(self, bases: Iterable[int], rights: Iterable[str]) -> "IPCCapability":
        if "derive" not in self.rights:
            raise PermissionError("capability lacks derive right")
        bb = frozenset(int(x) for x in bases)
        rr = frozenset(rights)
        if not bb or not bb <= self.bases:
            raise PermissionError("derived base set must narrow authority")
        if not rr or not rr <= self.rights:
            raise PermissionError("derived rights must narrow authority")
        return IPCCapability(self.carrier, bb, rr)

    def authorizes(self, endpoint: FiberEndpoint, right: str) -> bool:
        return endpoint.carrier == self.carrier and endpoint.base36 in self.bases and right in self.rights


@dataclass(frozen=True)
class Message36:
    message_id: str
    source_carrier: str
    source_base36: int
    destination_carrier: str
    destination_base36: int
    payload: Any
    payload_digest: str

    @classmethod
    def build(cls, source: FiberEndpoint, destination_carrier: Carrier, destination_base36: int, payload: Any) -> "Message36":
        if not 0 <= destination_base36 < 36:
            raise ValueError("destination base must lie in 0..35")
        pd = digest(payload)
        envelope = {
            "source_carrier": source.carrier.value,
            "source_base36": source.base36,
            "destination_carrier": destination_carrier.value,
            "destination_base36": destination_base36,
            "payload_digest": pd,
        }
        return cls(
            message_id=digest(envelope),
            source_carrier=source.carrier.value,
            source_base36=source.base36,
            destination_carrier=destination_carrier.value,
            destination_base36=destination_base36,
            payload=payload,
            payload_digest=pd,
        )


class MailboxFabric36:
    def __init__(self) -> None:
        self.mailboxes: list[list[Message36]] = [[] for _ in range(36)]
        self.acks: dict[str, str] = {}

    def send(self, source: FiberEndpoint, cap: IPCCapability, destination_carrier: Carrier, destination_base36: int, payload: Any) -> Message36:
        if not cap.authorizes(source, "send"):
            raise PermissionError("source capability does not authorize SEND36")
        msg = Message36.build(source, destination_carrier, destination_base36, payload)
        self.mailboxes[destination_base36].append(msg)
        return msg

    def recv(self, receiver: FiberEndpoint, cap: IPCCapability) -> Message36 | None:
        if not cap.authorizes(receiver, "recv"):
            raise PermissionError("receiver capability does not authorize RECV36")
        queue = self.mailboxes[receiver.base36]
        for i, msg in enumerate(queue):
            if msg.destination_carrier == receiver.carrier.value:
                return queue.pop(i)
        return None

    def ack(self, receiver: FiberEndpoint, cap: IPCCapability, message: Message36) -> str:
        if not cap.authorizes(receiver, "ack"):
            raise PermissionError("receiver capability does not authorize ACK36")
        if message.destination_carrier != receiver.carrier.value or message.destination_base36 != receiver.base36:
            raise PermissionError("receiver is not the destination of this message")
        ack = digest({"message_id": message.message_id, "receiver": receiver.public_descriptor()})
        self.acks[message.message_id] = ack
        return ack


def translate_carrier_state(_endpoint: FiberEndpoint, _destination: Carrier) -> FiberEndpoint:
    raise PermissionError("no carrier translation exists; IPC communicates over the common base without retyping")


def verify() -> dict[str, Any]:
    fabric = MailboxFabric36()
    circuit = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 2)
    pair = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 5)
    pair_other = FiberEndpoint(Carrier.PAIR_ST64, 6 * 9 + 1)

    cap81 = IPCCapability(Carrier.CIRCUIT_ST81, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))
    cap64 = IPCCapability(Carrier.PAIR_ST64, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))

    same_base_msg = fabric.send(circuit, cap81, Carrier.PAIR_ST64, pair.base36, {"syscall": "PING", "value": 81})
    received = fabric.recv(pair, cap64)
    ack = fabric.ack(pair, cap64, received) if received else None

    cross_base_msg = fabric.send(circuit, cap81, Carrier.PAIR_ST64, pair_other.base36, {"syscall": "MOVE", "value": 36})
    cross_received = fabric.recv(pair_other, cap64)

    read_only = cap64.derive({7}, {"recv"})
    send_escalation_blocked = False
    try:
        read_only.derive({7}, {"send", "recv"})
    except PermissionError:
        send_escalation_blocked = True

    wrong_base_blocked = False
    try:
        fabric.recv(pair_other, read_only)
    except PermissionError:
        wrong_base_blocked = True

    translation_blocked = False
    try:
        translate_carrier_state(circuit, Carrier.PAIR_ST64)
    except PermissionError:
        translation_blocked = True

    checks = {
        "both_carriers_share_36_base_range": circuit.base36 == pair.base36 == 7,
        "private_tags_remain_distinct": circuit.private_tag6 == 2 and pair.private_tag6 == 5,
        "cross_carrier_message_delivered": received is not None and received.payload["value"] == 81,
        "message_exposes_base_not_private_tag": received is not None and "private_tag6" not in received.__dict__,
        "destination_carrier_is_typed": received is not None and received.destination_carrier == Carrier.PAIR_ST64.value,
        "payload_is_content_addressed": received is not None and received.payload_digest == digest(received.payload),
        "ack_is_bound_to_receiver": ack is not None and fabric.acks.get(same_base_msg.message_id) == ack,
        "cross_base_delivery_works": cross_received is not None and cross_received.message_id == cross_base_msg.message_id,
        "rights_escalation_blocked": send_escalation_blocked,
        "base_escape_blocked": wrong_base_blocked,
        "carrier_translation_forbidden": translation_blocked,
        "carrier_identity_survives_ipc": circuit.carrier != pair.carrier,
    }

    return {
        "schema": "w33.heterogeneous-36-ipc.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "abi": {
            "base_states": 36,
            "fibre_states_per_machine_base": 6,
            "syscalls": ["SEND36", "RECV36", "ACK36"],
            "carrier_translation": "FORBIDDEN",
        },
        "sample": {
            "sender_public": circuit.public_descriptor(),
            "receiver_public": pair.public_descriptor(),
            "sender_private_tag": circuit.private_tag6,
            "receiver_private_tag": pair.private_tag6,
            "message_id": same_base_msg.message_id,
            "ack": ack,
        },
        "checks": checks,
        "interpretation": (
            "ST81 and ST64 behave as heterogeneous processors sharing a 36-address syscall plane. "
            "Communication uses neutral messages; it never constructs a gauge transform or an isomorphism between the two 216-state carriers."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
