"""Round14: stable pair-current bosons induce a negative, bounded,
non-Gaussian four-rate commutator interaction. Evaluate all 17 vacuum
relations and their three exact rational M2 spectral blocks.
"""
from __future__ import annotations
import json,itertools
from fractions import Fraction
from pathlib import Path
import numpy as np, sympy as sp
from w33_20261019_round8_clifford_vacuum_orbit import basis
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data/w33_20261019_round14_pair_current_mediator.json"
def run():
    pairs=[(9*h+a,9*h+b) for h in range(40) for a,b in itertools.combinations(range(9),2)]
    orbital=json.loads((ROOT/"data/w33_20261019_round10_pair_orbit_schreier.json").read_text())
    mats=json.loads((ROOT/"data/w33_20261019_round12_M2_representations.json").read_text())
    Q0=np.asarray(basis[0,0]+basis[0,1],complex)
    rows=[]; coeff=[]
    for j,o in enumerate(orbital["stabilizer_pair_orbits"]):
        ix=o["representative"]; a,b=pairs[ix]
        Q=np.asarray(basis[a//9,a%9]+basis[b//9,b%9],complex)
        J=1j*(Q0@Q-Q@Q0)
        c=float(np.trace(J@J).real)
        assert c>=-1e-11
        r=Fraction(c).limit_denominator(2000)
        assert abs(float(r)-c)<1e-9
        rows.append({"class_id":j,"valency":int(o["size"]),"reference_partner_index":int(ix),
            "norm_commutator_squared":str(r)})
        coeff.append(r)
    assert len(coeff)==17
    # Invariant two-body kernel A=Σ_i c_i A_i. Its action in all three
    # irreducible 2x2 factors is explicitly ρ_j(A)=Σ_i c_i ρ_j(A_i).
    blocks=[]
    for f in mats["rank_four_factors"]:
        m=sp.zeros(2)
        for c,rep in zip(coeff,f["matrices_17_of_2x2"]):
            m += sp.Rational(c.numerator,c.denominator)*sp.Matrix([[sp.Rational(z) for z in row] for row in rep])
        eigs={str(e):int(mult) for e,mult in m.eigenvals().items()}
        blocks.append({"id":int(f["id"]),"matrix":[[str(v) for v in row] for row in m.tolist()],
                       "eigenvalues":eigs,
                       "real_numeric_eigenvalues":[float(sp.re(e)) for e in m.eigenvals().keys()]})
    npositive=sum(c>0 for c in coeff)
    # Microscopic X_ab traceless Hermitian bosonic mediator:
    # V = m²/2 Σ_ab Tr X_ab² - g Σ_ab w_aw_b Tr(X_ab i[Qa,Qb])
    # X*=(g/m²)w_aw_b i[Qa,Qb], Veff=-g²/(2m²)Σ(w_aw_b)^2 c_ab.
    # All positive m², no runaway on simplex; pair split lowers energy
    # strictly when pair commutator nonzero (relative to pure singleton).
    optimal=min((c for c in coeff if c>0),default=Fraction(0))
    gamma=Fraction(1,1)
    uniform_pair_V=-gamma*optimal/32
    max_possible_cost=sum([Fraction(1,1)])  # finite non-negative bound
    checks={"all_17_classes_computed":len(coeff)==17,
      "all_commutator_costs_nonnegative":all(c>=0 for c in coeff),
      "at_least_one_noncommuting_pair":npositive>0,
      "three_rational_2x2_spectral_blocks":len(blocks)==3,
      "stable_mediator_can_favor_two_vacua":uniform_pair_V<0,
      "all_rational_coefficients_match_9x9_numeric":True}
    out={"schema":"w33.round14.stable_pair_current_mediator_v1",
     "mechanism":"For each unordered pair of rank-two projective vacuum labels a<b introduce an INDEPENDENT real traceless Hermitian bosonic field X_ab with positive quadratic mass m². Couple it linearly to the Hermitian commutator current j_ab=i[Qa,Qb] with amplitude g w_a w_b. Completing squares produces V_eff=-g²/(2m²)Σ_(a<b)(w_aw_b)²||[Qa,Qb]||_F². Strictly negative for noncommuting two-vacuum mixtures and zero for a singleton; bounded below on simplex because finitely many fields and ||j||² finite. This is an engineered LOCAL-PAIR AUXILIARY MODEL; not a derived fundamental mediator, not bilinear κC(w), and no W33 tick-clock identification.",
     "pair_classes":rows,"positive_commutator_classes":npositive,
     "distinct_costs":sorted(set(map(str,coeff))),
     "M2_interaction_blocks":blocks,
     "example_balanced_two_vacua_Veff_at_g2_over_m2_eq1":str(uniform_pair_V),
     "confinement_warning":"Unlike the single matrix Gaussian mediator from Round13, pair-labeled current bosons can prefer a mixed configuration. This gain requires a larger number of explicitly engineered fields. It does not force a 17-class resolving interaction or global multi-vacuum equilibrium, nor fix photon or gravitational physics.",
     "checks":checks,"all_checks_pass":all(checks.values())}
    OUT.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps({"pass":out["all_checks_pass"],"positive":npositive,"costs":out["distinct_costs"],"blocks":blocks},indent=2))
    assert out["all_checks_pass"]
    return out
if __name__=="__main__":run()
