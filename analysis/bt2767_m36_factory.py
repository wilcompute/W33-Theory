#!/usr/bin/env python3
"""Deterministic exact M36 preparation ROM and witness thresholds."""
from __future__ import annotations
import json,math,numpy as np
from collections import Counter
from pathlib import Path
from bt2772_2776_core import m36_grade_data
ROOT=Path(__file__).resolve().parents[1]
def ray_controls():
 rows=[]
 for family in range(4):
  for mu in range(3):
   for nu in range(3):
    if family==0:phase=[0,0,(3+2*mu)%6,(2*nu)%6]
    elif family==1:phase=[0,0,(3+2*mu)%6,(3+2*nu)%6]
    elif family==2:phase=[0,(3+2*mu)%6,0,(2*nu)%6]
    else:phase=[0,(2*mu)%6,(2*nu)%6,0]
    rows.append({'ray_id':family*9+3*mu+nu,'family':family,'mu':mu,'nu':nu,'dark_mode':family,'phase6':phase})
 return rows
def controls_to_ray(row):
 z=np.exp(1j*math.pi/3);return np.array([0 if i==row['dark_mode'] else z**row['phase6'][i] for i in range(4)],complex)/math.sqrt(3)
def expected_ray(row):
 w=np.exp(2j*math.pi/3);mu,nu,f=row['mu'],row['nu'],row['family']
 raw=([0,1,-w**mu,w**nu] if f==0 else [1,0,-w**mu,-w**nu] if f==1 else [1,-w**mu,0,w**nu] if f==2 else [1,w**mu,w**nu,0]);return np.array(raw,complex)/math.sqrt(3)
def build_rom():
 _,_,groups=m36_grade_data();by_size={len(ids):set(ids) for ids in groups.values()};exact={'deep':('(2+sqrt(3))/6',(2+math.sqrt(3))/6,0,by_size[8]),'mid':('(5+2*sqrt(3))/12',(5+2*math.sqrt(3))/12,1,by_size[24]),'shallow':('3/4',.75,2,by_size[4])};grades=Counter();rows=ray_controls()
 for row in rows:
  name=next(k for k,v in exact.items() if row['ray_id'] in v[3]);formula,value,code,_=exact[name];row.update({'grade':name,'grade_code':code,'nearest_stabilizer_fidelity_exact':formula,'nearest_stabilizer_fidelity_decimal':f'{value:.15f}'});grades[name]+=1
 assert grades==Counter({'mid':24,'deep':8,'shallow':4})
 return {'schema':'w33.pass2767.m36_preparation_rom.v2','status':'EXACT_PREPARATION_AND_WITNESS_ONLY','resource_type':'M36_Q4_RAW','hardware_factorization':{'shared_balanced_tritter':1,'dark_mode_choices':4,'phase_alphabet':'sixth roots of unity','states':36},'grade_census':dict(grades),'depolarizing_witness_thresholds':{'deep':{'exact':'(8-2*sqrt(3))/9','depolarizing_magic_witness_p_lt_decimal':f'{(8-2*math.sqrt(3))/9:.15f}'},'mid':{'exact':'(7-2*sqrt(3))/9','depolarizing_magic_witness_p_lt_decimal':f'{(7-2*math.sqrt(3))/9:.15f}'},'shallow':{'exact':'1/3','depolarizing_magic_witness_p_lt_decimal':f'{1/3:.15f}'}},'rows':rows,'boundary':'This ROM prepares and types the 36 ququart/two-qubit Witting rays. It does not identify them with qutrit magic states and does not certify a distillation code, injection gadget, or threshold for M36.','determinism':'All algebraic values are serialized as exact formulas plus fixed-width decimal strings; no NumPy eigenvalue float is stored.'}
def main():
 out=build_rom();p=ROOT/'data/PART_BT2767_M36_PREPARATION_ROM.json';p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('wrote',p)
if __name__=='__main__':main()
