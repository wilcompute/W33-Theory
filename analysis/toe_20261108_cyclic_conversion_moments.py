"""Closed symmetric-pair conversions with a declared vector contact action.

Exact classical relativistic thermal kernel and common-temperature MB moments.
Initial abundance, background expansion and frozen scalar phase are supplied.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import PchipInterpolator
from scipy.special import kve as scipy_kve,roots_genlaguerre

ROOT=Path(__file__).resolve().parents[1]
EPS=.05314971931113116
M_GEV=1.6e-5
MP_GEV=2.435e18


def kve(n,z):
    """Scaled K_n with standard asymptotic expansion beyond SciPy's range."""
    z=np.asarray(z);term=np.ones_like(z,dtype=float);series=term.copy()
    for j in range(1,7):
        term=term*(4*n*n-(2*j-1)**2)/(j*8*z)
        series+=term
    asym=np.sqrt(math.pi/(2*z))*series
    return np.where(z>1e4,asym,scipy_kve(n,z))


def equilibrium(m,T):
    z=m/T;logn=2*np.log(m)+np.log(kve(2,z))-z
    w=np.exp(logn-logn.max())
    return w/w.sum()


def energies_and_capacity(m,T):
    z=m/T;r=kve(1,z)/kve(2,z)
    E=m*r+3*T;C=3+z*z*(1-r*r)-3*z*r
    # Avoid cancellation of O(z^2) terms in the cold-gas heat capacity.
    cold=z>1000;u=T/m[cold]
    E[cold]=m[cold]+1.5*T+1.875*T*u-1.875*T*u*u+1.0546875*T*u**3+1.40625*T*u**4
    C[cold]=1.5+3.75*u-5.625*u*u+4.21875*u**3+7.03125*u**4
    return E,C


def mean_speed(m,T):
    # Exact classical isotropic integral of p/E, with c=1.
    return 2*T*(m+T)/(m*m*kve(2,m/T))


def cross_section_contact(s,mi,mj):
    """sigma/G^2, spin-averaged Dirac vector current, i != j."""
    if s<=4*max(mi,mj)**2:return 0.
    return (s+2*mi*mi)*(s+2*mj*mj)/(12*math.pi*s)*math.sqrt((s-4*mj*mj)/(s-4*mi*mi))


def downward_rates(mh,ml,T,order=96):
    """<sigma v>/(G^2 M^2), all masses and T in units M.

    s integral -> sqrt(s)=2mh+Tt. Generalized Laguerre weight t^.5 exp(-t)
    removes the initial-pair square-root threshold. Spin factors cancel.
    """
    nodes,weights=roots_genlaguerre(order,.5)
    E=2*mh[:,None]+T*nodes
    s=E*E
    # Factor threshold differences before evaluation, avoiding cold subtraction.
    first=T*nodes*(4*mh[:,None]+T*nodes)
    second=(2*(mh-ml)[:,None]+T*nodes)*(E+2*ml[:,None])
    root=np.sqrt(np.maximum(0,first*second))
    integrand=(s+2*mh[:,None]**2)*(s+2*ml[:,None]**2)*root*kve(1,E/T)/np.sqrt(nodes)
    integral=integrand@weights
    return integral/(48*math.pi*mh**4*kve(2,mh/T)**2)


class Rates:
    def __init__(self,m,order=96,points=160):
        self.m=np.asarray(m);pairs=[(i,j)for i in range(len(m))for j in range(i)if m[i]!=m[j]]
        self.hi=np.array([i if m[i]>m[j]else j for i,j in pairs])
        self.lo=np.array([j if m[i]>m[j]else i for i,j in pairs])
        self.mh=m[self.hi];self.ml=m[self.lo]
        self.temperatures=np.geomspace(1e-13,.3,points)
        table=np.array([downward_rates(self.mh,self.ml,T,order)for T in self.temperatures])
        assert np.all(table>0)
        self.interpolate=PchipInterpolator(np.log(self.temperatures),np.log(table),axis=0)
        self.order=order;self.points=points

    def coefficients(self,T):
        if not self.temperatures[0]<=T<=self.temperatures[-1]:
            raise ValueError('Temperature outside verified kernel table')
        down=np.exp(self.interpolate(math.log(T)))
        # Ratio neq_hi^2/neq_lo^2, with common fugacity cancelling exactly.
        logratio=2*(2*np.log(self.mh/self.ml)+np.log(kve(2,self.mh/T)/kve(2,self.ml/T))-(self.mh-self.ml)/T)
        return down,np.exp(logratio)

    def derivative(self,eta,T,prefactor):
        down,ratio=self.coefficients(T)
        flux=prefactor*down*(eta[self.hi]**2-ratio*eta[self.lo]**2)
        out=np.zeros_like(eta);np.add.at(out,self.hi,-flux);np.add.at(out,self.lo,flux)
        return out


