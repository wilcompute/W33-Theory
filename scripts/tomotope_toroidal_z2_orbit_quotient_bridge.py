#!/usr/bin/env python3
"""Part DCXIV: Z2 orbit-quotient bridge via Burnside.

Uses the DCXIII swap involution to compute orbit quotients for:

1) oriented shell of size 42 (forward_1..21, backward_1..21),
2) weighted shell of size 168 (4 tagged copies per oriented channel).

For both actions, fixed points are zero, so Burnside gives:

  quotient_size = (|X| + |Fix(sigma)|)/2 = |X|/2.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
Z2_PATH = ROOT / "data" / "tomotope_toroidal_z2_swap_symmetry_bridge.json"
OUT_PATH = ROOT / "data" / "tomotope_toroidal_z2_orbit_quotient_bridge.json"


@dataclass(frozen=True)
class OrbitSummary:
    oriented_size: int
    oriented_fixed_points: int
    oriented_orbit_count: int
    weighted_size: int
    weighted_fixed_points: int
    weighted_orbit_count: int
    all_identities_hold: bool


def _sigma_oriented(label: tuple[str, int]) -> tuple[str, int]:
    direction, idx = label
    return ("backward", idx) if direction == "forward" else ("forward", idx)


def _sigma_weighted(label: tuple[str, int, int]) -> tuple[str, int, int]:
    direction, idx, slot = label
    return (("backward" if direction == "forward" else "forward"), idx, slot)


def _orbit_decomposition(elements: list[tuple], sigma) -> tuple[int, int]:
    universe = set(elements)
    fixed = sum(1 for x in elements if sigma(x) == x)

    seen: set[tuple] = set()
    orbit_count = 0
    for x in elements:
        if x in seen:
            continue
        y = sigma(x)
        seen.add(x)
        seen.add(y)
        orbit_count += 1

    # Defensive: ensure every element accounted for.
    if seen != universe:
        raise ValueError("Orbit decomposition incomplete")
    return fixed, orbit_count


def build_bridge() -> dict[str, Any]:
    z2 = json.loads(Z2_PATH.read_text(encoding="utf-8"))
    upstream_ok = bool(z2["summary"]["all_identities_hold"])

    oriented = [("forward", i) for i in range(1, 22)] + [("backward", i) for i in range(1, 22)]
    oriented_fixed, oriented_orbits = _orbit_decomposition(oriented, _sigma_oriented)

    weighted = [
        (direction, idx, slot)
        for direction in ["forward", "backward"]
        for idx in range(1, 22)
        for slot in range(1, 5)
    ]
    weighted_fixed, weighted_orbits = _orbit_decomposition(weighted, _sigma_weighted)

    identities = {
        "upstream_z2_identities_hold": upstream_ok,
        "oriented_size_is_42": len(oriented) == 42,
        "oriented_fixed_zero": oriented_fixed == 0,
        "oriented_orbit_count_21": oriented_orbits == 21,
        "oriented_burnside_exact": oriented_orbits == (len(oriented) + oriented_fixed) // 2,
        "weighted_size_is_168": len(weighted) == 168,
        "weighted_fixed_zero": weighted_fixed == 0,
        "weighted_orbit_count_84": weighted_orbits == 84,
        "weighted_burnside_exact": weighted_orbits == (len(weighted) + weighted_fixed) // 2,
    }

    summary = OrbitSummary(
        oriented_size=len(oriented),
        oriented_fixed_points=oriented_fixed,
        oriented_orbit_count=oriented_orbits,
        weighted_size=len(weighted),
        weighted_fixed_points=weighted_fixed,
        weighted_orbit_count=weighted_orbits,
        all_identities_hold=all(identities.values()),
    )

    return {
        "summary": asdict(summary),
        "identities": identities,
        "notes": (
            "DCXIV Burnside certificate: the Z2 swap has no fixed points on oriented "
            "or weighted shells, so quotients are exactly 42/2=21 and 168/2=84."
        ),
    }


def write_bridge(path: Path = OUT_PATH) -> Path:
    payload = build_bridge()
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def main() -> None:
    out = write_bridge()
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
