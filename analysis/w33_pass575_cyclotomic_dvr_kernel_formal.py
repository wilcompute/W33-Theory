#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass575_cyclotomic_dvr_kernel_formal.json'
LEAN=ROOT/'formal'/'W33'/'Pass575CyclotomicDVRKernel.lean'

def payload():
 x=sp.symbols('x');f=x**4-5*x**3+10*x**2-10*x+5
 unit=-x**3+5*x**2-10*x+10
 s=LEAN.read_text()
 required=(
  'theorem five_eq_lambda_mul',
  'theorem five_mem_lambda_span',
  'theorem mk_mem_lambda_span_of_residue_zero',
  'theorem residueIdeal_eq_lambda_span',
  'def orderLocalCertificate',
 )
 bad=tuple(t for t in ('sorry','admit','axiom') if re.search(r'\b'+t+r'\b',s))
 checks={
  'quartic_relation_exact':sp.expand(f-(x**4-5*x**3+10*x**2-10*x+5))==0,
  'five_factor_identity':sp.expand(5-x*unit-f)==0,
  'shifted_polynomial_mod5_is_X4':sp.Poly(f,x,modulus=5)==sp.Poly(x**4,x,modulus=5),
  'all_required_theorems_present':all(t in s for t in required),
  'uses_AdjoinRoot_surjectivity':'AdjoinRoot.mk_surjective' in s,
  'uses_divX_decomposition':'Polynomial.divX_mul_X_add' in s,
  'uses_exact_ZMod_divisibility':'ZMod.intCast_zmod_eq_zero_iff_dvd' in s,
  'no_placeholders':not bad,
  'kernel_equality_statement_exact':'residueIdeal = Ideal.span ({lambdaBar} : Set CyclotomicFiveOrder)' in s,
 }
 return {
  'schema':'w33.pass575.cyclotomic_dvr_kernel_formal.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'formal_file':str(LEAN.relative_to(ROOT)),
  'theorem':{'kernel':'ker(residueMap) = (lambdaBar)','key_relation':'5 = lambdaBar * (-lambdaBar^3 + 5 lambdaBar^2 - 10 lambdaBar + 10)','method':'Use p = p.divX * X + C(p.coeff 0); residue zero makes the constant coefficient divisible by five, and the defining quartic makes five divisible by lambdaBar.'},
  'remaining_boundary':['construct the 5-adic completion','prove completeness and field structure','derive the DVR valuation and total ramification internally'],
  'checks':checks,
  'boundary':'The Python owner certifies the exact algebra and source custody. Lean compilation is authoritative only when the repository workflow reports success.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 575 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
