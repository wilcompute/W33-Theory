"""Momentum-resolved classical collision benchmark for the current sterile proposal.

Not a complete hot-SM/UV completion. Fixed RD g*=106.75; four massless bath
scalars; V_portal=lambda_p/4*(w+s)^2 sum h_a^2; mN=y*w, w=vS/sqrt2.
Includes contact ss<->hh, elastic sh<->sh, s<->hh and s->NN. Scalar self
collisions, quantum statistics, NN backreaction and thermal masses omitted.
Methods are established kinetic theory (Merle-Totzauer1502.01011); no new
Boltzmann equation or primordial initial-condition prediction is claimed.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy.integrate import solve_ivp, simpson
from scipy.special import k1

ROOT=Path(__file__).resolve().parents[1]
GS=106.75
MP=1.22e19
M0=MP/(1.66*math.sqrt(GS))
YCOEFF=45/(4*math.pi**4*GS)
INCOMING='data/toe_20261106_sterile_parent_consistency.json'


def quadrature(n=96,maximum=50.):
    z,w=np.polynomial.legendre.leggauss(n)
    return (z+1)*maximum/2,w*maximum/2


def rates(row,portal_fraction=.5):
    lam=row['portal_floor']*(row['portal_clock_cap']/row['portal_floor'])**portal_fraction
    mass=row['m_S_GeV'];w=row['canonical_real_scalar_vev_GeV'];y=row['y']
    gn=y*y*mass/(16*math.pi)
    gh=lam*lam*w*w/(8*math.pi*mass)  # four identical h_a h_a channels
    return dict(lambda_portal=lam,M_keV=row['M_keV'],m_S_GeV=mass,w_GeV=w,y=y,
                Gamma_NN_GeV=gn,Gamma_hh_GeV=gh,
                A=lam*lam*M0/(32*math.pi**3*mass),
                DN=M0*gn/mass**2,DH=M0*gh/mass**2,
                inherited_portal_fraction=portal_fraction)


def inverse_decay_branch(M_keV,m_S_GeV=1000.,clock_fraction=.8,target_omega=.12):
    """Analytic zero-initial, no-annihilation abundance family, not a mass prediction.

    At lambda_p=eta*alpha_max*mh^2/(2*b*w^2), mN=y*w,
    Gamma_hh/Gamma_NN=[eta*alpha_max*mh^2/(sqrt2*b*mN*mS)]^2.
    Integrating the scalar number equation gives YN=2*c*(3pi/2)*
    DN*DH/(DN+DH), independently of parent kinetic equilibration.
    Full collision runs below retain contact annihilation, not this closure.
    """
    M=M_keV*1e-6;mass=m_S_GeV;eta=clock_fraction
    K=2.2e-6*125.25**2/(math.sqrt(2)*.053)
    ratio=(eta*K/(M*mass))**2
    dn_eq=target_omega/(2.744e8*M*2*YCOEFF*3*math.pi/2)
    y=math.sqrt(16*math.pi*mass/M0*dn_eq*(1+1/ratio))
    w=M/y
    lam=eta*2.2e-6*125.25**2/(.053*2*w*w)
    gn=y*y*mass/(16*math.pi);gh=lam*lam*w*w/(8*math.pi*mass)
    return dict(lambda_portal=lam,M_keV=M_keV,m_S_GeV=mass,w_GeV=w,y=y,
                Gamma_NN_GeV=gn,Gamma_hh_GeV=gh,A=lam*lam*M0/(32*math.pi**3*mass),
                DN=M0*gn/mass**2,DH=M0*gh/mass**2,
                clock_fraction_input=eta,proxy_alpha_over_inherited_bound=eta,
                minimal_Z2_parent_quartic_if_imposed=mass**2/(2*w*w),
                old_annihilation_only_portal_floor=math.sqrt(32*math.pi*mass/M0),
                analytic_target_omega_no_contact_annihilation=target_omega,
                analytic_width_ratio=ratio,
                target_scope='Density input fixes y in the no-contact zero-initial linear limit; mN, mS and clock margin remain supplied. Full output includes contact gain/loss.')


class Kernel:
    def __init__(self,q,w,A,DN,DH,elastic=True):
        self.q=q;self.w=w;self.A=A;self.DN=DN;self.DH=DH;self.elastic=elastic
        self.number_weights=w*q*q
        self.angular=np.exp(-abs(q[:,None]-q[None,:])/2)*(-np.expm1(-np.minimum(q[:,None],q[None,:])))

    def components(self,r):
        E=np.hypot(self.q,r);feq=np.exp(-E);jweights=self.number_weights/E
        if self.elastic and self.A:
            common=2*self.A/(E*self.q)[:,None]*(self.w*self.q/E)[None,:]*self.angular
            delta=(E[None,:]-E[:,None])/2
            gain=common*np.exp(delta)
            loss=np.sum(common*np.exp(-delta),axis=1)
            L=gain-np.diag(loss)
        else:L=np.zeros((len(E),len(E)))
        return E,feq,jweights,L

    def rhs(self,r,f):
        E,feq,jw,L=self.components(r)
        J=jw@f;Jeq=r*k1(r)
        return ((self.A*Jeq+self.DH*r*r)*feq-(self.A*J+(self.DH+self.DN)*r*r)*f)/E+L@f

    def jac(self,r,f):
        E,feq,jw,L=self.components(r)
        J=jw@f
        return L-np.diag((self.A*J+(self.DH+self.DN)*r*r)/E)-self.A*np.outer(f/E,jw)


def initial(q,r,kind):
    if kind=='zero':return np.zeros_like(q)
    if kind=='thermal_MB':return np.exp(-np.hypot(q,r))
    raise ValueError(kind)


def decay_postprocess(q,w,rr,ff,DN,bins):
    """Integrate exact isotropic two-body daughter intervals in comoving q=p/T.

    Each parent q has daughters uniformly distributed between (E-q)/2 and
    (E+q)/2. Histogram bin integrals, not sampled bin centers, retain number.
    Global first three moments use analytic angular integrals independently.
    """
    hist=np.zeros((len(rr),len(bins)-1));mom=np.zeros((len(rr),4))
    for j,r in enumerate(rr):
        E=np.hypot(q,r);sink=DN*r*r*w*q*q/E*np.maximum(ff[:,j],0)
        lo=(E-q)/2;hi=(E+q)/2
        overlap=np.maximum(0,np.minimum(bins[1:,None],hi)-np.maximum(bins[:-1,None],lo))
        hist[j]=2*(overlap/q)@sink
        angular=np.array([np.ones_like(q),E/2,E*E/4+q*q/12,(E**3+E*q*q)/8])
        mom[j]=2*angular@sink
    h=simpson(hist,x=rr,axis=0);m=simpson(mom,x=rr,axis=0)
    assert abs(h.sum()-m[0]) < max(1e-13,1e-10*m[0])
    return h,m


def solve_case(pars,kind,nq=96,nr=801,elastic=True,r0=.001,rend=120.,qmax=50.,rtol=2e-8):
    q,w=quadrature(nq,qmax)
    ker=Kernel(q,w,pars['A'],pars['DN'],pars['DH'],elastic)
    start=time.monotonic()
    sol=solve_ivp(ker.rhs,(r0,rend),initial(q,r0,kind),method='BDF',jac=ker.jac,
                  rtol=rtol,atol=1e-12,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    rr=np.geomspace(r0,rend,nr);ff=sol.sol(rr)
    raw_min=float(ff.min())
    if raw_min < -5e-10:raise RuntimeError('Negative parent distribution beyond tolerance')
    bins=np.concatenate(([0.],np.geomspace(.001,100.,180)))
    h,m=decay_postprocess(q,w,rr,ff,pars['DN'],bins)
    Inum=ker.number_weights@ff
    YN=YCOEFF*m[0]
    omega=2.744e8*pars['M_keV']*1e-6*YN
    fthermal=np.exp(-np.hypot(q,1.))
    f_at_1=sol.sol(1.)
    details=[]
    for r in [.1,.3,1.,2.,3.,5.,10.,20.,50.,120.]:
        E=np.hypot(q,r);f=sol.sol(r);eq=np.exp(-E)
        eqI=float(ker.number_weights@eq)
        details.append(dict(r=r,T_GeV=pars['m_S_GeV']/r,
                            Y_S=float(YCOEFF*(ker.number_weights@f)),
                            parent_number_over_MB_equilibrium=float(ker.number_weights@f)/eqI if eqI>1e-40 else None))
    # Cumulative s balance, including bath inverse decays and annihilation.
    J=np.sum((w*q*q)[:,None]/np.hypot(q[:,None],rr)*np.maximum(ff,0),axis=0)
    Jeq=rr*k1(rr)
    ann=pars['A']*(Jeq**2-J**2)
    bath=pars['DH']*rr**2*(Jeq-J)
    sink=pars['DN']*rr**2*J
    integrated=simpson(ann+bath-sink,x=rr)
    balance_error=float(Inum[-1]-Inum[0]-integrated)
    balance_scale=max(float(abs(Inum[0])+simpson(abs(ann)+abs(bath)+abs(sink),x=rr)),1e-12)
    branch=pars['DN']/(pars['DN']+pars['DH'])
    number_sumrule=2*branch*(Inum[0]-Inum[-1]+simpson(ann+pars['DH']*rr**2*Jeq,x=rr))
    upper_IN=2*branch*(Inum[0]+pars['A']*3*math.pi**2/32+pars['DH']*3*math.pi/2)
    time_fractions={}
    for temp in [100.,160.,200.]:
        rc=pars['m_S_GeV']/temp
        if rc>=rend:frac=0.
        elif rc<=r0:frac=1.
        else:
            mask=rr>rc
            jc=float(np.sum(w*q*q/np.hypot(q,rc)*np.maximum(sol.sol(rc),0)))
            rpart=np.r_[rc,rr[mask]]
            npart=np.r_[2*pars['DN']*rc*rc*jc,2*sink[mask]]
            frac=float(simpson(npart,x=rpart)/m[0])
        time_fractions[str(temp)]=frac
    bin_average_fN=h/((bins[1:]**3-bins[:-1]**3)/3)
    return dict(parameters=pars,initial_scalar=kind,elastic_scattering_included=elastic,nq=nq,nr=nr,
                r_interval=[r0,rend],q_parent_max=qmax,
                omega_h2=omega,Y_N=YN,mean_q=float(m[1]/m[0]),rms_q=float(math.sqrt(m[2]/m[0])),
                third_raw_q_moment=float(m[3]/m[0]),
                Y_scalar_remaining=float(YCOEFF*Inum[-1]),
                raw_min_f_scalar=raw_min,
                scalar_number_at_r1_over_equilibrium=float(ker.number_weights@f_at_1/(ker.number_weights@fthermal)),
                scalar_integrated_number_balance_absolute_error=balance_error,
                scalar_integrated_number_balance_relative_error=balance_error/balance_scale,
                daughter_number_histogram_vs_analytic_moment_relative_error=float((h.sum()-m[0])/m[0]),
                integrated_number_sumrule_Y_N=float(YCOEFF*number_sumrule),
                integrated_number_sumrule_relative_error=float((number_sumrule-m[0])/m[0]),
                infinite_interval_dropping_annihilation_loss_upper_omega=float(2.744e8*pars['M_keV']*1e-6*YCOEFF*upper_IN),
                fraction_sterile_number_produced_below_temperature_GeV=time_fractions,
                max_final_bin_averaged_spin_summed_fN=float(bin_average_fN.max()),
                fraction_N_in_bins_with_average_fN_above_point1=float(h[bin_average_fN>.1].sum()/h.sum()),
                occupancy_scope='Finite-bin averages only, not a pointwise Pauli bound or a computation of NN inverse decays.',
                comoving_daughter_bin_edges=bins.tolist(),
                comoving_daughter_Y_per_bin=(YCOEFF*h).tolist(),
                scalar_history=details,solver=dict(method='BDF',rtol=rtol,atol=1e-12,
                                                evaluations=sol.nfev,seconds=time.monotonic()-start))


def build(quick=False):
    parent=json.loads((ROOT/INCOMING).read_text())
    rows=parent['incoming_open_points_under_parent_hypothesis']
    results=[]
    fractions=[.5] if quick else [0.,.5,1.]
    for row in rows:
        for fraction in fractions:
            for kind in ['zero','thermal_MB']:
                out=solve_case(rates(row,fraction),kind,nq=64 if quick else 96,nr=501 if quick else 1001)
                results.append(out)
                print(row['M_keV'],row['m_S_GeV'],fraction,kind,'Omega',out['omega_h2'],'q',out['mean_q'],'balance',out['scalar_integrated_number_balance_relative_error'],flush=True)
    reopened=[]
    for Mk in [16.,30.,100.]:
        par=inverse_decay_branch(Mk)
        out=solve_case(par,'zero',nq=64 if quick else 96,nr=701 if quick else 1001)
        reopened.append(out)
        print('INVERSE_BRANCH',Mk,'Omega',out['omega_h2'],'lambdaS',par['minimal_Z2_parent_quartic_if_imposed'],'portal',par['lambda_portal'],flush=True)
    return dict(status='PASS_DECLARED_MOMENTUM_RESOLVED_CLASSICAL_COLLISION_BENCHMARK',quick=quick,
                input_raw_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in [INCOMING,'analysis/toe_uv/sterile_hh.py','analysis/toe_uv/sterile_hh.json']},
                rows=results,reopened_inverse_decay_examples=reopened,
                analytic_number_sumrule='IN=2*BR_N*[IS(initial)-IS(final)+integral dr A*(Jeq^2-J^2)+DH*integral dr r^3*K1(r)]. Elastic scattering drops out exactly. integrals on0..infinity: r^3*K1=3pi/2 and (r*K1)^2=3pi^2/32.',
                linear_zero_initial_limit='For A=0, no initial scalar and complete final decay, YN=2*c*(3pi/2)*DN*DH/(DN+DH). Equality of scalar and bath distributions is NOT required. This is standard integrated source/branching logic, applied here to the stored proposal.',
                clock_branch_identity='At inherited clock cap fraction eta, Gamma_hh/Gamma_NN=[eta*alpha_max*mh^2/(sqrt2*b*mN*mS)]^2, independent of y. This is an algebraic identity under the stated width and clock conventions, not a measured bound.',
                definitions='r=mS/T, q=p/T, E=sqrt(q^2+r^2), J=integral dq q^2 fS/E, Jeq=r*K1(r); fN spin-summed, YN=45/(4pi^4 gs)*integral dq q^2 fN.',
                action='Canonical real fluctuation s about w=vS/sqrt2, mass mS supplied. Portal V=lambda_p/4*(w+s)^2 sum_{a=1}^4 h_a^2. Four effectively massless bath real scalars maintained in MB equilibrium. Majorana mN=y*w. No minimal Z2 scalar self-potential inferred.',
                collision_normalization='Tagged-s ss->h_a h_a has identical-final phase factor1/2; summed |M|^2=4lambda_p^2. sigma*vM=4lambda_p^2/(64pi E1E2). A=lambda_p^2*M0/(32pi^3*mS). Gamma_hh=lambda_p^2*w^2/(8pi*mS), Gamma_NN=y^2*mS/(16pi).',
                scalar_equation='dfS/dr=[A*(Jeq*exp(-E)-J*fS)+r^2*(DH*(exp(-E)-fS)-DN*fS)]/E+L_el fS.',
                elastic_equation='L_el f_i=2A/(Ei qi)*sum_j wj qj/Ej*[exp(-|qi-qj|/2)-exp(-(qi+qj)/2)]*[exp((Ej-Ei)/2)fj-exp((Ei-Ej)/2)fi]. Positive transitions, MB detailed balance and exact quadrature number conservation.',
                daughter_equation='Each parent at(q,r) decays with probability DN*r^2/E dr; two daughters have uniform q in[(E-q)/2,(E+q)/2]. Histogram overlap integral and analytic angular moments agree in number.',
                ownership='Methods are established scalar-decay kinetic theory, including Merle-Totzauer1502.01011. Previous repo packet3869fe29 owns canonical normalization, prior CW application and moment-proxy criticism. This supplies a specified contact/elastic/inverse-decay numerical benchmark for the current stored points; no novelty of kinetic theory claimed.',
                sources=['https://arxiv.org/abs/1502.01011','https://arxiv.org/abs/1609.01289','https://arxiv.org/abs/0911.1120'],
                scope='Full isotropic parent momentum dynamics within the declared collision truncation; no scalar kinetic-equilibrium closure imposed. Fixed g*=106.75, radiation domination and constant masses/vev during production. Quantum Bose/Pauli factors, NN inverse decays, finite-temperature masses/phase transitions, changing g*, scalar self interactions, off-shell higher-order processes and late coupled-cosmology transfer function are omitted. Previous minimal Z2 parent quartic is large, so these tree collision rates do not certify that UV completion. New quartic_if_imposed values are diagnostics only: even a quartic below1 does not justify omitting self number-changing processes. The transport model requires a separately negligible self-collision sector. No Ly-alpha exclusion or solved TOE.',
                initial_condition_scope='zero versus inherited MB thermal parent at r=.001 are separate inputs; neither is selected by a UV reheating mechanism.')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--quick',action='store_true');args=parser.parse_args()
    out=build(args.quick)
    name='data/toe_20261107_sterile_phase_space'+('_quick' if args.quick else '')+'.json'
    (ROOT/name).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],flush=True)
