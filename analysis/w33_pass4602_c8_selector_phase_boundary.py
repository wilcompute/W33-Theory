#!/usr/bin/env python3
"""Pass 4602 -- exact C8-alone phase boundary on the first three exhausted GQ anchors.

Pass4573 showed GQ(2,2) fails C8-alone apartment selection and sampled GQ(2,4).
This pass exhausts the entire primitive-C8 degree-four spectrum of Q^-(5,2)=
GQ(2,4). Exactly 1080 four-line supports have coefficient 60 and they are
exactly the 1080 apartments. Thus the s=2,t=4 geometry works, while s=t=2 fails.
Together with Pass4548, GQ(3,3) also works (coefficient712, 1620 apartments).
The full symbolic classification in arbitrary (s,t) remains open.
"""
from __future__ import annotations
import itertools,json,math
from collections import Counter,defaultdict
from pathlib import Path
import w33_pass4573_general_gq_c8_selector_obstruction as p4573
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4602_C8_SELECTOR_PHASE_BOUNDARY.json'

def global_c8_poly(pts,lines):
    dedges,nxt,rev=p4573.nb_tables(pts,lines);total=Counter()
    for s in range(len(dedges)):
        f=p4573.half(s,4,nxt);r=p4573.half(s,4,rev)
        for st in set(f)&set(r):
            rr=r[st]
            for m,c in f[st].items():
                for n,d in rr.items():total[m^n]+=c*d
    out=Counter()
    for m,v in total.items():
        if m.bit_count()==4:
            assert v%8==0;out[v//8]+=1
    return out

def main():
    p,l=p4573.qminus_gq24();assert (len(p),len(l))==(27,45)
    d=global_c8_poly(p,l);zero=math.comb(45,4)-sum(d.values());d[0]=zero
    expected=Counter({0:75375,6:25920,32:12960,10:12960,16:9720,4:6480,12:2160,24:1620,60:1080,36:720})
    assert d==expected
    aps=p4573.apartments(l);assert len(aps)==1080
    tables=p4573.prepare_c8(p,l)
    assert {p4573.primitive_c8_coeff(tables,p4573.mask(S)) for S in aps}=={60}
    assert d[60]==len(aps)
    old=json.loads((ROOT/'data/PART_W33_PASS4573_GENERAL_GQ_C8_SELECTOR_OBSTRUCTION.json').read_text())
    assert old['counterexample']['primitive_C8_degree4_apartment_coefficient']==36
    w33=json.loads((ROOT/'data/PART_W33_PASS4548_C7_C8_HIGHER_BODY_TOMOGRAPHY.json').read_text())
    assert '1620' in str(w33) and '712' in str(w33)
    out={'pass':4602,'exact_anchors':{
      'GQ(2,2)':{'C8_alone_selects_apartments':False,'apartment_coefficient':36,'collision':'60 K1,3 supports also coefficient36'},
      'GQ(2,4)':{'C8_alone_selects_apartments':True,'apartment_coefficient':60,'apartments':1080,'coefficient60_supports':1080,'full_degree4_spectrum':{str(k):v for k,v in sorted(d.items())}},
      'GQ(3,3)':{'C8_alone_selects_apartments':True,'apartment_coefficient':712,'apartments':1620}},
      'phase_boundary':'the minimal GQ(2,2) collision disappears in GQ(2,4); C8-alone selection is not controlled by s=2 alone',
      'universal_fallback':'C6 degree-two reconstructs line adjacency for every thick GQ, hence apartments as induced C4s',
      'boundary':'Three anchors are exhausted exactly. A closed symbolic criterion in arbitrary (s,t) is still OPEN.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({**out,'exact_anchors':{k:({kk:vv for kk,vv in v.items() if kk!='full_degree4_spectrum'} if isinstance(v,dict) else v) for k,v in out['exact_anchors'].items()}},indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
