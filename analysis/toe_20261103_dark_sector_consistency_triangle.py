#!/usr/bin/env python3
"""Independent falsifier triangle: coupled-DE background reconstruction,
phiMDE baryon-slip control, and ultralight-boson UV/structure window.

Uses *frozen* CLASS+Dovekie parameters from b5b4db003 and publications.
Neither the exact constant-clock reconstruction nor the phiMDE toy is an
actual re-fit to DESI. All physical assumptions are exported to JSON.
"""
from __future__ import annotations
from pathlib import Path
import json, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
MPC_M=3.085677581491367e22
HBAR_EV_S=6.582119569e-16
MPL_EV=2.435e27
EV_TO_MPC_INV=5.067730716e6*MPC_M
LYA_BOUND_2026_EV=1.9e-21

def get_inputs():
    raw=json.loads((ROOT/'analysis/toe_uv/class_fit_dovekie.json').read_text())
    cpl=raw['CPL']['p']; fading=raw['free_neg']
    h=float(cpl['h'])
    ob=float(cpl['wb'])/h**2
    oc=float(cpl['wc'])/h**2
    orad=9.2e-5 # separately stated approximate radiation density
    return dict(omega_b=ob,omega_c=oc,omega_r=orad,
        omega_DE=1-ob-oc-orad,beta=float(fading['p']['cp']),
        w0=float(cpl['w0']),wa=float(cpl['wa']),
        h_fading=float(fading['p']['h']),
        phi_today_fading=float(fading['info']['phi0']),
        phi_rec_fading=float(fading['info']['phi_rec']),
        fit_delta_chi2_vs_LCDM=float(fading['chi2']-raw['LCDM']['chi2']),
        source='analysis/toe_uv/class_fit_dovekie.json (full Planck plik-lite + DESI DR2 + DES-Dovekie; best fits only)')

def exact_clock(p,s,z):
    """Reconstructed scalar potential for x(N)=s*N and m=m0 exp(-beta*x).
    No approximation: Friedmann and Raychaudhuri determine E2(N) exactly.
    x is phi/Mpl, N=ln a, H0=1, densities normalized to Mpl²H0².
    """
    N=-math.log1p(z); b=p['omega_b'];c=p['omega_c'];r=p['omega_r'];beta=p['beta']
    sb=3*b/(3-s*s);sc=3*c/(3+beta*s-s*s);sr=4*r/(4-s*s)
    C=1-sb-sc-sr
    eA=C*math.exp(-s*s*N);eb=sb*math.exp(-3*N)
    ec=sc*math.exp(-(3+beta*s)*N);er=sr*math.exp(-4*N)
    E2=eA+eb+ec+er
    dE2=-s*s*eA-3*eb-(3+beta*s)*ec-4*er
    rhob=3*b*math.exp(-3*N)
    rhoc=3*c*math.exp(-(3+beta*s)*N)
    rhor=3*r*math.exp(-4*N)
    rhoc_ref=3*c*math.exp(-3*N)
    rhophi=3*E2-rhob-rhoc-rhor
    kinetic=.5*E2*s*s
    V=rhophi-kinetic
    dV=(3-.5*s*s)*dE2+3*rhob+(3+beta*s)*rhoc+4*rhor
    rhoeff=3*E2-rhob-rhoc_ref-rhor
    one_plus_weff=(E2*s*s+rhoc-rhoc_ref)/rhoeff
    weff=-1+one_plus_weff
    wphi=-1+E2*s*s/rhophi
    residual_c=(3+beta*s)*rhoc+(-(3+beta*s)*rhoc)
    residual_scalar=3*s*s*E2 -beta*s*rhoc - (-3*dE2-3*rhob-(3+beta*s)*rhoc-4*rhor)
    # d rho_phi/dN = -3 H² s² + beta*s*rho_c.
    # RHS from differentiated Friedmann:
    rhophi_prime=3*dE2+3*rhob+(3+beta*s)*rhoc+4*rhor
    residual_phi=rhophi_prime+3*E2*s*s-beta*s*rhoc
    kg_residual=s*(3+.5*dE2/E2)+dV/(s*E2)-beta*rhoc/E2
    return dict(z=z,N=N,E2=E2,Eprime2=dE2,rhoc=rhoc,
        rhoc_standard=rhoc_ref,rhophi=rhophi,eff_dark_density=rhoeff,
        kinetic_density=kinetic,potential_density=V,wphi=wphi,weff=weff,
        kg_residual=kg_residual,continuity_residual=residual_phi,
        mass_ratio_to_today=math.exp(-beta*s*N))

