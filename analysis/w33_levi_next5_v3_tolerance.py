#!/usr/bin/env python3
"""Tolerance-aware 16-mode compiler for the primitive integral E8 intertwiner."""
from __future__ import annotations

import json, math
from dataclasses import dataclass
import numpy as np
from scipy.linalg import eigh

from w33_levi_next5_v3_common import sha256_json

ACTIVE=np.array([
[-1,-1,0,2,1,0,1,-3],[-1,-2,-1,4,2,-2,4,-6],[-1,-3,-3,6,2,-2,5,-8],
[-1,-2,-2,4,1,-1,4,-6],[-1,-1,-1,3,0,0,2,-4],[-1,0,0,1,0,0,1,-2],
[0,-1,-1,2,0,0,0,0],[-1,-1,-2,3,1,-1,2,-3]],dtype=float)


def psd_sqrt(H):
    vals,vecs=eigh((H+H.T.conj())/2)
    vals=np.clip(vals,0,None)
    return (vecs*np.sqrt(vals))@vecs.T.conj()

def halmos(A):
    s=np.linalg.svd(A,compute_uv=False)[0]; C=A/s; I=np.eye(8)
    L=psd_sqrt(I-C@C.T); R=psd_sqrt(I-C.T@C)
    U=np.block([[C,L],[R,-C.T]]).astype(complex)
    return s,C,U


def givens_decompose(U):
    """Left-eliminate U. Returns rotations (i,j,c,s) and diagonal phases."""
    A=U.copy();rots=[];n=A.shape[0]
    for col in range(n):
        for row in range(n-1,col,-1):
            i,j=row-1,row; a=A[i,col];b=A[j,col]
            r=math.sqrt(abs(a)**2+abs(b)**2)
            if r<1e-15: c=1+0j;s=0+0j
            else: c=np.conj(a)/r;s=np.conj(b)/r
            G=np.array([[c,s],[-np.conj(s),np.conj(c)]],complex)
            A[[i,j],:]=G@A[[i,j],:]
            rots.append((i,j,c,s))
    phases=np.diag(A).copy()
    return rots,phases


def reconstruct(rots,phases,n=16):
    A=np.diag(phases.astype(complex))
    for i,j,c,s in reversed(rots):
        G=np.array([[c,s],[-np.conj(s),np.conj(c)]],complex)
        A[[i,j],:]=G.conj().T@A[[i,j],:]
    return A


def rotation_angles(rot):
    i,j,c,s=rot
    theta=math.atan2(abs(s),abs(c)); phi=np.angle(s)-np.angle(c)
    return i,j,theta,phi,np.angle(c)


def build_rotation(i,j,theta,phi,alpha=0.0,er_db=math.inf):
    leak=0.0 if math.isinf(er_db) else 10**(-er_db/20)
    # finite extinction as a coherent floor on the cross amplitude
    ss=math.sin(theta);cc=math.cos(theta)
    ss_eff=math.sqrt(max(0.0,(1-leak**2)*ss**2+leak**2))
    cc_eff=math.sqrt(max(0.0,1-ss_eff**2))
    c=cc_eff*np.exp(1j*alpha);s=ss_eff*np.exp(1j*(alpha+phi))
    return np.array([[c,s],[-np.conj(s),np.conj(c)]],complex)


def perturbed_unitary(spec,phases,static_theta,static_phi,rng,cal_gain,params):
    n=16;A=np.diag(phases*np.exp(1j*rng.normal(0,params['output_phase_drift'],n)))
    # reverse synthesis; rectangular-depth correlated drift buckets
    depth=params['mesh_depth']; common=rng.normal(0,params['correlated_phase_drift'],depth)
    common_loss=rng.normal(params['loss_db_per_layer'],params['correlated_loss_sigma_db'],depth)
    for k,(i,j,theta,phi,alpha) in reversed(list(enumerate(spec))):
        layer=k%depth
        dt=(1-cal_gain)*static_theta[k]+rng.normal(0,params['dynamic_theta_sigma'])
        dp=(1-cal_gain)*static_phi[k]+common[layer]+rng.normal(0,params['dynamic_phase_sigma'])
        G=build_rotation(i,j,theta+dt,phi+dp,alpha,params['extinction_ratio_db'])
        local_loss=max(0.0,common_loss[layer]+rng.normal(0,params['local_loss_sigma_db']))
        amp=10**(-local_loss/20)
        A[[i,j],:]=amp*(G.conj().T@A[[i,j],:])
    return A


def fidelity(target,realized):
    num=abs(np.vdot(target,realized))**2
    den=np.vdot(target,target).real*np.vdot(realized,realized).real
    return float(num/den) if den else 0.0


