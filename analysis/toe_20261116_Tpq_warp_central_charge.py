"""Verify the fixed-Page cubic anomaly and non-axisymmetric warp splitting."""

import json
from pathlib import Path

import sympy as sp

from toe_20261116_Tpq_coupled_warp_branch import metric_response, numerical_branch, scalar_reduction


def anomaly_checks():
    detuning, amplitude = sp.symbols("t epsilon")
    kinetic = sp.Rational(80, 3)
    coupling = sp.Rational(256, 3)
    norm_per_volume = sp.Rational(1, 5)
    relative_integral = kinetic*norm_per_volume/8*(
        detuning*amplitude**2/2-coupling*amplitude**3/3
    )
    shift = sp.expand(relative_integral.subs(amplitude, detuning/coupling))
    assert shift == detuning**3/65536
    return "-(32-lambda)^3/65536"


def static_multiplet():
    t = sp.Symbol("t")
    axial = sp.diag(-sp.Rational(1, 2), -sp.Rational(1, 2), 1)
    identity = sp.eye(3)

    def tensor(i, j):
        return identity[:, i]*identity[:, j].T+identity[:, j]*identity[:, i].T

    angular_basis = (axial, tensor(0, 2), tensor(1, 2), tensor(0, 1), sp.diag(1, -1, 0))
    predicted = (-t, 0, 0, 3*t, 3*t)
    for variation, eigenvalue in zip(angular_basis, predicted):
        image = t*(variation-2*(axial*variation+variation*axial
                                -sp.Rational(2, 3)*sp.trace(axial*variation)*identity))
        assert image == eigenvalue*variation
    return [str(level) for level in predicted]


def main():
    x, y = scalar_reduction()
    metric = metric_response(x, y)
    examples = []
    for p, q in ((7, 8), (8, 9), (38, 43)):
        row = numerical_branch(p, q, metric, 8)
        page = row["page_integral_relative_shift"]
        graviton = row["graviton_integral_relative_shift"]
        exact_ratio_shift = (graviton-2*page-page*page)/(1+page)**2
        cubic = row["lambda_minus_32"]**3/65536
        assert abs(exact_ratio_shift/cubic-1) < 0.05, (p, q, exact_ratio_shift, cubic)
        examples.append({"chern_pair": [p, q], "central_charge_relative_shift": exact_ratio_shift,
                         "leading_cubic_shift": cubic, "numerical_over_cubic": exact_ratio_shift/cubic})
    data = {"central_charge_leading_relative_shift": anomaly_checks(),
            "warped_static_quadrupole_derivatives_to_first_order": static_multiplet(),
            "detuning_variable": "t=32-lambda", "examples": examples}
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_Tpq_warp_central_charge.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the fixed-Page cubic central charge and static quadrupole splitting.")


if __name__ == "__main__":
    main()