def constant_clock_test(p):
    w0=p['w0'];ode=p['omega_DE'];wa=p['wa'];beta=p['beta']
    s_abs=math.sqrt(3*ode*(1+w0))
    assert s_abs>0 and s_abs<1
    results=[]
    for s in [s_abs,-s_abs]:
        samples=[exact_clock(p,s,z) for z in (0.,.25,.5,1.,2.)]
        assert all(r['E2']>0 and r['rhophi']>0 and r['potential_density']>0 and r['eff_dark_density']>0 for r in samples)
        assert max(abs(x['kg_residual']) for x in samples)<1e-11
        assert max(abs(x['continuity_residual']) for x in samples)<1e-11
        assert abs(samples[0]['weff']-w0)<1e-12
        # w_a=-d w/d(ln a) at N=0; derived analytically.
        q=s*s;Q=3*ode
        wa_pred=(q*(3*(p['omega_b']+p['omega_c'])+4*p['omega_r']+q)+beta*s*3*p['omega_c'])/Q-3*q*q/Q**2
        finite=(exact_clock(p,s,1e-4)['weff']-exact_clock(p,s,0)['weff'])/1e-4
        assert abs(wa_pred-finite)<2e-4
        results.append(dict(dphi_dln_a=s,predicted_CPL_wa_tangent_at_today=wa_pred,
             target_CPL_wa=wa,discrepancy_to_target_wa=wa_pred-wa,
             model_w_eff_at_z1=samples[3]['weff'],
             target_CPL_w_at_z1=w0+wa*.5,
             samples=samples))
    assert all(x['predicted_CPL_wa_tangent_at_today']>0 for x in results)
    assert wa<0
    return dict(status='PASS_EXACT_CONSTANT_CLOCK_RECONSTRUCTION_FALSIFIER',
        scalar_clock='x=phi/Mpl=s ln a, with |s| fixed by fitted CPL w0',
        background_action='Einstein gravity, canonical phi, V(phi) reconstructed from Raychaudhuri; CDM mass m(phi)=m0 exp(-beta phi/Mpl)',
        analytic_E2='C exp(-s² N)+[3Omega_b/(3-s²)]exp(-3N)+[3Omega_c/(3+beta s-s²)]exp(-(3+beta s)N)+[4Omega_r/(4-s²)]exp(-4N), C chosen E(0)=1',
        exact_phantom_reconstruction='rho_eff=rho_phi+rho_c0 a^-3[exp(-beta s N)-1], w_eff=-1+(H² s²+rho_c-rho_c0 a^-3)/rho_eff',
        target_w0=w0,target_wa=wa,linear_scalar_clock_s_abs=s_abs,
        results=results,
        scope='Both sign branches are exact local canonical scalar backgrounds with a constructed multi-exponential V(phi); comparison to an independently fitted CPL central pair is a shape diagnostic, NOT an observational likelihood exclusion. The fitted fading model has a time-varying scalar clock and is not refuted.')

def test_growth(p):
    beta=p['beta'];u=beta*beta
    ophi=2*u/3;oc=1-ophi
    ex=1+2*u
    bias=(3-2*u)/((1+2*u)*(3+2*u))
    # Exact pressureless coupled scalar-dominated matter-era saddle, with
    # baryons test species (zero contribution to H and gravitational source).
    A=.5-3*u
    B=1.5*oc*(1+2*u)
    assert abs(ex*ex+A*ex-B)<2e-14
    assert abs(bias*(ex*ex+(.5-u)*ex)-1.5*oc)<2e-14
    def rhs(N,v):
        dc,dcp,db,dbp=v
        return [dcp,-A*dcp+B*dc,dbp,-(.5-u)*dbp+1.5*oc*dc]
    n0=-6
    y0=[math.exp(ex*n0),ex*math.exp(ex*n0),
        bias*math.exp(ex*n0),bias*ex*math.exp(ex*n0)]
    y=solve_ivp(rhs,(n0,0),y0,rtol=3e-12,atol=3e-14)
    assert y.success
    end=y.y[:,-1]
    err=max(abs(end[0]-1),abs(end[2]-bias))
    assert err<5e-9,err
    rec=p['phi_rec_fading'];now=p['phi_today_fading']
    fit_shift=math.exp(beta*(now-rec))
    early_ratio=math.exp(2*u*math.log(1101))
    return dict(status='PASS_ANALYTIC_PHIMDE_GROWTH_BARYON_BIAS_CONTROL',
        beta=beta,omega_phi=ophi,total_equation_of_state=2*u/3,
        dark_matter_density_power=-(3+2*u),
        growing_CDM_exponent=ex,
        uncoupled_test_baryon_to_CDM_density_contrast=bias,
        baryon_slip_fraction=1-bias,
        scalar_fifth_force_Geff_over_G=1+2*u,
        ode_control_max_error=err,
        fitted_recombination_to_today_mass_ratio=fit_shift,
        naive_attractor_extended_to_recombination_mass_ratio=early_ratio,
        caveat='Exact idealized phiMDE saddle neglects baryon gravitational backreaction and scalar potential; cannot extrapolate from recombination to today when radiation/DE are important. Real CLASS multi-fluid growth and RSD likelihood are required.',
        sources=['Amendola PhysRevD62 043511 (2000)','Amendola and Tocchini-Valentini PhysRevD66 043528 (2002)'])

