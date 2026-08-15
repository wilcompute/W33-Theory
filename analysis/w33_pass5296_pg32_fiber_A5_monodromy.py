#!/usr/bin/env python3
"""Pass5296: the q5 PG(3,2) minimum fiber carries PSL2(5)=A5 monodromy.

Fix a W(3,5) point p.  Its stabilizer in PSp4(5) acts on the six W-lines through
p through a group of order60, namely PSL2(5) ~= A5.  The induced action on
E6/<111111> ~= F2^4 is faithful and transitive on the 15 nonzero fiber vectors.
On the 35 projective lines of PG(3,2) the orbit sizes are 5,10,10,10.  The
5-line orbit is a spread: its five lines are disjoint and partition all 15
projective points.  In the pair-label model, the 35 PG lines are 20 triangles
of K6 plus 15 perfect matchings; A5 splits them as triangle orbits 10+10 and
matching orbits 5+10.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from sympy.combinatorics import Permutation,PermutationGroup
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5296_PG32_FIBER_A5_MONODROMY.json'

def main():
    G=build_W(5);pts=G['pts'];pi={p:i for i,p in enumerate(pts)}
    def norm(v):
        for x in v:
            if x:
                s=pow(x,-1,5);return tuple(s*y%5 for y in v)
        raise ValueError
    def sp(u,v):return (u[0]*v[2]-u[2]*v[0]+u[1]*v[3]-u[3]*v[1])%5
    def pperm(v):
        out=[]
        for x in pts:
            a=sp(x,v);out.append(pi[norm(tuple((x[k]+a*v[k])%5 for k in range(4)))])
        return Permutation(out)
    gens=[pperm(v) for v in ((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,0,1))]
    GP=PermutationGroup(gens);assert GP.order()==4680000
    base,strong=GP.schreier_sims_incremental(base=[0]);stabgens=[g for g in strong if g(0)==0]
    lines0=[li for li,L in enumerate(G['lines']) if 0 in L];assert len(lines0)==6
    lk={tuple(sorted(L)):i for i,L in enumerate(G['lines'])};li={x:i for i,x in enumerate(lines0)}
    six=[]
    for g in stabgens:
        six.append(Permutation([li[lk[tuple(sorted(g(p) for p in G['lines'][L]))]] for L in lines0]))
    H6=PermutationGroup(six);assert H6.order()==60

    pairs=list(itertools.combinations(range(6),2));pidx={p:i for i,p in enumerate(pairs)}
    h15=[]
    for g in H6.generators:
        h15.append(Permutation([pidx[tuple(sorted((g(i),g(j))))] for i,j in pairs]))
    H15=PermutationGroup(h15);assert H15.order()==60 and [len(o) for o in H15.orbits()]==[15]

    masks=[(1<<i)|(1<<j) for i,j in pairs]
    def cls(m):
        if m.bit_count()==4:m^=63
        ij=tuple(i for i in range(6) if (m>>i)&1);return pidx[ij]
    PGlines=set()
    for a,b in itertools.combinations(range(15),2):PGlines.add(tuple(sorted((a,b,cls(masks[a]^masks[b])))))
    assert len(PGlines)==35
    def orb(L):
        S={L};Q=[L]
        while Q:
            x=Q.pop()
            for g in H15.generators:
                y=tuple(sorted(g(i) for i in x))
                if y not in S:S.add(y);Q.append(y)
        return S
    rem=set(PGlines);orbs=[]
    while rem:
        O=orb(next(iter(rem)));rem-=O;orbs.append(O)
    assert sorted(map(len,orbs))==[5,10,10,10]
    def kind(L):
        E=[pairs[i] for i in L];d=Counter(v for e in E for v in e)
        return 'triangle' if len(d)==3 else 'matching'
    profiles=sorted((len(O),dict(Counter(kind(L) for L in O))) for O in orbs)
    assert sorted(x[0] for x in profiles)==[5,10,10,10]
    O5=next(O for O in orbs if len(O)==5);cnt=Counter(i for L in O5 for i in L);assert len(cnt)==15 and set(cnt.values())=={1}
    out={'pass':5296,'status':'THEOREM_Q5_PG32_FIBER_MONODROMY_IS_A5_WITH_INVARIANT_SPREAD',
      'point_stabilizer_image_on_six_lines':'PSL2(5) ~= A5','image_order':60,
      'fiber':'E6/<111111> ~= F2^4','nonzero_fiber_orbit':15,
      'PG3_2_line_orbits':[{'size':len(O),'kind_profile':dict(Counter(kind(L) for L in O))} for O in sorted(orbs,key=len)],
      'invariant_spread':'The unique size-5 line orbit partitions all 15 PG(3,2) points.',
      'interpretation':'The five spread lines correspond to a distinguished A5 orbit of five perfect matchings/V4-type triples inside the 15 pair labels.',
      'boundary':'Finite q5 code-geometry action only; no physical monodromy is asserted.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
