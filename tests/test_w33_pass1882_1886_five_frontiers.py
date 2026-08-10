from __future__ import annotations
import importlib.util,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);assert spec and spec.loader
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def test_frozen_aggregate_verifier():
 mod=load(ROOT/'analysis/w33_pass1882_1886_verify_frozen.py','p1882_1886')
 out=mod.main();assert out['n_verified']==out['n_checks']==42

def test_exact_frontier_values_and_boundaries():
 d={p:json.loads((ROOT/f'data/w33_pass{p}_'+{
 1882:'decoder_chart_to_global_obstruction',1883:'full_primal_weight_enumerator',1884:'two_adic_maximal_order',1885:'exceptional_s6_carrier_intertwiners',1886:'geometric_c4_clock_model'}[p]+'.json').read_text(encoding="utf-8")) for p in range(1882,1887)}
 assert d[1882]['weight5']['corrected_status']=='upper_bound_only'
 assert d[1882]['weight6']['unique_minimum_coefficient_status']=='OPEN'
 assert [d[1883]['primal_weight_enumerator'][str(w)] for w in (12,14,16)]==[891792940,54326090880,3770230198995]
 assert d[1884]['quotient_smith_invariants']==[1,2,4,8,32,64,256,1024]
 assert d[1885]['separator_V9_multiplicities']=={'15':0,'24':1,'30':0,'81':0,'90':1}
 assert d[1885]['explicit_maps']['orthogonality']=='N24^T N90 = 0'
 assert d[1886]['outer_automorphism_fixed_subgroup_structure']=='C4'
 assert d[1886]['fixed_loop']['duad']==[2,3]
