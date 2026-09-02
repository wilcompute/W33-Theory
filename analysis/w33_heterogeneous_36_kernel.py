#!/usr/bin/env python3
"""Hardened ST81/ST64 heterogeneous kernel over the common 36-state ABI.

This extends ``w33_heterogeneous_36_ipc.py`` from a minimal mailbox into a
small fail-closed kernel with:

* per-channel monotonically increasing sequence numbers,
* nonce/message replay rejection,
* bounded queues and explicit backpressure,
* immutable content-addressed shared-object handles,
* one-time receiver-bound acknowledgements,
* an executable noninterference check over all six private fibre tags,
* typed WebAssembly host imports for SEND36/RECV36/ACK36.

The kernel never translates the private six-state fibre coordinate.  Its public
state is restricted to carrier identity, the common base36 address, content
identity, sequence/nonce data and capabilities.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

from w33_heterogeneous_36_ipc import FiberEndpoint, IPCCapability
from w33_typed_universal_microvm import Carrier
import w33_wasm3_capability_runtime as wasm


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def carrier_code(carrier: Carrier) -> int:
    return 0 if carrier == Carrier.CIRCUIT_ST81 else 1


def carrier_from_code(code: int) -> Carrier:
    if int(code) == 0:
        return Carrier.CIRCUIT_ST81
    if int(code) == 1:
        return Carrier.PAIR_ST64
    raise ValueError("unknown W33 carrier code")


@dataclass(frozen=True)
class SharedHandle36:
    object_id: str
    destination_carrier: str
    destination_base36: int
    rights: tuple[str, ...] = ("read",)

    def __post_init__(self) -> None:
        if not 0 <= self.destination_base36 < 36:
            raise ValueError("shared handle base must lie in 0..35")
        if not self.rights or not set(self.rights) <= {"read"}:
            raise ValueError("shared handles are immutable read capabilities")

    def descriptor(self) -> dict[str, Any]:
        return {
            "object_id": self.object_id,
            "destination_carrier": self.destination_carrier,
            "destination_base36": self.destination_base36,
            "rights": list(self.rights),
        }


class SharedObjectStore36:
    def __init__(self) -> None:
        self.objects: dict[str, Any] = {}

    def put(self, payload: Any, destination_carrier: Carrier, destination_base36: int) -> SharedHandle36:
        if not 0 <= destination_base36 < 36:
            raise ValueError("destination base must lie in 0..35")
        object_id = digest({"mediaType": "application/vnd.w33.shared36.v1+json", "payload": payload})
        self.objects.setdefault(object_id, payload)
        return SharedHandle36(object_id, destination_carrier.value, destination_base36)

    def read(self, receiver: FiberEndpoint, handle: SharedHandle36) -> Any:
        if "read" not in handle.rights:
            raise PermissionError("shared handle lacks read right")
        if receiver.carrier.value != handle.destination_carrier or receiver.base36 != handle.destination_base36:
            raise PermissionError("shared handle not delegated to this carrier/base endpoint")
        if handle.object_id not in self.objects:
            raise KeyError("shared object is absent")
        return self.objects[handle.object_id]


@dataclass(frozen=True)
class KernelMessage36:
    message_id: str
    sequence: int
    nonce: str
    source_carrier: str
    source_base36: int
    destination_carrier: str
    destination_base36: int
    shared_handle: SharedHandle36

    def public_descriptor(self) -> dict[str, Any]:
        return {
            "message_id": self.message_id,
            "sequence": self.sequence,
            "nonce": self.nonce,
            "source_carrier": self.source_carrier,
            "source_base36": self.source_base36,
            "destination_carrier": self.destination_carrier,
            "destination_base36": self.destination_base36,
            "shared_handle": self.shared_handle.descriptor(),
        }

    def channel_key(self) -> tuple[str, int, str, int]:
        return (
            self.source_carrier,
            self.source_base36,
            self.destination_carrier,
            self.destination_base36,
        )


class HeterogeneousKernel36:
    def __init__(self, queue_depth: int = 8, object_store: SharedObjectStore36 | None = None) -> None:
        if queue_depth <= 0:
            raise ValueError("queue depth must be positive")
        self.queue_depth = int(queue_depth)
        self.object_store = object_store or SharedObjectStore36()
        self.queues: dict[tuple[str, int, str, int], list[KernelMessage36]] = {}
        self.next_send: dict[tuple[str, int, str, int], int] = {}
        self.next_recv: dict[tuple[str, int, str, int], int] = {}
        self.seen_nonces: set[str] = set()
        self.delivered: set[str] = set()
        self.acks: dict[str, str] = {}

    @staticmethod
    def _key(source: FiberEndpoint, destination_carrier: Carrier, destination_base36: int) -> tuple[str, int, str, int]:
        return (source.carrier.value, source.base36, destination_carrier.value, int(destination_base36))

    def send(
        self,
        source: FiberEndpoint,
        cap: IPCCapability,
        destination_carrier: Carrier,
        destination_base36: int,
        handle: SharedHandle36,
        nonce: str | None = None,
    ) -> KernelMessage36:
        if not cap.authorizes(source, "send"):
            raise PermissionError("source capability does not authorize SEND36")
        if not 0 <= destination_base36 < 36:
            raise ValueError("destination base must lie in 0..35")
        if handle.destination_carrier != destination_carrier.value or handle.destination_base36 != destination_base36:
            raise PermissionError("shared handle delegation does not match message destination")

        key = self._key(source, destination_carrier, destination_base36)
        queue = self.queues.setdefault(key, [])
        if len(queue) >= self.queue_depth:
            raise BufferError("SEND36 backpressure: destination channel queue is full")

        sequence = self.next_send.get(key, 0)
        if nonce is None:
            nonce = digest({
                "channel": list(key),
                "sequence": sequence,
                "object_id": handle.object_id,
            })
        if nonce in self.seen_nonces:
            raise PermissionError("SEND36 replay nonce already used")

        envelope = {
            "sequence": sequence,
            "nonce": nonce,
            "source_carrier": source.carrier.value,
            "source_base36": source.base36,
            "destination_carrier": destination_carrier.value,
            "destination_base36": destination_base36,
            "shared_handle": handle.descriptor(),
        }
        msg = KernelMessage36(
            message_id=digest(envelope),
            sequence=sequence,
            nonce=nonce,
            source_carrier=source.carrier.value,
            source_base36=source.base36,
            destination_carrier=destination_carrier.value,
            destination_base36=destination_base36,
            shared_handle=handle,
        )
        queue.append(msg)
        self.next_send[key] = sequence + 1
        self.seen_nonces.add(nonce)
        return msg

    def recv(self, receiver: FiberEndpoint, cap: IPCCapability) -> KernelMessage36 | None:
        if not cap.authorizes(receiver, "recv"):
            raise PermissionError("receiver capability does not authorize RECV36")

        candidates: list[tuple[str, tuple[str, int, str, int], KernelMessage36]] = []
        for key, queue in self.queues.items():
            if not queue:
                continue
            if key[2] != receiver.carrier.value or key[3] != receiver.base36:
                continue
            msg = queue[0]
            expected = self.next_recv.get(key, 0)
            if msg.sequence != expected:
                raise RuntimeError("channel sequence gap/out-of-order delivery")
            candidates.append((msg.message_id, key, msg))

        if not candidates:
            return None
        _, key, msg = min(candidates, key=lambda row: row[0])
        if msg.message_id in self.delivered:
            raise PermissionError("message replay detected at RECV36")
        self.queues[key].pop(0)
        self.next_recv[key] = msg.sequence + 1
        self.delivered.add(msg.message_id)
        return msg

    def ack(self, receiver: FiberEndpoint, cap: IPCCapability, message: KernelMessage36) -> str:
        if not cap.authorizes(receiver, "ack"):
            raise PermissionError("receiver capability does not authorize ACK36")
        if message.message_id not in self.delivered:
            raise PermissionError("cannot ACK an undelivered message")
        if receiver.carrier.value != message.destination_carrier or receiver.base36 != message.destination_base36:
            raise PermissionError("ACK36 endpoint is not the message destination")
        if message.message_id in self.acks:
            raise PermissionError("ACK36 is one-shot; duplicate acknowledgement rejected")
        ack = digest({
            "message_id": message.message_id,
            "sequence": message.sequence,
            "receiver": receiver.public_descriptor(),
        })
        self.acks[message.message_id] = ack
        return ack


WASM_IMPORT_SIGNATURES = {
    "SEND36": "(i32 destination_carrier, i32 destination_base36, i32 shared_handle) -> i32 message_token",
    "RECV36": "() -> i32 message_token_or_zero",
    "ACK36": "(i32 message_token) -> i32 ack_token",
}


class WasmKernelImports:
    """Endpoint-bound host functions for the real Wasm runtime.

    The guest never passes state216 or private_tag6.  Endpoint identity is bound
    by the host at instantiation; only destination carrier/base and opaque
    shared/message handles cross the Wasm ABI.
    """

    def __init__(
        self,
        kernel: HeterogeneousKernel36,
        endpoint: FiberEndpoint,
        capability: IPCCapability,
        shared_handles: Mapping[int, SharedHandle36] | None = None,
    ) -> None:
        self.kernel = kernel
        self.endpoint = endpoint
        self.capability = capability
        self.shared_handles = dict(shared_handles or {})
        self.messages: dict[int, KernelMessage36] = {}
        self.ack_tokens: dict[int, str] = {}
        self.next_message_token = 1
        self.next_ack_token = 1

    def _remember_message(self, msg: KernelMessage36) -> int:
        for token, existing in self.messages.items():
            if existing.message_id == msg.message_id:
                return token
        token = self.next_message_token
        self.next_message_token += 1
        self.messages[token] = msg
        return token

    def SEND36(self, args: tuple[int, ...], _runtime: wasm.CapabilityWasmRuntime) -> int:
        if len(args) != 3:
            raise RuntimeError("SEND36 Wasm ABI requires three i32 arguments")
        destination_carrier = carrier_from_code(args[0])
        destination_base = int(args[1])
        handle_id = int(args[2])
        handle = self.shared_handles.get(handle_id)
        if handle is None:
            raise PermissionError("unknown shared-object handle")
        msg = self.kernel.send(
            self.endpoint,
            self.capability,
            destination_carrier,
            destination_base,
            handle,
        )
        return self._remember_message(msg)

    def RECV36(self, args: tuple[int, ...], _runtime: wasm.CapabilityWasmRuntime) -> int:
        if args:
            raise RuntimeError("RECV36 Wasm ABI takes no arguments")
        msg = self.kernel.recv(self.endpoint, self.capability)
        return 0 if msg is None else self._remember_message(msg)

    def ACK36(self, args: tuple[int, ...], _runtime: wasm.CapabilityWasmRuntime) -> int:
        if len(args) != 1:
            raise RuntimeError("ACK36 Wasm ABI requires one message token")
        message = self.messages.get(int(args[0]))
        if message is None:
            raise PermissionError("unknown message token")
        ack = self.kernel.ack(self.endpoint, self.capability, message)
        token = self.next_ack_token
        self.next_ack_token += 1
        self.ack_tokens[token] = ack
        return token

    def host_functions(self) -> dict[tuple[str, str], wasm.HostCallable]:
        return {
            ("w33.kernel", "SEND36"): self.SEND36,
            ("w33.kernel", "RECV36"): self.RECV36,
            ("w33.kernel", "ACK36"): self.ACK36,
        }


def _full_cap(carrier: Carrier) -> IPCCapability:
    return IPCCapability(
        carrier,
        frozenset(range(36)),
        frozenset({"send", "recv", "ack", "derive"}),
    )


def _noninterference_transcript(private_tag: int) -> dict[str, Any]:
    store = SharedObjectStore36()
    kernel = HeterogeneousKernel36(queue_depth=2, object_store=store)
    source = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + private_tag)
    handle = store.put({"word": "same-public-workload"}, Carrier.PAIR_ST64, 7)
    msg = kernel.send(source, _full_cap(Carrier.CIRCUIT_ST81), Carrier.PAIR_ST64, 7, handle)
    return msg.public_descriptor()


def verify() -> dict[str, Any]:
    store = SharedObjectStore36()
    kernel = HeterogeneousKernel36(queue_depth=2, object_store=store)
    sender = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 2)
    receiver = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 5)
    cap81 = _full_cap(Carrier.CIRCUIT_ST81)
    cap64 = _full_cap(Carrier.PAIR_ST64)

    handle = store.put({"tensor": [3, 6, 9], "kind": "shared-demo"}, Carrier.PAIR_ST64, 7)
    first = kernel.send(sender, cap81, Carrier.PAIR_ST64, 7, handle, nonce="nonce-0")
    second = kernel.send(sender, cap81, Carrier.PAIR_ST64, 7, handle, nonce="nonce-1")

    backpressure_blocked = False
    try:
        kernel.send(sender, cap81, Carrier.PAIR_ST64, 7, handle, nonce="nonce-2")
    except BufferError:
        backpressure_blocked = True

    got0 = kernel.recv(receiver, cap64)
    got1 = kernel.recv(receiver, cap64)
    payload = store.read(receiver, got0.shared_handle) if got0 else None
    ack0 = kernel.ack(receiver, cap64, got0) if got0 else None

    duplicate_ack_blocked = False
    try:
        if got0:
            kernel.ack(receiver, cap64, got0)
    except PermissionError:
        duplicate_ack_blocked = True

    replay_nonce_blocked = False
    try:
        kernel.send(sender, cap81, Carrier.PAIR_ST64, 7, handle, nonce="nonce-0")
    except PermissionError:
        replay_nonce_blocked = True

    tag_transcripts = [_noninterference_transcript(tag) for tag in range(6)]
    private_fields_absent = all(
        "private_tag6" not in json.dumps(row, sort_keys=True)
        and "state216" not in json.dumps(row, sort_keys=True)
        for row in tag_transcripts
    )

    # Real Wasm import: main() calls w33.kernel.SEND36(1, 7, 42).
    wasm_store = SharedObjectStore36()
    wasm_kernel = HeterogeneousKernel36(queue_depth=2, object_store=wasm_store)
    wasm_sender = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 1)
    wasm_receiver = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 4)
    wasm_handle = wasm_store.put({"from": "wasm", "value": 36}, Carrier.PAIR_ST64, 7)
    imports = WasmKernelImports(wasm_kernel, wasm_sender, cap81, {42: wasm_handle})
    module = wasm.decode_module(wasm.build_host_import_module())
    runtime = wasm.CapabilityWasmRuntime(module, Carrier.CIRCUIT_ST81, imports.host_functions())
    wasm_message_token = runtime.execute_export("main")
    wasm_received = wasm_kernel.recv(wasm_receiver, cap64)
    wasm_payload = wasm_store.read(wasm_receiver, wasm_received.shared_handle) if wasm_received else None

    checks = {
        "sequence_numbers_are_monotone": first.sequence == 0 and second.sequence == 1,
        "bounded_queue_backpressure": backpressure_blocked,
        "receive_preserves_channel_order": got0 is not None and got1 is not None and got0.sequence == 0 and got1.sequence == 1,
        "shared_object_handle_delivers_content": payload == {"tensor": [3, 6, 9], "kind": "shared-demo"},
        "ack_bound_to_delivered_receiver": ack0 is not None and kernel.acks.get(first.message_id) == ack0,
        "duplicate_ack_fails_closed": duplicate_ack_blocked,
        "nonce_replay_fails_closed": replay_nonce_blocked,
        "all_six_private_tags_have_identical_public_transcript": all(row == tag_transcripts[0] for row in tag_transcripts[1:]),
        "private_fibre_fields_never_enter_public_message": private_fields_absent,
        "wasm_import_is_real_binary_call": isinstance(wasm_message_token, int) and wasm_message_token > 0,
        "wasm_send36_reaches_other_carrier": wasm_payload == {"from": "wasm", "value": 36},
        "wasm_guest_never_passes_private_tag": all("state216" not in sig and "private" not in sig for sig in WASM_IMPORT_SIGNATURES.values()),
    }

    return {
        "schema": "w33.heterogeneous-36-kernel.v2",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "abi": {
            "syscalls": WASM_IMPORT_SIGNATURES,
            "queue_depth": kernel.queue_depth,
            "carrier_translation": "FORBIDDEN",
            "shared_memory": "immutable content-addressed receiver-bound handles",
        },
        "sample": {
            "message0": first.public_descriptor(),
            "message1": second.public_descriptor(),
            "ack0": ack0,
            "wasm_message_token": wasm_message_token,
            "wasm_payload": wasm_payload,
        },
        "noninterference": {
            "varied_secret": "private_tag6 in {0,...,5}",
            "held_public": "carrier=ST81, base36=7, destination ST64/base7, payload and sequence",
            "public_transcripts_equal": all(row == tag_transcripts[0] for row in tag_transcripts[1:]),
        },
        "checks": checks,
        "honesty_boundary": (
            "The noninterference result is exhaustive for the six private fibre tags under this kernel's deterministic public transcript. "
            "It is not a timing/cache side-channel proof for a physical implementation or host language runtime."
        ),
    }


def main() -> int:
    payload = verify()
    print(json.dumps(payload, indent=2))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
