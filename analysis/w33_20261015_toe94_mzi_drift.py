"""TOE94 Witting four-mode MZI drift and calibrated entanglement threshold.

For all 40 TOE93 meshes, replace every relative MZI phase by a
bounded synthetic deterministic drift. Reconstruct each Alice/Bob U4
and their 16x16 joint matching operator, compare its spectral norm
with the ideal 2-design operator. Bound every separable source under
trusted, setting-complete POVM calibration. No real hardware data.
"""
from __future__ import annotations
import json,math
import numpy as np
from scipy.stats import binom
from analysis.w33_20261015_toe90_vlasov_ququart_design import ROOT
from analysis.w33_20261015_toe93_mzi_bill import factor,H
from analysis.w33_20261015_toe92_optical_givens_mesh import decompose
from tools.bt1408_witting_contextual_communication_bridge import construct_witting_40_rays,find_tetrads
def perturbed(G,basis,index,delta,side):
    theta,l,r=factor(G)
    a=delta*((basis+2*index+side)%3+1)/3
    if side:a=-a
    t=theta+a
    rotation=np.diag([1,1j])@H@np.diag(np.exp(1j*np.array([t,-t])))@H@np.diag([1,-1j])
    M=np.diag(np.exp(1j*np.array(l)))@rotation@np.diag(np.exp(1j*np.array(r)))
    assert np.max(abs(M.conj().T@M-np.eye(2)))<1e-10
    return M
def measured(U,basis,delta,side):
    diag,steps=decompose(U)
    result=np.diag(np.diag(diag))
    for ix,(a,b,G) in reversed(list(enumerate(steps))):
        g=perturbed(G,basis,ix,delta,side)
        m=np.eye(4,dtype=complex);m[np.ix_([a,b],[a,b])]=g.conj().T
        result=m@result
    assert np.max(abs(result.conj().T@result-np.eye(4)))<1e-9
    return result
def witness(v,delta):
    R=np.array(construct_witting_40_rays(),complex)
    B=find_tetrads(list(R))
    phi=np.zeros(16,complex)
    for i in range(4):phi[5*i]=.5
    C=np.zeros((16,16),complex)
    for b,t in enumerate(B):
        U=R[list(t)].conj()
        A=measured(U,b,delta,0)
        S=measured(U,b,delta,1)
        for j in range(4):
            aa=np.outer(A[j].conj(),A[j])
            bb=np.outer(S[j],S[j].conj())
            C+=np.kron(aa,bb)/40
    ideal=(np.eye(16)+4*np.outer(phi,phi.conj()))/5
    delta_op=C-ideal
    err=float(np.max(abs(np.linalg.eigvalsh(delta_op))))
    assert np.max(abs(C-C.conj().T))<1e-10
    assert abs(err)<1
    # Isotropic two-ququart model rho(v), all bases trusted/calibrated.
    rho=v*np.outer(phi,phi.conj())+(1-v)*np.eye(16)/16
    obs=float(np.trace(rho@C).real)
    sep_ceiling=.4+err
    # A bounded unmodeled false-click contamination p_b may yield
    # adversarially favorable matching in any of 4 labels (max 1).
    p_bad=.001
    robust=(1-p_bad)*sep_ceiling+p_bad
    observed_with_uniform_random_bad=(1-p_bad)*obs+p_bad*.25
    return {'phase_drift_max_radians':delta,
      'max_joint_operator_spectral_deviation':round(err,12),
      'trusted_no_background_separable_upper':round(sep_ceiling,12),
      'unmodeled_adversarial_click_fraction_upper':p_bad,
      'adversarial_click_contamination_separable_upper':round(robust,12),
      'synthetic_isotropic_visibility':v,
      'synthetic_raw_match_probability':round(obs,12),
      'synthetic_uniform_noise_click_match':round(observed_with_uniform_random_bad,12),
      'violation_after_calibrated_adversarial_click_bound':observed_with_uniform_random_bad>robust}
def certificate():
    rows=[witness(.95,d) for d in (0.,.001,.002,.005,.01)]
    assert rows[0]['max_joint_operator_spectral_deviation']==0.
    assert all(x['max_joint_operator_spectral_deviation']>=0 for x in rows)
    return {'scope':'All 40 four-mode MZI basis analyzers with bounded synthetic per-coupler phase drifts on two arms; calibrated 16x16 POVM operator inequality. No measurement of real devices or detector side-channel characterization.',
      'sampling_protocol':'Uniform random setting among 40, no basis/outcome-dependent postselection. Measure all precommitted heralds and include losses as failure when evaluating event-ready witness.',
      'rigorous_trusted_calibration_inequality':'Tr rho_sep C_delta <= 2/5 + ||C_delta-C_ideal||op, valid for all separable two-ququart states and fully trusted calibrated POVM. Under arbitrary click contamination <=b, upper is (1-b)*(2/5+norm)+b.',
      'drift_recipe':'For setting b, Givens step j and arm s, internal half-phase shifted by +/- delta*[1+((b+2j+s)%3)]/3. The model is deterministic not randomized calibration.',
      'rows':rows}
if __name__=='__main__':
 d=certificate()
 (ROOT/'data/w33_20261015_toe94_mzi_drift.json').write_text(json.dumps(d,sort_keys=True,indent=2)+'\n')
 print('DRIFT94',[(x['phase_drift_max_radians'],x['trusted_no_background_separable_upper'],x['violation_after_calibrated_adversarial_click_bound']) for x in d['rows']],flush=True)