def ultralight(p):
    beta=p['beta'];h=p['h_fading'];ob=p['omega_b'];oc=p['omega_c'];orr=p['omega_r']
    om=ob+oc;ode=1-om-orr
    H0=h*100*1000/MPC_M*HBAR_EV_S
    mass=1e-20
    def E2(a):return orr*a**-4+om*a**-3+ode
    def ha(a):return H0*math.sqrt(E2(a))
    aosc=brentq(lambda la:math.log(ha(math.exp(la))/mass),-31.,0.,xtol=1e-13)
    aosc=math.exp(aosc)
    rho_DM0=3*H0**2*MPL_EV**2*oc
    chi0=math.sqrt(2*rho_DM0)/mass
    chiosc=chi0*aosc**(-1.5)
    cutoff=(8*math.pi**2*H0**2*MPL_EV**2/beta**2)**.25
    loopratio=(mass/cutoff)**4
    comps=[]
    for z in (0,3,5,1100):
        a=1/(1+z);H=ha(a);om_a=om*a**-3/E2(a)
        kJ=a*(6*om_a*H*H*mass*mass)**.25*EV_TO_MPC_INV
        comps.append(dict(z=z,H_eV=H,mass_over_H=mass/H,
            comoving_instantaneous_Jeans_k_Mpc_inv=kJ,
            adiabaticity_estimate_2beta_squared_H_over_m=2*beta**2*H/mass))
    assert comps[-1]['mass_over_H']>1e5
    assert mass>LYA_BOUND_2026_EV
    assert loopratio<1e-65
    return dict(status='PASS_CONDITIONAL_ULTRALIGHT_BOSON_WKB_AND_LOOP_WINDOW',
        candidate='Real oscillating dark scalar chi with effective mass m_chi(phi)=m0 exp(-beta phi/Mpl), canonical quintessence phi and Einstein gravity',
        fiducial_dark_scalar_mass_eV=mass,
        lyalpha_pure_fuzzy_2026_model_dependent_lower_limit_eV=LYA_BOUND_2026_EV,
        fading_beta=beta,H0_eV=H0,
        onset_a_when_H_equals_m=aosc,
        onset_redshift=1/aosc-1,
        chi_amplitude_today_over_Mpl=chi0/MPL_EV,
        chi_amplitude_at_onset_over_Mpl=chiosc/MPL_EV,
        present_DM_energy_density_eV4=rho_DM0,
        MS_bosonic_one_loop_scalar_mass_cap_for_delta_mphi_less_H0_eV=cutoff,
        loop_delta_mphi_squared_over_H0_squared=loopratio,
        benchmark_redshift_scales=comps,
        caveat='Uses pure FDM Lyman-alpha bound as comparator (not a fit for interacting FDM); kJ is instantaneous matter Jeans approximation, not full transfer function. m(phi) in an ultra-light scalar EFT is not derived from an axion shift symmetry; possible quantum gravity/string constraints and fifth-force/growth effects remain untested. The loop naturalness criterion is scheme/protection-dependent and not a direct observational limit.',
        sources=['Liu Gong Zhou JCAP09(2026)051','D Amico Hamill Kaloper PhysRevD94 103526 (2016)'])

def main():
    p=get_inputs()
    results=dict(status='PASS_DARK_SECTOR_THREE_INDEPENDENT_FALSIFIERS',
        date='2026-11-03',inputs=p,
        constant_clock=constant_clock_test(p),
        analytic_two_species_growth=test_growth(p),
        oscillating_scalar_candidate=ultralight(p),
        scope='No re-fit, no new measured astrophysical observation, no standard model derivation; exact reconstruction, idealized analytic growth, and conditional microphysical window only.')
    target=ROOT/'data/toe_20261103_dark_sector_consistency_triangle.json'
    target.write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    brief={'beta':p['beta'],'cpl_target':[p['w0'],p['wa']],
      'constant_clock_wa':[r['predicted_CPL_wa_tangent_at_today'] for r in results['constant_clock']['results']],
      'constant_clock_weff_z1':[r['model_w_eff_at_z1'] for r in results['constant_clock']['results']],
      'bias':results['analytic_two_species_growth']['uncoupled_test_baryon_to_CDM_density_contrast'],
      'fit_recombination_mass_ratio':results['analytic_two_species_growth']['fitted_recombination_to_today_mass_ratio'],
      'FDM_onset_z':results['oscillating_scalar_candidate']['onset_redshift'],
      'FDM_loop_ratio':results['oscillating_scalar_candidate']['loop_delta_mphi_squared_over_H0_squared']}
    print('TOE_CONSISTENCY',json.dumps(brief),flush=True)
    return results
if __name__=='__main__':main()
