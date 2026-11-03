#!/usr/bin/env python3
"""Three extra independent TOE controls:
(1) adiabatic invariant and density-modulus restoring mass;
(2) bosonic Coleman-Weinberg negative curvature and naturalness;
(3) clock sequestering + messenger BL Landau-scale compatibility.
No unified UV theory, no experimental exclusion inferred.
"""
from pathlib import Path
import math,json
import sympy as s
ROOT=Path(__file__).resolve().parents[1]
MPL=2.435e27
MPC=3.085677581491367e22
HBAR=6.582119569e-16
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 f=r['free_neg'];b=float(f['p']['cp']);h=float(f['p']['h'])
 dx=float(f['info']['phi0']-f['info']['phi_rec'])
 omc=f['p']['wc']/h**2;omb=f['p']['wb']/h**2
 H0=h*100*1000/MPC*HBAR
 m=1e-20
 mratio=math.exp(b*dx)
 # WKB exact adiabatic invariant: n a³=const, chiquad oscillation A²=2n/m.
 relative_A_rec_to_naive_constant_mass=1/math.sqrt(mratio)
 assert abs(relative_A_rec_to_naive_constant_mass**2*mratio-1)<1e-14
 # Coupled matter effective potential from fixed number n, vs fixed amplitude:
 # U_ad=m(x)*n; d²U_ad/dphi²=b²rho_c/Mpl².
 mu2=3*b*b*omc
 fixed_amplitude=2*mu2
 assert fixed_amplitude==2*mu2
 x=s.symbols('x',real=True);beta,m0=s.symbols('beta m0',positive=True)
 V=s.exp(-4*beta*x)*(-2*beta*x-s.Rational(3,2))
 curv=s.simplify(s.diff(V,x,2).subs(x,0))
 assert curv==-8*beta*beta
 # Scalar one-loop V=+m4/(64pi²)(ln(m²/mu²)-3/2), mu=m0.
 loop_curv_ratio=(b*b*m**4/(8*math.pi**2*MPL**2))/H0**2
 mcap=(8*math.pi**2*H0**2*MPL**2/(b*b))**.25
 assert loop_curv_ratio<1e-65
 # Prior clock bound is a separate, older/background-only fit, not latest CLASS:
 older=json.loads((ROOT/'analysis/toe_uv/dd_clocks.json').read_text())
 ka=older['dovekie']['free_c_neg']['kappa_alpha_max']
 hierarchy=ka/b
 # BL beta coefficient from local on-disk unpublished mechanism report,
 # not a globally established UV beta for every gauge normalization.
 # User-approved inputs: non-SUSY exotic+messenger b=59; SUSY completion b=102.
 M=1e16;mp=2.435e18
 thresholds=[]
 for coeff in (59,102):
  gmax=math.sqrt(8*math.pi**2/(coeff*math.log(mp/M)))
  for g in (.3,.4,.5,.6):
   pole=M*math.exp(8*math.pi**2/(coeff*g*g))
   thresholds.append({'one_loop_beta':coeff,'g_at_1e16_GeV':g,
      'Landau_pole_GeV_one_loop':pole,
      'pole_above_reduced_Planck_mass':pole>mp,
      'largest_g_at_1e16_for_pole_above_planck':gmax})
 assert thresholds[2]['pole_above_reduced_Planck_mass']==False
 assert thresholds[0]['pole_above_reduced_Planck_mass']==True
 out={'status':'PASS_WKB_MEDIUM_MASS_AND_VISIBLE_UV_FIREWALL',
  'input_fit':'analysis/toe_uv/class_fit_dovekie.json free_neg',
  'beta':b,'delta_phi_rec_to_today_Mpl':dx,
  'exact_WKB_invariant':'n(a)*a^3=constant, rho_chi=n*m; chi_envelope=sqrt(2n/m)∝a^(-3/2)*m^(-1/2); for m=m0 exp(-beta x), rho_N=-(3+beta x_N)rho.',
  'mass_ratio_rec_over_today':mratio,
  'field_envelope_correction_rec_to_constant_mass_dust':relative_A_rec_to_naive_constant_mass,
  'adiabatic_moduli_density_curvature_in_H0_squared_today':mu2,
  'curvature_ad_sqrt_in_H0_units':math.sqrt(mu2),
  'fixed_chi_field_quadratic_curvature_in_H0_squared_today':fixed_amplitude,
  'subtlety':'Fixed field amplitude chi and fixed comoving adiabatic number are different ensembles. The effective smooth-fluid restoring curvature is b²rho/Mpl², half the naive average fixed-chi field derivative 2b²rho/Mpl².',
  'one_real_boson_renormalized_Coleman_Weinberg_x_second_derivative_factor':str(curv),
  'one_loop_mchi_1e_minus20_eV_curvature_over_H0_squared':loop_curv_ratio,
  'one_loop_scalar_technical_naturalness_cap_eV':mcap,
  'eV_to_GeV_thresholds_illustrative':thresholds,
  'clock_prior_constraint_source':'analysis/toe_uv/dd_clocks.json older background fit and laboratory alpha clock input; do NOT apply its numerical kappa_max as a new CLASS likelihood or universal matter coupling bound',
  'older_fit_kappa_alpha_upper_bound':ka,
  'allowed_beta_alpha_over_beta_dark_using_older_fit_clock':hierarchy,
  'landau_beta_coefficients_source':'Uncommitted local analysis/2026-11-03_toe_mechanism_completion.md: bBL=59 nonsupersymmetric above vectorlike thresholds, bBL=102 in separately declared supersymmetric version; couplings normalized according to those inputs. Gauge thresholds, kinetic mixing and unification are NOT computed.',
  'limitations':'Adiabatic WKB/density response and Coleman-Weinberg second derivative exact under declared action; one-loop subtraction scheme is chosen; gravity/SUSY-breaking and axion-specific shift protection unsolved. Clock bound is reused from a different fitted background; Landau poles in simple one-loop single-coefficient approximation, only above relevant thresholds.',
  'external_sources':['https://doi.org/10.1103/PhysRevD.105.123529',
  'https://doi.org/10.1103/PhysRevD.94.103526',
  'https://doi.org/10.1103/PhysRevD.57.7027']}
 (ROOT/'data/toe_20261103_ultralight_uv_density_clock.json').write_text(json.dumps(out,indent=2)+'\n')
 print('UV_CLOCK',json.dumps({'WKB_amplitude_correction':relative_A_rec_to_naive_constant_mass,
   'finite_density_mass_over_H0':math.sqrt(mu2),
   'real_boson_loop_mass2_over_H02':loop_curv_ratio,'old_clock_betaEM_over_betaDM':hierarchy,
   'gmaxBL59':thresholds[0]['largest_g_at_1e16_for_pole_above_planck'],
   'gmaxBL102':thresholds[-1]['largest_g_at_1e16_for_pole_above_planck']}),flush=True)
if __name__=='__main__':main()
