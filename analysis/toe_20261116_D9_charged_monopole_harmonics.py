#!/usr/bin/env python3
"""Exact charged-scalar monopole harmonic KK spectrum on S2xS2.

This is the test-scalar *charged* covariant Laplacian, NOT a
diagonalization of Einstein-Maxwell metric-vector-scalar coupled modes.
Unit electric charge; first Chern numbers n1,n2 ∈ Z; q_i=n_i/2.
For j_i=|q_i|+k_i and k_i>=0,
lambda= [j1(j1+1)-q1²]/r1² + [j2(j2+1)-q2²]/r2²,
multiplicity (2j1+1)(2j2+1).
"""
from fractions import Fraction as F
import json
from itertools import product
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"toe_20261116_D9_charged_monopole_KK_probe.json"
def levels(n1,n2,t,K):
    q1=F(n1,2);q2=F(n2,2)
    result=[]
    for k1,k2 in product(range(K+1),repeat=2):
        j1=abs(q1)+k1;j2=abs(q2)+k2
        angular1=j1*(j1+1)-q1*q1
        angular2=j2*(j2+1)-q2*q2
        assert angular1>=0 and angular2>=0
        LL=20*(angular1+t*angular2)/(1+t)
        multiplicity=int((2*j1+1)*(2*j2+1))
        assert multiplicity>0
        result.append({"k1":k1,"k2":k2,"j1":str(j1),"j2":str(j2),
                       "m2L2":str(LL),"degeneracy":multiplicity})
    return result

def run():
    shapes=[]
    for n1,n2 in product(range(-4,5),repeat=2):
        q1,q2=F(n1,2),F(n2,2)
        samples=levels(n1,n2,F(3,2),5)
        counterpart=levels(-n1,-n2,F(3,2),5)
        assert samples==counterpart
        assert len(samples)==36
        lo=min(F(s["m2L2"]) for s in samples)
        ground=20*(abs(q1)+F(3,2)*abs(q2))/(1+F(3,2))
        assert lo==ground
        assert samples[0]["degeneracy"]==(abs(n1)+1)*(abs(n2)+1)
        all_deg=sum(s["degeneracy"] for s in samples)
        expected=((6)*(abs(n1)+6))*((6)*(abs(n2)+6))
        assert all_deg==expected
        shapes.append({"charges":[n1,n2],
                       "lowest_j":[str(abs(q1)),str(abs(q2))],
                       "lowest_m2L2_t3half":str(ground),
                       "lowest_degeneracy":samples[0]["degeneracy"],
                       "charged_spectrum_is_nonzero_if_any_flux":bool(lo>0),
                       "multiplicity_total_levels_k0_to5":all_deg,
                       "central_2pi_rotation_parities":[(-1)**n1,(-1)**n2]})
    assert len(shapes)==81
    x=levels(1,2,F(1),2)
    assert x[0]["m2L2"]=="15" and x[0]["degeneracy"]==6
    result={
      "status":"EXACT_D9_S2S2_CHARGED_SCALAR_MONOPOLE_HARMONIC_KK",
      "unit_electric_charge":True,"compact_monopole_charges_checked":[-4,4],
      "number_of_charge_pairs_checked":81,
      "angular_momenta":"j_i=abs(n_i)/2+k_i, k_i=0,1,2,...",
      "covariant_spherical_harmonic_eigenvalue":"r_i^-2*(j_i*(j_i+1)-n_i^2/4)",
      "combined_mass_formula":"m²L² = 20/(1+t)*[(j1(j1+1)-n1²/4)+t*(j2(j2+1)-n2²/4)], t=r1²/r2²",
      "spectral_degeneracy":"(2j1+1)(2j2+1)",
      "lowest_m2L2_formula":"20/(1+t)*(abs(n1)/2+t*abs(n2)/2)",
      "lowest_multiplicity_formula":"(abs(n1)+1)(abs(n2)+1)",
      "nonzero_flux_charged_probe_has_positive_covariant_gap":True,
      "unit_flux_example_n1_n2":[1,2],
      "unit_flux_example_t_equal":1,
      "unit_flux_example_lowest_m2L2":15,
      "unit_flux_example_lowest_multiplicity":6,
      "parity_selection":"a 2π rotation in SU2_i center multiplies charged line-bundle sections by (-1)^n_i",
      "charge_grid_results":shapes,
      "scope":"Geometric charged scalar PROBE with a specified unit electric charge and standard Dirac monopole connections. The original minimal Einstein-Maxwell theory does not automatically contain this charged matter field. Not the mixed vector/scalar KK masses or a stability proof.",
      "literature":"Wu and Yang 1976 monopole harmonics, L² eigenvalue j(j+1) and covariant laplacian j(j+1)-q²."
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n")
    return result
if __name__=="__main__":
    d=run();print("PASS",d["status"],"pairs",d["number_of_charge_pairs_checked"],flush=True)
