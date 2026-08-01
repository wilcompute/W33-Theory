#!/usr/bin/env python3
"""Fail-closed reconciliation of the independently owned Passes 1841--1845 packet."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'
EXPECTED={
 'aggregate':'74fe918ebe6f2609e678363e4602a68ffb186e0571f1b5817757035828471063',
 '1841':'505747e002c226a90351263ca4180fcdab6a99e4b4ff51f88b8e7f178964bec0',
 '1842':'bc11980c93740e62bdb09367e6e38c80dd1b5a6e9e85bb9c4f92521e7861aa59',
 '1843':'40d048869615194effb319011d5189d010eefb51af5246545b8504e1252e072a',
 '1844':'534715d711e54b69bbd8b9bedc42f469a05acfff2049d6de48871e168a500953',
 '1845':'634941bb1ce14ee419cf8d4cc5a9ecd64ebe5a07d5107f5d5734a7115f8f8670'}
def main():
 p=json.loads((DATA/'w33_pass1841_1845_five_executions.json').read_text())
 checks={
  'aggregate_status':p['status']=='PASS',
  'aggregate_hash':p['certificate_sha256']==EXPECTED['aggregate'],
  'pass_hashes':all(p['passes'][k]['certificate_sha256']==EXPECTED[k] for k in EXPECTED if k!='aggregate'),
  'two_orbits_minimum':p['checks']['second_signature_orbit_found'],
  'second_no_lift':p['checks']['second_orbit_no_lift'],
  'outer_fixes_both':p['checks']['outer_fixed_two_known_orbits'],
 }
 out={'schema':'w33.pass1846.parallel_reconciliation.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
 'parallel_aggregate_sha256':EXPECTED['aggregate'],
 'certified_signature_solutions_lower_bound':28800,
 'certified_inner_orbits':[
  {'size':2880,'type_multiset':'6T128+3T96','stabilizer':'C3xC3','lift':'UNSAT'},
  {'size':25920,'type_multiset':'3T128+2T120+2T104+2T96','stabilizer':'1','lift':'UNSAT'}],
 'boundary':'This reconciles the independently owned packet. The binary signature-resolution orbit census remains incomplete, so two no-lift orbits do not prove global nine-cover UNSAT.'}
 raw=json.dumps(out,sort_keys=True,separators=(',',':')).encode();out['sha256']=hashlib.sha256(raw).hexdigest()
 print(json.dumps(out,sort_keys=True,separators=(',',':')))
 raise SystemExit(out['status']!='PASS')
if __name__=='__main__':main()
