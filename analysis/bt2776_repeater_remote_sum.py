#!/usr/bin/env python3
"""Pass 2776: exact qutrit purification, erasure code, and repeater budget."""
from __future__ import annotations

import itertools
import json
import os
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def purify_fidelity(f: float) -> float:
    return (33 * f * f - 2 * f + 1) / (27 * f * f - 6 * f + 11)


def purify_success(f: float) -> float:
    return (27 * f * f - 6 * f + 11) / 32


def swap_fidelity(f: float) -> float:
    return f * f + (1 - f) ** 2 / 8


def isotropic_visibility(f: float) -> float:
    return (9 * f - 1) / 8


def from_visibility(v: float) -> float:
    return (1 + 8 * v) / 9


def apply_isotropic_operation(f: float, operation_visibility: float) -> float:
    return from_visibility(isotropic_visibility(f) * operation_visibility)


def memory_decay(f: float, time_s: float, coherence_s: float) -> float:
    return 1 / 9 + (f - 1 / 9) * math.exp(-time_s / coherence_s)


def logical_erasure_success(rail_success: float) -> float:
    return 3 * rail_success**2 - 2 * rail_success**3


def qutrit_codewords() -> dict[int, list[tuple[int, int, int]]]:
    return {s: [(r, (r + s) % 3, (r + 2 * s) % 3) for r in range(3)] for s in range(3)}


def verify_transversal_sum() -> bool:
    code = qutrit_codewords()
    for s, t in itertools.product(range(3), repeat=2):
        produced = {
            ((a[0] + b[0]) % 3, (a[1] + b[1]) % 3, (a[2] + b[2]) % 3)
            for a in code[s]
            for b in code[t]
        }
        expected = set(code[(s + t) % 3])
        if produced != expected:
            return False
    return True


def repeater_case(total_km: float, segments: int, purification_rounds: int, *, source_rate_hz: float,
                  source_fidelity: float, attenuation_db_per_km: float, coupling: float,
                  detector: float, local_transmission: float, memory_coherence_s: float,
                  swap_visibility: float, rail_availability: float) -> dict:
    segment_km = total_km / segments
    elementary_probability = 10 ** (-attenuation_db_per_km * segment_km / 10) * (coupling * detector * local_transmission) ** 2
    raw_rate = source_rate_hz * elementary_probability
    classical_one_way = segment_km / 200000.0
    f = source_fidelity
    rate = raw_rate
    for _ in range(purification_rounds):
        wait = (2 / max(rate, 1e-30)) + 2 * classical_one_way
        f = memory_decay(f, wait, memory_coherence_s)
        ps = purify_success(f)
        f = purify_fidelity(f)
        rate *= ps / 2
    elementary_fidelity = f
    levels = int(round(math.log2(segments)))
    assert 2**levels == segments
    for level in range(levels):
        rate /= 2
        wait = (2**level) * 2 * classical_one_way
        f = memory_decay(f, wait, memory_coherence_s)
        f = swap_fidelity(f)
        f = apply_isotropic_operation(f, swap_visibility)
        for _ in range(purification_rounds):
            wait_p = (2 / max(rate, 1e-30)) + 2 * (2**level) * classical_one_way
            f = memory_decay(f, wait_p, memory_coherence_s)
            ps = purify_success(f)
            f = purify_fidelity(f)
            rate *= ps / 2
    physical_end_rate = rate
    logical_success = logical_erasure_success(rail_availability)
    logical_remote_sum_rate = physical_end_rate * logical_success / 3
    return {
        "segments": segments,
        "segment_km": segment_km,
        "purification_rounds": purification_rounds,
        "elementary_link_probability": elementary_probability,
        "raw_elementary_rate_hz": raw_rate,
        "elementary_fidelity_after_purification": elementary_fidelity,
        "end_to_end_bell_fidelity": f,
        "physical_end_pair_rate_hz": physical_end_rate,
        "rail_availability": rail_availability,
        "logical_erasure_success": logical_success,
        "logical_remote_sum_rate_hz": logical_remote_sum_rate,
        "purifiable_after_distribution": f > 1 / 3,
    }


