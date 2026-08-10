from __future__ import annotations
import json
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parents[1]
NAMES={1065:'schur_cocycle',1066:'outer_lift',1067:'outer_class_geometry',1068:'chevie_g25_g32_matrices',1069:'photonic_pipeline'}

def load_all():
    return {p:json.loads((ROOT/'data'/f'w33_pass{p}_{NAMES[p]}.json').read_text(encoding="utf-8")) for p in NAMES}

def test_all_five_passes_are_green():
    R=load_all();assert all(r['status']=='PASS' and all(r['checks'].values()) for r in R.values())

def test_exact_check_total_is_65():
    assert sum(r['check_count'] for r in load_all().values())==65

def test_cohomology_and_outer_lift_decisions():
    R=load_all();assert R[1065]['cohomology_decision']['class_nonzero']
    assert R[1066]['structural_decision']['globally_split']
    assert R[1066]['outer_class_lifts']['36']['lift_square']=='global_negation'
    assert R[1066]['outer_class_lifts']['540']['lift_order']==2

def test_outer_geometries_are_exact_bijections():
    R=load_all();assert R[1067]['checks']['class36_to_spreads_is_bijection']
    assert R[1067]['checks']['class540_to_disjoint_line_pairs_is_bijection']

def test_chevie_parabolic_inclusion_is_matrix_level():
    R=load_all();assert R[1068]['checks']['pointwise_e4_stabilizer_equals_embedded_G25']
    assert R[1068]['checks']['explicit_inclusion_intertwines_generators']

def test_photonic_pipeline_hits_all_fail_closed_branches():
    R=load_all();verdicts=[x['joint_verdict'] for x in R[1069]['analyses']]
    assert verdicts==['supports_W33_contextual_point_Hessian_tower','local_Hessian_present_contextual_substrate_rejected','contextuality_present_selected_tower_rejected','joint_rejection']
    assert R[1069]['invalid_calibration_test']['joint_verdict']=='inconclusive_no_claim'

def test_generated_hardware_artifacts_are_wired():
    manifest=json.loads((ROOT/'hardware'/'w33_pass1069_photonic_manifest.json').read_text(encoding="utf-8"))
    fixture=json.loads((ROOT/'hardware'/'w33_pass1069_synthetic_blinded.json').read_text(encoding="utf-8"))
    with (ROOT/'hardware'/'w33_pass1069_control_schedule.csv').open() as f: rows=list(csv.DictReader(f))
    assert manifest['schema']=='w33.pass1069.photonic_protocol_manifest.v1'
    assert len(fixture['datasets'])==4 and fixture['synthetic_fixture_only']
    assert len(rows)==48 and sum(r['arm']=='contextuality' for r in rows)==40 and sum(r['arm']=='central_C3' for r in rows)==8
