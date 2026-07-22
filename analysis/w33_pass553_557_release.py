#!/usr/bin/env python3
"""Combined custody certificate for Passes 553--557."""
from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass553_557_intrinsic_automaton_formal_control_release.json'
FILES={n:next((ROOT/'data').glob(f'w33_pass{n}_*.json')) for n in range(553,558)}

def main_payload():
 parts={f'pass{n}':json.loads(p.read_text()) for n,p in FILES.items()}
 p553,p554,p555,p556,p557=(parts[f'pass{n}'] for n in range(553,558))
 checks={
  'all_owner_certificates_pass':all(p['status']=='PASS' for p in parts.values()),
  'core_is_affine_4_simplex':p553['core']['affine_span_dimension']==4 and len(p553['core']['points'])==5,
  'full_core_affine_group_s5':p553['automorphisms']['order']==120,
  'physical_core_image_d10':p553['automorphisms']['component_image_order']==10,
  'z9_fourth_packet_6561':p554['layers'][-1]['sections']==6561,
  'z9_fourth_image_921':p554['layers'][-1]['distinct_charpolys']==921,
  'future_automaton_counts':[x['minimal_markov_states'] for x in p554['minimal_future_automaton']['layers']]==[41,122,365,1081,921],
  'all_98_fibres_classified':len(p555['catalog'])==98,
  'five_translation_types':len(p555['type_counts'])==5,
  'three_five_cube_fibres':p555['five_cube_result']['count']==3,
  'quartic_level_is_80':p556['quartic_readout']['target_level_size']==80,
  'quartic_blind_orientation_latch_required':p556['odd_switch_test']['same_quartic_invariant'] and p556['odd_switch_test']['A_product_mod5']!=p556['odd_switch_test']['B_product_mod5'],
  'formal_support_pass':p557['status']=='PASS',
  'formal_periods_exact':p557['formalized']['periods_first7']==[312,1560,1560,7800,7800,39000,39000],
 }
 return {
  'schema':'w33.pass553_557.intrinsic_automaton_formal_control.release.v1',
  'status':'PASS' if all(checks.values()) else 'FAIL',
  'headline':{
   'five_point_core':'affine 4-simplex with full S5 affine symmetry; physical component image D10',
   'z9_automaton':'four packets give 921 polynomials; minimal future states 41,122,365,1081,921',
   'fibre_catalog':'98 fibres collapse to five translation-geometric types; three have five parallel 4-cubes',
   'formal':'Lean arithmetic/period interfaces with local-field assumptions explicit',
   'hardware':'quartic readout gates the 80-word fibre but a separate orientation latch distinguishes the odd switch',
  },
  'parts':parts,
  'owner_check_total':sum(len(p.get('checks',{})) for p in parts.values()),
  'release_checks':checks,
  'boundary':'Exact for the fixed-magnitude q=5 cube, the four-packet 6,561-section Z/9 affine family, the stated valuation interfaces, and the compiled control overlay. No full q=5 orbit image, full Z/9 image, or hardware feasibility claim is made.',
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 pl=main_payload();text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Passes 553-557 certificate drift')
 else:
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':pl['status'],'owner_checks':pl['owner_check_total'],'release_checks':sum(pl['release_checks'].values()),'release_total':len(pl['release_checks'])}))
 return 0 if pl['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
