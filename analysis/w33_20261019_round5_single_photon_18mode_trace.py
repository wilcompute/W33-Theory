"""Front 3: single-photon, 18 optical-mode path-interferometer
realization of the 9-level normalized trace, using 9 deterministic
basis-state preparations (classical randomness). This is an exact
ideal transfer-matrix design, NOT a manufactured optical device.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from w33_20261019_nextfive_optics_su9 import proj0,proj1,proj_null,G,I9
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round5_single_photon_18mode_trace.json"
I=np.eye(9,dtype=complex)
a=proj0;b=proj1;c=proj_null
t=np.pi/2
def phase(P,theta):return I+(np.exp(1j*theta)-1)*P
def loop(p,q):
    U=phase(p,t);V=phase(q,t)
    return U@V@U.conj().T@V.conj().T
H=np.kron(np.array([[1,1],[1,-1]],complex)/np.sqrt(2),I)
def optical_matrix(W):
    CW=np.zeros((18,18),complex)
    CW[:9,:9]=I
    CW[9:,9:]=W
    return H@CW@H
def per_j_trace(W):
    V=optical_matrix(W)
    out=[]
    for j in range(9):
        inp=np.zeros(18,complex);inp[j]=1
        psi=V@inp
        p0=float(np.vdot(psi[:9],psi[:9]).real)
        p1=float(np.vdot(psi[9:],psi[9:]).real)
        out.append({"input_9mode_basis_j":j,"ancilla_0_probability":p0,
                    "ancilla_1_probability":p1,"X_mean":p0-p1,
                    "exact_Real_diagonal_W":float(W[j,j].real)})
    return out
def run():
    W=loop(a,b);N=loop(a,c)
    B=phase(proj0,t);Bi=phase(proj0,-t)
    # Exactly four projector phases, and four total basis-conjugation blocks.
    compiled=B@G@B@G.conj().T@Bi@G@Bi@G.conj().T
    errcomp=float(np.linalg.norm(W-compiled))
    errunit=float(np.linalg.norm(optical_matrix(W).conj().T@optical_matrix(W)-np.eye(18)))
    x=per_j_trace(W);null=per_j_trace(N)
    means={k:float(np.mean([v[k] for v in x])) for k in ("X_mean","exact_Real_diagonal_W")}
    mean_null=float(np.mean([v["X_mean"] for v in null]))
    expect=float(np.trace(W).real/9)
    # 9-mode register can be realized via any unitary 9-mode processor.
    # The ancilla is PATH OF SAME PHOTON: not a photon-photon gate.
    # Input I9/9 comes from classical randomization over nine basis modes.
    # Each trial is pure; the trace is recovered by balanced averaging.
    checks={"18mode_optical_transfer_unitary":errunit<1e-12,
            "four_projector_pulses_compose":errcomp<1e-12,
            "normalized_trace_averaging":abs(means["X_mean"]-expect)<1e-12,
            "ideal_deficit_noncommuting_8_over_27":abs(1-expect-8/27)<1e-12,
            "commuting_control_null":abs(1-mean_null)<1e-12,
            "probabilities_within_zero_one":all(0<=v["ancilla_0_probability"]<=1 and 0<=v["ancilla_1_probability"]<=1 for v in x+null)}
    out={"schema":"w33.round5.single_photon_18mode_trace.v1",
      "architecture":"ONE PHOTON: 2 path modes (ancilla) x 9 OAM/time-bin/spatial register modes. Two balanced path couplers H and a one-arm 9x9 loop W; mode count 18. Nine equiprobable basis inputs yield I9/9, no genuine two-photon controlled operation required.",
      "basis":"|path> tensor |j> for j=0,...,8; deterministic classical preparation of j per trial",
      "network":"H2 x I9; path-controlled W=diag(I9,W); H2 x I9; measure port-0 vs port-1, sum over 9 internal output modes.",
      "controlled_loop_compilation":"W=U_P(theta) G U_P(theta) G^dag U_P(-theta) G U_P(-theta) G^dag, G=CZ*(F3 tensor I3); 4 rank3 projector phase pulses, 2 G and 2 G^dag, 2 path Hadamards; 9 mode hardware on signal arm only.",
      "coherent_gate_not_required":"No photon-photon entangling gate. One coherent photon carrying path+9-mode DOFs implements ideal transfer matrix. Large detector arrays / mode sorter and interferometric stability still required.",
      "per_input_signal":x,"per_input_commuting_null":null,
      "mean_signal":means,"mean_null":mean_null,
      "expected_trace":expect,"compiled_loop_residual":errcomp,"unitarity_residual":errunit,
      "ideal_deficit":1-expect,
      "prior_art":"Generic single-photon OAM/path controlled unitaries and DQC1 trace interferometry are established: https://link.springer.com/article/10.1140/epjqt/s40507-022-00142-1 and https://link.springer.com/article/10.1007/s13538-025-02006-2",
      "scope":"This is an ideal network synthesis, not experimental calibration or evidence of universal photonic/TOE computation. Rank3 phase shifts in OAM/time-bin register and controlled beam paths require hardware-specific designs.",
      "checks":{k:bool(v) for k,v in checks.items()},"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"checks":out["checks"],"deficit":out["ideal_deficit"],
       "unitarity_residual":errunit,"compile_residual":errcomp},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
