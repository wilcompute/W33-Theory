"""Round34 exact local CP-SAT repair around p13 2-cycle near-certificate.

Fix untouched voltages to best stochastic assignment and solve
complete 1620 nonzero eight-cycle constraints with a limited set
of 16 then 32/48 incident edge variables. Extract reproducible
feasible witness if any, else report each neighborhood UNSAT/UNKNOWN
without extrapolating to global infeasibility.
"""
from pathlib import Path
import sys,json,math
import numpy as np
from ortools.sat.python import cp_model
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'analysis'))
from w33_20261009_toe26_css_matching_family import wilson
from w33_20261009_toe31_compact_voltage_cover import lift_cert
OUT=ROOT/'data/w33_20261010_toe34_p13_local_exact_repair.json'
def verify(volt,C,ed,p):
 x=np.asarray(volt,dtype=np.int32)
 viol=np.flatnonzero((C@x)%p==0)
 return len(viol),viol
def repair(p=13,limit_each=25):
 base=json.loads((ROOT/'data/w33_20261010_toe34_p13_breakout_voltage.json').read_text())
 voltage=np.asarray(base['best_voltages'],dtype=np.int32)
 ed,D,C=wilson();C=C.astype(np.int32)
 original,bad=verify(voltage,C,ed,p);assert original==2
 bad_sites=set(int(j) for ci in bad for j in np.flatnonzero(C[ci]))
 rng=np.random.default_rng(340131)
 groups=[sorted(bad_sites)]
 for count in (28,48,72):
  # edges ranked by co-occurrences with immediate 8-cycle neighbors
  score=np.zeros(160,dtype=np.int32)
  for j in bad_sites:
   for ci in np.flatnonzero(C[:,j]):
    score+=np.abs(C[ci]).astype(np.int32)
  ordering=sorted((j for j in range(160) if j not in bad_sites),key=lambda j:(-int(score[j]),int(j)))
  groups.append(sorted(list(bad_sites)+ordering[:max(0,count-len(bad_sites))]))
 records=[];winner=None
 for num,free in enumerate(groups):
  model=cp_model.CpModel()
  vs={j:model.NewIntVar(0,p-1,f'v{j}') for j in free}
  for ci,row in enumerate(C):
   touched=np.flatnonzero(row)
   variable=[j for j in touched if j in vs]
   constant=sum(int(row[j])*int(voltage[j]) for j in touched if j not in vs)
   if not variable:
    assert constant%p!=0
    continue
   expression=constant+sum(int(row[j])*vs[j] for j in variable)
   rem=model.NewIntVar(1,p-1,f'rem{ci}')
   carry=model.NewIntVar(-40,40,f'carry{ci}')
   model.Add(expression==p*carry+rem)
  for j,v in vs.items():model.AddHint(v,int(voltage[j]))
  solver=cp_model.CpSolver();solver.parameters.max_time_in_seconds=limit_each
  solver.parameters.num_search_workers=8
  solver.parameters.random_seed=340131+num
  status=solver.Solve(model)
  names={cp_model.OPTIMAL:'OPTIMAL',cp_model.FEASIBLE:'FEASIBLE',
   cp_model.INFEASIBLE:'INFEASIBLE',cp_model.UNKNOWN:'UNKNOWN',
   cp_model.MODEL_INVALID:'MODEL_INVALID'}
  name=names[status]
  row=dict(free_variables=len(free),free_edge_indices=free,solver_status=name,
      solver_seconds=solver.WallTime(),branches=solver.NumBranches())
  if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
   arr=voltage.copy()
   for j in free:arr[j]=solver.Value(vs[j])
   score,_=verify(arr,C,ed,p);assert score==0
   conn,n=lift_cert(ed,arr,p)
   row.update(zero_8cycles=score,connected=conn,vertices=n)
   winner=arr.tolist()
   records.append(row)
   print('P13 EXACT LOCAL FOUND!',len(free),conn,n,flush=True)
   break
  records.append(row)
  print('P13 local',len(free),name,'seconds',solver.WallTime(),flush=True)
 result=dict(status='PASS',source_prior_best_zero_cycles=original,source_prior_bad_cycle_ids=bad.tolist(),
  search_neighborhoods=records,valid_p13_certificate_found=winner is not None,
  scope='Each INFEASIBLE local neighborhood rules out repair while all other voltages are frozen; it is NOT global p13 infeasibility. UNKNOWN means solver inconclusive. Only a FOUND witness with independently verified nonzero 1620 holonomies is a valid p13 cover.')
 if winner is not None:
  result['p13_voltages']=winner
  result['HGP_n']=(160*p)**2+(80*p-1)**2
  result['HGP_k']=(80*p+1)**2
 OUT.write_text(json.dumps(result,indent=2)+'\n')
 return result
if __name__=='__main__':repair()
