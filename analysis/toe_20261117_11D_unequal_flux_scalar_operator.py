"""Gauge-constrained sphere-singlet scalar pencil of AdS5 x S2 x S2 x T2."""

import json

import sympy as sp


def outer(vector):
    return vector*vector.T


def pencil(lam, asymmetry):
    """Return the positive kinetic matrix and symmetric mass matrix at lambda>0."""
    lam, asymmetry = map(sp.sympify, (lam, asymmetry))
    n = sp.Matrix([2, 2, 1])
    z1, z2 = sp.Matrix([-4, 0, -2]), sp.Matrix([0, -4, -2])
    k1, k2 = 6+2*asymmetry, 6-2*asymmetry
    flux = sp.Matrix([2*sp.sqrt(1+asymmetry), 2*sp.sqrt(1-asymmetry)])
    kinetic_scalars = sp.diag(4, 4, 2)+outer(n)/2
    hessian = (
        -2*k1*outer(-n/2-sp.Matrix([2, 0, 0]))
        -2*k2*outer(-n/2-sp.Matrix([0, 2, 0]))
        +8*outer(-n/2-sp.Matrix([4, 4, 0]))
        +2*(1+asymmetry)*outer(z1)+2*(1-asymmetry)*outer(z2)
    )
    mixing = -sp.sqrt(lam)*sp.Matrix.hstack(flux[0]*z1, flux[1]*z2)
    flux_outer = outer(flux)
    kinetic_axions = sp.eye(2)-3*flux_outer/(8*(lam+3))
    mass_axions = lam*sp.eye(2)+5*lam*flux_outer/(8*(lam+3))
    kinetic = sp.diag(kinetic_scalars, kinetic_axions)
    mass = (lam*kinetic_scalars+hessian).row_join(mixing).col_join(
        mixing.T.row_join(mass_axions)
    )
    return kinetic, mass


def verify():
    lam, k, d, z = sp.symbols("lambda k d z", real=True)
    kinetic, mass = pencil(lam, d)
    assert sp.simplify(kinetic[3:, 3:].det()-lam/(lam+3)) == 0
    kin_eq, mass_eq = pencil(lam, 0)
    # The normalizations (beta1-beta2) and (a1-a2) span the known odd sector.
    odd = sp.Matrix([[1, 0], [-1, 0], [0, 0], [0, 1], [0, -1]])
    odd_determinant = sp.factor((odd.T*(mass_eq-z*kin_eq)*odd).det())
    assert sp.expand(odd_determinant/16-((lam-4-z)*(lam-z)-16*lam)) == 0
    bf = (mass+4*kinetic).subs(sp.sqrt(lam), k).subs(lam, k*k)
    determinant = sp.factor(bf.det(method="domain-ge").subs(k*k, lam))
    positive = (lam**4+40*lam**3+(336-80*d*d)*lam**2
                +(2304-896*d*d)*lam+3840*d*d)
    assert sp.simplify(determinant-72*lam*(lam-12)*positive/(lam+3)) == 0
    sample_bf = (mass_eq+4*kin_eq).subs(lam, 1)
    pivots = [sample_bf[:i, :i].det() for i in range(6)]
    assert all(pivots) and sum(1 for i in range(1, 6) if pivots[i]*pivots[i-1] < 0) == 1
    threshold = (mass+4*kinetic).subs(lam, 12)
    normalized = sp.Matrix([1, (d-9)/(d+9), 4*d/(d+9), -sp.sqrt(3*(1+d)),
                            sp.sqrt(3*(1-d))*(9-d)/(d+9)])
    assert (threshold*normalized).applyfunc(sp.simplify) == sp.zeros(5, 1)
    characteristic = sp.factor(
        (mass-z*kinetic).subs(sp.sqrt(lam), k).subs(lam, k*k).det(method="domain-ge")
    )
    static_determinant = sp.factor(characteristic.subs(z, 0).subs(k*k, lam))
    assert sp.simplify(static_determinant-72*lam**4*(lam**2+8*lam-560-80*d*d)/(lam+3)) == 0
    limit = sp.factor(sp.limit(characteristic / kinetic.det().subs(lam, k*k), k, 0))
    assert sp.expand(limit+z*z*(z-32)*(z*z-8*z-48-80*d*d)) == 0
    a, vs = sp.symbols("A V_s")
    trace = (5+3*z/lam)*a
    axial_constraint = -4*(lam+3)*a
    # The x-x equation follows from the other scalar Einstein constraints.
    assert sp.expand((lam*trace/2+axial_constraint+3*vs/4).subs(
        vs, 2*(lam-z+8)*a
    )) == 0
    return {"equal_flux_sphere_odd_characteristic_polynomial": str(odd_determinant/16),
            "BF_determinant_at_arbitrary_flux": str(determinant),
            "strictly_positive_factor_for_lambda_positive": str(positive),
            "exact_LDL_sample_pivots_as_successive_principal_determinants": list(map(str, pivots)),
            "BF_saturating_vector_at_lambda_12": list(map(str, normalized)),
            "static_marginal_mode_determinant": str(static_determinant),
            "positive_static_threshold": str(-4+4*sp.sqrt(36+5*d*d)),
            "nonzero_momentum_characteristic_polynomial_limit_at_lambda_zero": str(limit),
            "BF_violating_scalar_count_per_signed_momentum": {
                "0<lambda<12": 1, "lambda>=12": 0
            }}


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
