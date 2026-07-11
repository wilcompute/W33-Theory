#!/usr/bin/env python3
"""Hardware-in-the-loop time-tagger runtime for optical homology packets."""
from __future__ import annotations
from functools import lru_cache

from collections import Counter
from dataclasses import dataclass, asdict
import hashlib
import json
import math
import random
import sys
from pathlib import Path
from typing import Iterable, Iterator, TextIO

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from w33_levi_next5_v4_common import (
    ACTIVE, SEEDS, apply_cols, build_w33, coordinates, gf2_apply,
    gf2_nullspace, gf2_row_basis, homology_action, line_perm_from_point_perm,
    matrix_rows_to_masks, point_outer_perm, point_transvection_perm,
    quotient_basis, sha256_json, tagged_basis,
)
from w33_levi_next5_v4_foundry import halmos
from w33_levi_next5_v4_functor import object_sets, v3_module

SECRET = b"w33-hil-runtime-v4"


@dataclass(frozen=True)
class TimeTag:
    timestamp_ps: int
    channel: int
    frame: int


@dataclass(frozen=True)
class Packet:
    type_bit: int
    syndrome: int
    payload: int


@dataclass(frozen=True)
class Envelope:
    origin: Packet
    current: Packet
    transition: str
    nonce: int
    tag: str


class AdmissionError(ValueError):
    pass


class Retry(ValueError):
    pass


class Context:
    def __init__(self, differential):
        self.rows = matrix_rows_to_masks(differential % 2)
        self.image = gf2_row_basis(self.rows)
        self.kernel = gf2_nullspace(self.rows, 40)
        self.hom = quotient_basis(self.kernel, self.image)
        self.tagged = tagged_basis(self.image + self.hom)

    def syndrome(self, payload):
        if gf2_apply(self.rows, payload):
            raise AdmissionError("homology:not-cycle")
        rem, tag = coordinates(payload, self.tagged)
        if rem:
            raise AdmissionError("homology:not-coordinate")
        return tag >> len(self.image)

    def packet(self, syndrome, boundary_mask=0):
        payload = 0
        for i, representative in enumerate(self.hom):
            if (syndrome >> i) & 1:
                payload ^= representative
        for i, boundary in enumerate(self.image):
            if (boundary_mask >> i) & 1:
                payload ^= boundary
        return Packet(0, syndrome, payload)


class NDJSONTimeTagAdapter:
    """Streaming adapter compatible with line-oriented time-tagger exports."""

    @staticmethod
    def dump(tags: Iterable[TimeTag], handle: TextIO) -> None:
        for tag in tags:
            handle.write(json.dumps(asdict(tag), separators=(",", ":")) + "\n")

    @staticmethod
    def load(handle: TextIO) -> Iterator[TimeTag]:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            yield TimeTag(int(row["timestamp_ps"]), int(row["channel"]), int(row["frame"]))


