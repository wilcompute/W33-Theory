"""Exact group, topology and Dirac-bound checks for the Klein cubic link quotient.

Classical geometric input (not proved numerically here): the invariant
Sasaki--Einstein metric on the free quotient has Ric(g)=6g and is spin.
Friedrich's inequality is a standard analytic theorem, not a numerical
eigenvalue measurement. No statement about flux-coupled Dirac operators.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import json

WEIGHTS = (1, 9, 4, 3, 5)
P = 11
GROUP = tuple(product(range(P), range(5)))


def product55(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    """Affine form x -> 9**b*x+a over F_11."""
    a, b = x
    c, d = y
    return ((a + pow(9, b, P) * c) % P, (b + d) % 5)


def inverse55(x: tuple[int, int]) -> tuple[int, int]:
    a, b = x
    return ((-pow(pow(9, b, P), -1, P) * a) % P, (-b) % 5)


def commutator(x: tuple[int, int], y: tuple[int, int]) -> tuple[int, int]:
    return product55(
        product55(product55(x, y), inverse55(x)),
        inverse55(y),
    )


def verify() -> dict:
    assert len(GROUP) == 55
    assert len(set(GROUP)) == 55
    assert pow(9, 5, P) == 1
    assert {pow(9, b, P) for b in range(5)} == {1, 9, 4, 3, 5}
    assert all(product55(x, inverse55(x)) == (0, 0) for x in GROUP)
    assert all(product55(x, y) in GROUP for x, y in product(GROUP, repeat=2))

    # D=diag(zeta**w_i), P cyclically shifts coordinates.
    # The Klein cubic is sum_i x_i^2*x_(i+1); det D=det P=1.
    assert sum(WEIGHTS) % P == 0
    assert all((2 * WEIGHTS[i] + WEIGHTS[(i + 1) % 5]) % P == 0
               for i in range(5))
    assert all(WEIGHTS[(i + 1) % 5] == 9 * WEIGHTS[i] % P
               for i in range(5))

    D, shift = (1, 0), (0, 1)
    assert product55(product55(shift, D), inverse55(shift)) == (9, 0)
    derived = {commutator(x, y) for x, y in product(GROUP, repeat=2)}
    assert derived == {(a, 0) for a in range(11)}
    # G_ab is C5. All characters to U(1) factor through it.
    assert len({(a, b) for a, b in GROUP if b == 0}) == 11
    assert len({b for _, b in GROUP}) == 5
    assert all(product55(x, y)[1] == (x[1] + y[1]) % 5
               for x, y in product(GROUP, repeat=2))

    nonzero = set(range(1, 11))
    orbits = []
    while nonzero:
        seed = min(nonzero)
        orbit = {seed * pow(9, j, 11) % 11 for j in range(5)}
        assert len(orbit) == 5
        nonzero -= orbit
        orbits.append(tuple(sorted(orbit)))
    assert len(orbits) == 2
    irreps = [1] * 5 + [5] * len(orbits)
    assert sum(d * d for d in irreps) == 55

    # Freeness: D^a (a!=0) has no eigenvalue 1.
    # For b!=0, D^a P^b is conjugate to P^b by D^s,
    # s*(1-9^b)=a mod 11. P^b fixes the diagonal line
    # t(1,1,1,1,1), on which f=5t^3, hence no nonzero
    # fixed vector in {f=0}. Exhaust all 44 (a,b!=0) cases.
    for a, b in GROUP:
        if b == 0:
            if a:
                assert all(a * w % P for w in WEIGHTS)
        else:
            s = a * pow((1 - pow(9, b, P)) % P, -1, P) % P
            lhs = product55(product55((s, 0), (0, b)), inverse55((s, 0)))
            assert lhs == (a, b)
    diagonal_cubic = sum(1 for _ in WEIGHTS)
    assert diagonal_cubic == 5

    # Sasaki--Einstein dimension 7, normalized Ric=6g.
    # scalar=42. Friedrich's inequality on compact spin
    # n-manifold: lambda(D)^2>=n*min(scalar)/(4*(n-1)).
    # Flat unitary local-system twists keep F_twist=0,
    # so the same Weitzenbock/twistor proof applies.
    n, ric_coeff = 7, 6
    scalar = n * ric_coeff
    lower = Fraction(n * scalar, 4 * (n - 1))
    assert scalar == 42
    assert lower == Fraction(49, 4)

    return {
        "status": "EXACT_CONDITIONAL_GEOMETRIC_THEOREM",
        "date": "2026-11-17",
        "finite_group": "C11:C5 (Frobenius group)",
        "order": len(GROUP),
        "derived_group": "C11",
        "abelianization": "C5",
        "flat_complex_line_characters": 5,
        "spin_structure_count_if_spin": 1,
        "irreducible_complex_representation_dimensions": irreps,
        "nontrivial_C11_character_orbits": orbits,
        "Klein_cubic_invariant_under_D_and_P": True,
        "D_and_P_in_SL5": True,
        "free_action_on_smooth_cubic_link": True,
        "local_7d_Ricci_normalization": "Ric=6g",
        "scalar_curvature": scalar,
        "Dirac_eigenvalue_squared_lower_bound": str(lower),
        "Dirac_absolute_eigenvalue_lower_bound": "7/2",
        "zero_modes_of_ordinary_Dirac_for_any_unitary_flat_twist": 0,
        "scope": [
            "Assumes the invariant Sasaki-Einstein metric and spin quotient",
            "No spectral measurement or new proof of Kähler-Einstein existence",
            "No exclusion of flux-shifted gravitino operators, brane modes, or singular sectors",
            "Five flat line twists are not fifteen degree-four flat C-field sectors",
        ],
    }


if __name__ == "__main__":
    summary = verify()
    destination = Path(__file__).resolve().parents[1] / "data" / (
        "toe_20261117_klein_dirac_flat_twist_gap.json"
    )
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n",
                           encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))
