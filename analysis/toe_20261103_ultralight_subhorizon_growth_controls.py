#!/usr/bin/env python3
"""Transparent subhorizon two-species growth/oscillating-ULA emulator.

NOT a CLASS/CAMB Boltzmann calculation, not a fit or a valid Lyman-alpha
transfer likelihood: deliberately exposes assumptions and missing forces.
Uses axion effective-fluid quantum pressure and coupled-dark fifth force.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
MPC_M=3.085677581491367e22
HBAR=6.582119569e-16
C=299792.458
EV_PER_MPC=1.973269804e-7/MPC_M
def inputs():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 c=r['free_neg'];h=c['p']['h']
 return {'h':h,'Omega_b':c['p']['wb']/h**2,'Omega_chi':c['p']['wc']/h**2,
   'Omega_rad':9.2e-5,'beta':c['p']['cp'],'Dx':c['info']['phi0']-c['info']['phi_rec'],
   'H0_eV':100*h*1000/MPC_M*HBAR,'mchi_eV':1e-20}
def state(a,p,pclock=1.,beta_on=True,quantum_on=True,k=0.1):
 """A toy background; changes in mass compensated by a separately supplied
 fixed rho_DE, which is NOT scalar-field energy-conserving dynamics."""
 ob,oc,orr=p['Omega_b'],p['Omega_chi'],p['Omega_rad']
 ode=1-ob-oc-orr
 ar=1/1101
 dx=p['Dx']; beta=p['beta'] if beta_on else 0
 x=dx*(a**pclock-1)/(1-ar**pclock)
 xn=dx*pclock*a**pclock/(1-ar**pclock)
 mm=p['mchi_eV']*math.exp(-beta*x)
 ec=oc*a**-3*math.exp(-beta*x)
 eb=ob*a**-3;er=orr*a**-4
 E2=er+eb+ec+ode
 dE2=-4*er-3*eb-(3+beta*xn)*ec
 hN=dE2/(2*E2)
 omc=ec/E2;omb=eb/E2
 H=p['H0_eV']*math.sqrt(E2)
 kk=k*p['h']*EV_PER_MPC
 pressure=kk**4/(4*a**4*mm**2*H**2) if quantum_on else 0
 # Scalar Compton range gamma ~ H0 at all redshifts is a toy local screening;
 # k in h/Mpc; for k>=.05 S~1.
 kphi=p['H0_eV']/EV_PER_MPC/p['h']*a
 screen=k*k/(k*k+kphi*kphi)
 return dict(a=a,E2=E2,hN=hN,Omegac=omc,Omegab=omb,pressure=pressure,
             fifth=2*beta**2*screen, beta=beta,x=x,xN=xn,m=mm,kJeans_h_per_Mpc=(
               (6*(ec+eb)*p['H0_eV']**2*mm**2*a**4)**.25/EV_PER_MPC/p['h']))
def integrate(p,k=0.1,beta_on=True,quantum_on=True,mchi=1e-20,pclock=1.):
 pp=dict(p,mchi_eV=mchi)
 ai=.01;Ni=math.log(ai)
 # fixed common initial adiabatic growing mode, not scale-dependent
 # radiation-era transfer function (major limitation at high k).
 y0=[ai,ai,ai,ai]
 def ode(N,y):
  z=state(math.exp(N),pp,pclock,beta_on,quantum_on,k)
  dc,vc,db,vb=y
  g=1.5*(z['Omegac']*dc+z['Omegab']*db)
  src=1.5*z['Omegac']*z['fifth']*dc
  return [vc,-(2+z['hN']-z['beta']*z['xN'])*vc+g+src-z['pressure']*dc,
          vb,-(2+z['hN'])*vb+g]
 tt=np.array([Ni,math.log(.25),math.log(.5),math.log(1/1.5),0])
 rr=solve_ivp(ode,(Ni,0),y0,t_eval=tt,rtol=2e-9,atol=3e-11,method='DOP853',max_step=.025)
 assert rr.success,(rr.message,k)
 return {str(z):{'delta_c':float(rr.y[0,j]),'growth_rate_c':float(rr.y[1,j]/rr.y[0,j]),
               'delta_b':float(rr.y[2,j]),'baryon_to_chi_bias':float(rr.y[2,j]/rr.y[0,j]),
               'growth_rate_b':float(rr.y[3,j]/rr.y[2,j])}
            for j,z in enumerate([99.,3.,1.,.5,0.])}
def main():
 p=inputs()
 regimes=[]
 for k in [.05,.2,1.,10.,100.,300.,500.]:
  coupled=integrate(p,k=k,beta_on=True,quantum_on=True)
  uncoupled=integrate(p,k=k,beta_on=False,quantum_on=True)
  pure_classic=integrate(p,k=k,beta_on=False,quantum_on=False)
  z=0.;a=coupled[str(z)];control=uncoupled[str(z)]
  regimes.append({'k_h_per_Mpc':k,'coupled':coupled,'uncoupled_ultralight':uncoupled,
                  'pressureless_uncoupled':pure_classic,
                  'z0_chi_growth_ratio_to_uncoupled_ultralight':a['delta_c']/control['delta_c'],
                  'z0_chi_growth_ratio_to_pressureless':a['delta_c']/pure_classic[str(z)]['delta_c'],
                  'z0_chi_bias':a['baryon_to_chi_bias'],
                  'z0_kJeans_h_per_Mpc':state(1,p,k=k)['kJeans_h_per_Mpc']})
 # High-pressure effect should become non-negligible at high k but negligible at k=.2.
 low=regimes[1]
 assert abs(low['uncoupled_ultralight']['0.0']['delta_c']/low['pressureless_uncoupled']['0.0']['delta_c']-1)<1e-7
 assert regimes[-1]['uncoupled_ultralight']['0.0']['delta_c']/regimes[-1]['pressureless_uncoupled']['0.0']['delta_c']<.99
 # Boundary: beta=0 and m infinite returns pressureless growth independent k.
 for k in (.1,100):
  a=integrate(p,k,beta_on=False,quantum_on=False)
  assert abs(a['0.0']['delta_c']-pure_classic['0.0']['delta_c'])<1e-8
 # Today's fitted excursion directly makes m(rec)/m(0)=~1.01493.
 ar=1/1101
 mr=state(ar,p)['m'];m0=state(1,p)['m']
 assert abs(mr/m0-math.exp(p['beta']*p['Dx']))<1e-12
 out={'status':'PASS_FIVE_MODE_SUBHORIZON_TWO_FLUID_BENCHMARK',
 'source_data':p,'results':regimes,'mass_ratio_recombination_to_today':mr/m0,
 'model':'Newtonian N=ln a ODE: chi delta_NN +(2+H_N/H-beta*x_N)delta_N+ k^4/(4a^4mchi² H²)delta=3/2*(Omega_b delta_b+Omega_chi[1+2beta² S(k)]delta_chi); baryons same equation without fifth force or quantum pressure.',
 'clock_interpolation':'phi/Mpl = Dx*(a^pclock-1)/(1-a_rec^pclock), pclock=1; fit endpoint values exact but trajectory is supplied, not best-fit CLASS scalar solution.',
 'dark_energy_background':'LCDM-like constant Omega_DE plus variable chi density. Not a covariantly conserved two-scalar Friedmann/Klein-Gordon solution; force and friction are an exploratory closure.',
 'limitations':'The large-k initial conditions omit radiation transfer/ULA suppression. The toy ODE is NOT CLASS, not a full Boltzmann code, not a real Lyman-alpha emulator or RSD/lensing likelihood, no baryon feedback, relativistic scalar perturbations or quantum correction to field x. Growth on k~100 h/Mpc not physically interpretable without its earlier transfer function.',
 'sources':['https://doi.org/10.1103/PhysRevD.105.123529','https://doi.org/10.1088/1475-7516/2026/09/051']}
 (ROOT/'data/toe_20261103_ultralight_subhorizon_growth_controls.json').write_text(json.dumps(out,indent=2)+'\n')
 print('GROWTH',json.dumps([{'k':z['k_h_per_Mpc'],'ratio':z['z0_chi_growth_ratio_to_uncoupled_ultralight'],'bias':z['z0_chi_bias'],'kJ':z['z0_kJeans_h_per_Mpc']} for z in regimes]),flush=True)
if __name__=='__main__':main()
