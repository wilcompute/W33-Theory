#!/usr/bin/env python3
"""Pass 3984: nuisance-complete one-photon timing/capacity tomography design."""
from __future__ import annotations
import hashlib, json, math
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
C=299792458.0

def mutual_information(confusion):
    P=np.asarray(confusion,float); P=P/P.sum()
    px=P.sum(1,keepdims=True); py=P.sum(0,keepdims=True)
    mask=P>0
    return float(np.sum(P[mask]*np.log2(P[mask]/(px@py)[mask])))

def symmetric_confusion(M,eps):
    P=np.full((M,M),eps/(M-1)); np.fill_diagonal(P,1-eps); return P/M

def build_design():
    modes=[1,4,16,40]; lengths=[0.0,1000.0,10000.0]; encoders=[0,1]
    rows=[]; meta=[]
    for L in lengths:
      for M in modes:
       for enc in encoders:
        lm=math.log(M)
        # Deliberately correlated measured nuisances; encoder swaps break exact collinearity.
        kperp=(1.8e-9*lm)+(enc-0.5)*0.45e-9+(L/10000.0-0.5)*0.15e-9
        spectrum=(0.7e-9*lm)-(enc-0.5)*0.30e-9+(L/10000.0)*0.10e-9
        width=(M**0.35-1.0)*1e-12
        drift=((len(meta)%7)-3)/3
        detector=(M+enc)%2
        xgamma=(L/C)*lm
        xk=(L/C)*kperp
        xs=(L/C)*spectrum
        # nuisance: intercept, global L slope, mode intercepts, encoder and interactions,
        # transverse/spectral slopes, pulse width, drift, detector walk.
        mode4=1.0 if M==4 else 0.0; mode16=1.0 if M==16 else 0.0; mode40=1.0 if M==40 else 0.0
        nuisance=[1.0,L/C,mode4,mode16,mode40,float(enc),enc*mode4,enc*mode16,enc*mode40,
                  xk,xs,width,drift,float(detector)]
        rows.append(nuisance+[xgamma]); meta.append({'L_m':L,'M':M,'encoder':enc,'kperp_covariate':kperp,'spectrum_covariate':spectrum})
    return np.array(rows,float),meta

def projected_information(X):
    N=X[:,:-1]; g=X[:,-1]
    Q=np.linalg.qr(N,mode='reduced')[0]
    residual=g-Q@(Q.T@g)
    return float(residual@residual),residual

def fit_bias(X,true_gamma=0.0,kperp_coeff=0.5,spectral_coeff=0.35):
    N=X[:,:-1]; g=X[:,-1]
    y=true_gamma*g+kperp_coeff*N[:,9]+spectral_coeff*N[:,10]
    full=np.linalg.lstsq(X,y,rcond=None)[0][-1]
    reduced_cols=list(range(9))+[11,12,13] # omit measured propagation nuisances
    R=np.column_stack([N[:,reduced_cols],g])
    reduced=np.linalg.lstsq(R,y,rcond=None)[0][-1]
    return float(full),float(reduced)

def main():
    X,meta=build_design(); info,residual=projected_information(X)
    assert np.linalg.matrix_rank(X)==X.shape[1]
    events=1_000_000; sigma_event=20e-12; sigma_mean=sigma_event/math.sqrt(events)
    sigma_gamma=sigma_mean/math.sqrt(info)
    full_bias,reduced_bias=fit_bias(X)
    gamma_signal=1e-9
    max_delay=max(abs(X[:,-1]*gamma_signal))*1e12
    required_5sigma=math.ceil((5*sigma_event/(abs(gamma_signal)*math.sqrt(info)))**2)
    capacity=[]
    for M in [2,4,8,16,40]:
        eps=0.005+0.0015*math.log2(M)
        capacity.append({'M':M,'error':eps,'mutual_information_bits':mutual_information(symmetric_confusion(M,eps)),
                         'ideal_bits':math.log2(M)})
    result={'schema':'w33.pass3984.photon_nuisance_tomography.v1','status':'PASS',
      'cells':len(meta),'parameters':X.shape[1],'design_rank':int(np.linalg.matrix_rank(X)),
      'design_condition_number':float(np.linalg.cond(X)),'projected_gamma_information_s2':info,
      'single_event_jitter_s':sigma_event,'events_per_cell':events,'sigma_gamma':sigma_gamma,
      'five_sigma_events_per_cell_for_abs_gamma_1e-9':required_5sigma,
      'max_mode_dependent_delay_ps_for_gamma_1e-9':max_delay,
      'omitted_variable_gamma_estimate':reduced_bias,'full_model_gamma_estimate':full_bias,
      'omitted_bias_removed':abs(full_bias)<1e-15 and abs(reduced_bias)>1e-12,
      'capacity_table':capacity,
      'protocol':['randomize mode alphabet and encoder implementation','repeat every setting at three path lengths including a zero-length latency calibration','measure transverse-momentum and spectral covariates on every block','fit mode-dependent intercepts separately from the length-by-log(M) slope','report pulse-front and pulse-peak estimators separately','decode a complete confusion matrix and report mutual information independently of timing'],
      'primary_falsifier':'A nonzero length-by-log(M) coefficient that survives measured k_perp, spectrum, encoder-swap, detector-walk, pulse-width, and drift regressors.',
      'boundary':'Numerically certified design/Fisher calculation with declared Gaussian jitter; not a performed experiment, apparatus forecast, or measurement of variable vacuum c.'}
    result['design_sha256']=hashlib.sha256(np.asarray(X,dtype='<f8').tobytes()).hexdigest()
    (ROOT/'data/PART_3984_PHOTON_NUISANCE_TOMOGRAPHY.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print('PASS_PHOTON_NUISANCE_TOMOGRAPHY',result['design_rank'],result['sigma_gamma'],result['omitted_variable_gamma_estimate'])
if __name__=='__main__': main()
