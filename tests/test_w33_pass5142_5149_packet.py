from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'


def load(n,name):
    p=DATA/name
    assert p.exists(),p
    j=json.loads(p.read_text())
    assert j['pass']==n
    return j


def test_pass5142_leader20_barrier():
    j=load(5142,'PART_W33_PASS5142_Q5_CUBIC_LEADER20_CLOSURE.json')
    assert j['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_20'
    assert j['leader18']['uniform_weight_lower_bound']==800
    assert j['leader19']['uniform_weight_lower_bound']==673


def test_pass5143_metric_formula_and_anchors():
    j=load(5143,'PART_W33_PASS5143_ROOT_CAYLEY_METRIC_THEOREM.json')
    assert j['status']=='THEOREM_ROOT_CAYLEY_METRIC_CHAR_GT3'
    for qs,v in j['anchors'].items():
        q=int(qs);expect=[1,4*(q-1),8*(q-1)**2,(q-1)**2*(10*q-21),(q-1)**2*(q-4)**2]
        assert v==expect and sum(v)==q**4


def test_pass5144_gram_bridge():
    j=load(5144,'PART_W33_PASS5144_ROOT_COSET_GRAM_THETA_BRIDGE.json')
    assert j['identity']=='H H^T = 4 I + A_theta over Z'
    assert j['anchors']['3']['rank_Q']==69
    assert j['anchors']['3']['theta_minus4']==12
    assert j['anchors']['5']['rank_Q']==405
    assert j['anchors']['5']['theta_minus4']==220


def test_pass5145_leader21_barrier():
    j=load(5145,'PART_W33_PASS5145_Q5_CUBIC_LEADER21_CLOSURE.json')
    assert j['status']=='THEOREM_Q5_STRICT_COUNTEREXAMPLE_LEADER_AT_LEAST_21'
    assert j['adjacent_pair_cap']==31
    assert j['uniform_leader20_weight_lower_bound']==711


def test_pass5146_embedded_sharp_family():
    j=load(5146,'PART_W33_PASS5146_Q5_SHARP_LEADER18_EMBEDDED_CENSUS.json')
    assert j['abstract_sharp_adjacent_pairs']==27
    assert sum(j['opposite_line_carrier']['weight_histogram'].values())==4096
    assert j['opposite_line_carrier']['minimum_weight_in_family']==5832
    assert j['k33_grid_carrier']['apartment_word_weight']==5832


def test_pass5147_projection_identity():
    j=load(5147,'PART_W33_PASS5147_ROOT_PROJECTION_DIRICHLET_THEOREM.json')
    assert j['status']=='THEOREM_ALL_Q_ROOT_PROJECTION_DIRICHLET_MEAN_VALUE'
    assert 'A_theta=q(P0+P1+P2+P3)-4I' in j['operator_identity']


def test_pass5148_exact_wall():
    j=load(5148,'PART_W33_PASS5148_Q5_LEADER21_EXACT_WALL.json')
    assert j['adjacent_pair_cap']==33
    assert j['branches']['n1=32']['weight_lower_bound']==637
    assert j['branches']['n1=33']['remaining_triple_intersection_mass']==42


def test_shared_manuscript_insert_is_wired():
    insert=ROOT/'analysis/PASS5142_5149_cubic_root_projection_insert.tex'
    manifest=ROOT/'analysis/W33_CURRENT_FRONTIER_MANIFEST.tex'
    assert insert.exists()
    s=manifest.read_text()
    assert r'\input{analysis/PASS5142_5149_cubic_root_projection_insert}' in s
    for wrapper in ('w33_paper.tex','photonic_holonet.tex','holonet_machine_blueprint.tex'):
        t=(ROOT/wrapper).read_text()
        assert r'\input{analysis/W33_CURRENT_FRONTIER_MANIFEST}' in t
