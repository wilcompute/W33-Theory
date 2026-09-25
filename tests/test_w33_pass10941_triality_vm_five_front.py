#!/usr/bin/env python3
"""Cross-front regression for the Pass 10941 triality VM packet."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    return json.loads((ROOT / "data" / name).read_text())


def rank_mod(A, p):
    A = A.copy() % p
    rank = 0
    for col in range(A.shape[1]):
        hits = np.flatnonzero(A[rank:, col])
        if not len(hits):
            continue
        pivot = rank + int(hits[0])
        A[[rank, pivot]] = A[[pivot, rank]]
        A[rank] = A[rank] * pow(int(A[rank, col]), -1, p) % p
        for row in np.flatnonzero(A[:, col]):
            if row != rank:
                A[row] = (A[row] - A[row, col] * A[rank]) % p
        rank += 1
    return rank


def test_five_front_contract():
    chart = load("w33_pass10941_rational_triality_coordinate_chart.json")
    vm = load("w33_pass10941_symplectic_vm_gate_compiler.json")
    uqc = load("w33_pass10941_qutrit_universal_instruction_bridge.json")
    lift = load("w33_pass10941_w90_integral_lift.json")
    ad = load("w33_pass10941_ramified_dual_ad.json")
    ham = load("w33_pass10941_normalized_root_hamiltonian.json")

    assert chart["fixed_presentation"]["jacobi_checks"] == 18**3
    assert chart["split_rational_nogo"]["trialitarian_centroid_nontrivial_idempotents"] == 0
    assert chart["split_rational_nogo"]["split_centroid_nontrivial_idempotents"] == 6

    assert {(p["local_Lie_closure_dimension"], p["connected_Lie_closure_dimension"])
            for p in vm["prime_packets"]} == {(57, 105)}
    assert vm["universality"]["universal_quantum_computation"] is False
    assert vm["universality"]["scope_of_false_flag"].startswith("bare Clifford")
    assert uqc["claim_lattice"]["bare_pass10941_vm_is_universal"] is False
    assert uqc["claim_lattice"]["ideal_nonstabilizer_analyzer_or_choi_port_closes_logical_universality"] is True
    assert uqc["claim_lattice"]["endogenous_fault_tolerant_magic_factory_is_proved"] is False
    lowering = uqc["seven_qutrit_clifford_lowering"]
    assert lowering["all_25_vm_generators_lowered_exactly_mod3"] is True
    assert len(lowering["lowerings"]) == 25
    assert lowering["maximum_clifford_macro_length"] == 7
    analyzer = uqc["nonclifford_resource_equivalence"]["programmed_analyzer"]
    assert [r["zeta9_exponents"] for r in analyzer["analyzer_vectors"]] == [
        [0, 8, 1], [0, 5, 4], [0, 2, 7]
    ]
    assert uqc["alternative_choi_injection"]["maximum_vm_feedforward_micro_ops"] == 5
    assert uqc["distillation_and_source_boundary"]["pass416_direct_five_qutrit_T_orbit_distills"] is False

    A = np.loadtxt(ROOT / lift["central_idempotent"]["matrix_path"], dtype=np.int64, delimiter="\t")
    assert np.array_equal(A @ A, 48 * A)
    assert rank_mod(A, 103) == 90
    assert (rank_mod(A, 2), rank_mod(A, 3)) == (14, 25)

    ramified = [row["prime"] for row in ad["prime_charts"]]
    parent = load("w33_20260924_trialitarian_asai_cube_descent.json")
    assert ramified == parent["cubic_field"]["ramified_primes"] == [3, 43, 733]
    assert all(row["epsilon_chart"] == [0, 1, 0] for row in ad["prime_charts"])

    schedule = load("w33_pass409_sparse8_holonet_schedule.json")
    assert ham["cycle"]["frame_l1_weights"] == [4, 5, 5, 4, 5, 5]
    assert ham["cycle"]["ticks"] == schedule["ticks_per_AB_cycle"] == 432
    assert ham["loss_falsifier"]["declared_AB_cycle_survival_target"] == 0.90


def test_visible_surfaces_are_unique():
    tail = (ROOT / "analysis/W33_SHARED_FRONTIER_TAIL.tex").read_text()
    assert tail.count("PASS10941_TRIALITY_VM_FIVE_FRONT_INSERT") == 1
    site = (ROOT / "docs/index.html").read_text()
    assert site.count('id="pass10941-triality-vm-five-front"') == 1
    report = (ROOT / "analysis/PASS10941_RESERVATION.md").read_text()
    for marker in ("centroid obstruction", "seven-qutrit Clifford", "A^2=48A",
                   "automatic-differentiation", "normalized falsifier",
                   "|b_m\\rangle=Z^{-m}|M_T^*\\rangle"):
        assert marker in report


if __name__ == "__main__":
    test_five_front_contract()
    test_visible_surfaces_are_unique()
    print("PASS10941_FIVE_FRONT_REGRESSION PASS")