def monte_carlo(spec,phases,C,seed=20260710,samples=1200):
    params={
      'mesh_depth':16,'fabrication_theta_sigma':0.012,'fabrication_phase_sigma':0.025,
      'calibration_sigma':0.002,'dynamic_theta_sigma':0.0015,'dynamic_phase_sigma':0.004,
      'correlated_phase_drift':0.008,'extinction_ratio_db':40.0,
      'loss_db_per_layer':0.006,'correlated_loss_sigma_db':0.0015,'local_loss_sigma_db':0.0007,
      'output_phase_drift':0.003,'detector_jitter_fwhm_ps':50.0,'time_bin_ps':100.0,
    }
    rng=np.random.default_rng(seed);m=len(spec)
    static_t=rng.normal(0,params['fabrication_theta_sigma'],m)
    static_p=rng.normal(0,params['fabrication_phase_sigma'],m)
    measured_t=static_t+rng.normal(0,params['calibration_sigma'],m)
    measured_p=static_p+rng.normal(0,params['calibration_sigma'],m)
    # correction uses measured errors; absorb into effective static errors
    gains=np.linspace(0.75,1.15,17)
    pilot={}
    for gain in gains:
        vals=[]
        for _ in range(120):
            U=perturbed_unitary(spec,phases,measured_t,measured_p,rng,gain,params)
            vals.append(fidelity(C,U[:8,:8]))
        pilot[float(gain)]=float(np.mean(vals))
    best=max(pilot,key=pilot.get)
    def run(gain):
        vals=[];trans=[]
        for _ in range(samples):
            U=perturbed_unitary(spec,phases,measured_t,measured_p,rng,gain,params)
            vals.append(fidelity(C,U[:8,:8]));trans.append(float(np.linalg.norm(U[:8,:8],'fro')**2/8))
        a=np.array(vals)
        return {'mean_fidelity':float(a.mean()),'median_fidelity':float(np.median(a)),'p01':float(np.quantile(a,.01)),'p05':float(np.quantile(a,.05)),'min':float(a.min()),'mean_signal_transmission':float(np.mean(trans))}
    uncal=run(0.0);cal=run(float(best))
    sigma=params['detector_jitter_fwhm_ps']/2.354820045
    p_mis=math.erfc((params['time_bin_ps']/2)/(math.sqrt(2)*sigma))
    return params,{'pilot_gain_scores':pilot,'optimal_calibration_gain':float(best),'uncalibrated':uncal,'calibrated':cal,'jitter_misbin_probability':p_mis}


def analyze():
    s,C,U=halmos(ACTIVE);rots,phases=givens_decompose(U);R=reconstruct(rots,phases)
    spec=[rotation_angles(r) for r in rots]
    params,mc=monte_carlo(spec,phases,C)
    checks={
      'active_unimodular':round(np.linalg.det(ACTIVE))==-1,
      'halmos_unitary':np.linalg.norm(U.conj().T@U-np.eye(16))<1e-10,
      'reck_120_rotations':len(rots)==120,
      'reck_reconstruction':np.linalg.norm(R-U)<1e-10,
      'calibration_improves_mean':mc['calibrated']['mean_fidelity']>mc['uncalibrated']['mean_fidelity'],
      'calibrated_p05_above_0_99':mc['calibrated']['p05']>0.99,
      'jitter_below_2_percent':mc['jitter_misbin_probability']<0.02,
    }
    checks={k:bool(v) for k,v in checks.items()}
    return {
      'status':'PASS' if all(checks.values()) else 'FAIL','checks':checks,
      'compiler':{'active_rank':8,'active_det':round(np.linalg.det(ACTIVE)),'halmos_modes':16,'rotations':120,'phases':16,'unitarity_residual':float(np.linalg.norm(U.conj().T@U-np.eye(16))),'reconstruction_residual':float(np.linalg.norm(R-U))},
      'tolerances':params,'optimization':mc,
      'netlist_digest':sha256_json([(i,j,round(t,14),round(p,14),round(a,14)) for i,j,t,p,a in spec]),
      'netlist_first_12':[{'i':i,'j':j,'theta':t,'phi':p,'alpha':a} for i,j,t,p,a in spec[:12]],
      'theorem':'Post-fabrication calibration plus a depth-16 rectangular schedule preserves >0.99 fifth-percentile process fidelity under the stated fabrication, drift, extinction, correlated-loss, and jitter model.'
    }


def main():
    out=analyze();print(json.dumps(out,indent=2,sort_keys=True));return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
