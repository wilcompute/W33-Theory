"""Verify the canonically normalized D9 vector blocks and first massive gap."""

import json
from fractions import Fraction as F
from itertools import product
from math import sqrt
from pathlib import Path

import numpy as np
import sympy as sp


KAPPA = 4


def vector_block(curvatures, levels):
    """Return the vector block in units of the squared AdS radius."""
    active = [i for i, level in enumerate(levels) if level]
    individual = [curvature * level * (level+1)
                  for curvature, level in zip(curvatures, levels)]
    lam = sum(individual)
    if not active:
        return np.zeros((1, 1)), (0.0,)
    count = len(active) + int(len(active) == 2)
    block = np.diag([float(lam)] + [float(lam + 2*KAPPA)] * count)
    couplings_squared = [2*(curvatures[i] + KAPPA)*individual[i] for i in active]
    couplings = list(map(sqrt, couplings_squared))
    block[0, 1:1+len(active)] = block[1:1+len(active), 0] = couplings
    determinant = lam**2 - 2*sum(k*x for k, x in zip(curvatures, individual))
    assert determinant == lam*(lam+2*KAPPA) - sum(couplings_squared)
    assert determinant >= 0
    assert (determinant == 0) == (levels in ((1, 0), (0, 1)))
    upper = float(lam + KAPPA) + sqrt(KAPPA**2 + sum(couplings_squared))
    lower = float(determinant) / upper
    expected = (lower,) + (float(lam + 2*KAPPA),) * (count-1) + (upper,)
    assert np.allclose(np.linalg.eigvalsh(block), expected, rtol=1e-10, atol=1e-11)
    if determinant == 0:
        killing_null = np.array([-sqrt(2*(curvatures[active[0]]+KAPPA)), sqrt(lam)])
        assert np.linalg.norm(block @ killing_null) < 1e-11
    return block, expected


def gap_candidates(loose_curvature):
    k = loose_curvature
    _, single = vector_block((k, 20-k), (2, 0))
    _, mixed = vector_block((k, 20-k), (1, 1))
    return single[0], mixed[0]


def crossover_checks():
    k, m = sp.symbols("k m")
    single = m*m - (12*k+8)*m + 24*k*k
    mixed = m*m - 88*m + 8*k*(20-k)
    polynomial = k**3 + 44*k*k - 480*k + 800
    assert sp.expand(sp.resultant(single, mixed, m) + 128*k*polynomial) == 0
    assert all(polynomial.subs(k, i) % 13 != 0 for i in range(13))
    # The degree-three curvature cannot give a rational squared flux ratio.
    assert sp.rem((20-k)**2*(k+4), polynomial, k) == -80*k*k + 720*k + 800
    assert sp.rem(k*k*(24-k), polynomial, k) == 68*k*k - 480*k + 800
    left, right = F(2), F(21, 10)
    for _ in range(45):
        midpoint = (left+right)/2
        value = midpoint**3 + 44*midpoint**2 - 480*midpoint + 800
        if value > 0:
            left = midpoint
        else:
            right = midpoint
    k_star = (left+right)/2
    first, second = gap_candidates(k_star)
    assert abs(first-second) < 1e-13
    charge_ratio = (20-k_star)/k_star * sqrt((k_star+4)/(24-k_star))
    return {"curvature_in_ads_units": float(k_star), "first_positive_squared_mass_ads_units": first,
            "loose_to_tight_flux_ratio": float(charge_ratio),
            "exact_crossover_excluded_for_integer_fluxes": True}


def spectrum_checks():
    samples = (F(1, 1000), F(1, 10), F(1), F(2), F(21, 10), F(5), F(10))
    rows = []
    for k in samples:
        zero_count, count = 0, 0
        positive = []
        for levels in product(range(9), repeat=2):
            ell1, ell2 = levels
            multiplicity = (2*ell1+1)*(2*ell2+1)
            _, values = vector_block((k, 20-k), levels)
            count += len(values)*multiplicity
            zero_count += values.count(0)*multiplicity
            positive.extend((value, levels) for value in values if value > 0)
        first, levels = min(positive)
        assert count == 25921 and zero_count == 7
        assert abs(first - min(gap_candidates(k))) < 1e-13
        rows.append({"loose_curvature_in_ads_units": str(k), "first_level": levels,
                     "first_positive_vector_squared_mass_ads_units": first,
                     "first_spin_two_squared_mass_ads_units": float(2*k),
                     "massless_vectors": zero_count, "vectors_in_window": count})
    assert abs(rows[-1]["first_positive_vector_squared_mass_ads_units"] - (44 - 4*sqrt(71))) < 1e-13
    return rows


