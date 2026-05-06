#!/usr/bin/env python3
"""PART CCCXLVII -- Multi-Sector Extension Compiler.

Generalizes the one-sector observable identity to S sectors.  Each channel i can
belong to a sector a(i), and estimates

    X_i = X_{a(i)} + noise_i.

This is the minimal extension needed when one physical response packet cannot be
explained by a single spectral scale.  We compare one-sector, two-sector, and
free-channel alternatives by GLS/AIC/BIC on synthetic packets.
"""
from __future__ import annotations
import json, math
from pathlib import Path
from typing import Any, Dict, List
ROOT=Path(__file__).resolve().parents[1]
Q=3; K=12; V=40; PHI3=Q*Q+Q+1; PHI6=Q*Q-Q+1; B=2*V-PHI3; A0=(V//2)*PHI6; DELTA=B*B+4*A0; M2_DIMLESS=DELTA/4.0
CHANNELS=["mass","gap","heat_trace","spinor_trace","resolvent_trace","zeta"]
def ok(n,c,v=None): return {"name":n,"passed":bool(c),"value":v}
def inv(M):
    n=len(M); A=[row[:] + [1.0 if i==j else 0.0 for j in range(n)] for i,row in enumerate(M)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(A[r][c])); A[c],A[p]=A[p],A[c]; piv=A[c][c]
        if abs(piv)<1e-30: raise ValueError('singular')
        A[c]=[x/piv for x in A[c]]
        for r in range(n):
            if r==c: continue
            f=A[r][c]; A[r]=[A[r][j]-f*A[c][j] for j in range(2*n)]
    return [row[n:] for row in A]
def T(M): return [list(row) for row in zip(*M)]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def mv(A,v): return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def design(assignments):
    sectors=sorted(set(assignments)); return [[1.0 if assignments[i]==s else 0.0 for s in sectors] for i in range(len(assignments))],sectors
def fit(x,C,assignments):
    A,sectors=design(assignments); At=T(A); Ci=inv(C); N=mm(mm(At,Ci),A); Ni=inv(N); beta=mv(Ni,mv(mm(At,Ci),x)); yhat=mv(A,beta); res=[xi-yi for xi,yi in zip(x,yhat)]; chi2=dot(res,mv(Ci,res)); n=len(x); k=len(beta); dof=n-k
    return {"assignments":assignments,"sectors":sectors,"sector_scales":beta,"chi_square":chi2,"degrees_of_freedom":dof,"reduced_chi_square":chi2/dof if dof else float('nan'),"aic":chi2+2*k,"bic":chi2+k*math.log(n),"residuals":res,"passes_reduced_chi_square_lt_3":(chi2/dof)<3 if dof else False}
def covariance(sig=0.01,rho=0.10):
    n=len(CHANNELS); return [[(1 if i==j else rho)*sig*sig for j in range(n)] for i in range(n)]
def compare(x,C):
    models={
        "one_sector":fit(x,C,[0,0,0,0,0,0]),
        "two_sector_geometry_response":fit(x,C,[0,0,1,1,1,1]),
        "two_sector_even_odd_channels":fit(x,C,[0,1,0,1,0,1]),
        "free_channel":fit(x,C,list(range(6)))
    }
    return {"models":models,"best_aic":min(models,key=lambda m:models[m]['aic']),"best_bic":min(models,key=lambda m:models[m]['bic'])}
def synthetic_one_sector(X): return [X]*6
def synthetic_two_sector(X0,X1): return [X0,X0,X1,X1,X1,X1]
def build_results():
    checks=[]; X0=(7/3)**2*M2_DIMLESS; X1=X0*1.37; C=covariance(sig=0.01,rho=0.10)
    one=compare(synthetic_one_sector(X0),C); two=compare(synthetic_two_sector(X0,X1),C); bad=compare([X0,X0+0.4,X1-0.3,X1+0.6,X0-0.7,X1+0.2],C)
    checks.append(ok('dimensionless W33 M2=5049/4',abs(M2_DIMLESS-5049/4)<1e-15,M2_DIMLESS))
    checks.append(ok('one-sector data BIC selects one-sector model',one['best_bic']=='one_sector',one['best_bic']))
    checks.append(ok('two-sector data BIC selects geometry/response split',two['best_bic']=='two_sector_geometry_response',two['best_bic']))
    checks.append(ok('two-sector fit recovers X0',abs(two['models']['two_sector_geometry_response']['sector_scales'][0]-X0)<1e-8,two['models']['two_sector_geometry_response']['sector_scales']))
    checks.append(ok('two-sector fit recovers X1',abs(two['models']['two_sector_geometry_response']['sector_scales'][1]-X1)<1e-8,two['models']['two_sector_geometry_response']['sector_scales']))
    checks.append(ok('one-sector fails two-sector data',two['models']['one_sector']['reduced_chi_square']>3,two['models']['one_sector']['reduced_chi_square']))
    checks.append(ok('free-channel saturates bad data',abs(bad['models']['free_channel']['chi_square'])<1e-8,bad['models']['free_channel']['chi_square']))
    verified=all(c['passed'] for c in checks)
    return {"part":"CCCXLVII","title":"Multi-Sector Extension Compiler","verified":verified,"checks_total":len(checks),"checks_passed":sum(c['passed'] for c in checks),"dimensionless_kernel":{"M2":"5049/4","one_sector_identity":"all channels share one scale X","multi_sector_identity":"channels share scale by sector assignment a(i)"},"model_formulas":{"one_sector":"X_i=X+noise_i","multi_sector":"X_i=X_{a(i)}+noise_i","free_channel":"X_i=alpha_i+noise_i"},"sample_scales":{"X0":X0,"X1":X1,"ratio_X1_over_X0":X1/X0},"one_sector_case":one,"two_sector_case":two,"bad_mixed_case":bad,"architecture_upgrade":"CCCXLVI compared one-sector/nuisance/broken alternatives. CCCXLVII generalizes the response identity to multiple spectral sectors X_a, allowing model comparison between one-sector, structured multi-sector, and free-channel alternatives.","theorem":"If a response packet cannot satisfy one common scale, the next controlled extension is a sector map a(i) with X_i=X_{a(i)}+noise_i. Structured multi-sector models can be selected against the one-sector model and against the saturated free-channel alternative by GLS/AIC/BIC.","honesty_boundary":"Sector assignments here are synthetic hypotheses. Real use requires deriving sector maps from W33 operators or physical channel identifications.","checks":checks}
def main():
    r=build_results(); out=ROOT/'PART_CCCXLVII_multi_sector_extension_results.json'; out.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n',encoding='utf-8'); print(json.dumps({"part":r['part'],"verified":r['verified'],"checks_passed":r['checks_passed'],"checks_total":r['checks_total'],"out_path":str(out)},indent=2))
if __name__=='__main__': main()
