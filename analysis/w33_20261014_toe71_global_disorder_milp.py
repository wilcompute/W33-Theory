"""TOE71 numerical global mixed-integer W33 hopping-disorder optimization.

At fixed q=(0,-1,1), the 238 native winding octagons (159 active)
are multiaffine functions of 160 hopping amplitudes. A multiaffine
function attains its global box minimum at some corner. This code gives
an EXACT 0-1 formulation of those corners and solves using floating
HiGHS MILP. Solver optimality is NUMERICAL, NOT a formal exact dual proof.
All returned winning witnesses are cross-checked by Python big integers.
"""
from __future__ import annotations
from pathlib import Path
import json,sys,math
import numpy as np
from scipy.sparse import lil_matrix
from scipy.optimize import milp,Bounds,LinearConstraint,brentq
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,windings,HIGH

def native_active_cycles():
    ed,adj,cycles=octagons()
    out=[]
    for ci,w in windings(cycles,ed):
        c=(1 if sum(w)%2 else -1)*(w[2]-w[1])**2
        if c:out.append((int(c),tuple(cycles[ci])))
    assert len(out)==159
    return out

def exact_rayleigh(active,high,n,d):
    H=set(high);u=d+n;v=d-n
    return sum(c*u**len(H.intersection(cy))*v**(8-len(H.intersection(cy)))
               for c,cy in active)

def exact_milp_model(active):
    # x[e] binary; z[i,k] binary indicating exactly k high links on cycle i.
    # sum_k z[i,k]=1; sum_k k*z[i,k]=sum_{e in cycle}x[e].
    # At integral x,z these constraints give the original EXACT corner
    # polynomial without any approximated nonlinear product.
    ncy=len(active);sz=160+9*ncy;A=lil_matrix((2*ncy,sz),dtype=float)
    for i,(coef,cy) in enumerate(active):
        for k in range(9):
            A[2*i,160+9*i+k]=1
            A[2*i+1,160+9*i+k]=k
        for e in cy:A[2*i+1,e]=-1
    rhs=np.tile([1,0],ncy).astype(float)
    return A.tocsc(),rhs

def optimize(eps,active,A,rhs):
    sz=A.shape[1];c=np.zeros(sz)
    for i,(coef,cy) in enumerate(active):
        for k in range(9):
            c[160+9*i+k]=coef*(1+eps)**k*(1-eps)**(8-k)
    result=milp(c,integrality=np.ones(sz,dtype=int),
                bounds=Bounds(np.zeros(sz),np.ones(sz)),
                constraints=LinearConstraint(A,rhs,rhs),
                options={"time_limit":30,"mip_rel_gap":0.0})
    assert result.status==0 and result.x is not None, result.message
    high=tuple(np.flatnonzero(result.x[:160]>.5).tolist())
    assert abs(float(np.dot(c,result.x))-result.fun)<1e-7
    assert abs(result.fun-result.mip_dual_bound)<1e-7
    # Ratios are exactly rational at the tested eps values.
    n=int(round(eps*10000000));d=10000000
    exact=exact_rayleigh(active,high,n,d)
    assert abs(exact/d**8-result.fun)<3e-8
    return {
        "epsilon_str":f"{n}/{d}","solver_status":"optimal",
        "integer_variables":sz,"cycles":len(active),
        "floating_objective":float(result.fun),
        "floating_solver_dual_bound":float(result.mip_dual_bound),
        "branch_and_bound_nodes":int(result.mip_node_count),
        "optimal_high_native_edges":list(high),
        "exact_winner_numerator":str(exact),
        "exact_winner_denominator":f"{d}^8",
        "qualification":"HiGHS uses finite-precision floating MILP bounds; 'optimal' is its numerical declaration, NOT a formal exact rational proof of all-corner optimality."
    }

def certificate():
    active=native_active_cycles()
    A,rhs=exact_milp_model(active)
    results=[optimize(eps,active,A,rhs)
             for eps in (.245,.244616,.2446151,.244615,.244)]
    for r in results:
        assert r["optimal_high_native_edges"]==list(HIGH)
    assert int(results[0]["exact_winner_numerator"])<0
    assert int(results[2]["exact_winner_numerator"])>0
    assert int(results[1]["exact_winner_numerator"])<0
    # Root of known integer polynomial along the explicitly constructed mask.
    def polynomial(e):
        u=1+e;v=1-e
        return 72*u**2*v**6+46*u**3*v**5+34*u**4*v**4-12*u**8
    threshold=brentq(polynomial,.2446,.2447,xtol=5e-16)
    assert .2446151<threshold<.244616
    return {
      "status":"PASS_TOE71_GLOBAL_INTEGER_PROGRAM_SOLVER",
      "fixed_phase_Rayleigh_direction":[0,-1,1],
      "native_edge_count":160,"active_winding_octagons":159,
      "integer_program_equivalence":"Exact logical equivalence at integral x,z; solver numerical tolerances remain",
      "tested_global_corner_optima":results,
      "explicit_17_edge_root":threshold,
      "qualification":"Global optimality over all 2^160 corners is REPORTED BY NUMERICAL MILP, not formal exact proof. The special direction does not determine the full Hessian minimum eigenvalue.",
      "next_proof":"Export rational branch-and-bound/cutting-plane certificates and verify with an independent integer proof checker."
    }

if __name__=="__main__":
    out=certificate()
    (ROOT/"data/w33_20261014_toe71_global_disorder_milp.json").write_text(
      json.dumps(out,indent=2)+"\n",encoding="utf-8")
    print(out["status"],out["explicit_17_edge_root"])
