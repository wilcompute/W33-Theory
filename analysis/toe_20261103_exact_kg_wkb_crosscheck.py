#!/usr/bin/env python3
"""Independent exact Klein-Gordon vs WKB adiabatic invariant test.

A mass varying oscillator in a *given* self-consistent coupled scalar+CDM
Friedmann background. The test oscillator is a test field and does NOT
self-consistently source Einstein equations (avoids double counting CDM).
"""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.integrate import solve_ivp,quad
ROOT=Path(__file__).resolve().parents[1]
src=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
beta=float(src['free_neg']['p']['cp'])
h=src['free_neg']['p']['h'];ob=src['free_neg']['p']['wb']/h**2;oc=src['free_neg']['p']['wc']/h**2;orr=9.2e-5
lam=.5; v0=.5;V0=1-ob-oc-orr-v0*v0/6
def scalar_bg():
 def f(N,x,v):
  rb=ob*math.exp(-3*N);rc=oc*math.exp(-3*N-beta*x);rr=orr*math.exp(-4*N);V=V0*math.exp(-lam*x)
  E2=(rb+rc+rr+V)/(1-v*v/6)
  hn=-1.5*(rb+rc)/E2-2*rr/E2-v*v/2
  vn=-(3+hn)*v+3*(lam*V+beta*rc)/E2
  return E2,hn,vn
 def ode(N,y):
  x,v=y;return [v,f(N,x,v)[2]]
 N0=-math.log(2)
 bg=solve_ivp(ode,(0,N0),[0,v0],rtol=3e-12,atol=3e-12,dense_output=True,max_step=.012)
 assert bg.success
 def at(N):
  x,v=bg.sol(N);E2,hn,_=f(N,float(x),float(v))
  return float(x),float(v),E2,hn
 return N0,at
def trajectory(Q0,at,N0):
 xi,vi,E2i,hni=at(N0)
 # choose phase=0 initial, physical amplitude chi_ini=1, chi_N from WKB
 # log envelope = -3N/2+beta x/2
 def E(N):
  x,v,E2,hn=at(N)
  return x,v,E2,hn,Q0*math.exp(-beta*x)/math.sqrt(E2)
 yi=[1.,-1.5+.5*beta*vi]
 def rhs(N,y):
  chi,u=y;x,v,E2,hn,q=E(N)
  return [u,-(3+hn)*u-q*q*chi]
 maxq=Q0/max(math.sqrt(E2i),1)
 sol=solve_ivp(rhs,(N0,0),yi,method='DOP853',rtol=2e-10,atol=2e-11,
               dense_output=True,max_step=min(.006,1/(18*Q0)))
 assert sol.success,sol.message
 ns=np.linspace(N0,0,2001);vals=sol.sol(ns)
 xs=np.array([at(n)[0] for n in ns])
 E2s=np.array([at(n)[2] for n in ns])
 masses=np.exp(-beta*xs)
 # instantaneous adiabatic conserved particle-number J = e^{3N} H0 * (0.5 E2 chi_N² + 0.5 Q0² mratio² chi²)/(Q0*mratio)
 A=np.exp(3*ns)*(.5*E2s*vals[1]**2+.5*(Q0*masses)**2*vals[0]**2)/(Q0*masses)
 # Compare rolling-average over many points but for fewer than 6 oscillations it is not stable.
 j0=float(np.median(A[:101]));jend=float(np.median(A[-101:]))
 dev=float(abs(jend/j0-1))
 # A clear late-time bound on max deviation in final samples, robust to oscillatory phase.
 spread=float((np.percentile(A[-200:],95)-np.percentile(A[-200:],5))/np.median(A[-200:]))
 # Canonical Q=a^(3/2) chi has Q_ddot+[m²-1.5 Hdot-2.25H²]Q=0.
 # At finite H/m, the invariant E_Q/omega_eff corrects the naive rho/m.
 hns=np.array([at(n)[3] for n in ns])
 weff2=(Q0*masses)**2-E2s*(1.5*hns+2.25)
 assert np.all(weff2>0)
 Aq=np.exp(3*ns)*(.5*E2s*(vals[1]+1.5*vals[0])**2+
                  .5*weff2*vals[0]**2)/np.sqrt(weff2)
 jc0=float(np.median(Aq[:101]))
 jcend=float(np.median(Aq[-101:]))
 devc=abs(jcend/jc0-1)
 spreadc=float((np.percentile(Aq[-200:],95)-np.percentile(Aq[-200:],5))/np.median(Aq[-200:]))
 envelope_amp=np.exp(-1.5*(ns-N0)+.5*beta*(xs-xi))
 q_adiab=math.sqrt(E2i)/Q0
 return {'m_over_H_today':Q0,'m_over_H_early':Q0*math.exp(-beta*xi)/math.sqrt(E2i),
     'small_adiabatic_H_over_m_early':q_adiab,'integrator_steps':len(sol.t),
     'n_grid_points':len(ns),'comoving_adiabatic_number_initial_median':j0,
     'comoving_adiabatic_number_final_median':jend,
     'relative_final_to_initial_WKB_number_drift':dev,
     'late_invariant_5_to95_percent_fractional_spread':spread,
     'canonical_Q_a3over2_action_initial_median':jc0,
     'canonical_Q_a3over2_action_final_median':jcend,
     'canonical_corrected_action_relative_drift':devc,
     'canonical_corrected_late_action_5to95_fractional_spread':spreadc,
     'analytical_envelope_ratio_end_over_start':float(envelope_amp[-1]),
     'input_mass_change_end_over_start':float(masses[-1]/masses[0]),
     'terminal_x':xs[-1],'initial_x':xi}
def main():
 N0,at=scalar_bg()
 vals=[trajectory(Q,at,N0) for Q in (20,40,80,160)]
 print('WKB_ROWS',json.dumps(vals),flush=True)
 assert vals[-1]['canonical_corrected_action_relative_drift']<.005
 assert vals[-1]['canonical_corrected_late_action_5to95_fractional_spread']<.01
 assert vals[0]['canonical_corrected_late_action_5to95_fractional_spread']>vals[-1]['canonical_corrected_late_action_5to95_fractional_spread']
 out={'status':'PASS_EXACT_KLEIN_GORDON_WKB_VARYING_MASS_BENCHMARK',
  'input_beta_frozen':beta,'background':'previous self-consistent canonical-phi + coupled pressureless-CDM FLRW exponential V, lambda=.5 v0=.5, z from 1 to0, test scalar only',
  'oscillator':'linear test chi_NN +(3+dlnH/dN)chi_N+(mchi/H)^2 chi=0, mchi/H0=Q0 exp(-beta*x)',
  'adiabatic_number':'J=e^(3N)*(H² chi_N²+mchi² chi²)/(2 mchi) tends to constant in WKB; envelope chi~a^(-3/2)mchi^(-1/2)',
  'runs':vals,
  'scope':'Direct high-frequency scalar KG evolution with mass variation on a fixed self-consistent averaged FLRW background. No perturbation Boltzmann hierarchy, no radiation-era transfer, no backreaction by chi test field (separate already averaged dust sources the background), no instrument data. Not a patched CLASS ultralight implementation.',
  'literature':['https://doi.org/10.1103/PhysRevD.105.123529','https://doi.org/10.1103/fy1y-rjst']}
 (ROOT/'data/toe_20261103_exact_kg_wkb_crosscheck.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':main()
