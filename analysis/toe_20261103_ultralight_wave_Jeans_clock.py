#!/usr/bin/env python3
"""Wave Jeans crossing: convert the previously fitted fading scalar mass
history to a physically dimensioned effective-fluid pressure benchmark.

Not a Boltzmann solver or a Lyman-alpha limit.
"""
from pathlib import Path
import math,json
ROOT=Path(__file__).resolve().parents[1]
c=299792458.
Mpc=3.085677581491367e22
hbar_eVs=6.582119569e-16
def main():
 r=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
 p=r['free_neg']['p'];info=r['free_neg']['info']
 h=p['h'];H0=100*h*1000/Mpc
 Om=p['wc']/h**2
 beta=float(p['cp'])
 mass_now=1e-20
 mrec_over_today=math.exp(beta*(info['phi0']-info['phi_rec']))
 assert 1.0<mrec_over_today<1.1
 mass_Hz=mass_now/hbar_eVs
 # k_J^4 = 16 pi G rho_chi(a) (mchi(a)/hbar)^2 a^4 / c^4
 # rho_chi(a)=rho_chi0 a^-3 m(a)/m0 =>
 # k_J(a)=k_J(0) a^(1/4) [m(a)/m0]^(3/4)
 today=(6*Om*H0**2*mass_Hz**2)**.25 /c *Mpc/h
 a_rec=1/1101
 rec=today*a_rec**.25*mrec_over_today**.75
 epochs=[{'epoch':'z0','a':1.,'mass_ratio':1.,'kJeans_h_Mpc':today},
         {'epoch':'z1090','a':a_rec,'mass_ratio':mrec_over_today,'kJeans_h_Mpc':rec}]
 for e in epochs:
  e['checks_k_over_kJeans_to_fourth']={str(k):(k/e['kJeans_h_Mpc'])**4 for k in (.05,.2,1,10,100,300,500,1000)}
 assert epochs[0]['checks_k_over_kJeans_to_fourth']['1']<1e-8
 assert epochs[1]['checks_k_over_kJeans_to_fourth']['500']>1
 assert epochs[0]['checks_k_over_kJeans_to_fourth']['500']<1
 # ratio mass variation control: without fading at same a
 varying_mass_Jeans_fractional_shift_at_recomb=mrec_over_today**.75-1
 out={'status':'PASS_DIMENSIONFUL_ULTRALIGHT_JEANS_CROSSING_AND_MASS_HISTORY',
  'input_fit':'analysis/toe_uv/class_fit_dovekie.json:free_neg',
  'mass_today_eV_illustrative':mass_now,'Omega_chi_today':Om,'H0_s_inv':H0,
  'm_recombination_over_today_from_actual_fitted_field_excursion':mrec_over_today,
  'table':epochs,
  'Jeans_fractional_shift_at_recombination_due_only_to_mass_variation':varying_mass_Jeans_fractional_shift_at_recomb,
  'formula':'Effective nonrelativistic ultralight scalar pressure omega_Q²= hbar² k_comoving^4/(4m_phys²a^4) and gravitational driving 4piG rho_chi; kJeans=[16piG rho_chi (mchi/hbar)^2 a^4/c^4]^(1/4), kJeans(a)=kJeans0*a^(1/4)*(m(a)/m0)^(3/4) when comoving particle number conserved.',
  'scope':'Linear Newtonian pressure-versus-self-gravity COMPARISON using a frozen mass input and fitted CLASS field excursion endpoints, NOT an accurate ultralight perturbation treatment, Boltzmann hierarchy or data-driven axion mass posterior. WKB after oscillation is assumed; at radiation era full transfer must be computed. Normalization uses the frozen cosmology and a separate supplied ultralight mass, so derived kJeans does not imply evidence for FDM.',
  'prior':['https://doi.org/10.1103/PhysRevD.105.123529','https://doi.org/10.1103/fy1y-rjst']}
 (ROOT/'data/toe_20261103_ultralight_wave_Jeans_clock.json').write_text(json.dumps(out,indent=2)+'\n')
 print('JEANS',json.dumps({'kJ0':today,'kJrec':rec,'mrec_m0':mrec_over_today,
 'kJ_fading_ratio_rec':varying_mass_Jeans_fractional_shift_at_recomb}),flush=True)
if __name__=='__main__':main()