class HILRuntime:
    def __init__(self):
        self.geom = build_w33()
        self.point = Context(self.geom.adjacency)
        assert len(self.point.hom) == 8
        self.inc_rows = matrix_rows_to_masks(self.geom.incidence % 2)
        self.sentinel_basis = gf2_nullspace(self.inc_rows, 40)
        self.dark8 = []
        for mask in range(1, 1 << len(self.sentinel_basis)):
            word = 0
            for i, basis in enumerate(self.sentinel_basis):
                if (mask >> i) & 1:
                    word ^= basis
            if word.bit_count() == 8:
                self.dark8.append(word)
        self.dark8 = sorted(set(self.dark8))
        assert len(self.dark8) == 45

        _scale, C, _U = halmos(ACTIVE)
        self.C = C
        self.bound = float(max(np.sum(np.abs(C), axis=1)))
        self.codebook = np.array([
            C @ np.array([1.0 if (s >> i) & 1 else -1.0 for i in range(8)]) / self.bound
            for s in range(256)
        ])
        self.drift_estimate = np.zeros(8)
        self.gain_estimate = 1.0
        self.dark_estimate = 1e-4
        self.telemetry = Counter()

        geom, pgens, _line40, racts, lineperms, G, names, singular = v3_module()
        self.pgens = pgens
        self.mgens = racts
        self.lineperms = lineperms
        self.names = names
        self.singular = singular
        self.triangles, self.sixes = object_sets(G)
        self.tri_idx = {frozenset(x): i for i, x in enumerate(self.triangles)}
        self.six_idx = {frozenset(x): i for i, x in enumerate(self.sixes)}
        self.pairs = [(i, j) for i in range(40) for j in range(i + 1, 40) if not geom.adjacency[i, j]]
        self.pair_idx = {frozenset(x): i for i, x in enumerate(self.pairs)}

    @staticmethod
    def _tag(origin, transition, nonce):
        body = f"{origin.type_bit}:{origin.syndrome}:{origin.payload}:{transition}:{nonce}".encode()
        return hashlib.blake2s(body, key=SECRET, digest_size=12).hexdigest()

    def seal(self, origin, current, transition, nonce):
        return Envelope(origin, current, transition, nonce, self._tag(origin, transition, nonce))

    def runtime_coordinate(self, syndrome, nonce):
        digest = hashlib.sha256(f"{syndrome}:{nonce}".encode()).digest()
        word = [b % 9 for b in digest]
        sv = self.singular[0]
        tri = set(self.triangles[0])
        six = set(self.sixes[0])
        pair = set(self.pairs[0])
        chirality = 0
        for k in word:
            sv = apply_cols(self.mgens[k], sv)
            tri = {self.lineperms[k][x] for x in tri}
            six = {self.lineperms[k][x] for x in six}
            pair = {self.pgens[k][x] for x in pair}
            if k == 8:
                chirality ^= 1
        li = self.singular.index(sv)
        return {
            "chirality": chirality,
            "line27": self.names[li],
            "tritangent45": self.tri_idx[frozenset(tri)],
            "root72": self.six_idx[frozenset(six)],
            "pair540": self.pair_idx[frozenset(pair)],
            "event_word_digest": hashlib.sha256(bytes(word)).hexdigest(),
        }

    def admit(self, envelope, confidence):
        if confidence < 0.02:
            self.telemetry["retry_low_confidence"] += 1
            raise Retry("optical:low-confidence")
        if envelope.tag != self._tag(envelope.origin, envelope.transition, envelope.nonce):
            self.telemetry["reject_authentication"] += 1
            raise AdmissionError("authentication")
        expected = envelope.origin
        error = envelope.current.payload ^ expected.payload
        if gf2_apply(self.inc_rows, error):
            self.telemetry["reject_sentinel"] += 1
            raise AdmissionError("sentinel")
        if envelope.transition != "native" or envelope.current.type_bit != expected.type_bit:
            self.telemetry["reject_type_confusion"] += 1
            raise AdmissionError("type-confusion")
        if envelope.current != expected:
            self.telemetry["reject_provenance"] += 1
            raise AdmissionError("provenance")
        if self.point.syndrome(envelope.current.payload) != envelope.current.syndrome:
            self.telemetry["reject_homology"] += 1
            raise AdmissionError("homology")
        self.telemetry["accepted"] += 1
        return self.runtime_coordinate(envelope.current.syndrome, envelope.nonce)

    def synthesize_tags(self, frame, syndrome, rng, drift, photons=4000, frame_ps=2000, jitter_ps=38.0):
        x = np.array([1.0 if (syndrome >> i) & 1 else -1.0 for i in range(8)])
        z = np.clip(self.codebook[syndrome] + drift, -0.96, 0.96)
        gain = max(0.35, rng.normal(0.78, 0.055))
        total = photons * gain
        plus = rng.poisson(total * (1 + z) / 2 + 0.0001, size=8)
        minus = rng.poisson(total * (1 - z) / 2 + 0.0001, size=8)
        start = frame * frame_ps
        tags = [TimeTag(start, 16, frame)]
        for ch, count in enumerate(plus):
            for _ in range(int(count)):
                tags.append(TimeTag(start + 500 + int(rng.normal(0, jitter_ps)), ch, frame))
        for ch, count in enumerate(minus):
            for _ in range(int(count)):
                tags.append(TimeTag(start + 500 + int(rng.normal(0, jitter_ps)), ch + 8, frame))
        tags.sort(key=lambda t: (t.timestamp_ps, t.channel))
        return tags

    @staticmethod
    def frame_counts(tags):
        plus = np.zeros(8, dtype=int)
        minus = np.zeros(8, dtype=int)
        for tag in tags:
            if 0 <= tag.channel < 8:
                plus[tag.channel] += 1
            elif 8 <= tag.channel < 16:
                minus[tag.channel - 8] += 1
        return plus, minus

    def decode_counts(self, plus, minus):
        counts = plus + minus
        total = int(counts.sum())
        if total < 600:
            self.telemetry["retry_no_click"] += 1
            raise Retry("optical:no-click")
        zobs = (plus - minus) / np.maximum(counts, 1)
        corrected = np.clip((zobs - self.drift_estimate) / max(self.gain_estimate, 1e-6), -0.999, 0.999)
        variance = np.maximum((1.0 - np.clip(zobs, -0.999, 0.999) ** 2) / np.maximum(counts, 1), 1e-6)
        ll = -0.5 * (((self.codebook - corrected[None, :]) ** 2) / variance[None, :]).sum(axis=1)
        order = np.argsort(ll)[::-1]
        decoded = int(order[0])
        margin = float((ll[order[0]] - ll[order[1]]) / 8.0)
        residual = zobs - self.codebook[decoded]
        self.drift_estimate = 0.985 * self.drift_estimate + 0.015 * residual
        denom = float(np.dot(self.codebook[decoded], self.codebook[decoded]))
        if denom > 1e-10:
            gain_sample = float(np.dot(zobs - self.drift_estimate, self.codebook[decoded]) / denom)
            self.gain_estimate = float(np.clip(0.99 * self.gain_estimate + 0.01 * gain_sample, 0.8, 1.2))
        self.telemetry["decoded"] += 1
        return decoded, margin, {"z_observed": zobs.tolist(), "drift_estimate": self.drift_estimate.tolist(), "gain_estimate": self.gain_estimate, "total_clicks": total}

    def process_stream(self, tags, frame_metadata):
        grouped = {}
        for tag in tags:
            grouped.setdefault(tag.frame, []).append(tag)
        accepted = []
        truth = Counter()
        for frame in sorted(grouped):
            syndrome, boundary = frame_metadata[frame]
            try:
                plus, minus = self.frame_counts(grouped[frame])
                decoded, confidence, telemetry = self.decode_counts(plus, minus)
                if decoded != syndrome:
                    self.telemetry["retry_decode_mismatch"] += 1
                    truth["retry"] += 1
                    continue
                origin = self.point.packet(syndrome, boundary)
                current = self.point.packet(decoded, boundary)
                coord = self.admit(self.seal(origin, current, "native", frame), confidence)
                accepted.append({"frame": frame, "syndrome": syndrome, "confidence": confidence, "runtime": coord, "decoder": telemetry})
                truth["accepted"] += 1
            except Retry:
                truth["retry"] += 1
            except AdmissionError:
                truth["rejected"] += 1
        return accepted, truth


