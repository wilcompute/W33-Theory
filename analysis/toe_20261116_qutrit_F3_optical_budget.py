"""Executable three-time-bin four-MUB optical protocol and trusted detector budget.

d=3 four bases are computational and three quadratic-chirped
Fourier matrices U_b=D_b F3, b=0,1,2, D_b=diag(omega^(2*b*n^2)).
For Bell reference measure conjugate U_b*; for signal U_b.
Projective matched event is sum_k P_R(b,k) tensor P_S(b,k).
We prove sum_b P_match(b) = I9 + 3 |Phi3><Phi3|.
The U_b† three-port analysis circuit is phase D_b† followed by F3†;
a deterministic Reck Givens decomposition of F3† uses 3 two-mode
lossless couplers and diagonal output phase.

An event-ready attempt must exist independent of coincidence;
no-clicks count 0. With Gaussian independent bin dephasing
variance sigma² and isotropic source visibility v, predict Bell
fidelity F = v*(1+2exp(-sigma²))/3 + (1-v)/9;
matched probability q = (1+3F)/4.
Photonic efficiencies eta=eta_ref*eta_signal*eta_memory*eta_path.
Separable null p0=1/2+epsilon+setting_TV.
This is a trusted-device model and synthetic protocol, no hardware.
"""
import json, math, cmath
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_qutrit_F3_4MUB_optical_noise_budget.json"
w=cmath.exp(2j*math.pi/3)

def matrices():
    n=np.arange(3)
    F=np.array([[w**(i*j)/math.sqrt(3) for j in range(3)] for i in range(3)],complex)
    B=[np.eye(3,dtype=complex)]
    for b in range(3):
        D=np.diag([w**(2*b*i*i) for i in range(3)])
        B.append(D@F)
    return F,B

def reck3(U):
    """U = G1^dag... G3^dag D with 3 neighboring two-mode couplers."""
    V=U.copy()
    givens=[]
    for j in range(2):
        for i in range(2,j,-1):
            a,b=V[i-1,j],V[i,j]
            norm=math.sqrt(abs(a)**2+abs(b)**2)
            G=np.array([[a.conjugate()/norm,b.conjugate()/norm],
                        [-b/norm,a/norm]],complex)
            H=np.eye(3,dtype=complex)
            H[i-1:i+1,i-1:i+1]=G
            V=H@V
            givens.append(H)
    D=np.diag(np.diag(V))
    assert np.max(np.abs(V-D))<1e-12
    rec=D.copy()
    for G in reversed(givens):
        rec=G.conj().T@rec
    assert np.max(np.abs(rec-U))<1e-12
    assert len(givens)==3
    return {"couplers":len(givens),
       "mode_pairs_in_application_order":[[int(np.where(abs(H-np.eye(3))>1e-10)[0].min()),int(np.where(abs(H-np.eye(3))>1e-10)[0].max())] for H in givens],
       "reconstruction_max_error":float(np.max(np.abs(rec-U))),
       "unitarity_error":float(np.max(np.abs(U.conj().T@U-np.eye(3))))}

def mub_identity():
    F,B=matrices()
    phi=np.zeros(9,complex)
    for i in range(3):phi[3*i+i]=1/math.sqrt(3)
    projector=np.outer(phi,phi.conj())
    operator=np.zeros((9,9),complex)
    overlap=np.zeros((4,4))
    for b,U in enumerate(B):
        for k in range(3):
            state=np.kron(U[:,k].conj(),U[:,k])
            operator+=np.outer(state,state.conj())
        for c,V in enumerate(B):
            if b!=c: overlap[b,c]=np.max(abs(U.conj().T@V)**2)
    err=float(np.max(abs(operator-np.eye(9)-3*projector)))
    assert err<1e-12
    assert np.allclose(overlap[~np.eye(4,dtype=bool)],1/3,atol=1e-12)
    return {"operator_max_norm_residual":err,
            "mutually_unbiased_pairwise_overlap_squared":1/3,
            "F3_analzyer_Reck_couplers":reck3(F.conj().T)}

def case(visibility,sigma,eta_R,eta_S,eta_memory,eta_path,eps=.01,leak=.0):
    if not(all(0<=v<=1 for v in (visibility,eta_R,eta_S,eta_memory,eta_path)) and sigma>=0 and eps>=0 and leak>=0):raise ValueError("bad model inputs")
    eta=eta_R*eta_S*eta_memory*eta_path
    coh=math.exp(-sigma**2)
    F=visibility*(1+2*coh)/3+(1-visibility)/9
    q=(1+3*F)/4
    p0=.5+eps+leak
    observed=eta*q
    threshold=p0/q
    return {"v":visibility,"phase_sigma_radians":sigma,
       "reference_detector_efficiency":eta_R,"signal_detector_efficiency":eta_S,
       "memory_throughput":eta_memory,"optical_path_throughput":eta_path,
       "total_eventready_pair_detection":eta,
       "coherence_multiplier":coh,"Bell_fidelity":F,
       "matched_probability_given_perfect_detection":q,
       "observed_clickmatch_probability":observed,
       "calibrated_separable_null_p0":p0,
       "minimum_pair_efficiency_to_be_detectable":threshold,
       "detectable_with_positive_asymptotic_gap":observed>p0}

def verify():
    B=mub_identity()
    a=case(.75,.15,.90,.90,.95,.95)
    b=case(.75,.15,.85,.85,.80,1.)
    c=case(.75,0,1,1,1,1,eps=0)
    assert a["detectable_with_positive_asymptotic_gap"]
    assert not b["detectable_with_positive_asymptotic_gap"]
    assert abs(c["matched_probability_given_perfect_detection"]-(1+2*.75)/3)<1e-12
    assert abs(c["minimum_pair_efficiency_to_be_detectable"]-.6)<1e-12
    # 500-ps bins vs detector jitter must be independently measured;
    # no arbitrary cross-talk estimate supplied from timing alone.
    return {"status":"PASS_QUTRIT_4MUB_FOURIER_3COUPLER_AND_LOSS_PHASE_BUDGET",
       "hardware_measurement_sequence":"Herald pair before basis choice; sample one of four bases after preparation; phase-compensate R basis as U_b* and S as U_b; for b=0,1,2 apply phase D_b dagger then 3-mode Fourier inverse on signal, and conjugate on reference; time-tag computational outputs; record all no-clicks as 0.",
       "four_MUB_matrices":"U_Z=I; U_b = diag(omega^(2 b n^2)) F3 for b in {0,1,2}; F3[n,k]=omega^(nk)/sqrt(3).",
       "identity_and_analyzer":B,
       "phase_noise_law":"Gaussian independent relative phases variance sigma^2 give E Bell fidelity v*(1+2*exp(-sigma^2))/3+(1-v)/9",
       "eventready_witness_threshold":"eta_R*eta_S*eta_memory*eta_path > (1/2+eps+setting_TV) / ((1+3F)/4)",
       "not_experimental_data":True,
       "example_feasible":a,"example_not_feasible":b,
       "limits":"Source herald may not depend on the later measurement outcome, phase and setting leakage must be calibrated; single-photon memory SWAP and causal reset are not built. Hardware loss might be basis-dependent and require a per-setting POVM bound."}
if __name__=="__main__":
    x=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(x["status"],x["example_feasible"]["observed_clickmatch_probability"],x["example_not_feasible"]["observed_clickmatch_probability"])
