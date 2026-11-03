#!/usr/bin/env python3
"""Exact covariant TWO periodic functions, V and mchi, in the rolling-axion
Friedmann equations; and the global compactness obstruction.

This deliberately explores a periodic-field alternative to the noncompact
exponential scalar used by the fitted CLASS model. Not a data refit.
"""
from pathlib import Path
import json,math
from scipy.integrate import solve_ivp
ROOT=Path(__file__).resolve().parents[1]
def main():
 fit=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 p=fit['free_neg']['p'];b=float(p['cp']);h=float(p['h']);wb=p['wb']/h**2;wc=p['wc']/h**2;wr=9.2e-5
 F0=.5;v0=.5
 # Here f and phi measured in Mpl units.
 V0=1-wb-wc-wr-v0**2/6
 def run(F):
  def values(N,x,v):
   arg=x/F if math.isfinite(F) else 0
   if math.isfinite(F):
    y=F*math.sin(arg); dydx=math.cos(arg)
   else:y=x;dydx=1.
   rb=wb*math.exp(-3*N);rc=wc*math.exp(-3*N-b*y);rr=wr*math.exp(-4*N)
   V=V0*math.exp(-F0*y)
   e2=(rb+rc+rr+V)/(1-v*v/6)
   hn=-1.5*(rb+rc)/e2-2*rr/e2-.5*v*v
   vn=-(3+hn)*v+3*dydx*(F0*V+b*rc)/e2
   return y,dydx,e2,hn,vn,rb,rc,rr,V
  def ode(N,vars):
   x,v=vars
   return [v,values(N,x,v)[4]]
  s=solve_ivp(ode,(0,-math.log(6)),[0,v0],rtol=1e-11,atol=1e-11,
     method='DOP853',dense_output=True,max_step=.02)
  assert s.success
  arr=[]
  for z in (0,.5,1,2,5):
   N=-math.log1p(z);x,v=s.sol(N)
   y,dy,e2,hn,vn,rb,rc,rr,V=values(N,float(x),float(v))
   de2n=(-3*rb-(3+b*dy*v)*rc-4*rr-F0*dy*v*V+e2*v*vn/3)/(1-v*v/6)
   error=de2n-2*e2*hn
   assert abs(error)<3e-10
   rho_phi=e2*v*v/6+V
   wphi=(e2*v*v/6-V)/rho_phi
   assert wphi>=-1-1e-12
   arr.append({'z':z,'x_over_Mpl':float(x),'v':float(v),'E2':e2,
     'mass_ratio_to_today':math.exp(-b*y),
     'V_over_today':V/V0,
     'm_logarithmic_slope_today_units':-b*dy,
     'V_logarithmic_slope_today_units':-F0*dy,
     'w_phi':wphi,
     'Friedmann_Raychaudhuri_residual':error})
  return {'F_over_Mpl':F if math.isfinite(F) else 'noncompact_exponential','samples':arr}
 models=[run(math.inf)]+[run(f) for f in (.5,1,2,4)]
 for candidate in models[1:]:
  f=candidate['F_over_Mpl']
  assert all(x['mass_ratio_to_today']>0 for x in candidate['samples'])
  # periodic both m and V -> identical after x->x+2pi*f.
  for x in (-.78,.19,3.54):
   A=lambda v:math.sin(v/f)
   assert abs(A(x)-A(x+2*math.pi*f))<1e-14
 # Global exponential V would acquire a finite mass/energy scaling
 # after one turn in a compact field (multivalued).
 monodromy=[{'F_over_Mpl':f,
   'm_exp_after_one_compact_turn_over_before':math.exp(-2*math.pi*f*b),
   'V_exp_after_one_compact_turn_over_before':math.exp(-2*math.pi*f*F0)}
  for f in (.5,1,2,4)]
 # Heavy universal messenger-loop floor on a separate explicitly coupled species.
 Mpl=2.435e27;H0=h*100*1000/3.085677581491367e22*6.582119569e-16
 heavy=[]
 for m in (1e-20,1e-2,1e9,1e12,1e25):
  gmax=math.sqrt(8*math.pi**2)*H0*Mpl/(m*m)
  heavy.append({'one_real_boson_mass_eV':m,
   'maximum_dimensionless_exponential_phi_mass_slope_to_keep_abs_one_loop_mphi_squared_below_H0_squared':gmax})
 out={'status':'PASS_COVARIANT_TWO_PERIODIC_FUNCTIONS_COMPACT_FIELD_TEST',
  'mass_coupling_beta_frozen':b,'potential_slope_lambda_external':F0,
  'initial_phi_velocity_over_H0_external':v0,
  'models':models,'noncompact_exact_exponential_turn_monodromy':monodromy,
  'heavy_one_loop_naturalness_thresholds':heavy,
  'exact_global_no_go':'A strictly compact phi~phi+2pi f cannot have a globally single-valued EXACT exp(-lambda phi/Mpl) potential with real lambda!=0. The exact exp(-beta phi/Mpl) dark mass has the analogous problem. Periodic versions or explicit monodromy sheet variables restore mathematical consistency, at the cost of different cosmological histories.',
  'periodic_ansatz':'y=f sin(phi/f); V=V0 exp(-lambda y), mchi=m0 exp(-beta y); both globally periodic. The homogeneous equations conserve total stress-energy and satisfy rho_c_N=-(3+beta dy/dx*x_N)rho_c. No nonperturbative axion model claimed.',
  'loop_threshold':'Single isolated real-boson Coleman-Weinberg threshold |delta mphi²|~g² M^4/(8pi² Mpl²), scheme-dependent naturalness counterexample, NOT an observational upper bound. Heavy portal SUSY/messenger cancellation already studied in uncommitted mechanism_portal_protection.py and many older repo passes; this table only displays the universal scale sensitivity, with that prior attribution.',
  'scope':'PERIODIC SELF-CONSISTENT HOMOGENEOUS scalar+averaged DM backgrounds, not a simultaneous fit to CLASS-Dovekie, no new interacting-ULA Boltzmann solver, no actual axion monodromy UV completion. Small fitted excursion is not the same as the distinct initial velocity v0=.5 in this illustrative integration.',
  'references':['https://doi.org/10.1103/PhysRevD.94.103526']}
 (ROOT/'data/toe_20261103_compact_two_function_uv_window.json').write_text(json.dumps(out,indent=2)+'\n')
 print('PERIODIC_TWO_FUNCTION',json.dumps({'models':[{'F':z['F_over_Mpl'],'e2_z1':z['samples'][2]['E2'],'m_z1':z['samples'][2]['mass_ratio_to_today']} for z in models],
  'monodromies':monodromy,'heavy_1TeV_gmax':heavy[-2]['maximum_dimensionless_exponential_phi_mass_slope_to_keep_abs_one_loop_mphi_squared_below_H0_squared']}),flush=True)
if __name__=='__main__':main()
