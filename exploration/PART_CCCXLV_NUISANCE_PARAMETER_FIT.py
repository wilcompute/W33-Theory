#!/usr/bin/env python3
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Any, Dict, List
ROOT = Path(__file__).resolve().parents[1]
Q=3; K=12; V=40
PHI3=Q*Q+Q+1; PHI4=Q*Q+1; PHI6=Q*Q-Q+1
B=2*V-PHI3; A_PARAM=(V//2)*PHI6; DELTA=B*B+4*A_PARAM
M2_DIMLESS=DELTA/4.0
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
DEFAULT_TAU=0.001; DEFAULT_T=0.01; DEFAULT_S=100.0; DEFAULT_P=2

def ok(name, condition, value=None): return {"name":name,"passed":bool(condition),"value":value}
def channels_from_scale(scale, tau=DEFAULT_TAU, t=DEFAULT_T, s=DEFAULT_S, p=DEFAULT_P):
    root=math.sqrt(scale)
    return {"mass":root,"gap":2*root,"heat_trace":2*math.exp(-scale*tau),"spinor_trace":2*math.cosh(root*t),"resolvent_trace":2*s/(s*s-scale),"zeta":2/(scale**p),"samples":{"tau":tau,"t":t,"s":s,"p":p}}
def scale_from_channel(name,value,samples):
    tau=samples['tau']; t=samples['t']; s=samples['s']; p=samples['p']
    if name=='mass': return value*value
    if name=='gap': return (value/2)**2
    if name=='heat_trace': return -math.log(value/2)/tau
    if name=='spinor_trace': return (math.acosh(value/2)/t)**2
    if name=='resolvent_trace': return s*s - 2*s/value
    if name=='zeta': return (2/value)**(1/p)
    raise ValueError(name)
def derivative_scale_wrt_channel(name,value,samples):
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
def channel_scale_vector(packet): return [scale_from_channel(n,packet[n],packet['samples']) for n in CHANNELS]
def jacobian(packet): return [derivative_scale_wrt_channel(n,packet[n],packet['samples']) for n in CHANNELS]
def default_sigmas(packet, rel=1e-6): return [abs(packet[n])*rel for n in CHANNELS]
def make_value_covariance(sigmas,rho=0.0):
    n=len(sigmas); return [[(1 if i==j else rho)*sigmas[i]*sigmas[j] for j in range(n)] for i in range(n)]
def propagate_covariance(value_cov, derivs):
    n=len(derivs); return [[derivs[i]*value_cov[i][j]*derivs[j] for j in range(n)] for i in range(n)]
def invert_matrix(mat):
    n=len(mat); aug=[row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(mat)]
    for col in range(n):
        pivot=max(range(col,n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-30: raise ValueError('singular matrix')
        aug[col],aug[pivot]=aug[pivot],aug[col]
        scale=aug[col][col]; aug[col]=[x/scale for x in aug[col]]
        for r in range(n):
            if r==col: continue
            factor=aug[r][col]; aug[r]=[aug[r][c]-factor*aug[col][c] for c in range(2*n)]
    return [row[n:] for row in aug]
def transpose(mat): return [list(row) for row in zip(*mat)]
def matmul(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def matvec(a,v): return [sum(a[i][j]*v[j] for j in range(len(v))) for i in range(len(a))]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def max_abs_matrix_diff(a,b): return max(abs(a[i][j]-b[i][j]) for i in range(len(a)) for j in range(len(a[0])))
def design_matrix(templates):
    n=len(CHANNELS); columns=[[1.0]*n]+templates; return [[col[i] for col in columns] for i in range(n)]
def nuisance_template(): return [0.0,0.0,1.0,-0.5,0.75,-0.25]
def gls_fit(x,cov,templates):
    A=design_matrix(templates); At=transpose(A); invC=invert_matrix(cov); normal=matmul(matmul(At,invC),A); normal_inv=invert_matrix(normal)
    rhs=matvec(matmul(At,invC),x); beta=matvec(normal_inv,rhs); fitted=matvec(A,beta); residuals=[xi-fi for xi,fi in zip(x,fitted)]
    chi2=dot(residuals,matvec(invC,residuals)); dof=len(x)-len(beta)
    return {"beta":beta,"cov_beta":normal_inv,"fitted":fitted,"residuals":residuals,"chi_square":chi2,"degrees_of_freedom":dof,"reduced_chi_square":chi2/dof if dof>0 else float('nan'),"passes_reduced_chi_square_lt_3":(chi2/dof)<3 if dof>0 else False}
def fit_packet(packet,value_cov,templates):
    derivs=jacobian(packet); scale_cov=propagate_covariance(value_cov,derivs); x=channel_scale_vector(packet)
    return {"channels":CHANNELS,"scale_values":x,"scale_covariance":scale_cov,"templates":templates,"fit":gls_fit(x,scale_cov,templates)}
def build_synthetic_scale_fit(true_scale,cov,theta,bad_extra=0.0):
    template=nuisance_template(); base=[true_scale]*len(CHANNELS); x=[base[i]+theta*template[i]+(bad_extra if i==3 else 0.0) for i in range(len(CHANNELS))]
    return {"scale_values":x,"template":template,"theta_true":theta,"bad_extra":bad_extra,"fit_without_nuisance":gls_fit(x,cov,[]),"fit_with_nuisance":gls_fit(x,cov,[template])}
def build_results():
    checks=[]; kappa=7/3; true_scale=kappa*kappa*M2_DIMLESS; packet=channels_from_scale(true_scale); sigmas=default_sigmas(packet,rel=1e-6); value_cov=make_value_covariance(sigmas,rho=0.15); derivs=jacobian(packet); scale_cov=propagate_covariance(value_cov,derivs)
    clean=build_synthetic_scale_fit(true_scale,scale_cov,theta=0.0); systematic=build_synthetic_scale_fit(true_scale,scale_cov,theta=0.02); bad=build_synthetic_scale_fit(true_scale,scale_cov,theta=0.02,bad_extra=1.0); fit_with_packet=fit_packet(packet,value_cov,[nuisance_template()])
    inv_scale_cov=invert_matrix(scale_cov); identity_check=matmul(scale_cov,inv_scale_cov); identity=[[1.0 if i==j else 0.0 for j in range(len(CHANNELS))] for i in range(len(CHANNELS))]
    checks.append(ok('dimensionless W33 M2=5049/4',abs(M2_DIMLESS-5049/4)<1e-15,M2_DIMLESS))
    checks.append(ok('scale covariance inverse valid',max_abs_matrix_diff(identity_check,identity)<1e-6,max_abs_matrix_diff(identity_check,identity)))
    checks.append(ok('clean nuisance fit recovers scale',abs(clean['fit_with_nuisance']['beta'][0]-true_scale)<1e-8,clean['fit_with_nuisance']['beta'][0]))
    checks.append(ok('clean nuisance amplitude near zero',abs(clean['fit_with_nuisance']['beta'][1])<1e-8,clean['fit_with_nuisance']['beta'][1]))
    checks.append(ok('systematic nuisance fit recovers scale',abs(systematic['fit_with_nuisance']['beta'][0]-true_scale)<1e-8,systematic['fit_with_nuisance']['beta'][0]))
    checks.append(ok('systematic nuisance fit recovers theta',abs(systematic['fit_with_nuisance']['beta'][1]-0.02)<1e-8,systematic['fit_with_nuisance']['beta'][1]))
    checks.append(ok('systematic packet improves chi-square with nuisance',systematic['fit_with_nuisance']['chi_square']<systematic['fit_without_nuisance']['chi_square'],{'without':systematic['fit_without_nuisance']['chi_square'],'with':systematic['fit_with_nuisance']['chi_square']}))
    checks.append(ok('systematic packet passes with nuisance',systematic['fit_with_nuisance']['passes_reduced_chi_square_lt_3'] is True,systematic['fit_with_nuisance']['reduced_chi_square']))
    checks.append(ok('bad packet still fails with nuisance',bad['fit_with_nuisance']['passes_reduced_chi_square_lt_3'] is False,bad['fit_with_nuisance']['reduced_chi_square']))
    checks.append(ok('nuisance design matrix has two columns',len(design_matrix([nuisance_template()])[0])==2,design_matrix([nuisance_template()])[0]))
    checks.append(ok('packet fit with nuisance is well-defined',fit_with_packet['fit']['degrees_of_freedom']==len(CHANNELS)-2,fit_with_packet['fit']['degrees_of_freedom']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXLV","title":"Nuisance/Systematic Parameter Fit Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(1 for c in checks if c['passed']),"true_scale":true_scale,"dimensionless_kernel":{"M2":"5049/4","role":"physical channel estimates fit X=kappa^2M2 with optional nuisance modes"},"nuisance_model":{"linear_model":"X_i = X*1_i + theta*b_i + noise_i","design_matrix":"A=[1,b]","estimator":"beta_hat=(A^T C^-1 A)^-1 A^T C^-1 X","chi_square":"chi2=(X-A beta_hat)^T C^-1 (X-A beta_hat)","degrees_of_freedom":"N-rank(A)","template_b":nuisance_template()},"clean_fit":clean,"systematic_fit":systematic,"bad_fit":bad,"packet_fit_with_nuisance":fit_with_packet['fit'],"architecture_upgrade":"CCCXLIV supplied correlated covariance fitting. CCCXLV adds explicit nuisance/systematic parameters, allowing coherent systematic modes to be fit and removed while retaining a residual chi-square falsification test.","theorem":"For a one-sector W33 response packet with known systematic templates, the common scale and nuisance amplitudes are estimated by generalized least squares with design matrix A=[1,b1,b2,...]. A coherent systematic lying in the nuisance template subspace is absorbed without falsifying the model; residuals outside that subspace still produce a chi-square failure.","honesty_boundary":"The nuisance template here is synthetic. Real empirical use must derive nuisance templates from actual detector, calibration, or modeling systematics.","checks":checks}
def main():
    results=build_results(); out_path=ROOT/'PART_CCCXLV_nuisance_parameter_fit_results.json'; out_path.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":results['part'],"verified":results['verified'],"checks_passed":results['checks_passed'],"checks_total":results['checks_total'],"out_path":str(out_path)},indent=2))
if __name__=='__main__': main()