def build() -> dict:
    assert verify_transversal_sum()
    scenario = {
        "total_km": 600.0,
        "source_rate_hz": 8200.0,
        "source_fidelity": 0.806,
        "attenuation_db_per_km": 0.2,
        "coupling": 0.8,
        "detector": 0.8,
        "local_transmission": 0.7,
        "memory_coherence_s": 100.0,
        "swap_visibility": 0.99,
        "rail_availability": 0.9,
    }
    rows = [
        repeater_case(scenario["total_km"], segments, rounds, **{k: v for k, v in scenario.items() if k != "total_km"})
        for segments in (1, 2, 4, 8, 16, 32, 64)
        for rounds in range(4)
    ]
    feasible = [row for row in rows if row["end_to_end_bell_fidelity"] >= 0.6]
    best = max(feasible, key=lambda row: row["logical_remote_sum_rate_hz"]) if feasible else None
    f0 = scenario["source_fidelity"]
    max_wait = scenario["memory_coherence_s"] * math.log((9 * f0 - 1) / 2)
    return {
        "schema": "w33.pass2776.repeater_remote_sum.v1",
        "status": "EXACT_RECURRENCES_WITH_EXPLICIT_ENGINEERING_SCENARIO",
        "qutrit_purification": {
            "fidelity_map": "F'=(33F^2-2F+1)/(27F^2-6F+11)",
            "success_probability": "P=(27F^2-6F+11)/32",
            "fixed_points": ["1/9", "1/3", "1"],
            "distillation_region": "F>1/3",
        },
        "swapping": {"ideal_isotropic_map": "F_swap=F^2+(1-F)^2/8"},
        "memory": {
            "map": "F(t)=1/9+(F(0)-1/9) exp(-t/Tmem)",
            "maximum_wait_before_crossing_F=1/3_for_scenario_source_s": max_wait,
        },
        "outer_erasure_code": {
            "code": "[[3,1,2]]_3 polynomial/threshold secret-sharing code",
            "basis": "|s_L>=sum_r |r,r+s,r+2s>/sqrt(3)",
            "logical_success": "eta_L=3 eta^2-2 eta^3",
            "erasure_recursion": "e_L=3e^2-2e^3",
            "concatenation_threshold": "e<1/2 (eta>1/2)",
            "transversal_sum_verified": True,
        },
        "feed_forward": {
            "classical_payload_per_physical_remote_sum": "two trits",
            "logical_payload": "six trits for three rails before erasure recovery",
            "latency_model": "fiber propagation at 2e5 km/s plus controller latency",
        },
        "illustrative_scenario": scenario,
        "sweep": rows,
        "best_row_with_F_at_least_0_6": best,
        "rows_with_F_at_least_0_8": [row for row in rows if row["end_to_end_bell_fidelity"] >= 0.8],
        "threshold_packet": {
            "isotropic_entanglement_purification": "F>1/3",
            "heralded_erasure_concatenation": "rail erasure e<1/2",
            "memory_wait": "t<Tmem*ln((9F0-1)/2) to remain above F=1/3",
        },
        "boundary": (
            "The recurrence, swapping, memory, and erasure formulas are exact for the stated isotropic and independent-erasure models. "
            "The 600 km rate sweep is an engineering model, not an experimental repeater demonstration or a full queueing-theory optimum."
        ),
    }


def main() -> None:
    out = build()
    if os.environ.get("W33_EMIT_FULL_CERT") == "1":
        path = ROOT / "data" / "PART_BT2776_REPEATER_REMOTE_SUM.json"
        path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    summary = {
        "schema": out["schema"],
        "status": out["status"],
        "qutrit_purification": out["qutrit_purification"],
        "swapping": out["swapping"],
        "memory": out["memory"],
        "outer_erasure_code": out["outer_erasure_code"],
        "feed_forward": out["feed_forward"],
        "illustrative_scenario": out["illustrative_scenario"],
        "best_row_with_F_at_least_0_6": out["best_row_with_F_at_least_0_6"],
        "rows_with_F_at_least_0_8_count": len(out["rows_with_F_at_least_0_8"]),
        "threshold_packet": out["threshold_packet"],
        "boundary": out["boundary"],
    }
    path = ROOT / "data" / "PART_BT2776_REPEATER_REMOTE_SUM_summary.json"
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"best": summary["best_row_with_F_at_least_0_6"], "thresholds": summary["threshold_packet"]}, indent=2))


if __name__ == "__main__":
    main()
