#!/usr/bin/env python3
"""Pass5215 helper: construct the 16 projective collineations fixing apartment 0.

Generate Sp(4,3) from symplectic transvections, quotient its central +/-I by
projective point action, and retain the stabilizer of the base apartment.  The
resulting 16 permutations act on all 1620 apartments and are consumed by the
orbit-complete C++ radius-seven census.
"""
from __future__ import annotations
from collections import deque
from pathlib import Path
from analysis.w33_pass5074_gauge_active_chart_tester import build_W

def main(path='/tmp/w33_pass5215_q3_stab.txt'):
    q=3;G=build_W(q);pts=G['pts'];pidx={p:i for i,p in enumerate(pts)}
    def sym(x,y):return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1])%3
    def norm(v):
        for x in v:
            if x:
                z=pow(x,-1,3);return tuple(z*y%3 for y in v)
        raise ValueError
    def trans(v):
        M=[[0]*4 for _ in range(4)]
        for j in range(4):
            e=tuple(int(k==j) for k in range(4));s=sym(e,v)
            w=tuple((e[k]+s*v[k])%3 for k in range(4))
            for i in range(4):M[i][j]=w[i]
        return tuple(sum(M,[]))
    def mm(A,B):return tuple(sum(A[4*i+k]*B[4*k+j] for k in range(4))%3 for i in range(4) for j in range(4))
    def mv(A,v):return tuple(sum(A[4*i+k]*v[k] for k in range(4))%3 for i in range(4))
    I=tuple(int(i==j) for i in range(4) for j in range(4));gens=[trans(v) for v in pts]
    group={I};Q=deque([I])
    while Q:
        A=Q.popleft()
        for B in gens:
            C=mm(A,B)
            if C not in group:group.add(C);Q.append(C)
    assert len(group)==51840
    apt0=G['apartments'][0];aidx={A:i for i,A in enumerate(G['apartments'])};actions={};stab=[]
    for M in group:
        pa=tuple(pidx[norm(mv(M,p))] for p in pts)
        if pa in actions:continue
        actions[pa]=1
        if frozenset(pa[p] for p in apt0)==apt0:
            perm=tuple(aidx[frozenset(pa[p] for p in A)] for A in G['apartments'])
            assert perm[0]==0;stab.append(perm)
    assert len(actions)==25920 and len(stab)==16
    p=Path(path);p.write_text(str(len(stab))+' '+str(len(G['apartments']))+'\n'+'\n'.join(' '.join(map(str,P)) for P in stab)+'\n')
    print(p)
if __name__=='__main__':main()
