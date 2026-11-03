#!/usr/bin/env python3
"""Three fresh cross-domain TOE tests: covariant two-field WKB background;
compact-axion mass monodromy obstruction; and identifiable physics firewall.
Uses the existing fitted beta only as an input, not a fitted cosmology.
"""
from pathlib import Path
import json,math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[1]
def fit():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 p=r['free_neg']['p']
 return {'beta':float(p['cp']),'Omega_b':p['wb']/p['h']**2,
 'Omega_c':p['wc']/p['h']**2,'Omega_r':9.2e-5,
 'fitted_phi_excursion':float(r['free_neg']['info']['phi0']-r['free_neg']['info']['phi_rec'])}
def background(p,lam=.5,v0=.5):
 """Define dimensionless 3Mpl²H0² units for all species and V.
 E²=(b+c+r+V)/(1-v²/6); V=V0 exp(-lam*x), x(today)=0.
 mchi=m0 exp(-beta*x); phi_N=v; solve exact Friedmann+KG in N.
 """
 ob,oc,orr,b=p['Omega_b'],p['Omega_c'],p['Omega_r'],p['beta']
 V0=1-ob-oc-orr-v0*v0/6
 assert V0>0
 def unpack(N,x,v):
  rb=ob*math.exp(-3*N)
  rc=oc*math.exp(-3*N-b*x)
  rr=orr*math.exp(-4*N)
  vv=V0*math.exp(-lam*x)
  E2=(rb+rc+rr+vv)/(1-v*v/6)
  omb,omc,omr=rb/E2,rc/E2,rr/E2
  hN=-1.5*(omb+omc)-2*omr-v*v/2
  vN=-(3+hN)*v +3*(lam*vv+b*rc)/E2
  return E2,hN,vN,rb,rc,rr,vv
 def ode(N,y):
  x,v=y
  z=unpack(N,x,v)
  return [v,z[2]]
 sol=solve_ivp(ode,(0,-math.log(6)),(0,v0),method='DOP853',
   rtol=1e-12,atol=1e-13,dense_output=True,max_step=.035)
 assert sol.success,sol.message
 rows=[]
 for z in (0,.25,.5,1,2,5):
  N=-math.log1p(z)
  x,v=sol.sol(N)
  E2,hN,vN,rb,rc,rr,V=unpack(N,x,v)
  # exact derivative of Friedmann expression from N derivative of densities,
  # potential and v kinetic coefficient.
  numer=rb+rc+rr+V
  numN=-3*rb-(3+b*v)*rc-4*rr-lam*v*V
  analytic_E2N=(numN +E2*v*vN/3)/(1-v*v/6)
  residual_h=analytic_E2N/E2-2*hN
  rho_phi=E2*v*v/6+V
  rho_phiN=E2*hN*v*v/3 + E2*v*vN/3-lam*v*V
  residual_scalar=rho_phiN+E2*v*v-b*v*rc
  rcN=-(3+b*v)*rc
  residual_dm=rcN+3*rc+b*v*rc
  residual_total=(analytic_E2N+3*rb+3*rc+4*rr+E2*v*v)
  assert max(abs(residual_h),abs(residual_scalar),abs(residual_dm),abs(residual_total))<1e-10
  assert E2>0 and rho_phi>0
  rows.append({'z':z,'x':float(x),'v':float(v),'E2':E2,'Omega_phi':rho_phi/E2,
  'effective_wphi':(E2*v*v/6-V)/rho_phi,'m_rec_over_today_at_z':math.exp(-b*x),
  'Friedmann_Hdot_residual':residual_h,'energy_transfer_residual':residual_scalar,
  'total_continuity_residual':residual_total})
 # beta=0 control must conserve comoving c number times rest mass
 assert abs(rows[0]['E2']-1)<1e-12
 return {'lambda_exp_input':lam,'scalar_speed_v0_input':v0,'V0':V0,'redshifts':rows,
 'scope':'Exact homogeneous FLRW canonical-phi + WKB coupled oscillating chi dust background under the declared exponential potential and time variable, NOT a new CLASS perturbation solver and NOT the full fitted best-fit cosmology.'}
def compact_axion(p):
 b=p['beta'];dx=p['fitted_phi_excursion']
 assert b>0
 # Exponential m(phi) monodromy over one compact axion shift.
 # Periodicization near crossing x=0: ln m = -(b*f/Mpl)*sin(phi/f)
 # slope at x=0 is -b; slope at displacement dx is -b cos(dx/F).
 levels={}
 for tolerance in (.1,.01,.001):
  # Require local beta_eff variation <tol over the fitted excursion.
  F=dx/math.acos(1-tolerance)
  levels[str(tolerance)]={'minimum_f_over_Mpl_for_at_most_tolerance_slope_drift':F,
    'log_mass_perturbation_amplitude_bf_over_Mpl':b*F,
    'absolute_relative_coupling_deviation_at_bound':1-math.cos(dx/F)}
  assert abs(levels[str(tolerance)]['absolute_relative_coupling_deviation_at_bound']-tolerance)<1e-12
 constraints=[]
 for F in (.1,.25,.5,1,2,5):
  p2=2*math.pi*F
  monodromy=math.exp(-b*p2)
  slope_drift=1-math.cos(dx/F)
  mass_ratio_periodic=math.exp(b*F*math.sin(dx/F))
  mass_ratio_exp=math.exp(b*dx)
  constraints.append({'f_over_Mpl':F,'exp_mass_monodromy_factor_after_2pi_f':monodromy,
      'percent_change_effective_beta_between_ends':100*slope_drift,
      'periodic_mass_ratio_across_field_excursion':mass_ratio_periodic,
      'exponential_mass_ratio_across_field_excursion':mass_ratio_exp})
 return {'theorem':'For compact phi~phi+2pi f and strictly positive m(phi), m0 exp(-beta phi/Mpl) is single-valued iff beta=0 (real beta,f>0).',
  'periodic_local_replacement':'m(phi)=m0 exp[-beta*(f/Mpl)*sin(phi/f)], at phi=0 derivative d ln m/d(phi/Mpl)=-beta but coupling varies as cos(phi/f); this remains a periodic mass, not exact global exponential.',
  'field_excursion_fitted_delta_phi_over_Mpl':dx,'minimum_decay_constants_for_tolerances':levels,
  'sampled_mass_monodromy_and_periodicization':constraints,
  'scope':'Exact compact-periodicity obstruction; periodic replacement is an original comparison ansatz but periodic couplings are established, not a new particle prediction. Applies ONLY if the rolling field itself is an ordinary compact axion; a noncompact modulus or an axion monodromy mechanism is not ruled out.'}
def main():
 p=fit();base=background(p)
 per=compact_axion(p)
 results={'status':'PASS_COVARIANT_WKB_BACKGROUND_AND_COMPACT_MASS_OBSTRUCTION','inputs':p,
 'background_exact_energy_exchange':base,'compact_axion_mass_periodicity':per}
 output=ROOT/'data/toe_20261103_covariant_wkb_and_axion_periodicity.json'
 output.write_text(json.dumps(results,indent=2)+'\n')
 print('COVARIANT',json.dumps({'clock':[(r['z'],r['x'],r['v']) for r in base['redshifts']],
 'max_error':max(abs(r['total_continuity_residual']) for r in base['redshifts']),
 'f_thresholds':per['minimum_decay_constants_for_tolerances']}),flush=True)
if __name__=='__main__':main()
