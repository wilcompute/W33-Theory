#!/usr/bin/env python3
"""Reproducible q=7 adjacency CSS CP-SAT parity-feasibility search.

Proof of d=14 would require INFEASIBLE in BOTH fixed-pair orbit cases.
UNKNOWN is NOT an absence proof. Does not modify repository files.
"""
import itertools,time,json
from ortools.sat.python import cp_model

def geometry():
    q=7
    def norm(v):
        z=pow(next(x for x in v if x),-1,q)
        return tuple(z*x%q for x in v)
    pts=sorted({norm(v) for v in itertools.product(range(q),repeat=4) if any(v)})
    def B(a,b):
        return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%q
    A=[[j for j,y in enumerate(pts) if i!=j and B(x,y)==0] for i,x in enumerate(pts)]
    assert len(A)==400 and all(len(row)==56 for row in A)
    return A

def case(A,kind,j,seconds=90,workers=8):
    model=cp_model.CpModel()
    x=[model.NewBoolVar("x"+str(i)) for i in range(400)]
    one=model.NewConstant(1)
    for neighbors in A:
        model.AddBoolXOr([x[t] for t in neighbors]+[one])
    model.Add(x[0]==1);model.Add(x[j]==1)
    model.Add(sum(x)>=10);model.Add(sum(x)<=12)
    s=cp_model.CpSolver()
    s.parameters.max_time_in_seconds=seconds
    s.parameters.num_search_workers=workers
    t=time.time();status=s.Solve(model)
    record=dict(pair_type=kind,pair=[0,j],status=s.StatusName(status),
                seconds=round(time.time()-t,3),conflicts=s.NumConflicts(),branches=s.NumBranches())
    if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        support=[i for i in range(400) if s.Value(x[i])]
        assert all(sum(t in support for t in row)%2==0 for row in A)
        record["weight"]=len(support);record["support"]=support
    return record

def main():
    A=geometry()
    adjacent=next(j for j in range(1,400) if j in A[0])
    far=next(j for j in range(1,400) if j not in A[0])
    result=[case(A,"adjacent",adjacent),case(A,"nonadjacent",far)]
    proof=all(r['status']=='INFEASIBLE' for r in result)
    print(json.dumps({"geometry":"W(3,7)","code":"[[400,48,d]], 10<=d<=14 previously certified",
      "status":"PROVED_d14" if proof else "OPEN_AFTER_CP_SAT",
      "cases":result,"boundary":"UNKNOWN is inconclusive; no solver timeout proves distance 14."},indent=2))
    return result

if __name__=='__main__':main()
