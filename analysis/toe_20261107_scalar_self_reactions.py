"""First omitted 3<->2 collision on the published sterile-parent histories.

This is a consistency diagnostic, NOT self-consistent dark-sector transport.
Tree scalar amplitudes include all 10 cubic-quartic and 15 cubic-cubic-cubic
diagrams. Established threshold nullification is credited to Voloshin and
Hufnagel--Tytgat2212.09759. All momenta are in units of the supplied mass.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import itertools
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, simpson, solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.special import kv
from scipy.stats import qmc

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('parent_kinetics',ROOT/'analysis/toe_20261107_sterile_phase_space.py')
p=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(p)
PAIRS=list(itertools.combinations(range(5),2))
DOUBLE_PAIRS=[(a,b) for ia,a in enumerate(PAIRS) for b in PAIRS[ia+1:] if not set(a)&set(b)]


def minkowski(x):
    return x[...,0]**2-np.sum(x[...,1:]**2,axis=-1)


def amplitude(legs,g3,g4):
    """All five legs incoming; g3 has units m and g4 is dimensionless.

    Numerically m=1, so physical M=returned value/m. An overall phase/sign
    drops out. Internal denominators never hit a physical one-particle pole
    in on-shell 3->2 equal-mass kinematics.
    """
    inv={a:1/(minkowski(legs[...,a[0],:]+legs[...,a[1],:])-1) for a in PAIRS}
    return g3*g4*sum(inv.values())+g3**3*sum(inv[a]*inv[b] for a,b in DOUBLE_PAIRS)


def directions(cosine,azimuth):
    s=np.sqrt(np.maximum(0,1-cosine*cosine))
    return np.stack([s*np.cos(azimuth),s*np.sin(azimuth),cosine],axis=-1)


def boost(four,beta):
    b2=np.sum(beta*beta,axis=-1);gamma=1/np.sqrt(1-b2)
    bp=np.sum(beta*four[...,1:],axis=-1)
    factor=np.divide(gamma-1,b2,out=np.full_like(b2,.5),where=b2>1e-20)*bp+gamma*four[...,0]
    return np.concatenate([(gamma*(four[...,0]+bp))[...,None],four[...,1:]+factor[...,None]*beta],axis=-1)


def kinematics(momentum,direction,final_direction):
    """Three positive incoming magnitudes and directions; final two in CM."""
    incoming=np.concatenate([np.sqrt(1+momentum**2)[...,None],momentum[...,None]*direction],axis=-1)
    total=incoming.sum(axis=-2);s=minkowski(total)
    final_E=np.sqrt(s)/2;final_p=np.sqrt(s/4-1)
    one=np.concatenate([final_E[...,None],final_p[...,None]*final_direction],axis=-1)
    two=np.concatenate([final_E[...,None],-final_p[...,None]*final_direction],axis=-1)
    beta=total[...,1:]/total[...,0,None]
    outgoing=np.stack([boost(one,beta),boost(two,beta)],axis=-2)
    return np.concatenate([incoming,-outgoing],axis=-2),np.sqrt(1-4/s)


def proposal(r,u):
    """Sample normalized q^2 exp(-sqrt(q^2+r^2)) with resolved inverse CDF."""
    grid=np.r_[0.,np.geomspace(1e-7,max(100.,12*math.sqrt(r)),24000)]
    # Shift exponential by r for stability; it cancels in the normalized CDF.
    density=grid**2*np.exp(r-np.hypot(grid,r))
    cdf=np.r_[0.,cumulative_trapezoid(density,grid)];cdf/=cdf[-1]
    distinct=np.r_[True,np.diff(cdf)>1e-15]
    return np.interp(u,cdf[distinct],grid[distinct])


def sample(r,power,seed):
    u=qmc.Sobol(11,scramble=True,seed=seed).random_base2(power)
    q=proposal(r,u[:,:3]);dirs=directions(2*u[:,3:6]-1,2*math.pi*u[:,6:9])
    final=directions(2*u[:,9]-1,2*math.pi*u[:,10])
    legs,beta=kinematics(q/r,dirs,final)
    return legs,beta


def collision_average(legs,beta,r,lam,ratio):
    """Forward/backward event densities in units m^4, with 3!2! factors.

    Sampling the incoming triple from normalized MB makes equilibrium energy
    conservation cancel all exponentials. ratio(q)=f_actual(q)/exp(-E/T).
    This permits the reverse 2->3 integral on precisely the same phase space.
    """
    g4=6*lam;g3=math.sqrt(18*lam)
    amp=amplitude(legs,g3,g4)
    q=np.linalg.norm(legs[...,1:],axis=-1)*r
    R=ratio(q)
    weight=beta*amp**2/np.prod(legs[:,:3,0],axis=1)
    n_eq=kv(2,r)/(2*math.pi**2*r)
    pref=n_eq**3/(math.factorial(3)*math.factorial(2)*64*math.pi)
    forward=pref*np.mean(weight*np.prod(R[:,:3],axis=1))
    reverse=pref*np.mean(weight*np.prod(R[:,3:],axis=1))
    return float(forward),float(reverse)


def elastic_sample(r,power,seed):
    u=qmc.Sobol(8,scramble=True,seed=seed).random_base2(power)
    q=proposal(r,u[:,:2]);dirs=directions(2*u[:,2:4]-1,2*math.pi*u[:,4:6])
    incoming=np.concatenate([np.sqrt(1+(q/r)**2)[...,None],(q/r)[...,None]*dirs],axis=-1)
    total=incoming.sum(axis=1);s=minkowski(total)
    E=np.sqrt(s)/2;mag=np.sqrt(np.maximum(0,s/4-1))
    direction=directions(2*u[:,6]-1,2*math.pi*u[:,7])
    one=np.concatenate([E[:,None],mag[:,None]*direction],axis=1)
    two=np.concatenate([E[:,None],-mag[:,None]*direction],axis=1)
    velocity=total[:,1:]/total[:,0,None]
    return np.concatenate([incoming,-np.stack([boost(one,velocity),boost(two,velocity)],axis=1)],axis=1),np.sqrt(1-4/s)


def elastic_average(legs,beta,r,lam,ratio):
    g4=6*lam;g3sq=18*lam
    amp=g4+g3sq*sum(1/(minkowski(legs[:,0]+legs[:,j])-1) for j in [1,2,3])
    q=np.linalg.norm(legs[...,1:],axis=-1)*r;R=ratio(q)
    forward=np.prod(R[:,:2],axis=1);reverse=np.prod(R[:,2:],axis=1)
    weight=beta*amp**2/np.prod(legs[:,:2,0],axis=1)
    n_eq=kv(2,r)/(2*math.pi**2*r)
    pref=n_eq**2/(math.factorial(2)**2*32*math.pi)
    events=pref*np.mean(weight*forward)
    # Factor1/2 avoids counting each forward/reverse elastic transition twice.
    # This is the classical Boltzmann entropy production, not net number change.
    logratio=np.log(np.maximum(forward,1e-300))-np.log(np.maximum(reverse,1e-300))
    entropy=pref/2*np.mean(weight*(forward-reverse)*logratio)
    return float(events),float(entropy)


def parent_history(mass,nq=144):
    pars=p.inverse_decay_branch(mass);q,w=p.quadrature(nq,70.)
    ker=p.Kernel(q,w,pars['A'],pars['DN'],pars['DH'])
    sol=solve_ivp(ker.rhs,(.001,10.),np.zeros_like(q),method='BDF',jac=ker.jac,rtol=2e-9,atol=1e-13,dense_output=True)
    assert sol.success
    return pars,q,w,sol


def history_ratio(q,f,r):
    # Log interpolation retains positivity and the exponential tail. Actual
    # upstream quadrature cutoff is70. Below its first node use the endpoint;
    # above70 explicitly truncate, with QMC tail fractions reported separately.
    interp=PchipInterpolator(q,np.log(np.maximum(f,1e-300)),extrapolate=False)
    def ratio(x):
        xx=np.clip(x,q[0],q[-1]);logf=interp(xx)
        ans=np.exp(np.minimum(600,logf+np.hypot(x,r)))
        return np.where(x>q[-1],0.,ans)
    return ratio


def evaluate(power=15,seeds=(701,1701,2701,3701)):
    parent={m:parent_history(m) for m in [16.,30.,100.]};rows=[]
    for r in [.3,1.,3.,6.]:
        runs={m:[] for m in parent};elastic_runs={m:[] for m in parent}
        diagnostics=[]
        for seed in seeds:
            legs,beta=sample(r,power,seed)
            elegs,ebeta=elastic_sample(r,power,seed+50000)
            diagnostics.append(float(np.mean(np.max(np.linalg.norm(legs[...,1:],axis=-1)*r,axis=1)>70)))
            for mass,(pars,q,w,sol) in parent.items():
                f=np.maximum(sol.sol(r),0.);lam=pars['minimal_Z2_parent_quartic_if_imposed']
                fw,bw=collision_average(legs,beta,r,lam,history_ratio(q,f,r))
                nS=float(w@(q*q*f))/(2*math.pi**2*r**3)
                factor=p.M0/pars['m_S_GeV']*r*r/nS
                runs[mass].append([fw*factor,bw*factor,(bw-fw)*factor])
                ev,entropy=elastic_average(elegs,ebeta,r,lam,history_ratio(q,f,r))
                elastic_runs[mass].append([ev*factor,entropy*factor])
        for mass,vals in runs.items():
            pars,q,w,sol=parent[mass];v=np.array(vals);mean=v.mean(axis=0)
            error=v.std(axis=0,ddof=1)/math.sqrt(len(seeds)) if len(seeds)>1 else np.full(3,np.nan)
            f=np.maximum(sol.sol(r),0.);J=float(w@(q*q/np.hypot(q,r)*f))
            n_integral=float(w@(q*q*f));E=np.hypot(q,r)
            omitted=pars['DN']*r**3*J/n_integral
            # Every physical diagram contains either g3*g4 or g3^3. Keeping
            # m fixed and scaling minimal-Z2 quartic by t scales |M|^2 by t^3.
            # Below is only a first-variation diagnostic, not an allowed UV bound.
            maxevent=max(mean[0],mean[1])
            elastic_vals=np.array(elastic_runs[mass]);elastic_mean=elastic_vals.mean(axis=0)
            row=dict(M_keV=mass,r=r,T_GeV=pars['m_S_GeV']/r,
                     lambda_S_if_minimal_Z2=pars['minimal_Z2_parent_quartic_if_imposed'],
                     gamma32_over_nS_H=float(mean[0]),gamma23_over_nS_H=float(mean[1]),
                     net_number_gain_over_nS_H=float(mean[2]),
                     replicate_standard_error_over_nS_H=error.tolist(),
                     gammaNN_over_nS_H=omitted,
                     elastic_event_density_over_nS_H=float(elastic_mean[0]),
                     elastic_entropy_production_over_nS_H=float(elastic_mean[1]),
                     elastic_replicate_standard_error_over_nS_H=(elastic_vals.std(axis=0,ddof=1)/math.sqrt(len(seeds))).tolist(),
                     quartic_for_max_oneway_rate_point1_at_fixed_history=float(pars['minimal_Z2_parent_quartic_if_imposed']*(.1/maxevent)**(1/3)),
                     fraction_samples_touching_q70_cutoff=max(diagnostics))
            rows.append(row)
            print('SELF',mass,r,'32',mean[0],'23',mean[1],'net',mean[2],'elastic_entropy',elastic_mean[1],flush=True)
    return dict(status='COMPUTED_FIRST_OMITTED_3TO2_COLLISION_NOT_CORRECTED_RELIC_DENSITY',
                parent_input_sha256={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest() for s in ['analysis/toe_20261107_sterile_phase_space.py','data/toe_20261107_sterile_phase_space.json']},
                power=power,scrambles=list(seeds),samples_per_temperature=len(seeds)*2**power,rows=rows,
                action='V=1/2 m^2 s^2+g3/3! s^3+g4/4! s^4; minimal broken Z2: g3=3m^2/w, g4=3m^2/w^2=6lambdaS. Amplitude evaluated with m=1.',
                phase_space='gamma32=1/(3!2!)*integral product_i=1..3[d^3pi/(2pi)^3/(2Ei) fi]*integral dPhi2 |M|^2. dPhi2=beta/(8pi) dOmega/(4pi). Both event directions share measure by detailed balance. dn/dt+3Hn=gamma23-gamma32.',
                elastic='M22=g4+g3^2*(1/(s-1)+1/(t-1)+1/(u-1)) with m=1. Event density uses1/(2!2!); entropy production uses an additional1/2 times(forward-reverse)*log(forward/reverse). Positive entropy production shows the frozen distribution is not an elastic collision equilibrium. Elastic collisions conserve particle number and energy.',
                threshold='M_threshold=-5*g3*(3*g4-g3^2)/8 in m=1 units; exact zero for g3^2=3g4. Known scalar threshold nullification, not a discovery here.',
                interpretation='Positive or negative large first omitted collision invalidates treating the published frozen history as a minimal-Z2 solution. No self-consistent corrected spectrum or density is computed. Linear response cannot be extrapolated through a large change.',
                scope='Tree, constant zero-temperature broken potential, classical statistics, fixed gstar and frozen incoming history. No Bose factors, thermal masses/restoration, mean-field evolution, 4<->2 collisions, loop corrections or transfer functions. Published weak-self-sector benchmark remains a separate conditional truncation.',
                sources=['https://arxiv.org/abs/2212.09759','https://arxiv.org/abs/hep-ph/9211242'])


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--power',type=int,default=15);args=a.parse_args()
    result=evaluate(args.power)
    (ROOT/'data/toe_20261107_scalar_self_reactions.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
