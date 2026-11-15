"""Exact Fermat slice and nodal root reflections for the cubic flux branch."""

import json
from collections import Counter
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp


def fermat_slice():
    coordinates = sp.symbols("z0:4")
    cubic = sum(z**3 for z in coordinates)
    monomial_basis = sp.Poly(sum(a*b*c for a in coordinates for b in coordinates for c in coordinates), *coordinates).monoms()
    infinitesimal_changes = [sp.Poly(zi*sp.diff(cubic, zj), *coordinates) for zi in coordinates for zj in coordinates]
    image = sp.Matrix([[change.coeff_monomial(m) for change in infinitesimal_changes] for m in monomial_basis])
    assert image.rank() == 16  # GL(4) includes polynomial rescaling.
    missing = [list(m) for m, row in zip(monomial_basis, image.tolist()) if not any(row)]
    assert len(missing) == 4
    assert all(sorted(m) == [0, 1, 1, 1] for m in missing)
    return missing


def nodal_reflections():
    basis = [tuple(int(i == j) for i in range(7)) for j in range(7)]
    h, *e = basis

    def add(a, b):
        return tuple(x+y for x, y in zip(a, b))

    def scale(a, factor):
        return tuple(factor*x for x in a)

    def sum_vectors(vectors):
        return tuple(map(sum, zip(*vectors)))

    def dot(a, b):
        return a[0]*b[0]-sum(x*y for x, y in zip(a[1:], b[1:]))

    flux = add(scale(h, 3), scale(sum_vectors(e), -1))
    roots = [add(a, scale(b, -1)) for a, b in permutations(e, 2)]
    roots += [scale(add(h, scale(sum_vectors(chosen), -1)), sign)
              for chosen in combinations(e, 3) for sign in (-1, 1)]
    roots += [scale(add(scale(h, 2), scale(sum_vectors(e), -1)), sign) for sign in (-1, 1)]
    lines = e + [add(h, scale(sum_vectors(chosen), -1)) for chosen in combinations(e, 2)]
    lines += [add(scale(h, 2), scale(sum_vectors(chosen), -1)) for chosen in combinations(e, 5)]
    line_set = set(lines)
    for root in roots:
        assert dot(root, root) == -2 and dot(root, flux) == 0
        reflected = {line: add(line, scale(root, dot(line, root))) for line in lines}
        assert set(reflected.values()) == line_set
        assert all(reflected[reflected[line]] == line for line in lines)
        by_pairing = Counter(dot(root, line) for line in lines)
        assert by_pairing == {-1: 6, 0: 15, 1: 6}
        assert all(dot(line, image) == 0 for line, image in reflected.items() if line != image)
        assert all(dot(flux, line) == dot(flux, image) == 1 for line, image in reflected.items())
    return len(roots)


if __name__ == "__main__":
    report = {
        "fermat_slice_monomial_powers": fermat_slice(),
        "massless_real_complex_structure_scalars_at_fixed_flux": 8,
        "nodal_root_reflections_checked": nodal_reflections(),
        "line_cycle_type_of_each_root_reflection": {"fixed": 15, "transpositions": 6},
        "flux_pairing_with_vanishing_root": 0,
    }
    result = json.dumps(report, indent=2) + "\n"
    path = Path(__file__).resolve().parents[1] / "data" / "toe_20261114_cubic_flux_moduli.json"
    path.write_text(result, encoding="utf-8", newline="\n")
    print(result, end="")
