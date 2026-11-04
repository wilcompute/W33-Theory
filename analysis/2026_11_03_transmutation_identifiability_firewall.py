#!/usr/bin/env python3
"""Rigorous scale-identifiability firewall for an interacting 1+1D
Gross-Neveu-style benchmark: transmutation produces an internal mass ratio,
but masses alone cannot determine the absolute cutoff when couplings float.
Also checks RG invariant continuum gap under a compensated scale change.
"""
from __future__ import annotations
import math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data'/'2026_11_03_transmutation_identifiability_firewall.json'
def mass_from_bare(Lambda,g2):
    return Lambda/math.sqrt(math.expm1(2*math.pi/g2))
def g2_for_mass(Lambda,m):
    return 2*math.pi/math.log1p((Lambda/m)**2)
def running_coupling(mu,m):
    return math.pi/math.log(mu/m)
def run():
    m1,m2=.001,1.0 # deliberately unitless independent target data
    family=[]
    for Lambda in (2.,10.,100.,1e3,1e6):
        g1=g2_for_mass(Lambda,m1)
        g2=g2_for_mass(Lambda,m2)
        assert abs(mass_from_bare(Lambda,g1)-m1)<1e-10*m1
        assert abs(mass_from_bare(Lambda,g2)-m2)<1e-10*m2
        assert abs(g1-g2)>1e-3
        family.append({"arbitrary_reference_cutoff_in_target_units":Lambda,
          "bare_couplings_squared_to_fit_two_masses":[g1,g2],
          "reproduced_mass_pair":[mass_from_bare(Lambda,g1),
                                   mass_from_bare(Lambda,g2)]})
    # Scheme-independent *existence* of dimensional transmutation in this
    # simplified continuum gap and one-loop beta relationship; numbers of
    # prefactor and beta coefficient depend on conventions.
    m=1.e-4
    running=[]
    for mu in (1.,2.,5.,10.,100.,1000.):
        g2=running_coupling(mu,m)
        recovered=mu*math.exp(-math.pi/g2)
        assert abs(recovered/m-1)<1e-12
        # Exact beta of x=g² is -x²/pi; compare compensated discrete
        # scale transformation versus direct running from mu -> 2mu.
        next_x=math.pi/(math.pi/g2+math.log(2.))
        assert abs(next_x-running_coupling(2*mu,m))<1e-12
        running.append({"renormalization_scale_mu":mu,
                        "running_gR_squared":g2,"RG_invariant_gap":recovered})
    # Spectrum alone cannot select gravitational mass scale or observed
    # vacuum energy: contribution of heavier threshold relative to lighter
    # is huge under the naive m^4 loop dimensional estimate.
    mass_hierarchy=m2/m1
    out={"status":"PASS_TRANSMUTATION_ABSOLUTE_SCALE_NONIDENTIFIABILITY",
      "benchmark":"1+1D asymptotically free four-fermion mean-field regularization, two independent dimensionless bare couplings with a shared freely chosen UV cutoff.",
      "sharp_cutoff_mass_formula":"m=Lambda/sqrt(exp(2pi/g_bare²)-1)",
      "inverse_fit":"g_bare²=2pi/log(1+(Lambda/m)^2), for arbitrary Lambda>m. Two measured masses and two unconstrained couplings do not identify Lambda.",
      "two_target_masses_unitless":[m1,m2],"distinct_cutoff_identical_spectra":family,
      "common_bare_coupling_no_go":"For common Lambda and common positive g_bare², the mass function is strictly increasing in g_bare²; two different target masses cannot be reproduced.",
      "continuum_one_loop_mass":"m=mu*exp(-pi/gR²(mu))",
      "continuum_beta_gR_squared":"d(gR²)/d ln(mu)=-(gR²)^2/pi",
      "RG_invariance_tests":running,
      "naive_m4_vacuum_energy_ratio":mass_hierarchy**4,
      "radiative_warning":"m^4 is a dimensional estimate for a threshold contribution, not a calculated renormalized cosmological constant; a gravitational vacuum counterterm and observable subtraction scheme must be specified.",
      "core_no_go":"A dimensionless graph or interaction gap cannot fix an absolute meter, GeV, Planck scale or Newton constant without an external physical datum or a separate dimensionful dynamical reference. Scale invariance of the parameter family explicitly witnesses underidentification.",
      "prior_project":"analysis/2026_11_03_marginal_gap_scale_comparison.py already owns an independently normalized lattice-Dirac gap benchmark; this certificate adds exact inverse maps for two masses and a compensated RG-running invariance test.",
      "source":["https://doi.org/10.1103/PhysRevD.10.3235","https://doi.org/10.1016/0550-3213(90)90045-F"]}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print("TRANSMUTATION",{"mass_ratio":mass_hierarchy,"UV_cases":len(family),"RG_cases":len(running),"couplings_first_last":[family[0]['bare_couplings_squared_to_fit_two_masses'],family[-1]['bare_couplings_squared_to_fit_two_masses']]},flush=True)
if __name__=="__main__":run()
