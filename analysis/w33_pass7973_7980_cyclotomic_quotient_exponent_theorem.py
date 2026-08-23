#!/usr/bin/env python3
"""Pass7973-7980 (outside-box): cyclotomic exponent theorem behind the purity tower.

Parallel Pass7341 observed experimentally that pure prime-power cyclotomic support
produces elementary quotients while the mixed d=9 support produces exponent 9.
The pure implication is in fact an elementary polynomial theorem.  This pass also
records the correct boundary: the converse is not forced by characteristic data
alone for an arbitrary integral module.
"""
from __future__ import annotations
import json
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS7973_7980_CYCLOTOMIC_QUOTIENT_EXPONENT_THEOREM.json'
x=sp.symbols('x')

def phi_prime_power(p,r):return sp.cyclotomic_poly(p**r,x,polys=True)

def main():
    checks=[]
    for p,r in [(2,1),(2,2),(2,3),(3,1),(3,2),(13,1)]:
        f=phi_prime_power(p,r);assert int(f.eval(1))==p
        q=sp.div(f-sp.Poly(p,x),sp.Poly(x-1,x));assert q[1].is_zero
        checks.append({'p':p,'r':r,'Phi':str(f.as_expr()),'Q':str(q[0].as_expr())})
    # Mixed prime-power support: product of s distinct cyclotomic factors has
    # value p^s at x=1, hence p^s annihilates the quotient by the same argument.
    f3=phi_prime_power(3,1);f9=phi_prime_power(3,2);m=f3*f9
    assert int(m.eval(1))==9
    q=sp.div(m-sp.Poly(9,x),sp.Poly(x-1,x));assert q[1].is_zero
    out={
      'schema':'w33.pass7973_7980.cyclotomic_quotient_exponent_theorem.v1','status':'PASS','passes':'7973-7980','outside_box':True,
      'theorem_single_factor':'Let M be an integral finite-order operator with minimal polynomial Phi_{p^r}. Since Phi_{p^r}(1)=p, write Phi_{p^r}(x)-p=(x-1)Q(x) with Q in Z[x]. Evaluating at M gives pI=(I-M)(-Q(M)); therefore p annihilates coker(I-M). If |det(I-M)|=p^n, the cokernel is exactly (Z/p)^n.',
      'multi_factor_bound':'If the minimal polynomial is the product of s distinct p-power cyclotomic factors, its value at 1 is p^s, so the cokernel exponent divides p^s.',
      'Leech_d9':'Phi_3 Phi_9 has s=2, hence exponent divides 9; Pass7645 measured (Z/3)^2 x (Z/9)^2, so exponent 9 saturates the bound.',
      'tower_consequence':['E8 d=3: elementary F3 quotient is forced once Phi3-only support is known','E8/Leech d=4 and Leech d=8: elementary F2 quotient is forced by Phi4/Phi8-only support','Leech d=13: elementary F13 quotient is forced by Phi13-only support'],
      'correction_to_empirical_purity_slogan':'Pure single prime-power cyclotomic support => elementary quotient is a theorem. The reverse implication for arbitrary mixed integral modules is not proved by characteristic-polynomial support alone; Pass7341 established it empirically for the six computed lattice cases.',
      'symbolic_checks':checks,
      'claim_boundary':'Integral module/cyclotomic arithmetic theorem; existence or nondegeneracy of a descended polar form is an additional statement.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'PASS','pure_implies_elementary':True,'mixed_bound':'p^s'}))
if __name__=='__main__':main()
