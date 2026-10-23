#!/usr/bin/env python3
"""Unrestricted depth-three W33 transvection routing via CP-SAT.

Exact model: each layer is any W33-edge matching, represented by
an involutory neighbor-or-self partner permutation, with all 40 token
trajectories explicitly enforced. Timeout UNKNOWN never means infeasible.
"""
from __future__ import annotations
import json,sys
from pathlib import Path
from ortools.sat.python import cp_model
try:
    from analysis.w33_20261022_five_followups_round5 import A,transvection
except ImportError:
    from w33_20261022_five_followups_round5 import A,transvection


def run(seconds=35,depth=3):
    goal=transvection(0)
    model=cp_model.CpModel()
    partner=[]
    for t in range(depth):
        vals=[]
        for v in range(40):
            allowed=[v]+[int(u) for u in range(40) if A[v,u]]
            vals.append(model.NewIntVarFromDomain(
                cp_model.Domain.FromValues(sorted(allowed)),f'p_{t}_{v}'))
        for v in range(40):
            model.AddElement(vals[v],vals,v)  # involution, each nonfixed pair an edge
        model.AddAllDifferent(vals)
        partner.append(vals)
    for token in range(40):
        pos=token
        for t in range(depth):
            dest=model.NewIntVar(0,39,f'x_{t+1}_{token}')
            model.AddElement(pos,partner[t],dest)
            pos=dest
        model.Add(pos==int(goal[token]))
    if depth==4:
        try:
            from analysis.w33_20261022_five_followups_round5 import routing_four_layers
        except ImportError:
            from w33_20261022_five_followups_round5 import routing_four_layers
        known=routing_four_layers()['all_schedules'][0]['layers']
        for t in range(4):
            chosen=list(range(40))
            for u,v in known[t]:chosen[u],chosen[v]=v,u
            for v in range(40):model.AddHint(partner[t][v],int(chosen[v]))
    solver=cp_model.CpSolver()
    solver.parameters.max_time_in_seconds=float(seconds)
    solver.parameters.num_search_workers=8
    solver.parameters.random_seed=20261023
    outcome=solver.Solve(model)
    status=solver.StatusName(outcome)
    report={"status":status,"requested_layers":depth,"n":40,
       "graph":"W33 12-regular collinearity",
       "exhaustive_proof_of_infeasibility":outcome==cp_model.INFEASIBLE,
       "feasible_route_found":outcome in (cp_model.FEASIBLE,cp_model.OPTIMAL),
       "termination_semantics":"UNKNOWN means inconclusive; only INFEASIBLE is an exhaustive no-go",
       "solver_wall_seconds":float(solver.WallTime()),
       "branches":int(solver.NumBranches()),
       "conflicts":int(solver.NumConflicts())}
    if report["feasible_route_found"]:
        moves=[];positions=list(range(40))
        for t in range(depth):
            swaps=[]
            for v in range(40):
                u=solver.Value(partner[t][v])
                if u>v:
                    assert A[v,u] and solver.Value(partner[t][u])==v
                    swaps.append([v,u])
                    positions[v],positions[u]=positions[u],positions[v]
            assert len({a for pair in swaps for a in pair})==2*len(swaps)
            moves.append(swaps)
        dest=[0]*40
        for v,token in enumerate(positions):dest[token]=v
        assert tuple(dest)==goal
        report["exact_layers"]=moves
        report["swaps"]=sum(len(z) for z in moves)
    return report


if __name__=="__main__":
    out=json.dumps(run(int(sys.argv[1]) if len(sys.argv)>1 else 35,
                       int(sys.argv[3]) if len(sys.argv)>3 else 3),indent=2)+"\n"
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(out,encoding="utf-8")
    else:print(out,end="")
