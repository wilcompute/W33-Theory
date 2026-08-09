#!/usr/bin/env python3
"""Pass 4507 -- adversarial frontier consistency guard.

This guard was added after two stale frozen-result failures were found in one
continuation run:

* Pass 4493's restricted section table disagreed with exact re-execution;
* Pass 4482's frozen ten-line basis no longer satisfied its own current witness.

The policy is now fail-closed: exact builders must agree, repaired witnesses must
regenerate their frozen summaries, corrected public/manuscript surfaces must not
contain the withdrawn 370/370 claim, and the concurrent public registry must
retain every packet from 4461 through 4510.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np

from w33_pass4461_line_signing_apartment_trace import geometry
from w33_pass4472_4479_apartment_module_thermo_ihara_pauli import build_geometry
from w33_pass4463_apartment_parity_tomography import rank_mod2

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4507_FRONTIER_CONSISTENCY_GUARD.json'


def load(path): return json.loads((ROOT/path).read_text(encoding='utf-8'))


def main()->int:
    p1,l1,A1,N1,_=geometry()
    p2,_,l2,_,A2,Astar2,*_=build_geometry()
    assert p1==p2
    assert l1==l2
    assert np.array_equal(np.asarray(A1,dtype=np.uint8),np.asarray(A2,dtype=np.uint8))
    N=np.asarray(N1,dtype=np.uint8)%2
    assert np.array_equal((N.T@N)%2,np.asarray(Astar2,dtype=np.uint8))

    c4482=load('data/PART_W33_PASS4482_TEN_LINE_PROTECTED_READOUT.json')
    assert c4482['status']=='REPAIRED_BY_PASS4507'
    selected=c4482['selected_line_indices']
    G=((N.T@N)%2)[np.ix_(selected,selected)]
    assert rank_mod2(G)==10 and int(G.sum()//2)==6
    assert c4482['basis_graph']['type']=='P4 disjoint-union 3K2'

    c4493=load('data/PART_W33_PASS4493_SYMMETRY_BREAKING_SECTION_THRESHOLD.json')
    assert c4493['status']=='CORRECTED_BY_PASSES_4503_4507'
    assert c4493['tested_subgroups']['one_line_stabilizer']['section_system']['consistent'] is False
    assert c4493['tested_subgroups']['one_point_stabilizer']['section_system']['consistent'] is False
    assert c4493['tested_subgroups']['incident_flag_stabilizer']['section_system']['affine_dimension']==6

    c4503=load('data/PART_W33_PASS4503_MAXIMAL_SUBGROUP_SPLITTING_ERRATUM.json')
    assert c4503['all_five_maximal_types_nonsplit'] is True
    assert c4503['maximal_subgroup_orders']==[960,720,648,648,576]
    c4504=load('data/PART_W33_PASS4504_MINIMAL_FLAG_SECTION.json')
    assert c4504['optimum']['score']==[42,9,13] and c4504['flag']['sections_exhausted']==64
    c4505=load('data/PART_W33_PASS4505_RADICAL_H1_THREE_CHARGES.json')
    assert c4505['cohomology']['dim_H1']==2 and c4505['support']['dimension']==23
    c4506=load('data/PART_W33_PASS4506_Q53_APARTMENT_PROTECTED_BRIDGE.json')
    assert c4506['GQ_3_9']['protected_quotient_dimension']==70 and c4506['dual_GQ_9_3']['gram_identity'] is False
    c4508=load('data/PART_W33_PASS4508_OUTER_COHOMOLOGY_FORK.json')
    assert c4508['radical_H1']['PGSp_outer_action']=='identity'
    assert c4508['protected_middle_H1']['PGSp_outer_action']=='basis swap'
    c4509=load('data/PART_W33_PASS4509_COHOMOLOGY_RESTRICTION_BARCODE.json')
    assert c4509['barcode']['incident_flag_162']['restriction_kernel_dimension']==2
    c4510=load('data/PART_W33_PASS4510_LOCAL_FLAG_GAUGE_CELL.json')
    assert c4510['graph']=='K1 join 4K3' and c4510['support_size']==13

    active=[
      'analysis/PASS4493_symmetry_breaking_section_insert.tex',
      'analysis/PASS4493_symmetry_breaking_section_index_insert.html',
      'docs/apartment-symmetry-breaking-section.html',
      'analysis/PASS4503_4510_apartment_obstruction_scaling_insert.tex',
      'analysis/PASS4503_4510_apartment_obstruction_scaling_index_insert.html',
      'docs/apartment-obstruction-cohomology-gq.html',
    ]
    for name in active:
        text=(ROOT/name).read_text(encoding='utf-8')
        assert 'rank(A)=rank([A|b])=370' not in text, name
        assert '370 / 370' not in text, name

    chain=(ROOT/'analysis/PASS4485_4488_apartment_core_self_gluing_insert.tex').read_text(encoding='utf-8')
    assert chain.count('PASS4495_4502_distance_cohomology_ihara_clifford_prism_insert')==1
    assert chain.count('PASS4503_4510_apartment_obstruction_scaling_insert')==1

    cfg=load('data/w33_public_frontier_extension_pass4461_4464.json')
    tokens={x['token'] for x in cfg['public_sections']}
    required={
      'pass4461-4464-line-signing-apartment-parity','pass4469-4471-apartment-h10-bridge',
      'pass4472-4479-apartment-module-thermo-ihara-pauli','pass4480-4483-apartment-h10-geometric-readout',
      'pass4485-4488-apartment-core-self-gluing','pass4490-4492-fixed-point-cocycle',
      'pass4493-symmetry-breaking-section-threshold','pass4495-4502-distance-cohomology-ihara-clifford-prism',
      'pass4503-4510-apartment-obstruction-scaling'}
    assert required<=tokens, sorted(required-tokens)

    out={
      'pass':4507,
      'theorem':'frontier consistency guard after stale-certificate and concurrent-registry failures',
      'builder_ordering_exactly_equal':True,
      'repaired_passes':[4482,4493],
      'guarded_current_passes':[4503,4504,4505,4506,4508,4509,4510],
      'public_tokens_required':sorted(required),
      'policy':'regenerate executable evidence and fail closed on script/certificate, manuscript/public, builder-order, or registry disagreement',
      'boundary':'This is release-integrity evidence, not a new mathematical theorem about W33 itself.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps(out,indent=2,sort_keys=True));return 0

if __name__=='__main__':raise SystemExit(main())
