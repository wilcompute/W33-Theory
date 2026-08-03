#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def invariant(e,d,k,j):return j*k*(e-d)%12==0
def minimum(n):
 d=3**n
 return next(e for e in range(1,13) if all(invariant(e,d,k,j) for k in (1,2) for j in range(12)))
def main():
 rows=[{'qutrits':n,'dimension':3**n,'dimension_mod_12':3**n%12,'finite_lift_exponent':minimum(n),'arbitrary_U1_exponent':3**n} for n in range(1,17)]
 checks={'odd_cube':all(r['finite_lift_exponent']==3 for r in rows if r['qutrits']%2),'even_ninth':all(r['finite_lift_exponent']==9 for r in rows if not r['qutrits']%2),'period_two':[r['finite_lift_exponent'] for r in rows[:8]]==[3,9,3,9,3,9,3,9],'all_mu12_phases_k1_k2':all(invariant(r['finite_lift_exponent'],r['dimension'],k,j) for r in rows for k in (1,2) for j in range(12)),'determinant_required':all(r['finite_lift_exponent'] not in (12,) for r in rows)}
 assert all(checks.values())
 out={'schema':'w33.pass2805.n_qutrit_sensor_exponent.v1','status':'EXACT','phase_group':'mu_12','condition':'e congruent to 3^n modulo 12','minimal_law':{'n_odd':3,'n_even':9},'determinant_free_minimum':12,'arbitrary_phase_boundary':'For unrestricted U(1) representative phases, e must equal the full dimension 3^n.','rows':rows,'checks':checks}
 p=ROOT/'data/PART_BT2805_N_QUTRIT_SENSOR_EXPONENT_results.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
