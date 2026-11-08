"""Canonical axion eigenmodes, relaxed troughs and convex-cosine controls.

Audit of the one-cosine simplification in31f833f38, not a rejection of the
multi-cosine model1605.00996. No cosmological likelihood is computed.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import sympy as s

ROOT=Path(__file__).resolve().parents[1]


def symbolic():
    a,phi,h,l=s.symbols('a phi h l',real=True)
    f,F,Lam,kappa=s.symbols('f F Lambda4 kappa',positive=True)
    phase=a/f+phi/F;V=Lam*(1-s.cos(phase));H=s.hessian(V,(a,phi))
    length=s.sqrt(f*f+F*F)
    rotated=s.simplify(phase.subs({a:(F*h-f*l)/length,phi:(f*h+F*l)/length},simultaneous=True))
    A,B,C,n=s.symbols('A B C n',positive=True)
    full=A*(1-s.cos(a/f))+B*(1-s.cos(phi/F))+C*(1-s.cos(a/f-n*phi/F))
    fullH=s.simplify(s.hessian(full,(a,phi)).subs({a:0,phi:0}))
    expected=s.Matrix([[(A+C)/f**2,-n*C/(f*F)],[-n*C/(f*F),(B+n*n*C)/F**2]])
    assert s.simplify(H.det())==0
    assert s.diff(rotated,l)==0
    assert s.simplify(fullH-expected)==s.zeros(2)
    det=s.factor(fullH.det())
    return dict(single_cosine_hessian=str(H),determinant=str(s.factor(H.det())),
                phase_in_canonical_modes=str(rotated),light_phase_derivative=str(s.diff(rotated,l)),
                massive_curvature='Lambda4*(1/f^2+1/F^2)*cos(sqrt(f^2+F^2)*h/(f*F))',
                trough='h=0 (mod2pi*f*F/sqrt(f^2+F^2)), a=-f*phi/F; massive eigenvalue constant along l',
                full_three_cosine_vacuum_hessian=str(fullH),full_three_cosine_determinant=str(det),
                corrected_scale_relation='If b=MP*tan(theta)/(2F), then F/MP=tan(theta)/(2b), not1/(2b*tan(theta)). This conditional algebra does not establish a varying physical mass.')


def hessian_cosines(amplitudes,charges,fields):
    phases=charges@fields;w=amplitudes*np.cos(phases)
    return np.einsum('i,ij,ik->jk',w,charges,charges)


def spectrum_and_slope(amplitudes,charges,fields):
    phases=charges@fields;w=amplitudes*np.cos(phases)
    H=hessian_cosines(amplitudes,charges,fields)
    angle=.5*math.atan2(2*H[0,1],H[0,0]-H[1,1])
    heavy=np.array([math.cos(angle),math.sin(angle)]);light=np.array([-heavy[1],heavy[0]])
    kh=charges@heavy;kl=charges@light
    high=float(w@(kh*kh));low_rayleigh=float(w@(kl*kl))
    # This positive minor formula avoids subtracting nearly equal determinants.
    det=sum(w[i]*w[j]*np.linalg.det(charges[[i,j]])**2 for i in range(len(w))for j in range(i+1,len(w)))
    low=float(det/high)
    gradient=-np.einsum('i,i,ij->j',amplitudes*np.sin(phases),kh*kh,charges)
    beta=-float(light@gradient)/(2*high)
    bound=.5*math.sqrt(low_rayleigh/high)*float(np.max(abs(kh*np.tan(phases))))
    return dict(heavy_mass_squared=high,light_mass_squared=low,light_rayleigh_curvature=low_rayleigh,
                beta_along_light_eigenvector=beta,convex_cosine_bound=bound,
                bound_ratio=abs(beta)/bound if bound>0 else 0.,heavy_eigenvector=heavy.tolist(),light_eigenvector=light.tolist())


def pinning_row(kappa,u=.7853981633974483,f=.01,F=10.):
    # V=Lambda4[ kappa*(a/f)^2/2+1-cos(a/f+phi/F) ], Lambda4=1.
    alpha=brentq(lambda x:kappa*x+math.sin(x+u),-u,0.,xtol=1e-15)
    phase=alpha+u;c=math.cos(phase);v=np.array([1/f,1/F])
    H=c*np.outer(v,v)+np.diag([kappa/(f*f),0.])
    eigenvalues,eigenvectors=np.linalg.eigh(H);heavy=eigenvectors[:,-1]
    slope=-f/F*c/(kappa+c);tangent=np.array([slope,1.])/math.sqrt(1+slope*slope)
    dh=-math.sin(phase)*float(heavy@v)**2*float(tangent@v)
    beta=-dh/(2*eigenvalues[-1])
    schur=kappa*c/(F*F*(kappa+c))
    return dict(kappa=kappa,held_phi_phase=u,f_over_MP=f,F_over_MP=F,
                relaxed_a_over_f=alpha,relaxed_phase=phase,gradient_residual=kappa*alpha+math.sin(phase),
                heavy_mass_squared=float(eigenvalues[-1]),light_mass_squared=float(eigenvalues[0]),
                relaxed_light_curvature=schur/(1+slope*slope),
                beta_physical_along_canonical_trough=float(beta),held_a_naive_beta=math.tan(u)/(2*F),
                da_dphi=slope,canonical_light_metric=1+slope*slope)


def convex_scan(count=4096):
    rng=np.random.default_rng(81108);rows=[]
    for _ in range(count):
        f,F=10**rng.uniform(-1,1,2);n=int(rng.choice([1,2,3,7,13,27]))
        # For n=1 the second phase can be x-d: keep all three in
        # (-pi/2,pi/2), as required by the positive-weight bound.
        x,d=rng.uniform(-.7,.7,2);y=(x-d)/n
        charges=np.array([[1/f,0.],[0.,1/F],[1/f,-n/F]])
        amp=10**rng.uniform(-3,3,3);fields=np.array([f*x,F*y])
        row=spectrum_and_slope(amp,charges,fields)
        assert row['bound_ratio']<=1+1e-10
        rows.append(row)
    return dict(count=count,max_bound_ratio=max(r['bound_ratio']for r in rows),
                max_mass_hierarchy=math.sqrt(max(r['heavy_mass_squared']/r['light_mass_squared']for r in rows)),
                interpretation='Standard Hellmann-Feynman plus Cauchy-Schwarz application on positive-cosine branches. Sampled verification, not a theorem derived by random search.',
                inequality='|MP*dln(mH)/dl| <= MP/2*sqrt((u^T H u)/lambdaH)*max_i |(qi.eH)*tan(qi.x)|, for canonical unit direction u, all Ai*cos(qi.x)>0. The scan uses u=eL. No claim for hilltops, negative cosine weights, cancellations or changing kinetic metric.')


def single_cosine_dynamics():
    f=1.;F=10.;k=math.hypot(1/f,1/F);Lam=1/(k*k)
    # Canonical heavy and light coordinates; changing light velocity is an
    # independent control for a supposed mass-varying interaction.
    histories=[]
    times=np.linspace(0,200,2001)
    for velocity in [0.,.03]:
        def rhs(t,z):return [z[1],-Lam*k*math.sin(k*z[0]),z[3],0.]
        sol=solve_ivp(rhs,(0,200),[.1/k,0.,0.,velocity],method='DOP853',rtol=1e-11,atol=1e-13,t_eval=times)
        assert sol.success
        energy=.5*sol.y[1]**2+Lam*(1-np.cos(k*sol.y[0]))
        histories.append(dict(light_velocity=velocity,heavy_coordinate=sol.y[0],relative_heavy_energy_drift=float(np.max(abs(energy/energy[0]-1)))))
    mismatch=float(np.max(abs(histories[0]['heavy_coordinate']-histories[1]['heavy_coordinate'])))
    return dict(max_heavy_history_difference=mismatch,max_relative_energy_drift=max(x['relative_heavy_energy_drift']for x in histories),
                scope='Two canonical fields in Minkowski time; no cosmological fit. Light velocity changes without changing the heavy trajectory. A separate light potential/interaction would change the model.')


def running_eft_control(beta0=.053,phi=.8):
    # Stable trig identity, independent of the atan near-pole implementation:
    # cos(atan(2b/Fi)+Fi*phi)/cos(atan(2b/Fi))
    # = cos(Fi*phi)-2*b*phi*sinc(Fi*phi).
    rows=[]
    for Fi in [.1,.01,.001,1e-6,1e-9]:
        x=Fi*phi;ratio=math.cos(x)-2*beta0*phi*np.sinc(x/math.pi)
        beta=(beta0*math.cos(x)+.5*Fi*math.sin(x))/ratio
        rows.append(dict(Fi=Fi,mass_ratio=math.sqrt(ratio),beta=beta))
    return dict(beta0=beta0,phi=phi,positive_Fi_rows=rows,
                continuous_Fi_zero_mass_ratio=math.sqrt(1-2*beta0*phi),
                continuous_Fi_zero_beta=beta0/(1-2*beta0*phi),
                separately_switched_exponential_mass_ratio=math.exp(-beta0*phi),
                identity='m^2/m0^2=cos(Fi*phi)-2*beta0*phi*sinc(Fi*phi); sinc(x)=sin(x)/x',
                scope='Audit of declared phenomenological mass law in d4c3be9c7. Fi=0 is a separately switched control in the code, not its continuous limit at fixed nonzero beta0. Does not establish a physical axion eigenmass or re-run CLASS.')


def build():
    result=dict(status='PHYSICAL_EIGENMODE_AND_DECLARED_COMPLETION_AUDIT_NOT_SOLVED_TOE',
                symbolic=symbolic(),pinning=[pinning_row(k,u)for u in [.3,math.pi/4,1.2]for k in np.geomspace(1e-6,1e6,25)],
                convex_controls=convex_scan(),single_cosine_dynamics=single_cosine_dynamics(),running_eft_control=running_eft_control(),
                scope='Single mixed cosine has one exactly flat canonical direction; its relaxed heavy mass does not vary along that direction. A stated quadratic pinning extension and convex three-cosine controls are tested separately. Does not exclude multi-cosine monodromy, finite-density effects, curved field metrics or full axion models. No full cosmological background/perturbation likelihood or naturalness completion.',
                sources=['https://arxiv.org/abs/1605.00996','analysis/toe_uv/monodromy_running.py','analysis/PASS12627_MCMC_SHEAR_RADIATIVE.md'])
    out=ROOT/'data/toe_20261108_axion_eigenmode_audit.json';out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('AXION_AUDIT',result['convex_controls'],result['single_cosine_dynamics'],flush=True)
    return result


if __name__=='__main__':build()
