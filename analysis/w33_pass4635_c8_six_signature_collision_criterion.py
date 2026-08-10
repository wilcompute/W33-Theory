#!/usr/bin/env python3
"""Pass 4635 -- a six-signature local criterion for primitive-C8 apartment/star collisions.

For a fixed four-line support, enumerate closed nonbacktracking walks of length 8
whose line-parity support is exactly that target.  Because the target has size 4,
proper-period subtractions cannot contribute to that parity support, so the
primitive degree-four C8 coefficient is raw_count/8.

Every apartment contribution falls into exactly four line-multiplicity species:
 A1 selected 1111, outside 22; A2 selected 1115; A3 selected 1133;
 A4 selected 1111, outside 4.
Every K1,3 contribution falls into exactly two:
 S1 selected 1111, outside 22; S2 selected 1113, outside 2.
Thus C8(apartment)=C8(star) iff the four apartment masses equal the two star
masses.  The GQ(2,2) collision is the exact cancellation 224+64=96+192.
"""
from __future__ import annotations
import itertools,json
from collections import Counter,defaultdict
from pathlib import Path
import w33_pass4573_general_gq_c8_selector_obstruction as p4573
from w33_pass4495_4502_distance_prism_reconstruction import geometry
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS4635_C8_SIX_SIGNATURE_COLLISION_CRITERION.json'

def half_sig(start,steps,trans):
    cur={(start,0,()):1}
    for _ in range(steps):
        z=defaultdict(int)
        for (st,m,ls),c in cur.items():
            for j,li in trans[st]:z[(j,m^(1<<li),tuple(sorted(ls+(li,))))]+=c
        cur=z
    by=defaultdict(lambda:defaultdict(Counter))
    for (st,m,ls),c in cur.items():by[st][m][ls]+=c
    return by

def signature_masses(pts,lines,target):
    dedges,nxt,rev=p4573.nb_tables(pts,lines);tm=p4573.mask(target);T=set(target);ans=Counter()
    for s in range(len(dedges)):
        f=half_sig(s,4,nxt);r=half_sig(s,4,rev)
        for st in set(f)&set(r):
            for m,cf in f[st].items():
                cr=r[st].get(m^tm)
                if not cr:continue
                for a,ca in cf.items():
                    for b,cb in cr.items():
                        C=Counter(a+b);sel=tuple(sorted(C[x] for x in T));out=tuple(sorted(v for x,v in C.items() if x not in T))
                        assert all(x&1 for x in sel) and all(not(x&1) for x in out)
                        ans[(sel,out)]+=ca*cb
    return ans

def choose_supports(lines):
    aps=p4573.apartments(lines);sts=p4573.stars(lines);assert aps and sts
    return aps[0],sts[0]
def dual_gq(pts,lines):
    newpts=list(range(len(lines)));newlines=[]
    for p in range(len(pts)):
        L=frozenset(i for i,x in enumerate(lines) if p in x);newlines.append(L)
    return newpts,newlines

def record(name,pts,lines,expected):
    ap,st=choose_supports(lines);A=signature_masses(pts,lines,ap);S=signature_masses(pts,lines,st)
    ca=sum(A.values())//8;cs=sum(S.values())//8;assert (ca,cs)==expected
    allowedA={((1,1,1,1),(2,2)),((1,1,1,5),()),((1,1,3,3),()),((1,1,1,1),(4,))}
    allowedS={((1,1,1,1),(2,2)),((1,1,1,3),(2,))}
    assert set(A)<=allowedA and set(S)<=allowedS
    def fmt(C):return {(''.join(map(str,k[0]))+'|'+''.join(map(str,k[1]))):v for k,v in sorted(C.items())}
    return {'geometry':name,'apartment_raw_signatures':fmt(A),'star_raw_signatures':fmt(S),'apartment_coefficient':ca,'star_coefficient':cs,'collision':ca==cs}

def main()->int:
    p22,l22=p4573.symplectic_gq22();p24,l24=p4573.qminus_gq24();p42,l42=dual_gq(p24,l24)
    pts,_,lines,*_=geometry()
    rows=[record('GQ(2,2)',p22,l22,(36,36)),record('GQ(2,4)=Q^-(5,2)',p24,l24,(60,36)),record('GQ(4,2)=dual Q^-(5,2)',p42,l42,(2812,792)),record('GQ(3,3)=W33',pts,lines,(712,180))]
    # exact anchor masses
    assert rows[0]['apartment_raw_signatures']=={'1111|22':224,'1115|':64}
    assert rows[0]['star_raw_signatures']=={'1111|22':96,'1113|2':192}
    assert rows[1]['apartment_raw_signatures']=={'1111|22':416,'1115|':64}
    assert rows[2]['apartment_raw_signatures']=={'1111|22':13088,'1111|4':1536,'1115|':4416,'1133|':3456}
    assert rows[3]['apartment_raw_signatures']=={'1111|22':3648,'1111|4':768,'1115|':896,'1133|':384}
    out={'pass':4635,'universal_support_species':{'apartment':['1111|22','1115|','1133|','1111|4'],'K13':['1111|22','1113|2'],'coefficient_rule':'primitive C8 degree-four coefficient = sum(raw signature masses)/8','collision_criterion':'sum of the four apartment masses equals sum of the two K1,3 masses'},'anchors':rows,'GQ22_explanation':'224+64 = 96+192 = 288, hence both coefficients equal 36','theorem':'Primitive-C8 apartment/K1,3 collisions reduce to equality of six local nonbacktracking walk-signature masses. The GQ(2,2) failure is an exact cancellation between different walk species; GQ(2,4), its dual, and W33 break that cancellation.','boundary':'This is a universal local species reduction plus exact anchors. Closed formulas for the six masses as functions of arbitrary (s,t) and embedding data remain OPEN.'}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps(out,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
