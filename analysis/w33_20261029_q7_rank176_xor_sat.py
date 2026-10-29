#!/usr/bin/env python3
"""Independent q7 CSS distance CP-SAT search: 176-rank XOR parity basis.

The q7 adjacency matrix has rank 176, kernel dim224, logical dim48.
Failure of time-limited search is never a proof that d=14.
"""
import itertools,json,time
from ortools.sat.python import cp_model
Q=7

def geometry():
 def norm(v):
  inv=pow(next(x for x in v if x),-1,Q)
  return tuple(x*inv%Q for x in v)
 P=sorted({norm(v) for v in itertools.product(range(Q),repeat=4) if any(v)})
 def symp(a,b):
  return (a[0]*b[1]-a[1]*b[0]+a[2]*b[3]-a[3]*b[2])%Q
 A=[sum(1<<j for j,y in enumerate(P) if i!=j and symp(x,y)==0) for i,x in enumerate(P)]
 assert len(A)==400 and all(x.bit_count()==56 for x in A)
 return A

def independent_rows(rows):
 piv={};out=[]
 for r in rows:
  w=r
  while w:
   k=w.bit_length()-1
   if k in piv:w^=piv[k]
   else:piv[k]=w;out.append(r);break
 return out

def try_pair(A,R,name,j,seconds=50):
 m=cp_model.CpModel()
 x=[m.NewBoolVar('x'+str(i)) for i in range(400)]
 one=m.NewConstant(1)
 for mask in R:
  m.AddBoolXOr([x[i] for i in range(400) if mask>>i&1]+[one])
 m.Add(x[0]==1);m.Add(x[j]==1)
 m.Add(sum(x)>=10);m.Add(sum(x)<=12)
 s=cp_model.CpSolver()
 s.parameters.num_search_workers=8
 s.parameters.max_time_in_seconds=seconds
 t=time.time();status=s.Solve(m)
 record=dict(pair_type=name,forced_support_pair=[0,j],
             status=s.StatusName(status),duration_sec=round(time.time()-t,2),
             branches=s.NumBranches(),conflicts=s.NumConflicts())
 if status in (cp_model.FEASIBLE,cp_model.OPTIMAL):
  support=[i for i in range(400) if s.Value(x[i])]
  word=sum(1<<i for i in support)
  assert all((mask&word).bit_count()%2==0 for mask in A)
  record['support']=support;record['weight']=len(support)
 return record

def verify(seconds=50):
 A=geometry();R=independent_rows(A)
 assert len(R)==176
 near=next(i for i in range(1,400) if A[0]>>i&1)
 far=next(i for i in range(1,400) if not A[0]>>i&1)
 rows=[try_pair(A,R,'adjacent',near,seconds),
       try_pair(A,R,'nonadjacent',far,seconds)]
 return dict(status='INFEASIBLE_BOTH_d14_PROVED' if all(x['status']=='INFEASIBLE' for x in rows) else 'OPEN_UNLESS_WITNESS',
             n=400,adjacency_rank=176,logical_qubits=48,
             row_constraint_reduction_from=400,row_constraint_reduction_to=176,
             previously_certified_distance_range=[10,14],
             search_weight_range=[10,12],results=rows,
             boundary='UNKNOWN means undecided, not no such words.')
if __name__=='__main__':print(json.dumps(verify(),indent=2))
