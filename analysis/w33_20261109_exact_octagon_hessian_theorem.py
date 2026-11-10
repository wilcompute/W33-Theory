#!/usr/bin/env python3
"""EXACT finite W33 octagon Hessian identity, via six rational evaluations.

Girth8 + W33 association-scheme spectrum permits exact identity
Hess_phi log det(I+t B(phi)B(phi)†)|phi=0
 = 2t^4/[(1+16t)(1+6t)^2] * C8.T C8,
where C8 is the 1620x160 oriented octagon-edge incidence matrix.
Proof: derive rational Hessian by Jacobi's determinant formula, clear
denominators, and check polynomial identity at SIX integer t values,
all using exact signed int64 and proven degree<=5. This is not just
a numerical test at a finite set of temperatures.
"""
import json,sys
from pathlib import Path
import numpy as np
from w33_20261109_flux_dark_mode_fragility import build
from w33_20261109_octagon_gauge_matter_tradeoff import loops_length8

def setup():
    B0,edges,G=build()
    B=B0.astype(np.int64)
    rings=loops_length8(G)
    assert len(rings)==1620
    ei={frozenset((p,40+l)):i for i,(p,l) in enumerate(edges)}
    C=np.zeros((1620,160),dtype=np.int64)
    for i,ring in enumerate(rings):
        for a,b in zip(ring,ring[1:]+ring[:1]):
            j=ei[frozenset((a,b))]
            C[i,j]+=1 if a<40 else -1
    Gram=C.T@C
    assert np.array_equal(np.diag(Gram),81*np.ones(160,dtype=np.int64))
    assert int(np.linalg.matrix_rank(C))==81
    return B,np.array(edges,dtype=np.int64),C,Gram

def integer_certificate(t,B,edges,Gram):
    # B B.T has eigenvalues 16(1), 6(24), 0(15).
    # At t, Q=(I+t B B.T)^-1 = N/(120 D).
    I=np.eye(40,dtype=np.int64)
    J=np.ones((40,40),dtype=np.int64)
    A=B@B.T-4*I
    P0=40*I-20*A+5*J # 120 * projector_0
    P16=3*J             # 120 * projector_16
    P6=120*I-P0-P16   # 120 * projector_6
    assert np.array_equal(P0@P0,120*P0)
    assert np.array_equal(P6@P6,120*P6)
    assert np.array_equal(P16@P16,120*P16)
    D=(1+16*t)*(1+6*t)
    N=D*P0+(1+16*t)*P6+(1+6*t)*P16
    NB=N@B
    BNB=B.T@NB
    # Prove signed-int64 intermediates cannot overflow before multiplying.
    lim=2**61
    maxN=int(max(abs(N.ravel())))
    maxNB=int(max(abs(NB.ravel())))
    maxBNB=int(max(abs(BNB.ravel())))
    maxGram=int(max(abs(Gram.ravel())))
    assert 120*D*(maxNB+maxN)<lim
    assert t*(maxNB**2+maxN*maxBNB)<lim
    assert 120**2*t**3*(1+16*t)*maxGram<lim
    p=edges[:,0];l=edges[:,1]
    e=np.arange(160)
    # For e=(p,l), f=(r,m), define D'=partial D/partial phi.
    # Tr(Q D''_ef) =
    #   -2t delta_ef (QB)_pl + 2t delta_{l,m} Q_{p,r}
    # Tr(Q D'_e Q D'_f) =
    #   -2t² [(QB)_{r,l}(QB)_{p,m} - Q_{p,r}(BᵀQB)_{l,m}].
    # Multiply full Hessian by (120²D²)/(2t).
    sameedge=(e[:,None]==e[None,:]).astype(np.int64)
    sameline=(l[:,None]==l[None,:]).astype(np.int64)
    term1=120*D*(-sameedge*NB[p,l][:,None] + sameline*N[p[:,None],p[None,:]])
    term2=t*(NB[p[None,:],l[:,None]]*NB[p[:,None],l[None,:]]-
             N[p[:,None],p[None,:]]*BNB[l[:,None],l[None,:]])
    lhs=term1+term2
    # Exact expected Hessian of logP:
    # a(t) Gram where a(t)=2t^4 /((1+16t)(1+6t)^2).
    # Multiplication by 120²D²/(2t) gives
    # 120² t³ (1+16t) Gram.
    rhs=120*120*t**3*(1+16*t)*Gram
    diff=lhs-rhs
    m=int(max(abs(diff.ravel())))
    return m,{"t":t,"max_absolute_integer_residual":m,
       "tested_off_diagonal_entries":int(len(diff.ravel())-160),
       "integer_values_within_safe_range":bool(max(abs(lhs.ravel()))<2**62)}

