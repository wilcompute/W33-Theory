#!/usr/bin/env python3
"""Forty native Witting tetrads vs full 40-POVM vs seeded random U4 bases.

Assess experimentally simpler single-basis projective readout of the
440 E8-derived mixed ququart states under a declared fixed uniform
440-label prior. The forty Witting tetrads are existing tomography
contexts, NOT new. Uniform randomly chosen labeled tetrad measurement
reproduces exactly the full Witting 40-outcome POVM information by
fourfold ray incidence; selecting best tetrad can outperform it.
Seeded Haar bases are *sampled candidates* only, not a proven optimum.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):
    if str(p) not in sys.path:sys.path.insert(0,str(p))
from exploration.w33_witting_srg_bridge import construct_witting_rays,witting_orthogonal_tetrads
OUT=ROOT/"data/toe_20261104_two_e8_witting_basis_information_search.json"
def mutual(q):
    assert np.min(q)>-1e-10 and np.max(abs(np.sum(q,axis=1)-1))<1e-10
    q=np.maximum(q,1e-300)
    marginal=q.mean(axis=0)
    return float(np.mean(np.sum(q*np.log2(q/marginal),axis=1)))
def main():
    j=json.loads((ROOT/"data/toe_20261104_witting_operator_dark_spectral_A5_duality.json").read_text())
    roots=json.loads((ROOT/"data/toe_20261104_two_e8_root_to_witting_density_codebook.json").read_text())
    O=np.array(j["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_real"])+1j*np.array(
      j["A5_classes"][1]["explicit_8_Hermitian_ququart_observables_imag"])
    theta01=np.array(roots["eight_real_parameters_for_440_states"])
    rays=np.array(construct_witting_rays())
    contexts=witting_orthogonal_tetrads()
    assert len(contexts)==40 and all(len(x)==4 for x in contexts)
    assert all(sum(i in b for b in contexts)==4 for i in range(40))
    rng=np.random.default_rng(992013)
    rand=[]
    for i in range(320):
        H=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        q,r=np.linalg.qr(H)
        phase=np.diag(r)/np.abs(np.diag(r))
        q=q*phase
        assert np.max(abs(q.conj().T@q-np.eye(4)))<1e-12
        rand.append(q.T) # q columns are output kets, row convention
    result=[]
    for eps in (.1,.2):
        theta=theta01*(eps/.1)
        rho=np.eye(4)[None,:,:]/4+np.einsum("nj,jab->nab",theta,O)
        assert np.min(np.linalg.eigvalsh(rho))>0
        prob40=1/40+theta@np.array(j["A5_classes"][1]["explicit_W33_40x8_observable_coefficient_map"]).T/5
        target=mutual(prob40)
        records=[]
        for b in contexts:
            states=rays[list(b)]
            probs=np.einsum("ia,nab,ib->ni",states.conj(),rho,states).real
            records.append(mutual(probs))
        assert abs(np.mean(records)-target)<1e-10
        random_scores=[]
        for states in rand:
            probs=np.einsum("ia,nab,ib->ni",states.conj(),rho,states).real
            random_scores.append(mutual(probs))
        best_idx=int(np.argmax(records))
        best_rand=int(np.argmax(random_scores))
        result.append(dict(epsilon=eps,
          uniform_Witting40_POVM_information_bits=target,
          uniform_random_labeled_Witting_tetrad_information_bits=float(np.mean(records)),
          all_40_native_Witting_tetrad_information_bits=records,
          best_native_tetrad_index=best_idx,
          best_native_tetrad_ray_labels=list(contexts[best_idx]),
          best_native_tetrad_bits=float(max(records)),
          worst_native_tetrad_bits=float(min(records)),
          native_tetrad_information_ratio_best_to_full=float(max(records)/target),
          sampled_Haar_basis_count=len(rand),
          seeded_Haar_median_information_bits=float(np.median(random_scores)),
          seeded_Haar_best_information_bits=float(max(random_scores)),
          seeded_Haar_worst_information_bits=float(min(random_scores)),
          best_sampled_Haar_unitary_rows_real=rand[best_rand].real.tolist(),
          best_sampled_Haar_unitary_rows_imag=rand[best_rand].imag.tolist(),
          global_optimum_claimed=False))
    out=dict(status="PASS_440_ROOT_WITTING_NATIVE_TETRAD_VS_HAAR_BASIS_INFORMATION_BUDGET",
       root_labels=440,ququart_dimension=4,
       fixed_uniform_prior=True,
       exact_Witting_tetrad_incidence_each_ray_in_four_tetrads=True,
       uniform_random_Witting_tetrad_with_basis_label_equals_full_POVM_information=True,
       epsilon_scan=result,
       novelty_boundary="Existing Witting tetrads, Born rule and classical mutual information. Independent new comparative work uses specific constructed 440 E8-root density codebook; random Haar performance is seeded empirical only.",
       physical_boundary="Computational information for iid known density preparations; not a proof of optimal measurement or finite-shot decoding, not an actual photonic test, nor temporal self-entanglement or TOE.")
    OUT.write_text(json.dumps(out,indent=2)+"\n",encoding="utf8")
    print(out["status"], [(r["epsilon"],r["uniform_Witting40_POVM_information_bits"],r["best_native_tetrad_bits"],r["seeded_Haar_best_information_bits"]) for r in result],flush=True)
    return out
if __name__=="__main__":main()
