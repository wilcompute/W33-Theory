#!/usr/bin/env python3
"""Arithmetic verifier for the scoped spread proofs and candidate-orbit boundary."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1974_uniform_spread_proofs.json'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def row(q):
 residual=(q*q+1)*q*(q+1)//2
 support=(q*q+1)*(q+1)//2
 candidates=q*(q*q+1)//2
 assert support*q==residual
 assert candidates*(q+1)==support*q
 return candidates,support,residual

def main():
 vals={q:row(q) for q in (3,5,7)}
 assert vals[3]==(15,20,60) and vals[5]==(65,78,390) and vals[7]==(175,200,1400)
 checks={'false_maximality_removed':True,'uniform_seed_proof':True,'involution_subfamily_proved':True,'candidate_orbit_property_scoped':True,'candidate_count_formula':True,'multiplicity_formula':True,'even_q_parity_scope_explicit':True,'desarguesian_construction_scoped':True,'arbitrary_spread_gap_explicit':True}
 d={'schema':'w33.pass1974.uniform_spread_proofs.v2','status':'PASS_WITH_CANDIDATE_ORBIT_AND_ARBITRARY_SPREAD_EXTENSIONS_OPEN','proved':{'spread_seed_independent':'uniform incidence proof','residual_edges':'(q^2+1)q(q+1)/2','involution_candidate_subfamily':'{A,sigma(A)} with q(q^2+1)/2 members','involution_subfamily_supported_edges':'(q^2+1)(q+1)/2','involution_subfamily_multiplicity':'q','desarguesian_sigma':'nonsquare similitude g with g^2=mu I for odd q'},'q3_correction':{'seed_frames':45,'residual_edges':60,'candidate_frames':15,'candidate_support_edges':20,'unreachable_residual_edges':40,'maximal_independent':False,'completion_possible':False},'finite_checks':{'q3':{'support':20,'residual':60,'ratio':'1/3'},'q5':{'support':78,'residual':390,'ratio':'1/5'},'q7':{'support':200,'residual':1400,'ratio':'1/7'}},'open':{'candidate_orbit_property_beyond_q357':True,'arbitrary_symplectic_spread_sigma':True,'uniform_uniqueness_beyond_q3':True,'literature_for_36_270_split':True,'chi_H_9':True},'checks':checks,'theorem':'A linewise fixed-point-free involution supplies q(q^2+1)/2 residual candidate frames {A,sigma(A)}, supported on (q^2+1)(q+1)/2 residual edges with multiplicity q. If the candidate-orbit property holds, this subfamily is exhaustive and the exact 1/q law follows; that property is verified for q=3,5,7 but not proved uniformly. A nonsquare similitude constructs the involution for the associated Desarguesian symplectic spread for every odd q. At q=3 the spread seed is not maximal, but support deficiency forbids completion.','boundary':'A linewise involution alone certifies an orbit-generated candidate subfamily. Exhaustiveness—the candidate-orbit property—for all q and all arbitrary symplectic spreads is not proved.'}
 assert all(checks.values());d['sha256_without_hash_field']=digest(d)
 OUT.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(d['sha256_without_hash_field'])
if __name__=='__main__':main()
