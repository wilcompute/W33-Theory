#!/usr/bin/env python3
"""Pass5304: exact q11 weight-20 dual density condition and search wall.

For q=11 the P-carriers have size24 and any two distinct carriers meet in 0 or 2
W-points.  If S is a weight-20 dual support and d_p is the number of selected
carriers through point p, then every d_p is even and sum d_p=20*24=480.  If e is
the number of adjacent selected carrier pairs (intersection size2), double
counting pair intersections gives

    2e = sum_p C(d_p,2).

For even d, C(d,2)>=d/2, with equality only at d=0,2.  Hence e>=120, with equality
iff the selected carriers cover exactly 240 W-points twice.  In that equality
case every selected carrier has graph degree12.  Thus the conjectural
K10,10+2-factor support is exactly the minimum-overlap boundary for a dual20.

Two bounded HiGHS searches (fixed carrier; then fixed adjacent carrier and binary
double-cover variables) found no incumbent before timeout.  This is explicitly
NOT an infeasibility certificate and does not prove nonexistence or q11 d=121.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
from analysis.w33_pass5293_allodd_rank_reduction_q11 import points,line_bases,norm,sp
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/PART_W33_PASS5304_Q11_DUAL20_DENSITY_WALL.json'

def null2(rows,q):
    A=[[x%q for x in r] for r in rows];piv=[];rr=0
    for c in range(4):
        k=next((i for i in range(rr,len(A)) if A[i][c]),None)
        if k is None:continue
        A[rr],A[k]=A[k],A[rr];iv=pow(A[rr][c],-1,q);A[rr]=[(x*iv)%q for x in A[rr]]
        for i in range(len(A)):
            if i!=rr and A[i][c]:
                f=A[i][c];A[i]=[(A[i][j]-f*A[rr][j])%q for j in range(4)]
        piv.append(c);rr+=1
    free=[c for c in range(4) if c not in piv];B=[]
    for f in free:
        x=[0]*4;x[f]=1
        for i,p in enumerate(piv):x[p]=(-A[i][f])%q
        B.append(tuple(x))
    return B

def linepts(u,v,q,pi):
    S={pi[norm(v,q)]}
    for a in range(q):S.add(pi[norm(tuple((u[k]+a*v[k])%q for k in range(4)),q)])
    return tuple(sorted(S))

def carriers(q=11):
    P=points(q);pi={p:i for i,p in enumerate(P)};C={}
    for u,v in line_bases(q):
        if sp(u,v,q)==0:continue
        H=linepts(u,v,q,pi);a,b=null2([(u[2],u[3],-u[0],-u[1]),(v[2],v[3],-v[0],-v[1])],q)
        Hp=linepts(a,b,q,pi);C[tuple(sorted(set(H)|set(Hp)))]=1
    return P,sorted(C)

def main():
    P,C=carriers();assert len(P)==1464 and len(C)==7381 and {len(x) for x in C}=={24}
    B0=set(C[0]);hist=Counter(len(B0&set(B)) for B in C[1:])
    assert hist==Counter({0:5940,2:1440})
    # PSp4(11) is transitive on these polar-pair carriers, so the fixed-carrier
    # intersection census applies to every carrier.
    total_incidence=20*24;lower_pairs=total_incidence//2;lower_edges=lower_pairs//2
    assert lower_edges==120
    out={'pass':5304,'status':'THEOREM_Q11_DUAL20_REQUIRES_AT_LEAST_120_SELECTED_CARRIER_EDGES_WITH_SEARCH_WALL',
      'q':11,'W_points':1464,'P_components':7381,'carrier_size':24,
      'fixed_carrier_intersections':{'0':5940,'2':1440},
      'dual20_double_count':'2e = sum_p binom(d_p,2), with every d_p even and sum d_p=480.',
      'edge_lower_bound':120,
      'equality':'e=120 iff every nonzero d_p=2, i.e. 240 W-points are covered exactly twice; then every selected carrier has degree12.',
      'predicted_shell':'K10,10 plus a 2-factor on each half has 20 vertices, degree12 and exactly120 edges, so it saturates the necessary overlap bound.',
      'bounded_search':{'unrestricted_fixed_coordinate':'35s HiGHS timeout, no incumbent','double_cover_fixed_adjacent_pair':'35s HiGHS timeout, no incumbent'},
      'boundary':'Solver timeout is not a lower-bound certificate. No q11 dual20 existence/nonexistence or footprint d=121 theorem is claimed.'}
    OUT.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
