"""Round26 stable-coupling W(3,q) tower: finite extensive energy
sandwich and honest variational localization discontinuity.
No many-body exact critical point or Lorentzian 4D continuum claimed.
"""
import math,json,numpy as np
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/w33_20261009_toe26_scaled_tower_competing_vacua.json'
def calc(q,rho=.5,t0=1.,u=5.):
 v=2*(q+1)*(q*q+1);k=q+1;N=round(rho*v)
 t=t0/k;U=u/v
 # Coherent product state psi = (sqrt(a)*site0 + sqrt(1-a)*uniform)/norm.
 # Native q+1-regular W(3,q) Levi graph has no loops.
 a_grid=np.linspace(0,1,101)
 e=[]
 for a in a_grid:
  A=math.sqrt(a);B=math.sqrt(1-a)/math.sqrt(v)
  norm2=1+2*A*B
  site=(A+B)/math.sqrt(norm2)
  rest=B/math.sqrt(norm2)
  # <psi|adj|psi> = [(1-a)k + 2 sqrt(a(1-a))k/sqrt(v)] / norm2
  hopping=((1-a)*k+2*A*B*k)/norm2
  ipr=site**4+(v-1)*rest**4
  E=-t*N*hopping-U*N*(N-1)*ipr/2
  e.append(E/v)
 j=int(np.argmin(e))
 uniform=-t0*N/v-U*N*(N-1)/(2*v*v)
 localized=-U*N*(N-1)/(2*v)
 assert abs(e[0]-uniform)<1e-8
 assert abs(e[-1]-localized)<1e-8
 lower=-(t0*N/v+U*N*(N-1)/(2*v))
 upper=min(uniform,localized)
 assert lower<=min(e)+1e-10 and min(e)<=upper+1e-10
 return dict(q=q,sites=v,bosons=N,degree=k,
  scaled_t=t,scaled_U=U,
  uniform_trial_E_per_site=uniform,
  collapsed_trial_E_per_site=localized,
  min_101_family_trial_E_per_site=float(e[j]),min_trial_a=float(a_grid[j]),
  rigorous_E0_over_v_lower=lower,rigorous_E0_over_v_upper=upper,
  finite_q_variational_endpoints_gap=float(abs(uniform-localized)))
def run():
 rows=[calc(q) for q in (2,3,5,7,11,31,101)]
 for a in rows:
  print('SCALED-Q',a['q'],a['sites'],'unif',round(a['uniform_trial_E_per_site'],5),
   'loc',round(a['collapsed_trial_E_per_site'],5),'best alpha',a['min_trial_a'],flush=True)
 rho=.5;t0=1.
 branch={}
 for u in (2.,3.5,4.,4.5,6.):
  limits=(-t0*rho,-u*rho*rho/2)
  # The coherent one-site/uniform mixing has large-q energy density
  # e(a)=-t0*rho(1-a)-u*rho² a²/2, concave, so minimum at endpoints.
  vals=[-t0*rho*(1-a)-u*rho*rho*a*a/2 for a in np.linspace(0,1,1001)]
  opt=int(np.argmin(vals));branch[str(u)]=dict(
   uniform_limit=limits[0],localized_limit=limits[1],
   best_alpha_limit=float(np.linspace(0,1,1001)[opt]),
   variational_limit_energy=min(limits))
 assert branch['2.0']['best_alpha_limit']==0.0 and branch['6.0']['best_alpha_limit']==1.0
 res=dict(status='PASS',
  family='Levi incidence graph W(3,q), v=2(q+1)(q²+1), degree k=q+1',
  fixed_density_rho=rho,scaled_hopping_t0=1.,example_scaled_coupling_u=5.,
  suggested_scaling='t(q)=t0/(q+1); U(q)=u/[2(q+1)(q²+1)]',
  q_examples=rows,variational_scan_across_u=branch,
  thermodynamic_exact_bounds='For N/v->rho, t=t0/k, U=u/v, the full many-boson ground-energy density satisfies -t0*rho-u*rho²/2 <= liminf E0/v <= limsup E0/v <= -max(t0*rho,u*rho²/2). Thus the pathology E0/v->-infinity of fixed U is removed, although a unique thermodynamic ground-energy limit is NOT established.',
  one_site_plus_uniform_coherent_trial='For psi=(sqrt(a)|site0>+sqrt(1-a)|uniform>)/norm, E_N/v -> -t0*rho(1-a)-u*rho² a²/2. It is strictly concave in a for u>0, so this restricted variational family has endpoint minimizers and a FIRST-ORDER CROSSING at u*rho=2*t0. This does not prove a phase transition in the full quantum Bose-Hubbard model.',
  remaining_physics='No true continuum limit, susceptibility divergence, Lorentzian 3+1D causal geometry, critical exponents, or finite-size exact spectrum is obtained. Coupling scaling is an explicitly free dynamical assumption.',
  prior='Round25 proved fixed-U energy density divergence and proposed this scaling; Round26 explicitly computes variational interpolation and rigourous energy density bounds without claiming the trial transition physical.')
 OUT.write_text(json.dumps(res,indent=2)+'\n')
 return res
if __name__=='__main__':run()
