#!/usr/bin/env python3
"""BT1687 — parity-routed QSVT hardware resource table v2."""
from __future__ import annotations

import json
import math
from pathlib import Path

PER_WALK = 0.99201699
ANALYZER = 0.98
DETECTOR = 0.85
BINS = 2048
PHASE_JITTER = 0.05
PARITY_FLIP = 0.05
DARK_PER_BIN = 1e-6


def snr(depth: int) -> float:
    survival = (PER_WALK ** depth) * ANALYZER * DETECTOR
    background = 1 - (1 - DARK_PER_BIN) ** BINS
    contrast = math.exp(-0.5 * PHASE_JITTER**2) * (1 - 2 * PARITY_FLIP) * (1 - background)
    return contrast * math.sqrt(BINS * survival)

RESULT = {
    "theorem": "BT1687 Hardware Resource Table v2",
    "architecture": "parity-routed LCU of Chebyshev-term QSP schedules",
    "component_defaults": {
        "per_walk_survival": PER_WALK,
        "analyzer_survival": ANALYZER,
        "detector_efficiency": DETECTOR,
        "time_bins": BINS,
        "phase_jitter_rms": PHASE_JITTER,
        "parity_flip_probability": PARITY_FLIP,
        "dark_count_probability_per_bin": DARK_PER_BIN
    },
    "selector_resources": {
        "P_clock_6": {
            "route": "e_c + o_c",
            "subsequences": 2,
            "chebyshev_terms": 4,
            "l1_mass": 1.0,
            "max_depth": 3,
            "needs_even_odd_sign_control": True
        },
        "P_clock_0": {
            "route": "e_c - o_c",
            "subsequences": 2,
            "chebyshev_terms": 4,
            "l1_mass": 1.0,
            "max_depth": 3,
            "needs_even_odd_sign_control": True
        },
        "P_matter_24": {
            "route": "certified even quartic p24",
            "subsequences": 1,
            "chebyshev_terms": 3,
            "l1_mass": 1.2939453125,
            "max_depth": 4,
            "needs_even_odd_sign_control": False
        },
        "P_matter_30": {
            "route": "e_30 + o_30",
            "subsequences": 2,
            "chebyshev_terms": 3,
            "l1_mass": 1.25,
            "max_depth": 2,
            "needs_even_odd_sign_control": True
        }
    },
    "two_port_resources": {
        "resonance": {
            "selector": "P_clock_6 tensor P_matter_24",
            "l1_mass": 1.2939453125,
            "subsequence_products": 2,
            "term_products": 12,
            "max_depth": 7,
            "estimated_snr": snr(7)
        },
        "companion": {
            "selector": "P_clock_0 tensor P_matter_30",
            "l1_mass": 1.25,
            "subsequence_products": 4,
            "term_products": 12,
            "max_depth": 5,
            "estimated_snr": snr(5)
        },
        "combined_l1_mass": 2.5439453125,
        "max_depth": 7,
        "time_bin_margin": 2041
    },
    "comparison_to_BT1661_monomial_minimal": {
        "BT1661_max_depth": 5,
        "BT1661_raw_combined_l1": 0.3958333333333333,
        "BT1673_block_encoded_best_l1": 334.6461794019932,
        "BT1687_parity_routed_logical_l1": 2.5439453125,
        "interpretation": "BT1687 has slightly greater max depth than the raw monomial compiler but avoids the huge block-encoding normalization blowup."
    },
    "boundary": "SNR estimates use BT1664 placeholder component defaults and treat LCU success/amplitude amplification separately from shot-noise port contrast. Real hardware needs calibrated component data and explicit ancilla success accounting."
}


def main() -> None:
    out = Path("data/PART_BT1687_HARDWARE_RESOURCE_TABLE_V2_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
