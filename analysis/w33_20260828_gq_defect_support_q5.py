#!/usr/bin/env python3
"""General ovoid-defect support theorem and the q=5 lower-bound upgrade.

For a generalized quadrangle GQ(q,q), let N be line-point incidence and A the
line-intersection graph. If x is the indicator of a point set of ovoid size
q^2+1 and Nx = 1+d, then sum(d)=0 and

    A d = (q-1) d.

Indeed NN^T=(q+1)I+A, while d is orthogonal to both the principal and least
eigenspaces. Thus every nonzero ovoid defect is an integer eigenfunction in
the r=q-1 eigenspace.

A self-contained support bound follows from a coordinate with |d|=M:
its neighbors sum to (q-1)M and its distance-two shell sums to -qM. Since
every coordinate has magnitude <=M, any nonzero d has support at least 2q.
If the deficiency is delta, exactly delta coordinates equal -1 (missed lines)
and the total positive mass is delta, so support(d)<=2 delta. Hence delta>=q.

Equality delta=q is rigid: all nonzero entries are +/-1; the positive and
negative supports are q-cliques in the line graph with no cross adjacency.
In a generalized quadrangle those q-cliques are punctured pencils, and the two
pencil centers must be collinear with their common hinge omitted. Therefore
EVERY deficiency-q configuration is a punctured-pencil defect dipole.

For W(3,5), exact backtracking rules out both an ovoid and the unique dipole
type up to flag transitivity. Consequently def(W(3,5)) >= 6. Holotrade has an
explicit feasible 26-set missing 12 lines, so the current certified interval is

    6 <= def(W(3,5)) <= 12.

This strengthens the parallel Holotrade q=5 commit, whose own scope correctly
said that dipole infeasibility alone did not exclude another deficiency-5
shape. The support/equality theorem closes exactly that gap.
"""
from __future__ import annotations
import itertools,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"PART_W33_20260828_GQ_DEFECT_SUPPORT_Q5.json"

def norm(v,q):
    i=next(k for k,x in enumerate(v) if x%q);z=pow(v[i]%q,-1,q)
    return tuple((z*x)%q for x in v)
def form(u,v,q):
    return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2])%q
def geometry(q):
    pts=sorted({norm(v,q) for v in itertools.product(range(q),repeat=4) if any(v)})
    idx={v:i for i,v in enumerate(pts)};lines=set()
    for ia,ib in itertools.combinations(range(len(pts)),2):
        a,b=pts[ia],pts[ib]
        if form(a,b,q):continue
        span=set()
        for s,t in itertools.product(range(q),repeat=2):
            if s==t==0:continue
            span.add(idx[norm(tuple((s*a[k]+t*b[k])%q for k in range(4)),q)])
        if len(span)==q+1:lines.add(tuple(sorted(span)))
    lines=sorted(lines)
    n=(q+1)*(q*q+1)
    assert len(pts)==len(lines)==n and all(len(L)==q+1 for L in lines)
    return pts,lines

def solve_target(lines,point_lines,target,size,limit=1):
    n=len(point_lines)
    allowed={p for p in range(n) if all(target[li]>0 for li in point_lines[p])}
    cand=[[p for p in L if p in allowed] for L in lines]
    cnt=[0]*len(lines);chosen=[];sol=[];nodes=0
    def rec():
        nonlocal nodes
        nodes+=1
        if len(sol)>=limit or len(chosen)>size:return
        unmet=[]
        for li,t in enumerate(target):
            if cnt[li]>t:return
            need=t-cnt[li]
            if need:
                F=[p for p in cand[li] if p not in chosen and
                   all(cnt[j]<target[j] for j in point_lines[p])]
                if len(F)<need:return
                unmet.append((len(F),-need,li,F))
        if not unmet:
            if len(chosen)==size:sol.append(tuple(sorted(chosen)))
            return
        remaining=sum(target[i]-cnt[i] for i in range(len(lines)))
        q1=len(point_lines[0])
        if len(chosen)+(remaining+q1-1)//q1>size:return
        _,ng,_,F=min(unmet);need=-ng
        for sub in itertools.combinations(F,need):
            d=Counter()
            for p in sub:
                for j in point_lines[p]:d[j]+=1
            if any(cnt[j]+z>target[j] for j,z in d.items()):continue
            chosen.extend(sub)
            for j,z in d.items():cnt[j]+=z
            rec()
            for j,z in d.items():cnt[j]-=z
            del chosen[-len(sub):]
            if len(sol)>=limit:return
    rec()
    return sol,nodes

