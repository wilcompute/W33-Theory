#!/usr/bin/env python3
"""Fail-closed verifier for the frozen Passes 1836--1840 certificates."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
 1836:'w33_pass1836_signature_resolution_witness.json',
 1837:'w33_pass1837_middle_layer_compression.json',
 1838:'w33_pass1838_weight5_dependency_frontier.json',
 1839:'w33_pass1839_geometric_four_bit_chirality.json',
 1840:'w33_pass1840_atlas_standard_word.json'}
def canonical_hash(d):
 x=dict(d);x.pop('sha256',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def load(name):
 d=json.loads((ROOT/'data'/name).read_text());assert d['status']=='PASS';assert d['sha256']==canonical_hash(d);return d
def verify():
 d={p:load(n) for p,n in FILES.items()}
 assert d[1836]['class_multiset']=={'T128':6,'T96':3} and d[1836]['target_verified'] and len(d[1836]['witness'])==9
 assert d[1837]['nine_line_spread_exists'] is False and d[1837]['maximum_disjoint_lines']==6 and d[1837]['maximum_partial_spreads']==72
 assert d[1837]['residual_srg']==[15,6,1,3] and d[1837]['residual_is_KG_6_2']
 assert d[1838]['weight6_codewords']==9600 and d[1838]['disjoint_equal_triple_pairs']==96000
 assert d[1838]['weight5_distinct_singleton_shadowed']==185040 and d[1838]['singleton_shadow_multiplicity']=={'1':185040}
 assert d[1839]['trace_matrix_determinant']==80 and d[1839]['trace_matrix'][0]==[3,4,2,3]
 assert d[1840]['group_order']==51840 and d[1840]['atlas_standard_conditions']=={'c_class':'2C','order_c':2,'order_cd':10,'order_d':9}
 assert d[1840]['word_length_cdD']==18 and d[1840]['verification']['word_evaluates_to_canonical_outer']
 agg=load('w33_pass1836_1840_five_frontiers.json')
 assert set(agg['passes'])==set(map(str,FILES)) and all(agg['checks'].values())
 return {'status':'PASS','aggregate_sha256':agg['sha256'],'pass_sha256':{str(p):d[p]['sha256'] for p in FILES}}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
