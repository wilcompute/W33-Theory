"""Certify the warp resonance test on quantized Einstein T(p,q) bundles."""

import json
from itertools import product
from pathlib import Path

import sympy as sp


ETA = sp.Symbol("eta")
TARGET = 32


def einstein_polynomial(p, q):
    return sp.Poly(q*q*ETA*(2-ETA)**2-p*p*(1-ETA)*(1+ETA)**2, ETA)


def interior_interval(p, q, precision=14):
    intervals = einstein_polynomial(p, q).intervals(eps=sp.Rational(1, 10**precision))
    roots = [(lo, hi) for (lo, hi), count in intervals if 0 < lo <= hi < 1 and count == 1]
    assert len(roots) == 1
    return roots[0]


def charged_gap():
    rows = []
    # For |n p| or |n q| >= 5 the vertical term alone exceeds 48.
    # When both are <= 4, j >= 7/2 gives a horizontal term >= 47
    # from that sphere and a vertical term >= 2.
    for p, q in product(range(1, 5), repeat=2):
        shape = einstein_polynomial(p, q)
        lo, hi = interior_interval(p, q)
        for twice_j, twice_k in product(range(p, 7, 2), range(q, 7, 2)):
            left = sp.Rational(twice_j*(twice_j+2)-p*p, 4)
            right = sp.Rational(twice_k*(twice_k+2)-q*q, 4)
            eigenvalue = 4*(1+ETA)*left+4*(2-ETA)*right+p*p*(1+ETA)**2/(2*ETA)
            numerator = sp.Poly(sp.cancel(2*ETA*(eigenvalue-TARGET)), ETA)
            common = sp.gcd(numerator, shape)
            assert common.degree() == 0 or common.count_roots(0, 1) == 0
            lower = 4*(1+lo)*left+4*(2-hi)*right+sp.Rational(p*p, 2)*(lo+2+1/hi)
            upper = 4*(1+hi)*left+4*(2-lo)*right+sp.Rational(p*p, 2)*(hi+2+1/lo)
            gap = max(TARGET-upper, lower-TARGET)
            assert gap > 0
            rows.append((gap, p, q, twice_j, twice_k, lower, upper))
    gap, p, q, twice_j, twice_k, lower, upper = min(rows)
    assert gap < 16
    return {
        "tested_labels": len(rows),
        "certified_gap_rounded_down": float(sp.floor(1000*gap)/1000),
        "closest_tested_label": {
            "absolute_effective_charges": [p, q], "twice_spins": [twice_j, twice_k],
            "scalar_eigenvalue_interval": [str(lower), str(upper)],
        },
    }


def neutral_and_endpoint_checks():
    # In the neutral sector all other labels are at most 24 or at least 40.
    assert 4*2+8*2 == 24
    assert min(4*6+8*2, 8*6+4*2) == 40
    assert 4*3*4 > 40
    assert einstein_polynomial(1, 0).eval(sp.Rational(1, 3)) == -sp.Rational(32, 27)
    assert einstein_polynomial(0, 1).eval(sp.Rational(1, 3)) == sp.Rational(25, 27)
    ratio = (1-ETA)*(1+ETA)**2/(ETA*(2-ETA)**2)
    assert sp.simplify(sp.diff(ratio, ETA) -
                       (1+ETA)*(2-ETA)*(-2+5*ETA-5*ETA**2)/(ETA*(2-ETA)**2)**2) == 0
    norm_residues = {(25*q*q-32*p*p) % 80 for p, q in product(range(80), repeat=2)}
    assert all(n % 80 not in norm_residues for n in range(-6, 17) if n)
    # A zero Chern number gives S2 times a lens space covered by the round S3.
    endpoint = {4*j*(j+1)+2*k*(k+2) for j, k in product(range(3), range(4))}
    assert min(abs(level-TARGET) for level in endpoint) == 2
    assert 4*3*4 > 34 and 2*4*6 > 34


def pell_sequences():
    unit_x, unit_y = 19601, 13860
    assert unit_x**2-2*unit_y**2 == 1 and unit_y % 20 == 0
    rows = []
    for seed in ((1, 1), (38, 43)):
        p, q = seed
        norm = 25*q*q-32*p*p
        examples = []
        for _ in range(4):
            assert 25*q*q-32*p*p == norm
            lo, hi = interior_interval(p, q, precision=42)
            detuning = tuple(24*point-8 for point in (lo, hi))
            assert all(value*norm < 0 for value in detuning)
            assert min(abs(value) for value in detuning) >= sp.Rational(14, 9*(p*p+q*q))
            midpoint = sum(detuning)/2
            # Rationalize sqrt(lambda+4)-6 to avoid cancellation in Delta-4.
            dimension_shift = midpoint/(sp.sqrt(36+midpoint)+6)
            examples.append({
                "chern_pair": [p, q], "neutral_eigenvalue_minus_32": float(midpoint),
                "detuning_times_p_squared": float(midpoint*p*p),
                "operator_dimension_minus_4": float(dimension_shift),
            })
            x, y = 5*q, 4*p
            p, q = (unit_y*x+unit_x*y)//4, (unit_x*x+2*unit_y*y)//5
        asymptotic = -sp.Rational(5, 12)*norm
        assert abs(examples[-1]["detuning_times_p_squared"]-float(asymptotic)) < 1e-8
        rows.append({"norm": norm, "asymptotic_detuning_times_p_squared": str(asymptotic),
                     "examples": examples})
    return rows


def projected_warp_branch():
    cosine, u = sp.symbols("x u", real=True)
    harmonic = sp.legendre(2, cosine)
    laplacian = sp.diff((1-cosine**2)*sp.diff(harmonic, cosine), cosine)
    assert sp.expand(laplacian+6*harmonic) == 0
    normal = sp.integrate(harmonic**2, (cosine, -1, 1))
    cubic = sp.integrate(harmonic**3, (cosine, -1, 1))
    source = 20*(u**-1-u**sp.Rational(3, 5))
    coefficient = sp.diff(source, u, 2).subs(u, 1)*cubic/(2*normal)
    assert coefficient == sp.Rational(32, 5)
    return {"quadratic_projected_source": str(coefficient),
            "leading_amplitude_per_32_minus_eigenvalue": str(1/coefficient),
            "solves_external_equation_at_fixed_internal_metric_only": True}


def main():
    neutral_and_endpoint_checks()
    data = {
        "warp_resonance_eigenvalue": TARGET,
        "resonance_for_any_integer_chern_pair": False,
        "nonzero_chern_numbers_charged_gap": charged_gap(),
        "endpoint_gap_lower_bound": 2,
        "neutral_gap_lower_bound": "14/[9(p^2+q^2)]",
        "neutral_near_resonances": pell_sequences(),
        "external_equation_bifurcation": projected_warp_branch(),
    }
    destination = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_Tpq_warp_resonance.json"
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Certified the integer-flux warp obstruction and two Pell near-resonance families.")


if __name__ == "__main__":
    main()
