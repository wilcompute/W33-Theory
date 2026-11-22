"""Exact Witting 2-design experiment: Schmidt-number coincidence and EB channel.

This is a trusted-measurement mathematical witness, NOT Bell nonlocality.
The Witting 40-ray 2-design is known prior geometry; new here are explicit
single-setting Schmidt thresholds, compressed-bin negative controls, and
the coherent-versus-measure/reprepare channel capacity distinction.
"""
from __future__ import annotations
import json, math,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"analysis"))
import toe_20261121_relational_reference_pareto as prior
OUT=ROOT/"data/toe_20261122_2design_entanglement_capacity.json"
OLD=[31,7,21,28,22,30,3,15,4,23,26,25,8,1,32,20,19,29,14,38,16,39,11,37]
NEW=[0,1,2,9,6,8,14,11,12,13,15,16,19,21,23,18,27,28,30,32,34,35,37,39]
def run():
    rays,_,_,_=prior.geometry()
    P=np.einsum("ai,aj->aij",rays,rays.conj())
    assert np.max(abs(P.sum(0)-10*np.eye(4)))<1e-12
    F=np.zeros((16,16),complex)
    for a in range(4):
        for b in range(4):F[4*a+b,4*b+a]=1
    phi=np.eye(4).reshape(16)/2; target=np.outer(phi,phi.conj())
    D=sum(np.kron(p,p) for p in P)
    C=sum(np.kron(p,p.conj()) for p in P)
    err=max(float(np.max(abs(D-2*(np.eye(16)+F)))),
            float(np.max(abs(C-2*np.eye(16)-8*target))))
    assert err<1e-11
    same=C/100
    thresholds=[]
    for k in (1,2,3):
        psi=np.zeros(16,dtype=complex)
        for a in range(k):psi[4*a+a]=1/math.sqrt(k)
        val=float(np.vdot(psi,same@psi).real)
        assert abs(val-(.02+.02*k))<1e-12
        thresholds.append({"maximum_Schmidt_number":k,
                 "p_same_upper_bound":.02+.02*k,
                 "certified_if_exceeded_at_least":k+1,
                 "saturated_by_Schmidt_rank_k_pure_state":True})
    iso=[]
    for v in (0,.1,.2,.25,.5,11/15,.75,1.):
        rho=v*target+(1-v)*np.eye(16)/16
        prob=float(np.trace(same@rho).real)
        assert abs(prob-(.025+.075*v))<1e-12
        iso.append({"visibility":v,"p_same":prob})
    compressed=[]
    for name,sel in (("prior25",OLD),("private_fisher25",NEW)):
        pool=sum(P[i] for i in range(40)if i not in sel)
        M=[P[i]/10 for i in sel]+[pool/10]
        S=sum(np.kron(m,m.conj())for m in M)
        pphi=float(np.vdot(phi,S@phi).real)
        _,V=np.linalg.eigh(pool)
        x=V[:,-1]
        psep=float(sum(np.vdot(x,m@x).real**2 for m in M))
        assert psep>pphi
        compressed.append({"layout":name,"p_same_on_maximally_entangled_target":pphi,
             "p_same_on_explicit_separable_product_state":psep,
             "naive_threshold_from_full_40_is_invalid":True})
    rng=np.random.default_rng(20261122)
    dep_errors=[]
    for _ in range(10):
        Z=rng.normal(size=(4,4))+1j*rng.normal(size=(4,4))
        rho=Z@Z.conj().T;rho/=np.trace(rho)
        measure_reprepare=sum(np.trace(p@rho)*p for p in P)/10
        dep_errors.append(float(np.max(abs(measure_reprepare-(np.eye(4)+rho)/5))))
    assert max(dep_errors)<1e-11
    # Choi of E(rho)=(rho+I)/5 has singlet fraction exactly 1/4,
    # the separability boundary for four-dimensional isotropic states.
    dep_choi_singlet_fraction=.2+.8/16
    assert abs(dep_choi_singlet_fraction-.25)<1e-12
    finite_shots=[]
    for v in (.25,.5,1.):
        eta=.8;pnull=eta**2*.04
        gap=eta**2*(.025+.075*v-.04)
        finite_shots.append({"isotropic_visibility":v,
          "each_detector_efficiency":eta,
          "illustrative_5sigma_normal_approx_launches":int(math.ceil(25*pnull*(1-pnull)/gap**2))})
    result={"status":"PASS","date":"2026-11-22","rays":40,
      "exact_2design_identity":"sum P_i tensor P_i = 2*(I_16+SWAP)",
      "same_label_effect":"sum_i (P_i/10) tensor (conjugate(P_i)/10) = .02I+.08|Phi4><Phi4|",
      "max_identity_error":err,"Schmidt_number_thresholds":thresholds,
      "isotropic_states":"p_same=.025+.075visibility; entangled iff visibility > .2",
      "isotropic_scan":iso,"compressed_separable_counterexamples":compressed,
      "measure_reprepare_identity":"sum_i Tr(P_i rho)P_i/10=(rho+I_4)/5",
      "measure_reprepare_depolarizing_shrinkage":.2,
      "Choi_singlet_fraction":dep_choi_singlet_fraction,
      "measure_reprepare_channel_is_entanglement_breaking":True,
      "max_tested_reprepare_identity_residual":max(dep_errors),
      "5sigma_illustrative_shots":finite_shots,
      "limits":"Trusted calibrated 40-outcome analyzers and paired labels; not Bell nonlocality, self-testing, or device-independent certification. 25-bin high coincidences need NOT imply entanglement. Measure-and-reprepare cannot preserve quantum capacity, unlike coherent Witting channel models. Normal approximation not a finite-shot guarantee."}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("PASS Witting 2-design Schmidt witness, compressed no-go, EB channel.")
    return result
if __name__=="__main__":run()
