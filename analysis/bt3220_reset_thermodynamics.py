#!/usr/bin/env python3
"""Pass 3220: rank and Landauer boundary for phase versus belief reset."""
from __future__ import annotations
import json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_BT3220_RESET_THERMODYNAMICS.json'
KB=1.380649e-23
EV=1.602176634e-19

def row(states,temperature=300.0):
 bits=math.log2(states);joules=KB*temperature*math.log(states)
 return {'state_capacity':states,'maximum_logical_capacity_bits':bits,
         'ensemble_assumption':'uniform/maximally mixed over all listed states',
         'temperature_kelvin':temperature,
         'landauer_floor_for_uniform_ensemble_joules':joules,
         'landauer_floor_for_uniform_ensemble_electron_volts':joules/EV}

def main():
 belief=876;phase=12
 result={'schema':'w33.pass3220.reset_thermodynamics.v2',
  'phase_only_marker':{'product_state_count':belief*phase,'image_rank':belief,
    'belief_capacity_erased_bits':0.0,'belief_landauer_floor_joules':0.0},
  'full_belief_reset':row(belief),
  'full_phase_and_belief_reset':row(belief*phase),
  'phase_factor_reset_only':row(phase),
  'theorem':'Because every phase-only letter acts as identity on belief, its product-map rank is at least 876. A rank-one belief reset removes log2(876) bits of state capacity; actual thermodynamic cost depends on the input distribution.',
  'boundary':'The k_B T ln(N) values apply to a uniform/maximally mixed N-state ensemble at the stated temperature. They are not distribution-independent per-event costs or CMOS, optical, controller, or laboratory energy predictions.'}
 OUT.parent.mkdir(exist_ok=True);OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'rank':belief,'uniform_belief_floor_J':result['full_belief_reset']['landauer_floor_for_uniform_ensemble_joules']},sort_keys=True))
if __name__=='__main__':main()
