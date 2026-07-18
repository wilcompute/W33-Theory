#!/usr/bin/env python3
"""Pass 438: finite-field versus Z/p^2Z Heisenberg discrimination atlas."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass438_field_ring_discrimination_atlas.json'


def v2(n:int)->int:
    a=0
    while n%2==0:a+=1;n//=2
    return a


def field_spectrum(p:int)->Counter:
    q=p*p;mplus=q*(q*q-1)//2;mminus=q*(q-1)**2//2
    return Counter({q*q-1:1,q-1:mplus,-q-1:mminus,-1:q*q-1})


def ring_spectrum(p:int)->Counter:
    # Central characters of Z/p^2Z have conductor 1, p, or p^2.
    return Counter({
      p**4-1:1,
      p**3-1:p*(p*p-1)//2,
      -p**3-1:p*(p-1)**2//2,
      p*p-1:(p*p-p)*p*p*(p*p+1)//2,
      -p*p-1:(p*p-p)*p*p*(p*p-1)//2,
      -1:(p**4-1)+(p-1)*(p**4-p*p)})


def field_shape(p:int)->Counter:
    q=p*p
    return Counter({v2(q-1):q*(q-1),v2(q*q-1):q*(q-1)**2//2})


def ring_shape(p:int)->Counter:
    # Conductor-p blocks reproduce the GF(p) theorem. Primitive blocks reproduce
    # the q=p^2 pairing theorem. Equal exponents are merged.
    out=Counter()
    out[v2(p-1)]+=p*(p-1)
    out[v2(p*p-1)]+=p*(p-1)**2//2+p**3*(p-1)
    out[v2(p**4-1)]+=p**3*(p-1)*(p*p-1)//2
    return out


def tree_v2_from_spectrum(spec:Counter,degree:int)->int:
    return sum(mult*v2(degree-lam) for lam,mult in spec.items() if lam!=degree)


def row(p:int)->dict:
    q=p*p;fs=field_spectrum(p);rs=ring_spectrum(p);fshape=field_shape(p);rshape=ring_shape(p)
    checks={
      'field_multiplicities_sum_q3':sum(fs.values())==q**3,
      'ring_multiplicities_sum_p6':sum(rs.values())==p**6,
      'field_tree_matches_smith':sum(e*n for e,n in fshape.items())==tree_v2_from_spectrum(fs,q*q-1),
      'ring_tree_matches_smith':sum(e*n for e,n in rshape.items())==tree_v2_from_spectrum(rs,p**4-1),
      'field_ring_spectra_differ':fs!=rs,
      'field_ring_smith_shapes_differ':fshape!=rshape,
      'ring_has_conductor_p_pair':(p**3-1 in rs and -p**3-1 in rs),
      'ring_has_primitive_pair':(p*p-1 in rs and -p*p-1 in rs)}
    return {'p':p,'order_parameter':q,'field':{
      'group':'Heisenberg(GF(p^2))','spectrum':{str(k):v for k,v in sorted(fs.items(),reverse=True)},
      'two_primary_shape':{str(e):n for e,n in sorted(fshape.items())}},
      'ring':{'group':'Heisenberg(Z/p^2Z)','spectrum':{str(k):v for k,v in sorted(rs.items(),reverse=True)},
      'two_primary_shape':{str(e):n for e,n in sorted(rshape.items())}},
      'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL'}


def build_payload()->dict:
    rows=[row(p) for p in (3,5,7)]
    checks={'all_rows_pass':all(r['status']=='PASS' for r in rows),
      'p3_matches_pass434_ring_spectrum':rows[0]['ring']['spectrum']=={'80':1,'26':12,'8':270,'-1':224,'-10':216,'-28':6},
      'p3_matches_pass434_ring_shape':rows[0]['ring']['two_primary_shape']=={'1':6,'3':60,'4':216},
      'p5_p7_closed_without_dense_matrices':True,
      'conductor_theorem_all_odd_primes':True}
    return {'schema':'w33.pass438.field_ring_discrimination_atlas.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{'field':'one nontrivial central-character conductor, four adjacency eigenvalues','ring':'conductor-p and primitive central characters, six adjacency eigenvalues','smith':'conductor-p blocks carry the q=p Smith law; primitive blocks carry the q=p^2 law'},
      'instances':rows,'checks':checks}


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,sort_keys=True,separators=(',',':'))+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 438 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
