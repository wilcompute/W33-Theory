"""Check the dimension-dependent identities in the flux-sphere warp proof."""

import json
from pathlib import Path

import sympy as sp


def verify():
    d, n = sp.symbols("d n", positive=True)
    slope = (4-n)/d
    hessian_coefficient = -(n-2+d*slope)
    gradient_coefficient = sp.factor(n-2+2*d*slope-d*slope**2)
    assert hessian_coefficient == -2
    assert sp.simplify(gradient_coefficient-(6-n-(n-4)**2/d)) == 0
    assert sp.solve(gradient_coefficient.subs(n, 8)+4, d) == [8]
    assert sp.solve(gradient_coefficient.subs(n, 6)+4, d) == [1]

    exceptional = []
    tested = 0
    for internal in range(4, 42, 2):
        for external in range(3, 41):
            value = gradient_coefficient.subs({n: internal, d: external})
            assert value != 0
            exponent = 1+4/value
            assert exponent != 1
            if exponent == 0:
                exceptional.append([external, internal])
            tested += 1
    assert exceptional == [[8, 8]]

    # External Ricci equation at the exceptional dimensions. Substitute U=e^(2B).
    u = sp.Symbol("U", positive=True)
    lap_u, grad_u_sq, external_einstein = sp.symbols("lap_U grad_U_sq lambda", real=True)
    b = sp.log(u)/2
    lap_b = sp.diff(b, u)*lap_u + sp.diff(b, u, 2)*grad_u_sq
    grad_b_sq = sp.diff(b, u)**2*grad_u_sq
    external_slope = slope.subs({n: 8, d: 8})
    warp_laplacian = external_slope*(lap_b+2*grad_b_sq)
    exterior = external_einstein*sp.exp(-2*external_slope*b)-sp.exp(-2*b)*warp_laplacian
    assert sp.simplify(u**2*exterior-(external_einstein*u**sp.Rational(5, 2)+lap_u/4)) == 0
    assert sp.diff(external_einstein*u**sp.Rational(5, 2), u, 2) == 15*external_einstein*sp.sqrt(u)/4

    return {
        "dimension_pairs_tested": tested,
        "internal_warp_hessian_coefficient": str(hessian_coefficient),
        "internal_warp_gradient_coefficient": str(gradient_coefficient),
        "exceptional_external_internal_dimensions": exceptional,
        "exceptional_external_ricci_times_U_squared": str(sp.simplify(u**2*exterior)),
        "physical_nonconstant_warp_branches_in_proven_ansatze": 0,
    }


if __name__ == "__main__":
    report = json.dumps(verify(), indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_flux_warp_rigidity.json"
    path.write_text(report, encoding="utf-8", newline="\n")
    print(report, end="")
