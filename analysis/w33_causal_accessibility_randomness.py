#!/usr/bin/env python3
"""Causal-accessibility version of observer-relative randomness.

The same finite timing model is used, but side information is attached to
spacetime events. An observer may condition only on events inside its past
light cone (c=1 units). This turns "has the key" into a causal-access question.
"""
from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "W33_CAUSAL_ACCESSIBILITY_RANDOMNESS.json"


def v2(n):
    k = 0
    while n and n % 2 == 0:
        n //= 2
        k += 1
    return k


def error_cell(z):
    return 2 * ((z & 1) + (z >> 1) - 1)


def observed(x, s0, s1):
    t0 = 3 + 2*v2(x + 1)
    t1 = 3 + 2*v2(x + 2)
    return (t0 + error_cell(s0), t1 + error_cell(s1))


def rows():
    out = []
    for x in range(8):
        for s0 in range(4):
            for s1 in range(4):
                out.append({"O": observed(x, s0, s1), "Y": x + 2, "S0": s0, "S1": s1})
    return out


EVENTS = {
    "Y": (0, 0),
    "S0": (1, -1),
    "S1": (1, 3),
}


def in_past(event, observer):
    te, xe = event
    to, xo = observer
    return te <= to and abs(xo - xe) <= to - te


def accessible(observer):
    return tuple(k for k, event in EVENTS.items() if in_past(event, observer))


def entropy(counter):
    total = sum(counter.values())
    return -sum((n/total)*math.log2(n/total) for n in counter.values() if n)


def conditional_entropy(sample, side):
    joint, marginal = Counter(), Counter()
    for row in sample:
        skey = tuple(row[s] for s in side)
        joint[(row["O"], skey)] += 1
        marginal[skey] += 1
    return entropy(joint) - entropy(marginal)


def verify():
    sample = rows()
    observers = [
        ("origin_t0", (0, 0)),
        ("center_t1", (1, 0)),
        ("center_t2", (2, 0)),
        ("center_t3", (3, 0)),
        ("center_t4", (4, 0)),
        ("right_t2", (2, 2)),
    ]
    result_rows = []
    for name, event in observers:
        side = accessible(event)
        result_rows.append({
            "observer": name,
            "event": {"t": event[0], "x": event[1]},
            "accessible_side_information": list(side),
            "H_O_given_past_light_cone_bits": conditional_entropy(sample, side),
        })
    by_name = {r["observer"]: r for r in result_rows}
    assert by_name["origin_t0"]["accessible_side_information"] == ["Y"]
    assert abs(by_name["origin_t0"]["H_O_given_past_light_cone_bits"] - 3.0) < 1e-12
    assert by_name["center_t2"]["accessible_side_information"] == ["Y", "S0"]
    assert abs(by_name["center_t2"]["H_O_given_past_light_cone_bits"] - 1.5) < 1e-12
    assert by_name["right_t2"]["accessible_side_information"] == ["Y", "S1"]
    assert abs(by_name["right_t2"]["H_O_given_past_light_cone_bits"] - 1.5) < 1e-12
    assert by_name["center_t4"]["accessible_side_information"] == ["Y", "S0", "S1"]
    assert by_name["center_t4"]["H_O_given_past_light_cone_bits"] == 0.0

    center = [by_name[f"center_t{t}"] for t in range(1, 5)]
    hs = [r["H_O_given_past_light_cone_bits"] for r in center]
    assert all(b <= a + 1e-12 for a, b in zip(hs, hs[1:]))

    return {
        "schema": "w33.causal-accessibility-randomness.v1",
        "status": "PASS",
        "c": 1,
        "side_information_events": {
            k: {"t": v[0], "x": v[1]} for k, v in EVENTS.items()
        },
        "observers": result_rows,
        "worldline_monotonicity": "PASS",
        "core_result": (
            "A globally retained seed need not be locally usable. Conditioning is restricted "
            "to J^-(observer): along x=0 the timing-record uncertainty falls from 3 to 1.5 "
            "to 0 bits only when the corresponding seed events enter the causal past."
        ),
        "same_time_observer_dependence": (
            "At t=2, x=0 has Y+S0 while x=2 has Y+S1. Both see 1.5 residual bits, "
            "but they possess different decrypting side information."
        ),
        "boundary": (
            "This is a finite 1+1D causal toy model, not a claim that physical horizons are "
            "cryptographic ciphers or that relativity creates fundamental randomness."
        ),
    }


if __name__ == "__main__":
    result = verify()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
