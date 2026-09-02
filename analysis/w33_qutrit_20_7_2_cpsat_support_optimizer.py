#!/usr/bin/env python3
"""Exact CP-SAT support optimization for the W33 [[20,7,2]]_3 symplectic map.

We optimize the explicit nonlocal embedding in two exact stages over GF(3).

A-stage.  The constraints H A = T separate by physical column.  We freeze one
verified invertible 20-column minor of the original A; this guarantees rank(A)=20.
For each of the other 220 columns, CP-SAT minimizes Hamming weight exactly under
H a_j = t_j (mod 3).  Since the columns are independent once the minor is fixed,
the sum is a global optimum in that fixed-minor affine class.

B-stage.  For the optimized A, each row b_i of B independently solves
A b_i^T = e_i.  CP-SAT minimizes each row's Hamming support exactly.  Therefore
total support(B) is globally minimal for that fixed optimized A.

This is an exact algebraic support certificate.  Fixed-minor optimality is not a
claim of globally minimum A support over every possible rank-20 minor, and low
Hamming support is not by itself a physical locality/threshold theorem.
"""
from __future__ import annotations
import hashlib, json
import numpy as np
from ortools.sat.python import cp_model

import w33_qutrit_20_7_2_symplectic_embedding as base
import w33_qutrit_20_7_2_sparse_symplectic as sparse


def solve_min_weight_mod3(M, target, *, tag):
    M=np.array(M,dtype=np.int64)%3; target=np.array(target,dtype=np.int64)%3
    rows,cols=M.shape
    model=cp_model.CpModel()
    x=[model.NewIntVar(0,2,f'{tag}_x_{i}') for i in range(cols)]
    nz=[model.NewBoolVar(f'{tag}_nz_{i}') for i in range(cols)]
    for i in range(cols):
        model.Add(x[i]==0).OnlyEnforceIf(nz[i].Not())
        model.Add(x[i]>=1).OnlyEnforceIf(nz[i])
    for r in range(rows):
        max_sum=int(sum(int(M[r,i])*2 for i in range(cols)))
        k=model.NewIntVar(-1,max_sum//3+1,f'{tag}_k_{r}')
        model.Add(sum(int(M[r,i])*x[i] for i in range(cols))-3*k==int(target[r]))
    model.Minimize(sum(nz))
    solver=cp_model.CpSolver()
    solver.parameters.num_search_workers=1
    solver.parameters.random_seed=0
    solver.parameters.cp_model_presolve=True
    status=solver.Solve(model)
    if status!=cp_model.OPTIMAL:
        raise RuntimeError(f'{tag}: exact optimum not certified, status={solver.StatusName(status)}')
    v=np.array([solver.Value(q) for q in x],dtype=np.int64)%3
    if not np.array_equal((M@v)%3,target): raise RuntimeError(f'{tag}: solver witness violates GF(3) constraints')
    return v,int(sum(1 for q in v if q%3)),float(solver.ObjectiveValue()),int(solver.NumBranches())


def base_problem():
    hx,hz,h,targets,A0=sparse.build_base()
    _,piv=base.rref(A0)
    fixed=[int(x) for x in piv[:20]]
    if len(fixed)!=20 or base.rank(A0[:,fixed])!=20: raise RuntimeError('base A has no verified 20-column minor')
    return hx,hz,h,targets,A0,fixed


def optimize_A():
    hx,hz,h,targets,A0,fixed=base_problem()
    T=targets
    A=A0.copy()%3
    fixed_set=set(fixed); records=[]
    for j in range(240):
        if j in fixed_set:
            records.append({'column':j,'fixed_minor':True,'weight':int(np.count_nonzero(A[:,j])),'branches':0})
            continue
        col,w,obj,branches=solve_min_weight_mod3(h,T[:,j],tag=f'A{j}')
        A[:,j]=col
        records.append({'column':j,'fixed_minor':False,'weight':w,'branches':branches})
    if base.rank(A)!=20: raise RuntimeError('fixed minor failed to preserve rank 20')
    if not np.array_equal((h@A)%3,T): raise RuntimeError('optimized A violates H A = T')
    return hx,hz,h,T,A0,A,fixed,records


def optimize_B(A):
    rows=[]; records=[]
    eye=np.eye(20,dtype=np.int64)
    for i in range(20):
        v,w,obj,branches=solve_min_weight_mod3(A,eye[:,i],tag=f'B{i}')
        rows.append(v); records.append({'row':i,'weight':w,'branches':branches})
    B=np.array(rows,dtype=np.int64)%3
    if not np.array_equal((A@B.T)%3,eye): raise RuntimeError('optimized B is not a right symplectic dual')
    return B,records


def matrix_hash(a): return 'sha256:'+hashlib.sha256(bytes(int(x) for x in a.flatten())).hexdigest()
def weights(a): return [int(np.count_nonzero(x%3)) for x in a]


def optimized_witness():
    hx,hz,h,T,A0,A,fixed,arec=optimize_A()
    B,brec=optimize_B(A)
    return hx,hz,h,T,A0,A,B,fixed,arec,brec


def verify():
    hx,hz,h,T,A0,A,B,fixed,arec,brec=optimized_witness()
    oldB,_=sparse.right_inverse(A0)
    wa0=int(np.count_nonzero(A0)); wa=int(np.count_nonzero(A)); wb0=int(np.count_nonzero(oldB)); wb=int(np.count_nonzero(B))
    checks={
      'fixed_minor_rank_20':base.rank(A[:,fixed])==20,
      'A_rank_20':base.rank(A)==20,
      'HA_constraints_exact':np.array_equal((h@A)%3,T),
      'ABt_identity':np.array_equal((A@B.T)%3,np.eye(20,dtype=np.int64)),
      'A_support_not_worse_than_base':wa<=wa0,
      'B_support_exact_rows_nonzero':all(x['weight']>0 for x in brec),
      'all_220_free_A_columns_optimized':sum(not x['fixed_minor'] for x in arec)==220,
      'all_20_B_rows_optimized':len(brec)==20,
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      'schema':'w33.qutrit-20-7-2-cpsat-support-optimizer.v1','status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'fixed_minor_columns_0_indexed':fixed,
      'A':{'sha256':matrix_hash(A),'support':wa,'base_support':wa0,'support_delta':wa-wa0,'row_weights':weights(A),'free_column_optimum_weight_sum':sum(x['weight'] for x in arec if not x['fixed_minor'])},
      'B':{'sha256':matrix_hash(B),'support':wb,'baseline_right_inverse_support':wb0,'support_delta_vs_baseline':wb-wb0,'row_weights':weights(B),'exact_row_optimum_weight_sum':sum(x['weight'] for x in brec)},
      'solver':{'A_columns':arec,'B_rows':brec,'deterministic_workers':1},
      'theorem':'With the displayed 20-column minor frozen, A has globally minimum total Hamming support among all HA=T maps in that fixed-minor class; for this optimized A, B has globally minimum total support among all right duals AB^T=I20.',
      'boundary':'The A optimum is conditional on the fixed rank-preserving minor. Joint global A/B support over all possible minors is not claimed. Support optimality is algebraic, not a photonic locality or fault-tolerance threshold theorem.'
    }

if __name__=='__main__':
    out=verify(); print(json.dumps(out,indent=2)); raise SystemExit(0 if out['status']=='PASS' else 1)
