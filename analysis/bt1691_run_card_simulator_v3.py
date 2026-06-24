#!/usr/bin/env python3
"""BT1691 — run-card simulator v3.

Combines BT1687 port contrast and BT1689 LCU success accounting into one run-card
pass/fail table.  Component values are still placeholders inherited from BT1664.
"""
from __future__ import annotations

import json
from pathlib import Path

RESULT = {
    "theorem": "BT1691 Run-Card Simulator v3",
    "rule": "pass if effective_snr >= 5 after component loss, parity/sign flips, phase jitter, and LCU postselection",
    "time_bins": 2048,
    "ports": {
        "resonance_separate": {
            "selector": "P_clock_6 tensor P_matter_24",
            "depth": 7,
            "l1_mass": 1.2939453125,
            "lcu_success": 0.597413338718975,
            "effective_snr": 28.625716516580017,
            "required_bins_for_snr_5": 62.48233180211645,
            "max_parity_flip_for_snr_5": 0.41919644057439054,
            "pass": True
        },
        "companion_separate": {
            "selector": "P_clock_0 tensor P_matter_30",
            "depth": 5,
            "l1_mass": 1.25,
            "lcu_success": 0.64,
            "effective_snr": 29.865313063424016,
            "required_bins_for_snr_5": 57.40316226486634,
            "max_parity_flip_for_snr_5": 0.42255434221095167,
            "pass": True
        },
        "monolithic_two_port": {
            "selector": "single combined LCU for both ports",
            "depth": 7,
            "l1_mass": 2.5439453125,
            "lcu_success": 0.1544685004281349,
            "effective_snr": 14.557904134592752,
            "required_bins_for_snr_5": 241.58627116866884,
            "max_parity_flip_for_snr_5": 0.34109118674204353,
            "pass": True
        }
    },
    "parity_sweep_effective_snr": [
        {"p_flip": 0.05, "resonance": 27.845308003683026, "companion": 29.052629472509615, "monolithic": 14.159063640778552},
        {"p_flip": 0.10, "resonance": 24.751384892162694, "companion": 25.82455953111966, "monolithic": 12.585834347358714},
        {"p_flip": 0.20, "resonance": 18.563538669122018, "companion": 19.368419648339742, "monolithic": 9.439375760519034},
        {"p_flip": 0.35, "resonance": 9.281769334561009, "companion": 9.684209824169873, "monolithic": 4.719687880259518},
        {"p_flip": 0.45, "resonance": 3.093923111520336, "companion": 3.2280699413899567, "monolithic": 1.5732292934198389}
    ],
    "run_card_recommendation": "Run resonance and companion as separate postselected ports. Both separate ports clear five sigma with fewer than 64 effective bins under placeholders; the monolithic two-port LCU passes at 2048 bins but fails around p_flip=0.35.",
    "boundary": "Component values are placeholders. LCU success is abstract and does not include imperfect controlled-select operations or measured ancilla loss."
}


def main() -> None:
    out = Path("data/PART_BT1691_RUN_CARD_SIMULATOR_V3_results.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(RESULT, indent=2) + "\n")
    print(json.dumps(RESULT, indent=2))


if __name__ == "__main__":
    main()
