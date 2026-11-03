#!/usr/bin/env python3
"""An exact two-scale observable identifiability test for coupled CDM.

Purely phenomenological: background inferred log mass change D=beta*DeltaPhi
and fifth-force enhancement g(k)=2 beta² k²/(k²+mu²).
Massless case recovers beta and excursion up to a global sign, massive case
requires at least two growth scales. No real data/error covariance fitted.
"""
from pathlib import Path
import json, math
import sympy as s

ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
    p=raw['free_neg'];beta=float(p['p']['cp'])
    excursion=float(p['info']['phi0']-p['info']['phi_rec'])
    D=beta*excursion
    G=2*beta**2
    b,x=s.symbols('beta Delta',real=True)
    jac=s.Matrix([[s.diff(b*x,b),s.diff(b*x,x)],[s.diff(2*b*b,b),s.diff(2*b*b,x)]])
    det=s.factor(jac.det())
    assert det==-4*b*b

    # Massive scalar: a=1. g(k) is a Yukawa k-space fifth-force coefficient.
    mu=.03  # h/Mpc, entirely hypothetical finite-range stress-test
    k1=.05; k2=.2
    val=lambda k:2*beta*beta*k*k/(k*k+mu*mu)
    g1,g2=val(k1),val(k2)
    inv1,inv2=1/g1,1/g2
    X1,X2=1/k1**2,1/k2**2
    slope=(inv1-inv2)/(X1-X2)
    intercept=inv1-slope*X1
    recovered_beta=math.sqrt(1/(2*intercept))
    recovered_mu=math.sqrt(slope/intercept)
    recovered_excursion=D/recovered_beta
    assert abs(recovered_beta/beta-1)<1e-12
    assert abs(recovered_mu/mu-1)<1e-12
    assert abs(recovered_excursion-excursion)<1e-12
    # For a massless scalar, one k suffices; for unknown mu, one k does not.
    sample=[
     {'k_h_per_Mpc':k,'g_eff_minus_1':val(k),
      'G_eff_over_G':1+val(k),
      'suppression_relative_to_massless':val(k)/G}
     for k in (k1,k2)
    ]
    absolute_10_percent_beta_fractional_precision_on_G=0.2*G
    out={'status':'PASS_EXACT_TWO_OBSERVABLES_AND_TWO_SCALES_IDENTIFIABILITY',
         'beta_source':'analysis/toe_uv/class_fit_dovekie.json free_neg.p.cp',
         'fit_beta':beta,'fit_scalar_excursion_today_minus_recombination_Mpl':excursion,
         'mass_log_ratio_recombination_over_today':D,
         'mass_ratio_recombination_over_today':math.exp(D),
         'massless_fifth_force_enhancement_over_newton':G,
         'jacobian_map':'(beta,DeltaPhi)->(D=beta*DeltaPhi,g=2*beta²)',
         'exact_jacobian_determinant':str(det),
         'inversion_massless':{'beta_abs':math.sqrt(G/2),'DeltaPhi_abs':abs(D)/math.sqrt(G/2),
         'degeneracy':'Simultaneous sign flip (beta, DeltaPhi)->(-beta,-DeltaPhi) leaves these two observables invariant'},
         'one_scale_massive_underdetermination':'If scalar has unknown Compton scale mu, one g(k) gives one equation in (beta,mu), even when D is known. Three unknowns beta,DeltaPhi,mu but only two observables.',
         'two_scale_massive_yukawa_control':{'hypothetical_mu_h_per_Mpc':mu,
            'k_samples':sample,'inverse_growth_identity':'1/g(k)=1/(2 beta²)+mu²/(2 beta² k²)',
            'recovered_beta':recovered_beta,'recovered_mu':recovered_mu,
            'recovered_excursion':recovered_excursion},
         'absolute_G_precision_needed_for_10percent_beta_measurement_rough_linear_1sigma':absolute_10_percent_beta_fractional_precision_on_G,
         'scope':'This is an *identifiability and precision-target theorem* under linear unscreened Yukawa growth, not a new observational fit. The finite range mu=0.03 h/Mpc is a toy example; an ordinary rolling quintessence field with mphi~H0 is nearly massless on these subhorizon scales. Nonlinear screening, baryonic bias and relativistic observations can spoil this simple inversion.',
         'literature':['Amendola PhysRevD69 103524 (2004)','Yang et al Eur Phys J C 86 1115 (2026)']}
    (ROOT/'data/toe_20261103_dark_sector_observable_identifiability.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('OBSERVABLE_MAP',json.dumps({'beta':beta,'D':D,'G':G,'jacobian_det':str(det),
      'two_scales':sample,'reconstruction_error':max(abs(recovered_beta-beta),abs(recovered_mu-mu))}),flush=True)
    return out
if __name__=='__main__':main()
