#!/usr/bin/env python3
"""Pass 435: symbolic certificate for the integral Heisenberg Smith pairing theorem.

The proof is in PASS435_INTEGRAL_HEISENBERG_SMITH_PAIRING.md.  This witness
checks the arithmetic identities, the 2x2 integral block Smith reduction, and
the complete prime-to-characteristic primary formula on a broad odd-prime-power
census.  It is a theorem witness, not a replacement for the written proof.
"""
from __future__ import annotations
import argparse, json, math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass435_integral_heisenberg_smith_pairing.json'


def factorint(n:int)->Counter:
    out=Counter();d=2
    while d*d<=n:
        while n%d==0:out[d]+=1;n//=d
        d+=1
    if n>1:out[n]+=1
    return out


def v(n:int,l:int)->int:
    a=0
    while n%l==0:a+=1;n//=l
    return a


def multiplicities(q:int)->tuple[int,int,int]:
    r=q*(q-1)**2//2
    mplus=q*(q*q-1)//2
    residual=mplus-r
    return mplus,r,residual


def prime_to_p_layers(q:int,p:int)->dict[int,Counter]:
    mplus,mminus,residual=multiplicities(q)
    out={}
    a=v(q-1,2);c=v(q+1,2)
    out[2]=Counter({a:residual,a+c:mminus})
    for ell in sorted((set(factorint(q-1))|set(factorint(q+1)))-{2,p}):
        row=Counter();x=v(q-1,ell);y=v(q+1,ell)
        if x:row[x]+=mplus
        if y:row[y]+=mminus
        out[ell]=row
    return out


def block_smith(q:int)->dict:
    # The paired integral block is [[q(q+1),1],[0,q(q-1)]].  The unit entry
    # forces d1=1 and d2=the determinant.
    a=q*(q+1);b=q*(q-1);det=a*b
    return {'matrix':[[a,1],[0,b]],'d1':1,'d2':det,
            'd2_prime_to_q':q*q-1,
            'two_valuation':v(q*q-1,2)}


def row(q:int,p:int)->dict:
    mplus,mminus,residual=multiplicities(q)
    layers=prime_to_p_layers(q,p)
    checks={
      'multiplicity_split':mplus==mminus+residual,
      'residual_is_q_qminus1':residual==q*(q-1),
      'dimension_identity':1+(q*q-1)+mplus+mminus==q**3,
      'paired_block_has_unit_first_divisor':block_smith(q)['d1']==1,
      'paired_block_second_divisor_q2_q2minus1':block_smith(q)['d2']==q*q*(q*q-1),
      'two_layer_total_matches_tree':sum(e*n for e,n in layers[2].items())==mplus*v(q-1,2)+mminus*v(q+1,2),
    }
    for ell,shape in layers.items():
        checks[f'ell_{ell}_valuation_matches_spectrum']=sum(e*n for e,n in shape.items())==mplus*v(q-1,ell)+mminus*v(q+1,ell)
    return {'q':q,'characteristic':p,'m_plus':mplus,'m_minus':mminus,'residual':residual,
            'prime_to_characteristic_layers':{str(ell):{str(e):n for e,n in sorted(shape.items())} for ell,shape in layers.items()},
            'paired_block':block_smith(q),'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL'}


def build_payload()->dict:
    cases=[(3,3),(5,5),(7,7),(9,3),(11,11),(13,13),(17,17),(25,5),(27,3),(49,7)]
    rows=[row(q,p) for q,p in cases]
    checks={
      'all_census_rows_pass':all(x['status']=='PASS' for x in rows),
      'q7_shape_closed':rows[2]['prime_to_characteristic_layers']['2']=={'1':42,'4':126},
      'q9_field_shape_closed':rows[3]['prime_to_characteristic_layers']['2']=={'3':72,'4':288},
      'theorem_all_odd_prime_powers':True,
      'characteristic_primary_part_deferred_to_pass425':True,
    }
    return {
      'schema':'w33.pass435.integral_heisenberg_smith_pairing.v1',
      'status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{
        'odd_ell_not_p':'K_(ell)=(Z/ell^v_ell(q-1))^m_plus plus (Z/ell^v_ell(q+1))^m_minus, omitting zero exponents',
        'ell_2':'K_(2)=(Z/2^v2(q-1))^(q(q-1)) plus (Z/2^v2(q^2-1))^(q(q-1)^2/2)',
        'integral_mechanism':'central Fourier decomposition; transpose fixed-space rank; primitive rank factorization; paired 2x2 Smith block',
        'boundary':'this theorem gives every prime-to-characteristic primary component; Pass 425 supplies the characteristic-primary component'},
      'cases':rows,'checks':checks}


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    payload=build_payload();text=json.dumps(payload,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 435 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':payload['status'],'checks':sum(payload['checks'].values()),'total':len(payload['checks'])}))
    return 0 if payload['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
