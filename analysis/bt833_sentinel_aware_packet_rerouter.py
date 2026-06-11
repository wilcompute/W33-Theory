#!/usr/bin/env python3
"""
BT833 - Sentinel-aware holonet packet rerouter.

BT829 gives exact sentinel energy for any touched W33 point set.  BT833 closes
the loop with the packet compiler: before committing, each digit route may add
up to two waypoint points chosen to reduce the g=15 sentinel energy.

This rerouting is charged to the durable commit phase, not to the BT827 fast
8n route bound.  The compiler can therefore trade reversible move count for a
lower sentinel activation while staying below the BT830 commit tick.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, permutations
import json
from pathlib import Path

from bt828_holonet_packet_compiler import compile_digit
from bt829_fault_sentinel_monitor import (
    build_adjacency,
    build_geometry,
    centered_norm,
    frac,
    sentinel_projector,
    subset_energy,
)
from bt830_two_phase_commit_clock import commit_ticks


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def path_cost(path: tuple[int, ...], depth: int) -> int:
    return sum(compile_digit(a, b, depth)["reversible_moves"] for a, b in zip(path, path[1:]))


def best_route_for_digit(src: int, dst: int, depth: int, projector, max_waypoints: int = 2) -> dict:
    candidates = []
    direct_path = (src, dst)
    direct_energy = subset_energy(projector, set(direct_path))
    direct_cost = path_cost(direct_path, depth)

    for count in range(max_waypoints + 1):
        if count == 0:
            waypoint_orders = [()]
        else:
            waypoint_orders = []
            for combo in combinations([p for p in range(40) if p not in (src, dst)], count):
                waypoint_orders.extend(permutations(combo))
        for waypoints in waypoint_orders:
            path = (src,) + tuple(waypoints) + (dst,)
            touched = set(path)
            energy = subset_energy(projector, touched)
            norm = centered_norm(40, touched)
            cost = path_cost(path, depth)
            candidates.append((energy, cost, path, norm))

    energy, cost, path, norm = min(candidates, key=lambda row: (row[0], row[1], row[2]))
    return {
        "depth": depth,
        "source_digit": src,
        "target_digit": dst,
        "direct_path": list(direct_path),
        "direct_moves": direct_cost,
        "direct_sentinel_energy": frac(direct_energy),
        "chosen_path": list(path),
        "waypoints": list(path[1:-1]),
        "rerouted_moves": cost,
        "extra_moves": cost - direct_cost,
        "rerouted_sentinel_energy": frac(energy),
        "rerouted_sentinel_fraction": frac(None if norm == 0 else energy / norm),
        "energy_delta": frac(direct_energy - energy),
        "strictly_reduces_sentinel": energy < direct_energy,
    }


def main() -> None:
    geom = build_geometry()
    projector = sentinel_projector(build_adjacency(geom))
    bt828 = load_json("data/bt828_holonet_packet_compiler.json")
    bt830 = load_json("data/bt830_two_phase_commit_clock.json")

    rerouted_programs = []
    for program in bt828["compiled_programs"]:
        digit_routes = [
            best_route_for_digit(row["source_digit"], row["target_digit"], row["depth"], projector)
            for row in program["digit_packets"]
        ]
        rerouted_moves = sum(row["rerouted_moves"] for row in digit_routes)
        direct_energy_total = sum(Fraction(row["direct_sentinel_energy"]) for row in digit_routes)
        rerouted_energy_total = sum(Fraction(row["rerouted_sentinel_energy"]) for row in digit_routes)
        commit = commit_ticks(program["level"])
        rerouted_programs.append({
            "program": program["program"],
            "level": program["level"],
            "direct_moves": program["reversible_moves"],
            "rerouted_moves": rerouted_moves,
            "extra_moves": rerouted_moves - program["reversible_moves"],
            "commit_ticks": commit,
            "fits_commit_phase": rerouted_moves < commit,
            "direct_sentinel_energy_total": frac(direct_energy_total),
            "rerouted_sentinel_energy_total": frac(rerouted_energy_total),
            "sentinel_energy_reduction": frac(direct_energy_total - rerouted_energy_total),
            "digit_routes": digit_routes,
        })

    checks = {
        "bt830_commit_clock_loaded": bt830["protocol"]["commit_phase"].startswith("commit only"),
        "every_digit_reduces_sentinel": all(
            route["strictly_reduces_sentinel"]
            for program in rerouted_programs
            for route in program["digit_routes"]
        ),
        "every_program_reduces_total_sentinel": all(
            Fraction(program["rerouted_sentinel_energy_total"]) < Fraction(program["direct_sentinel_energy_total"])
            for program in rerouted_programs
        ),
        "every_program_fits_commit_phase": all(program["fits_commit_phase"] for program in rerouted_programs),
        "some_reroute_uses_two_waypoints": any(
            len(route["waypoints"]) == 2
            for program in rerouted_programs
            for route in program["digit_routes"]
        ),
        "adjacent_pair_can_be_context_completed_to_zero": (
            best_route_for_digit(0, 1, 0, projector)["rerouted_sentinel_energy"] == "0"
        ),
        "nonedge_pair_drops_below_direct": (
            Fraction(best_route_for_digit(0, 39, 0, projector)["rerouted_sentinel_energy"]) < Fraction("5/6")
        ),
    }
    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT833 check failed: {name}")

    out = {
        "theorem": "BT833 sentinel-aware packet rerouter",
        "reroute_policy": {
            "sentinel": "BT829 g=15 projector energy",
            "search": "up to two W33 waypoint points per digit, minimizing energy then move count",
            "cost_model": "extra reversible moves are charged to the BT830 durable commit phase",
        },
        "rerouted_programs": rerouted_programs,
        "checks": checks,
    }
    path = ROOT / "data" / "bt833_sentinel_aware_packet_rerouter.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)
    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
