"""TOE72: exact 3x3 Hessian on 17-edge native adversary and six
independent fixed-direction full-160-link MILP probes.

Every MILP formulation is logically exact at 0/1 assignments but HiGHS
optimality is FLOATING-POINT; no formal global spectral threshold claimed.
"""
from __future__ import annotations
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
from w33_20261014_toe69_five_fronts import octagons,windings,HIGH

def certificate():
    ed,adj,cycles=octagons()
    winds=windings(cycles,ed)
    # H(e) = (1/d^8)sum_k C[k]*(d+n)^k*(d-n)^(8-k).
    C=np.zeros((9,3,3),dtype=np.int64)
    high=set(HIGH)
    for ci,w in winds:
        v=np.array(w,dtype=np.int64)
        coef=(1 if sum(w)%2 else -1)
        k=len(high.intersection(cycles[ci]))
        C[k]+=coef*np.outer(v,v)
    assert np.array_equal(C[:,1,1],C[:,2,2])
    assert np.array_equal(C[:,0,1],C[:,0,2])
    q=np.array((0,-1,1),dtype=np.int64)
    qcoeff=[int(q@C[k]@q) for k in range(9)]
    assert qcoeff==[0,0,72,46,34,0,0,0,-12]
    matrices=[]
    for n,d in ((6,25),(6115,25000),(49,200)):
        # object-int avoids overflowing fixed int64 for large denominator.
        big=np.zeros((3,3),dtype=object)
        for k in range(9):
            for a in range(3):
                for b in range(3):
                    big[a,b]+=int(C[k,a,b])*(d+n)**k*(d-n)**(8-k)
        assert big[1,1]==big[2,2] and big[0,1]==big[0,2]
        eig=np.linalg.eigvalsh(np.asarray(big,dtype=float)/d**8)
        ray=sum(qcoeff[k]*(d+n)**k*(d-n)**(8-k) for k in range(9))
        assert abs(eig[0]-ray/(2*d**8))<1e-8
        matrices.append({"epsilon":f"{n}/{d}",
                         "exact_Hessian_integer_numerator":[[str(x) for x in row] for row in big],
                         "integer_denominator":f"{d}^8",
                         "q_Rayleigh_numerator":str(ray),
                         "smallest_numeric_eigenvalue":float(eig[0])})
    # Full 160-corner numerical MILP probes at one near-boundary epsilon.
    direction_set=[(0,-1,1),(1,0,0),(1,-1,0),(1,1,1),(1,1,-1),(0,1,1)]
    n,d=1223,5000
    runs=[]
    for direction in direction_set:
        active=[]
        for ci,w in winds:
            v=sum(a*b for a,b in zip(direction,w))
            if v:
                active.append(((1 if sum(w)%2 else -1)*v*v,cycles[ci]))
        ncy=len(active);nvar=160+9*ncy
        A=lil_matrix((2*ncy,nvar),dtype=float)
        obj=np.zeros(nvar)
        for i,(coef,es) in enumerate(active):
            for k in range(9):
                A[2*i,160+9*i+k]=1
                A[2*i+1,160+9*i+k]=k
                obj[160+9*i+k]=coef*(1+n/d)**k*(1-n/d)**(8-k)
            for e in es:A[2*i+1,e]=-1
        rhs=np.tile((1.,0.),ncy)
        res=milp(obj,integrality=np.ones(nvar),
            bounds=Bounds(np.zeros(nvar),np.ones(nvar)),
            constraints=LinearConstraint(A.tocsc(),rhs,rhs),
            options={"time_limit":30,"mip_rel_gap":0.0})
        assert res.status==0 and res.x is not None,res.message
        assert abs(res.fun-res.mip_dual_bound)<1e-7
        selected=set(np.flatnonzero(res.x[:160]>.5).tolist())
        exact=sum(int(coef)*(d+n)**len(selected.intersection(es))*
                  (d-n)**(8-len(selected.intersection(es)))
                  for coef,es in active)
        assert abs(exact/d**8-res.fun)<5e-8
        assert exact>0
        runs.append({"direction":list(direction),
           "active_native_winding_octagons":ncy,
           "solver_status":"numerical_optimal",
           "floating_minimum":float(res.fun),
           "floating_dual_bound":float(res.mip_dual_bound),
           "winning_high_edges":sorted(selected),
           "winning_exact_integer_numerator":str(exact),
           "integer_denominator":f"{d}^8"})
    assert all(x["winning_exact_integer_numerator"]!="0" for x in runs)
    return {
      "status":"PASS_TOE72_FULL_HESSIAN_AND_MULTIRAY_MILP_PROBES",
      "native_octagons_with_nonzero_winding":len(winds),
      "exact_high_count_Hessian_coefficients":C.tolist(),
      "exact_antisymmetric_eigenvector":[0,-1,1],
      "exact_antisymmetric_rayleigh_coefficients":qcoeff,
      "fixed_adversary_rational_epsilon_matrices":matrices,
      "all_160_edge_corner_probes_epsilon":"1223/5000",
      "six_independent_full_160_edge_MILP_directions":runs,
      "scope":"Proves exact Hessian symmetry/eigendirection for fixed 17-high witness. Six full-160-edge MILPs use finite precision; only sampled q directions, NOT the entire real sphere or formal globally certified full-Hessian positive-disorder threshold."
    }

if __name__=="__main__":
    c=certificate()
    (ROOT/"data/w33_20261014_toe72_hessian_multiray.json").write_text(json.dumps(c,indent=2)+"\n")
    print(c["status"],[z["floating_minimum"] for z in c["six_independent_full_160_edge_MILP_directions"]])
