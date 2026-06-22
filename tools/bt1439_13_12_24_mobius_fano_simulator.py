#!/usr/bin/env python3
"""BT1439: 13-12-24 Moebius/Fano simulator.

Otto's visible model has 13 half-turns and 12 slings directed to icosahedron
vertices.  The W33 lift tested here is:
  active bins = 12 slings * (13 phase ticks + 1 closure tick) = 168
  guard bins  = 12 slings * 2 orientations = 24
  total       = 192
This is a finite-bus simulator, not an electron derivation.
"""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1439_13_12_24_mobius_fano_simulator.json"


def icosa_vertices() -> list[tuple[float, float, float]]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    verts = []
    for s1 in (-1.0, 1.0):
        for s2 in (-1.0, 1.0):
            verts.append((0.0, s1, s2 * phi))
            verts.append((s1, s2 * phi, 0.0))
            verts.append((s1 * phi, 0.0, s2))
    # stable unique order
    return sorted(set(verts))


def dist2(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b))


def main() -> None:
    verts = icosa_vertices()
    distances = sorted({round(dist2(a, b), 12) for a, b in itertools.combinations(verts, 2)})
    edge_d2 = distances[0]
    edges = [(i, j) for i, j in itertools.combinations(range(len(verts)), 2) if abs(dist2(verts[i], verts[j]) - edge_d2) < 1e-9]
    degrees = {i: 0 for i in range(len(verts))}
    for i, j in edges:
        degrees[i] += 1
        degrees[j] += 1

    half_turns = 13
    slings = 12
    active_bins = []
    for sling in range(slings):
        for phase in range(half_turns):
            active_bins.append({"bin": len(active_bins), "sling": sling, "vertex": sling, "phase": phase, "kind": "half_turn_phase"})
        active_bins.append({"bin": len(active_bins), "sling": sling, "vertex": sling, "phase": "closure", "kind": "closure_tick"})
    guard_bins = [
        {"guard_bin": sling * 2 + orient, "sling": sling, "vertex": sling, "orientation": orient}
        for sling in range(slings)
        for orient in range(2)
    ]
    checks = {
        "icosahedron_has_12_vertices": len(verts) == 12,
        "icosahedron_has_30_edges": len(edges) == 30,
        "icosahedron_is_5_regular": sorted(degrees.values()) == [5] * 12,
        "half_turns_are_phi3": half_turns == 13,
        "slings_are_k": slings == 12,
        "active_bins_are_168": len(active_bins) == 168,
        "guard_bins_are_24": len(guard_bins) == 24,
        "total_bus_is_192": len(active_bins) + len(guard_bins) == 192,
        "active_formula_is_12_times_14": len(active_bins) == 12 * (13 + 1),
        "guard_formula_is_12_times_2": len(guard_bins) == 12 * 2,
    }
    result = {
        "bt": 1439,
        "title": "13-12-24 Moebius/Fano finite-bus simulator",
        "verified": all(checks.values()),
        "otto_visible_inputs": {"half_turns": 13, "slings": 12, "target_polyhedron": "regular icosahedron"},
        "w33_lift": {
            "Phi3": half_turns,
            "k": slings,
            "active_bins": len(active_bins),
            "guard_bins": len(guard_bins),
            "total_bus": len(active_bins) + len(guard_bins),
            "active_formula": "12 * (13 phase ticks + 1 closure tick) = 168",
            "guard_formula": "12 * 2 orientations = 24",
        },
        "icosahedron": {"vertices": verts, "edge_count": len(edges), "degree_profile": sorted(degrees.values())},
        "samples": {"active_first_16": active_bins[:16], "guard_all": guard_bins},
        "boundary": "This simulator proves a clean finite 13-12-24 bus lift. It does not prove Otto's electron model.",
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1439, "verified": result["verified"], "bus": result["w33_lift"]}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
