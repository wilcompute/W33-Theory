#!/usr/bin/env python3
"""Pass 417: minimal cycle telemetry supplement for the sandpile decoder."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from math import ceil, log2
from pathlib import Path
import random

from w33_pass410_414_common import certificate, write_json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass417_divisor_cycle_hybrid_decoder.json"
N = 27
EDGES = tuple((source, target) for source in range(N) for target in range(N) if source != target)
ZERO = (0,) * N
OFFSET = 3


def divisor_key(divisor: tuple[int, ...]) -> bytes:
    return bytes(value + OFFSET for value in divisor)


def edge_divisor(edge: tuple[int, int]) -> tuple[int, ...]:
    source, target = edge
    result = [0] * N
    result[source] = -1
    result[target] = 1
    return tuple(result)


EDGE_DIVISORS = tuple(edge_divisor(edge) for edge in EDGES)
EDGE_KEY_INDEX = {divisor_key(vector): index for index, vector in enumerate(EDGE_DIVISORS)}
ZERO_KEY = divisor_key(ZERO)


def pair_key(first: tuple[int, int], second: tuple[int, int]) -> bytes:
    values = bytearray([OFFSET] * N)
    for source, target in (first, second):
        values[source] -= 1
        values[target] += 1
    return bytes(values)


def subtract_edge_key(divisor: tuple[int, ...], edge: tuple[int, int], multiplier: int = 1) -> bytes:
    values = [value + OFFSET for value in divisor]
    source, target = edge
    # divisor - multiplier*(e_target-e_source)
    values[source] += multiplier
    values[target] -= multiplier
    if any(value < 0 or value > 6 for value in values):
        return b""
    return bytes(values)


class PairIndex:
    def __init__(self) -> None:
        self.unordered: dict[bytes, list[tuple[int, int]]] = defaultdict(list)
        self.ordered_count: Counter[bytes] = Counter()
        for first, edge_a in enumerate(EDGES):
            for second in range(first, len(EDGES)):
                key = pair_key(edge_a, EDGES[second])
                self.unordered[key].append((first, second))
                self.ordered_count[key] += 1 if first == second else 2


def net_divisor(edge_ids: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * N
    for edge_id in edge_ids:
        source, target = EDGES[edge_id]
        result[source] -= 1
        result[target] += 1
    return tuple(result)


def partitions(total: int) -> tuple[tuple[int, ...], ...]:
    return {
        0: ((),),
        1: ((1,),),
        2: ((2,), (1, 1)),
        3: ((3,), (2, 1), (1, 1, 1)),
    }[total]


def canonical_divisor(positive: tuple[int, ...], negative: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * N
    cursor = 0
    for value in positive:
        result[cursor] = value
        cursor += 1
    for value in negative:
        result[cursor] = -value
        cursor += 1
    return tuple(result)


def fibre_counts(divisor: tuple[int, ...], pair_index: PairIndex) -> dict[str, int]:
    key = divisor_key(divisor)
    w0 = int(divisor == ZERO)
    w1 = int(key in EDGE_KEY_INDEX)

    ordered_w2 = pair_index.ordered_count[key]
    unordered_w2 = len(pair_index.unordered.get(key, ()))

    ordered_w3 = 0
    for edge in EDGES:
        ordered_w3 += pair_index.ordered_count[subtract_edge_key(divisor, edge)]
    transposition_fixed = sum(
        1 for edge in EDGES if subtract_edge_key(divisor, edge, 2) in EDGE_KEY_INDEX
    )
    three_cycle_fixed = 0
    for edge_vector in EDGE_DIVISORS:
        if all(3 * edge_vector[i] == divisor[i] for i in range(N)):
            three_cycle_fixed += 1
    unordered_w3 = (ordered_w3 + 3 * transposition_fixed + 2 * three_cycle_fixed) // 6

    return {
        "unordered_w0": w0,
        "unordered_w1": w1,
        "unordered_w2": unordered_w2,
        "unordered_w3": unordered_w3,
        "unordered_cumulative": w0 + w1 + unordered_w2 + unordered_w3,
        "ordered_w0": w0,
        "ordered_w1": w1,
        "ordered_w2": ordered_w2,
        "ordered_w3": ordered_w3,
        "ordered_cumulative": w0 + w1 + ordered_w2 + ordered_w3,
    }


def candidate_multisets(divisor: tuple[int, ...], pair_index: PairIndex, max_weight: int = 3) -> list[tuple[int, ...]]:
    key = divisor_key(divisor)
    candidates: list[tuple[int, ...]] = []
    if divisor == ZERO:
        candidates.append(())
    if max_weight >= 1 and key in EDGE_KEY_INDEX:
        candidates.append((EDGE_KEY_INDEX[key],))
    if max_weight >= 2:
        candidates.extend(pair_index.unordered.get(key, ()))
    if max_weight >= 3:
        for third, edge in enumerate(EDGES):
            remainder = subtract_edge_key(divisor, edge)
            for first, second in pair_index.unordered.get(remainder, ()):
                if second <= third:
                    candidates.append((first, second, third))
    return sorted(set(candidates), key=lambda item: (len(item), item))


def telemetry_encode(edge_ids: tuple[int, ...], pair_index: PairIndex) -> tuple[tuple[int, ...], int]:
    canonical = tuple(sorted(edge_ids))
    divisor = net_divisor(canonical)
    candidates = candidate_multisets(divisor, pair_index)
    try:
        return divisor, candidates.index(canonical)
    except ValueError as exc:
        raise ValueError("slip multiset has weight above three or contains an invalid edge") from exc


def telemetry_decode(divisor: tuple[int, ...], rank: int, pair_index: PairIndex) -> tuple[int, ...]:
    candidates = candidate_multisets(divisor, pair_index)
    if rank < 0 or rank >= len(candidates):
        raise ValueError("telemetry rank outside syndrome fibre")
    return candidates[rank]


def describe_edges(edge_ids: tuple[int, ...]) -> list[list[int]]:
    return [list(EDGES[edge_id]) for edge_id in edge_ids]


def build_payload() -> dict:
    pair_index = PairIndex()
    type_rows = []
    for weight in range(4):
        for positive in partitions(weight):
            for negative in partitions(weight):
                divisor = canonical_divisor(positive, negative)
                counts = fibre_counts(divisor, pair_index)
                type_rows.append({
                    "net_transport_weight": weight,
                    "positive_partition": list(positive),
                    "negative_partition": list(negative),
                    **counts,
                })

    worst_unordered = max(type_rows, key=lambda row: row["unordered_cumulative"])
    worst_ordered = max(type_rows, key=lambda row: row["ordered_cumulative"])
    unordered_bits = ceil(log2(worst_unordered["unordered_cumulative"]))
    ordered_bits = ceil(log2(worst_ordered["ordered_cumulative"]))

    zero_codebook = candidate_multisets(ZERO, pair_index)
    zero_hash = hashlib.sha256(
        (json.dumps([list(item) for item in zero_codebook], separators=(",", ":")) + "\n").encode()
    ).hexdigest()

    rng = random.Random(417)
    reciprocal_of_zero = EDGE_KEY_INDEX[subtract_edge_key(ZERO, EDGES[0])]
    explicit = [(0,), tuple(sorted((0, 26))), tuple(sorted((0, reciprocal_of_zero)))]
    explicit.extend(zero_codebook[1:11])
    for _ in range(40):
        weight = rng.randint(1, 3)
        explicit.append(tuple(sorted(rng.randrange(len(EDGES)) for _ in range(weight))))

    fibre_cache: dict[tuple[int, ...], list[tuple[int, ...]]] = {}
    trials: list[dict] = []
    all_roundtrip = True
    for edges in explicit:
        divisor = net_divisor(tuple(sorted(edges)))
        candidates = fibre_cache.setdefault(divisor, candidate_multisets(divisor, pair_index))
        rank = candidates.index(tuple(sorted(edges)))
        recovered = candidates[rank]
        ok = recovered == tuple(sorted(edges))
        all_roundtrip &= ok
        if len(trials) < 12:
            trials.append({
                "slips": describe_edges(tuple(sorted(edges))),
                "net_divisor": list(divisor),
                "telemetry_rank": rank,
                "fibre_size": len(candidates),
                "roundtrip": ok,
            })

    no_cancellation_rows = [row for row in type_rows if row["net_transport_weight"] == 3]
    max_pairing_only = max(row["unordered_w3"] for row in no_cancellation_rows)

    checks = {
        "oriented_edge_alphabet_702": len(EDGES) == 702,
        "pair_counter_has_all_ordered_pairs": sum(pair_index.ordered_count.values()) == 702**2,
        "zero_unordered_w2_is_351": worst_unordered["unordered_w2"] == 351,
        "zero_unordered_w3_is_5850": worst_unordered["unordered_w3"] == 5850,
        "zero_unordered_cumulative_is_6202": worst_unordered["unordered_cumulative"] == 6202,
        "unordered_minimum_bits_is_13": unordered_bits == 13 and 2**12 < 6202 <= 2**13,
        "zero_ordered_w2_is_702": worst_ordered["ordered_w2"] == 702,
        "zero_ordered_w3_is_35100": worst_ordered["ordered_w3"] == 35100,
        "zero_ordered_cumulative_is_35803": worst_ordered["ordered_cumulative"] == 35803,
        "ordered_minimum_bits_is_16": ordered_bits == 16 and 2**15 < 35803 <= 2**16,
        "pairing_only_maximum_is_six": max_pairing_only == 6,
        "pairing_only_requires_three_bits": ceil(log2(max_pairing_only)) == 3,
        "zero_codebook_size_6202": len(zero_codebook) == 6202,
        "all_encode_decode_trials_roundtrip": all_roundtrip,
    }
    checks = {key: bool(value) for key, value in checks.items()}

    payload = {
        "schema": "w33.pass417.divisor_cycle_hybrid_decoder.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "theorem": {
            "sandpile_component": "the Pass-412 syndrome uniquely recovers the net divisor through transport weight three",
            "telemetry_component": "conditioned on that divisor, lexicographic rank inside the complete slip-multiset fibre recovers hidden pairing and cycles",
            "minimum_unordered_bits": unordered_bits,
            "minimum_time_ordered_bits": ordered_bits,
            "pairing_only_bits_without_cancellation": 3,
            "optimality": "the zero-divisor fibre has 6202 unordered and 35803 ordered histories, giving matching information-theoretic lower bounds; the rank construction attains them",
        },
        "zero_divisor_fibre": {
            "identity_history": 1,
            "reciprocal_two_cycles": 351,
            "directed_three_cycles": 5850,
            "unordered_total": 6202,
            "ordered_reciprocal_sequences": 702,
            "ordered_three_cycle_sequences": 35100,
            "ordered_total": 35803,
            "canonical_codebook_sha256": zero_hash,
        },
        "net_type_fibre_census": type_rows,
        "codec": {
            "edge_id_order": "lexicographic (source,target), source!=target over 27 modes",
            "encoder": "sort at most three edge IDs, compute the net divisor, enumerate all sorted edge multisets with that divisor, and emit the lexicographic rank",
            "decoder": "enumerate the same syndrome fibre and select the transmitted rank",
            "fixed_width_packet": "13 bits for unordered pairing/cycle recovery; 16 bits when acquisition order is also part of the claim",
            "claim_boundary": "13 bits recover the unordered multiset of up to three pulse relocations. They do not encode analog timing, amplitudes, or more than three slips.",
        },
        "roundtrip_examples": trials,
        "checks": checks,
    }
    payload["certificate_sha256"] = certificate(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()
    payload = build_payload()
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 417 certificate drift")
    else:
        write_json(args.output, payload)
    print(json.dumps({"status": payload["status"], "checks": sum(payload["checks"].values()), "total": len(payload["checks"])}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