def main(path=None):
    B,edges,C,Gram=setup()
    controls=[]
    for t in (1,2,3,4,5,6):
        m,c=integer_certificate(t,B,edges,Gram)
        controls.append(c)
        assert m==0,(t,m)
    # Each matrix component of the cleared denominator is polynomial
    # degree<=5 (N degree<=2; D degree2). Six distinct integer roots
    # imply identity for all complex t, including positive real t.
    # Full single-edge finite-flux determinant crosscheck prior exact:
    prior=json.loads((Path(__file__).resolve().parents[1]/"data/w33_20261109_one_edge_flux_poly_curvature.json").read_text())
    assert prior["P_one_pi_minus_flat_exact_factored"]=="324*t**4*(6*t + 1)**22"
    # For any β, the full Hessian free energy is -κcrit(β) Gram,
    # κcrit=(4/β) Σ_n t_n^4/((1+16t_n)(1+6t_n)^2).
    out={"status":"PASS_EXACT_ALL_T_W33_OCTAGON_GAUGE_FERMION_HESSIAN_IDENTITY",
      "graph":{"vertices":80,"edges":160,"length8_octagons":1620,
               "cycle_rank":81},
      "exact_matrix_identity":"Hess_phi log det(I+t B(phi)B(phi)^dagger)|phi=0 = [2 t^4 / ((1+16t)(1+6t)^2)] C8.T C8 for ALL t >=0; C8 is 1620x160 oriented octagon-edge incidence",
      "all_six_integer_point_full_160x160_certificates":controls,
      "proof_by_polynomial_identity":"For D(t)=(1+16t)(1+6t), the inverse Q=(I+t BB^T)^-1=N/(120D), with N(t)=D(120P0)+(1+16t)(120P6)+(1+6t)(120P16), where 120P0=40I-20A+5J; 120P16=3J; 120P6=120I-P0num-P16num. Jacobi's formula expresses Hess logP via Q, QB, B^TQB and edge deltas. Multiply both sides by 120^2 D^2/(2t): each resulting entry is an integer polynomial in t of degree<=5. All 25600 matrix entries agree at the six distinct integers t=1..6 by exact int64 arithmetic. Polynomial identity theorem proves equality for all t, including t=0 by continuity.",
      "consequence_all_beta":"For half-filled spinless W33 fermions Fbeta=-2/beta sum_s log(2cosh(beta singular(B)/2)), the exact quadratic form about flat connection is Hess_phi Fbeta|flat = -kappa_critical(beta) C8.T C8 with kappa_critical(beta) = (4/beta) SUM_{n>=0} [t_n^4/((1+16t_n)(1+6t_n)^2)], t_n=beta²/[pi²(2n+1)²]. Under all-octagon Wilson action with coefficient kappa, Hess total=(kappa-kappa_critical) C8.T C8, with the 79 pure gauge null directions on full 160-edge coordinates and 81 physical directions.",
      "local_stability_beta1_approx":prior["beta_curvature_controls"][2]["kappa_local_single_link_Matsubara"],
      "zero_eigenvalue_count_Gauge":79,
      "positive_eigenvalue_count_Physical":81,
      "scope":"This EXACT identity and local flat-vacuum stability threshold apply to a finite W33 tight-binding free-fermion and all-1620-octagon compact U1 gauge model; do not infer global ground-state selection, continuum phase transition, gravity, or physical coupling values. No proof that all1620 octagons are local plaquettes in a 3D manifold."
    }
    if path:Path(path).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print("EXACT_FULL_HESSIAN",json.dumps({"all_residuals":[x["max_absolute_integer_residual"] for x in controls],
       "kappa_beta1":out["local_stability_beta1_approx"]}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
