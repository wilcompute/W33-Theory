#!/usr/bin/env python3
"""Architecture atlas for the Holonet universality frontier.

This is a structured synthesis, not a hardware-performance ranking.  It keeps
distinct uses of the phrase "single photon" from being conflated.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/w33_20260924_photonic_universality_architecture_atlas.json"

architectures = [
    {
        "id": "ADQC_FLYING_QUTRIT_HEAD",
        "quantum_memory": "stationary qutrit nodes",
        "flying_resource": "one photonic qutrit ancilla active per interaction cycle",
        "fixed_quantum_primitive": "one ancilla-register entangler E_AR",
        "program_surface": "ancilla measurement basis + classical Pauli frame",
        "nonclifford_location": "programmed ancilla analyzer basis",
        "scaling": "register dimension grows by adding memory nodes, not photon modes",
        "fault_tolerance": "open physical problem for qutrit memory-photon interface/analyzer",
        "holonet_fit": "direct: qutrit Clifford, 81 Pauli frame, spread measurements, routing",
        "evidence": "exact gate algebra in companion 2026-09-24 producer + Proctor et al. 2017",
    },
    {
        "id": "SINGLE_PHOTON_NETWORK_BUS",
        "quantum_memory": "stationary cavity/matter nodes",
        "flying_resource": "single photon mediating interactions across selected nodes",
        "fixed_quantum_primitive": "node-dependent photon reflection/scattering",
        "program_surface": "routing / node selection / local controls",
        "nonclifford_location": "depends on node gate set; not supplied by routing alone",
        "scaling": "network nodes scale; photon is a bus and disentangles at gate end",
        "fault_tolerance": "interface loss/cooperativity/error model required",
        "holonet_fit": "strong routing interpretation; exact qutrit extension remains open",
        "evidence": "Cohen & Molmer, Phys. Rev. A 98, 030302(R) (2018), qubit nodes",
    },
    {
        "id": "FUSION_BASED_PHOTONICS",
        "quantum_memory": "short-lived photonic resource states / fusion network",
        "flying_resource": "many photons, constant-size resource blocks",
        "fixed_quantum_primitive": "resource-state generation + entangling fusion measurements",
        "program_surface": "fusion measurement bases and network boundaries",
        "nonclifford_location": "logical measurement program / encoded resource layer",
        "scaling": "fault-tolerant network scales through repeated constant-size blocks",
        "fault_tolerance": "native model includes loss/fusion failure thresholds",
        "holonet_fit": "candidate reinterpretation of spread/route microframes as fusion schedule",
        "evidence": "Bartolucci et al., Nature Communications 14, 912 (2023)",
    },
    {
        "id": "SINGLE_EMITTER_CLUSTER_FACTORY",
        "quantum_memory": "growing multidimensional photonic cluster state",
        "flying_resource": "many sequential photons emitted by one reusable matter node",
        "fixed_quantum_primitive": "emission + delayed feedback/reinteraction",
        "program_surface": "cluster measurement bases",
        "nonclifford_location": "MBQC measurement program",
        "scaling": "one emitter can generate a larger graph, but photon count grows",
        "fault_tolerance": "requires cluster-code threshold/loss analysis",
        "holonet_fit": "natural for temporal loop/feedback language, not literal one-photon memory",
        "evidence": "Ferreira et al., Nature Physics 20, 865-870 (2024)",
    },
    {
        "id": "LOOP_CV_TIME_BIN",
        "quantum_memory": "time-bin modes in a single spatial optical channel",
        "flying_resource": "optical modes/pulses; not restricted to one photon",
        "fixed_quantum_primitive": "nested-loop measurement-induced gate processor",
        "program_surface": "electrically programmable measurement/gate sequence",
        "nonclifford_location": "non-Gaussian gate/resource for full CV universality",
        "scaling": "arbitrary number of time-bin modes through component reuse",
        "fault_tolerance": "GKP-style encoding is the natural route",
        "holonet_fit": "very strong time-bin/loop hardware analogy; different carrier model",
        "evidence": "Takeda & Furusawa, Phys. Rev. Lett. 119, 120504 (2017)",
    },
    {
        "id": "ONE_PARTICLE_MODE_REGISTER",
        "quantum_memory": "orthogonal internal/path/time/frequency modes of one photon",
        "flying_resource": "the same one-particle Hilbert space",
        "fixed_quantum_primitive": "multiport unitary / quantum walk",
        "program_surface": "interferometer settings",
        "nonclifford_location": "arbitrary mode unitary if hardware supplies it",
        "scaling": "n logical qutrits require at least 3^n orthogonal modes",
        "fault_tolerance": "mode loss/crosstalk plus exponential mode count",
        "holonet_fit": "excellent finite-module demo; rejected as scalable memory substrate",
        "evidence": "dimension theorem; single-photon quantum-walk experiments are finite-register demonstrations",
    },
]

ids = [x["id"] for x in architectures]
assert len(ids) == len(set(ids)) == 6
assert architectures[-1]["scaling"].endswith("3^n orthogonal modes")
out = {
    "schema": "w33.20260924.photonic_universality_architecture_atlas.v1",
    "status": "PASS_PHOTONIC_UNIVERSALITY_ARCHITECTURE_SEPARATION",
    "architectures": architectures,
    "terminology_firewall": {
        "single_photon_register": "one photon carries data directly in its finite mode Hilbert space",
        "single_photon_bus": "one photon mediates gates between stationary memories",
        "single_photon_at_a_time": "successive detected ancillas may be distinct photons",
        "single_emitter": "one reusable matter node emits many photons",
        "single_spatial_mode": "many time bins/pulses share one optical path; not one photon",
    },
    "holonet_decision": {
        "discard": "single photon as the scalable tensor-product memory",
        "retain": [
            "single-photon qutrit as finite local processor/analyzer",
            "temporal/frequency/path routing",
            "81-state Pauli-frame controller",
            "spread/MUB measurement programs",
            "networked qutrit SUM and entanglement distribution",
        ],
        "new_primary_architecture": "ADQC_FLYING_QUTRIT_HEAD",
        "parallel_fault_tolerant_architecture": "FUSION_BASED_PHOTONICS",
        "parallel_continuous_variable_architecture": "LOOP_CV_TIME_BIN",
        "reason": (
            "The first relocates scale into quantum memories while preserving a single flying qutrit head; "
            "the others expose fault-tolerant photonic routes that do not depend on the same magic-injection story."
        ),
    },
    "cross_architecture_insight": (
        "Measurement is the common programmable boundary. ADQC, MBQC, fusion-based computation, "
        "and loop-based measurement-induced gates all move algorithmic variability away from a large "
        "menu of coherent two-body gates and toward measurement basis choice plus classical feed-forward."
    ),
    "boundary": (
        "This atlas separates resource models and records literature-supported capabilities. "
        "It does not prove that the Holonet hardware realizes any external architecture without "
        "an explicit optical/memory interface and fault model."
    ),
}
OUT.write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": out["status"], "architectures": ids}, indent=2))
