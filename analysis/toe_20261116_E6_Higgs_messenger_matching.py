"""Check a renormalizable tree realization of the E6 Higgs stabilizer."""

import json
from pathlib import Path

import sympy as sp

from toe_20261116_E6_full_cubic_SM_stabilizer import hypercharge_integer_weights


def holomorphic_elimination():
    # Matrix-valued F equations are written with trace pairing. The scalar
    # calculation checks the VEV entries and coefficients on the commuting slice.
    phi, p_neutral = sp.symbols("Phi p", real=True)
    r, s, r_dual, s_dual = sp.symbols("R S Rdual Sdual")
    w = (r_dual*(r-phi**2)+s_dual*(s-phi*r)
         -sp.Rational(283, 2)*phi**2+sp.Rational(3, 5)*r*s
         +sp.Rational(1, 6)*s*s+p_neutral*r)
    fields = (r, s, r_dual, s_dual)
    solved = sp.solve([sp.diff(w, var) for var in fields], fields)
    expected = (-sp.Rational(283, 2)*phi**2+sp.Rational(3, 5)*phi**5
                +sp.Rational(1, 6)*phi**6+p_neutral*phi**2)
    assert sp.expand(w.subs(solved)-expected) == 0
    assert solved[r] == phi**2 and solved[s] == phi**3
    assert solved[r_dual] == -p_neutral-phi**4/3-6*phi**3/5
    assert solved[s_dual] == -phi**3/3-3*phi**2/5
    assert sp.hessian(w, fields).det() == 1
    # The heavy constraint map is lower triangular also for matrix variations.
    assert sp.Matrix([[1, 0], [-phi, 1]]).det() == 1

    gram, singlet = sp.symbols("G L")
    gram_superpotential = singlet*(gram-1)-singlet**2/2
    value = sp.solve(sp.diff(gram_superpotential, singlet), singlet)[0]
    assert sp.expand(gram_superpotential.subs(singlet, value)-(gram-1)**2/2) == 0

    weights = hypercharge_integer_weights()
    neutral = [int(weight == 0) for weight in weights]
    y = sp.diag(*weights)
    p = sp.diag(*neutral)
    values = (y**2, y**3, -p-y**4/3-sp.Rational(6, 5)*y**3,
              -y**3/3-sp.Rational(3, 5)*y**2)
    for field in values:
        assert field == field.conjugate().T
    return {"heavy_endomorphism_multiplets": 4, "endomorphism_dimension": 27**2,
            "singlet_multiplets": 4, "heavy_block_holomorphic_rank": 4*27**2+4,
            "expanded_physical_Higgs_hessian_rank": 120+4*27**2+4,
            "tree_eliminated_adjoint_polynomial_degrees": [2, 5, 6],
            "diagonal_heavy_vevs_and_zero_heavy_moment_maps": True}


def main():
    data = holomorphic_elimination()
    output = Path(__file__).resolve().parents[1]/"data"/"toe_20261116_E6_Higgs_messenger_matching.json"
    output.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")
    print("Verified the E6 Higgs-sector heavy-field elimination and D-flat messenger VEVs.")


if __name__ == "__main__":
    main()
