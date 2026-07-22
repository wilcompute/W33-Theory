#!/usr/bin/env python3
"""Pass 557: fail-closed formal support for the q=5 valuation laws.

Lean formalizes the residue/period arithmetic and theorem interfaces. The
cyclotomic Hensel and companion-matrix order facts remain explicit hypotheses;
the executable Pass 552 certificate supplies those exact computations.
"""
from __future__ import annotations
import argparse,json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass557_formal_valuation_support.json'
FILES={
 'constant':ROOT/'formal'/'W33'/'Pass557ConstantValuation.lean',
 'period':ROOT/'formal'/'W33'/'Pass557OddPeriodLift.lean',
 'root':ROOT/'formal'/'W33.lean',
}

def odd_period(k:int)->int:
 return 312*5**(k//2)

def main_payload():
 d552=json.loads((ROOT/'data'/'w33_pass552_q5_constant_and_switch_valuations.json').read_text())
 periods=[x['period'] for x in d552['odd_switch_family']['precision_periods']]
 expected=[odd_period(k) for k in range(1,8)]
 texts={k:p.read_text() for k,p in FILES.items()}
 banned=('sorry','axiom','admit')
 theorem_names=(
  'constantOddBase_period','constantOddBase_mod','constant_odd_formula',
  'constant_four_divides_formula','oddPeriod_step','oddPeriod_first_seven',
  'oddPeriod_closed_first_seven','odd_switch_period','odd_switch_lift_valuation')
 checks={
  'pass552_certificate_pass':d552['status']=='PASS',
  'period_formula_matches_first7':periods==expected,
  'lift_valuations_1_3_5_7':[x['matrix_minus_identity_vpi'] for x in d552['odd_switch_family']['order_lifting']]==[1,3,5,7],
  'constant_formula_verified_window_50000':d552['constant_family']['verified_modular_window']==50000,
  'lean_files_present':all(p.exists() for p in FILES.values()),
  'all_theorem_names_present':all(any(n in t for t in texts.values()) for n in theorem_names),
  'no_unproved_placeholders':not any(b in t.lower() for t in texts.values() for b in banned),
  'root_imports_both_modules':all(n in texts['root'] for n in ('Pass557ConstantValuation','Pass557OddPeriodLift')),
 }
 return {
  'schema':'w33.pass557.formal_valuation_support.v1',
  'status':'PASS' if all(checks.values()) else 'FAIL',
  'formalized':{
   'constant':'mod-20 residue controller and explicit Hensel/LTE certificate interface',
   'odd_switch':'two-step period recurrence, first-seven closed form, and explicit matrix-order lift interface',
   'periods_first7':periods,
   'lift_valuations':[1,3,5,7],
  },
  'boundary':'Lean certifies the finite arithmetic, recurrence, and theorem interfaces. The cyclotomic Hensel/LTE and companion-matrix order inputs remain explicit hypotheses; hosted Lean CI is the authoritative compile test.',
  'checks':checks,
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 pl=main_payload();text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 557 certificate drift')
 else:
  a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':pl['status'],'checks':sum(pl['checks'].values()),'total':len(pl['checks'])}))
 return 0 if pl['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
