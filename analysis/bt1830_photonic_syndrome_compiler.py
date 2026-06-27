#!/usr/bin/env python3
"""
BT1830 -- Photonic Syndrome Compiler.

BT1828 realizes P,G,E,C as commuting finite syndrome Hamiltonians.  BT1829
shows how the C term behaves dynamically under phase slips.  This compiler
lowers the four terms into an explicit component grammar for a photonic
time-bin/OAM/path implementation.

The compiler is intentionally finite and conservative: it emits a JSON
intermediate representation (IR), validates register arities and term coverage,
and constructs the bipartite factor graph linking registers to syndrome checks.
"""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1830_photonic_syndrome_compiler.json"


def build_ir() -> dict:
    registers = {
        "S0": {"kind": "qutrit_path", "levels": 3, "role": "strand coordinate 0"},
        "S1": {"kind": "qutrit_path", "levels": 3, "role": "strand coordinate 1"},
        "S2": {"kind": "qutrit_path", "levels": 3, "role": "strand coordinate 2"},
        "Q0": {"kind": "D4_glue_quartet", "levels": 4, "bits": 2, "role": "quartet coordinate 0"},
        "Q1": {"kind": "D4_glue_quartet", "levels": 4, "bits": 2, "role": "quartet coordinate 1"},
        "Q2": {"kind": "D4_glue_quartet", "levels": 4, "bits": 2, "role": "quartet coordinate 2"},
        "R": {"kind": "C12_ring", "levels": 12, "role": "clock/winding readout"},
    }
    terms = {
        "P0": {
            "operator": "strand mismatch projector",
            "registers": ["S0"],
            "implementation": "qutrit sorter + target-bin dark/bright comparator",
            "term": "1[S0 != i]",
        },
        "P1": {
            "operator": "strand mismatch projector",
            "registers": ["S1"],
            "implementation": "qutrit sorter + target-bin dark/bright comparator",
            "term": "1[S1 != j]",
        },
        "P2": {
            "operator": "strand mismatch projector",
            "registers": ["S2"],
            "implementation": "qutrit sorter + target-bin dark/bright comparator",
            "term": "1[S2 != s]",
        },
        "G0": {
            "operator": "D4 glue parity high bit",
            "registers": ["Q0", "Q1", "Q2"],
            "implementation": "two-bit XOR parity ancilla, compare with chi_high(T)",
            "term": "bit1(Q0 xor Q1 xor Q2 xor chi)",
        },
        "G1": {
            "operator": "D4 glue parity low bit",
            "registers": ["Q0", "Q1", "Q2"],
            "implementation": "two-bit XOR parity ancilla, compare with chi_low(T)",
            "term": "bit0(Q0 xor Q1 xor Q2 xor chi)",
        },
        "E01": {
            "operator": "K4 edge energy",
            "registers": ["Q0", "Q1"],
            "implementation": "quartet equality interferometer; bright if Q0 != Q1",
            "term": "1[Q0 != Q1]",
        },
        "E12": {
            "operator": "K4 edge energy",
            "registers": ["Q1", "Q2"],
            "implementation": "quartet equality interferometer; bright if Q1 != Q2",
            "term": "1[Q1 != Q2]",
        },
        "E20": {
            "operator": "K4 edge energy",
            "registers": ["Q2", "Q0"],
            "implementation": "quartet equality interferometer; bright if Q2 != Q0",
            "term": "1[Q2 != Q0]",
        },
        "Cwind": {
            "operator": "C12 winding syndrome",
            "registers": ["R"],
            "implementation": "12-bin ring interferometer / OAM winding readout",
            "term": "C/12",
        },
        "Cslip01": {
            "operator": "phase-slip collision guard",
            "registers": ["R"],
            "implementation": "coincidence/equality monitor for clock coordinates 0 and 1",
            "term": "1[x0=x1]",
        },
        "Cslip12": {
            "operator": "phase-slip collision guard",
            "registers": ["R"],
            "implementation": "coincidence/equality monitor for clock coordinates 1 and 2",
            "term": "1[x1=x2]",
        },
        "Cslip20": {
            "operator": "phase-slip collision guard",
            "registers": ["R"],
            "implementation": "coincidence/equality monitor for clock coordinates 2 and 0",
            "term": "1[x2=x0]",
        },
    }
    stages = [
        {
            "stage": "prepare",
            "description": "encode each local symbol x=4*strand+quartet into qutrit path S and D4 quartet Q; route ordered triple into the C12 ring R",
        },
        {
            "stage": "measure_P",
            "description": "read three qutrit mismatch projectors P0,P1,P2",
        },
        {
            "stage": "measure_G",
            "description": "compute two D4 parity ancillas G0,G1 from Q0,Q1,Q2 and table chi",
        },
        {
            "stage": "measure_E",
            "description": "read the three K4 equality-vs-edge comparators E01,E12,E20",
        },
        {
            "stage": "measure_C",
            "description": "read winding Cwind and collision guards Cslip01,Cslip12,Cslip20",
        },
        {
            "stage": "classical_decode",
            "description": "assemble H=(P0+P1+P2,G0+G1,E01+E12+E20,Cwind) and flag phase-slip events if any Cslip term fires",
        },
    ]
    return {"registers": registers, "terms": terms, "stages": stages}


