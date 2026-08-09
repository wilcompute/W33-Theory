from __future__ import annotations

import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(name): return json.loads((ROOT/name).read_text(encoding='utf-8'))


def test_4503_all_maximal_types_nonsplit_and_flag_splits():
    d=load('data/PART_W33_PASS4503_MAXIMAL_SUBGROUP_SPLITTING_ERRATUM.json')
    assert d['pass']==4503 and d['all_five_maximal_types_nonsplit'] is True
    assert d['maximal_subgroup_orders']==[960,720,648,648,576]
    for name in [
      'maximal_2^4_A5_order960','maximal_spread_S6_order720',
      'maximal_line_stabilizer_order648','maximal_point_stabilizer_order648',
      'maximal_class45_involution_centralizer_order576']:
        assert d['results'][name]['split'] is False
    flag=d['results']['canonical_flag_stabilizer_order162']
    assert (flag['rank_coefficient'],flag['rank_augmented'],flag['affine_section_dimension'])==(384,384,6)


def test_4504_explicit_flag_section_optimum():
    d=load('data/PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json')
    assert d['pass']==4504 and d['flag']['sections_exhausted']==64
    assert d['optimum']['score']==[42,9,13]
    assert sorted(d['optimum']['column_weights'])==[1,1,1,1,5,5,5,5,9,9]
    assert len(d['optimum']['union'])==13
    assert all(x['split'] is False for x in d['order648_no_go'].values())


def test_4505_full_radical_h1():
    d=load('data/PART_W33_PASS4505_RADICAL_H1_THREE_CHARGES.json')
    assert (d['cohomology']['dim_Z1'],d['cohomology']['dim_B1'],d['cohomology']['dim_H1'])==(31,29,2)
    assert d['cohomology']['nonzero_classes']==3
    assert d['support']['dimension']==23 and d['support']['all_three_nonzero_classes_same_support'] is True
    assert '6-dimensional' in d['negative_result']


def test_4506_q53_bridge_and_dual_failure():
    d=load('data/PART_W33_PASS4506_Q53_APARTMENT_PROTECTED_BRIDGE.json')
    q=d['GQ_3_9'];dual=d['dual_GQ_9_3']
    assert (q['points'],q['lines'],q['apartments'])==(112,280,102060)
    assert (q['rank_H'],q['rank_N'],q['rank_NtN'])==(279,91,70)
    assert (q['apartment_radical_dimension'],q['protected_quotient_dimension'])==(209,70)
    assert q['gram_identity_HHt_eq_NtN'] is True
    assert (dual['rank_apartment_gram'],dual['rank_incidence_gram'],dual['gram_identity'])==(1,22,False)


def test_4507_fail_closed_release_guard_certificate():
    d=load('data/PART_W33_PASS4507_FRONTIER_CONSISTENCY_GUARD.json')
    assert d['builder_ordering_exactly_equal'] is True
    assert d['repaired_passes']==[4482,4493]
    assert 4510 in d['guarded_current_passes']
    assert 'fail closed' in d['policy']


def test_4508_outer_action_fork():
    d=load('data/PART_W33_PASS4508_OUTER_COHOMOLOGY_FORK.json')
    assert d['radical_H1']['dimension']==d['protected_middle_H1']['dimension']==2
    assert d['radical_H1']['PGSp_outer_action']=='identity'
    assert d['protected_middle_H1']['PGSp_outer_action']=='basis swap'
    assert (d['radical_H1']['nonzero_outer_fixed_classes'],d['protected_middle_H1']['nonzero_outer_fixed_classes'])==(3,1)


def test_4509_restriction_barcode_and_4510_local_cell():
    b=load('data/PART_W33_PASS4509_COHOMOLOGY_RESTRICTION_BARCODE.json')['barcode']
    assert b['M20_960']['restriction_kernel_dimension']==0
    assert b['spread_S6_720']['restriction_kernel_dimension']==0
    assert b['class45_C576']['restriction_kernel_dimension']==0
    assert b['point_648']['restriction_kernel_dimension']==1
    assert b['line_648']['restriction_kernel_dimension']==1
    assert b['point_648']['killed_nonzero_classes']!=b['line_648']['killed_nonzero_classes']
    assert b['incident_flag_162']['restriction_kernel_dimension']==2
    d=load('data/PART_W33_PASS4510_LOCAL_FLAG_GAUGE_CELL.json')
    assert d['support_size']==13 and d['radius']==1 and d['graph']=='K1 join 4K3'
    assert len(d['pencils_by_point_on_fixed_line'])==4
    assert all(len(p)==3 for p in d['pencils_by_point_on_fixed_line'])


def test_public_and_manuscript_frontier_is_reconciled():
    cfg=load('data/w33_public_frontier_extension_pass4461_4464.json')
    tokens={x['token'] for x in cfg['public_sections']}
    assert {'pass4490-4492-fixed-point-cocycle','pass4493-symmetry-breaking-section-threshold','pass4495-4502-distance-cohomology-ihara-clifford-prism','pass4503-4510-apartment-obstruction-scaling'}<=tokens
    page=(ROOT/'docs/apartment-obstruction-cohomology-gq.html').read_text(encoding='utf-8')
    assert 'all maximal subgroup types remain nonsplit' in page.lower()
    assert '70' in page and 'K1 ∨ 4K3' in page
    stale=(ROOT/'docs/apartment-symmetry-breaking-section.html').read_text(encoding='utf-8')
    assert 'false positive' in stale.lower()
    assert 'rank(A)=rank([A|b])=370' not in stale
    chain=(ROOT/'analysis/PASS4485_4488_apartment_core_self_gluing_insert.tex').read_text(encoding='utf-8')
    assert chain.count('PASS4503_4510_apartment_obstruction_scaling_insert')==1
