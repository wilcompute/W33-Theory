"""Classical two-moment scalar/sterile transport with full tree 3<->2 rates.

Internal MB kinetic equilibrium is an explicit closure, not a full Boltzmann
solution. Fixed masses/vevs, four massless bath scalars and fixed RD gstar.
Includes the leading portal self-exchange diagrams omitted by contact-only
kinetics. No Bose statistics, thermal potential,4<->2 or UV protection.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp,simpson,quad
from scipy.interpolate import PchipInterpolator
from scipy.special import kve,kv,roots_genlaguerre

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('scalar_self',ROOT/'analysis/toe_20261107_scalar_self_reactions.py')
self=importlib.util.module_from_spec(spec);spec.loader.exec_module(self)
p=self.p
TABLE='data/toe_20261107_coupled_scalar_rate_table.json'


def make_rates(power=15,count=65):
    rows=[]
    for x in np.geomspace(.0001,10000.,count):
        vals=[]
        for seed in [4107,84107]:
            legs,beta=self.sample(x,power,seed)
            amp=self.amplitude(legs,math.sqrt(18),6.)
            vals.append(float(np.mean(beta*amp**2/np.prod(legs[:,:3,0],axis=1))/(768*math.pi)))
        rows.append(dict(inverse_dark_temperature=x,Tdark_over_m=1/x,
                         gamma32_over_n_eq_cubed_per_lambdaS_cubed=float(np.mean(vals)),
                         replicate_values=vals))
        print('RATE',x,rows[-1]['gamma32_over_n_eq_cubed_per_lambdaS_cubed'],flush=True)
    out=dict(power=power,scrambles=[4107,84107],rows=rows,
             definition='gamma32=m^4*lambdaS^3*k32(Tdark/m)*(nS/m^3)^3; inverse gamma23 replaces one actual nS by equilibrium n_eq(Tdark). All3!2! factors included.',
             source_raw_sha256={s:hashlib.sha256((ROOT/s).read_bytes()).hexdigest()for s in ['analysis/toe_20261107_scalar_self_reactions.py','analysis/toe_20261107_coupled_scalar_moments.py']},
             ownership='Full finite-momentum25diagram amplitude from c7079f950; established cannibal kinetics2212.09759. No new threshold theorem.')
    (ROOT/TABLE).write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    return out


def thermal_energy(t):
    x=1/np.asarray(t)
    return kve(1,x)/kve(2,x)+3*t


def heat_capacity(t):
    if t<.001:return 1.5+3.75*t-5.625*t*t
    ratio=float(kve(1,1/t)/kve(2,1/t))
    return 3+(1-ratio*ratio)/(t*t)-3*ratio/t


class ThermalRates:
    def __init__(self,table=None):
        table=table or json.loads((ROOT/TABLE).read_text())
        rows=sorted(table['rows'],key=lambda x:x['Tdark_over_m'])
        self.temperatures=np.array([x['Tdark_over_m']for x in rows])
        self.chemical=PchipInterpolator(np.log(self.temperatures),np.log([x['gamma32_over_n_eq_cubed_per_lambdaS_cubed']for x in rows]),extrapolate=False)
        temps=np.geomspace(1e-6,1e5,6000)
        kinetic=thermal_energy(temps)-1
        self.inverse_energy=PchipInterpolator(np.log(kinetic),np.log(temps),extrapolate=True)
        y,w=roots_genlaguerre(80,.5)
        ann=[];energy=[];elastic=[]
        c,cw=np.polynomial.legendre.leggauss(32)
        for t in temps[::6]:
            z=2+t*y;F=(1+3/(z*z-1))**2
            weights=w*z*np.sqrt((z*z-4)/y)*kve(1,z/t)*F
            total=weights.sum()
            ann.append(total/(64*math.pi*kve(2,1/t)**2))
            energy.append(float(weights@(2*t+z*kve(0,z/t)/kve(1,z/t))/total))
            mandel_t=-(z*z-4)[:,None]*(1-c)/2
            mandel_u=-(z*z-4)[:,None]*(1+c)/2
            matrix=6+18*(1/(z*z-1)[:,None]+1/(mandel_t-1)+1/(mandel_u-1))
            angular=matrix**2@cw/2
            elastic.append(float(np.sum(w/np.sqrt(y)*(z*z-4)*kve(1,z/t)*angular)/(256*math.pi*kve(2,1/t)**2)))
        self.ann=PchipInterpolator(np.log(temps[::6]),np.log(ann),extrapolate=True)
        self.pairenergy=PchipInterpolator(np.log(temps[::6]),np.log(energy),extrapolate=True)
        self.elastic=PchipInterpolator(np.log(temps[::6]),np.log(elastic),extrapolate=True)

    def temperature(self,energy):
        target=max(1+1e-9,energy)
        t=float(np.exp(self.inverse_energy(math.log(target-1))))
        # A tiny interpolation error is amplified by chemical relaxation rates
        # much faster than H. Polish the thermodynamic inversion, rather than
        # loosening equilibrium/conservation tests.
        for _ in range(3):
            candidate=t-(float(thermal_energy(t))-target)/heat_capacity(t)
            t=max(t/2,candidate)
        return t

    def k32(self,t):
        clipped=float(np.clip(t,self.temperatures[0],self.temperatures[-1]))
        return float(np.exp(self.chemical(math.log(clipped))))

    def a22(self,t):return float(np.exp(self.ann(math.log(t))))
    def epair(self,t):return float(np.exp(self.pairenergy(math.log(t))))
    def self_elastic(self,t):return float(np.exp(self.elastic(math.log(t))))


def elastic_generator(q,w,r,A,full_exchange=True,nangle=20):
    """Integrate the invariant t-dependent matrix element before bath reduction.

    Kij=1/2 integral_{|qi-qj|}^{qi+qj} dQ exp(-Q/2)
        [1+3r^2/((Ei-Ej)^2-Q^2-r^2)]^2.
    It reduces exactly to the previous contact kernel if exchange is disabled.
    """
    E=np.hypot(q,r)
    if full_exchange:
        z,weights=np.polynomial.legendre.leggauss(nangle)
        lower=abs(q[:,None]-q);upper=q[:,None]+q
        Q=(lower+upper)[...,None]/2+(upper-lower)[...,None]*z/2
        transfer=(E[:,None]-E)**2
        F=(1+3*r*r/(transfer[...,None]-Q*Q-r*r))**2
        angular=(upper-lower)/4*np.sum(weights*np.exp(-Q/2)*F,axis=-1)
    else:
        angular=np.exp(-abs(q[:,None]-q)/2)*(-np.expm1(-np.minimum(q[:,None],q)))
    common=2*A/(E*q)[:,None]*(w*q/E)[None,:]*angular
    delta=(E[None,:]-E[:,None])/2
    return common*np.exp(delta)-np.diag(np.sum(common*np.exp(-delta),axis=1))


class Moments:
    def __init__(self,pars,rates,nq=48,nangle=20,chemical_scale=1.,portal_exchange=True):
        self.pars=pars;self.rates=rates;self.nq=nq;self.nangle=nangle
        self.chemical_scale=chemical_scale;self.portal_exchange=portal_exchange
        self.z,self.w=np.polynomial.legendre.leggauss(nq)

    def closure(self,r,I,R):
        I=max(float(I),1e-50)
        t=self.rates.temperature(max(float(R)/(r*I),1+1e-9))
        x=1/t;ratio=float(kve(1,x)/kve(2,x))
        n=I/(2*math.pi**2*r**3)
        neq=float(t*kv(2,x)/(2*math.pi**2))
        J=I/r*ratio
        return t,n,neq,J

    def pieces(self,r,I,R):
        a=self.pars;t,n,neq,J=self.closure(r,I,R);theta=t*r
        I=max(float(I),1e-50);R=max(float(R),r*I)
        sourceJ=r*kv(1,r);sourceI=r*r*kv(2,r)
        number_decay=r**3*(a['DH']*sourceJ-(a['DH']+a['DN'])*J)
        energy_decay=r**3*(a['DH']*sourceI-(a['DH']+a['DN'])*I)
        chemical=-2*math.pi**2*p.M0/a['m_S_GeV']*r**5*a['minimal_Z2_parent_quartic_if_imposed']**3*self.chemical_scale*self.rates.k32(t)*n*n*(n-neq)
        bath_n=float(kv(2,r)/(2*math.pi**2*r))
        if self.portal_exchange:
            gain=self.rates.a22(1/r)*bath_n**2;loss=self.rates.a22(t)*n*n
            gainE=gain*self.rates.epair(1/r);lossE=loss*self.rates.epair(t)
        else:
            gain=bath_n**2/(32*math.pi)*(kve(1,r)/kve(2,r))**2
            loss=n*n/(32*math.pi)*(kve(1,1/t)/kve(2,1/t))**2
            gainE=gain*2*kve(2,r)/kve(1,r)
            lossE=loss*2*kve(2,1/t)/kve(1,1/t)
        factor=2*math.pi**2*p.M0/a['m_S_GeV']*a['lambda_portal']**2
        number_ann=2*factor*r**5*(gain-loss)
        energy_ann=factor*r**6*(gainE-lossE)
        maximum=max(40.,40*theta,12*math.sqrt(r*theta))
        q=(self.z+1)*maximum/2;w=self.w*maximum/2;E=np.hypot(q,r)
        shape=np.exp(np.maximum(-740,(r-E)/theta))
        f=I*shape/float(w@(q*q*shape))
        L=elastic_generator(q,w,r,a['A'],self.portal_exchange,self.nangle)
        energy_elastic=r*float((w*q*q*E)@(L@f))
        return dict(t=t,n=n,neq=neq,J=J,number_decay=number_decay,energy_decay=energy_decay,
                    chemical=chemical,number_ann=number_ann,energy_ann=energy_ann,energy_elastic=energy_elastic,
                    scalar_energy=R,scalar_number=I)

    def rhs(self,logr,state):
        r=math.exp(logr);I,R=state[:2];d=self.pieces(r,I,R);DN=self.pars['DN']
        return [d['number_decay']+d['number_ann']+d['chemical'],
                r*r*d['J']+d['energy_decay']+d['energy_ann']+d['energy_elastic'],
                2*DN*r**3*d['J'],DN*r**3*max(I,0),
                DN*r**3*(2*max(R,0)/3-r*r*d['J']/6),d['number_ann'],d['chemical']]


def solve(mass,rates,nq=48,nangle=20,chemical_scale=1.,portal_exchange=True,r0=.001,rend=80.,method='BDF',seed_interval=1e-5):
    pars=p.inverse_decay_branch(mass);model=Moments(pars,rates,nq,nangle,chemical_scale,portal_exchange)
    # Raw extensive variables near zero let a finite-difference Jacobian probe
    # unphysical energies per particle. Log(number),log(Tdark) instead enforce
    # the positive thermodynamic manifold. The seed is the zero-population
    # source over a declared tiny initial log-r interval, refined separately.
    initial=model.rhs(math.log(r0),[1e-30,2e-30,0.,0.,0.])
    initialI=max(1e-30,initial[0]*seed_interval)
    initialR=max(r0*initialI*1.001,initial[1]*seed_interval)
    initialT=rates.temperature(initialR/(r0*initialI))
    def physical(logr,state):
        I=math.exp(state[0]);t=math.exp(state[1]);r=math.exp(logr)
        return np.r_[I,r*I*thermal_energy(t),state[2:]]
    def logarithmic(logr,state):
        st=physical(logr,state);I,R=st[:2];r=math.exp(logr);t=math.exp(state[1])
        derivative=model.rhs(logr,st);dlogI=derivative[0]/I
        dlogT=(derivative[1]-R*(1+dlogI))/(r*I*t*heat_capacity(t))
        return np.r_[dlogI,dlogT,derivative[2:]]
    sol=solve_ivp(logarithmic,(math.log(r0)+seed_interval,math.log(rend)),[math.log(initialI),math.log(initialT),0.,0.,0.,0.,0.],method=method,
                  rtol=2e-7,atol=[1e-8,1e-8,1e-12,1e-12,1e-12,1e-11,1e-11],max_step=.06,dense_output=True)
    if not sol.success:raise RuntimeError(sol.message)
    I,R,IN,M1,M2,ann_integral,self_integral=physical(sol.t[-1],sol.y[:,-1])
    history=[]
    for r in [.003,.01,.03,.1,.3,1.,3.,6.,10.,20.,40.,80.]:
        if r<r0 or r>rend:continue
        st=physical(math.log(r),sol.sol(math.log(r)));d=model.pieces(r,*st[:2]);n=d['n'];neq=d['neq']
        history.append(dict(r=r,T_GeV=pars['m_S_GeV']/r,Tdark_over_T=d['t']*r,
                            nS_over_n_eq_dark=n/neq if neq>1e-290 else None,
                            nS_over_n_eq_bath=float(n/(kv(2,r)/(2*math.pi**2*r))),
                            net_self_number_over_nS_H=float(d['chemical']/max(st[0],1e-40)),
                            scalar_I=float(st[0]),scalar_R=float(st[1]),sterile_IN=float(st[2]),
                            self_elastic_particle_rate_over_H=float(2*n*rates.self_elastic(d['t'])*pars['minimal_Z2_parent_quartic_if_imposed']**2*p.M0/pars['m_S_GeV']*r*r),
                            max_MB_occupation=float(2*math.pi**2*n/(d['t']*kve(2,1/d['t']))),
                            Hartree_self_restoration_ratio=float(6*pars['minimal_Z2_parent_quartic_if_imposed']*n*kve(1,1/d['t'])/kve(2,1/d['t'])),
                            Hartree_bath_restoration_ratio=float(2*pars['lambda_portal']/(math.pi**2*r*r))))
    times=np.linspace(sol.t[0],sol.t[-1],1601);sampled=sol.sol(times)
    rr=np.exp(times);II=np.exp(sampled[0]);tt=np.exp(sampled[1])
    nn=II/(2*math.pi**2*rr**3);rat=kve(1,1/tt)/kve(2,1/tt)
    production=2*pars['DN']*rr**3*II/rr*rat
    elastic=np.array([2*n*rates.self_elastic(t)*pars['minimal_Z2_parent_quartic_if_imposed']**2*p.M0/pars['m_S_GeV']*r*r for n,t,r in zip(nn,tt,rr)])
    occupation=2*math.pi**2*nn/(tt*kve(2,1/tt))
    hartree=6*pars['minimal_Z2_parent_quartic_if_imposed']*nn*rat+2*pars['lambda_portal']/(math.pi**2*rr**2)
    integral=float(simpson(production,x=times))
    fraction=lambda mask:float(simpson(production*mask,x=times)/integral)
    diagnostics=dict(max_MB_occupation=float(occupation.max()),max_classical_Hartree_restoration_ratio=float(hartree.max()),
                     fraction_N_produced_with_elastic_rate_below10=fraction(elastic<10),
                     fraction_N_produced_with_MB_occupation_above_point1=fraction(occupation>.1),
                     fraction_N_produced_with_Hartree_ratio_above1=fraction(hartree>1),
                     fraction_N_produced_below160GeV=fraction(pars['m_S_GeV']/rr<160),
                     daughter_number_integral_relative_error=float(integral/IN-1),
                     Tdark_over_m_range=[float(tt.min()),float(tt.max())],
                     rate_table_clipped_samples=int(np.sum((tt<rates.temperatures[0])|(tt>rates.temperatures[-1]))),
                     scope='Production-weighted classical closure flags, not a quantum error estimate or a finite-temperature phase-transition solution.')
    source=pars['DH']*quad(lambda r:r**3*kv(1,r),math.exp(sol.t[0]),rend,epsabs=1e-12)[0]
    branch=pars['DN']/(pars['DN']+pars['DH'])
    number_identity=2*branch*(initialI-I+source+ann_integral+self_integral)
    budget=dict(inverse_Higgs_source_integral=source,net_annihilation_integral=float(ann_integral),
                net_self_number_integral=float(self_integral),initial_scalar_I=initialI,
                predicted_sterile_IN=float(number_identity),sterile_IN=float(IN),
                relative_balance_error=float(number_identity/IN-1),
                identity='IN=2BR_N*(Iinitial-Ifinal+inverse_Higgs_source+net_annihilation+net_self_number). Elastic collisions conserve number.')
    return dict(M_keV=mass,parameters=pars,nq=nq,nangle=nangle,chemical_scale=chemical_scale,
                portal_self_exchange=portal_exchange,method=method,omega_h2=float(2.744e8*mass*1e-6*p.YCOEFF*IN),
                Y_N=float(p.YCOEFF*IN),mean_q=float(M1/IN),rms_q=float(math.sqrt(M2/IN)),
                scalar_I_final=float(I),scalar_R_final=float(R),history=history,
                solver_evaluations=sol.nfev,seed_interval=seed_interval,closure_diagnostics=diagnostics,integrated_number_budget=budget,
                minimum_sampled_scalar_I=float(np.exp(sol.y[0]).min()),
                minimum_sampled_dark_temperature=float(np.exp(sol.y[1]).min()))


def run(nq=48,nangle=20):
    rates=ThermalRates();rows=[]
    for mass in [16.,30.,100.]:
        row=solve(mass,rates,nq,nangle);rows.append(row)
        print('MOMENTS',mass,row['omega_h2'],row['mean_q'],row['rms_q'],flush=True)
    result=dict(status='CLASSICAL_INTERNAL_MB_TWO_MOMENT_TRANSPORT_NOT_FULL_KINETICS',rows=rows,
                definitions='I=2pi^2*nS/T^3; R=2pi^2*rhoS/T^4; x=ln(mS/T). Internal fS=z exp(-E/Tdark). Self reactions change I but conserve R. Free Rdot=r^2*J. Sterile zeroth/first/second comoving q moments integrated alongside.',
                sources=['https://arxiv.org/abs/2212.09759','https://arxiv.org/abs/2003.12606'],
                scope='Fixed classical broken scalar potential and RD gstar. Includes3<->2, leading portal contact+selfexchange ss<->hh and sh<->sh, s<->hh and s->NN. Internal MB kinetic-equilibrium closure imposed; initial and late closure require separate tests. No Bose factors, quantum loop amplitudes,4<->2, meanfield, thermal restoration, SM transitions or NN inverse decays. No full minimal UV completion, physical exclusion, transfer function or solved TOE.',
                input_raw_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest()for f in [TABLE,'analysis/toe_20261107_scalar_self_reactions.py','data/toe_20261107_sterile_phase_space.json']})
    (ROOT/'data/toe_20261107_coupled_scalar_moments.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    return result


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--rates',action='store_true');a.add_argument('--power',type=int,default=15);a.add_argument('--nodes',type=int,default=48);args=a.parse_args()
    if args.rates:make_rates(args.power)
    else:run(args.nodes)
