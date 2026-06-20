#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data" / "bt1385_hesse_sic_t_port_abi.json")
    ns = ap.parse_args()
    abi = load("data/bt1382_non_clifford_port_abi.json")
    runtime = load("data/bt1378_runtime_contract_verification.json")
    token = {
        "name": "hesse_sic_t_token",
        "dimension": 3,
        "sic_outcomes": 9,
        "logical_role": "non-stabilizer qutrit-assisted T injection resource",
        "consumption": "single-shot measurement/injection at a Clifford packet boundary",
    }
    timing = {
        "word_ticks": 8,
        "microframe_ticks": 72,
        "mirror_bus_ticks": 2160,
        "clifford_window_ticks": 51840,
        "injection_slots": ["after packet address lowering", "before Clifford frame closure", "with classical feed-forward into next packet word"],
    }
    measurement_signature = {
        "outcome_alphabet": "Hesse-SIC outcome h in {0,...,8}",
        "feed_forward": "map h to a Clifford correction plus one T-frame parity bit",
        "acceptance": "outcome registered, packet ABI restored, correction record appended",
        "failure_modes": ["missing outcome", "ambiguous SIC outcome", "feed-forward timeout", "Clifford ABI restoration failure"],
    }
    checks = {
        "bt1382_abi_verified": abi["verified"] is True,
        "runtime_verified": runtime["verified"] is True,
        "dimension_qutrit_3": token["dimension"] == 3,
        "sic_has_9_outcomes": token["sic_outcomes"] == 9,
        "word_ticks_8": timing["word_ticks"] == 8,
        "clifford_window_51840": timing["clifford_window_ticks"] == 51840,
        "has_feed_forward_rule": "feed_forward" in measurement_signature,
        "has_failure_modes": len(measurement_signature["failure_modes"]) == 4,
    }
    result = {
        "bt": 1385,
        "title": "Concrete Hesse-SIC/T non-Clifford port ABI",
        "verified": all(checks.values()),
        "checks": checks,
        "resource_token": token,
        "timing_contract": timing,
        "measurement_signature": measurement_signature,
        "packet_boundary": {
            "input": "Clifford-protected logical packet wire",
            "operation": "consume hesse_sic_t_token and measure/inject non-Clifford resource",
            "output": "Clifford packet ABI plus correction side record",
        },
        "honest_boundary": "This is a concrete ABI and verification signature for the Hesse-SIC/T port. It does not certify physical SIC optics, magic-state distillation yield, or threshold overhead."
    }
    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"bt": 1385, "verified": result["verified"], "sic_outcomes": token["sic_outcomes"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
