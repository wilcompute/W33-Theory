#!/usr/bin/env python3
"""Pass 2920: separate support, phase, transcript, and implementation erasure costs.

The prior blueprint attached 8/3 bits to a "support readout" without specifying which
record was erased. These are distinct quantities:
  * H(frame | support) = 8/3 bits: phase information discarded by support projection;
  * H(support) = 4 log2(3) - 8/3 bits: entropy of the support outcome itself;
  * H(frame) = log2(81): minimum compressed exact transcript for identifying the frame;
  * 4(1 + 94/27) bits: naive reset cost if every raw four-bit adaptive snapshot is stored.
The script freezes the exact identities and their Landauer floors at 300 K.
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "PART_BT2920_ADAPTIVE_OBSERVER_INFORMATION_BUDGET_results.json"
CANONICAL = ROOT / "data" / "PART_BT2847_BT2853_PROTECTED_OBSERVER_NOISY_M36_results.json"
KB = 1.380649e-23
TEMPERATURE_K = 300.0
LN2 = math.log(2.0)


def support(state):
    return tuple(int(value != 0) for value in state)


def shannon_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities if p > 0)


def landauer(bits):
    return bits * KB * TEMPERATURE_K * LN2


def main() -> None:
    states = list(product(range(3), repeat=4))
    fibers = {}
    for state in states:
        fibers[support(state)] = fibers.get(support(state), 0) + 1
    fiber_histogram = {}
    for size in fibers.values(): fiber_histogram[size] = fiber_histogram.get(size, 0) + 1
    support_probabilities = [size / 81 for size in fibers.values()]
    frame_entropy = math.log2(81)
    support_entropy = shannon_entropy(support_probabilities)
    conditional_phase_entropy = sum((size / 81) * math.log2(size) for size in fibers.values())
    expected_support_weight = sum((size / 81) * sum(mask) for mask, size in fibers.items())
    adaptive_mean_operations = Fraction(94, 27)
    expected_snapshot_count = 1 + adaptive_mean_operations
    naive_raw_snapshot_bits = 4 * expected_snapshot_count
    compressed_transcript_bits = frame_entropy
    raw_to_compressed_ratio = float(naive_raw_snapshot_bits) / compressed_transcript_bits

    canonical_observer_check = None
    if CANONICAL.is_file():
        canonical = json.loads(CANONICAL.read_text(encoding="utf-8"))
        adaptive = canonical["pass2852_adaptive_observer"]
        canonical_observer_check = adaptive["uniform_mean_exact"] == "94/27" and adaptive["worst_case_operations"] == 4
        assert canonical_observer_check

    quantities = {
        "full_frame_entropy_bits": frame_entropy,
        "support_outcome_entropy_bits": support_entropy,
        "discarded_phase_entropy_bits": conditional_phase_entropy,
        "expected_support_weight": expected_support_weight,
        "adaptive_mean_operations": str(adaptive_mean_operations),
        "adaptive_expected_snapshots": str(expected_snapshot_count),
        "naive_raw_snapshot_reset_bits": str(naive_raw_snapshot_bits),
        "minimum_compressed_exact_transcript_bits": compressed_transcript_bits,
        "raw_to_compressed_reset_ratio": raw_to_compressed_ratio,
    }
    energies = {
        "full_frame_or_compressed_exact_transcript_J": landauer(frame_entropy),
        "support_outcome_record_J": landauer(support_entropy),
        "discarded_phase_given_support_J": landauer(conditional_phase_entropy),
        "naive_raw_adaptive_snapshots_J": landauer(float(naive_raw_snapshot_bits)),
    }
    checks = {
        "state_count_81": len(states) == 81,
        "support_count_16": len(fibers) == 16,
        "fiber_histogram_1_2_4_8_16": fiber_histogram == {1: 1, 2: 4, 4: 6, 8: 4, 16: 1},
        "phase_entropy_equals_8_over_3": abs(conditional_phase_entropy - 8 / 3) < 1e-12,
        "expected_support_weight_equals_8_over_3": abs(expected_support_weight - 8 / 3) < 1e-12,
        "entropy_chain_rule": abs(frame_entropy - support_entropy - conditional_phase_entropy) < 1e-12,
        "adaptive_snapshot_count_121_over_27": expected_snapshot_count == Fraction(121, 27),
        "naive_snapshot_bits_484_over_27": naive_raw_snapshot_bits == Fraction(484, 27),
        "canonical_observer_if_present": canonical_observer_check in (None, True),
    }
    assert all(checks.values()), [name for name, ok in checks.items() if not ok]
    result = {
        "schema": "w33.pass2920.adaptive_observer_information_budget.v1",
        "status": "COMPLETE_EXACT_INFORMATION_ACCOUNTING", "check_count": len(checks), "checks": checks,
        "fiber_histogram": {str(k): v for k, v in sorted(fiber_histogram.items())},
        "quantities": quantities, "landauer_300K": energies,
        "headline": "The former 8/3-bit 'support readout' number is specifically the conditional phase entropy H(frame|support), not the entropy of the support record and not the reset cost of an adaptive raw transcript.",
        "corrected_interpretation": {
            "phase_projection": "8/3 bits are lost when a full frame is replaced by its support mask",
            "support_record": "H(S)=4 log2(3)-8/3 bits for a uniform frame",
            "compressed_identification": "an exact full transcript needs log2(81) bits after optimal compression",
            "raw_implementation": "storing each four-bit adaptive snapshot costs 484/27 bits on average before compression",
        },
        "claim_boundary": "Landauer applies to logically irreversible erasure of the named representation; it is a lower bound, not a measured detector or CMOS energy.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS {len(checks)}/{len(checks)}"); print(result["headline"])
    for name, value in quantities.items(): print(f"  {name}: {value}")


if __name__ == "__main__":
    main()
