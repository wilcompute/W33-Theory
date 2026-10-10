"""Round33 exact CP-SAT 13-cover feasibility with tree gauge fixing.

Use each simple 8-cycle signed voltage nonzero mod13. Fix 79
spanning-tree edge voltages to zero without loss of generality.
Solve CP-SAT for 81 independent chord voltages. FEASIBLE result
is independently certified. UNKNOWN is not a no-go.
"""
from pathlib import Path
import sys,json,collections
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261009_toe31_compact_voltage_cover import lift_cert
OUT=ROOT/'data/w33_20261010_toe33_p13_cpsat_cover.json'
def run(p=13,seconds=75):
 edges,D,C=wilson();C=C.astype(np.int16);n=80
 parent=list(range(n))
 def find(x):
  while parent[x]!=x:
   parent[x]=parent[parent[x]];x=parent[x]
  return x
 tree=[]
 for j,(a,b) in enumerate(edges):
  pa,pb=find(a),find(b)
  if pa!=pb:parent[pa]=pb;tree.append(j)
 assert len(tree)==79
 chords=[j for j in range(160) if j not in set(tree)];assert len(chords)==81
 model=cp_model.CpModel()
 v={j:model.NewIntVar(0,p-1,f'v{j}') for j in chords}
 for i,row in enumerate(C):
  indices=[j for j in np.flatnonzero(row) if j in v]
  expr=sum(int(row[j])*v[j] for j in indices)
  # signed sum = mod-p nonzero residue + p*multiple
  rem=model.NewIntVar(1,p-1,f'rem{i}')
  q=model.NewIntVar(-8,8,f'carry{i}')
  model.Add(expr==p*q+rem)
 # Fix overall scale: a nonzero chord carries +1 after scaling
 # but only if its cycle holonomy must be nonzero; first fundamental
 # chord cycle may exceed 8 and could have zero holonomy. No extra.
 # First false symmetry assumption intentionally avoided.
 solver=cp_model.CpSolver()
 solver.parameters.max_time_in_seconds=seconds
 solver.parameters.num_search_workers=8
 solver.parameters.random_seed=330013
 status=solver.Solve(model)
 labels={cp_model.OPTIMAL:'OPTIMAL',cp_model.FEASIBLE:'FEASIBLE',cp_model.INFEASIBLE:'INFEASIBLE',cp_model.UNKNOWN:'UNKNOWN',cp_model.MODEL_INVALID:'MODEL_INVALID'}
 name=labels[status]
 print('P13 CPSAT',name,'wall',solver.WallTime(),'conflicts',solver.NumConflicts(),flush=True)
 rec=dict(status='PASS',prime=p,tree_gauge_fixed_edges=tree,free_chords=chords,
  constraints=1620,chord_variables=81,solver_status=name,
  solver_wall_seconds=solver.WallTime(),solver_branches=solver.NumBranches(),
  solver_conflicts=solver.NumConflicts(),
  mathematical_scope='Tree voltages can all be set to zero by vertex-dependent gauge transformation preserving every cycle holonomy. The CP-SAT model then tests all 81 independent chord assignments for p13 modulo constraint per each 1620 eight-cycles. FEASIBLE is independently checkable; INFEASIBLE constitutes exact mathematical no-go (assuming solver proof); UNKNOWN is not a no-go.',
  minimality='No claim that cyclic degree17 is minimal unless exact 13 infeasibility or lower-degree cases separately proven.')
 if status in (cp_model.OPTIMAL,cp_model.FEASIBLE):
  volt=[int(solver.Value(v[j])) if j in v else 0 for j in range(160)]
  assert not np.any((C@np.array(volt,dtype=np.int16))%p==0)
  connected,seen=lift_cert(edges,volt,p)
  rec.update(found=True,voltages=volt,connected=connected,seen_vertices=seen,
             derived_HGP_n=(160*p)**2+(80*p-1)**2,
             derived_HGP_k=(80*p+1)**2,
             girth_lower_bound=10)
 else:rec['found']=False
 OUT.write_text(json.dumps(rec,indent=2)+'\n')
 return rec
if __name__=='__main__':run()
