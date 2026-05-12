#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
from math import gcd
import json


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def phase_state(h: int) -> tuple[int, int, int]:
    return (3 * h % 12, -2 * h % 12, h % 7)


@dataclass(frozen=True)
class FullPhaseSuperperiod:
    local_transport_period: int
    face_decimal_period: int
    fano_period: int
    full_period: int
    euler_drift: int
    fano_automorphism_order: int
    subperiod_28: int
    subperiod_euler_drift_56: int
    checks: dict[str, bool]


def build() -> FullPhaseSuperperiod:
    local_transport_period = 12 // gcd(12, 3)
    face_decimal_period = 12 // gcd(12, 2)
    fano_period = 7
    full_period = lcm(lcm(local_transport_period, face_decimal_period), fano_period)
    euler_drift = -2 * full_period
    fano_aut = (8 - 1) * (8 - 2) * (8 - 4)
    sub28 = local_transport_period * fano_period
    sub56 = -2 * sub28
    checks = {
        "local_transport_period_4": local_transport_period == 4,
        "face_decimal_period_6": face_decimal_period == 6,
        "fano_period_7": fano_period == 7,
        "full_period_84": full_period == 84,
        "euler_drift_minus168": euler_drift == -168,
        "fano_aut_order_168": fano_aut == 168,
        "state_period_84": phase_state(0) == phase_state(84) and all(phase_state(k) != phase_state(0) for k in range(1, 84)),
        "subperiod_28_56": sub28 == 28 and sub56 == -56,
    }
    return FullPhaseSuperperiod(
        local_transport_period=local_transport_period,
        face_decimal_period=face_decimal_period,
        fano_period=fano_period,
        full_period=full_period,
        euler_drift=euler_drift,
        fano_automorphism_order=fano_aut,
        subperiod_28=sub28,
        subperiod_euler_drift_56=sub56,
        checks=checks,
    )


def main() -> None:
    result = build()
    payload = asdict(result)
    payload["all_checks_pass"] = all(result.checks.values())
    print(json.dumps(payload, indent=2))
    assert payload["all_checks_pass"]


if __name__ == "__main__":
    main()
