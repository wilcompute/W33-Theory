"""Constrained physical scalar matrices for the two-sphere magnetic branch."""

import json
from fractions import Fraction as F
from itertools import product
from math import sqrt
from pathlib import Path

import numpy as np
import sympy as sp


def build_matrix(action, dimension):
    columns = [action([int(i == j) for i in range(dimension)]) for j in range(dimension)]
    return list(zip(*columns))


def scalar_sectors(curvatures, levels, check_constraints=False, *, laplacians=None):
    lam = ([k * ell * (ell+1) for k, ell in zip(curvatures, levels)]
           if laplacians is None else laplacians)
    total = sum(lam)
    flux_sq = [2*(k+4) for k in curvatures]
    active = [i for i, ell in enumerate(levels) if ell > 0]
    tensor = [i for i, ell in enumerate(levels) if ell > 1]
    div = [F(1, 2)*lam[i]-curvatures[i] for i in range(2)]
    mixed = len(active) == 2
    common = total + 8

    def even_action(x):
        trace = x[:2]
        tensor_terms = dict(zip(tensor, x[2:2+len(tensor)]))
        cross, rotated_cross = x[-2:] if mixed else (0, 0)
        h = -F(2, 3)*sum(trace)
        current = [h-trace[i]+div[i]*tensor_terms.get(i, 0)+lam[1-i]*cross
                   if i in active else 0 for i in range(2)]
        flux_change = sum(lam[i]*current[i]-flux_sq[i]*trace[i] for i in range(2))
        trace_mass = [(common+flux_sq[i])*trace[i]-lam[i]*current[i]+F(2, 7)*flux_change
                      for i in range(2)]
        tensor_mass = {i: (total-2*curvatures[i])*tensor_terms[i]-2*current[i] for i in tensor}
        cross_mass = common*cross+rotated_cross
        rotated_cross_mass = (common*rotated_cross + flux_sq[0]*current[1]
                              + flux_sq[1]*current[0] + flux_sq[0]*flux_sq[1]*cross)
        if check_constraints:
            h_mass = -F(2, 3)*sum(trace_mass)
            assert sp.expand(h_mass-common*h-F(2, 7)*flux_change) == 0
            for i in active:
                current_mass = (h_mass-trace_mass[i]+div[i]*tensor_mass.get(i, 0)
                                + lam[1-i]*cross_mass)
                maxwell_rhs = ((total+flux_sq[i])*current[i]
                               - flux_sq[i]*(trace[i]+div[i]*tensor_terms.get(i, 0))
                               + lam[1-i]*rotated_cross)
                assert sp.expand(current_mass-maxwell_rhs) == 0
        return (trace_mass + [tensor_mass[i] for i in tensor]
                + ([cross_mass, rotated_cross_mass] if mixed else []))

    def odd_action(x):
        tensor_terms = dict(zip(tensor, x[:-1]))
        cross = [x[-1], -x[-1]-sum(div[i]*tensor_terms[i]/lam[1-i] for i in tensor)]
        current = [-div[i]*tensor_terms.get(i, 0)-lam[1-i]*cross[i] for i in range(2)]
        tensor_mass = {i: (total-2*curvatures[i])*tensor_terms[i]+2*current[i] for i in tensor}
        cross_mass = [common*cross[i]+current[1-i]-flux_sq[1-i]*cross[1-i] for i in range(2)]
        if check_constraints:
            current_mass = [-div[i]*tensor_mass.get(i, 0)-lam[1-i]*cross_mass[i] for i in range(2)]
            assert sp.cancel(sum(lam[i]*current[i] for i in range(2))) == 0
            assert sp.cancel(sum(lam[i]*current_mass[i] for i in range(2))) == 0
            for i in range(2):
                maxwell_rhs = lam[1-i]*(current[i]-current[1-i]
                                       - flux_sq[i]*cross[i]+flux_sq[1-i]*cross[1-i])
                assert sp.cancel(current_mass[i]-maxwell_rhs) == 0
        return [tensor_mass[i] for i in tensor] + cross_mass[:1]

    even = build_matrix(even_action, 2 + len(tensor) + 2*int(mixed))
    odd = build_matrix(odd_action, 1 + len(tensor)) if mixed else []
    return even, odd


def spectrum(curvatures, levels):
    masses = []
    for sector in scalar_sectors(curvatures, levels):
        if sector:
            values = np.linalg.eigvals(np.array(sector, dtype=float))
            assert max(abs(values.imag)) < 1e-7, (curvatures, levels, values)
            masses.extend(values.real)
    return sorted(masses)


def shifted_polynomials(k, x, y, z):
    other = 20-k
    flux1, flux2 = 2*k+8, 2*other+8
    weighted = flux1*x+flux2*y
    residual = (z**3 - 56*z*z + (3840+12*k*other-12*weighted)*z/7
                + 16*(flux1*x*(10+other)+flux2*y*(10+k))/7)
    odd = (z*((z-8)**2-flux1*flux2)
           - flux1*x*(z+2*other) - flux2*y*(z+2*k))
    return residual, odd


