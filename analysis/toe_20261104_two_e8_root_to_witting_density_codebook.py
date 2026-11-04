#!/usr/bin/env python3
"""A class1 A5-unitary-covariant 440-state mixed-ququart codebook from two E8 glues.

Two E8 root shells live in the common real A4⊕A4 eight-space:
240 roots each, exactly40 shared, hence440 unique. Transport their
normalized real eight-coordinate directions via the independently
certified W33 A5 class1 observable intertwiner to traceless Hermitian
4x4 operators O_j with Tr(O_j O_k)=2 delta_jk.

For a scaled root v of squared norm2 let t(v) be the 8D Euclidean
coordinates (norm sqrt2), rho(v)=I4/4+(epsilon/sqrt2)*sum t_j O_j.
All 440 rho are distinct, positive and mixed, with uniform exact
purity 1/4+2 epsilon². Their HS cross-overlaps are
Tr(rho_v rho_w)=1/4+epsilon²(v.w), preserving the native rational
two-glue metric, including the previously proven non-integral
mixed-sheet pairings. Witting40 POVM distinguishes all 440, with a
closed-form linear probability inversion for eight real parameters.

These 440 density preparations are NOT 440 mutually orthogonal states,
not a new finite-dimensional Hilbert space, and not a physical E8
particle spectrum, but a concrete experimentally preparable
tomographic geometric image of the existing icosian packet shell.
"""
from __future__ import annotations
import json,sys,math,collections
from pathlib import Path
import numpy as np
from scipy.spatial.distance import pdist
ROOT=Path(__file__).resolve().parents[1]
for path in (ROOT,ROOT/"analysis"):
    if str(path) not in sys.path:sys.path.insert(0,str(path))
