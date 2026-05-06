#!/usr/bin/env python3
"""PART CCCXLVI -- Profile Likelihood / Model Comparison Compiler.

Builds directly on CCCXLV.  A one-sector response packet may be fit by:

M0: one common scale only,                    X_i = X + noise_i
M1: one common scale plus nuisance template,  X_i = X + theta b_i + noise_i
M2: broken/free channel model,                X_i = alpha_i + noise_i

For fixed covariance C, the profiled Gaussian log-likelihood differs by chi^2.
We report chi^2, dof, AIC, BIC, and likelihood-ratio improvements.  Synthetic
packets verify: clean prefers M0 by parsimony, coherent systematic prefers M1,
and off-template broken data is not saved by M1.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Any, Dict, List
ROOT = Path(__file__).resolve().parents[1]
Q=3; K=12; V=40
PHI3=Q*Q+Q+1; PHI6=Q*Q-Q+1
B=2*V-PHI3; A0=(V//2)*PHI6; DELTA=B*B+4*A0; M2_DIMLESS=DELTA/4.0
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
DEFAULT_TAU=0.001; DEFAULT_T=0.01; DEFAULT_S=100.0; DEFAULT_P=2

def ok(name, condition, value=None): return {"name":name,"passed":bool(condition),"value":value}
def channels_from_scale(scale,tau=DEFAULT_TAU,t=DEFAULT_T,s=DEFAULT_S,p=DEFAULT_P):
    r=math.sqrt(scale)
    return {"mass":r,"gap":2*r,"heat_trace":2*math.exp(-scale*tau),"spinor_trace":2*math.cosh(r*t),"resolvent_trace":2*s/(s*s-scale),"zeta":2/(scale**p),"samples":{"tau":tau,"t":t,"s":s,"p":p}}
def scale_from_channel(name,value,samples):
    tau=samples['tau']; t=samples['t']; s=samples['s']; p=samples['p']
    if name=='mass': return value*value
    if name=='gap': return (value/2)**2
    if name=='heat_trace': return -math.log(value/2)/tau
    if name=='spinor_trace': return (math.acosh(value/2)/t)**2
    if name=='resolvent_trace': return s*s-2*s/value
    if name=='zeta': return (2/value)**(1/p)
    raise ValueError(name)
def derivative(name,value,samples):
    tau=samples['tau']; t=samples['t']; s=samples['s']; p=samples['p']
    if name=='mass': return 2*value
    if name=='gap': return value/2
    if name=='heat_trace': return -1/(tau*value)
    if name=='spinor_trace':
        u=value/2; return math.acosh(u)/(t*t*math.sqrt(u*u-1))
    if name=='resolvent_trace': return 2*s/(value*value)
    if name=='zeta':
        x=scale_from_channel(name,value,samples); return -x/(p*value)
    raise ValueError(name)
def values(packet): return [scale_from_channel(n,packet[n],packet['samples']) for n in CHANNELS]
def jac(packet): return [derivative(n,packet[n],packet['samples']) for n in CHANNELS]
def sigmas(packet,rel=1e-6): return [abs(packet[n])*rel for n in CHANNELS]
def cov_y(sig,rho=0.15): return [[(1 if i==j else rho)*sig[i]*sig[j] for j in range(len(sig))] for i in range(len(sig))]
def propagate(cov,der): return [[der[i]*cov[i][j]*der[j] for j in range(len(der))] for i in range(len(der))]
def inv(mat):
    n=len(mat); aug=[row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(mat)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(aug[r][c])); aug[c],aug[p]=aug[p],aug[c]
        if abs(aug[c][c])<1e-30: raise ValueError('singular')
        sc=aug[c][c]; aug[c]=[x/sc for x in aug[c]]
        for r in range(n):
            if r==c: continue
            f=aug[r][c]; aug[r]=[aug[r][k]-f*aug[c][k] for k in range(2*n)]
    return [row[n:] for row in aug]
def T(m): return [list(row) for row in zip(*m)]
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,v): return [sum(a[i][j]*v[j] for j in range(len(v))) for i in range(len(a))]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def design(cols): return [[col[i] for col in cols] for i in range(len(cols[0]))]
def fit_gls(x,C,cols):
    A=design(cols); At=T(A); Ci=inv(C); N=mm(mm(At,Ci),A); Ni=inv(N); rhs=mv(mm(At,Ci),x); beta=mv(Ni,rhs); yhat=mv(A,beta); res=[xi-yi for xi,yi in zip(x,yhat)]; chi2=dot(res,mv(Ci,res)); n=len(x); k=len(cols); dof=n-k
    return {"k":k,"beta":beta,"chi_square":chi2,"degrees_of_freedom":dof,"reduced_chi_square":chi2/dof if dof else float('nan'),"aic":chi2+2*k,"bic":chi2+k*math.log(n),"residuals":res}
def template(): return [0,0,1,-0.5,0.75,-0.25]
def compare_models(x,C):
    n=len(x); one=[1.0]*n; eye=[[1.0 if i==j else 0.0 for i in range(n)] for j in range(n)]
    models={"M0_common_scale":fit_gls(x,C,[one]),"M1_scale_plus_nuisance":fit_gls(x,C,[one,template()]),"M2_free_channels":fit_gls(x,C,eye)}
    best_aic=min(models,key=lambda m:models[m]['aic']); best_bic=min(models,key=lambda m:models[m]['bic'])
    models['likelihood_ratio_M0_to_M1']={"delta_chi_square":models['M0_common_scale']['chi_square']-models['M1_scale_plus_nuisance']['chi_square'],"delta_dof":1}
    return {"models":models,"best_aic":best_aic,"best_bic":best_bic}
def synthetic_x(scale,theta=0.0,bad=0.0):
    b=template(); x=[scale+theta*b[i] for i in range(len(b))]; x[3]+=bad; return x
def build_results():
    checks=[]; scale=(7/3)**2*M2_DIMLESS; packet=channels_from_scale(scale); C=propagate(cov_y(sigmas(packet),rho=0.15),jac(packet))
    clean=compare_models(synthetic_x(scale,0),C); systematic=compare_models(synthetic_x(scale,0.02),C); bad=compare_models(synthetic_x(scale,0.02,bad=1.0),C)
    checks.append(ok('dimensionless W33 M2=5049/4',abs(M2_DIMLESS-5049/4)<1e-15,M2_DIMLESS))
    checks.append(ok('clean BIC prefers common-scale model',clean['best_bic']=='M0_common_scale',clean['best_bic']))
    checks.append(ok('systematic BIC prefers nuisance model',systematic['best_bic']=='M1_scale_plus_nuisance',systematic['best_bic']))
    checks.append(ok('systematic nuisance LR improves chi-square',systematic['models']['likelihood_ratio_M0_to_M1']['delta_chi_square']>10,systematic['models']['likelihood_ratio_M0_to_M1']))
    checks.append(ok('systematic nuisance fit recovers theta',abs(systematic['models']['M1_scale_plus_nuisance']['beta'][1]-0.02)<1e-8,systematic['models']['M1_scale_plus_nuisance']['beta']))
    checks.append(ok('bad data not accepted by nuisance model',bad['models']['M1_scale_plus_nuisance']['reduced_chi_square']>3,bad['models']['M1_scale_plus_nuisance']['reduced_chi_square']))
    checks.append(ok('bad AIC falls to free-channel broken model',bad['best_aic']=='M2_free_channels',bad['best_aic']))
    checks.append(ok('free-channel model has zero residual chi-square',abs(bad['models']['M2_free_channels']['chi_square'])<1e-8,bad['models']['M2_free_channels']['chi_square']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXLVI","title":"Profile Likelihood / Model Comparison Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"true_scale":scale,"model_definitions":{"M0":"X_i=X+noise_i","M1":"X_i=X+theta b_i+noise_i","M2":"X_i=alpha_i+noise_i (broken/free-channel model)"},"criteria":{"aic":"chi2+2k","bic":"chi2+k log N","lr":"Delta chi2 between nested models"},"clean_case":clean,"systematic_case":systematic,"bad_case":bad,"architecture_upgrade":"CCCXLV added nuisance templates. CCCXLVI profiles the nuisance model and compares common-scale, nuisance, and broken/free-channel alternatives by chi-square, AIC, BIC, and likelihood-ratio improvements.","theorem":"The one-sector W33 response model can be compared as nested Gaussian GLS models. A coherent modeled systematic should select the nuisance model over the no-nuisance model, while off-template residuals should force rejection or selection of the broken/free-channel alternative.","honesty_boundary":"The likelihoods here use synthetic covariance and Gaussian residual assumptions. Real use requires experimentally justified covariance, priors, and nuisance templates.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXLVI_profile_likelihood_model_comparison_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
