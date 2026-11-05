#!/usr/bin/env python3
"""Follow-through fronts 3–5: Witting Helstrom mesh, trusted qutrit reset, flavour/chirality.

Reuses the repository's authoritative Witting rays, 4-port Givens compiler,
and exact three-time qutrit memory model. Reports idealized experiments only.
"""
from __future__ import annotations
from itertools import combinations,product
from pathlib import Path
from fractions import Fraction
import math,sys,json
import numpy as np
from scipy.stats import binom
ROOT=Path(__file__).resolve().parents[1]
for p in (ROOT,ROOT/"analysis"):sys.path.insert(0,str(p))
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays
from toe_20261104_fourrail_givens_drift_detector_validation import compile_mesh,emitted
from toe_20261104_reset_immune_quantum_memory_falsifier import evolution,negativity,fidelity

OUT=ROOT/"data"/"toe_20261105_photon_memory_chirality.json"

def photonic():
    rays=np.asarray(construct_witting_40_rays(),complex)
    assert rays.shape==(40,4)
    P=np.einsum("ja,jb->jab",rays,rays.conj())
    assert np.max(abs(sum(P)-10*np.eye(4)))<1e-11
    O=np.abs(rays.conj()@rays.T)**2
    pairs={
      "orthogonal":next((i,j)for i,j in combinations(range(40),2) if O[i,j]<1e-10),
      "nonorthogonal":next((i,j)for i,j in combinations(range(40),2) if abs(O[i,j]-1/3)<1e-10)
    }
    rng=np.random.default_rng(20261105)
    records=[]
    for kind,(i,j) in pairs.items():
        for eps in (.1,.2):
            A=(1-eps)*np.eye(4)/4+eps*P[i]
            B=(1-eps)*np.eye(4)/4+eps*P[j]
            eig,U=np.linalg.eigh(A-B)
            expected=eps*math.sqrt(1-O[i,j])
            trace_distance=float(np.sum(abs(eig))/2)
            assert abs(trace_distance-expected)<1e-12
            # Interferometer U^dagger diagonalizes the Helstrom difference.
            optimal=U.conj().T
            gates,phases=compile_mesh(optimal)
            assert len(gates)<=6
            ports_A=np.real(np.diag(optimal@A@optimal.conj().T))
            ports_B=np.real(np.diag(optimal@B@optimal.conj().T))
            tvports=float(sum(abs(ports_A-ports_B))/2)
            assert abs(tvports-trace_distance)<1e-12
            probs_A=np.real(np.einsum("jab,ba->j",P,A))/10
            probs_B=np.real(np.einsum("jab,ba->j",P,B))/10
            tvw=float(sum(abs(probs_A-probs_B))/2)
            assert tvw<trace_distance-1e-10
            calibrations=[]
            for sigma in (0,.005,.02):
                tvs=[]
                for _ in range(32):
                    V=emitted(gates,phases,rng,sigma)
                    p=np.real(np.diag(V@A@V.conj().T))
                    q=np.real(np.diag(V@B@V.conj().T))
                    tvs.append(float(sum(abs(p-q))/2))
                if sigma==0:assert max(abs(v-trace_distance) for v in tvs)<1e-11
                calibrations.append(dict(assumed_static_beamsplitter_noise_sigma=sigma,
                                         realizations=32,
                                         mean_port_total_variation=float(np.mean(tvs)),
                                         worst_observed_port_total_variation=float(min(tvs))))
            for eta in (.6,.85,1.):
                native=.5*(1+eta*tvw)
                helm=.5*(1+eta*trace_distance)
                assert helm>native
                records.append(dict(type=kind,ray_pair=[i,j],epsilon=eps,
                  independent_loss_efficiency=eta,
                  native_Witting40_success=native,
                  Helstrom_four_port_success=helm,
                  Helstrom_trace_distance=trace_distance,
                  Witting_total_variation=tvw,
                  two_mode_givens_gates=len(gates),
                  ideal_mesh_reconstruction_verified=True,
                  static_calibration_samples=calibrations if eta==.85 else None))
    return dict(status="PASS_NATIVE_WITTING_VS_PAIR_ADAPTED_HELSTROM_COMPILED",
                physical_modes=4,native_effects=40,records=records,
                bound="All mixed state preparations and detector loss models are assumed; calibration drift samples do not give a worst-case certified hardware bound.",
                prior_art="Helstrom discrimination, ququart unitary Givens decomposition, and Witting 2-design are known.")

