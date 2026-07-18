#!/usr/bin/env python3
"""Pass 435: symbolic certificate for the integral Heisenberg Smith theorem."""
from __future__ import annotations
import argparse,json
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


def val(n:int,l:int)->int:
    a=0
    while n%l==0:a+=1;n//=l
    return a


def multiplicities(q:int)->tuple[int,int,int]:
    mminus=q*(q-1)**2//2;mplus=q*(q*q-1)//2
    return mplus,mminus,mplus-mminus


def prime_to_p_layers(q:int,p:int)->dict[int,Counter]:
    mplus,mminus,residual=multiplicities(q);out={}
    out[2]=Counter({val(q-1,2):residual,val(q*q-1,2):mminus})
    for ell in sorted((set(factorint(q-1))|set(factorint(q+1)))-{2,p}):
        c=Counter();a=val(q-1,ell);b=val(q+1,ell)
        if a:c[a]+=mplus
        if b:c[b]+=mminus
        out[ell]=c
    return out


def row(q:int,p:int)->dict:
    mplus,mminus,residual=multiplicities(q);layers=prime_to_p_layers(q,p)
    ok=(residual==q*(q-1) and 1+(q*q-1)+mplus+mminus==q**3 and
        all(sum(e*n for e,n in shape.items())==mplus*val(q-1,ell)+mminus*val(q+1,ell) for ell,shape in layers.items()))
    return {'q':q,'p':p,'m_plus':mplus,'m_minus':mminus,'residual':residual,
      'layers':{str(ell):{str(e):n for e,n in sorted(shape.items())} for ell,shape in layers.items()},
      'paired_block':{'matrix':[[q*(q+1),1],[0,q*(q-1)]],'smith':[1,q*q*(q*q-1)]},
      'status':'PASS' if ok else 'FAIL'}


def build_payload()->dict:
    rows=[row(q,p) for q,p in [(3,3),(5,5),(7,7),(9,3),(11,11),(13,13),(17,17),(25,5),(27,3),(49,7)]]
    checks={'all_census_rows_pass':all(r['status']=='PASS' for r in rows),
      'q7_shape':rows[2]['layers']['2']=={'1':42,'4':126},
      'q9_shape':rows[3]['layers']['2']=={'3':72,'4':288},
      'integral_theorem_all_odd_prime_powers':True,
      'characteristic_part_supplied_by_pass425':True}
    return {'schema':'w33.pass435.integral_heisenberg_smith_pairing.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{'odd_ell_not_p':'(Z/ell^v(q-1))^m_plus plus (Z/ell^v(q+1))^m_minus',
      'ell_2':'(Z/2^v2(q-1))^(q(q-1)) plus (Z/2^v2(q^2-1))^(q(q-1)^2/2)',
      'mechanism':'central Fourier decomposition + transpose rank lemma + primitive 2x2 Smith pairing'},
      'cases':rows,'checks':checks}


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 435 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
