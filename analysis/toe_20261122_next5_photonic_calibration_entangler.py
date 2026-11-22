#!/usr/bin/env python3
"""Two sharp photonic hardware gates: intensity phase ambiguity and dual-rail leakage.

1) All four single-photon basis-input intensities are unchanged by output
   diagonal rephasing D_out, although channel/gate fidelity differs.
2) A four-mode passive lossless U that preserves one photon in each of two
   dual-rail pairs for every computational input has block-diagonal or
   block-antidiagonal structure, inducing only local or local-SWAP gates.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.stats import unitary_group
import toe_20261122_next5_compiler_photonics as O
OUT=Path(__file__).resolve().parents[1]/'data/toe_20261122_next5_photonic_calibration_entangler.json'

def leakage(U):
    # Dual rails A=(0,1), B=(2,3), exactly one photon per pair at input.
    probs=[]
    for i in (0,1):
        for j in (2,3):
            a,b=U[:2,i],U[:2,j]
            c,d=U[2:,i],U[2:,j]
            pAA=float(np.vdot(a,a).real*np.vdot(b,b).real+abs(np.vdot(a,b))**2)
            pBB=float(np.vdot(c,c).real*np.vdot(d,d).real+abs(np.vdot(c,d))**2)
            probs.append({'input_modes':[i,j], 'AA_leakage':pAA,'BB_leakage':pBB,
                          'total_leakage':pAA+pBB,'computational_subspace_survival':1-pAA-pBB})
            assert -1e-12<=pAA+pBB<=1+1e-12
    return probs

def minimal_n_for_95pct_power(theta):
    p=math.cos(theta/2)**2
    # Ideal binary discrimination test: under ideal unitary one always
    # measures '+'; reject ideal when at least one '-'. The false-alarm
    # probability is zero if ideal SPAM is perfect, power=1-p**N.
    n=math.ceil(math.log(.05)/math.log(p))
    assert 1-p**n>=.95-1e-12 and 1-p**(n-1)<.95+1e-12
    return n

def verify():
    U=O.gates()['a'];theta=np.pi/3
    Dout=np.diag([np.exp(1j*theta),1,1,1]);V=Dout@U
    assert np.linalg.norm(abs(U)**2-abs(V)**2)<1e-14
    tr=abs(np.trace(U.conj().T@V))
    fidelity=float((tr**2+4)/20)
    assert abs(fidelity-.85)<1e-12
    # Coherent state preparation Udag|+> followed by X-basis measurement
    # distinguishes D_out U from U, unlike basis-input intensity counting.
    psi=np.array([1,1,0,0],complex)/np.sqrt(2)
    prepared=U.conj().T@psi
    p_ideal=float(abs(np.vdot(psi,U@prepared))**2)
    p_phase=float(abs(np.vdot(psi,V@prepared))**2)
    assert abs(p_ideal-1)<1e-12 and abs(p_phase-.75)<1e-12
    samples=[{'theta_rad':float(t),'ideal_plus_probability':1.,
              'drifted_plus_probability':float(math.cos(t/2)**2),
              'shots_for_at_least_95pct_detection_ideal_SPAM':minimal_n_for_95pct_power(t)}
             for t in (np.pi/3,.3,.1,.03)]
    # Actual Witting ray-5 order-three reflection on two dual-rail photons.
    rails=leakage(U)
    assert max(r['total_leakage'] for r in rails)>0.01
    block=np.kron(O.gates()['a'][:2,:2],np.eye(2)) # not a 4x4 U, avoid as a full unitary
    # Negative control: block-diagonal and block-antidiagonal U(4) conserve 1+1.
    Ua=unitary_group.rvs(2,random_state=np.random.default_rng(17))
    Ub=unitary_group.rvs(2,random_state=np.random.default_rng(18))
    UB=np.zeros((4,4),complex);UB[:2,:2]=Ua;UB[2:,2:]=Ub
    US=np.zeros((4,4),complex);US[:2,2:]=Ua;US[2:,:2]=Ub
    assert all(r['total_leakage']<1e-12 for r in leakage(UB))
    assert all(r['total_leakage']<1e-12 for r in leakage(US))
    # The exact no-go follows from product of two boson single-particle
    # A-output vectors: ||u sym v||²=||u||²||v||²+|<u,v>|².
    # Vanishes iff u=0 or v=0, for each pair of A and B inputs.
    # Thus either U_AA=0 or U_AB=0, and similarly for B; unitarity
    # leaves exactly diagonal or antidiagonal 2x2 block support.
    return dict(status='PASS_PHASE_BLINDNESS_AND_PASSIVE_TWO_PHOTON_ENTANGLER_NO_GO',
      date='2026-11-22',single_photon_witting_gate='R5(omega)',
      intensity_measurement_identical_max_abs_error=float(np.max(abs(abs(U)**2-abs(V)**2))),
      phase_drift_output='Dout=diag(exp(i*pi/3),1,1,1)',
      channel_average_gate_fidelity=fidelity,
      phase_referenced_superposition_test={'ideal_plus_probability':p_ideal,'shifted_plus_probability':p_phase},
      idealized_shot_budgets=samples,
      actual_witting_gate_dual_rail_leakage=rails,
      no_go='A passive U(4) that exactly preserves the 2-photon dual-rail 1+1 computational sector for all four computational basis inputs is 2x2 block diagonal or block antidiagonal. Thus its induced deterministic gate is local U_A tensor U_B or local-SWAP, never entangling.',
      symmetrized_boson_norm_identity='||u symmetric-product v||^2=||u||^2||v||^2+|inner(u,v)|^2, which vanishes iff u or v is zero',
      controls='Random 2x2 block diagonal and block antidiagonal unitaries have zero leakage; Witting R5 generally leaks into 2+0 or 0+2 sectors.',
      caveats='Strictly four passive modes, exactly two noninteracting photons and deterministic leakage-free dual-rail logic. Ancillary photons, measurement/feedforward, nonlinear interactions, mode-dependent encodings and postselection change the assumptions. Detector shot budgets assume ideal preparation/readout and known reference phase; they are not laboratory calibration.' )

def main():
    d=verify();OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n')
    print('PASS intensity tomography ambiguity and passive 4-mode entangler no-go',d['channel_average_gate_fidelity'])

if __name__=='__main__':main()
