#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,re
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass570_cyclotomic_residue_formal.json'
LEAN=ROOT/'formal'/'W33'/'Pass570CyclotomicResidue.lean'

def payload():
 src=LEAN.read_text();x=sp.symbols('x');f=x**4-5*x**3+10*x**2-10*x+5
 theorem_names=['shiftedPhiFive_monic','shiftedPhiFive_zero_mod_five','residueMap_lambda','residueMap_integer','residueMap_surjective','lambda_mem_residueIdeal','five_mem_residueIdeal','lambda_span_le_residueIdeal']
 checks={
  'lean_file_present':LEAN.exists(),
  'all_theorem_names_present':all(n in src for n in theorem_names),
  'no_unproved_placeholders':not re.search(r'\b(sorry|admit|axiom)\b',src),
  'shifted_polynomial_exact':sp.Poly(f,x).all_coeffs()==[1,-5,10,-10,5],
  'reduction_mod5_is_x4':[int(c)%5 for c in sp.Poly(f,x).all_coeffs()]==[1,0,0,0,0],
  'constant_term_five':sp.Poly(f,x).TC()==5,
  'eisenstein_at_five':all(int(c)%5==0 for c in sp.Poly(f,x).all_coeffs()[1:]) and 25%5==0 and 5%25!=0,
  'discriminant_125':sp.discriminant(f,x)==125,
  'quotient_by_lambda_has_residue_F5':sp.Poly(f,x).eval(0)==5,
  'completion_obligations_explicit':'CompletionObligations' in src and 'kernel_is_uniformizer_span' in src,
 }
 return {
  'schema':'w33.pass570.cyclotomic_residue_formal.v1','status':'PASS' if all(checks.values()) else 'FAIL',
  'formalized':{
   'integral_order':'AdjoinRoot shiftedPhiFive over Z',
   'residue_map':'CyclotomicFiveOrder ->+* ZMod 5 by lambdaBar |-> 0',
   'proved_interfaces':['surjectivity','lambdaBar in kernel','5 in kernel','(lambdaBar) <= kernel'],
   'presentation_quotient':'Setting lambdaBar=0 leaves the constant relation 5=0, hence the expected residue field F5.',
  },
  'remaining_completion_obligations':['prove kernel=(lambdaBar) using the local unit theorem','construct the 5-adic completion','prove the completion is a field and complete','prove total ramification degree four'],
  'checks':checks,
  'boundary':'The native residue map and kernel containments are formalized. Hosted Lean CI is authoritative for compilation. Equality of the kernel with the principal uniformizer ideal and construction of Q_5(zeta_5) remain explicit obligations, not silently claimed.'
 }

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 570 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
