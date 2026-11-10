#!/usr/bin/env python3
"""Independent replay of a finite W33 nonlinear U(1) vacuum theorem.

The specified model is a half-filled 40x40 point-line tight-binding
fermion plus the ALL-1620-shortest-octagon Wilson action. This is not
a physical gauge-coupling prediction or a continuum TOE.
"""
import json
import math
import sys
import numpy as np
from scipy.optimize import brentq
from w33_20261109_full_u1_variational_vacuum import model, physics

PI=math.pi
SQ6=math.sqrt(6.)

def coeff(beta,n):
    t=(beta/(PI*(2*n+1)))**2
    return 162*t**4/((1+16*t)*(1+6*t)**2)

def local_critical(beta):
    z=SQ6*beta/2
    return (beta/1152 - math.tanh(2*beta)/6400
            - math.tanh(z)/(400*SQ6)
            + beta/(1440*math.cosh(z)**2))

def pi_boundary(beta):
    return (2/(81*beta))*sum(
        (a:=coeff(beta,n))/(1+2*a) for n in range(1600))

def edge_delta(beta,kappa,y):
    return 81*kappa*y-(2/beta)*sum(
        math.log1p(coeff(beta,n)*y) for n in range(1600))

def minimizer(beta,kappa):
    kc=local_critical(beta)
    kp=pi_boundary(beta)
    if kappa>=kc:
        return 0.
    if kappa<=kp:
        return 2.
    return brentq(
        lambda y: 81*kappa-(2/beta)*sum(
            (a:=coeff(beta,n))/(1+a*y) for n in range(1600)),
        0,2,xtol=1e-13)

def main():
    B,edges,G,chords,endpoints,W=ctx=model()
    assert len(chords)==81 and W.shape==(1620,81)
    U=W[:81]
    # NEW integer improvement over "unimodular": signed permutation.
    assert np.array_equal(U.T@U,np.eye(81,dtype=int))
    assert np.all(np.sum(abs(U),axis=1)==1)
    assert np.all(np.sum(abs(U),axis=0)==1)

    # P_theta(t) = P0(t)+162*t^4*(1+6*t)^22*(1-cos theta).
    p,l=endpoints[0]
    det_err=[]
    for t in (.2,.7,2.):
        for th in (.2,1.1,PI):
            T=B.astype(complex)
            T[p,l]=np.exp(1j*th)
            observed=np.linalg.slogdet(np.eye(40)+t*T@T.conj().T)[1]
            predicted=(math.log1p(16*t)+24*math.log1p(6*t)
                +math.log1p(
                    162*t**4/((1+16*t)*(1+6*t)**2)*(1-math.cos(th))))
            det_err.append(abs(observed-predicted))
    assert max(det_err)<5e-11,det_err

    checks=[]
    for beta in (.1,.3,.5,1.,2.,5.,10.):
        k=local_critical(beta)
        partial=(2/(81*beta))*sum(coeff(beta,n) for n in range(1600))
        assert abs(k-partial)<2e-11,(beta,k,partial)
        checks.append((beta,k))
    assert all(a[1]<b[1] for a,b in zip(checks,checks[1:]))

    beta=1.
    kc=local_critical(beta)
    kp=pi_boundary(beta)
    assert 0<kp<kc
    k=(kp+kc)/2
    ym=minimizer(beta,k)
    assert 0<ym<2 and edge_delta(beta,k,ym)<min(
        edge_delta(beta,k,0),edge_delta(beta,k,2))
    for th in (.02,.4,1.2,PI):
        x=np.zeros(81)
        x[0]=th
        y=1-math.cos(th)
        f0=physics(np.zeros(81),ctx,0)[2]
        f1=physics(x,ctx,0)[2]
        assert abs((f1-f0)-edge_delta(beta,0,y))<3e-10
        assert abs(physics(x,ctx,1)[3]-81*y)<2e-11

    # Global sufficient flat-vacuum condition: from f'' >= -beta/4,
    # F(x)-F(0) >= -(beta/2-s_beta)*sum_j(1-cos x_j).
    # Since U is signed permutation:
    # S_all(x) >= sum_j(1-cos x_j).
    s=math.tanh(2*beta)/40+0.9*math.tanh(SQ6*beta/2)/SQ6
    kglobal=beta/2-s
    assert abs(kglobal-0.1668784485566458)<1e-12
    rng=np.random.default_rng(20261110)
    f0=physics(np.zeros(81),ctx,0)[2]
    for scale in (.02,.2,2.):
        x=rng.normal(size=81)*scale
        f=physics(x,ctx,0)[2]
        chord_penalty=float(np.sum(1-np.cos(x)))
        action=physics(x,ctx,1)[3]
        assert action>=chord_penalty-1e-10
        assert f-f0+kglobal*chord_penalty>=-2e-10

    # At zero temperature a rank-one edge phase lifts one of 15
    # dark singular modes at slope 3/8: F_infty has a linear cusp.
    small=[]
    for th in (.01,.001,.0001):
        T=B.astype(complex)
        T[p,l]=np.exp(1j*th)
        svals=np.linalg.svd(T,compute_uv=False)
        lifted=sorted(svals)[14]
        slope=lifted/abs(th)
        assert abs(slope-.375)<3e-4,slope
        small.append(slope)

    result={"status":"PASS_FINITE_W33_NONLINEAR_FLUX_CLOSED_CRITICAL_GLOBAL_COERCIVITY",
        "basis_octagons_signed_permutation":True,
        "all_beta_local_critical_formula":"beta/1152-tanh(2beta)/6400-tanh(sqrt(6)beta/2)/(400sqrt(6))+beta sech^2(sqrt(6)beta/2)/1440",
        "beta1":{"kappa_pi":kp,"kappa_c":kc,
                 "one_edge_interior_minimizer_y":ym,
                 "rigorous_global_sufficient_kappa":kglobal},
        "determinant_max_log_error":max(det_err),
        "beta_series_checks":checks,
        "zero_temperature_single_dark_slope":small,
        "scope":"Finite all-octagon W33 model. Global threshold sufficient, not sharp. No continuum or physical gauge coupling."}
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
