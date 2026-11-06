#!/usr/bin/env python3
"""Pass 3160: adaptive equal-footprint dual-ISA scheduler.

The runtime decision is exact for the frozen additive model.  The two hardware-compatible
four-opcode ISAs share opcode width and decoder-operation count.  A separately reported
six-opcode design is a larger-area advisory, not silently folded into the equal-footprint
switch.
"""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'PART_BT3160_ADAPTIVE_DUAL_ISA_results.json'
CURRENT={'name':'current4','generators':['F_p','CX_pf','CX_fp','Z1'],
         'mean_length':14.175585133744857,'collision_probability':45/324,
         'collision_exposures':1.9688312685756746,'decoder_units':6}
LOW={'name':'low_collision4','generators':['CX_fp','CX_pf','F_f','Z0'],
     'mean_length':15.216323969288219,'collision_probability':36/324,
     'collision_exposures':1.6907026632542463,'decoder_units':6}
FAST6={'name':'fast6_advisory','generators':['F_f','CX_pf','CX_fp','Z0','Z1','Z3'],
       'mean_length':13.72936957018747,'collision_probability':63/486,
       'collision_exposures':1.779733092431709,'decoder_units':8}

def cost(isa,c):return isa['mean_length']+c*isa['collision_exposures']
def threshold(switch_cost=0.0,direction='up'):
    dL=LOW['mean_length']-CURRENT['mean_length']
    dE=CURRENT['collision_exposures']-LOW['collision_exposures']
    return (dL+(switch_cost if direction=='up' else -switch_cost))/dE

def effective_collision_cost(base,entropy_bits,route_burden,calibration_confidence,
                             entropy_weight=.35,route_weight=.5,calibration_weight=1.0):
    return base+entropy_weight*entropy_bits+route_weight*route_burden+calibration_weight*(1-calibration_confidence)

def choose(previous,c_eff,switch_cost=.25):
    up=threshold(switch_cost,'up');down=threshold(switch_cost,'down')
    if previous=='current4':return 'low_collision4' if c_eff>up else 'current4'
    return 'current4' if c_eff<down else 'low_collision4'

def main():
    examples=[]
    for base,H,R,K in [(1,1,0,.99),(2,3,1,.9),(3,5,2,.7),(4,7,3,.5)]:
        c=effective_collision_cost(base,H,R,K)
        examples.append({'base':base,'entropy_bits':H,'route_burden':R,'calibration_confidence':K,
                         'effective_collision_cost':c,'from_current':choose('current4',c),
                         'from_low_collision':choose('low_collision4',c)})
    d6_low=(LOW['mean_length']-FAST6['mean_length'])/(FAST6['collision_exposures']-LOW['collision_exposures'])
    out={'schema':'w33.pass3160.adaptive_dual_isa.v1','current':CURRENT,'low_collision':LOW,
      'zero_switch_threshold':threshold(),
      'hysteresis_switch_cost_instructions':.25,
      'current_to_low_threshold':threshold(.25,'up'),
      'low_to_current_threshold':threshold(.25,'down'),
      'effective_cost_law':'c_eff=c_base+0.35 H_causal+0.5 route_burden+1.0(1-calibration_confidence)',
      'examples':examples,
      'six_opcode_advisory':dict(FAST6,
         runtime_relation='dominates current4 in mean length and collision exposures before decoder cost',
         crossover_vs_low_collision4=d6_low,
         integration_boundary='not selected by the equal-footprint dual scheduler until area/timing are observed'),
      'boundary':'Exact for the frozen additive instruction-plus-collision model and stated hysteresis. Coefficients mapping uncertainty, route burden and calibration confidence to collision cost are explicit controller parameters, not laboratory measurements.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
