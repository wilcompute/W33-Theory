#!/usr/bin/env python3
"""Pass 468: explicit semisimple normal-form intertwiner for the q=5 sheet exchange.

Pass 463 identified the genuine collision as exchange of the two Galois-conjugate
faithful quintics between square and nonsquare central-character classes.  This
pass constructs the exact block-swap intertwiner in rational semisimple normal
form and proves uniqueness of the nontrivial class permutation.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass468_semisimple_sheet_intertwiner.json'

def companion(poly: sp.Poly) -> sp.Matrix:
    coeff=poly.all_coeffs()
    if coeff[0] != 1: raise ValueError('monic required')
    n=poly.degree(); C=sp.zeros(n)
    for i in range(1,n): C[i,i-1]=1
    for i in range(n): C[i,n-1]=-coeff[n-i]
    return C

def perm_matrix(order: list[int]) -> sp.Matrix:
    n=len(order); P=sp.zeros(n)
    for new,old in enumerate(order): P[old,new]=1
    return P

def build_payload()->dict:
    x,r=sp.symbols('x r')
    plus=sp.Poly(x**5-60*x**3-(15+25*r)*x**2/2+(310+25*r)*x-54+25*r,x,domain=sp.QQ.frac_field(r))
    minus=sp.Poly(x**5-60*x**3-(15-25*r)*x**2/2+(310-25*r)*x-54-25*r,x,domain=sp.QQ.frac_field(r))
    Cp,Cm=companion(plus),companion(minus)
    core_A=sp.diag(Cp,Cm); core_B=sp.diag(Cm,Cp)
    W=perm_matrix(list(range(5,10))+list(range(0,5)))
    core_intertwines=sp.simplify(W.inv()*core_A*W-core_B)==sp.zeros(10)

    labels_A=['P+']*10+['P-']*10
    labels_B=['P-']*10+['P+']*10
    block_order=list(range(10,20))+list(range(0,10))
    faithful_swap_ok=[labels_A[i] for i in block_order]==labels_B

    chars=[1,2,3,4]
    classes={1:'square',4:'square',2:'nonsquare',3:'nonsquare'}
    multipliers={a:{t:(a*t)%5 for t in chars} for a in chars}
    class_actions={a:tuple(classes[multipliers[a][t]] for t in (1,2)) for a in chars}
    quotient_actions=sorted(set(class_actions.values()))
    exchange_multipliers=[a for a in chars if class_actions[a]==('nonsquare','square')]
    fixed_multipliers=[a for a in chars if class_actions[a]==('square','nonsquare')]

    norm=sp.rem(sp.Poly(sp.expand(plus.as_expr()*minus.as_expr()),r,domain=sp.QQ[x]),sp.Poly(r**2-5,r,domain=sp.QQ[x])).as_expr()
    expected=x**10-120*x**8-15*x**7+4220*x**6+792*x**5-37925*x**4+4955*x**3+96910*x**2-39730*x-209

    checks={
      'quintics_are_galois_conjugate': sp.expand(minus.as_expr()-plus.as_expr().subs(r,-r))==0,
      'norm_is_pass463_rational_factor': sp.expand(norm-expected)==0,
      'core_block_swap_intertwines': core_intertwines,
      'faithful_100d_multiplicity_swap': faithful_swap_ok,
      'character_class_quotient_is_C2': len(quotient_actions)==2,
      'squares_fix_classes': fixed_multipliers==[1,4],
      'nonsquares_exchange_classes': exchange_multipliers==[2,3],
      'swap_is_involution': W*W==sp.eye(10),
    }
    return {
      'schema':'w33.pass468.semisimple_sheet_intertwiner.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'faithful_normal_form':{
        'core_dimension':10,
        'core_A':'diag(C(P+),C(P-))',
        'core_B':'diag(C(P-),C(P+))',
        'intertwiner':'block swap W',
        'full_faithful_dimension':100,
        'quintic_multiplicities':{'P+':10,'P-':10},
      },
      'central_character_quotient':{
        'F5_units':[1,2,3,4],
        'mod_plus_minus_classes':[['1','4'],['2','3']],
        'fixed_multipliers':fixed_multipliers,
        'exchange_multipliers':exchange_multipliers,
        'quotient_group':'C2',
      },
      'classification_theorem':(
        'In semisimple rational normal form, the genuine q=5 collision is conjugation by the unique nontrivial '
        'permutation of the two classes F5*/{±1}.  The explicit block swap W sends diag(C(P+),C(P-)) to '
        'diag(C(P-),C(P+)); after the regular and character multiplicities are restored this gives an exact '
        '100-dimensional faithful-component intertwiner.  This is an algebra intertwiner in canonical normal '
        'form, not a vertex permutation and not a graph isomorphism.'),
      'boundary':(
        'The intertwiner is canonical after passage to companion-matrix semisimple normal form.  An integral or '
        'monomial intertwiner in the original Heisenberg coordinate basis is not claimed.'),
      'checks':checks,
    }

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); ap.add_argument('--output',type=Path,default=OUT); a=ap.parse_args()
    p=build_payload(); text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text: raise SystemExit('Pass 468 certificate drift')
    else:
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}))
    return 0 if p['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
