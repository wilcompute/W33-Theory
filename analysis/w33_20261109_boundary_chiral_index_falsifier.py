#!/usr/bin/env python3
"""Boundary index experiment: W33 40x40 chirality remains paired, 41x40 index1.

Construct a one-point boundary defect on the fully gapped 15-link π
matrix. Index is rank-nullity, not a 3+1D Weyl fermion or proof of
anomaly cancellation. Explicit analytic protected zero vector.
"""
import json,sys,math
from pathlib import Path
import numpy as np
from w33_20261109_flux_dark_mode_fragility import build
def index_stats(T):
    nr,nc=T.shape
    rank=np.linalg.matrix_rank(T,tol=1e-10)
    return {"rows":nr,"columns":nc,"rank":int(rank),
            "left_chiral_zero_count":int(nr-rank),
            "right_chiral_zero_count":int(nc-rank),
            "net_left_minus_right":int(nr-nc),
            "total_chiral_zero_modes":int(nr+nc-2*rank)}
def main(path=None):
    root=Path(__file__).resolve().parents[1]
    B,edges,G=build()
    data=json.loads((root/"data/w33_20261109_flux_mass_gap_design.json").read_text())
    T=B.astype(complex)
    for x in data["best_15_edges"]:T[x["point"],x["line"]]=-1
    assert np.linalg.matrix_rank(T)==40
    rng=np.random.default_rng(20261109555)
    defect=np.zeros(40,dtype=complex)
    inds=np.array(sorted(set(int(i) for i in rng.choice(40,4,replace=False))))
    defect[inds]=np.exp(1j*rng.uniform(-2,2,4))
    A=np.vstack([T,defect])
    s=index_stats(A)
    assert s["net_left_minus_right"]==1 and s["total_chiral_zero_modes"]==1
    # Solve T† x_first40 + defect† x_extra=0 for x_extra=1
    x=-np.linalg.solve(T.conj().T,defect.conj())
    state=np.r_[x,1.+0j]
    state/=np.linalg.norm(state)
    assert np.linalg.norm(A.conj().T@state)<1e-12
    ipr=float(sum(abs(state)**4))
    root_occupancy=float(abs(state[-1])**2)
    # Chirality + pure-gauge invariance, then adversarial local
    # phase disorder in original incidence entries.
    controls=[]
    for scale in (0.0,.01,.1,1.):
        Q=A.copy()
        phases=rng.uniform(-scale,scale,Q.shape)
        Q[np.nonzero(Q)]*=np.exp(1j*phases[np.nonzero(Q)])
        q=index_stats(Q)
        assert q["net_left_minus_right"]==1
        assert q["total_chiral_zero_modes"]>=1
        v=np.linalg.svd(Q.conj().T)[2].conj().T[:,-1]
        assert np.linalg.norm(Q.conj().T@v)<1e-12
        controls.append({"random_link_phase_scale":scale,
             "zero_mode_count":q["total_chiral_zero_modes"],
             "residual":float(np.linalg.norm(Q.conj().T@v)),
             "defect_amplitude_probability":float(abs(v[-1])**2),
             "inverse_participation":float(np.sum(abs(v)**4))})
    # Balanced B: no robust index under flux. Add one point row:
    # net index1 is robust no matter which phases on nonzero links.
    output={"status":"PASS_FINITE_W33_SQUARE_CHIRAL_NO_INDEX_VS_BOUNDARY_DEFECT_INDEX1",
        "original_balanced_gapped_40x40":index_stats(T),
        "boundary_defect_extra_point_four_link_lines":[int(v) for v in inds],
        "rectangular_41x40_index":s,
        "boundary_zero_exact_vector_residual":float(np.linalg.norm(A.conj().T@state)),
        "boundary_zero_probability_at_defect_site":root_occupancy,
        "boundary_zero_inverse_participation":ipr,
        "phase_disorder_controls":controls,
        "proof":"For any complex matrix T with n_p point and n_l line modes, H(T)=[0,T;T†,0] anticommutes with Γ=diag(+I_np,-I_nl). Index dim ker T†−dim ker T=np−nl, independent of flux and rank. A square 40x40 matrix necessarily has index zero; adding one boundary point produces index +1 and one exact protected zero whenever its 41x40 coupling has full column rank.",
        "scope":"This is a finite chiral-sublattice imbalance zero mode at an explicitly added boundary defect, NOT an unpaired 3+1D Weyl fermion, protected bulk band, anomaly-free standard model, or physical chirality selection. The induced zero amplitude spreads over the original gapped graph through T^{-†}. The extra point is an additional primitive, not derived from W33 symmetry.",
        "prior_art":"Lieb sublattice imbalance and the chiral matrix index theorem are standard. The user project already has separate lattice chirality no-go work; this numerical W33 boundary construction is an explicit falsifiable alternative, not a novel general theorem."}
    if path:Path(path).write_text(json.dumps(output,indent=2,sort_keys=True)+"\n")
    print("BOUNDARY_INDEX",json.dumps({"square":output["original_balanced_gapped_40x40"],
          "rectangular":s,"defect_probability":root_occupancy,"ipr":ipr}))
    return output
if __name__=="__main__":main(sys.argv[1] if len(sys.argv)>1 else None)