def memory():
    fcoh=fidelity(evolution())
    fclassic=fidelity(evolution("classical"))
    fmark=fidelity(evolution("depolarizing",0))
    assert abs(fcoh-1)<1e-12 and abs(fclassic-1/3)<1e-12 and abs(fmark-1/9)<1e-12
    records=[]
    for p in (.2,.3,.35,.6,1.):
        rho=evolution("depolarizing",p)
        f=fidelity(rho);neg=negativity(rho)
        assert abs(f-(1+8*p)/9)<1e-12
        assert abs(neg-max(0,(4*p-1)/3))<1e-12
        eta=.85;n=3000;alpha=.01
        # Separable EB-memory benchmark with the exact same independently
        # calibrated detector efficiency.
        pnull=eta/3+(1-eta)/9
        palt=eta*f+(1-eta)/9
        threshold=int(binom.isf(alpha,n,pnull))+1
        fp=float(binom.sf(threshold-1,n,pnull))
        power=float(binom.sf(threshold-1,n,palt))
        assert fp<=alpha+1e-12
        records.append(dict(memory_survival=p,quantum_fidelity=f,
                            negativity=neg,detector_efficiency=eta,
                            calibrated_separable_null=pnull,
                            unconditional_success_probability=palt,
                            shots=n,rejection_threshold=threshold,
                            binomial_false_positive=fp,binomial_power=power))
    # Explicit outcome-dependent herald for a *separable* F=1/3 input:
    # conditional fidelity may exceed 1/3 if the apparatus preferentially
    # retains Bell-projection successes. It is NOT fair sampling.
    fbase=1/3
    positive_eta=.95;negative_eta=.10
    selected=positive_eta*fbase/(positive_eta*fbase+negative_eta*(1-fbase))
    assert selected>.8
    assert any(x["binomial_power"]>.99 for x in records if x["memory_survival"]>=.6)
    return dict(status="PASS_QUTRIT_RESET_MEMORY_TRUSTED_LOSS_AND_ADVERSARIAL_HERALD",
                coherent_reset_fidelity=fcoh,classical_dephased_memory_fidelity=fclassic,
                no_memory_fidelity=fmark,
                binomial_records=records,
                state_dependent_loss_false_witness_conditional_fidelity=selected,
                state_dependent_loss_detector_success_eta=.95,
                state_dependent_loss_detector_failure_eta=.10,
                scope="Outcome-dependent detection falsely inflates a separable state's conditional Bell statistic; this is a measurement bias, not entanglement. Trusted independent efficiency and no quantum bypass remain necessary.")

def flavor():
    # All charges in units of X=a*(6Y)+b*(3(B-L)), LH Weyl basis.
    data={"Q":(6,1,1),"uc":(3,-4,-1),"dc":(3,2,-1),
          "L":(2,-3,-3),"ec":(1,6,3),"nc":(1,0,3)}
    records=[]
    for a,b in product(range(-3,4),repeat=2):
        if not (a or b):continue
        charge={s:a*ys+b*bl for s,(_,ys,bl) in data.items()}
        # SU3^2 X, SU2^2 X, mixed gravity, cubic X,
        # Y^2X and YX^2: multiply by 36 or 6 to keep integers.
        anomalies=[
            2*charge["Q"]+charge["uc"]+charge["dc"],
            3*charge["Q"]+charge["L"],
            sum(data[s][0]*charge[s] for s in data),
            sum(data[s][0]*charge[s]**3 for s in data),
            sum(data[s][0]*data[s][1]**2*charge[s] for s in data),
            sum(data[s][0]*data[s][1]*charge[s]**2 for s in data)]
        assert anomalies==[0]*6,(a,b,anomalies)
        higgs=3*a
        yuk=[charge["Q"]+higgs+charge["uc"],
             charge["Q"]-higgs+charge["dc"],
             charge["L"]-higgs+charge["ec"],
             charge["L"]+higgs+charge["nc"]]
        assert yuk==[0]*4
        records.append(dict(a=a,b=b,charges=charge))
    assert len(records)==48
    # SSH proxy for a pair of boundary chiral modes: the two ends carry
    # opposite sublattice polarization; the finite matrix has exact
    # chiral anticommutation but not a single unpaired Weyl fermion.
    L=20
    def ssh(t1,t2):
        H=np.zeros((2*L,2*L))
        for i in range(L):
            H[2*i,2*i+1]=H[2*i+1,2*i]=t1
            if i+1<L:H[2*i+1,2*i+2]=H[2*i+2,2*i+1]=t2
        S=np.diag(np.tile([1,-1],L))
        assert np.max(abs(S@H+H@S))<1e-13
        w,V=np.linalg.eigh(H)
        pos=np.argsort(abs(w))[:2]
        return sorted(abs(w[pos])),[
            float(np.dot(V[:L*2,j].conj() * V[:L*2,j],np.arange(2*L))) for j in pos]
    top,loc=ssh(.6,1)
    triv,_=ssh(1.4,1)
    assert max(top)<1e-3 and min(triv)>.4
    return dict(status="PASS_ANOMALY_FREE_CHARGE_FAMILY_AND_CHIRAL_EDGE_PAIR_FIREWALL",
      integer_U1_charge_parameter_choices=48,
      representative_mixed_charge_records=records[:8],
      all_six_anomalies_vanish=True,
      all_four_yukawa_monomials_allowed=True,
      topological_open_SSH_smallest_abs_modes=top,
      trivial_open_SSH_smallest_abs_modes=triv,
      lattice_chiral_symmetry_exact=True,
      no_unique_flavor_selector="48 different integer charge pairs satisfy the scanned anomaly and Yukawa conditions, and the finite chiral chain produces paired boundaries. Neither fixes SM masses, CKM, CP sign, or nature's chirality.",
      prior_art="SM plus right-handed neutrino anomaly-free Y/B-L combinations and SSH boundary modes are established.")

def main():
    results={"adaptive_Witting_photonic":photonic(),
             "trusted_memory":memory(),"chirality_flavor":flavor()}
    out=dict(status="PASS_FIVE_FRONT_CONTINUATION_3OF5",results=results)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    for k,x in results.items():print("PASS",k,x["status"])
    print("CERTIFICATE",OUT)
    return out
if __name__=="__main__":main()
