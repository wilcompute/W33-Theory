"""Nonabelian 2-loop character calibration under common phase drift,
mode-dependent detection and finite Bernoulli statistics.
"""
from pathlib import Path
import json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/toe_20261119_SU3_reference_calibration_gauge_frame_falsifier.json'
O=np.exp(2j*np.pi/3)
F=np.array([[O**(a*b) for b in range(3)] for a in range(3)])/np.sqrt(3)

def Kloop():
    A=np.diag(np.exp(1j*np.array([.37,1.1,-1.47])))
    B0=np.diag(np.exp(1j*np.array([.41,.91,-1.32])))
    B=F@B0@F.conj().T
    return A@B@A.conj().T@B.conj().T

def compare(gamma=.4,v=.8,N=10000,M=3000,reps=5000,drift=.0):
    # 2p(theta)-1 = (v/3) Re[e^{-i(theta+gamma)}t].
    # Reference t=3: z_ref=(2pref0-1)+i(2pref90-1)=v e^{-i gamma}
    # Target: z_t=3[(2pt0-1)+i(2pt90-1)]=v e^{-i(gamma+drift)}t.
    t=np.trace(Kloop())
    rng=np.random.default_rng(20261119)
    def probabilities(t,phase):
        z=v*np.exp(-1j*phase)*t/3
        return (.5+.5*z.real,.5+.5*z.imag)
    pref=probabilities(3,gamma)
    pt=probabilities(t,gamma+drift)
    assert all(0<p<1 for p in pref+pt)
    pr0=rng.binomial(M,pref[0],size=reps)/M
    pr1=rng.binomial(M,pref[1],size=reps)/M
    ps0=rng.binomial(N,pt[0],size=reps)/N
    ps1=rng.binomial(N,pt[1],size=reps)/N
    ref=(2*pr0-1)+1j*(2*pr1-1)
    target=3*((2*ps0-1)+1j*(2*ps1-1))
    est=target/ref
    rms=float(np.sqrt(np.mean(abs(est-t)**2)))
    firstorder_mse=(18/N+2*abs(t)**2/M)/v**2
    systematic=abs(t)*(2*abs(math.sin(drift/2)))
    delta=.01
    log=math.log(8/delta)
    noise_tar=6*math.sqrt(2)*math.sqrt(log/(2*N))
    noise_ref=2*math.sqrt(2)*math.sqrt(log/(2*M))
    bound=(noise_tar+abs(t)*noise_ref)/(v-noise_ref)
    if drift==0:
        assert float(np.mean(abs(est-t)<=bound))>.98
    return {'common_reference_phase':gamma,'target_extra_drift':drift,
        'trace_true':[float(t.real),float(t.imag)],
        'calibration_and_target_trials_per_phase':[M,N],
        'simulation_repetitions':reps,'complex_RMSE':rms,
        'firstorder_RMSE_prediction':float(np.sqrt(firstorder_mse)),
        'differential_drift_asymptotic_bias':float(systematic),
        'conservative_99pct_complex_error_bound_no_differential_drift':bound,
        'coverage_if_valid_common_phase':float(np.mean(abs(est-t)<=bound))}

def color_detector():
    K=Kloop();t=np.trace(K)
    eta=np.diag([.4,1.,1.6]);eta=eta.astype(complex)
    rng=np.random.default_rng(251119)
    distort=[];identity=[];errors=[]
    for i in range(64):
        Z=rng.normal(size=(3,3))+1j*rng.normal(size=(3,3));U,_=np.linalg.qr(Z)
        U/=np.linalg.det(U)**(1/3)
        rotated=U@K@U.conj().T
        distorted=3*np.trace(eta@rotated)/np.trace(eta)
        distort.append(distorted)
        identity.append(3*np.trace(eta@np.eye(3))/np.trace(eta))
        errors.append(float(abs(distorted-t)))
    assert max(errors)>.05
    assert max(abs(x-3) for x in identity)<1e-12
    assert max(abs(np.trace(K)-np.trace(U@K@U.conj().T)) for U in [np.eye(3)])<1e-12
    return {'gauge_rotations':64,'trace_true':[float(t.real),float(t.imag)],
      'mode_efficiencies':[.4,1,1.6],
      'max_color_biased_frame_trace_error':max(errors),
      'mean_color_biased_frame_trace_error':float(np.mean(errors)),
      'identity_reference_trace_all_frames':3.,
      'theorem':'A fixed lab loss matrix eta!=cI yields Tr(eta U K U†), not invariant under simultaneous local gauge-frame conjugation of K. Identity-loop calibration sees Tr eta and cannot remove orientation-dependent bias.',
      'required_hardware':'color/mode independent detection OR matched transport and tomography of eta with local gauge frames.'}

def run():
    no_drift=compare(drift=0)
    drift=compare(drift=.2)
    biased=color_detector()
    out={'status':'PASS_SU3_PHASE_IDENTIFIABILITY_AND_COLOR_LOSS_NO_GO',
       'reference_compensated':no_drift,'differential_phase_drift':drift,
       'color_mode_gauge_bias':biased,
       'analytical_identifiability':'z_target=v e^{-i delta_target} Tr K and z_identity=v e^{-i delta_ref}; ratio=exp[-i(delta_target-delta_ref)] Tr K',
       'loss_caution':'Bernoulli iid accepted detection model only, not photonic implementation or quantum error correction.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(out,indent=2)+'\n')
    print('SU3 RMSE',no_drift['complex_RMSE'],drift['complex_RMSE'],'COLOR BIAS MAX',biased['max_color_biased_frame_trace_error'])
    return out
if __name__=='__main__':run()