def factor_graph(ir: dict) -> nx.Graph:
    graph = nx.Graph()
    for reg in ir["registers"]:
        graph.add_node(reg, bipartite="register")
    for term, spec in ir["terms"].items():
        graph.add_node(term, bipartite="term")
        for reg in spec["registers"]:
            graph.add_edge(term, reg)
    return graph


def main() -> int:
    ir = build_ir()
    graph = factor_graph(ir)

    register_degrees = {r: graph.degree(r) for r in ir["registers"]}
    term_degrees = {t: graph.degree(t) for t in ir["terms"]}

    coverage = {
        "P_terms": sorted([t for t in ir["terms"] if t.startswith("P")]),
        "G_terms": sorted([t for t in ir["terms"] if t.startswith("G")]),
        "E_terms": sorted([t for t in ir["terms"] if t.startswith("E")]),
        "C_terms": sorted([t for t in ir["terms"] if t.startswith("C")]),
    }

    checks = {
        "seven_registers": len(ir["registers"]) == 7,
        "three_qutrit_strand_registers": sum(1 for r in ir["registers"].values() if r["kind"] == "qutrit_path") == 3,
        "three_D4_quartet_registers": sum(1 for r in ir["registers"].values() if r["kind"] == "D4_glue_quartet") == 3,
        "one_C12_ring_register": sum(1 for r in ir["registers"].values() if r["kind"] == "C12_ring") == 1,
        "twelve_syndrome_terms": len(ir["terms"]) == 12,
        "P_has_three_projectors": len(coverage["P_terms"]) == 3,
        "G_has_two_parity_bits": len(coverage["G_terms"]) == 2,
        "E_has_three_K4_edges": len(coverage["E_terms"]) == 3,
        "C_has_winding_plus_three_guards": coverage["C_terms"] == ["Cslip01", "Cslip12", "Cslip20", "Cwind"],
        "factor_graph_is_bipartite": nx.is_bipartite(graph),
        "factor_graph_nodes": graph.number_of_nodes() == 19,
        "factor_graph_edges": graph.number_of_edges() == 19,
        "all_terms_have_registers": all(term_degrees[t] >= 1 for t in term_degrees),
        "all_registers_are_used": all(register_degrees[r] >= 1 for r in register_degrees),
        "six_compilation_stages": len(ir["stages"]) == 6,
    }

    payload = {
        "bt": "BT1830",
        "title": "Photonic Syndrome Compiler",
        "verified": all(checks.values()),
        "summary": (
            "The BT1828 commuting syndrome Hamiltonian is lowered into a finite photonic "
            "compiler IR.  The registers are three qutrit strand paths, three D4 quartet "
            "registers, and one C12 winding ring.  The terms are 3 P projectors, 2 G parity "
            "bits, 3 E K4 edge comparators, one C winding readout, and three phase-slip guards. "
            "The resulting bipartite factor graph has 19 nodes and 19 edges and covers every "
            "BT1824/BT1828 term."
        ),
        "ir": ir,
        "factor_graph": {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "register_degrees": register_degrees,
            "term_degrees": term_degrees,
            "coverage": coverage,
        },
        "resource_counts": {
            "qutrit_sorters": 3,
            "D4_quartet_registers": 3,
            "D4_parity_ancillas": 2,
            "K4_equality_interferometers": 3,
            "C12_ring_winding_readouts": 1,
            "phase_slip_collision_guards": 3,
            "classical_decoder_outputs": ["P", "G", "E", "C", "phase_slip_flag"],
        },
        "interpretation": (
            "This is a compiler boundary object: it turns the finite law into named optical "
            "syndrome components without claiming chip-level loss budgets or detector efficiencies."
        ),
        "boundary": (
            "BT1830 is an IR/compiler specification, not a fabricated hardware design.  The next "
            "step is to attach loss/noise parameters and compile each component to concrete beam "
            "splitter, delay, OAM, and detector primitives."
        ),
        "checks": checks,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True))
    print(json.dumps({"verified": payload["verified"], "resource_counts": payload["resource_counts"]}, indent=2))
    return 0 if payload["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
