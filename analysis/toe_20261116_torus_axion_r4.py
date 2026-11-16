"""Check the toroidal axion embedding and the arithmetic of the R4 cusp probe."""

import json
from collections import Counter
from fractions import Fraction
from itertools import product
from math import gcd
from pathlib import Path

import sympy as sp

from toe_20261115_quiver_torus_charges import torus_cubic


DATA = Path(__file__).resolve().parents[1] / "data"


def check_cubic_action(matrix):
    cubic = torus_cubic()
    substitution = {}
    for i in range(1, 7):
        labels = (f"E{i}", f"Q{i}")
        for label, row in zip(labels, matrix.tolist()):
            substitution[label] = [(new_label, int(sign)) for new_label, sign in zip(labels, row) if sign]
    result = Counter()
    for term, coefficient in cubic.items():
        factors = [substitution.get(label, [(label, 1)]) for label in term]
        for monomials in product(*factors):
            result[frozenset(label for label, _ in monomials)] += coefficient * sp.prod(sign for _, sign in monomials)
    assert {term: coefficient for term, coefficient in result.items() if coefficient} == cubic


def axion_weyl_images():
    kinetics = json.loads((DATA / "toe_20261115_torus_kinetic_reconstruction.json").read_text(encoding="utf-8"))
    charges = json.loads((DATA / "toe_20261115_quiver_torus_charges.json").read_text(encoding="utf-8"))
    directions = kinetics["symmetric_generators_by_scalar_character"]

    def canonical(entries):
        entries = sorted((*sorted((left, right)), sign) for left, right, sign in entries)
        common = entries[0][2]
        return tuple((left, right, common*sign) for left, right, sign in entries)

    origin = canonical(directions["63"])
    assert origin == tuple((f"E{i}", f"Q{i}", 1) for i in range(1, 7))
    queue = [origin]
    seen = {origin}
    for generator in queue:
        for lift in charges["signed_integral_lifts_of_simple_reflections"]:
            action = lift["permutation"]
            minus = set(lift["negated_after_permutation"])
            image = canonical([
                (action[left], action[right], sign*(-1)**((action[left] in minus) + (action[right] in minus)))
                for left, right, sign in generator
            ])
            if image not in seen:
                seen.add(image)
                queue.append(image)
    assert seen == {canonical(entries) for entries in directions.values()} and len(seen) == 36
    return len(seen)


def verify():
    x, y = sp.symbols("x y", real=True)
    metric = sp.Matrix([[x*x+y*y, x], [x, 1]])/y
    s_matrix = sp.Matrix([[0, -1], [1, 0]])
    t_matrix = sp.Matrix([[1, 1], [0, 1]])
    check_cubic_action(s_matrix)
    check_cubic_action(t_matrix)
    for transformation, x_prime, y_prime in (
        (s_matrix, -x/(x*x+y*y), y/(x*x+y*y)),
        (t_matrix, x+1, y),
    ):
        transformed = metric.subs({x: x_prime, y: y_prime}, simultaneous=True)
        assert (transformed-transformation*metric*transformation.T).applyfunc(sp.simplify) == sp.zeros(2, 2)
    assert metric.diff(x).subs({x: 0, y: 1}) == sp.Matrix([[0, 1], [1, 0]])
    assert metric.det().simplify() == 1

    v = sp.symbols("v", positive=True)
    cusp_tests = []
    for q in range(1, 21):
        for a in range(q):
            if gcd(a, q) != 1:
                continue
            r = pow(-a, -1, q) if q > 1 else 0
            t = (-a*r-1)//q
            assert sp.det(sp.Matrix([[r, t], [q, -a]])) == 1
            point = sp.Rational(a, q) + sp.I*v
            mapped = sp.cancel((r*point+t)/(q*point-a))
            assert sp.simplify(mapped - sp.Rational(r, q) - sp.I/(q*q*v)) == 0
            charge = sp.Matrix([-a, q])
            mass_matrix = sp.Matrix([[1, x], [x, x*x+y*y]])/y
            square = (charge.T*mass_matrix*charge)[0].subs({x: sp.Rational(a, q), y: v})
            assert sp.simplify(square-q*q*v) == 0
            if a in (0, 1) and q <= 6:
                cusp_tests.append({
                    "axion": str(Fraction(a, q)), "duality_matrix": [[r, t], [q, -a]],
                    "primitive_charge": [-a, q], "dual_volume": f"1/({q*q}*y)",
                    "leading_r4_ratio_to_zero_axion": str(Fraction(1, q**4)),
                    "first_subleading_cusp_scale": str(Fraction(1, q**3)),
                    "leading_d4r4_ratio_to_zero_axion": str(Fraction(1, q**7)),
                })

    t = sp.Symbol("t")
    for q in range(1, 25):
        cyclotomic = sp.Poly(sp.cyclotomic_poly(q, t), t)
        residues = [a for a in range(q) if gcd(a, q) == 1]
        for n in range(13):
            ramanujan = sum(d*sp.mobius(q//d) for d in sp.divisors(gcd(q, n)))
            phase_sum = sum(t**((a*n) % q) for a in residues)
            assert sp.rem(sp.Poly(phase_sum-ramanujan, t), cyclotomic).is_zero
    assert sp.simplify(4*sp.zeta(2)*sp.pi/(2*sp.zeta(4)) - 30/sp.pi) == 0
    negative_argument = -sp.Rational(1, 2)
    reflected_argument = 3-negative_argument
    epstein_reflection = (
        sp.pi**(negative_argument-reflected_argument)
        * sp.gamma(reflected_argument)/sp.gamma(negative_argument)
    )
    assert sp.simplify(-8*sp.zeta(4)*epstein_reflection) == sp.Rational(1, 12)
    half_integer_peaks = {
        str(s): str(sp.simplify(sp.sqrt(sp.pi)*sp.gamma(s-sp.Rational(1, 2))/sp.gamma(s)))
        for s in (sp.Rational(3, 2), sp.Integer(2), sp.Rational(5, 2), sp.Rational(7, 2))
    }
    return {
        "axion_tangent_weyl_images": axion_weyl_images(),
        "cusp_tests": cusp_tests,
        "rank_one_cusp_kernel_masses": half_integer_peaks,
        "d4r4_leading_factor_times_positive_epstein_at_7_over_2": "1/12",
        "normalized_r4_fourier_limits": {
            n: {"leading_rational_multiplier_of_30_over_pi": str(sum(Fraction(1, d**3) for d in sp.divisors(n))),
                "subleading_rational_multiplier_of_2B_over_zeta3": str(sum(Fraction(1, d**2) for d in sp.divisors(n)))}
            for n in range(1, 13)
        },
        "normalized_d4r4_leading_fourier_divisor_weights": {
            n: str(sum(Fraction(1, d**6) for d in sp.divisors(n))) for n in range(1, 13)
        },
    }


if __name__ == "__main__":
    path = DATA / "toe_20261116_torus_axion_r4.json"
    path.write_text(json.dumps(verify(), indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Verified integral axion dualities, all 36 scalar images, and the R4 cusp and Fourier arithmetic")
