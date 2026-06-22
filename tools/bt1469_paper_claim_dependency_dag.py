#!/usr/bin/env python3
"""BT1469: dependency DAG for exact, resonance, and blocked paper claims."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1469_paper_claim_dependency_dag.json"


def topo(nodes: list[str], edges: list[tuple[str, str]]) -> list[str]:
    incoming = {n: set() for n in nodes}
    outgoing = {n: set() for n in nodes}
    for a, b in edges:
        outgoing[a].add(b)
        incoming[b].add(a)
    ready = sorted([n for n in nodes if not incoming[n]])
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
    node_data = {
        "N0_szilassi_coordinates": {"tier": "exact_coordinate", "claim": "unique fixed Szilassi hexagon and C2 boundary shift"},
        "N1_closure_bus_arithmetic": {"tier": "exact_finite_arithmetic", "claim": "3*2*2=12, 2*12=24, 12*(13+1)=168"},
        "N2_frobenius_tau4": {"tier": "exact_finite_group", "claim": "tau4 fixes face 4 and gives 2+2+2+1"},
        "N3_s3_c3_classifier": {"tier": "exact_finite_group", "claim": "closure/shear layer is S3 x C3"},
        "N4_retwined_decoder": {"tier": "verified_finite_decoder", "claim": "closure rows obey retwined active/guard decoder contract"},
        "N5_closure_packet_abi": {"tier": "exact_runtime_abi", "claim": "ABI maps loop inputs to active/guard outputs and claim tier"},
        "N6_quartic_coefficient_bridge": {"tier": "numerical_structural_resonance", "claim": "4-phi^2=3+phi and square=13+phi^5 echoes closure arithmetic"},
        "N7_rounded_g_resonance": {"tier": "numerical_resonance", "claim": "visible rounded g value is numerically close to measured g"},
        "N8_formula_level_claims": {"tier": "blocked_pending_transcription", "claim": "Otto equations 49,50,64,65,66 require formula transcription"},
        "N9_real_world_model": {"tier": "speculative_not_imported", "claim": "external real-world particle interpretation is not imported"},
    }
    edges = [
        ("N0_szilassi_coordinates", "N1_closure_bus_arithmetic"),
        ("N0_szilassi_coordinates", "N2_frobenius_tau4"),
        ("N1_closure_bus_arithmetic", "N4_retwined_decoder"),
        ("N2_frobenius_tau4", "N3_s3_c3_classifier"),
        ("N3_s3_c3_classifier", "N4_retwined_decoder"),
        ("N4_retwined_decoder", "N5_closure_packet_abi"),
        ("N1_closure_bus_arithmetic", "N6_quartic_coefficient_bridge"),
        ("N6_quartic_coefficient_bridge", "N7_rounded_g_resonance"),
        ("N6_quartic_coefficient_bridge", "N8_formula_level_claims"),
        ("N8_formula_level_claims", "N9_real_world_model"),
    ]
    nodes = list(node_data.keys())
    order = topo(nodes, edges)
    exact_tiers = {"exact_coordinate", "exact_finite_arithmetic", "exact_finite_group", "verified_finite_decoder", "exact_runtime_abi"}
    blocked_tiers = {"blocked_pending_transcription", "speculative_not_imported"}
    exact_nodes = {n for n, d in node_data.items() if d["tier"] in exact_tiers}
    blocked_nodes = {n for n, d in node_data.items() if d["tier"] in blocked_tiers}
    unsafe_back_edges = [(a, b) for a, b in edges if a in blocked_nodes and b in exact_nodes]
    checks = {
        "dag_topologically_sorted": len(order) == len(nodes),
        "has_exact_root": order[0] == "N0_szilassi_coordinates",
        "no_blocked_to_exact_edges": len(unsafe_back_edges) == 0,
        "runtime_abi_depends_on_decoder": ("N4_retwined_decoder", "N5_closure_packet_abi") in edges,
        "real_world_model_is_terminal": all(a != "N9_real_world_model" for a, _ in edges),
        "formula_claims_precede_real_world_model": order.index("N8_formula_level_claims") < order.index("N9_real_world_model"),
    }
    result = {
        "bt": 1469,
        "title": "Paper-claim dependency DAG",
        "verified": all(checks.values()),
        "nodes": node_data,
        "edges": [{"from": a, "to": b} for a, b in edges],
        "topological_order": order,
        "firewall_rule": "Exact finite claims may feed runtime claims; resonance may point to blocked formula claims; blocked/speculative claims never support exact claims.",
        "unsafe_back_edges": unsafe_back_edges,
        "checks": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1469, "verified": result["verified"], "nodes": len(nodes), "edges": len(edges)}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
