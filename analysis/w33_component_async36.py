#!/usr/bin/env python3
"""Typed asynchronous component linking over the heterogeneous W33 36-state ABI.

This is a W33-native engineering layer inspired by the WebAssembly Component
Model/WASI 0.3 pattern (typed interfaces plus async/future/stream composition),
not an implementation of the Component Model specification.

The theorem exercised here is narrower and executable:
  * imports and exports must match exactly before components link;
  * cross-carrier interfaces may expose only neutral ABI types;
  * bounded SEND36 backpressure is represented by a future rather than a busy
    polling loop;
  * freeing the destination queue makes the pending future ready;
  * streams/futures never expose the private six-state fibre tag.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any

from w33_heterogeneous_36_ipc import FiberEndpoint, IPCCapability
from w33_heterogeneous_36_kernel import (
    HeterogeneousKernel36,
    SharedHandle36,
    SharedObjectStore36,
)
from w33_typed_universal_microvm import Carrier


def canon(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode()


def digest(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(value)).hexdigest()


NEUTRAL_TYPES = frozenset({"u32", "handle36", "message36", "ack36", "future<u32>", "stream<u32>"})


@dataclass(frozen=True)
class FuncSig:
    params: tuple[str, ...]
    results: tuple[str, ...]
    is_async: bool = False

    def descriptor(self) -> dict[str, Any]:
        return {"params": list(self.params), "results": list(self.results), "async": self.is_async}


@dataclass(frozen=True)
class Interface:
    name: str
    functions: tuple[tuple[str, FuncSig], ...]

    def descriptor(self) -> dict[str, Any]:
        return {"name": self.name, "functions": {n: s.descriptor() for n, s in self.functions}}


@dataclass(frozen=True)
class ComponentDecl:
    name: str
    carrier: Carrier
    imports: tuple[Interface, ...] = ()
    exports: tuple[Interface, ...] = ()


class LinkError(ValueError):
    pass


class ComponentLinker:
    @staticmethod
    def _cross_carrier_safe(interface: Interface) -> bool:
        for _, sig in interface.functions:
            for ty in sig.params + sig.results:
                if ty not in NEUTRAL_TYPES:
                    return False
        return True

    def link(self, consumer: ComponentDecl, provider: ComponentDecl, interface_name: str) -> dict[str, Any]:
        want = next((i for i in consumer.imports if i.name == interface_name), None)
        have = next((i for i in provider.exports if i.name == interface_name), None)
        if want is None or have is None:
            raise LinkError("required import/export interface is absent")
        if want.descriptor() != have.descriptor():
            raise LinkError("component interface signature mismatch")
        cross = consumer.carrier != provider.carrier
        if cross and not self._cross_carrier_safe(want):
            raise LinkError("cross-carrier interface leaks non-neutral type")
        row = {
            "consumer": consumer.name,
            "provider": provider.name,
            "consumer_carrier": consumer.carrier.value,
            "provider_carrier": provider.carrier.value,
            "interface": want.descriptor(),
            "cross_carrier": cross,
        }
        row["link_digest"] = digest(row)
        return row


class FutureU32:
    def __init__(self) -> None:
        self.state = "PENDING"
        self.value: int | None = None

    @property
    def ready(self) -> bool:
        return self.state == "READY"

    def resolve(self, value: int) -> None:
        if self.state != "PENDING":
            raise RuntimeError("future may resolve exactly once")
        self.value = int(value) & 0xFFFFFFFF
        self.state = "READY"

    def take(self) -> int:
        if self.state != "READY" or self.value is None:
            raise RuntimeError("future is not ready")
        self.state = "CONSUMED"
        return self.value


class StreamU32:
    def __init__(self, capacity: int = 8) -> None:
        if capacity <= 0:
            raise ValueError("stream capacity must be positive")
        self.capacity = int(capacity)
        self.items: list[int] = []
        self.closed = False

    def push(self, value: int) -> None:
        if self.closed:
            raise RuntimeError("stream closed")
        if len(self.items) >= self.capacity:
            raise BufferError("stream backpressure")
        self.items.append(int(value) & 0xFFFFFFFF)

    def pop(self) -> int | None:
        return None if not self.items else self.items.pop(0)

    def close(self) -> None:
        self.closed = True


@dataclass
class PendingSend:
    future: FutureU32
    source: FiberEndpoint
    capability: IPCCapability
    destination_carrier: Carrier
    destination_base36: int
    handle: SharedHandle36
    nonce: str


class Async36Runtime:
    """Cooperative async wrapper around the fail-closed HeterogeneousKernel36."""
    def __init__(self, kernel: HeterogeneousKernel36) -> None:
        self.kernel = kernel
        self.pending: list[PendingSend] = []
        self.message_tokens: dict[int, Any] = {}
        self.next_token = 1

    def _token(self, message: Any) -> int:
        token = self.next_token
        self.next_token += 1
        self.message_tokens[token] = message
        return token

    def send_async(self, source: FiberEndpoint, cap: IPCCapability,
                   destination_carrier: Carrier, destination_base36: int,
                   handle: SharedHandle36, nonce: str) -> FutureU32:
        fut = FutureU32()
        try:
            msg = self.kernel.send(source, cap, destination_carrier, destination_base36, handle, nonce=nonce)
            fut.resolve(self._token(msg))
        except BufferError:
            self.pending.append(PendingSend(fut, source, cap, destination_carrier,
                                            destination_base36, handle, nonce))
        return fut

    def pump(self) -> int:
        made_ready = 0
        still: list[PendingSend] = []
        for row in self.pending:
            try:
                msg = self.kernel.send(row.source, row.capability, row.destination_carrier,
                                       row.destination_base36, row.handle, nonce=row.nonce)
                row.future.resolve(self._token(msg))
                made_ready += 1
            except BufferError:
                still.append(row)
        self.pending = still
        return made_ready

    def recv_stream(self, receiver: FiberEndpoint, cap: IPCCapability, stream: StreamU32) -> int:
        pushed = 0
        while len(stream.items) < stream.capacity:
            msg = self.kernel.recv(receiver, cap)
            if msg is None:
                break
            stream.push(self._token(msg))
            pushed += 1
        return pushed


def full_cap(carrier: Carrier) -> IPCCapability:
    return IPCCapability(carrier, frozenset(range(36)), frozenset({"send", "recv", "ack", "derive"}))


def verify() -> dict[str, Any]:
    ipc = Interface("w33:ipc36", (
        ("send", FuncSig(("u32", "u32", "handle36"), ("future<u32>",), True)),
        ("recv", FuncSig((), ("stream<u32>",), True)),
    ))
    a = ComponentDecl("st81-guest", Carrier.CIRCUIT_ST81, imports=(ipc,))
    b = ComponentDecl("st64-kernel", Carrier.PAIR_ST64, exports=(ipc,))
    link = ComponentLinker().link(a, b, "w33:ipc36")

    bad = Interface("w33:bad", (("leak", FuncSig(("private_tag6",), ("u32",))),))
    leak_blocked = False
    try:
        ComponentLinker().link(
            ComponentDecl("a", Carrier.CIRCUIT_ST81, imports=(bad,)),
            ComponentDecl("b", Carrier.PAIR_ST64, exports=(bad,)),
            "w33:bad",
        )
    except LinkError:
        leak_blocked = True

    store = SharedObjectStore36()
    kernel = HeterogeneousKernel36(queue_depth=1, object_store=store)
    async_rt = Async36Runtime(kernel)
    sender = FiberEndpoint(Carrier.CIRCUIT_ST81, 6 * 7 + 2)
    receiver = FiberEndpoint(Carrier.PAIR_ST64, 6 * 7 + 5)
    handle = store.put({"payload": "component-async"}, Carrier.PAIR_ST64, 7)
    first = async_rt.send_async(sender, full_cap(sender.carrier), receiver.carrier, 7, handle, "async-0")
    second = async_rt.send_async(sender, full_cap(sender.carrier), receiver.carrier, 7, handle, "async-1")
    pending_before = second.state == "PENDING"
    stream = StreamU32(capacity=1)
    got = async_rt.recv_stream(receiver, full_cap(receiver.carrier), stream)
    woke = async_rt.pump()
    pending_after = second.state == "READY"

    serialized = json.dumps({"link": link, "stream": stream.items}, sort_keys=True)
    checks = {
        "cross_carrier_interface_links_exactly": link["cross_carrier"] is True,
        "private_interface_type_rejected": leak_blocked,
        "first_send_ready": first.ready,
        "second_send_waits_on_backpressure": pending_before,
        "receiver_frees_one_slot": got == 1,
        "pump_wakes_pending_send": woke == 1 and pending_after,
        "private_fibre_absent_from_public_state": "private_tag6" not in serialized and "state216" not in serialized,
    }
    return {
        "schema": "w33.component-async36.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "link": link,
        "checks": checks,
        "interpretation": "The common 36-state ABI is a typed asynchronous component boundary; backpressure becomes a future dependency rather than a carrier retyping operation.",
    }


if __name__ == "__main__":
    payload = verify()
    print(json.dumps(payload, indent=2))
    raise SystemExit(0 if payload["status"] == "PASS" else 1)
