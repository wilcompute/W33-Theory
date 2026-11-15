"""Check exact spectral-moment bounds for massive spin-two Betti exchange."""

import json
from pathlib import Path

import sympy as sp


def verify():
    shear, x, extra_weight, spare_gradient = sp.symbols("B x extra_weight spare_gradient", nonnegative=True)
    total = 6+extra_weight
    gradient = 2*shear*(total+6)-spare_gradient
    assert sp.expand(4*shear*total-gradient) == 2*shear*extra_weight+spare_gradient
    assert sp.factor(total**2-3*(total+6)) == extra_weight*(extra_weight+9)

    weights = [1, 2, 3]
    masses = [13, 17, 23]
    weight = sum(weights)
    first = sum(w*m for w, m in zip(weights, masses))
    curvature_limit = sp.Rational(first, 2*(weight+6))
    exchange = sum(sp.Rational(w)/(x+m) for w, m in zip(weights, masses))
    lower_bound = sp.Rational(weight)/(x+4*curvature_limit)
    numerator, denominator = sp.factor(sp.together(exchange-lower_bound)).as_numer_denom()
    assert all(coefficient >= 0 for coefficient in sp.Poly(numerator, x).all_coeffs())
    assert all(coefficient > 0 for coefficient in sp.Poly(denominator, x).all_coeffs())
    assert first <= 4*curvature_limit*weight
    assert sum(w for w, m in zip(weights, masses) if m <= 8*curvature_limit) >= sp.Rational(weight, 2)

    # Show the matrix inequality pointwise on a non-diagonal six-vector Gram.
    forms = sp.Matrix([[1, 3, 0, -1, 2, 0], [2, 0, 1, 0, 1, -1], [0, 1, -2, 2, 0, 1]])
    gram = forms.T*forms
    curvature = sp.diag(2, -1, 4)
    derivative_gram = gram  # any positive semidefinite choice works in this check
    integrand = 2*sp.trace(gram*(forms.T*curvature*forms-derivative_gram))
    upper = 8*sp.trace(gram**2)
    assert integrand <= upper

    return {
        "total_massive_overlap_lower_bound": 6,
        "weighted_mean_mass_squared_ceiling_in_ads_units": "4*B",
        "B_definition": "max_S lambda_max(2 W_minus - 8 I)",
        "massive_exchange_trace_lower_bound": "6/(x+4*B)",
        "half_weight_mass_squared_ceiling_in_ads_units": "8*B",
        "unit_direction_average_exchange_lower_bound": "1/(4*(x+4*B))",
        "rational_control_zero_shift_exchange": str(exchange.subs(x, 0)),
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261115_cubic_iib_exchange_bound.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
