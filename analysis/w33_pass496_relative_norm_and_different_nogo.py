#!/usr/bin/env python3
"""Pass 496: relative norm square theorem and a cyclotomic-different no-go."""
from __future__ import annotations
import argparse, importlib.util, json, math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass496_relative_norm_and_different_nogo.json'
_spec=importlib.util.spec_from_file_location('p493',ROOT/'analysis'/'w33_pass493_mixed_characteristic_falsifiers.py')
P=importlib.util.module_from_spec(_spec);_spec.loader.exec_module(P)
def single_delta(R,c=None):
    c=R.one if c is None else c
    r=int(round(math.log(R.char_order,R.p)));C=P.Cyc(R.p,r);H=P.Heis(R,C)
    F=H.block(H.full_sec(tuple(R.zero for _ in H.pairs)));dF=P.det_bareiss(F,C)
    offs=tuple(c if i==0 else R.zero for i in range(len(H.pairs)))
    d=P.det_bareiss(H.block(H.full_sec(offs)),C);delta=C.sub(d,dF)
    N=abs(C.norm(delta));v=C.vlam(delta);root=math.isqrt(N)
    unit=N//(R.p**v);uroot=math.isqrt(unit)
    return {'ring':R.name,'p':R.p,'character_order':R.char_order,
      'depth':v,'fixed_by_conjugation':C.sigma(C.m-1,delta)==delta,
      'full_norm_digits':len(str(N)),'full_norm_is_square':root*root==N,
      'relative_norm_digits':len(str(root)),'real_prime_valuation':v//2,
      'unit_norm_is_square':uroot*uroot==unit,
      'independent_Galois_embeddings':C.deg//2}
def different_exponent(p,n): return p**(n-1)*(n*p-n-1)
def projective_depth(p,n): return p**(n-1)*(p+1)
def main_payload():
    witnesses=[single_delta(P.Zmod(3,2)),single_delta(P.Zmod(5,2)),single_delta(P.Eisenstein27())]
    comparisons=[]
    for p,n in [(3,2),(5,2),(3,3),(7,2),(11,2)]:
        d=projective_depth(p,n);diff=different_exponent(p,n)
        comparisons.append({'p':p,'n':n,'projective_depth':d,'cyclotomic_different_exponent':diff,'unequal':d!=diff})
    checks={
      'all_real':all(x['fixed_by_conjugation'] for x in witnesses),
      'all_even_depths':all(x['depth']%2==0 for x in witnesses),
      'all_full_norms_square':all(x['full_norm_is_square'] for x in witnesses),
      'all_unit_norms_square':all(x['unit_norm_is_square'] for x in witnesses),
      'sample_different_inequalities':all(x['unequal'] for x in comparisons),
      'symbolic_no_equality_for_odd_primes':all((p+2)%(p-1)!=0 or (p+2)//(p-1)<2 for p in range(3,100,2) if all(p%d for d in range(2,int(p**.5)+1))),
    }
    return {'schema':'w33.pass496.relative_norm_and_different_nogo.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':'If Delta is fixed by conjugation in K/K+, then N_K/Q(Delta)=N_K+/Q(Delta)^2 and v_lambda(Delta) is even.',
      'nogo':'For every odd prime p and n>=2, |P^1(Z/p^n)| differs from the p-adic cyclotomic different exponent.',
      'proof_of_nogo':'Equality would require n(p-1)=p+2. For p=3 this gives n=5/2; for p>=5 the ratio is <2.',
      'witnesses':witnesses,'different_comparisons':comparisons,
      'hardware_bridge':'Only phi(p^r)/2 independent real embeddings are needed for a Galois phase-cycle norm measurement.',
      'checks':checks}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
 pl=main_payload();text=json.dumps(pl,sort_keys=True,separators=(',',':'))+'\n'
 if a.check:
  if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 496 certificate drift')
 else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
 print(json.dumps({'status':pl['status'],'checks':sum(pl['checks'].values()),'total':len(pl['checks'])}))
 return 0 if pl['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