def background():
    # CP-symmetric particles and antiparticles each carry half the supplied Y.
    tau0=.1;xi=.1;Ypart=.00137;gR=3.36;gs=3.91;mA=.01
    Tgamma=tau0*M_GEV/xi
    n0=Ypart*2*math.pi**2/45*gs*Tgamma**3
    Hrad0=math.sqrt(math.pi**2*gR/90)*Tgamma**2/MP_GEV
    return dict(tau0=tau0,xi=xi,Y_particles=Ypart,g_rho=gR,g_s=gs,mA_GeV=mA,
                Tgamma0_GeV=Tgamma,n_particles0_GeV3=n0,H_radiation0_GeV=Hrad0,
                equality_Tgamma_GeV=.8e-9)


def response(m,eta,nodes=2048):
    # Same frozen-population observable as the preceding paper/control packet.
    phases=2*math.pi*np.arange(len(m))/len(m)
    theta=2*math.pi*np.arange(nodes)/nodes
    masses=np.sqrt(1+EPS*EPS+2*EPS*np.cos(theta[:,None]+phases))
    slopes=-EPS*np.sin(theta[:,None]+phases)/masses
    mean=masses@eta
    return dict(fractional_rms=float(np.std(mean)/np.mean(mean)),
                max_abs_beta_f_equals_MP=float(np.max(abs((slopes@eta)/mean))))


