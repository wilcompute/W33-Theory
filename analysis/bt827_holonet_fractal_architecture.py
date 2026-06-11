#!/usr/bin/env python3
"""
BT827 - Photonic holonet fractal architecture.

BT826 identifies the single-core runtime:

    |Sp(4,3)| = 24 * 2160 = 24 * 45 * 48.

BT827 turns the paper's "universal computer = universal network" statement
into explicit engineering invariants for the recursive holonet:

    W^[0] = one photonic qutrit carrier,
    W^[n] = W(3,3) whose 40 sites are copies of W^[n-1].

The reversible transport plane has hierarchical routing diameter at most
8n for 40^n leaves: three in-chart Q3 XOR moves plus five chart-web
apartment hops per changed address digit.  Thus routing is O(log_40 N).

The persistent commit plane is different: it uses the Csaszar/tomotope
consensus ladder, with T(g)=4(7^g-1) ticks for level-g commits.  This
keeps fast reversible networking separate from slower durable memory writes.
"""
from __future__ import annotations

import json
from fractions import Fraction
from math import log, log2
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: str) -> dict:
    with (ROOT / path).open() as f:
        return json.load(f)


def holonet_instances(level: int, branching: int = 40) -> int:
    if level <= 0:
        return 0
    return (branching**level - 1) // (branching - 1)


def consensus_ticks(level: int) -> int:
    if level == 0:
        return 1
    return 4 * (7**level - 1)


def main() -> None:
    bt826 = load_json("data/bt826_photonic_mirror_middleware.json")

    q = 3
    lam = 2
    mu = 4
    v = 40
    k = 12
    undirected_edges = v * k // 2
    directed_edges = 2 * undirected_edges
    logical_st_slots = q**4
    magic_rays = 36
    contexts = 40
    chart_count = 540
    apartment_links = 1620
    chart_web_diameter = 5
    cube_diameter = 3
    digit_route_bound = chart_web_diameter + cube_diameter
    mirror_slots = bt826["factorization"]["mirror_slots"]
    runtime_order = bt826["factorization"]["sp_order"]
    tomotope_blocks = bt826["factorization"]["tomotope_middle_blocks"]
    polar_geography = bt826["factorization"]["polar_pair_geography"]
    full_slot_lift = bt826["factorization"]["full_slot_stabilizer"]

    checks = {
        "w33_edges_are_240": undirected_edges == 240,
        "directed_edges_are_480": directed_edges == 480,
        "steinberg_slots_are_q4": logical_st_slots == 81,
        "mirror_bus_factorizations": mirror_slots == 540 * 4 == 240 * 9 == 40 * 54 == 45 * 48,
        "runtime_factorization": runtime_order == 24 * mirror_slots == 24 * 45 * 48,
        "bt826_factors_match": (
            full_slot_lift == 24 and polar_geography == 45 and tomotope_blocks == 48
        ),
        "digit_route_bound_is_cube_plus_chart": digit_route_bound == 8,
        "minimal_turing_signature_is_substrate": (lam, q) == (2, 3),
        "classical_record_near_64_bits": 63 < v * log2(q) < 64,
        "edge_code_rate": Fraction(logical_st_slots, undirected_edges) == Fraction(27, 80),
    }

    levels = []
    for n in range(1, 7):
        instances = holonet_instances(n, v)
        leaves = v**n
        reversible_bound = digit_route_bound * n
        levels.append(
            {
                "level": n,
                "leaf_photonic_cores": leaves,
                "w33_instances_total": instances,
                "edge_qutrit_slots_total": undirected_edges * instances,
                "directed_transport_slots_total": directed_edges * instances,
                "chart_routers_total": chart_count * instances,
                "apartment_links_total": apartment_links * instances,
                "mirror_slots_total": mirror_slots * instances,
                "local_clifford_runtime_atoms_total": runtime_order * instances,
                "magic_rays_at_leaves": magic_rays * leaves,
                "contexts_at_leaves": contexts * leaves,
                "reversible_route_hops_bound": reversible_bound,
                "reversible_route_bound_formula": "8*n = 8*log_40(N)",
                "persistent_commit_ticks": consensus_ticks(n),
            }
        )
        assert reversible_bound == digit_route_bound * n
        assert reversible_bound == digit_route_bound * round(log(leaves, v))

    architecture_layers = [
        {
            "layer": "L0 photonic carrier",
            "object": "one self-entangled qutrit photon",
            "function": "operand state, Choi gate state, two-trit feedforward record",
        },
        {
            "layer": "L1 W33 data plane",
            "object": "40 points, 240 edges, 40 contexts",
            "function": "state/operator geometry; edge-code memory and entanglement links",
        },
        {
            "layer": "L2 Q3 chart routers",
            "object": "540 cube charts with 3-bit XOR addresses",
            "function": "local dimension-order routing and register moves",
        },
        {
            "layer": "L3 building fabric",
            "object": "1620 apartment links, chart-web diameter 5",
            "function": "global inter-chart routing",
        },
        {
            "layer": "L4 mirror middleware",
            "object": "2160 D12 chart-transversal/antipode slots",
            "function": "transport bus distinct from the C12 phase clock",
        },
        {
            "layer": "L5 tomotope packet",
            "object": "48 local edge-face blocks, 192 flags",
            "function": "local packet format for durable mirror transport",
        },
        {
            "layer": "L6 Clifford runtime",
            "object": "24 x 45 x 48 = 51840",
            "function": "complete optical two-qutrit Clifford control",
        },
    ]

    out = {
        "theorem": "BT827 photonic holonet fractal architecture",
        "single_core": {
            "w33_points": v,
            "w33_edges": undirected_edges,
            "directed_edges": directed_edges,
            "contexts": contexts,
            "steinberg_slots": logical_st_slots,
            "edge_code_rate": "27/80",
            "magic_rays": magic_rays,
            "charts": chart_count,
            "apartments": apartment_links,
            "mirror_slots": mirror_slots,
            "tomotope_middle_blocks": tomotope_blocks,
            "runtime_order": runtime_order,
            "runtime_factorization": "24 * 2160 = 24 * 45 * 48",
        },
        "architecture_layers": architecture_layers,
        "fractal_scaling": {
            "definition": "W^[0]=photon qutrit; W^[n]=W(3,3) with 40 copies of W^[n-1]",
            "leaf_cores": "40^n",
            "w33_instances_total": "(40^n - 1) / 39",
            "reversible_route_bound": "8n = 8 log_40(N)",
            "digit_route_bound_components": {
                "Q3_xor_diameter": cube_diameter,
                "chart_web_apartment_diameter": chart_web_diameter,
                "sum": digit_route_bound,
            },
            "persistent_commit_ticks": "T(0)=1, T(g)=4(7^g-1) for g>=1",
            "levels": levels,
        },
        "universal_computation": {
            "minimal_classical_signature": "lambda states, q symbols = (2,3)",
            "boundary": "Wolfram-Smith (2,3) machine is a weak-universality/minimality benchmark, not the paper's only universality proof",
            "quantum_universality": "BT825 Clifford completeness + BT822/BT823 magic/contextuality",
            "network_universality": "routing words are Clifford/control words because chart XOR moves and mirror slots are register operations",
            "classical_record_bits": v * log2(q),
        },
        "checks": checks,
    }

    for name, ok in checks.items():
        if not ok:
            raise AssertionError(f"BT827 check failed: {name}")

    path = ROOT / "data" / "bt827_holonet_fractal_architecture.json"
    with path.open("w") as f:
        json.dump(out, f, indent=2)

    print(json.dumps(out, indent=2))
    print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
