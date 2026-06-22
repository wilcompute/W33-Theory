#!/usr/bin/env python3
"""BT1481: merge the E6 firewall closure square into the claim dependency DAG."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data" / "bt1469_paper_claim_dependency_dag.json"
OUT = ROOT / "data" / "bt1481_e6_firewall_claim_dag_merge.json"


def topo(nodes: dict, edges: list[dict]) -> list[str]:
    incoming = {n: set() for n in nodes}
    outgoing = {n: set() for n in nodes}
    for e in edges:
        outgoing[e["from"]].add(e["to"])
        incoming[e["to"]].add(e["from"])
    ready = sorted(n for n in nodes if not incoming[n])
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for m in sorted(outgoing[n]):
            incoming[m].remove(n)
            if not incoming[m]:
                ready.append(m)
                ready.sort()
    if len(order) != len(nodes):
        raise RuntimeError("cycle detected")
    return order


def main() -> None:
    base = json.loads(BASE.read_text(encoding="utf-8"))
    nodes = dict(base["nodes"])
    edges = list(base["edges"])
    extra_nodes = {
        "E0_e6_firewall_square": {"tier": "exact_finite_arithmetic", "claim": "E6 firewall square 36->72, 72+6=78, 72+9=81"},
        "E1_oriented_72_sector": {"tier": "exact_finite_arithmetic", "claim": "72 is both E6 oriented-root sector and ABI active/guard row count"},
        "E2_h1_81_closure": {"tier": "exact_finite_arithmetic", "claim": "81 is H1/CSS closure obtained by adjoining q^2=9 firewall sector to 72"},
        "E3_c3_v4_grid": {"tier": "exact_finite_structure", "claim": "12 closure strands form C3 x V4 with three channels and four triangles"},
    }
    nodes.update(extra_nodes)
    extra_edges = [
        {"from": "E0_e6_firewall_square", "to": "E1_oriented_72_sector"},
        {"from": "E1_oriented_72_sector", "to": "N4_retwined_decoder"},
        {"from": "E1_oriented_72_sector", "to": "E2_h1_81_closure"},
        {"from": "E2_h1_81_closure", "to": "N5_closure_packet_abi"},
        {"from": "E3_c3_v4_grid", "to": "N5_closure_packet_abi"},
        {"from": "N0_szilassi_coordinates", "to": "E3_c3_v4_grid"},
        {"from": "E0_e6_firewall_square", "to": "E3_c3_v4_grid"},
    ]
    edges.extend(extra_edges)
    order = topo(nodes, edges)
    blocked_tiers = {"blocked_pending_transcription", "speculative_not_imported"}
    exact_tiers = {"exact_coordinate", "exact_finite_arithmetic", "exact_finite_group", "verified_finite_decoder", "exact_runtime_abi", "exact_finite_structure"}
    unsafe = []
    for e in edges:
        if nodes[e["from"]]["tier"] in blocked_tiers and nodes[e["to"]]["tier"] in exact_tiers:
            unsafe.append(e)
    checks = {
        "base_verified": base.get("verified") is True,
        "node_count_increased_by_4": len(nodes) == len(base["nodes"]) + 4,
        "dag_topological": len(order) == len(nodes),
        "e6_square_upstream_of_decoder": order.index("E1_oriented_72_sector") < order.index("N4_retwined_decoder"),
        "h1_81_upstream_of_abi": order.index("E2_h1_81_closure") < order.index("N5_closure_packet_abi"),
        "grid_upstream_of_abi": order.index("E3_c3_v4_grid") < order.index("N5_closure_packet_abi"),
        "no_blocked_to_exact_edges": not unsafe,
    }
    result = {
        "bt": 1481,
        "title": "E6 firewall to claim-DAG merge",
        "verified": all(checks.values()),
        "nodes": nodes,
        "edges": edges,
        "topological_order": order,
        "added_nodes": extra_nodes,
        "added_edges": extra_edges,
        "firewall_rule": "E6 closure-square evidence may support exact finite ABI/CSS claims; blocked formula/physics claims still cannot support exact claims.",
        "unsafe_edges": unsafe,
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1481, "verified": result["verified"], "nodes": len(nodes)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
