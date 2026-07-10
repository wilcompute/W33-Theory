"""Track module extracted from w33_levi_next5_v2."""
from __future__ import annotations
from w33_levi_next5_v2_common import *

class SentinelFaultStack(TypedFaultStack):
    """Authenticated typed stack with a context-readout syndrome on payload error."""

    def __init__(self) -> None:
        super().__init__()
        self.sentinel_rows = self.kernel.geometry.incidence_columns
        self.sentinel_code = base.gf2_nullspace(self.sentinel_rows, 40)
        self.codewords = base.enumerate_code(self.sentinel_code)
        nonzero = [word.bit_count() for word in self.codewords if word]
        self.minimum_distance = min(nonzero)
        self.weight_enumerator = dict(sorted(Counter(word.bit_count() for word in self.codewords).items()))

    def expected_packet(self, envelope: TransportEnvelope) -> TypedPacket:
        self.kernel.validate(envelope.origin)
        if envelope.transition == "native":
            return envelope.origin
        if envelope.transition == "mirror":
            return self.kernel.mirror(envelope.origin)
        raise AdmissionError("framing: unknown transition")

    def sentinel_syndrome(self, envelope: TransportEnvelope) -> tuple[int, int]:
        expected = self.expected_packet(envelope)
        delta = envelope.current.payload ^ expected.payload
        return delta, base.gf2_apply(self.sentinel_rows, delta)

    def reseal(self, current: TypedPacket, origin: TypedPacket, transition: str, nonce: int) -> TransportEnvelope:
        body = self._body(current, origin, transition, nonce)
        parity = self._parity(body)
        return TransportEnvelope(current, origin, transition, nonce, parity, self._tag(body, parity))

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
            delta, syndrome = self.sentinel_syndrome(envelope)
        except PacketValidationError as exc:
            raise AdmissionError(f"levi-origin: {exc}") from exc
        if delta and syndrome:
            raise AdmissionError("sentinel: context readout detected payload displacement")
        return super().admit(envelope, route_available)

    def combined_theorem(self, seed: int = 20260710) -> dict:
        rng = np.random.default_rng(seed)
        zero = self.kernel.encode(0, 0)
        legal_native = self.admit(self.seal_native(zero, 1)) == zero
        legal_mirror = self.admit(self.seal_mirror(zero, 2)).type_bit == 1

        sub8_rejected = Counter()
        for weight in range(1, 8):
            for trial in range(64):
                support = rng.choice(40, size=weight, replace=False)
                error = sum(1 << int(bit) for bit in support)
                forged = TypedPacket(0, 0, error)
                envelope = self.reseal(forged, zero, "native", 1000 + 64 * weight + trial)
                try:
                    self.admit(envelope)
                except AdmissionError as exc:
                    sub8_rejected[str(exc).split(":", 1)[0]] += 1

        minimum_word = next(word for word in self.codewords if word.bit_count() == self.minimum_distance)
        dark_packet = self.kernel.encode(0, minimum_word)
        dark_envelope = self.reseal(dark_packet, zero, "native", 7777)
        dark_reason = None
        try:
            self.admit(dark_envelope)
        except AdmissionError as exc:
            dark_reason = str(exc).split(":", 1)[0]

        confused = TypedPacket(1, 0, 0)
        confusion_envelope = self.reseal(confused, zero, "native", 8888)
        confusion_reason = None
        try:
            self.admit(confusion_envelope)
        except AdmissionError as exc:
            confusion_reason = str(exc).split(":", 1)[0]

        checks = {
            "sentinel_dimension_15": len(self.sentinel_code) == 15,
            "sentinel_distance_8": self.minimum_distance == 8,
            "minimum_words_45": self.weight_enumerator.get(8) == 45,
            "legal_native_accepted": legal_native,
            "legal_mirror_accepted": legal_mirror,
            "all_sampled_weight_1_to_7_errors_rejected_at_sentinel": sub8_rejected["sentinel"] == 7 * 64,
            "distance_theorem_covers_all_weight_below_8": all(weight == 0 or weight >= 8 for weight in self.weight_enumerator),
            "sentinel_dark_weight8_still_rejected_by_provenance": dark_reason == "type-confusion",
            "authenticated_raw_type_confusion_rejected": confusion_reason == "type-confusion",
        }
        return {
            "status": "PROVED" if all(checks.values()) else "FAIL",
            "all_pass": all(checks.values()),
            "checks": checks,
            "code": {
                "parameters": "[40,15,8]_2",
                "weight_enumerator": {str(k): v for k, v in self.weight_enumerator.items()},
            },
            "sampled_sub8_rejection_layers": dict(sub8_rejected),
            "weight8_dark_codeword_rejection_layer": dark_reason,
            "type_confusion_rejection_layer": confusion_reason,
            "theorem": (
                "No nonzero payload displacement of support <8 is sentinel-dark; a displacement in the "
                "distance-8 dark code or a raw type retag is still rejected by immutable transition provenance."
            ),
        }
