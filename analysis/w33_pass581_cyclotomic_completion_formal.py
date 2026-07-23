#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass581_cyclotomic_completion_formal.json'
LEAN=ROOT/'formal'/'W33'/'Pass581CyclotomicCompletion.lean'
PREV=ROOT/'formal'/'W33'/'Pass575CyclotomicDVRKernel.lean'

def payload():
    x=sp.symbols('x');f=x**4-5*x**3+10*x**2-10*x+5
    text=LEAN.read_text();prev=PREV.read_text()
    mod5=sp.Poly(f,x,modulus=5).as_expr()
    checks={
      'shifted_polynomial_reduces_to_x4_mod5':sp.expand(mod5-x**4)==0,
      'principal_kernel_theorem_imported':'theorem residueIdeal_eq_lambda_span' in prev,
      'quotient_equivalence_defined':'def residueQuotientEquiv' in text,
      'first_isomorphism_theorem_used':'quotientKerEquivOfSurjective' in text,
      'equal_ideal_transport_used':'Ideal.quotEquivOfEq' in text,
      'quotient_target_ZMod5':'≃+* ZMod 5' in text,
      'adic_completion_constructed':'AdicCompletion uniformizerIdeal CyclotomicFiveOrder' in text,
      'completion_algebra_map_defined':'def completionMap' in text,
      'completed_uniformizer_defined':'def completedLambda' in text,
      'no_sorry_admit_axiom':not re.search(r'\b(sorry|admit|axiom)\b',text),
      'remaining_DVR_boundary_explicit':'completion_is_dvr' in text and 'ramification_index_four' in text and 'residue_degree_one' in text,
    }
    return {
      'schema':'w33.pass581.cyclotomic_completion_formal.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'algebra':{
        'order':'Z[lambda]/(lambda^4-5lambda^3+10lambda^2-10lambda+5)',
        'uniformizer_ideal':'(lambda)','residue_quotient':'O_5/(lambda) ~= F_5',
        'reduction_mod5':str(mod5),'completion':'AdicCompletion (lambda) O_5',
      },
      'lean':{
        'source':str(LEAN.relative_to(ROOT)),
        'quotient_equivalence':'residueQuotientEquiv',
        'completion_type':'CyclotomicFiveAdicCompletion',
        'completed_uniformizer':'completedLambda',
      },
      'checks':checks,
      'boundary':'The quotient equivalence and λ-adic completion type are native Lean definitions. Locality, Noetherianity in the required instance form, the DVR structure, normalized valuation, e=4, and f=1 remain explicit theorem obligations; local Lean compilation is not claimed unless CI reports it.'
    }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 581 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
