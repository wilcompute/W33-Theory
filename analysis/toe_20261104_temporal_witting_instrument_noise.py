#!/usr/bin/env python3
"""CPTP Witting ququart readout of 2-time qutrit history + loss-aware no-go.

The existing repo establishes Witting 40 projective 2-design, graph W33,
TOE90 entanglement witness and Vlasov's 2025 QKD proposal. This
producer constructs 120 explicit Kraus operators K_(ray,input-index):
  C3_out ⊗ C3_in* (9D) --> C4 Witting ququart
with Witting POVM and measure/prepare. Check CPTP, EB, and a
sharp operational *limitation*: an output-only Witting POVM cannot
tell ideal identity-channel Choi J0 from completely depolarized J1;
they have the same output marginal. Joint process tomography can.

Also compute flagged-photon erasure, temporal depolarizing
composition, and normalized Choi negativity with loss.
"""
from __future__ import annotations
import json,math,sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
OUT=ROOT/"data"/"toe_20261104_temporal_witting_instrument_noise.json"
from exploration.w33_witting_srg_bridge import construct_witting_rays

def ptrace_in(rho,do=3,di=3):
    return np.einsum("aibi->ab",rho.reshape(do,di,do,di))
def negativity(rho,do,di):
    pt=rho.reshape(do,di,do,di).transpose(0,3,2,1).reshape(do*di,do*di)
    return float(sum(max(0,-e) for e in np.linalg.eigvalsh(pt)))
def jo_chanel(t):
    phi=np.eye(3,dtype=complex).reshape(-1)/math.sqrt(3)
    return t*np.outer(phi,phi.conj())+(1-t)*np.eye(9)/9

