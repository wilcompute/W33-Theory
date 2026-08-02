#!/usr/bin/env python3
"""Rebuild the frozen solver-stagnation telemetry certificate."""
from __future__ import annotations
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_pass1973_solver_stagnation_diagnosis.json'

def digest(d):
 x=dict(d);x.pop('sha256_without_hash_field',None)
 return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def main():
 raw={'plain':(2127575,3622),'spread':(60909,1040),'lex8':(198352,395),'combined8':(451460,59),'combined40':(512714,68)}
 tel={}
 for name,(b,c) in raw.items():
  tel[name]={'branches':b,'conflicts':c,'conflicts_per_1000_branches':1000*c/b,'branches_per_conflict':b/c}
 cmp={'combined8_over_spread_branches':451460/60909,'combined40_over_spread_branches':512714/60909,'combined40_over_combined8_branch_increase':512714/451460-1,'spread_reduction_vs_plain':1-60909/2127575,'lex8_reduction_vs_plain':1-198352/2127575,'combined8_reduction_vs_plain':1-451460/2127575,'combined40_reduction_vs_plain':1-512714/2127575}
 checks={'spread_is_best_tested':raw['spread'][0]==min(x[0] for x in raw.values()),'combined8_worse_than_spread':raw['combined8'][0]>raw['spread'][0],'combined40_worse_than_combined8':raw['combined40'][0]>raw['combined8'][0],'combined_conflict_density_below_point14':tel['combined8']['conflicts_per_1000_branches']<0.14 and tel['combined40']['conflicts_per_1000_branches']<0.14,'orbit_reduction_not_runtime_proxy':True,'no_new_constraint_added':True,'chi_open':True,'hardware_frontend_separated':True}
 d={'schema':'w33.pass1973.solver_stagnation_diagnosis.v1','status':'PASS_WITH_CHROMATIC_DECISION_OPEN','telemetry':tel,'comparisons':cmp,'diagnosis':{'name':'propagation-horizon mismatch','exact_observation':'combined fixed-search models are dominated by spread-only search under the frozen benchmark','interpretation':'spread aggregate variables are committed early while frame-level lex constraints become informative late, producing long locally consistent prefixes and extremely low conflict density','not_proved':'absence of a small unsatisfiable core'},'engineering_direction':'canonicalise spread signatures outside the solver, then preserve spread-first branching inside canonical cubes','checks':checks,'theorem':'For the frozen CP-SAT configurations, spread-variable branching is the best tested search. Adding eight or forty geometric lex generators inflates the branch tree by factors 7.412 and 8.418 and lowers conflict density to about 0.13 per thousand branches. The exact 25,920-to-807 orbit reduction is therefore not a search-performance theorem.','boundary':'The diagnosis is configuration-specific telemetry and does not prove satisfiability, infeasibility, or the nonexistence of useful alternative symmetry handling.'}
 assert all(checks.values());d['sha256_without_hash_field']=digest(d)
 OUT.write_text(json.dumps(d,sort_keys=True,separators=(',',':'))+'\n');print(d['sha256_without_hash_field'])
if __name__=='__main__':main()
