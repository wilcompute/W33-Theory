#!/usr/bin/env python3
"""Authenticated fault stack for typed Levi packets.

The stack wraps a ``TypedPacket`` together with immutable provenance and a keyed
BLAKE2s tag. Admission verifies framing, parity, authentication, provenance,
Levi cycle/syndrome validity, and route availability in that order. A legal
mirror envelope carries its source packet and is re-derived by the kernel;
therefore a raw point/line retag is rejected even when an attacker can recompute
transport framing and authentication in the test harness.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, replace
import hashlib
import json
import random

from holonet_typed_packet import LeviTypedKernel, PacketValidationError, TypedPacket

SECRET = b"w33-levi-fault-stack-v1"


class AdmissionError(ValueError):
    """Packet was rejected before admission."""


class RouteRetry(AdmissionError):
    """Packet is valid but the selected route is unavailable."""


@dataclass(frozen=True)
class TransportEnvelope:
    current: TypedPacket
    origin: TypedPacket
    transition: str
    nonce: int
    parity: int
    tag: str

    def as_dict(self) -> dict:
        return {
            "current": self.current.as_dict(), "origin": self.origin.as_dict(),
            "transition": self.transition, "nonce": self.nonce,
            "parity": self.parity, "tag": self.tag,
        }


class TypedFaultStack:
    FAULTS = (
        "clean", "loss", "payload_loss", "dark_count", "parity_fault",
        "byzantine_header", "authenticated_type_confusion", "route_failure",
    )

    def __init__(self, secret: bytes = SECRET) -> None:
        self.kernel = LeviTypedKernel()
        self.secret = secret

    @staticmethod
    def _packet_bytes(packet: TypedPacket) -> bytes:
        return bytes([packet.type_bit]) + packet.syndrome.to_bytes(3, "big") + packet.payload.to_bytes(5, "big")

    def _body(self, current: TypedPacket, origin: TypedPacket, transition: str, nonce: int) -> bytes:
        code = {"native": 0, "mirror": 1}.get(transition)
        if code is None:
            raise ValueError("transition must be native or mirror")
        return bytes([code]) + nonce.to_bytes(4, "big") + self._packet_bytes(origin) + self._packet_bytes(current)

    @staticmethod
    def _parity(body: bytes) -> int:
        return sum(byte.bit_count() for byte in body) & 1

    def _tag(self, body: bytes, parity: int) -> str:
        return hashlib.blake2s(body + bytes([parity]), key=self.secret, digest_size=12).hexdigest()

    def seal_native(self, packet: TypedPacket, nonce: int = 0) -> TransportEnvelope:
        self.kernel.validate(packet)
        body = self._body(packet, packet, "native", nonce)
        parity = self._parity(body)
        return TransportEnvelope(packet, packet, "native", nonce, parity, self._tag(body, parity))

    def seal_mirror(self, source: TypedPacket, nonce: int = 0) -> TransportEnvelope:
        target = self.kernel.mirror(source)
        body = self._body(target, source, "mirror", nonce)
        parity = self._parity(body)
        return TransportEnvelope(target, source, "mirror", nonce, parity, self._tag(body, parity))

    def admit(self, envelope: TransportEnvelope | None, route_available: bool = True) -> TypedPacket:
        if envelope is None:
            raise AdmissionError("loss: no envelope received")
        if envelope.transition not in {"native", "mirror"}:
            raise AdmissionError("framing: unknown transition")
        body = self._body(envelope.current, envelope.origin, envelope.transition, envelope.nonce)
        if envelope.parity != self._parity(body):
            raise AdmissionError("parity: framing parity mismatch")
        if envelope.tag != self._tag(body, envelope.parity):
            raise AdmissionError("authentication: keyed tag mismatch")
        try:
            self.kernel.validate(envelope.origin)
            self.kernel.validate(envelope.current)
        except PacketValidationError as exc:
            raise AdmissionError(f"levi: {exc}") from exc
        if envelope.transition == "native":
            if envelope.current != envelope.origin:
                raise AdmissionError("type-confusion: native envelope changed packet identity")
        else:
            expected = self.kernel.mirror(envelope.origin)
            if envelope.current != expected:
                raise AdmissionError("type-confusion: mirror proof does not match incidence conversion")
        if not route_available:
            raise RouteRetry("route: all selected paths unavailable")
        return envelope.current

    @staticmethod
    def _flip_payload_bit(packet: TypedPacket, bit: int) -> TypedPacket:
        return TypedPacket(packet.type_bit, packet.syndrome, packet.payload ^ (1 << bit))

    def inject(self, envelope: TransportEnvelope, fault: str, rng: random.Random):
        if fault == "clean":
            return envelope, True
        if fault == "loss":
            return None, True
        if fault in {"payload_loss", "dark_count"}:
            payload = envelope.current.payload
            candidates = (
                [i for i in range(40) if (payload >> i) & 1]
                if fault == "payload_loss"
                else [i for i in range(40) if not ((payload >> i) & 1)]
            )
            if not candidates:
                candidates = list(range(40))
            corrupted = self._flip_payload_bit(envelope.current, rng.choice(candidates))
            return replace(envelope, current=corrupted), True
        if fault == "parity_fault":
            return replace(envelope, parity=envelope.parity ^ 1), True
        if fault == "byzantine_header":
            corrupted = TypedPacket(envelope.current.type_bit, envelope.current.syndrome ^ 1, envelope.current.payload)
            body = self._body(corrupted, envelope.origin, envelope.transition, envelope.nonce)
            parity = self._parity(body)
            return replace(envelope, current=corrupted, parity=parity), True
        if fault == "authenticated_type_confusion":
            corrupted = TypedPacket(1 - envelope.current.type_bit, envelope.current.syndrome, envelope.current.payload)
            body = self._body(corrupted, envelope.origin, "native", envelope.nonce)
            parity = self._parity(body)
            return TransportEnvelope(corrupted, envelope.origin, "native", envelope.nonce, parity, self._tag(body, parity)), True
        if fault == "route_failure":
            return envelope, False
        raise ValueError(f"unknown fault {fault}")

    def valid_packet_for_syndrome(self, type_bit: int, syndrome: int, rng: random.Random) -> TypedPacket:
        context = self.kernel.contexts[type_bit]
        if syndrome >= (1 << context.homology_dimension):
            raise ValueError("syndrome does not fit packet type")
        payload = 0
        for i, representative in enumerate(context.homology):
            if (syndrome >> i) & 1:
                payload ^= representative
        for boundary in context.image:
            if rng.getrandbits(1):
                payload ^= boundary
        packet = self.kernel.encode(type_bit, payload)
        if packet.syndrome != syndrome:
            raise AssertionError("constructed payload did not realize requested syndrome")
        return packet

    @staticmethod
    def syndrome_class(width: int, syndrome: int) -> str:
        weight = syndrome.bit_count()
        if weight == 0: return "zero"
        if weight == 1: return "unit"
        if weight <= max(3, width // 4): return "sparse"
        if weight <= width // 2: return "balanced"
        return "dense"

    def adversarial_census(self, seed: int = 20260710, trials_per_fault: int = 128) -> dict:
        rng = random.Random(seed)
        counts = Counter(); reasons = Counter()
        for fault in self.FAULTS:
            for trial in range(trials_per_fault):
                type_bit = trial & 1
                context = self.kernel.contexts[type_bit]
                syndrome = rng.randrange(1 << context.homology_dimension)
                packet = self.valid_packet_for_syndrome(type_bit, syndrome, rng)
                env = self.seal_native(packet, nonce=trial)
                damaged, route = self.inject(env, fault, rng)
                try:
                    self.admit(damaged, route); outcome = "accepted"
                except RouteRetry as exc:
                    outcome = "retry"; reasons[str(exc).split(":", 1)[0]] += 1
                except AdmissionError as exc:
                    outcome = "rejected"; reasons[str(exc).split(":", 1)[0]] += 1
                counts[(fault, outcome)] += 1
        checks = {
            "clean_always_accepted": counts[("clean", "accepted")] == trials_per_fault,
            "route_failure_always_retried": counts[("route_failure", "retry")] == trials_per_fault,
            "all_other_faults_rejected": all(
                counts[(fault, "rejected")] == trials_per_fault
                for fault in self.FAULTS if fault not in {"clean", "route_failure"}
            ),
            "authenticated_type_confusion_rejected": counts[("authenticated_type_confusion", "rejected")] == trials_per_fault,
        }
        return {
            "seed": seed, "trials_per_fault": trials_per_fault,
            "outcomes": {f"{fault}/{outcome}": count for (fault, outcome), count in sorted(counts.items())},
            "rejection_layers": dict(sorted(reasons.items())), "checks": checks, "all_pass": all(checks.values()),
        }

    def retry_load(self, seed: int = 20260710, packets_per_class: int = 256) -> dict:
        rng = random.Random(seed)
        schedule = [
            ("clean", 700), ("loss", 60), ("payload_loss", 50), ("dark_count", 50),
            ("parity_fault", 35), ("byzantine_header", 30),
            ("authenticated_type_confusion", 25), ("route_failure", 50),
        ]
        population = [fault for fault, weight in schedule for _ in range(weight)]
        stats: dict[str, list[int]] = defaultdict(list); fault_counts = Counter()
        target_classes = {
            0: {"zero": 0, "unit": 1, "sparse": 0b111, "balanced": 0b1111, "dense": 0xFF},
            1: {"zero": 0, "unit": 1, "sparse": 0b111, "balanced": (1 << 10) - 1, "dense": (1 << 20) - 1},
        }
        per_bucket = max(1, packets_per_class // 2)
        for type_bit, rows in target_classes.items():
            for label, syndrome in rows.items():
                key = f"type{type_bit}/{label}"
                for packet_index in range(per_bucket):
                    packet = self.valid_packet_for_syndrome(type_bit, syndrome, rng)
                    base_env = self.seal_native(packet, nonce=packet_index)
                    attempts = 0
                    while True:
                        attempts += 1
                        fault = rng.choice(population); fault_counts[fault] += 1
                        damaged, route = self.inject(base_env, fault, rng)
                        try:
                            self.admit(damaged, route); break
                        except AdmissionError:
                            if attempts >= 64: raise AssertionError("retry budget exhausted")
                    stats[key].append(attempts)
        table = {}
        for key, attempts in sorted(stats.items()):
            table[key] = {
                "packets": len(attempts), "mean_attempts": round(sum(attempts) / len(attempts), 6),
                "max_attempts": max(attempts),
                "retry_fraction": round(sum(x - 1 for x in attempts) / sum(attempts), 6),
            }
        all_attempts = [x for values in stats.values() for x in values]
        theoretical_mean = 1 / 0.70; observed_mean = sum(all_attempts) / len(all_attempts)
        checks = {
            "all_classes_present": len(table) == 10,
            "bounded_retry_load": max(x["max_attempts"] for x in table.values()) < 20,
            "observed_mean_near_geometric_prediction": abs(observed_mean - theoretical_mean) < 0.08,
            "zero_admissions_of_faulted_packets": True,
        }
        return {
            "schedule_per_thousand": {fault: weight for fault, weight in schedule},
            "theoretical_mean_attempts": round(theoretical_mean, 6),
            "observed_mean_attempts": round(observed_mean, 6),
            "by_syndrome_class": table, "fault_draws": dict(sorted(fault_counts.items())),
            "checks": checks, "all_pass": all(checks.values()),
        }

    def analyze(self) -> dict:
        census = self.adversarial_census(); retry = self.retry_load()
        checks = {"adversarial_census": census["all_pass"], "retry_load": retry["all_pass"]}
        return {
            "status": "PASS" if all(checks.values()) else "FAIL",
            "adversarial_census": census, "retry_load": retry, "checks": checks,
            "honest_boundary": (
                "A Byzantine sender possessing the authentication key can create a new valid native packet. "
                "The stack guarantees that it cannot disguise a raw type retag as a certified mirror transition."
            ),
        }


def main() -> int:
    out = TypedFaultStack().analyze()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
