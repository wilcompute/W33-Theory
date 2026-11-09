#!/usr/bin/env python3
"""Externally extended 1D chiral W33 spectral-flow falsifier.

For W33 40x40 point-line incidence B, the W33-equivariant *point*
operator C=B B^T/16 has spectrum {0^15,(3/8)^24,1^1}. Introduce
extra periodic 1D Bloch coordinate (NOT native spacetime) and the
AIII off-diagonal block Q(k)=m I+lambda C+t exp(ik) I.
Its winding is # of eigenvalues of mI+lambda C inside |z|<t,
giving selectable indices 0,15,24,39,40 depending on externally
chosen m,t,lambda. Robust under gap-preserving perturbations and
local U1 point rephasings, but not dynamically selected by W33.
"""
import json,math,sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from w33_20261109_five_fronts import geometry

def geometry_matrix():
    _,lines,inc=geometry()
    B=np.zeros((40,40),dtype=int)
    for i,row in enumerate(inc):
        for j in row:B[i,j]=1
    assert int(B.sum())==160
    C=B@B.T
    e=np.linalg.eigvalsh(C)
    expected={0:15,6:24,16:1}
    for val,mul in expected.items():
        assert int(sum(abs(e-val)<1e-9))==mul
    assert np.linalg.matrix_rank(C,tol=1e-9)==25
    return C

def winding(m,t,lam=1):
    # Exact rational parameters and the 40 eigenvalues of W33 C/16.
    M,T,L=F(str(m)),F(str(t)),F(str(lam))
    eigs=[(F(0),15),(F(3,8),24),(F(1),1)]
    roots=[{"center":str(M+L*x),
             "multiplicity":n,
             "inside":bool(abs(M+L*x)<T)} for x,n in eigs]
    assert all(abs(M+L*x)!=T for x,n in eigs)
    Wind=sum(n for x,n in eigs if abs(M+L*x)<T)
    gap=min(abs(abs(M+L*x)-T) for x,n in eigs)
    # Verify winding with 8192 numerical k-steps, independent of root counting.
    ks=np.linspace(0,2*math.pi,8193)
    z=np.exp(1j*ks)
    f=np.zeros(len(ks))
    for e,n in eigs:
        f+=n*np.unwrap(np.angle(float(M+L*e)+float(T)*z))
    numerical=int(round((f[-1]-f[0])/(2*math.pi)))
    assert numerical==Wind,(numerical,Wind)
    return {"m":str(M),"t":str(T),"lambda":str(L),
            "rational_band_centers":roots,
            "spectral_gap_lower_bound":str(gap),
            "AIII_chiral_winding_index_exact":Wind,
            "discretized_independent_winding":numerical,
            "Hermitian_chiral_Bloch_H":"H(k)=[[0,Q(k)],[Q(k)^dag,0]], Gamma=diag(I40,-I40)",
            "local_1D_hopping":"The exp(ik) factor is one externally introduced nearest-neighbor oriented 1D hopping term."}

def main(path=None):
    C=geometry_matrix()
    cases=[(1.5,.4,1),(.3,.4,1),(-.4,.2,1),(.05,.5,1),(0,1.4,1)]
    results=[winding(*p) for p in cases]
    assert [x["AIII_chiral_winding_index_exact"] for x in results]==[0,15,24,39,40]
    rng=np.random.default_rng(20261109617)
    phi=rng.uniform(0,2*math.pi,40)
    g=np.exp(1j*phi)
    pert=(g[:,None]*(C/16))*g.conj()[None,:]
    gauge_error=float(max(abs(np.sort(np.linalg.eigvalsh(pert))-np.sort(np.linalg.eigvalsh(C/16)))))
    assert gauge_error<1e-12
    # Conservative operator-norm perturbations less than the gap cannot close it
    # by Weyl's smallest-singular-value perturbation bound.
    stability=[{"winding":x["AIII_chiral_winding_index_exact"],
                "allowed_generic_uniform_Q_perturbation_op_norm_strictly_below":str(F(x["spectral_gap_lower_bound"])),
                "certified_stability_reason":"sigma_min(Q(k)+Delta)>=sigma_min(Q(k))-||Delta||_op >0 for all k; winding is homotopy invariant"}
               for x in results]
    out={"status":"PASS_W33_EQUIVARIANT_EXTERNAL_1D_CHIRAL_WINDING_NOT_PREDICTED",
         "W33_point_operator":"C=B B^T/16, spectrum 0(15),3/8(24),1(1)",
         "native_W33_Dirac_index":0,
         "models":results,
         "distinct_indices":[0,15,24,39,40],
         "pure_point_gauge_phase_spectrum_error":gauge_error,
         "gap_protection":stability,
         "critical_scope":"A 1D AIII winding is robust but is supplied by an EXTRA circle/momentum plus tunable m,t,lambda. The closed native W33 graph does not choose any of the distinct indices. The protected boundary modes are not 3+1D Weyl particles, nor does this give SM hypercharges, anomaly cancellation or cosmology.",
         "positive_contribution":"Provides explicit symmetry-covariant, W33-spectral, gap-protected topological benchmark with a built-in falsifier: identical finite input geometry admits distinct indices by varying external couplings."}
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("PASS external topological AIII W33",json.dumps({"windings":out["distinct_indices"],
             "gauge_err":gauge_error,
             "gaps":[x["spectral_gap_lower_bound"] for x in results]}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
