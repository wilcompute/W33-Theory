#!/usr/bin/env python3
"""Pass 3164: exact tri-ISA promotion law before observed placement."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3164_TRI_ISA_PHYSICAL_CONTRACT_results.json'
ISAS={
'current4':{'opcodes':['F_p','CX_pf','CX_fp','Z1'],'mean_length':14.175585133744857,'diameter':19,'collision_probability':45/324,'decoder_operation_units':5},
'low4':{'opcodes':['CX_fp','CX_pf','F_f','Z0'],'mean_length':15.216323969288219,'diameter':20,'collision_probability':36/324,'decoder_operation_units':6},
'fast6':{'opcodes':['F_f','CX_pf','CX_fp','Z0','Z1','Z3'],'mean_length':13.72936957018747,'diameter':19,'collision_probability':63/486,'decoder_operation_units':7}}
def cross(a,b):
    A=ISAS[a];B=ISAS[b]
    return (B['mean_length']-A['mean_length'])/(A['mean_length']*A['collision_probability']-B['mean_length']*B['collision_probability'])
def cost(name,c):
    x=ISAS[name];return x['mean_length']*(1+c*x['collision_probability'])
def main():
    c_cf=cross('current4','fast6');c_fl=cross('fast6','low4');c_cl=cross('current4','low4')
    assert c_cf<0 and c_fl>0 and c_cl>0
    samples=[]
    for c in (0,1,3.741933823529581,10,16.701642492779975,25):
        vals={k:cost(k,c) for k in ISAS};samples.append({'collision_price':c,'costs':vals,'winner':min(vals,key=vals.get)})
    out={'schema':'w33.pass3164.tri_isa_physical_contract.v1','isas':ISAS,
      'crossovers':{'current4_vs_fast6':c_cf,'current4_vs_low4':c_cl,'fast6_vs_low4':c_fl},
      'theorem':'fast6 strictly dominates current4 for every nonnegative collision price in the frozen path-plus-collision model',
      'runtime_policy_without_area_charge':'fast6 below 16.7016424928, low4 above; current4 is a fail-closed hardware fallback',
      'sample_costs':samples,
      'placement_targets':['w33_pass3164_current4','w33_pass3164_low4','w33_pass3164_fast6'],
      'promotion_rule':'fast6 requires observed calibration, area fit and timing; mathematical dominance alone does not authorize hardware promotion',
      'boundary':'Exact runtime algebra from exact BFS/collision metrics. Decoder cells, RAM, Fmax, switching latency and physical error are pending observed placement.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
