#!/usr/bin/env python3
"""Explore 12-ray equal-weight Witting tight frames and their overlaps, exact Q(omega)."""
from collections import defaultdict
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
import toe_20261122_witting_qutrit_sic_mub30 as G
from toe_20261122_round6_minimal_ic import get_mats

def equal12():
    ps=[G.P_of(v) for v in G.W.all_rays()]
    coords=lambda M: np.array([int(3*M[i][j][k]) for i in range(4) for j in range(4) for k in range(2)],dtype=np.int64)
    A=np.column_stack([coords(p) for p in ps]);b=coords(tuple(tuple(G.ONE if i==j else G.ZERO for j in range(4)) for i in range(4)))*3
    assert np.max(abs(A@np.array([int(i in (1,3,5,7,12,13,18,19,27,29,33,39)) for i in range(40)])-b))==0
    return A,b

def enumerate_sample(iterations=50,time_per=0.4):
    A,b=equal12();_,B,t=get_mats();rng=np.random.default_rng(2606)
    solutions=set();out=[]
    for k in range(iterations):
        c=rng.normal(size=40)
        q=milp(c,integrality=np.ones(40),bounds=Bounds(np.zeros(40),np.ones(40)),constraints=LinearConstraint(A,b,b),options={'time_limit':time_per,'mip_rel_gap':0.05})
        if q.x is None:continue
        ids=tuple(np.where(q.x>0.5)[0].tolist());
        if ids in solutions:continue
        if len(ids)!=12 or not np.array_equal(A[:,ids].sum(axis=1),b):continue
        rank=np.linalg.matrix_rank(B[:,ids]);solutions.add(ids);out.append((ids,rank))
    overlaps={}
    for i,a in enumerate(out):
        for bb in out[i+1:]:
            n=len(set(a[0])&set(bb[0]))
            if n>=6:
                ids=sorted(set(a[0])|set(bb[0]));rank=np.linalg.matrix_rank(B[:,ids]);overlaps[(n,rank)]=overlaps.get((n,rank),0)+1
                if n>=7 and rank==16: print('POSSIBLE 17',a[0],bb[0],flush=True)
    print('samples',len(solutions),'rank hist',__import__('collections').Counter(r for ids,r in out),'overlaps',overlaps,flush=True)
    return out
if __name__=='__main__':enumerate_sample(100,.5)
