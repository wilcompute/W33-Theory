#!/usr/bin/env python3
"""Minimum phase-flip support that completely lifts native W33 30 zero modes.

Any k edge changes B->B+sum_{j<=k} delta_j e_point e_line^T raises
rank by <=k. Native rank=25, so k>=15 necessary to reach full rank.
Search 15 incident edges whose projected endpoint columns separately
span both 15D dark kernels (intersection of two linear matroids).
Check an actual phase-only pi flip at those edges gives full rank 40,
and certify exact integer determinant/rank using SymPy.
"""
import json,math,sys
from pathlib import Path
import numpy as np
from sympy import Matrix
from w33_20261109_flux_dark_mode_fragility import build

def independent(v,Q,tol=1e-8):
    r=v-Q@(Q.T@v) if Q.size else v
    norm=np.linalg.norm(r)
    return (norm>tol,r/norm if norm>tol else r)

def find_support(B,edges,seed=202611092026,tries=300):
    A=B@B.T-4*np.eye(40)
    C=B.T@B-4*np.eye(40)
    P=(8*np.eye(40)-4*A+np.ones((40,40)))/24
    R=(8*np.eye(40)-4*C+np.ones((40,40)))/24
    assert abs(np.trace(P)-15)<1e-12
    rng=np.random.default_rng(seed)
    records=[]
    for trial in range(tries):
        Qp=np.zeros((40,0));Ql=np.zeros((40,0))
        selected=[]
        candidate=np.arange(160);rng.shuffle(candidate)
        for ix in candidate:
            p,l=edges[ix]
            okp,u=independent(P[:,p],Qp)
            okl,v=independent(R[:,l],Ql)
            if okp and okl:
                Qp=np.column_stack([Qp,u]);Ql=np.column_stack([Ql,v])
                selected.append((p,l))
            if len(selected)==15:
                return selected,trial+1,P,R
        records.append(len(selected))
    raise RuntimeError("No common independent base found; best "+str(max(records)))

