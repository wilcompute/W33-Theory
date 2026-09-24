from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name):
    return json.loads((ROOT/"data"/name).read_text(encoding="utf-8"))

def test_compact_e8_two_control_is_exact_and_compact():
    d=load("w33_20260923_compact_e8_two_control.json")
    assert d["status"]=="PASS_TWO_FIXED_COMPACT_CONTROLS_GENERATE_E8_MINUS248"
    assert d["bracket_automorphism_checks"]==30628
    assert d["root_plane_fixed_killing_values"]==[-120]
    assert all(v["dimension"]==248 for v in d["exact_Q"].values())
    assert all(x>0 for x in d["split_cartan_killing_principal_minors"])

def test_sparse8_is_rank_optimal_and_unimodular():
    d=load("w33_20260923_compact_e8_sparse8.json")
    assert d["status"]=="PASS_MINIMAL_EIGHT_ROOT_COMPACT_E8_CONTROL"
    assert len(d["support"])==8
    assert abs(d["selected_root_determinant"])==1
    assert d["exact_Q"]["dimension"]==248
    assert d["lower_bound"]["minimum_support"]==8


def test_residual_is_cubic_jacobi_not_trinification():
    d=load("w33_20260923_cubic_jacobi_residual.json")
    assert d["status"].startswith("PASS_24D_RESIDUAL")
    assert d["ambient"]["dimension"]==24 and d["ambient"]["perfect"]
    assert d["radical"]["dimension"]==15
    assert d["radical"]["type"]=="Heisenberg h_15"
    assert d["nested_heisenberg"]["type"]=="Heisenberg h_9"
    q=d["levi_quotient"]
    assert q["dimension"]==9 and q["killing_rank_over_Q"]==9
    assert q["centroid_dimension_over_Q"]==3
    assert q["reduced_centroid_field_polynomial"]=="x^3 - x^2 - 53*x - 120"
    assert q["centroid_field_discriminant"]==94557

def test_split_cubic_levi_has_three_qubit_quartic_fingerprint():
    d=load("w33_20260923_cubic_jacobi_stu_split.json")
    assert d["status"].startswith("PASS_CUBIC_JACOBI_SPLITS")
    assert [r["prime"] for r in d["runs"]]==[107,151]
    for r in d["runs"]:
        assert r["commutant_dimensions"]=={"W8":1,"U6":3}
        assert r["associative_algebra_dimensions"]=={"W8":64,"U6":12}
        assert [r["invariant_polynomial_dimensions"][str(k)][0]
                for k in (1,2,3,4)]==[0,0,0,1]
        assert r["factor_derived_dimensions"]==[3,3,3]
        assert r["factor_cross_brackets_zero"] is True


def test_qutrit_bundle_routes_uniquely_to_constraint90_not_logical81():
    d=load("w33_20260923_qutrit_edge_triality_transducer.json")
    assert d["status"]=="PASS_UNIQUE_QUTRIT_FIBRE_TO_W90_CONSTRAINT_TRANSDUCER"
    assert d["induced_240_degrees"]==[10,60,80,90]
    assert d["signed_edge_240_degrees"]==[15,24,30,81,90]
    assert d["Hom_dimension"]==1
    assert d["unique_common_degree"]==90
    assert d["routing"]["canonical_frame"]==11
    assert d["routing"]["W90_contains_local_frames"]==[10,11]

def test_pass409_report_keeps_scope_firewalls():
    text=(ROOT/"analysis/PASS409_RESERVATION.md").read_text(encoding="utf-8")
    assert "rules out the" in text and "trinification reading" in text
    assert "A coordinate conjugating matrix" in text
    assert "does not derive spacetime dynamics" in text
    assert "continuum action" in text
    assert text.count("## 7. The qutrit fibre") == 1
    assert text.count("## 8. The minimal frame") == 1


def test_d4_contact_root_census_matches_residual_core():
    d=load("w33_pass409_d4_contact_root_census.json")
    assert d["status"]=="PASS_D4_CONTACT_GRADING_IS_A1_CUBED_ON_222_HEISENBERG"
    assert d["root_grade_counts"]=={"-2":1,"-1":8,"0":6,"1":8,"2":1}
    assert d["g0_semisimple"]=="A1^3"
    assert len(d["g_minus1_weight_set"])==8
    assert d["derived_contact_parabolic_dimension"]==18
    assert d["comparison_to_repo_core"]["fingerprint_matches"] is True

