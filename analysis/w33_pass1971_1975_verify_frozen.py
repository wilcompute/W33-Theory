#!/usr/bin/env python3
"""Fail-closed verifier for Passes 1971--1975."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FILES={
1971:ROOT/'data/w33_pass1971_spread_treatments_concordance.json',
1972:ROOT/'data/w33_pass1972_scalable_constraint_audit.json',
1973:ROOT/'data/w33_pass1973_solver_stagnation_diagnosis.json',
1974:ROOT/'data/w33_pass1974_uniform_spread_proofs.json',
1975:ROOT/'data/w33_pass1975_claim_ledger_physics_engineering.json'}
EXPECTED={1971:'47bd5542d06110ae1d6f87760c8043075752931fe46ed17bdbfa1392d4d955bb',1972:'e054590de94e710938076b27e64177407a9688529281a5b9628c579fa2094f71',1973:'0fe7146080cdf4216416b0a1da8dee00ef2d4a409214c5fdf0d073f9682fa693',1974:'ac56d4e6668cd89ed6e29936f57d4e8b8f91fdbc986f6805f64d4f44b573b221',1975:'c500a54f8de1bcedf782098872d6b174ba7d2ec3b89b646e9b6885ce3d15dbd1'}
AGG='c5611d6a3357ae3ac9a86fc107ce0ea004c75fd2e726dadd92061ed0832753c4'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 d={p:json.loads(f.read_text()) for p,f in FILES.items()}
 for p,z in d.items():
  assert z['sha256_without_hash_field']==EXPECTED[p]==digest(z),p
  assert all(z['checks'].values()),p
 assert d[1971]['corrections']['false_claim'].endswith('maximal independent set')
 assert d[1971]['solver_reconciliation']['combined_40_branches']==512714
 assert d[1972]['certified_examples']['pass1966_feasible_orbit']=={'after':807,'before':25920}
 assert d[1973]['telemetry']['spread']['branches']==60909
 assert d[1973]['telemetry']['combined8']['conflicts']==59
 assert d[1974]['q3_correction']['maximal_independent'] is False
 assert d[1974]['q3_correction']['unreachable_residual_edges']==40
 assert d[1975]['exact_inputs']['equivariant_linear_exports_from_90']==0
 assert len(d[1975]['engineering_proposals'])==5
 n=sum(len(z['checks']) for z in d.values());assert n==45
 a=json.loads((ROOT/'data/w33_pass1971_1975_five_frontiers.json').read_text())
 assert a['sha256_without_hash_field']==AGG==digest(a)
 assert a['certificates']=={str(k):v for k,v in EXPECTED.items()}
 assert a['n_checks']==a['n_verified']==n
 note=(ROOT/'analysis/W33_SPREAD_OBSTRUCTION_NOTE.md').read_text()
 draft=(ROOT/'analysis/W33_SPREAD_OBSTRUCTION_REFEREE_DRAFT.tex').read_text()
 assert 'not maximal independent' in note and 'not maximal independent' in draft
 assert 'propagation-horizon mismatch' in note and 'propagation-horizon mismatch' in draft
 out={'status':a['status'],'n_checks':n,'n_verified':n,'certificates':EXPECTED,'aggregate_sha256':AGG}
 print(json.dumps(out,indent=2,sort_keys=True));return out
if __name__=='__main__':main()
