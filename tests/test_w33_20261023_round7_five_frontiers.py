"""Independent round-seven regressions for all five research fronts."""
from pathlib import Path
import json
import math
import numpy as np
from analysis.w33_20261023_round7_four_frontiers import (
    make_geometry,modular_basis,delta_rows,
    reduce_and_insert,reduce_zero,source_free_chiral_clock,
    magic_factory_interface,kinetic_gap_obstruction)
from analysis.w33_20261023_three_layer_routing_cpsat import run as routing_sat

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/"data/PART_20261023_ROUND7_FOUR_FRONTIERS.json"


def test_GF9_four_explicit_Frobenius_extension_witnesses():
    cert=json.loads(CERT.read_text())["frobenius"]
    assert cert["rank_delta1"]==4
    assert cert["rank_DK_intersection_C"]-cert["rank_DC"]==4
    g=make_geometry(9);p=3;n=g["n"];perm=g["perm"]
    C=modular_basis(g["B"],p)
    B=np.asarray(g["B"],dtype=np.int64)
    DC=modular_basis(delta_rows(np.array(list(C.values())),perm,p),p)
    witnesses=cert["four_independent_witness_pairs"]
    assert len(witnesses)==4
    for item in witnesses:
        x=np.array(list(map(int,item["preimage_ternary"])),dtype=np.int64)
        y=np.array(list(map(int,item["image_ternary"])),dtype=np.int64)
        assert len(x)==n and len(y)==n
        assert not np.any(B@x%p)
        assert np.array_equal(delta_rows(x[None,:],perm,p)[0],y)
        assert reduce_zero(y,C,p)
        assert reduce_and_insert(y,DC,p)
    assert len(DC)==58


def test_source_free_chiral_K_symmetric_ground_branches_N2_exact_diagonalization():
    c=source_free_chiral_clock()
    assert c["exact_general_N_ground_degeneracy"]=="2^(N+1), K exchanges all-plus and all-minus macroscopic sectors"
    assert [x["ground_degeneracy"] for x in c["finite_N_checks"][:3]]==[4,8,16]
    omega=np.exp(2j*np.pi/3)
    x=np.roll(np.eye(3),1,axis=0).astype(complex)
    z=np.diag([1,omega,omega**2])
    rx=(x+x.conj().T)/2; rz=(z+z.conj().T)/2
    O=np.kron((rx@rz-rz@rx)/(2j),np.eye(3))
    parity=np.zeros((9,9))
    for a in range(3):
        for b in range(3):
            parity[3*(-a%3)+(-b%3),3*a+b]=1
    H=(np.eye(9)-9*parity)/2
    I=np.eye(9)
    otot=np.kron(O,I)+np.kron(I,O)
    H2=np.kron(H,I)+np.kron(I,H)-otot@otot/2
    e=np.linalg.eigvalsh(H2)
    expected=-8-2*9/32
    assert np.isclose(e[0],expected)
    assert np.count_nonzero(np.isclose(e,expected,atol=1e-8))==8
    assert np.allclose(H2,H2.conj().T)
    assert np.allclose(H2,H2.conj())  # K-even despite imaginary O


def test_permutation_routing_cpsat_UNSAT3_and_SAT4():
    three=routing_sat(seconds=12,depth=3)
    assert three["status"]=="INFEASIBLE",three
    four=routing_sat(seconds=12,depth=4)
    assert four["feasible_route_found"],four
    assert four["swaps"]==36
    assert len(four["exact_layers"])==4
    assert all(len(layer)==9 for layer in four["exact_layers"])


def test_magic_plus_Clifford_Choi_construction_and_error_budget():
    c=magic_factory_interface()
    assert c["magic_distillation"] is False
    assert c["logical_error_threshold"] is False
    assert c["Choi_F"]=="1-2eps/3"
    for sample in c["noise_samples"]:
        eps=sample["raw_depolarizing_parameter"]
        assert math.isclose(sample["Choi_resource_fidelity"],1-2*eps/3,abs_tol=1e-12)
        assert math.isclose(sample["upper_bound_output_trace_distance"],math.sqrt(2*eps/3),abs_tol=1e-12)


def test_all_q_normalized_kinetic_gap_is_not_gapless():
    c=kinetic_gap_obstruction()
    assert c["status"]=="ALL_Q_THEOREM_POSITIVE_ANCHOR_DEFECTS_CANNOT_CLOSE_NORMALIZED_W33_GAP"
    assert [x["q"] for x in c["examples"]]==[3,4,8,9]
    assert all(x["normalized_L_gap_lower_bound"]>=5/6 for x in c["examples"])
    assert c["examples"][-1]["normalized_L_gap_lower_bound"]==1-8/90
