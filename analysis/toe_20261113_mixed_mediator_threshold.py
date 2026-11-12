"""Exact mixed-cubic thresholds at the canonical flat W33 vacuum."""

from itertools import combinations
import json

import numpy as np
import sympy as sp

import toe_20261112_canonical_uv_fixed_point as uv


OUT = 'data/toe_20261113_mixed_mediator_threshold.json'


def one_adjoint_obstruction(internal, cartan):
    """A family-neutral singlet source vanishes while the adjoint square survives."""
    roots = internal[np.any(internal != np.array([np.diag(g.diagonal()) for g in internal]), axis=(1, 2))]
    i, j = next((i, j) for i, j in combinations(range(27), 2)
                if not roots[:, i, j].any() and not roots[:, j, i].any()
                and not np.array_equal(cartan[:, i], cartan[:, j]))
    x = np.eye(27, dtype=np.int64)[i] + np.eye(27, dtype=np.int64)[j]
    z = np.eye(27, dtype=np.int64)[i] - np.eye(27, dtype=np.int64)[j]
    assert z @ x == 0 and not np.einsum('i,aij,j->a', z, roots, x).any()
    gram = sp.Matrix(cartan @ cartan.T)
    source = sp.Matrix(cartan @ (z*x))
    norm_squared = (source.T * gram.inv() * source)[0]
    assert norm_squared > 0
    return dict(internal_indices=[i, j], singlet_source=0, adjoint_square=str(norm_squared))


def threshold():
    a, b, c, j = sp.symbols('a b c j')
    mass, mixing, coupling = 4, 3, sp.Rational(5, 3)
    w = mass*b*c-mixing*a*c+coupling*b*j
    eliminated = sp.solve([sp.diff(w, b), sp.diff(w, c)], [b, c])
    assert eliminated == {b: 3*a/4, c: -5*j/12}
    assert sp.expand(w.subs(eliminated).subs(a, 4*a/5)) == a*j
    assert sp.Rational(4, 5)**2+sp.Rational(3, 5)**2 == 1
    assert sp.hessian(w, (b, c)).det() == -mass**2
    unbroken_mass = sp.hessian(w.subs(j, 0), (a, b, c))
    assert sorted(unbroken_mass.eigenvals()) == [-5, 0, 5]
    single = mass*b*b/2-mixing*a*b+coupling*b*j
    eliminated_single = sp.solve(sp.diff(single, b), b)[0]
    assert sp.expand(single.subs(b, eliminated_single)).coeff(j, 2) == -coupling**2/(2*mass)
    return dict(mass_input=mass, mixing_input=mixing, cubic_input=str(coupling),
                light_old_and_mediator_components=['4/5', '3/5'],
                unbroken_heavy_singular_mass=5, normalized_mixed_cubic=1)


def uncoupled_adjoint_uv():
    """Conserved-current obstruction if the degree-five C primary survives."""
    a, b, c, t, u = sp.symbols('a b c t u', real=True)
    remaining_x = (11-a-b-4*c)/3
    s = (12*(a+b+c)-21)/5
    dims = [81]*5 + [78]*3 + [10]
    cases = []
    for omega, weight in [(True, 226), (False, 376)]:
        paired_x = [(2-remaining_x)/2+t, (2-remaining_x)/2-t] if omega else [t, u]
        x, y = paired_x
        charges = [x, y, remaining_x, 2-a-x, 2-b-y, a, b, c, s]
        sigma = sum(charges[:5])
        assert sp.expand(3*sigma+4*(a+b+c)) == 23
        assert sp.expand(9*sigma+5*s) == 48

        def trace(parameter):
            return sp.expand(sum(dim*(q-1)*sp.diff(q, parameter)**2
                                 for dim, q in zip(dims, charges)))

        if omega:
            assert trace(t) == -81*a-81*b
        else:
            assert trace(t) == -81*a and trace(u) == -81*b
        bare = trace(c)
        assert sp.expand(bare-6*(weight*(a+b)+101*c+27)/25) == 0
        correction = 25*(sp.Rational(2, 3)-5*c)
        corrected = sp.expand(bare+correction)
        assert corrected.coeff(c) < 0
        assert corrected.coeff(a) == corrected.coeff(b) > 0
        assert corrected.subs({a: 0, b: 0, c: 0}) > 0
        cases.append(dict(alternating_cubic=omega, bare_C_current_trace=str(bare),
                          C_current_trace_with_free_quintic=str(corrected)))
    return cases


def calculate():
    flat = uv.flat
    gauge, internal, cartan, _, _, y = flat.compact_chart()
    x, z = flat.repair_vevs()
    # Target the pair complementary to Z1 A (X0+X1).
    assert not np.einsum('i,aij,j->a', z[0], gauge[:78], x[2]).any()
    assert not (x[2]*np.repeat(y, 3)).any() and not (z[0]*np.repeat(y, 3)).any()
    mixed = sp.Matrix([[0, 0, 0], [1, 1, 0]])
    target = sp.Matrix([[0, 0, 1], [0, 0, 0]])
    assert mixed.rank() == 1 and (mixed+target).rank() == 2
    base = sp.Matrix(flat.read(uv.OUT)['one_loop_b0'])
    entries = flat.read(uv.THETA)['spin_witness']['representations']
    bifund = sp.Matrix(entries['27_tensor_3']['basic_trace_indices']) / 2
    adjoint = sp.Matrix(entries['E6_adjoint']['basic_trace_indices']) / 2
    adjoint_beta, bifund_beta = base-2*adjoint, base-2*bifund
    assert list(adjoint_beta) == [-45, -66] and list(bifund_beta) == [-39, -93]
    return dict(status='PASS', threshold=threshold(),
                mixed_rank_before_after=[1, 2],
                adjoint_pair_b0=list(map(int, adjoint_beta)),
                bifundamental_pair_b0=list(map(int, bifund_beta)),
                one_adjoint_obstruction=one_adjoint_obstruction(internal, cartan),
                two_adjoint_UV_tests=uncoupled_adjoint_uv())


if __name__ == '__main__':
    result = json.dumps(calculate(), indent=2) + '\n'
    (uv.flat.ROOT / OUT).write_text(result, encoding='utf-8')
    print(result)