from toe_20261104_reye_kernel_a4a4_e8_glue import roots_scaled5
OUT=ROOT/"data"/"toe_20261104_two_e8_root_to_witting_density_codebook.json"
def main():
    source=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
    class1=source["A5_classes"][1]
    E=np.array(class1["explicit_W33_40x8_observable_coefficient_map"],dtype=float)
    O=np.array(class1["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
        class1["explicit_8_Hermitian_ququart_observables_imag"])
    assert np.max(abs(E.T@E-np.eye(8)))<1e-9
    assert np.max(abs(E.T@np.ones(40)))<1e-9
    assert np.max(abs(np.real(np.einsum("iab,jba->ij",O,O))-2*np.eye(8)))<1e-9
    rootsplus=sorted(set(roots_scaled5(2)))
    rootsminus=sorted(set(roots_scaled5(3)))
    overlap=sorted(set(rootsplus)&set(rootsminus))
    union=sorted(set(rootsplus)|set(rootsminus))
    assert len(rootsplus)==len(rootsminus)==240
    assert len(overlap)==40 and len(union)==440
    # Exact 10-dimensional 5ths-coordinate representation shared by
    # the two integer E8 completions. Inherited packet potential
    # metric has scale5, hence /sqrt5 here.
    pos=[(r,c) for r in range(5) for c in range(5)]
    B=np.zeros((25,8))
    for i,(r,c) in enumerate(pos):
        for j in range(4):
            B[i,j]=int(r==j+1)-int(r==0)
            B[i,j+4]=int(c==j+1)-int(c==0)
    QB,_=np.linalg.qr(B)
    f=np.array([[(v[r]+v[c+5])/(5*math.sqrt(5)) for r,c in pos] for v in union])
    t=f@QB
    assert np.max(abs(f-t@QB.T))<1e-11
    assert np.max(abs(np.sum(t*t,axis=1)-2))<1e-11
    R=np.array(union,dtype=np.int64)
    dots_exact=R@R.T /25
    assert np.max(abs(t@t.T-dots_exact))<1e-11
    epsilon=.1
    theta=epsilon*t/math.sqrt(2)
    assert np.max(abs(np.linalg.norm(theta,axis=1)-epsilon))<1e-12
    # Uniform positivity for ALL points in the REAL 8D ball
    # ||theta||<=1/sqrt(24): for traceless Hermitian O with
    # Tr(O²)=2||theta||² and dim4, ||O||_op<=sqrt(3/2)||theta||.
    # Therefore lambda_min(I4/4+O)>=1/4-sqrt(3/2)||theta||.
    universal_radius=1/math.sqrt(24)
    assert epsilon<universal_radius
    Rho=np.eye(4)[None,:,:]/4+np.einsum("ij,jab->iab",theta,O)
    assert np.max(abs(Rho-Rho.conj().transpose(0,2,1)))<1e-10
    assert np.max(abs(np.trace(Rho,axis1=1,axis2=2)-1))<1e-10
    eigen=np.linalg.eigvalsh(Rho)
    assert float(eigen.min()) >=.25-math.sqrt(1.5)*epsilon-1e-12
    purity=np.real(np.einsum("iab,iba->i",Rho,Rho))
    assert np.max(abs(purity-(.25+2*epsilon*epsilon)))<1e-10
    root_rho_G=np.real(np.einsum("iab,jba->ij",Rho,Rho))
    target_overlap=.25+(epsilon**2)*dots_exact
    assert np.max(abs(root_rho_G-target_overlap))<1e-10
    assert len({tuple(np.round(x,10)) for x in theta})==440

    # Cross-glue ROOT bilinear form is fractional 40,000 times.
    M=np.array(rootsplus,dtype=np.int64)@np.array(rootsminus,dtype=np.int64).T
    assert M.shape==(240,240)
    fractionals=int(np.sum(M%25!=0))
    assert fractionals==40000
    assert not np.all(M%25==0)
    # Every state is distinguishable by Witting40 POVM:
    # P_i probability p_i=1/40+1/5 sum_j E_ij theta_j.
    probabilities=np.ones((440,40))/40+theta@E.T/5
    assert np.min(probabilities)>0
    assert np.max(abs(probabilities.sum(axis=1)-1))<1e-10
    reconstructed=5*probabilities@E
    assert np.max(abs(reconstructed-theta))<1e-10
    tv=pdist(probabilities,metric="cityblock")/2
    assert len(tv)==440*439//2
    assert tv.min()>1e-8
    # Information capacity: 440 possible labels do NOT carry log2(440)
    # perfectly readable bits in ONE ququart. Under a uniform 440-root
    # ensemble and the fixed 40-outcome Witting POVM, evaluate the
    # exact discrete channel's mutual information in bits/photon.
    marginal=probabilities.mean(axis=0)
    assert np.max(abs(marginal-1/40))<1e-12
    per_root_information=np.sum(probabilities*np.log2(probabilities/marginal),axis=1)
    info_bits=float(per_root_information.mean())
    assert 0<info_bits<2
    prior_entropy=math.log2(440)
    fano_error=.05
    binary_entropy=-(fano_error*math.log2(fano_error)+(1-fano_error)*math.log2(1-fano_error))
    fano_required=prior_entropy-binary_entropy-fano_error*math.log2(439)
    # I(R; Y^n) <= n I(R; Y) for n independent measurements
    # conditioned on R; by Fano this is a necessary, not sufficient,
    # sample count to classify 440 equally likely root labels.
    n_detected=math.ceil(fano_required/info_bits)
    eta=.85
    n_incident=math.ceil(fano_required/(eta*info_bits))
    assert n_incident>=n_detected>0
    # Trace overlap is a Hilbert-Schmidt observable, not a direct
    # single-copy distinguishability claim. The measurement record
    # is informationally complete on THIS eight-dimensional manifold.
    result=dict(status="PASS_440_TWO_E8_ROOT_MIXED_QUQUART_STATES_WITTING_TOMOGRAPHY",
       E8_plus_root_count=len(rootsplus),E8_minus_root_count=len(rootsminus),
       shared_roots_count=len(overlap),
       two_sheet_unique_roots_count=len(union),
       Witting_ququart_Hilbert_dimension=4,
       physical_density_matrix_parameter_dimension=8,
       Witting_40outcome_POVM_tomographic_rank_on_8D_codebook=8,
       all_440_real_root_vectors_spherical_norm_sq=2,
       all_440_hermitian_ququart_states_psd=True,
       all_440_density_matrices_distinct=True,
       uniform_real_coordinate_encoding_epsilon=epsilon,
       universal_PSD_8parameter_ball_radius=universal_radius,
       universal_lower_eigenvalue_bound=.25-math.sqrt(1.5)*epsilon,
       actual_minimum_density_eigenvalue=float(eigen.min()),
       uniform_density_purity=float(purity[0]),
       exact_density_purity_formula="1/4 + 2 epsilon^2",
       exact_density_Gram_formula="Tr(rho_r rho_s)=1/4 + epsilon^2 (r dot s)",
       maximum_density_Hilbert_Schmidt_Gram_residual=float(np.max(abs(root_rho_G-target_overlap))),
       cross_sheet_noninteger_root_innerproduct_pairs=fractionals,
       Witting_40outcome_probability_minimum=float(probabilities.min()),
       Witting_POVM_440_state_min_pair_total_variation=float(tv.min()),
       Witting_POVM_440_state_max_pair_total_variation=float(tv.max()),
       uniform_440root_label_entropy_bits=prior_entropy,
       uniform_440root_label_Witting_POVM_information_bits_per_detected_photon=info_bits,
       Holevo_single_ququart_upper_bound_accessible_bits_per_copy=2,
       Fano_target_max_classification_error=fano_error,
       Fano_required_information_bits=fano_required,
       Fano_necessary_detected_photon_count=n_detected,
       Fano_necessary_incident_photon_count_if_survival_85percent=n_incident,
       Fano_warning="Necessary information-theoretic lower bounds under known uniform 440-label prior, iid state preparation and fixed Witting POVM; NOT sufficient sample counts for an actual classifier. A collective quantum measurement may have different information per copy; single-copy Holevo bound remains 2 bits.",
       Witting_probability_linear_inverse="theta_j=5 sum_{i=1}^{40} E_ij p_i; E^T ones=0",
       all_440_exact_root_coordinates_scaled_by5=[list(v) for v in union],
       eight_real_parameters_for_440_states=theta.tolist(),
       physics_boundary="440 nonorthogonal density states controlled by classical preparations in a ququart. Cannot transmit 440 orthogonal quantum letters in dimension4; no self-entangled single photon, E8 particle representation, physical time clock, or Lorentzian dynamics.",
       provenance="E8 glues and 440 root union are existing icosian mathematics, Witting SIC/tight-frame and class1 A5 unitary support previous investigations; new is full 440-state positive quantum-operational codebook and exact root Hilbert-Schmidt Gram/tomographic inversion cert.")
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(result["status"],"min PSD",result["actual_minimum_density_eigenvalue"],
        "min TV",result["Witting_POVM_440_state_min_pair_total_variation"],flush=True)
    return result
if __name__=="__main__":main()
