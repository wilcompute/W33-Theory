"""Compare the electric STU radial path with the nearest E6 scalar geodesic."""

import json

import numpy as np
import sympy as sp

from toe_20261114_e6_attractor_torus import OUT as TORUS

OUT = TORUS.with_name("toe_20261114_e6_stu_radial.json")


def calculate():
    tau = sp.symbols("tau", nonnegative=True)
    q = sp.symbols("q1:4", positive=True)
    y = [a/(1 + a*tau) for a in q]
    y_mean = sum(y)/3
    velocity = sp.Matrix([y_mean - a for a in y])
    acceleration = velocity.diff(tau)
    determinant = sp.factor(sp.Matrix.hstack(sp.ones(3, 1), velocity, acceleration).det())
    vandermonde = sp.prod(y[j]-y[i] for i, j in [(0, 1), (0, 2), (1, 2)])
    assert sp.cancel(determinant + vandermonde) == 0
    # Dressed magnitudes equal a common factor times y, so the
    # gradient direction in the scalar plane is centered negative y squared.
    square_direction = acceleration
    assert sp.cancel(sp.Matrix.hstack(sp.ones(3, 1), velocity,
                                      -square_direction).det() - vandermonde) == 0
    assert sp.simplify(sum(velocity)) == sp.simplify(sum(acceleration)) == 0

    profile = json.loads(TORUS.read_text(encoding="utf-8"))
    chars = np.array(profile["characters"])
    cases = [(1, 2, 5), (1, 1, 5), (1, 1, 1), (.04, .12, .3)]
    controls = []
    for charges in cases:
        harmonic = 1 + np.array(charges)[:, None] * np.r_[0., np.geomspace(1e-5, 1e6, 512)]
        warp = np.prod(harmonic, axis=0)**(1/3)
        scalars = warp / harmonic
        bare = np.array(charges)[:, None]
        dressed = bare * scalars
        np.testing.assert_allclose(np.prod(scalars, axis=0), 1., atol=1e-13)
        np.testing.assert_allclose(np.prod(dressed, axis=0), np.prod(charges), rtol=1e-13)
        np.testing.assert_allclose(dressed[:, -1], np.prod(charges)**(1/3), rtol=2e-5)
        leading = np.cumsum(np.sort(chars @ dressed, axis=0)[::-1], axis=0)
        assert np.max(np.diff(leading[:3], axis=1)) < 1e-12
        controls.append(dict(charges=charges, horizon_magnitude=float(np.prod(charges)**(1/3)),
                             initial_curvature_determinant=str(determinant.subs(dict(zip(q, charges)),
                                                                                 simultaneous=True).subs(tau, 0)),
                             final_dressed=dressed[:, -1].tolist()))

    singular = []
    for count in (1, 2):
        exponents = [sp.Rational(count, 3)-int(i < count) for i in range(3)]
        assert sum(exponents) == 0
        distance_squared_coefficient = 3 * sum(a*a for a in exponents)
        assert distance_squared_coefficient == count * (3-count)
        singular.append(dict(nonzero_charges=count, scalar_exponents=list(map(str, exponents)),
                             distance_squared_log_coefficient=int(distance_squared_coefficient),
                             sphere_area_exponent=str(sp.Rational(count-3, 2)),
                             potential_exponent=str(2*sp.Rational(count-3, 3))))
    return dict(status="PASS", controls=controls, singular=singular)


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
