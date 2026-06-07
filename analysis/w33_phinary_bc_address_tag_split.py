#!/usr/bin/env python3
"""BT502: Phinary BC Address/Tag Split.

Finite address: t mod 30.
Irrational tag: t*acos(-2/3) mod 2pi.
Counter tag: -t*acos(-2/3) mod 2pi.
Relative tag: 2*t*acos(-2/3) mod 2pi.

The address repeats every 30 steps, but the phase tags do not repeat because
acos(-2/3)/pi is irrational.  This gives a finite address cycle with
nonperiodic orientation labels.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp

N = 30
SAMPLES = 300


def main() -> dict:
    allowed = {sp.Integer(-1), sp.Rational(-1, 2), sp.Integer(0), sp.Rational(1, 2), sp.Integer(1)}
    assert sp.Rational(-2, 3) not in allowed
    theta = math.acos(-2 / 3)
    phi = (1 + sp.sqrt(5)) / 2

    states = []
    for t in range(SAMPLES):
        states.append((
            t % N,
            round((t * theta) % (2 * math.pi), 14),
            round((-t * theta) % (2 * math.pi), 14),
            round((2 * t * theta) % (2 * math.pi), 14),
        ))
    assert len({s[0] for s in states}) == N
    assert len({s[1] for s in states}) == SAMPLES
    assert len({s[3] for s in states}) == SAMPLES
    assert len(states) == len(set(states))

    golden_tags = [sp.simplify(phi**t + phi**(-t)) for t in range(1, N + 1)]
    assert len(set(map(str, golden_tags))) == N
    lucas = [int(sp.lucas(t)) for t in range(0, 11)]
    assert {1, 2, 3, 7, 11}.issubset(set(lucas))

    lap_delta = (N * theta) % (2 * math.pi)
    rel_lap_delta = (2 * N * theta) % (2 * math.pi)
    assert abs(lap_delta) > 1e-12
    assert abs(rel_lap_delta) > 1e-12

    table = []
    for t in range(N):
        table.append({
            "t": t,
            "addr": t % N,
            "phase_deg": round(math.degrees((t * theta) % (2 * math.pi)), 10),
            "counter_deg": round(math.degrees((-t * theta) % (2 * math.pi)), 10),
            "relative_deg": round(math.degrees((2 * t * theta) % (2 * math.pi)), 10),
            "Lucas": int(sp.lucas(t)),
        })

    results = {
        "theorem": "BT502 Phinary BC Address/Tag Split",
        "address_layer": {"address": "t mod 30", "period": 30},
        "phase_layer": {
            "theta": "acos(-2/3)",
            "irrationality_reason": "-2/3 is not in the rational-cosine exceptional set {0, +/-1/2, +/-1}",
            "tag": "t*theta mod 2pi",
            "counter_tag": "-t*theta mod 2pi",
            "relative_tag": "2*t*theta mod 2pi",
            "one_lap_delta_degrees": round(math.degrees(lap_delta), 12),
            "one_lap_relative_delta_degrees": round(math.degrees(rel_lap_delta), 12),
        },
        "golden_layer": {
            "phi": "(1+sqrt(5))/2",
            "golden_tag": "phi^t + phi^-t",
            "first_30_golden_tags_unique": True,
            "Lucas_0_to_10": lucas,
            "Lucas_contains": [1, 2, 3, 7, 11],
        },
        "finite_check": {
            "samples": SAMPLES,
            "unique_addresses": N,
            "unique_phase_tags": SAMPLES,
            "unique_relative_tags": SAMPLES,
            "unique_combined_states": SAMPLES,
        },
        "first_ring_table": table,
        "interpretation": "finite 30-address cycle plus nonperiodic irrational phase tags; golden/Lucas tags give an exact symbolic coding layer",
    }
    out = Path("data/PART_BT502_PHINARY_BC_ADDRESS_TAG_SPLIT_results.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    return results

if __name__ == "__main__":
    main()
