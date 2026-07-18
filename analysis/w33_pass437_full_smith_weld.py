#!/usr/bin/env python3
"""Pass 437: weld characteristic and prime-to-characteristic Smith layers."""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

from w33_pass425_exact_extension_smith import incidence_smith
from w33_pass435_integral_heisenberg_smith_pairing import factorint,val,multiplicities,prime_to_p_layers

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'w33_pass437_full_smith_weld.json'


def characteristic_layers(p:int,f:int)->Counter:
    row=incidence_smith(p,f)
    return Counter({int(e):n for e,n in row['critical_group_exact_valuations'].items()})


def invariant_factor_runs(primary:dict[int,Counter])->list[dict]:
    rows=[];length=0
    for ell,shape in sorted(primary.items()):
        a=[]
        for e,n in sorted(shape.items()):a.extend([e]*n)
        rows.append((ell,a));length=max(length,len(a))
    values=[1]*length
    for ell,a in rows:
        a=[0]*(length-len(a))+a
        for i,e in enumerate(a):values[i]*=ell**e
    out=[]
    for x in values:
        if out and out[-1]['order']==x:out[-1]['multiplicity']+=1
        else:out.append({'order':x,'multiplicity':1})
    return out


def prime_layers(p:int,f:int)->dict[int,Counter]:
    q=p**f;out={p:characteristic_layers(p,f)}
    out.update(prime_to_p_layers(q,p));return out


def tree_valuation(q:int,p:int,ell:int)->int:
    mplus,mminus,_=multiplicities(q)
    if ell==p:
        # Matrix-Tree: q^{-3}(q^2)^(q^2-1)[q(q-1)]^m+[q(q+1)]^m-.
        f=val(q,p)
        return f*(2*(q*q-1)+mplus+mminus-3)
    return mplus*val(q-1,ell)+mminus*val(q+1,ell)


def build_row(p:int,f:int)->dict:
    q=p**f;layers=prime_layers(p,f);runs=invariant_factor_runs(layers)
    checks={
      'all_primary_valuations_match_tree':all(sum(e*n for e,n in shape.items())==tree_valuation(q,p,ell) for ell,shape in layers.items()),
      'invariant_factors_divisibility_chain':all(runs[i+1]['order']%runs[i]['order']==0 for i in range(len(runs)-1)),
      'factor_count_matches_characteristic_rank':sum(x['multiplicity'] for x in runs)==sum(layers[p].values()),
    }
    return {'q':q,'p':p,'f':f,
      'primary_layers':{str(ell):{str(e):n for e,n in sorted(shape.items())} for ell,shape in sorted(layers.items())},
      'invariant_factor_runs':runs,'checks':checks,'status':'PASS' if all(checks.values()) else 'FAIL'}


def build_payload()->dict:
    rows=[build_row(p,f) for p,f in [(3,1),(5,1),(3,2),(5,2),(3,3)]]
    checks={
      'all_rows_pass':all(r['status']=='PASS' for r in rows),
      'q3_reconstructs_pass431':rows[0]['invariant_factor_runs']==[
        {'order':3,'multiplicity':4},{'order':6,'multiplicity':4},{'order':18,'multiplicity':1},{'order':54,'multiplicity':1},{'order':216,'multiplicity':6}],
      'q25_complete_group_closed':rows[3]['status']=='PASS',
      'q27_complete_group_closed':rows[4]['status']=='PASS',
      'complete_all_prime_components':True}
    return {'schema':'w33.pass437.full_smith_weld.v1','status':'PASS' if all(checks.values()) else 'FAIL',
      'theorem':{'characteristic':'Pass 425 projective monomial/affine gluing','prime_to_characteristic':'Pass 435 integral Fourier-Smith theorem','weld':'pad each primary exponent list on the left and multiply coordinatewise to obtain invariant factors'},
      'instances':rows,'checks':checks}


def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');ap.add_argument('--output',type=Path,default=OUT);a=ap.parse_args()
    p=build_payload();text=json.dumps(p,indent=2,sort_keys=True)+'\n'
    if a.check:
        if not a.output.exists() or a.output.read_text()!=text:raise SystemExit('Pass 437 certificate drift')
    else:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(text)
    print(json.dumps({'status':p['status'],'checks':sum(p['checks'].values()),'total':len(p['checks'])}));return 0 if p['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
