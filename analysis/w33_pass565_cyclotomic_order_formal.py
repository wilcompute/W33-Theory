#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
LEAN=ROOT/'formal'/'W33'/'Pass565CyclotomicFiveOrder.lean'
OUT=ROOT/'data'/'w33_pass565_cyclotomic_order_formal.json'

def payload():
 x=sp.symbols('x');f=x**4-5*x**3+10*x**2-10*x+5
 coeff=sp.Poly(f,x).all_coeffs();disc=int(sp.discriminant(f,x));norm=int(abs(sp.Poly(f,x).eval(0)))
 eisen=coeff[0]%5!=0 and all(c%5==0 for c in coeff[1:]) and coeff[-1]%25!=0
 text=LEAN.read_text();names=['shiftedPhiFive','CyclotomicFiveOrder','lambdaBar','shiftedPhiFive_eval','shiftedPhiFive_monic','CompletionInterface']
 checks={
  'lean_file_present':LEAN.exists(),
  'native_adjoinroot_construction':'AdjoinRoot shiftedPhiFive' in text,
  'distinguished_uniformizer_class':'AdjoinRoot.root shiftedPhiFive' in text,
  'shifted_coefficients_exact':coeff==[1,-5,10,-10,5],
  'eisenstein_at_five_exact':eisen,
  'quartic_irreducible_over_Q':sp.Poly(f,x).is_irreducible,
  'uniformizer_norm_five':norm==5,
  'discriminant_five_cubed':disc==125,
  'all_declared_names_present':all(n in text for n in names),
  'no_placeholders':not re.search(r'\b(sorry|admit|axiom)\b',text),
  'completion_boundary_explicit':'stops before' in text and 'CompletionInterface' in text,
 }
 return {'schema':'w33.pass565.cyclotomic_order_formal.v1','status':'PASS' if all(checks.values()) else 'FAIL','algebraic_order':{'definition':'AdjoinRoot of X^4-5X^3+10X^2-10X+5 over Z','degree':4,'eisenstein_prime':5,'constant_norm':norm,'discriminant':disc,'lean_file':str(LEAN.relative_to(ROOT)),'lean_sha256':hashlib.sha256(text.encode()).hexdigest()},'formal_progress':'The integral order and distinguished uniformizer class are now native Lean definitions. Polynomial evaluation, monicity, and the completion interface are theorem-backed/scaffolded in Lean.','boundary':'This does not yet construct the completed field Q_5(zeta_5), prove completeness, identify the maximal ideal, or instantiate the residue and valuation maps. Hosted Lean CI is authoritative for compilation.','checks':checks}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args();p=payload();s=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=s:raise SystemExit('Pass 565 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
 print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