def solve(strength=100.,method='Radau',order=96,points=160,heating=True,initial='uniform',end=12.,rates=None):
    N=24;theta_i=.37;m=np.sqrt(1+EPS*EPS+2*EPS*np.cos(theta_i+2*np.pi*np.arange(N)/N))
    if rates is None:rates=Rates(m,order,points)
    bg=background();eta0=np.ones(N)/N if initial=='uniform'else equilibrium(m,bg['tau0'])
    work0=0.;z0=np.r_[eta0,math.log(bg['tau0']),work0]
    def rhs(loga,z):
        eta=z[:N];T=math.exp(z[N]);E,C=energies_and_capacity(m,T)
        matter=bg['equality_Tgamma_GeV']/bg['Tgamma0_GeV']*math.exp(loga)
        pref=strength*math.exp(-loga)/math.sqrt(1+matter)
        deta=rates.derivative(eta,T,pref)
        Cv=float(eta@C)
        # Subtract common rest energy to avoid cancellation; sum deta=0.
        exchange=float((E-E[0])@deta)if heating else 0.
        dT=(-3*T-exchange)/Cv
        return np.r_[deta,dT/T,3*T]
    times=np.linspace(0,end,1201)
    sol=solve_ivp(rhs,(0,end),z0,method=method,rtol=2e-8,atol=2e-12,t_eval=times)
    if not sol.success:raise RuntimeError(sol.message)
    eta=sol.y[:N];temps=np.exp(sol.y[N]);final=eta[:,-1]
    energy=[];capacity=[];occupation=[]
    for j,T in enumerate(temps):
        E,C=energies_and_capacity(m,T);energy.append(float(eta[:,j]@E));capacity.append(float(eta[:,j]@C))
        n=bg['n_particles0_GeV3']*math.exp(-3*times[j])*eta[:,j]
        mi=m*M_GEV;Td=T*M_GEV
        f0=n*2*math.pi**2/(2*mi**2*Td*kve(2,mi/Td))
        occupation.append(float(max(f0)))
    energy=np.array(energy);conserved=energy+sol.y[N+1]
    finalT=temps[-1];eq=equilibrium(m,finalT)
    down,_=rates.coefficients(finalT)
    gD=(strength/(bg['n_particles0_GeV3']/bg['H_radiation0_GeV'])*bg['mA_GeV']**4/M_GEV**2)**.25 if strength else 0.
    result=dict(strength=strength,method=method,heating=heating,initial=initial,background=bg,
                gD_for_supplied_mediator=gD,contact_coefficient_GeV_minus2=gD*gD/bg['mA_GeV']**2,
                initial_phase=theta_i,masses_over_M=m.tolist(),final_populations=final.tolist(),
                final_temperature_over_M=float(finalT),initial_temperature_over_M=bg['tau0'],
                final_mean_speed_over_c=float(final@mean_speed(m,finalT)),
                final_Tgamma_eV=bg['Tgamma0_GeV']*1e9*math.exp(-end),
                max_temperature_over_M=float(max(temps)),min_population=float(eta.min()),
                maximum_number_fraction_error=float(max(abs(eta.sum(axis=0)-1))),
                maximum_first_law_absolute_residual=float(max(abs(conserved-conserved[0]))),
                maximum_MB_zero_momentum_occupation=max(occupation),minimum_heat_capacity=float(min(capacity)),
                final_total_variation_from_instantaneous_equilibrium=float(.5*sum(abs(final-eq))),
                final_pair_kernel_prefactor_ceiling=float(strength*math.exp(-end)/math.sqrt(1+bg['equality_Tgamma_GeV']/bg['Tgamma0_GeV']*math.exp(end))*max(down)),
                final_response=response(m,final),evaluations=int(sol.nfev),rate_table=dict(laguerre_order=rates.order,temperature_points=rates.points),
                history=[dict(log_a=float(times[j]),temperature_over_M=float(temps[j]),mean_energy_over_M=float(energy[j]),first_fourier_population_abs=float(abs(eta[:,j]@np.exp(2j*np.pi*np.arange(N)/N))))for j in range(0,len(times),50)],
                scope='Common kinetic temperature and classical dilute MB distributions assumed; kinetic-equilibrium collision hierarchy not solved. Scalar phase frozen throughout formation. Fixed total initial abundance, supplied radiation+matter background; no abundance prediction, scalar/metric perturbations, full portals or UV completion. Heating-off row is an intentionally nonconserving diagnostic, not a physical closed-gas solution.')
    return result


def build():
    m=np.sqrt(1+EPS*EPS+2*EPS*np.cos(.37+2*np.pi*np.arange(24)/24));rates=Rates(m)
    rows=[solve(s,rates=rates)for s in [0.,1.,10.,100.,1000.]]
    rows.append(solve(100.,heating=False,rates=rates))
    out=dict(status='DECLARED_CYCLIC_VECTOR_CONTACT_CONVERSIONS_WITH_COUPLED_MB_ENERGY_NOT_PHYSICAL_COMPLETION',
             rows=rows,thermal_kernel='sigma_ij(s)/G^2=(s+2mi^2)(s+2mj^2)/(12pi*s)*sqrt((s-4mj^2)/(s-4mi^2)); gamma_ij symmetric under i<->j; thermal density includes spin2 particle and spin2 antiparticle.',
             equations='deta_hi/dloga=-pref*Kdown*(eta_hi^2-(neq_hi/neq_lo)^2*eta_lo^2), deta_lo opposite. dT/dloga=(-3T-sum_i E_i*deta_i/dloga)/sum_i eta_i*C_i; n_particles proportional a^-3. T and masses in units M. Common rest energy subtracted using sum deta=0.',
             density_convention='n_i counts particles only; antiparticles equal. Total physical density is2*n_particles. Pair conversion removes one particle and one antiparticle and produces one of each. No missing factor2 in the particle-fraction equation.',
             ownership='Published cyclic-partner population mechanism2610.30253; standard detailed-balance Boltzmann and MB moment methods. Prior scalar moment packet6fcbfcb supplies a separate physical sector, not these fermions.')
    (ROOT/'data/toe_20261108_cyclic_conversion_moments.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('CONVERSION_ROWS',[(r['strength'],r['heating'],r['final_temperature_over_M'],r['final_response'],r['maximum_first_law_absolute_residual'])for r in rows],flush=True)
    return out


if __name__=='__main__':build()
