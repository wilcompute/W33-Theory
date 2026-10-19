"""Round 4 front 3: exact unequal-angle commutator echo and honest
synthetic block-drift/erasure experimental error budget.

Research context: Nature Photonics 2026 high-dimensional two-photon CPF
(d=4, NOT a realized two-qutrit coherent ancilla projector gate).
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from w33_20261019_tick_operator_frame_majorization import points,symp,build_projectors
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"w33_20261019_round4_optical_correlated_noise.json"
p=points(); Q=build_projectors(p)
A=Q[0]
B=Q[3*next(j for j in range(1,40) if symp(p[0],p[j])!=0)]
C=Q[3*next(j for j in range(1,40) if symp(p[0],p[j])==0)]
I=np.eye(9,dtype=complex)
rng=np.random.default_rng(20261019)
def U(P,t):return I+np.expm1(1j*t)*P
def delta(P,R,t,s):
    X=U(P,t);Y=U(R,s)
    return float(1-np.trace(X@Y@X.conj().T@Y.conj().T).real/9)
def exact_unequal(t,s):return float((32/27)*np.sin(t/2)**2*np.sin(s/2)**2)
def simulate():
    phase=[]
    for t,s in ((np.pi/2,np.pi/2),(.2,2.),(.8,1.2),(1.4,1.7),
                (np.pi/2+.05,np.pi/2-.05),(np.pi,.25)):
        x=delta(A,B,t,s);n=delta(A,C,t,s);exp=exact_unequal(t,s)
        phase.append({"theta_P":t,"theta_Q":s,"observed":x,"exact":exp,
            "commuting_control":n,"max_residual":max(abs(x-exp),abs(n))})
    ideal=8/27
    # Independent full-shot erasure of each of the four controlled phases,
    # with an erased trial returning random ancilla bit if not heralded.
    leak=.015;fringe=.94;flip=.012
    survival=(1-leak)**4
    v=survival*fringe*(1-2*flip)
    noisy_delta=ideal*v
    n=math.ceil(32*math.log(4/.05)/noisy_delta**2)
    shots_per_cond=n
    # block-correlated fringe visibility: mean v0=survival*fringe*(1-2flip)
    # varies in ±12% *multiplicatively* across blocks; alternate stimulus
    # within each block so the latent nuisance affects both conditions.
    reps=1000;blocks=20;perblock=math.ceil(n/blocks)
    null_deltas=[];signal_deltas=[]
    for j in range(reps):
        # Test a drift artifact: sequential designs sample the high-visibility
        # regime first, low-visibility later, even if BOTH are commuting.
        drift=.12
        xhi=v*(1+drift);xlo=v*(1-drift)
        N=blocks*perblock
        sequential_null=(2*rng.binomial(N,(1+xhi)/2)/N-1) -(
            2*rng.binomial(N,(1+xlo)/2)/N-1)
        null_deltas.append(sequential_null)
        # In paired scheme same drift inside block, variable by block.
        diffs=[]
        for b in range(blocks):
            vb=float(np.clip(v*(1+rng.normal(0,.12)),0,.999))
            plus=2*rng.binomial(perblock,(1+vb)/2)/perblock-1
            minus=2*rng.binomial(perblock,(1+vb*(1-ideal))/2)/perblock-1
            diffs.append(plus-minus)
        signal_deltas.append(float(np.mean(diffs)))
    threshold=noisy_delta/2
    # Supplement with exact paired-null sham distribution.
    shams=[]
    for _ in range(reps):
        diffs=[]
        for b in range(blocks):
            vb=float(np.clip(v*(1+rng.normal(0,.12)),0,.999))
            q0=2*rng.binomial(perblock,(1+vb)/2)/perblock-1
            q1=2*rng.binomial(perblock,(1+vb)/2)/perblock-1
            diffs.append(q0-q1)
        shams.append(float(np.mean(diffs)))
    checks={
      "unequal_phases_exact":max(x["max_residual"] for x in phase)<1e-12,
      "coherent_overrotation_not_equivalent_to_erasure":phase[4]["observed"]>0,
      "paired_condition_detection_over_95pc":np.mean(np.array(signal_deltas)>threshold)>.95,
      "paired_sham_false_alarm_below_5pc":np.mean(np.array(shams)>threshold)<.05,
      "sequential_unpaired_drift_inflates_shams":np.mean(np.array(null_deltas)>threshold)>.5
    }
    result={
      "schema":"w33.round4.optical_block_drift.v1",
      "exact_unequal_angle":"1-ReTr loop/9=(32/27)*sin(thetaP/2)^2*sin(thetaQ/2)^2 for noncommuting pair; commuting exact 0",
      "phase_sweep":phase,
      "synthetic_noise":{"per_control_gate_erasure":leak,
        "erasure_model":"state-independent loss/erasure mapped to unflagged random ancilla bit; four independent gates",
        "survival_four_gates":survival,"ancilla_fringe_visibility":fringe,
        "readout_bit_flip":flip,"effective_visibility":v,
        "expected_contrast":noisy_delta,
        "hoeffding_shots_per_condition":shots_per_cond,
        "blocks":blocks,"shots_per_block":perblock,
        "repetitions":reps,"common_mode_block_drift_std_fraction":.12,
        "unpaired_systematic_phase_drift_fraction":.12,
        "half_contrast_threshold":threshold},
      "simulated_results":{"sequential_null_false_alarm_rate":float(np.mean(np.array(null_deltas)>threshold)),
        "paired_signal_detection_rate":float(np.mean(np.array(signal_deltas)>threshold)),
        "paired_null_false_alarm_rate":float(np.mean(np.array(shams)>threshold)),
        "paired_signal_mean":float(np.mean(signal_deltas)),
        "paired_sham_mean":float(np.mean(shams))},
      "hardware_prerequisites":"Coherent ancilla-controlled projector phase on a 9-level target, CZ, F3, conditioned inverse, survival monitoring, randomized interleaved reference/sham; postselection must be calibrated.",
      "prior_art":"2026 Nature Photonics demonstrated heralded 4-dimensional photon-photon controlled phase-flip with measured process fidelity 0.71±0.01 to 0.85±0.01; NOT proof of this controlled two-qutrit projector echo. https://www.nature.com/articles/s41566-026-01846-x",
      "physics_limit":"Synthetic independent loss and block drift only; not measured process fidelity, detector side channels, coherent cross-talk, entanglement decoherence or a new TOE prediction.",
      "checks":{k:bool(x) for k,x in checks.items()},
      "all_checks_pass":bool(all(checks.values()))}
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"checks":result["checks"],"simulated":result["simulated_results"],
                      "shots":shots_per_cond},indent=2))
    assert result["all_checks_pass"]
    return result
if __name__=="__main__":simulate()