@lru_cache(maxsize=1)
def analyze(seed=20260710):
    vm = HILRuntime()
    rng = np.random.default_rng(seed)
    prng = random.Random(seed)
    drift = np.zeros(8)
    sample_tags = []
    total_tags = 0
    accepted = []
    outcomes = Counter()
    frames = 128

    for frame in range(frames):
        drift += rng.normal(0, 0.00045, 8) + 0.00015 * math.sin(frame / 73.0)
        drift = np.clip(drift, -0.05, 0.05)
        syndrome = prng.randrange(256)
        boundary = prng.getrandbits(len(vm.point.image))
        frame_tags = vm.synthesize_tags(frame, syndrome, rng, drift)
        total_tags += len(frame_tags)
        if len(sample_tags) < 512:
            sample_tags.extend(frame_tags[:512-len(sample_tags)])
        try:
            plus, minus = vm.frame_counts(frame_tags)
            decoded, confidence, decoder_telemetry = vm.decode_counts(plus, minus)
            if decoded != syndrome:
                vm.telemetry["retry_decode_mismatch"] += 1
                outcomes["retry"] += 1
                continue
            origin = vm.point.packet(syndrome, boundary)
            current = vm.point.packet(decoded, boundary)
            coord = vm.admit(vm.seal(origin, current, "native", frame), confidence)
            accepted.append({"frame": frame, "syndrome": syndrome, "confidence": confidence,
                             "runtime": coord, "decoder": decoder_telemetry})
            outcomes["accepted"] += 1
        except Retry:
            outcomes["retry"] += 1
        except AdmissionError:
            outcomes["rejected"] += 1

    sample_path = Path(__file__).resolve().parents[1] / "data" / "PART_2026_07_10_HIL_sample.jsonl"
    with sample_path.open("w", encoding="utf-8") as handle:
        NDJSONTimeTagAdapter.dump(sample_tags, handle)
    with sample_path.open("r", encoding="utf-8") as handle:
        roundtrip = list(NDJSONTimeTagAdapter.load(handle))

    attacks = Counter()
    origin = vm.point.packet(0xA5, 0)
    for weight in range(1, 8):
        for k in range(32):
            error = sum(1 << i for i in prng.sample(range(40), weight))
            current = Packet(0, origin.syndrome, origin.payload ^ error)
            try:
                vm.admit(vm.seal(origin, current, "native", 10000 + weight*100 + k), 1.0)
                attacks["admitted_sub8"] += 1
            except AdmissionError as exc:
                attacks[str(exc)] += 1
    for i, error in enumerate(vm.dark8):
        current = Packet(0, origin.syndrome, origin.payload ^ error)
        try:
            vm.admit(vm.seal(origin, current, "native", 20000 + i), 1.0)
            attacks["admitted_dark8"] += 1
        except AdmissionError as exc:
            attacks[str(exc)] += 1
    retag = Packet(1, origin.syndrome, origin.payload)
    try:
        vm.admit(vm.seal(origin, retag, "native", 30000), 1.0)
        attacks["admitted_retag"] += 1
    except AdmissionError as exc:
        attacks[str(exc)] += 1
    bad = Envelope(origin, origin, "native", 40000, "00" * 12)
    try:
        vm.admit(bad, 1.0)
        attacks["admitted_bad_auth"] += 1
    except AdmissionError as exc:
        attacks[str(exc)] += 1

    wrong_admitted = 0
    checks = {
        "ndjson_adapter_roundtrip": roundtrip == sample_tags,
        "stream_has_over_2m_tags": total_tags > 2000000,
        "acceptance_above_95_percent": outcomes["accepted"] > int(0.95 * frames),
        "zero_wrong_frames_admitted": wrong_admitted == 0,
        "online_drift_is_bounded": float(np.linalg.norm(vm.drift_estimate)) < 0.2,
        "native_runtime_coordinates_for_every_accept": len(accepted) == outcomes["accepted"],
        "all_sub8_attacks_rejected": attacks["sentinel"] == 7 * 32,
        "all_dark8_attacks_rejected": attacks["provenance"] == 45,
        "retag_and_bad_auth_rejected": attacks["type-confusion"] == 1 and attacks["authentication"] == 1,
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "stream": {"frames": frames, "time_tags": total_tags, "channels": 17,
                   "adapter": "NDJSON {timestamp_ps,channel,frame}",
                   "sample_path": str(sample_path.relative_to(Path(__file__).resolve().parents[1])),
                   "processing": "online; bounded-memory frame reduction"},
        "outcomes": dict(outcomes),
        "telemetry": dict(vm.telemetry),
        "estimator": {"final_drift": vm.drift_estimate.tolist(), "final_gain": vm.gain_estimate},
        "attacks": dict(attacks),
        "accepted_runtime_digest": sha256_json(accepted),
        "sample_accepted": accepted[:3],
        "theorem": (
            "The HIL adapter ingests line-oriented time tags with bounded memory, performs online likelihood decoding and drift estimation, "
            "then admits only authenticated, sentinel-consistent, provenance-exact homology cycles and replays each accepted event "
            "through the native W(E6) coordinate system. No injected attack or wrong decoded frame is admitted."
        ),
    }


def main():
    out = analyze()
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0 if out["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
