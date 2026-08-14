#!/usr/bin/env python3
"""Pass5085: rank-two Pal V_{1,2} split relation -> line-theta dictionary.

For the standard symplectic basis e1,f1,e2,f2 and a!=0, the three V0
apartment terms in Pal's standard rank-two split relation are represented by
  A0={e1,f1,e2,f2},
  A1={e2+a e1,f2,e1,f1-a f2},
  A2={f1,e2+a e1,e2,f1-a f2}.
They all contain two points on L=<e1,e2> and two on the disjoint line
M=<f1,f2>.  The machine check below verifies that, for q=3 and q=5 and every
a!=0, the three coordinates are exactly a triangle in the line-side local
K_{q+1}: hence a line-theta triple.  Integral orientation can be chosen as
A_ij=R_i-R_j, giving A_01+A_12-A_02=0 before mod-2 reduction.
"""
from __future__ import annotations
import json
from pathlib import Path
from collections import Counter
from analysis.w33_pass5074_gauge_active_chart_tester import build_W
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5085_PAL_V12_LINE_THETA.json'

def norm(v,q):
    for x in v:
        if x%q:
            z=pow(x%q,-1,q);return tuple((z*y)%q for y in v)
    raise ValueError
def smul(a,v,q):return tuple((a*x)%q for x in v)
def add(a,b,q):return tuple((x+y)%q for x,y in zip(a,b))
def sub(a,b,q):return tuple((x-y)%q for x,y in zip(a,b))
def line_points(u,v,q):
    return {norm(add(smul(a,u,q),smul(b,v,q),q),q) for a in range(q) for b in range(q) if a or b}

def check(q):
    G=build_W(q);pidx={p:i for i,p in enumerate(G['pts'])};aidx={A:i for i,A in enumerate(G['apartments'])}
    lineidx={frozenset(L):i for i,L in enumerate(G['lines'])}
    e1=(1,0,0,0);f1=(0,0,1,0);e2=(0,1,0,0);f2=(0,0,0,1)
    L=frozenset(pidx[p] for p in line_points(e1,e2,q));M=frozenset(pidx[p] for p in line_points(f1,f2,q))
    li,mi=lineidx[L],lineidx[M];assert not (L&M)
    rows=[]
    for a in range(1,q):
        u=add(e2,smul(a,e1,q),q);w=sub(f1,smul(a,f2,q),q)
        vecsets=[[e1,f1,e2,f2],[u,f2,e1,w],[f1,u,e2,w]]
        sets=[frozenset(pidx[norm(v,q)] for v in vs) for vs in vecsets]
        ids=[aidx[S] for S in sets]
        assert len(set(ids))==3 and all(len(S&L)==2 and len(S&M)==2 for S in sets)
        hits=[]
        for typ,loc in G['charts']:
            if typ!='L':continue
            inv={v:k for k,v in loc.items()}
            if all(x in inv for x in ids):
                pairs=[inv[x] for x in ids];deg=Counter(t for e in pairs for t in e)
                if len(deg)==3 and set(deg.values())=={2}:hits.append(pairs)
        assert len(hits)==1
        rows.append({'a':a,'apartments':ids,'local_K_edges':[list(x) for x in hits[0]]})
    return {'q':q,'line_pair':[li,mi],'parameters_checked':q-1,'relations':rows}

def main():
    out={'pass':5085,'status':'EXACT_RANK_TWO_RELATION_DICTIONARY','source':'Pal arXiv:2605.06499v3, standard V1,2 split boundary (equation 29 in the paper)',
      'dictionary':{'V1,1':'point-side theta (Pass5075)','standard_V1,2':'line-side theta (this pass)'},
      'integral_orientation':'For three ordered geodesic roots R0,R1,R2, Aij=Ri-Rj gives A01+A12-A02=0; mod 2 this is the theta parity A01+A12+A02=0.',
      'checks':{'q3':check(3),'q5':check(5)},
      'scope':'rank two / genus two specialization; Pal Lemma 4.3 reduces general V1,2 first relations to V1,1 plus standard V1,2 modulo degree-two boundaries',
      'boundary':'This is a relation-type dictionary, not a claim that Pal provides the finite-GQ Pass5066 proof verbatim.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
