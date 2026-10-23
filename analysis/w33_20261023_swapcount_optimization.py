#!/usr/bin/env python3
"""Unrestricted four-layer W33 SWAP-count objective; UNKNOWN is inconclusive."""
import json,sys
from pathlib import Path
from ortools.sat.python import cp_model
try:
 from analysis.w33_20261022_five_followups_round5 import A,transvection,routing_four_layers
except ImportError:
 from w33_20261022_five_followups_round5 import A,transvection,routing_four_layers

def run(limit=45, max_swaps=35):
    goal=transvection(0);n=40;depth=4
    model=cp_model.CpModel();p=[];moving=[]
    for t in range(depth):
        row=[]
        for v in range(n):
            allowed=[v]+[u for u in range(n) if A[v,u]]
            row.append(model.NewIntVarFromDomain(cp_model.Domain.FromValues(allowed),f'partner_{t}_{v}'))
        model.AddAllDifferent(row)
        for v in range(n):model.AddElement(row[v],row,v)
        for v in range(n):
            b=model.NewBoolVar(f'active_{t}_{v}')
            model.Add(row[v]!=v).OnlyEnforceIf(b)
            model.Add(row[v]==v).OnlyEnforceIf(b.Not())
            moving.append(b)
        p.append(row)
    for token in range(n):
        position=token
        for t in range(depth):
            nextpos=model.NewIntVar(0,n-1,f'position_{t}_{token}')
            model.AddElement(position,p[t],nextpos)
            position=nextpos
        model.Add(position==int(goal[token]))
    model.Add(sum(moving)<=max_swaps*2)
    # Known optimum upper bound 36; the <=35 test intentionally has no witness.
    if max_swaps>=36:
        layout=routing_four_layers()["all_schedules"][0]["layers"]
        for t,layer in enumerate(layout):
            vals=list(range(n))
            for u,v in layer:vals[u],vals[v]=v,u
            for v in range(n):model.AddHint(p[t][v],vals[v])
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=float(limit)
    solver.parameters.num_search_workers=8
    solver.parameters.random_seed=20261023
    result=solver.Solve(model)
    data={"status":solver.StatusName(result),"anchor":0,"depth":4,"swap_budget":max_swaps,
          "wall_seconds":solver.WallTime(),"branches":solver.NumBranches(),"conflicts":solver.NumConflicts(),
          "proof_of_lower_bound_36":result==cp_model.INFEASIBLE,
          "unknown_not_a_proof":True}
    if result in (cp_model.FEASIBLE,cp_model.OPTIMAL):
        layers=[];positions=list(range(n))
        for t in range(depth):
            pairs=[]
            for v in range(n):
                u=solver.Value(p[t][v])
                if u>v:
                    assert A[v,u] and solver.Value(p[t][u])==v
                    pairs.append([v,u]);positions[v],positions[u]=positions[u],positions[v]
            assert len({x for uv in pairs for x in uv})==2*len(pairs)
            layers.append(pairs)
        dest=[0]*n
        for v,tok in enumerate(positions):dest[tok]=v
        assert tuple(dest)==goal
        data.update(layers=layers,swaps=sum(map(len,layers)))
    return data

if __name__=="__main__":
    d=run(int(sys.argv[1]) if len(sys.argv)>1 else 45,int(sys.argv[2]) if len(sys.argv)>2 else 35)
    data=json.dumps(d,indent=2)+"\n"
    if len(sys.argv)>3:Path(sys.argv[3]).write_text(data,encoding="utf8")
    else:print(data)
