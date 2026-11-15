"""Check local photon cones for magnetic potentials preserving D9 static shape."""

import json
from itertools import combinations
from pathlib import Path

import sympy as sp


def verify():
    ba, bb, x, y, t, p, s = sp.symbols("B_a B_b X Y T P s", positive=True)
    gamma, k, omega, amplitude = sp.symbols("gamma k omega epsilon", real=True)
    longitudinal, a2, a3, a4 = sp.symbols("a_long a2 a3 a4", real=True)
    fields = {(1, 2): ba, (3, 4): bb, (0, 1): amplitude * longitudinal}
    for index, polarization in enumerate((a2, a3, a4), start=2):
        fields[0, index] = -amplitude * omega * polarization
        fields[1, index] = fields.get((1, index), 0) + amplitude * k * polarization

    def component(i, j):
        return fields.get((i, j), 0)

    invariant_t = sum((-1 if i == 0 else 1)*f**2 for (i, _), f in fields.items())
    invariant_p = 0
    for i, j, m, n in combinations(range(5), 4):
        pfaffian = (component(i, j)*component(m, n) - component(i, m)*component(j, n)
                    + component(i, n)*component(j, m))
        invariant_p += (-1 if i == 0 else 1)*pfaffian**2

    background = {x: ba**2, y: bb**2}
    first_correction = (x+y)**4*x*y
    electric = sp.diff(first_correction, x)
    delta_parallel = 2*x*sp.diff(first_correction, x, 2)
    cross_magnetic = 4*(x+y)**3*x*y
    delta_cross = (x+y)**4*x
    quadratic = sp.expand(-invariant_t/2 - gamma*invariant_t**4*invariant_p).coeff(amplitude, 2)
    hessian = sp.hessian(quadratic, (longitudinal, a2, a3, a4))
    expected = sp.diag(
        1+2*gamma*electric,
        (1+2*gamma*electric)*omega**2-(1+2*gamma*(electric+delta_parallel))*k**2,
        *([(1+2*gamma*(cross_magnetic+delta_cross))*omega**2-(1+2*gamma*cross_magnetic)*k**2]*2),
    )
    assert (hessian-expected.subs(background)).applyfunc(sp.factor) == sp.zeros(4)

    # The determinant energy has the same speed for both tested polarizations.
    born = (sp.sqrt(1+s*t+s*s*p)-1)/s
    born_xy = born.subs({t:x+y, p:x*y})
    assert sp.simplify(1+2*x*sp.diff(born_xy, x, 2)/sp.diff(born_xy, x)-1/(1+s*x)) == 0
    assert sp.simplify((sp.diff(born, t)/(sp.diff(born, t)+x*sp.diff(born, p)))-1/(1+s*x)) == 0

    def sample(coupling):
        rules = {x: sp.Rational(1, 4), y: sp.Rational(1, 9), gamma: coupling}
        speeds = [
            (1+2*gamma*(electric+delta_parallel))/(1+2*gamma*electric),
            (1+2*gamma*cross_magnetic)/(1+2*gamma*(cross_magnetic+delta_cross)),
        ]
        return [sp.factor(speed.subs(rules)) for speed in speeds]

    positive = sample(sp.Rational(1, 10))
    negative = sample(sp.Rational(-1, 10))
    assert positive[0] > 1 > positive[1] > 0
    assert negative[1] > 1 > negative[0] > 0
    return {
        "squared_speeds": ["1 + 2*X*W_XX/W_X", "W_T/(W_T+X*W_P)"],
        "born_infeld_squared_speeds": ["1/(1+s*X)"]*2,
        "example_X_Y": ["1/4", "1/9"],
        "gamma_positive_squared_speeds": [str(value) for value in positive],
        "gamma_negative_squared_speeds": [str(value) for value in negative],
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_d9_protected_photon_cones.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
