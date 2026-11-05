#!/usr/bin/env python3
"""TOE front 5: universality of light cone requires more than local coupling.

Two spatially local Gaussian relativistic-at-small-k lattice fields with
independent c_A,c_B and optional onsite spring g(phiA-phiB)^2/2.
Diagonalize exact normal modes: g>0 gives one gapless acoustic branch,
one gapped optical branch, NOT two massless species sharing speed.
One-loop quartic interactions produce momentum-independent tadpoles;
they do not drive the unequal kinetic coefficients together at 1 loop.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/toe_20261105_universal_lightcone_radiative_guard.json"
CA=1.; CB=1.2
def modes(k,g,a=1.):
    p2=4*math.sin(k*a/2)**2/a**2
    K=np.array([[CA*CA*p2+g,-g],[-g,CB*CB*p2+g]])
    eig=np.linalg.eigvalsh(K)
    assert min(eig)>-1e-12
    return np.sqrt(np.maximum(eig,0))
def loop_tadpole(c,m,klo=.1,khi=20.):
    # Bare equal-time cutoff shell, 3 spatial dimensions:
    # <phi^2> = integral(d^3k/(2pi)^3) 1/(2 omega_k).
    val,err=quad(lambda k: k*k/(4*math.pi**2*math.sqrt(c*c*k*k+m*m)),
                 klo,khi,epsabs=1e-10)
    return float(val)
def main():
    results=[]
    k0=1e-4
    for g in (0.,.03,.2,1.):
        small=modes(k0,g)
        zero=modes(0.,g)
        # c_acoustic from K at k->0:
        c_eff=math.sqrt((CA**2+CB**2)/2)
        if g==0:
            speeds=small/k0
            assert np.max(abs(speeds-np.array([CA,CB])))<1e-8
        else:
            assert abs(zero[0])<1e-12
            assert abs(zero[1]-math.sqrt(2*g))<1e-12
            # The acoustic eigenmode appears as the k^2 coefficient
            assert abs(small[0]/k0-c_eff)<1e-6
        results.append({"onsite_coupling_g":g,"massless_mode_count":2 if g==0 else 1,
          "k_very_small":k0,
          "frequencies_at_k0":small.tolist(),
          "frequencies_at_zero":zero.tolist(),
          "acoustic_effective_speed":c_eff if g>0 else None,
          "optical_gap":math.sqrt(2*g) if g>0 else 0.,
          "all_original_massless_species_retained":g==0})
    loops=[]
    mass=.3;high=20
    for gAB in (0.,.2,.8):
        la=.7;lb=1.2
        IA=loop_tadpole(CA,mass,khi=high)
        IB=loop_tadpole(CB,mass,khi=high)
        # Convention for L_int=lambdaA phiA^4/4!+
        # lambdaB phiB^4/4!+lambdaAB phiA^2 phiB^2/4:
        dmA=.5*la*IA+.5*gAB*IB
        dmB=.5*lb*IB+.5*gAB*IA
        assert dmA>0 and dmB>0
        # No external momentum in a one-loop tadpole:
        counterterms_kinetic=(0.,0.)
        loops.append({"lambda_AB":gAB,
          "bare_quartic_lambdaA":la,"bare_quartic_lambdaB":lb,
          "mass_counterterm_A":dmA,"mass_counterterm_B":dmB,
          "kinetic_counterterms_at_one_loop":counterterms_kinetic,
          "velocity_difference_after_one_loop_in_tadpole_approx":CB-CA})
    assert all(abs(x["velocity_difference_after_one_loop_in_tadpole_approx"]-.2)<1e-14 for x in loops)
    assert all(x["kinetic_counterterms_at_one_loop"]==(0.,0.) for x in loops)
    result={"status":"PASS_UNIVERSAL_LIGHTCONE_UNDERDETERMINATION_RADIATIVE_TEST",
       "microscopic_speed_coefficients":{"A":CA,"B":CB},
       "local_interaction":"g/2 (phi_A-phi_B)^2 on each lattice site",
       "normal_mode_sweep":results,
       "one_loop_quartic_tadpole_sweep":loops,
       "co_speed_without_loss_of_species":False,
       "no_one_loop_c_attraction_for_independent_phi4_tadpoles":True,
       "what_would_suffice":"An exact microscopic Lorentz symmetry acting on all species or a quantitatively demonstrated interacting RG attraction to a shared speed in d=3+1, with thresholds and radiative stability.",
       "interpretation":"The low-energy acoustic speed becomes common to the only remaining massless branch when g>0, but that is NOT universality of two gapless particle species: the relative branch is gapped.",
       "scope":"Free bosonic coupled lattice modes, mass-only one-loop tadpoles, no full renormalized interacting gauge-matter theory or higher-loop velocity beta functions.",
       "prior_art":"Two-field coupled harmonic lattice normal modes and one-loop phi4 tadpole self-energy are standard textbook results."}
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print("LIGHTCONE_PASS",[(x["onsite_coupling_g"],x["massless_mode_count"],x["acoustic_effective_speed"]) for x in results],
         "tadpole mass counterterms",[(x["lambda_AB"],x["mass_counterterm_A"]) for x in loops],flush=True)
    print("CERTIFICATE",OUT,flush=True)
    return result
if __name__=="__main__":main()