def verify_factorizations(k, m):
    x, y = sp.symbols("x y")
    residual, odd = shifted_polynomials(k, x, y, m-x-y)
    even_block, odd_block = scalar_sectors((k, 20-k), (2, 2), check_constraints=True,
                                         laplacians=(x, y))
    assert sp.expand(sp.Matrix(odd_block).charpoly(m).as_expr()-odd) == 0
    assert sp.expand(sp.Matrix(even_block).charpoly(m).as_expr()-odd*residual) == 0
    single, _ = scalar_sectors((k, 20-k), (2, 0), laplacians=(x, sp.Integer(0)))
    assert sp.expand(sp.Matrix(single).charpoly(m).as_expr()-residual.subs(y, 0)) == 0
    f0 = -7 * residual.subs(m, 0)
    expected = (x*(x-2*k)*(7*x+296-10*k)
                + y*(y-2*(20-k))*(7*y+296-10*(20-k))
                + x*y*(21*(x+y)+112))
    assert sp.expand(f0-expected) == 0
    # Positivity and root ordering controls used in the all-level proof.
    budget = F(81, 10)
    s = 40-budget
    assert 21*s*s-368*s+3840-576*budget-7680 > 0
    assert F(519, 10)*F(319, 10)*F(5593, 10) / 76800 > budget
    s = 120-budget
    assert s*s-32*s-720-48*budget > 0
    for edge in (0, 10):
        z = 40-F(4, 3)*edge
        assert z*z-56*z+F(3840+12*edge*(20-edge), 7) < 0

    n, leading = sp.symbols("n leading")
    anisotropic = -7*residual.subs({x: n*k, y: 0, m: leading*k*k})
    expected_coefficient = 296*n*(n-2)-3840*leading
    assert sp.expand(sp.diff(anisotropic, k, 2).subs(k, 0)/2-expected_coefficient) == 0
    return {"mixed_even_factor": str(residual),
            "mixed_odd_polynomial": str(odd),
            "loose_sphere_fixed_ell_coefficient_of_k_squared": "37*n*(n-2)/480",
            "lightest_scalar_coefficient_of_k_squared": "37/20",
            "lightest_scalar_coefficient_of_inverse_flux_ratio_squared": "370/3"}


def verify_gap_switch(k, m):
    single, _ = shifted_polynomials(k, 6*k, sp.Integer(0), m-6*k)
    mixed, _ = shifted_polynomials(k, 2*k, 2*(20-k), m-40)
    shared = sp.Poly(sp.resultant(single, mixed, m), k)
    core = next(factor for factor, _ in shared.factor_list()[1] if factor.degree() == 7)
    assert core.is_irreducible
    brackets = [(sp.Rational(i, 1000), sp.Rational(i+1, 1000))
                for i in (2477, 2672, 5269, 7513)]
    assert shared.count_roots(sp.Rational(1, 1000), 10) == 4
    assert shared.count_roots(0, sp.Rational(1, 1000)) == 1  # only the degenerate endpoint
    assert all(shared.count_roots(lo, hi) == 1 for lo, hi in brackets)
    for index, mass, sign in ((0, sp.Rational(7, 2), -1), (2, 7, 1), (3, 8, 1)):
        lo, hi = brackets[index]
        for poly in (-single, mixed):
            at_mass = sp.Poly(poly.subs(m, mass), k)
            assert at_mass.count_roots(lo, hi) == 0
            assert sign*at_mass.eval(lo) > 0
    for point, mass, sign in ((sp.Rational(13, 5), sp.Rational(371, 100), -1),
                              (sp.Rational(14, 5), 4, 1)):
        assert all(sign*poly.subs({k: point, m: mass}) > 0 for poly in (-single, mixed))
    lo, hi = brackets[1]
    polynomial = shared.sqf_part()
    for _ in range(33):
        mid = (lo+hi)/2
        if polynomial.eval(lo)*polynomial.eval(mid) > 0:
            lo = mid
        else:
            hi = mid
    critical = float((lo+hi)/2)
    ratio = (20-critical)/critical*sqrt((critical+4)/(24-critical))
    # The mixed scalar gap is below the mixed vector and the first spin two.
    p = sp.symbols("p")
    mixed_in_p = m**3-176*m*m+(45760+108*p)*m/7-544*p
    assert sp.expand(mixed_in_p.subs(p, m*(88-m)/8)
                     - m*(-13*m*m+864*m+7744)/14) == 0
    assert sp.expand(mixed.subs(m, 2*k)-160*k*(k*(20-k)+96)/7) == 0
    return {"curvature_in_ads_units": critical, "loose_to_tight_flux_ratio": ratio,
            "curvature_isolating_interval": [str(bound) for bound in brackets[1]],
            "resultant": str(sp.factor(shared.as_expr())),
            "global_scalar_candidates": [[2, 0], [1, 1]],
            "exact_crossover_excluded_for_integer_fluxes": True,
            "lightest_massive_mode_across_spins_is_scalar": True}


def main():
    k, m = sp.symbols("k m")
    exact = {}
    for levels in product(range(4), repeat=2):
        sectors = scalar_sectors((k, 20-k), levels, check_constraints=True)
        exact[str(levels)] = [str(sp.factor(sp.Matrix(matrix).charpoly(m).as_expr()))
                              for matrix in sectors if matrix]
    rows = []
    for curvature in (0.0001, 0.001, 0.01, 0.1, 0.5, 1, 2, 2.5, 3, 4, 5, 6, 7, 8, 9, 10):
        samples = [(spectrum((curvature, 20-curvature), levels)[0], levels)
                   for levels in product(range(13), repeat=2)]
        lightest, levels = min(samples)
        assert lightest > 0, (curvature, lightest, levels)
        candidates = [spectrum((curvature, 20-curvature), candidate)[0]
                      for candidate in ((2, 0), (1, 1))]
        assert abs(lightest-min(candidates)) < 1e-9
        rows.append({"loose_curvature": curvature, "lightest_in_window": float(lightest), "level": levels})
    data = {"all_level_factorizations": verify_factorizations(k, m),
            "global_gap_crossover": verify_gap_switch(k, m),
            "exact_low_blocks": exact, "finite_window_checks": rows}
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261116_D9_scalar_spectrum.json"
    output.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("Verified the gauge constraints and both scalar parity matrices.")


if __name__ == "__main__":
    main()
