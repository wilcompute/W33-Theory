#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from collections import Counter


DEFAULT_ORBIT_SIZES = [72] + [27] * 6 + [1] * 6


@dataclass(frozen=True)
class WE6OrbitPhaseShell:
    orbit_sizes: list[int]
    orbit_size_counts: dict[str, int]
    carrier_size: int
    e6_root_shell: int
    matter_orbit_shell: int
    singleton_axis_shell: int
    phase_shell: int
    clock_sheets: dict[str, int]
    checks: dict[str, bool]


def load_orbit_sizes() -> list[int]:
    path = Path("artifacts/we6_orbits_on_e8_roots.json")
    if not path.exists():
        return DEFAULT_ORBIT_SIZES
    data = json.loads(path.read_text(encoding="utf-8"))
    return [int(x) for x in data.get("orbit_sizes", DEFAULT_ORBIT_SIZES)]


def build() -> WE6OrbitPhaseShell:
    orbit_sizes = sorted(load_orbit_sizes(), reverse=True)
    counts = Counter(orbit_sizes)
    carrier = sum(orbit_sizes)
    e6_root_shell = 72 if counts[72] == 1 else 0
    matter_orbit_shell = counts[27] * 27
    singleton_axis_shell = counts[1]
    phase_shell = matter_orbit_shell + singleton_axis_shell
    clock_sheets = {
        "carrier_240_over_12": carrier // 12,
        "e6_72_over_12": e6_root_shell // 12,
        "phase_168_over_12": phase_shell // 12,
    }
    checks = {
        "carrier_240": carrier == 240,
        "one_72_orbit": counts[72] == 1,
        "six_27_orbits": counts[27] == 6,
        "six_singletons": counts[1] == 6,
        "phase_shell_168": phase_shell == 168,
        "e6_plus_phase_240": e6_root_shell + phase_shell == 240,
        "matter_shell_162_is_81_plus_81": matter_orbit_shell == 162,
        "clock_sheets_20_6_14": clock_sheets == {
            "carrier_240_over_12": 20,
            "e6_72_over_12": 6,
            "phase_168_over_12": 14,
        },
    }
    return WE6OrbitPhaseShell(
        orbit_sizes=orbit_sizes,
        orbit_size_counts={str(k): v for k, v in sorted(counts.items(), reverse=True)},
        carrier_size=carrier,
        e6_root_shell=e6_root_shell,
        matter_orbit_shell=matter_orbit_shell,
        singleton_axis_shell=singleton_axis_shell,
        phase_shell=phase_shell,
        clock_sheets=clock_sheets,
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