def line_graph_params(lines,q):
    n=len(lines);adj=[set() for _ in range(n)]
    for i,j in itertools.combinations(range(n),2):
        if set(lines[i])&set(lines[j]):adj[i].add(j);adj[j].add(i)
    deg={len(x) for x in adj};assert deg=={q*(q+1)}
    lam=set();mu=set()
    for i,j in itertools.combinations(range(n),2):
        c=len(adj[i]&adj[j]);(lam if j in adj[i] else mu).add(c)
    assert lam=={q-1} and mu=={q+1}
    return {"v":n,"k":q*(q+1),"lambda":q-1,"mu":q+1,
            "eigenvalues":[q*(q+1),q-1,-(q+1)]}

def instance(q):
    _,lines=geometry(q);n=len(lines);size=q*q+1
    pls=[[] for _ in range(n)]
    for li,L in enumerate(lines):
        for p in L:pls[p].append(li)
    params=line_graph_params(lines,q)
    ovoid,ov_nodes=solve_target(lines,pls,[1]*n,size,limit=1)
    hinge=0;a,b=lines[hinge][0],lines[hinge][1]
    miss=sorted(set(pls[a])-{hinge});doub=sorted(set(pls[b])-{hinge})
    assert len(miss)==len(doub)==q
    target=[1]*n
    for l in miss:target[l]=0
    for l in doub:target[l]=2
    dip,dip_nodes=solve_target(lines,pls,target,size,limit=10)
    return {
      "q":q,"points":n,"lines":n,"set_size":size,
      "line_graph":params,
      "ovoid_exists":bool(ovoid),"ovoid_backtrack_nodes":ov_nodes,
      "deficiency_q_dipole_exists":bool(dip),"dipole_solution_count_capped":len(dip),
      "dipole_backtrack_nodes":dip_nodes,
      "dipole_profile":{"0":q,"1":n-2*q,"2":q},
      "profile_incidence_sum":n,
      "required_incidence_sum":(q+1)*size
    }

def main():
    q3=instance(3);q5=instance(5)
    assert not q3["ovoid_exists"] and q3["deficiency_q_dipole_exists"]
    assert not q5["ovoid_exists"] and not q5["deficiency_q_dipole_exists"]
    assert q5["profile_incidence_sum"]==q5["required_incidence_sum"]==156
    out={
      "schema":"w33.20260828.gq-defect-support-q5.v1","status":"PASS",
      "general_theorem":{
        "defect_eigen_equation":"A_line d = (q-1)d for Nx=1+d and |x|=q^2+1",
        "nonzero_support_lower_bound":"|supp(d)| >= 2q",
        "deficiency_lower_bound":"nonzero deficiency delta >= q",
        "equality_classification":"delta=q iff the defect is a punctured-pencil dipole: q missed arms at a, q doubled arms at collinear b, common hinge omitted from both defect supports",
        "proof_key":"At a maximum coordinate M, neighbor sum is (q-1)M and distance-2 sum is -qM; equality forces two q-cliques with no cross adjacency."
      },
      "instances":{"q3":q3,"q5":q5},
      "q5_consequence":{
        "deficiency_5_possible":False,
        "proved_lower_bound":6,
        "parallel_Holotrade_feasible_upper_bound":12,
        "certified_interval":[6,12],
        "parallel_commit":"a41a53f5d4e70f30c4ab1e44679bece9a6bedf30"
      },
      "theorem":"For W(3,5), deficiencies 1-4 are excluded by the 2q eigenfunction support bound; deficiency 5 would have to be a punctured-pencil dipole; the representative dipole is exactly infeasible and flag transitivity covers all representatives. Since W(3,5) has no ovoid (also independently verified here), def(W(3,5))>=6.",
      "boundary":"The upper bound 12 is imported from Holotrade's explicit feasible witness and is not re-derived by this script. No claim is made that 6 is attained."
    }
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","q3_dipole":True,"q5_dipole":False,"q5_interval":[6,12],
                      "q5_nodes":{"ovoid":q5["ovoid_backtrack_nodes"],"dipole":q5["dipole_backtrack_nodes"]}}))
if __name__=="__main__":main()
