#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'data'
def load(name):return json.loads((D/name).read_text())
def main()->int:
    a=load('PART_BT3124_D4_27_FRONTIER_results.json')
    b=load('PART_BT3125_RANK3_M36_FRONTIER_results.json')
    c=load('PART_BT3126_U42_CHARACTER_DECOMPOSITION_results.json')
    d=load('PART_BT3127_ROBUST_JOINT_POMDP_results.json')
    e=load('PART_BT3128_SELFDUAL_TIMING_FABRIC_results.json')
    f=load('PART_BT3129_UNIVERSAL_ISA_PARETO_results.json')
    g=load('PART_BT3130_FLAG_ORBIT_PREDICTIVE_QUOTIENT_results.json')
    h=load('PART_BT3131_ROUTE_TIME_PRODUCT_CODE_results.json')
    checks={
      '3124':a['exact_weight_1_to_4_constraints']==164220 and a['known_full_d4_upper_bound']==28,
      '3125':b['all_totally_isotropic_rank3_subspaces']==50868675 and b['pilot']['hits']==[],
      '3126':c['degree_check']==6480 and c['commutant_check']==1770 and c['nonzero_constituent_count']==18,
      '3127':d['states']==32 and d['first_action']=='route' and d['robust_policy_adverse']['objective']<d['nominal_policy_adverse']['objective'],
      '3128':e['ticks']==2796 and e['events']==1068 and e['phase_covariance_all_ticks'] and e['event_covariance_all_ticks'],
      '3129':f['connected']==80 and f['full_sp4']==24 and f['min_collision_count']==36 and f['current']['collisions']==45,
      '3130':g['raw_states']==6480 and g['orbit_states']==1770 and g['fixed_register_saving_bits']==2,
      '3131':h['route_unique'] and h['route_min_hamming']==1 and h['phase_min_hamming_28']==21,
    }
    out={'schema':'w33.pass3124_3132.deep_five_front_closure.v1','status':'COMPLETE_EXACT_MODELED_AND_SOURCE' if all(checks.values()) else 'FAIL',
         'check_count':len(checks),'checks':checks,
         'headlines':{
          '3124':'The exact central-r2 feasibility model has 120 variables and 164,220 weight-1..4 constraints; 66 new cut rounds reached eight residual collisions but did not prove 27 infeasible.',
          '3125':'A duplicate-free 220-pivot shard engine covers all 50,868,675 rank-three isotropic six-qubit subspaces; the 4,096-assignment pilot and predecessor samples contain no usable code.',
          '3126':'The 6,480 flag character decomposes with multiplicities [1,0,0,1,3,3,3,8,8,10,3,11,11,6,6,9,9,14,16,24], giving degree 6,480 and commutant 1,770.',
          '3127':'A 32-state regime-augmented Bayes POMDP cuts adverse-model objective by 4.19% relative to the nominal-only policy in the frozen synthetic model.',
          '3128':'The typed timing fabric verifies the reversal R(t)=1952-t mod 2796 on every phase and calibration event.',
          '3129':'Only 24 connected four-opcode sets generate full Sp(4,3); the universal Pareto frontier trades 36 collisions/slow mixing against 45 collisions/fast mixing.',
          '3130':'H-invariant control factors exactly through 1,770 flag orbits, saving two fixed register bits and 1.911 average uniform bits.',
          '3131':'The route-time product is injective on 585,912 states, but route distance is one while phase distance is 21; synchronization corrects errors, route localization does not.'},
         'claim_boundary':'Exact finite computations, bounded search, and explicit synthetic decision models are separated. No 27-row impossibility, full rank-three census result, laboratory optics, physical heat, or observed RTL/PDF claim is made.'}
    (D/'PART_BT3124_BT3132_DEEP_FIVE_FRONT_summary.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True));print(f"PASS {sum(checks.values())} / {len(checks)}")
    return 0 if all(checks.values()) else 1
if __name__=='__main__':raise SystemExit(main())