def build():
    rays=np.asarray(construct_witting_rays())
    assert rays.shape==(40,4)
    P=np.array([np.outer(r,r.conj()) for r in rays])
    assert np.max(abs(P.sum(axis=0)-10*np.eye(4)))<1e-12
    swap=np.zeros((16,16),dtype=complex)
    for i in range(4):
        for j in range(4):
            swap[4*i+j,4*j+i]=1
    design=sum(np.kron(proj,proj) for proj in P)
    assert np.max(abs(design-2*(np.eye(16)+swap)))<1e-11

    V=np.eye(4,3,dtype=complex)
    kraus=[]
    for proj in P:
        for a in range(3):
            bra=np.eye(3,dtype=complex)[a:a+1,:]
            kraus.append(np.kron(proj@V,bra)/math.sqrt(10))
    assert len(kraus)==120 and all(K.shape==(4,9) for K in kraus)
    completeness=sum(K.conj().T@K for K in kraus)
    assert np.max(abs(completeness-np.eye(9)))<1e-12

    cases=[]
    for depolarizing_probability in (0,.25,.5,.75,1):
        t=1-depolarizing_probability
        J=jo_chanel(t)
        out=sum(K@J@K.conj().T for K in kraus)
        marg=ptrace_in(J)
        assert np.max(abs(marg-np.eye(3)/3))<1e-12
        assert np.max(abs(out-sum(
            (np.trace((proj@V)@marg@(proj@V).conj().T)/10)*proj
            for proj in P)))<1e-12
        probabilities=np.array([sum(float(np.trace(K@J@K.conj().T).real)
                for K in kraus[3*i:3*i+3]) for i in range(40)])
        assert abs(probabilities.sum()-1)<1e-12
        expected=np.array([np.trace((V.conj().T@proj@V)@marg).real/10 for proj in P])
        assert np.max(abs(probabilities-expected))<1e-12
        cases.append(dict(p=depolarizing_probability,
           trace_output_local=np.round(probabilities,12).tolist(),
           output_ququart_diagonal=np.round(out.diagonal().real,12).tolist(),
           trace_norm_Choi_vs_identity=float(np.sum(abs(np.linalg.eigvalsh(J-jo_chanel(1)))))))
    assert all(c["trace_output_local"]==cases[0]["trace_output_local"] for c in cases)
    assert all(c["output_ququart_diagonal"]==cases[0]["output_ququart_diagonal"] for c in cases)
    # Max possible joint two-time distinguishing success for J0 vs J1
    # is 1/2(1+D), D=1/2||J0-J1||_1=8/9.
    D=.5*cases[-1]["trace_norm_Choi_vs_identity"]
    assert abs(D-8/9)<1e-12

    noise=[]
    Jvac=np.zeros((12,12),dtype=complex)
    # Factor ordering output4 ⊗ input3; pure vacuum output component3.
    Jvac[9:12,9:12]=np.eye(3)/3
    embed=np.kron(V,np.eye(3))
    for m in (0,1,4,8,13,14,20):
        t=.9**m
        for eta in (1,.6,.2,0):
            J=eta*embed@jo_chanel(t)@embed.conj().T+(1-eta)*Jvac
            assert abs(np.trace(J)-1)<1e-12
            assert np.min(np.linalg.eigvalsh(J))>-1e-12
            N=negativity(J,4,3)
            expected=eta*max(0,(4*t-1)/3)
            assert abs(N-expected)<1e-11
            F=(1+8*t)/9
            noise.append(dict(exchange_count=m,
                per_exchange_depolarizing_probability=.1,
                survival_probability=eta,
                normalized_postselected_Choi_fidelity=F,
                Choi_entanglement_negativity_unconditional=N,
                entanglement_breaking_conditional_on_survival=t<=.25+1e-12,
                mean_tries_per_success=None if eta==0 else 1/eta))
    assert all(x["Choi_entanglement_negativity_unconditional"]==0
        for x in noise if x["exchange_count"]==14)
    assert all(x["Choi_entanglement_negativity_unconditional"]>0
        for x in noise if x["exchange_count"]==13 and x["survival_probability"]>0)
    return dict(status="PASS_WITTING_120_KRAUS_CPTP_INSTRUMENT_AND_TEMPORAL_NO_GO",
      Witting_40_ray_first_moment_identity="sum_r |r><r|=10 I4",
      Witting_40_ray_second_moment_identity="sum_r P_r⊗P_r=2(I16+SWAP)",
      kraus_operator_count=120,
      input_history_dimension=9,output_ququart_dimension=4,
      CPTP_completeness_worst_residual=float(np.max(abs(completeness-np.eye(9)))),
      map_is_measure_and_prepare_entanglement_breaking=True,
      p0_to_p1_channel_states_full_joint_trace_distance=D,
      ideal_joint_time_process_distinguishing_success_probability=(1+D)/2,
      output_only_Witting_readout_p0_vs_p1_trace_distance=0,
      output_only_Witting_readout_p0_vs_p1_success_probability=.5,
      output_only_process_state_reduction="I3/3 for every depolarizing p; Witting measures only the output qutrit (embedded in C4), losing input-output correlations",
      sample_readouts=cases,
      flagged_erasure_and_repeated_exchanges=noise,
      last_entangled_exchange_for_p_point_one=13,
      first_entanglement_breaking_exchange_for_p_point_one=14,
      quantitative_assumptions="Each exchange independently applies depolarizing p=0.1; independent vacuum erasure with flagged survival eta; no coherent memory cross-talk, no postselection cost beyond 1/eta, and trusted Choi tomography.",
      physical_limit="This is a CPTP 9D->4D Witting measure-prepare channel that DESTROYS temporal correlations. It proves no autonomous output-only Witting ray POVM on a maximally mixed output can certify Choi self-entanglement; joint multi-time intervention/process tomography needed. It does not prove a single self-entangled photon or retrocausal signaling.",
      prior_art="Vlasov Witting scheme arxiv:2503.18431; repo TOE90 2-design, 2026-11-04 temporal Choi; general entanglement breaking/depolarizing threshold is standard QIT.")
def main():
    out=build()
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(out["status"],"joint",out["ideal_joint_time_process_distinguishing_success_probability"],flush=True)
    return out
if __name__=="__main__":main()
