"""Check the continuum KK overlap sum rule against positive graph regulators."""

import json
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_kk_graph_sum_rule.json"


def check_graph(adjacency, mode, measure, label):
    n = len(mode)
    edges = [(i, j) for i, j in combinations(range(n), 2) if adjacency[i][j]]
    laplacian = [sum(a * (mode[i] - mode[j]) for j, a in enumerate(row))
                 for i, row in enumerate(adjacency)]
    k = next(i for i, v in enumerate(mode) if v)
    mass = Fraction(laplacian[k], mode[k])
    assert mass > 0 and all(y == mass*f for y, f in zip(laplacian, mode, strict=True))
    quartic = measure * sum(f**4 for f in mode)
    weighted_exchange = measure * sum(adjacency[i][j] * (mode[i]**2-mode[j]**2)**2
                                      for i, j in edges)
    defect = measure * sum(adjacency[i][j] * (mode[i]-mode[j])**4 for i, j in edges)
    assert 4*mass*quartic - 3*weighted_exchange == defect > 0
    return dict(graph=label, sites=n, edges=len(edges), mass=str(mass),
                normalized_defect=str(defect/(4*mass*quartic)))


def calculate():
    a, b, x = sp.symbols("a b x")
    assert sp.expand(4*(a-b)*(a**3-b**3) - 3*(a*a-b*b)**2 - (a-b)**4) == 0
    sites = list(product(range(4), repeat=2))
    moves = {(a % 4, b % 4) for a, b in product((-2, -1, 1, 2), repeat=2)
             if abs(a) + abs(b) == 3}
    knight = [[int(((a-c) % 4, (b-d) % 4) in moves) for c, d in sites] for a, b in sites]
    assert all(sum(row) == 4 for row in knight)
    knight_result = check_graph(knight, [(-1)**(a+b) for a, b in sites],
                                Fraction(1, 16), "4x4 toroidal knight")
    assert knight_result["normalized_defect"] == "1"

    def pairing(u, v):
        return (u[0]*v[1]-u[1]*v[0]+u[2]*v[3]-u[3]*v[2]) % 3

    points = [v for v in product(range(3), repeat=4) if next((a for a in v if a), 0) == 1]
    w33 = [[int(i != j and pairing(u, v) == 0) for j, v in enumerate(points)]
           for i, u in enumerate(points)]
    mat = sp.Matrix(w33)
    assert mat.shape == (40, 40) and set(map(sum, w33)) == {12}
    identity = sp.eye(40)
    projected = (mat-2*identity)*(mat-12*identity)*identity[:, 0]
    w33_result = check_graph(w33, list(map(int, projected)), Fraction(1, 40), "W(3,3) point graph")

    # Smooth axisymmetric l=1 mode of either sphere using unit volume measure.
    f = sp.sqrt(3)*x
    avg = lambda expr: sp.integrate(expr, (x, -1, 1))/2
    degree_two = sp.sqrt(5)*(3*x*x-1)/2
    assert sp.expand(f*f-1-2*degree_two/sp.sqrt(5)) == 0
    assert avg(f**4) == sp.Rational(9, 5)
    assert 4*2*avg(f**4) == 3*6*avg(f*f*degree_two)**2

    return dict(status="PASS", graph_controls=[knight_result, w33_result],
                smooth_sphere=dict(mass_r_squared=2, quartic="9/5",
                                   exchange_r_squared="24/5", defect=0),
                cycle_relative_defect="sin(pi/N)^2 for the first real Fourier mode, N>=5")


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
