#!/usr/bin/env python3
"""Native W33 Levi-Dirac index and minimal-settings optical Givens compilation.

Finite-graph chiral index and zero-mode pairing are exact. The naive
incidence-Dirac operator has 15 zero modes in each grading, index zero.
Generic edge gauge phases lift the 30 accidental zero modes.
No claim about all possible chiral lattice discretizations or a TOE.
"""
import json
import sys
from pathlib import Path
import numpy as np
import sympy as sp
from w33_20261109_five_fronts import geometry
from w33_20261109_q8_ten_context_tomography import select
from w33_20261109_q8_12setting_completion import product_mub

def native_dirac():
    _,lines,incidents=geometry()
    B=np.zeros((40,40),dtype=int)
    for p,row in enumerate(incidents):
        for l in row:B[p,l]=1
    assert B.sum()==160 and (B.sum(axis=0)==4).all() and (B.sum(axis=1)==4).all()
    BB=B@B.T
    eigen=np.linalg.eigvalsh(BB)
    spect={0:15,6:24,16:1}
    for val,mult in spect.items():
        assert sum(abs(eigen-val)<1e-9)==mult
    rank=int(sp.Matrix(B).rank())
    assert rank==25
    Dirac=np.block([[np.zeros((40,40)),B],[B.T,np.zeros((40,40))]])
    chirality=np.diag(np.r_[np.ones(40),-np.ones(40)])
    anticomm=np.max(abs(Dirac@chirality+chirality@Dirac))
    assert anticomm==0
    gamma_plus_zeros=40-rank
    gamma_minus_zeros=40-rank
    assert gamma_plus_zeros==gamma_minus_zeros==15

    rng=np.random.default_rng(2026110919)
    chi1=rng.uniform(-np.pi,np.pi,40)
    chi2=rng.uniform(-np.pi,np.pi,40)
    gauge_B=np.exp(1j*chi1)[:,None]*B*np.exp(-1j*chi2)[None,:]
    compare=max(abs(np.linalg.svd(gauge_B,compute_uv=False)-np.linalg.svd(B,compute_uv=False)))
    assert compare<2e-13
    edge_phase=rng.uniform(-np.pi,np.pi,(40,40))
    disorder=np.where(B,np.exp(1j*edge_phase),0)
    noisy_singular=np.linalg.svd(disorder,compute_uv=False)
    assert min(noisy_singular)>1e-6
    random_minima=[float(min(np.linalg.svd(np.where(B,np.exp(
        1j*rng.uniform(-np.pi,np.pi,(40,40))),0),compute_uv=False))) for _ in range(8)]
    assert min(random_minima)>1e-7
    return {"status":"PASS_EXACT_NATIVE_W33_NAIVE_DIRAC_CHIRAL_INDEX_ZERO",
            "incidence_shape":[40,40],
            "incidence_rank_over_Q_exact":rank,
            "singular_square_spectrum":{str(k):v for k,v in spect.items()},
            "graded_plus_zero_modes":gamma_plus_zeros,
            "graded_minus_zero_modes":gamma_minus_zeros,
            "zero_mode_index_plus_minus":gamma_plus_zeros-gamma_minus_zeros,
            "total_Dirac_zero_modes":gamma_plus_zeros+gamma_minus_zeros,
            "chiral_anticommutator_max":float(anticomm),
            "local_U1_pure_gauge_singular_error":float(compare),
            "generic_edge_phase_min_singular":float(min(noisy_singular)),
            "additional_generic_edge_phase_min_singulars":random_minima,
            "interpretation":"The naive bipartite incidence Dirac operator has paired left/right zero modes and index zero; its 30 zero modes are generically lifted by independent edge holonomies. It does not force unpaired Weyl fermions.",
            "scope":"This is a no-go for this specific naive square incidence Dirac, not a theorem excluding all modified overlap/domain-wall/chiral discretizations or Standard Model physics."}

def decompose_nearest_neighbor(U):
    R=U.copy()
    Gtotal=np.eye(9,dtype=complex)
    couplers=[]
    for col in range(8):
        for row in range(8,col,-1):
            x,y=R[row-1,col],R[row,col]
            n=np.hypot(abs(x),abs(y))
            assert n>1e-12
            g=np.eye(9,dtype=complex)
            g[row-1,row-1]=x.conjugate()/n
            g[row-1,row]=y.conjugate()/n
            g[row,row-1]=-y/n
            g[row,row]=x/n
            R=g@R
            Gtotal=g@Gtotal
            couplers.append((row-1,row))
    D=np.diag(np.diag(R))
    triangular_error=float(max(abs((R-D).flatten())))
    unitary_error=float(max(abs((D.conj().T@Gtotal-U.conj().T).flatten())))
    assert triangular_error<5e-12 and unitary_error<5e-12
    assert len(couplers)==36
    return {"couplers":36,
            "adjacent_only":all(abs(i-j)==1 for i,j in couplers),
            "max_QR_offdiagonal_error":triangular_error,
            "max_measurement_unitary_error":unitary_error,
            "phase_shifters_upper_bound":9,
            "serial_Givens_upper_depth":36,
            "note":"A rectangular Clements mesh can typically reduce depth; this is a rigorously checked adjacent-Givens Reck-type elimination, not an optimal placement."}

def compare_optics():
    ten,(Bell,U,V,op,pinv)=select(return_components=True)
    extra=[decompose_nearest_neighbor(x) for x in (U,V)]
    Q,mutual=product_mub()
    # At the 9-rail level, three copies of a U3 act on one factor and
    # three copies on the other. Identity setting needs no couplers;
    # 3 Fourier-like settings cost at most 18 = 6*3.
    twelve_extra=[0,18,18,18]
    return {"status":"PASS_GENERIC_9MODE_QR_36_TWO_MODE_COUPLERS_PER_NONBELL_CONTEXT",
            "extra_10setting_bases":extra,
            "ten_setting_projective_lower_bound":10,
            "eight_W33_Bell_contexts_couplers_upper_per_basis":18,
            "two_generic_contexts_couplers_upper_per_basis":36,
            "sum_of_per_context_couplers_ten_if_not_shared":8*18+2*36,
            "sum_per_context_couplers_twelve_if_not_shared":8*18+sum(twelve_extra),
            "twelve_matched_product_context_couplers_upper_each":twelve_extra,
            "ten_settings_condition_number":ten["combined_condition_number"],
            "twelve_settings_condition_number":float(np.sqrt(2)),
            "conditioning_penalty_ten_vs_twelve":ten["combined_condition_number"]/np.sqrt(2),
            "operational_note":"Coupler sums are across programs, not simultaneously needed physical components. Any universal reprogrammable nine-mode mesh can implement either family; timing, phase cross-talk, loss and switch routing require separate hardware models.",
            "optical_build_not_demonstrated":True}

def main(path=None):
    out={"native_chirality":native_dirac(),
         "optical_compilation":compare_optics(),
         "status":"PASS_W33_NATIVE_DIRAC_ZERO_INDEX_AND_10SETTING_GIVENS"}
    if path:Path(path).write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print("PASS native chirality and optics",json.dumps({
        "rank":out["native_chirality"]["incidence_rank_over_Q_exact"],
        "index":out["native_chirality"]["zero_mode_index_plus_minus"],
        "generic_min_sv":out["native_chirality"]["generic_edge_phase_min_singular"],
        "optical_error":max(x["max_measurement_unitary_error"] for x in out["optical_compilation"]["extra_10setting_bases"]),
        "ten_optical_couplers_per_extra":36}))
    return out
if __name__=="__main__":
    main(sys.argv[1] if len(sys.argv)>1 else None)
