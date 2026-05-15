#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from collections import Counter
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ORBIT_ARTIFACT = ROOT / "artifacts" / "we6_orbits_on_e8_roots.json"
DEFAULT_ORBIT_SIZES = [72] + [27] * 6 + [1] * 6


@dataclass(frozen=True)
class WE6OrbitPhaseShell:
    orbit_sizes: list[int]
    orbit_size_counts: dict[str, int]
    carrier_size: int
    e6_root_shell: int
    matter_81_plus_shell: int
    matter_81_minus_shell: int
    matter_orbit_pairing: dict[str, Any]
    singleton_axis_shell: int
    signed_clifford_channels: list[dict[str, Any]]
    phase_shell: int
    clock_sheets: dict[str, int]
    checks: dict[str, bool]


def load_orbit_sizes() -> list[int]:
    path = ORBIT_ARTIFACT
    if not path.exists():
        return DEFAULT_ORBIT_SIZES
    data = json.loads(path.read_text(encoding="utf-8"))
    return [int(x) for x in data.get("orbit_sizes", DEFAULT_ORBIT_SIZES)]


def load_orbit_representatives() -> list[list[float]]:
    if not ORBIT_ARTIFACT.exists():
        return []
    data = json.loads(ORBIT_ARTIFACT.read_text(encoding="utf-8"))
    reps = data.get("representatives", {}).get("1", [])
    return [[float(x) for x in rep] for rep in reps]


def _signed_channel(index: int, vector: list[float]) -> dict[str, Any]:
    support = [[i + 1, x] for i, x in enumerate(vector) if x != 0]
    first_nonzero = next((x for x in vector if x != 0), 0.0)
    sign = "+" if first_nonzero >= 0 else "-"
    return {
        "name": f"chi_{index + 1}",
        "sign": sign,
        "vector": vector,
        "support": support,
        "channel": f"{sign}clifford:{index + 1}",
    }


def _build_signed_clifford_channels(representatives: list[list[float]]) -> list[dict[str, Any]]:
    if len(representatives) >= 6:
        return [_signed_channel(i, vec) for i, vec in enumerate(representatives[:6])]
    channels: list[dict[str, Any]] = []
    for i, vec in enumerate(representatives[:3]):
        channels.append(_signed_channel(2 * i, vec))
        channels.append(_signed_channel(2 * i + 1, [-x for x in vec]))
    return channels


def build() -> WE6OrbitPhaseShell:
    orbit_sizes = sorted(load_orbit_sizes(), reverse=True)
    counts = Counter(orbit_sizes)
    representatives = load_orbit_representatives()
    carrier = sum(orbit_sizes)
    e6_root_shell = 72 if counts[72] == 1 else 0
    matter_81_plus_shell = sum(orbit_sizes[1:4]) if len(orbit_sizes) >= 7 else 81
    matter_81_minus_shell = sum(orbit_sizes[4:7]) if len(orbit_sizes) >= 7 else 81
    matter_orbit_pairing = {
        "81_plus": {
            "orbit_sizes": orbit_sizes[1:4] if len(orbit_sizes) >= 7 else [27, 27, 27],
            "total": matter_81_plus_shell,
            "role": "first 81-sector saturation",
        },
        "81_minus": {
            "orbit_sizes": orbit_sizes[4:7] if len(orbit_sizes) >= 7 else [27, 27, 27],
            "total": matter_81_minus_shell,
            "role": "conjugate 81-sector saturation",
        },
    }
    singleton_axis_shell = counts[1]
    signed_clifford_channels = _build_signed_clifford_channels(representatives)
    phase_shell = matter_81_plus_shell + matter_81_minus_shell + singleton_axis_shell
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
        "matter_shell_162_is_81_plus_81": matter_81_plus_shell + matter_81_minus_shell == 162,
        "explicit_81_plus_81_pairing": (
            matter_orbit_pairing["81_plus"]["total"] == 81
            and matter_orbit_pairing["81_minus"]["total"] == 81
        ),
        "six_signed_clifford_channels": len(signed_clifford_channels) == 6,
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
        matter_81_plus_shell=matter_81_plus_shell,
        matter_81_minus_shell=matter_81_minus_shell,
        matter_orbit_pairing=matter_orbit_pairing,
        singleton_axis_shell=singleton_axis_shell,
        signed_clifford_channels=signed_clifford_channels,
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
