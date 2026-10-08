"""Independent H27-H13 and five physics-front regression tests, October 8 2026."""
import itertools, json, math, sys
from pathlib import Path
import numpy as np
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import w33_20261008_h27_h13_five_frontiers as h
from w33_20261008_five_physics_frontiers import projective_points_and_lines


def test_elation_H27_W33_13_plus_27_is_actual_symplectic_group():
    pts,_=projective_points_and_lines()
    symp=np.array(h.J)
    polar=[p for p in pts if (symp@p)[0]%3==0]
    far=[p for p in pts if (symp@p)[0]%3!=0]
    assert len(polar)==13 and len(far)==27
    all_mats=[h.um(a,b,c) for a,b,c in itertools.product(range(3),repeat=3)]
    assert all(np.array_equal(h.mm(h.mm(g.T,symp),g),symp%3) for g in all_mats)
    assert {h.canon(g@np.array((0,0,0,1))) for g in all_mats}==set(far)
    assert h.h27_and_h13()["isomorphism_checked_multiplications"]==729


def test_explicit_F3_H13_H27_subgroup_729_multiplications_independent():
    for (a,b,c),(d,e,f) in itertools.product(itertools.product(range(3),repeat=3),repeat=2):
        new=((a+d)%3,(b+e)%3,(c+f+a*e-b*d)%3)
        assert np.array_equal(h.mm(h.um(a,b,c),h.um(d,e,f)),h.um(*new))
        assert np.array_equal(h.mm(h.ut8(a,b,2*c-a*b),h.ut8(d,e,2*f-d*e)),
                              h.ut8(*new[:2], 2*new[2]-new[0]*new[1]))


def test_nine_central_orbits_three_elements_each():
    p=np.array((0,0,0,1))
    orbit={h.canon(h.um(a,b,c)@p) for a,b,c in itertools.product(range(3),repeat=3)}
    c=h.um(0,0,1)
    triples={tuple(sorted({h.canon(np.linalg.matrix_power(c,j)@np.array(v)) for j in range(3)}))
             for v in orbit}
    assert len(triples)==9 and all(len(t)==3 for t in triples)


def test_operator_vs_regular_center_does_not_intertwine_without_dressing():
    r=h.representation_character_probe()
    assert r["regular_center_eigenvalue_multiplicities_1_omega_omega2"]==[9,9,9]
    assert r["operator_center_eigenvalue_multiplicities_1_omega_omega2"]==[0,27,0]
    assert r["no_27x27_representation_intertwiner_for_fixed_central_character"]


def test_two_actual_W33_cycle_centers_fail_to_glue_as_centers():
    data=h.global_cycle_glue()
    assert data["intersection_size"]==1
    assert data["central_commutator_rank"]==2
    assert data["commutator_nonzero_entries"]>0
    assert all(len(v)==8 for v in (data["cycleA"],data["cycleB"]))


def test_optimal_proxy_depth_36_is_not_a_hardware_achievement():
    data=json.loads((ROOT/"data/w33_20261008_h27_h13_five_frontiers.json").read_text())
    best=data["photonic_optimization"]
    assert best["best_proxy_stages"]==36
    rows=best["tested_depths"]
    assert max(rows,key=lambda r:r["launched_information_proxy"])["stages"]==36
    assert rows[-1]["survival"]<.004
    assert rows[2]["conditional_gap"]>.21
    assert best["union_bound_observables"]==1404
    assert best["confidence_level_for_complete_offdiagonal_scan"]==0.95
    assert best["best_Hoeffding_expected_launch_stages"] in (36,72)
    for row in rows:
        n=row["successful_detections_per_input_setting"]
        assert n>=8*math.log(2*1404/0.05)/(row["conditional_gap"]**2)
        assert row["total_required_successful_detections"]==54*n
        assert row["expected_launches_under_independent_loss"]>=54*n


def test_signed_triangle_fiber_and_minus_identity_obstruction():
    x=h.signed_vacuum_cover()
    assert x["vacua"]==320
    assert x["flags"]==160
    assert x["forget_sign_fiber_degree"]==2
    assert x["equivariant_320_to_projective_320_isomorphism"] is False
    assert x["physical_lorentz_chirality_selected"] is False


def test_E6_center_scalar_cannot_realize_distinct_X3_charges():
    r=h.proton_center_guard()
    assert r["different_Q_Uc"] is True
    assert r["X3_charges"]["Q"]==2
    assert r["X3_charges"]["Uc"]==0
    assert r["central_operator_H27_alone_cannot_be_X3_on_Q_and_Uc_within_one_E6_27"]


def test_explicit_invariant_CY_polynomial_has_free_fixed_loci_but_no_smoothness_certificate():
    data=json.loads((ROOT/"data/w33_20261008_h27_h13_five_frontiers.json").read_text())
    p=data["flavor_polynomial_candidate"]
    assert p["invariant_linear_system_dimension"]==21
    assert p["all_g_h_gh_fixed_points_avoided"]==[16,16,16]
    assert p["smoothness_proved"] is False
    assert len(p["coefficients"])==len(p["degree_vectors_in_each_orbit"])==21
    # Independent invariant orbital action on all 81 quartic multiweights.
    for orb in p["degree_vectors_in_each_orbit"]:
        for t in orb:
            assert sum(q==1 for q in t)%2==0
            flipped=[2-v for v in t]
            assert flipped in orb


def test_bundle_kinetic_metric_work_remains_uncompleted():
    r=h.build()
    assert "h27_h13" in r
    assert "flavor_polynomial_candidate" in r
    assert not r["flavor_polynomial_candidate"]["Ricci_flat_HYM_kinetic_metrics_computed"]
