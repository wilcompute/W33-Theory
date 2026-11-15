"""Symbolic transfer spectrum on the positive electric STU branch."""
from collections import Counter
import json

import networkx as nx
import sympy as sp

from toe_20261114_e6_stu_five_tests import DICTIONARY, OLD, R, TORUS, flatten_columns, matrix_basis

OUT = OLD.with_name("toe_20261114_e6_stu_symbolic_transfer.json")


def support(a):
    return {(i, j) for i, j, _ in a.row_list()} | {(j, i) for i, j, _ in a.row_list()}


def calculate():
    cert, cubic, _, _, _ = R.load()
    algebra = matrix_basis(cert["cubic_27"]["generators"])
    columns = flatten_columns(algebra)
    triad = json.loads(TORUS.read_text())["native_coordinates"]
    signs = set(json.loads(DICTIONARY.read_text())["coordinate_negative_sign_indices"])
    q = sp.zeros(27, 1)
    for i in triad:
        q[i] = -1 if i in signs else 1
    basis = [sp.SparseMatrix(27, 27, columns*z)
             for z in sp.Matrix.hstack(*(a*q for a in algebra)).nullspace()]
    assert len(basis) == 52

    incidence = sp.Matrix([[int(i in term) for i in range(27)] for term in sorted(cubic)])
    diagonal = sp.Matrix.hstack(*incidence.nullspace())
    proj = diagonal*(diagonal.T*diagonal).inv()*diagonal.T
    weights = proj[:, triad[:2]]*proj[triad[:2], triad[:2]].inv()
    u, v = sp.symbols("u v", positive=True)
    d = [u**(-2*a)*v**(-2*b) for a, b in weights.tolist()]
    # q_boundary = D^-1 q; its positive coefficient magnitudes are therefore
    # u squared, v squared and their inverse product.
    magnitudes = [1/d[i] for i in triad]
    assert magnitudes == [u**2, v**2, 1/(u**2*v**2)]
    ratios = [a/b for i, a in enumerate(magnitudes) for b in magnitudes[i+1:]]
    gains = [sp.factor(4*r/(1+r)**2) for r in ratios]

    graph = nx.Graph()
    graph.add_nodes_from(range(len(basis)))
    owners = {}
    for k, a in enumerate(basis):
        for entry in support(a):
            if entry in owners:
                graph.add_edge(k, owners[entry])
            owners[entry] = k
    blocks = sorted(tuple(sorted(c)) for c in nx.connected_components(graph))
    assert Counter(map(len, blocks)) == {2: 24, 4: 1}

    x = sp.Symbol("x")
    f, g_scale = sp.symbols("f g", positive=True)
    radial_diagonal = [f**(2*a)*g_scale**(2*b) for a, b in weights.tolist()]
    records = Counter()
    for block in blocks:
        generators = [basis[k] for k in block]
        entries = sorted((i,j) for i,j in set().union(*map(support, generators)) if i <= j)
        horizon = sp.Matrix([[a[i,j]+a[j,i] for a in generators] for i,j in entries])
        boundary = sp.Matrix([[a[i,j]*d[j]/d[i]+a[j,i]*d[i]/d[j] for a in generators]
                              for i,j in entries])
        metric = sp.diag(*(1 if i == j else 2 for i,j in entries))
        g = boundary.T*metric*boundary
        h = horizon.T*metric*horizon
        radial = sp.Matrix([[a[i,j]*d[j]/d[i]*radial_diagonal[i]/radial_diagonal[j]
                             + a[j,i]*d[i]/d[j]*radial_diagonal[j]/radial_diagonal[i]
                             for a in generators] for i,j in entries])
        radial_gram = radial.T*metric*radial
        rank = horizon.rank()
        if all(sp.cancel(z) == 0 for z in g-h):
            assert rank < len(block) or h.det() > 0
            assert all(sp.cancel(z) == 0 for z in radial_gram-h)
            records[("unit", rank)] += 1
            continue
        assert len(block) == 2 and rank == 1
        det = sp.factor(g.det())
        polynomial = sp.factor((x*g-h).det()/det)
        p = next(i for i, gain in enumerate(gains) if sp.cancel(polynomial-x*(x-gain)) == 0)
        ratio = ratios[p]
        ratio_at_radius = ratio * [f**2/g_scale**2, f**4*g_scale**2, f**2*g_scale**4][p]
        even_gain = ratio*(1+ratio_at_radius)**2/(ratio_at_radius*(1+ratio)**2)
        odd_gain = ratio*(1-ratio_at_radius)**2/(ratio_at_radius*(1-ratio)**2)
        assert sp.cancel((x*g-radial_gram).det()/det - (x-even_gain)*(x-odd_gain)) == 0
        # Equality of boundary magnitudes leaves only the even direction.
        collision = [v, v**(-sp.Rational(1,2)), v**-2][p]
        radial_collision = [g_scale, g_scale**(-sp.Rational(1,2)), g_scale**-2][p]
        assert all(sp.simplify(z.subs({u: collision, f: radial_collision},
                                     simultaneous=True)) == 0 for z in radial_gram-h)
        determinant_factor = sp.cancel(det/(ratio-1/ratio)**2)
        assert determinant_factor.is_positive and not determinant_factor.free_symbols
        # On the matching collision curve, the block reverts to an isometry.
        collision = [v, v**(-sp.Rational(1,2)), v**-2][p]
        assert all(sp.simplify(z.subs(u, collision)) == 0 for z in g-h)
        records[("pair", p)] += 1
    assert records == {("unit", 1): 12, ("unit", 4): 1,
                       ("pair", 0): 4, ("pair", 1): 4, ("pair", 2): 4}
    a, b, c, tau, z = sp.symbols("a b c tau z", positive=True)
    denom = (1+a*tau)*(1+b*tau)
    surviving = (a+b+2*a*b*tau)**2/((a+b)**2*denom)
    decaying = 1/denom
    assert sp.limit(surviving, tau, sp.oo) == 4*a*b/(a+b)**2
    for gain, limit in [(surviving, (1+2*z)**2/(a*z*(1+z))),
                        (decaying, 1/(a*z*(1+z)))]:
        assert sp.cancel(sp.limit(gain.subs(tau, z/b)/b, b, 0)-limit) == 0
        assert sp.limit(gain, b, 0) == 1/(1+a*tau)
    area_squared = (1+a*tau)*(1+b*tau)*(1+c*tau)/tau**3
    assert sp.cancel(sp.limit(area_squared.subs(tau, z/b)/b, b, 0)-a*c*(1+z)/z) == 0

    return dict(status="PASS", blocks={f"{k}-{i}": n for (k, i), n in sorted(records.items())},
                squared_gain=[str(gain) for gain in gains], total_scalar_kernel=14,
                finite_radius_blocks_verified=True,
                double_scaling_squared_gains_over_small_charge=[
                    "(1+2*z)^2/(a*z*(1+z))", "1/(a*z*(1+z))"])


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result, flush=True)
