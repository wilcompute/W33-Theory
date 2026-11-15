"""Verify homogeneous D9 radion response to an external KK mass source."""

import json
from pathlib import Path

import sympy as sp


def verify():
    u, v, delta, z, source = sp.symbols("u v delta z J", real=True)
    angular_eigenvalue = sp.Symbol("n", positive=True)
    # Normalize A+B=1. The internal Einstein equations give f_i^2=2 A_i+2/5.
    curvatures = ((1 + delta) / 2, (1 - delta) / 2)
    log_radii = (u + v, u - v)
    volume = sp.exp(-8 * u / 3)
    potential = volume * sum(
        -2 * curvature * sp.exp(-2 * beta)
        + (curvature + sp.Rational(1, 5)) * sp.exp(-4 * beta)
        for curvature, beta in zip(curvatures, log_radii)
    )
    mass = volume * sum(
        weight * sp.exp(-2 * beta)
        for weight, beta in zip(((1 + z) / 2, (1 - z) / 2), log_radii)
    )
    origin = {u: 0, v: 0}
    assert sp.Matrix([sp.diff(potential, x) for x in (u, v)]).subs(origin) == sp.zeros(2, 1)
    # L^2=20 in these units. The known kinetic metric is diag(56/3,8).
    curvature = (20 * sp.hessian(potential, (u, v))).subs(origin)
    gradient = sp.Matrix([sp.diff(mass, x) for x in (u, v)]).subs(origin)
    susceptibility = sp.factor((gradient.T * curvature.inv() * gradient)[0])
    expected = sp.Rational(7, 120) * (1 + 5 * (z - delta)**2 / (21 - 5 * delta**2))
    assert sp.simplify(susceptibility - expected) == 0
    assert (curvature.inv() * gradient.subs(z, delta)).applyfunc(sp.simplify) == sp.Matrix([-sp.Rational(1, 80), 0])

    laplacian = sp.Symbol("x", nonnegative=True)
    response_matrix = curvature + laplacian * sp.diag(sp.Rational(56, 3), 8)
    shape_response = sp.factor(-(response_matrix.inv() * gradient.subs(z, delta))[1])
    expected_shape = sp.Rational(1, 4) * delta * laplacian / (
        (laplacian + 20) * (laplacian + 36) - sp.Rational(1200, 7) * delta**2
    )
    assert sp.simplify(shape_response - expected_shape) == 0

    sourced = potential + source * angular_eigenvalue * mass.subs(z, delta)
    volume_force = sp.diff(sourced, u).subs(v, 0)
    shape_force = sp.diff(sourced, v).subs(v, 0)
    assert sp.simplify(shape_force - 3 * delta * volume_force / 7) == 0
    # Factor the stationarity equation before substituting the logarithmic branch.
    force = sp.simplify(volume_force * sp.exp(20 * u / 3) * 3 / 28)
    assert sp.simplify(force - ((1 - source * angular_eigenvalue / 2) * sp.exp(2 * u) - 1)) == 0

    return {
        "H_times_L_squared": [[str(entry) for entry in row] for row in curvature.tolist()],
        "static_log_mass_susceptibility_per_L_squared": str(expected),
        "equal_angular_degrees": {
            "static_log_mass_susceptibility_per_L_squared": "7/120",
            "inverse_HL_squared_times_log_mass_gradient": ["-1/80", "0"],
            "shape_response_per_log_mass_source_per_L_squared": str(expected_shape),
            "homogeneous_sourced_stationary_branch": "v=0, exp(2*u)=1/(1-J*n/2)",
            "sourced_potential_parameter_range": "J*n < 2",
            "mixed_11_spin2_m2_L2": 40,
            "mixed_22_spin2_m2_L2": 120,
        },
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    output = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_d9_radion_response.json"
    output.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