def test_cubic_branch_locus_is_exact_and_dual_number():
    d=load("w33_pass409_cubic_ramification_audit.json")
    assert d["field"]["discriminant"]==94557
    assert d["field"]["discriminant_factorization"]=={"3":1,"43":1,"733":1}
    assert [r["prime"] for r in d["ramified_reductions"]]==[3,43,733]
    for r in d["ramified_reductions"]:
        assert r["epsilon_multiplication_rank"]==1
        assert r["trace_form_rank"]==2
        assert r["levi_killing_rank"]==6


def test_explicit_rank90_transducer_is_not_just_character_overlap():
    d=load("w33_pass409_qutrit_edge_intertwiner.json")
    assert d["status"]=="PASS_EXPLICIT_RANK90_W_E6_INTERTWINER_OVER_GF103"
    w=d["matrix_witness"]
    assert w["intertwiner_shape"]==[90,90]
    assert w["intertwiner_rank"]==90
    assert w["all_generator_equations_hold"] is True
    assert d["character_audit"]["unique_common_degree"]==90
    assert "raw_stdout" not in d


def test_trialitarian_asai_cube_descent_is_rational_and_symplectic():
    d=load("w33_20260924_trialitarian_asai_cube_descent.json")
    assert d["status"]=="PASS_TRIALITARIAN_D4_ASAI_CUBE_DESCENT"
    assert d["cubic_field"]["galois_closure"]=="S3"
    assert d["restricted_standard_U6"]["commutant_dimension"]==3
    assert d["restricted_standard_U6"]["associative_envelope_Q_dimension"]==12
    w=d["asai_cube_W8"]
    assert w["commutant_dimension"]==1
    assert w["associative_envelope_Q_dimension"]==64
    assert w["S3_fixed_dimension_eight_highest_weights"]==[[1,1,1]]
    phase=d["heisenberg_phase_space"]
    assert phase["W8_symplectic_rank"]==8
    assert phase["orthogonalized_cross_rank"]==0
    assert phase["orthogonal_U6_symplectic_rank"]==6
    assert phase["phase_basis_pivot_minor_determinant"]==-1
    assert phase["levi_preserves_orthogonal_U6_checks"]==54
    assert phase["W8_U6orth_cross_brackets_zero"] is True
    assert phase["central_product"]=="h7 = h4 *_Z h3"
    assert d["trialitarian_D4_core"]["dimension"]==18


def test_pass409_visible_surfaces_are_single_and_clean():
    insert=(ROOT/"analysis/PASS20260923_compact_e8_cubic_jacobi_triality_insert.tex").read_text(encoding="utf-8")
    report=(ROOT/"analysis/PASS409_RESERVATION.md").read_text(encoding="utf-8")
    site=(ROOT/"docs/index.html").read_text(encoding="utf-8")
    assert insert.count(r"\paragraph{Boundary.}") == 1
    assert insert.count(r"\operatorname{TensorInd}") == 2
    assert site.count('href="https://github.com/wilcompute/W33-Theory/blob/master/analysis/PASS20260924_trialitarian_asai_cube_descent.md"') == 1
    for text in (insert,report):
        assert not any(ord(char)<32 and char not in "\n\r\t" for char in text)

def test_sparse8_holonet_schedule_is_exactly_six_microframes():
    d=load("w33_pass409_sparse8_holonet_schedule.json")
    assert d["status"].startswith("PASS_MINIMAL_EIGHT_ROOT")
    assert d["microframes_per_AB_cycle"]==6
    assert d["ticks_per_AB_cycle"]==432
    assert d["AB_cycles_per_30_microframe_Coxeter_bus"]==5
    assert d["AB_cycles_per_51840_tick_window"]==120
    for control in ("A","B"):
        s=d["schedules"][control]
        assert s["clique_lower_bound"]==3
        assert s["chromatic_number"]==3
        assert all(b["all_commute"] for b in s["batches"])
