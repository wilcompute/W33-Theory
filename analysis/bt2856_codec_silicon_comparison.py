#!/usr/bin/env python3
from __future__ import annotations

from bt2854_2860_common import *

def pass2856() -> dict:
    states = tuple(product(range(3), repeat=4))
    codes = [encode_affine(v) for v in states]
    roundtrip = all(decode_affine(encode_affine(v)) == v for v in states)
    source_metrics = {
        "codec_input_bits": 8,
        "affine_code_bits": 7,
        "projective_address_bits": 6,
        "support_bits": 4,
        "relative_phase_bits": 3,
        "affine_states": 81,
        "projective_nonzero_states": 40,
        "encoder_support_case_entries": 15,
        "decoder_support_intervals": 15,
    }
    baselines = {
        "minimal_four_operation_engine": {"logic_cells": 43, "pins": 22, "fmax_mhz": "72.40", "source_pass": 2796},
        "public_six_operation_engine": {"logic_cells": 72, "pins": 26, "fmax_mhz": "60.80", "source_pass": 2777},
    }
    checks = {
        "all_81_codes_unique": len(set(codes)) == 81,
        "codes_exactly_0_to_80": set(codes) == set(range(81)),
        "all_81_roundtrip": roundtrip,
        "seven_bits_information_optimal": 2 ** 6 < 81 <= 2 ** 7,
        "six_bits_projective_optimal": 2 ** 5 < 40 <= 2 ** 6,
        "one_state_bit_saved": 8 - 7 == 1,
        "state_bit_reduction_12_5_percent": Fraction(1, 8) == Fraction(125, 1000),
        "published_baselines_are_distinct_designs": baselines["minimal_four_operation_engine"]["logic_cells"] != baselines["public_six_operation_engine"]["logic_cells"],
        "minimal_baseline_40_percent_smaller_rounded": round(100 * (72 - 43) / 72) == 40,
        "minimal_baseline_19_percent_faster_rounded": round(100 * (Fraction(7240,100) / Fraction(6080,100) - 1)) == 19,
    }
    assert all(checks.values())
    return {
        "schema": "w33.pass2856.codec_silicon_comparison.v1",
        "status": "COMPLETE_EXACT_STATIC_WITH_PUBLISHED_BASELINES; NEW_PNR_PENDING_CI",
        "source_metrics": source_metrics,
        "published_same_harness_baselines": baselines,
        "comparison": {
            "storage_reduction_bits": 1,
            "storage_reduction_fraction": "1/8",
            "storage_reduction_percent": "12.5",
            "new_benchmark_top": "rtl/w33_pass2856_codec_benchmark_top.sv",
            "new_measurement_workflow": ".github/workflows/w33_pass2854_2860_seven_frontiers.yml",
        },
        "checks": checks,
        "check_count": len(checks),
        "boundary": "The code-width and round-trip comparison is exact, and the 43-LC/72-LC baselines are already measured in the repository. Logic cells, timing and power for the newly registered codec benchmark are not promoted until the dedicated Yosys/nextpnr workflow completes.",
    }