def anisotropic_checks():
    # For the loose sphere's lower vector branch, count full SO(3) multiplets
    # beneath m^2 L^2=budget using its exact quadratic in lambda.
    budget = 1
    rows = []
    for k in (F(1, 100), F(1, 10000), F(1, 1000000)):
        lam_max = float(k+budget) + sqrt(float(k*k + 2*(k+KAPPA)*budget))
        ell_max = int((sqrt(1+4*lam_max/float(k))-1)/2)
        count = (ell_max+1)**2 - 4
        assert ell_max >= 2
        assert vector_block((k, 20-k), (ell_max, 0))[1][0] <= budget
        assert vector_block((k, 20-k), (ell_max+1, 0))[1][0] > budget
        first, _ = gap_candidates(k)
        ratio = (20-k)/k * sqrt((k+4)/(24-k))
        rows.append({"loose_curvature": str(k), "count_below_m2L2_one": count,
                     "scaled_count": float(k*count),
                     "loose_to_tight_flux_ratio": float(ratio),
                     "gap_times_flux_ratio_squared": float(first*ratio**2)})
    assert abs(rows[-1]["scaled_count"] - (1+sqrt(8))) < 0.005
    assert abs(rows[-1]["gap_times_flux_ratio_squared"] - 200) < 0.001
    return rows


def mixed_scalar_checks():
    """Check the even scalar block at the first mixed angular harmonic."""
    k, eigenvalue = sp.symbols("k m")
    u, v, c, d = sp.symbols("u v c d")
    curvatures = (k, 20-k)
    lambdas = [2*curvature for curvature in curvatures]
    fluxes_sq = [2*(curvature+KAPPA) for curvature in curvatures]
    h = -sp.Rational(2, 3)*(u+v)
    currents = (h-u+lambdas[1]*c, h-v+lambdas[0]*c)
    delta_flux = sum(lam*current-flux_sq*trace for lam, current, flux_sq, trace
                     in zip(lambdas, currents, fluxes_sq, (u, v)))
    rows = [(48+flux_sq)*trace-lam*current+sp.Rational(2, 7)*delta_flux
            for flux_sq, trace, lam, current in zip(fluxes_sq, (u, v), lambdas, currents)]
    rows.extend((48*c+d, 48*d+fluxes_sq[0]*currents[1]+fluxes_sq[1]*currents[0]
                 +sp.prod(fluxes_sq)*c))
    # Check the external trace Einstein equation after eliminating the shifts.
    assert sp.expand(-sp.Rational(2, 3)*sum(rows[:2])-48*h
                     -sp.Rational(2, 7)*delta_flux) == 0
    # Independently project the two Maxwell equations on the coexact forms.
    for i, trace in enumerate((u, v)):
        other = 1-i
        mass_times_current = -sp.Rational(2, 3)*sum(rows[:2])-rows[i]+lambdas[other]*rows[2]
        maxwell_rhs = (40+fluxes_sq[i])*currents[i]-fluxes_sq[i]*trace+lambdas[other]*d
        assert sp.expand(mass_times_current-maxwell_rhs) == 0
    block = sp.Matrix(rows).jacobian((u, v, c, d))
    p = sp.symbols("p")
    cubic = eigenvalue**3 - 176*eigenvalue**2 + (45760+108*p)*eigenvalue/7 - 544*p
    expected = (eigenvalue-96)*cubic.subs(p, k*(20-k))
    assert sp.expand(block.charpoly(eigenvalue).as_expr()-expected) == 0
    # The cubic values at the checking points are affine in p. Its three
    # disjoint sign-change intervals cover all the roots for 0 < p <= 100.
    for p_value in (0, 100):
        for point, sign in ((16, 1), (80, -1), (96, -1), (128, 1)):
            assert sign * cubic.subs({p: p_value, eigenvalue: point}) > 0
    assert cubic.subs(eigenvalue, 0) == -544*p
    equal_roots = [float(sp.re(root)) for root in sp.nroots(expected.subs(k, 10))]
    # The odd scalar solution has cross-metric coefficients f1 and -f2,
    # and exact internal Maxwell coefficients -lambda2 and lambda1.
    b1, b2 = -lambdas[1], lambdas[0]
    odd_mass = 96
    assert sp.expand(lambdas[0]*b1 + lambdas[1]*b2) == 0
    for i, field in enumerate((b1, b2)):
        other = 1-i
        assert sp.expand(lambdas[i]-odd_mass-(b1-b2)+fluxes_sq[other]+2*KAPPA) == 0
        signed_flux_sum = (1-2*i)*sum(fluxes_sq)
        assert sp.expand(odd_mass*field + lambdas[other]*((1-2*i)*(b2-b1)+signed_flux_sum)) == 0
    return {"level": [1, 1], "scalar_polarizations_per_harmonic": 4,
            "harmonic_degeneracy": 9, "cubic_in_m2L2": str(cubic),
            "equal_radii_m2L2": equal_roots, "universal_m2L2": 96,
            "cubic_root_brackets": [[0, 16], [16, 80], [96, 128]],
            "odd_scalar_polarizations_per_harmonic": 1, "odd_scalar_m2L2": odd_mass}


def main():
    data = {"vector_gap_crossover": crossover_checks(),
            "full_vector_blocks_on_sampled_shapes": spectrum_checks(),
            "anisotropic_single_sphere_tower": anisotropic_checks(),
            "first_mixed_scalar_blocks": mixed_scalar_checks()}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D9_mixed_vector_spectrum.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified D9 vector blocks, the light-vector gap, and both first mixed scalar blocks.")


if __name__ == "__main__":
    main()