def main(path=None):
    B,edges,G=build()
    selected,attempts,P,R=find_support(B,edges)
    assert len(selected)==15 and len(set(selected))==15
    SS=sorted(set(p for p,l in selected))
    TT=sorted(set(l for p,l in selected))
    assert len(SS)==len(TT)==15
    eigp=np.linalg.eigvalsh(P[np.ix_(SS,SS)])
    eigl=np.linalg.eigvalsh(R[np.ix_(TT,TT)])
    assert eigp[0]>1e-10 and eigl[0]>1e-10
    # Exactly 15 phase-only flips, no amplitude changes:
    Z=B.astype(np.int64)
    for p,l in selected:
        assert Z[p,l]==1
        Z[p,l]=-1
    rank=int(np.linalg.matrix_rank(Z))
    assert rank==40,rank
    det=Matrix(Z.tolist()).det(method="domain-ge")
    assert det==65536,det
    # The determinant is a degree <=15 polynomial in a common change
    # delta=z-1. Since rank(B)=25, no power delta^k with k<15
    # can occur; 15 is the maximum power, hence exactly c*delta^15.
    # Exact integer checks at z in {0,-1,2} certify c=-2.
    zeros=B.astype(np.int64)
    plus=B.astype(np.int64)
    for p,l in selected:
        zeros[p,l]=0  # z=0, delta=-1
        plus[p,l]=2   # z=2, delta=+1 (not phase-only test)
    det0=Matrix(zeros.tolist()).det(method="domain-ge")
    det2=Matrix(plus.tolist()).det(method="domain-ge")
    assert det0==2 and det2==-2,(det0,det2)
    # Consequently det(B(theta))=-2*(exp(i theta)-1)^15
    # for ALL theta: every nontrivial common phase lifts every mode.
    # Tests theta is common across 15 edges and physical constant modulus.
    sv=np.linalg.svd(Z,compute_uv=False)
    one_before=np.linalg.svd(B,compute_uv=False)
    assert min(abs(Z[B==1].ravel()))==1
    exact_rank_staircase=[]
    for k in range(0,16):
        ZZ=B.copy().astype(int)
        for p,l in selected[:k]:ZZ[p,l]=-1
        rk=int(np.linalg.matrix_rank(ZZ))
        assert rk==25+k,(k,rk)
        exact_rank_staircase.append(rk)
    phase_controls=[]
    for theta in (math.pi/6,math.pi/3,math.pi/2,math.pi):
        Q=B.astype(complex)
        for a,b in selected:Q[a,b]=np.exp(1j*theta)
        exact=-2*(np.exp(1j*theta)-1)**15
        computed=np.linalg.slogdet(Q)
        rel=abs(computed[0]*np.exp(computed[1]-np.log(abs(exact)))-exact/abs(exact))
        assert rel<1e-6,(theta,rel)
        phase_controls.append({"theta":theta,"smallest_singular_value":float(np.linalg.svd(Q,compute_uv=False)[-1]),"relative_phase_determinant_error":float(rel)})
    # Gauge-invariant loop flux: phase pi for 15 edges, at least one cycle
    # must carry nonzero phase. The graph is bridgeless (girth8) so
    # a single edge flip cannot be pure gauge.
    out={"status":"PASS_MINIMUM_15_INCIDENCE_PI_FLIPS_LIFT_30_FLAT_ZERO_MODES",
         "original_40x40_incidence_rank":25,
         "required_number_of_link_changes_lower_bound":15,
         "constructed_phase_only_pi_flip_links":[{"point":p,"line":l} for p,l in selected],
         "independent_pair_matroid_search_trials":attempts,
         "selected_point_dark_projector_smallest_Gram_eigenvalue":float(eigp[0]),
         "selected_line_dark_projector_smallest_Gram_eigenvalue":float(eigl[0]),
         "perturbed_incidence_matrix_rank":rank,
         "perturbed_integer_matrix_determinant":str(det),
         "exact_determinant_polynomial":"det(B+(z-1) E_selected)=-2*(z-1)^15; phase-only z=e^(i theta)",
         "exact_three_integer_controls":{"z_minus1":str(det),"z_zero":str(det0),"z_two":str(det2)},
         "continuous_phase_numerical_controls":phase_controls,
         "perturbed_smallest_singular_value":float(sv[-1]),
         "remaining_exact_chiral_zero_modes":0,
         "ordered_edge_flip_incidence_rank_staircase":exact_rank_staircase,
         "ordered_edge_flip_chiral_zero_mode_staircase":[80-2*x for x in exact_rank_staircase],
         "necessary_and_sufficient_within_link_support_model":"At least 15 link entry changes are required to lift 15+15 W33 chiral flat modes, and this explicit 15-link phase-flip assignment suffices. Thus minimum support is exactly 15. This is a finite integer matrix theorem, not a mechanism selecting physical gauge fluxes.",
         "proof":"Rank(B+Delta) <=25+rank(Delta)<=25+k. Selected distinct incident edges have 15 independently projected endpoint columns in each 15D null space. Actual phase-only pi flips B_ij->-B_ij on these edges yield a 40x40 integer matrix whose nonzero exact determinant verifies rank40. In particular all zero modes are gone. No hopping magnitudes changed.",
         "scope":"A free choice of fifteen U1 Wilson phases is not derived from dynamics; it is an adversarial link assignment. Preserving only bipartite chirality does not guarantee zero eigenvalues on equal-size sublattices. No continuum Weyl index or SM particle spectrum is established.",
         "prior_art":"Rank perturbation bounds, matroid common bases, bipartite tight binding and Wilson phases are standard mathematical tools; native W33 setting and exact certificate are the project-specific advance."}
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("MINIMAL_W33_FLUX",json.dumps({"rank":rank,"flips":len(selected),
       "exact_determinant":str(det)[:80],"singular_gap":float(sv[-1]),"trials":attempts}))
    return out
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
