"""Explicit native-cover/knight/Clifford maps, extending the May29 owner.

Prior owners: w33_cl4_q4_hypercube_network_unification.py (Boolean lattice,
Pascal row and knight Q4); w33_pass5316_latin_knight_q4_affine_derivative_census.py
(affine colorings); w33_20261031_unitary_stabilizer_lift.py (actual spinors);
w33_20261102_chiral_surface_development.py (native branched covers).
No novelty claimed for Clifford groups, their orders, or simplex face counts.
"""
import collections
import hashlib
import itertools
import json
import pathlib
import sys

import sympy as s

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'analysis'))
from w33_20261102_chiral_surface_development import torus, develop, manifold
import numpy as np


def gray(cell):
    x, y = divmod(cell, 4)
    return (x ^ (x >> 1)) | ((y ^ (y >> 1)) << 2)


def switch(mask):
    return mask ^ (15 if mask.bit_count() % 2 else 0)


def board_switch(cell):
    x, y = divmod(cell, 4)
    return 4 * ((-x + 2*y) % 4) + ((2*x-y) % 4)


def board_edges(moves):
    return {tuple(sorted((4*x+y, 4*((x+dx) % 4)+(y+dy) % 4)))
            for x, y in itertools.product(range(4), repeat=2) for dx, dy in moves}


def compose(a, b):
    """Adjoint a after b; phases are powers of i, without floating arithmetic."""
    return tuple(a[b[j]] for j in range(16)) + tuple((b[16+j]+a[16+b[j]]) % 4 for j in range(16))


IDENTITY = tuple(range(16)) + (0,)*16


def closure(gens, bound):
    seen = {IDENTITY}
    queue = [IDENTITY]
    for a in queue:
        for g in gens:
            b = compose(g, a)
            if b not in seen:
                seen.add(b)
                queue.append(b)
        assert len(seen) <= bound
    return seen


def matrices():
    d = json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    parse = lambda a: s.Matrix([[s.sympify(x) for x in row] for row in a])
    axes = [parse(a) for a in d['gamma_axes']]
    blades = []
    for mask in range(16):
        a = s.eye(4)
        for j in range(4):
            if mask >> j & 1:
                a *= axes[j]
        blades.append(a)
    return axes, blades, [parse(a) for a in d['unitary_generators']], parse(d['complex_symplectic_form'])


def adjoint_action(numerator, denominator_squared, blades):
    """Exact action of numerator/sqrt(denominator_squared)."""
    target, phases = [], []
    for a in blades:
        b = numerator*a*numerator.conjugate().T/denominator_squared
        matches = [(j, k) for j, c in enumerate(blades) for k in range(4) if b == s.I**k*c]
        assert len(matches) == 1
        j, k = matches[0]
        target.append(j)
        phases.append(k)
    assert len(set(target)) == 16
    return tuple(target+phases)


def build():
    grid = board_edges([(1, 0), (-1, 0), (0, 1), (0, -1)])
    knight = board_edges([(1, 2), (-1, 2), (2, 1), (2, -1)])
    diagonal = board_edges([(1, 1), (-1, -1)])
    f = board_switch
    image = lambda edges: {tuple(sorted((f(a), f(b)))) for a, b in edges}
    assert len(grid) == len(knight) == 32 and len(diagonal) == 16
    assert not grid & knight and image(grid) == knight and image(diagonal) == diagonal
    assert all(gray(f(v)) == switch(gray(v)) and f(f(v)) == v for v in range(16))
    assert all((gray(a)^gray(b)).bit_count() == 1 for a, b in grid)
    assert all((gray(a)^gray(b)).bit_count() == 3 for a, b in knight)
    assert grid | knight == {tuple(sorted((a, b))) for a in range(16) for b in range(16)
                             if gray(a).bit_count() % 2 != gray(b).bit_count() % 2}
    old = json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())
    C = np.array(old['completion_table'])
    faces = torus(4, 4)
    transported = [tuple(f(v) for v in face) for face in faces]
    source, target = develop(faces, C), develop(transported, C)
    pi = dict(source['labels'])
    pit = dict(target['labels'])
    assert set(manifold(transported)[0]) == knight | diagonal
    assert all(pit[f(v)] == pi[v] == pi[f(v)] for v in range(16))
    parity_colors = {}
    for v in range(16):
        x, y = divmod(v, 4)
        key = (x % 2, y % 2)
        assert key not in parity_colors or parity_colors[key] == pi[v]
        parity_colors[key] = pi[v]
    assert len(set(parity_colors.values())) == 4
    grade_fibers = {str(color): [sum(pi[v] == color and gray(v).bit_count() == k for v in range(16))
                               for k in range(5)] for color in sorted(set(pi.values()))}
    assert sorted(grade_fibers.values()) == sorted([[1, 0, 2, 0, 1], [0, 2, 0, 2, 0],
                                                   [0, 2, 0, 2, 0], [0, 0, 4, 0, 0]])
    axes, blades, gens, omega = matrices()
    P = blades[15]
    assert P*P == s.eye(4)
    assert all((P*a)**2 == -s.eye(4) for a in axes[:4])
    assert all(s.trace(a.conjugate().T*b) == (4 if j == k else 0)
               for j, a in enumerate(blades) for k, b in enumerate(blades))
    N = s.eye(4) + s.I*P
    assert N.conjugate().T*N == 2*s.eye(4)
    action = adjoint_action(N, 2, blades)
    assert action[:16] == tuple(switch(v) for v in range(16))
    assert compose(action, action) == tuple(range(16))+tuple(2*(v.bit_count() % 2) for v in range(16))
    assert compose(compose(action, action), compose(action, action)) == IDENTITY
    assert N.T*omega*N != 2*omega
    assert N**2 == 2*s.I*P and N**4 == -4*s.eye(4) and N**8 == 16*s.eye(4)
    old_actions = [adjoint_action(2*g, 4, blades) for g in gens]
    restricted = closure(old_actions, 960)
    enlarged = closure(old_actions+[action], 11520)
    assert len(restricted) == 960 and len(enlarged) == 11520
    assert len({a[:16] for a in restricted}) == 60
    unsigned = {a[:16] for a in enlarged}
    assert len(unsigned) == 720
    assert sum(a[:16] == tuple(range(16)) for a in enlarged) == 16
    # Ovoids: all five-element pairwise anticommuting subsets of actual Pauli axes.
    anti = lambda i, j: blades[i]*blades[j] == -blades[j]*blades[i]
    ovoids = [tuple(t) for t in itertools.combinations(range(1, 16), 5)
              if all(anti(i, j) for i, j in itertools.combinations(t, 2))]
    assert len(ovoids) == 6
    initial = tuple(sorted([1, 2, 4, 8, 15]))
    assert initial in ovoids
    assert all(tuple(sorted(a[v] for v in initial)) == initial for a in restricted)
    orbit = {tuple(sorted(a[v] for v in initial)) for a in enlarged}
    six_actions = {tuple(ovoids.index(tuple(sorted(a[v] for v in t))) for t in ovoids) for a in unsigned}
    assert len(orbit) == 6 and len(six_actions) == 720
    gate_on_ovoids = tuple(ovoids.index(tuple(sorted(action[v] for v in t))) for t in ovoids)
    assert sum(i != j for i, j in enumerate(gate_on_ovoids)) == 2
    stabilizer = {a for a in enlarged if tuple(sorted(a[v] for v in initial)) == initial}
    assert len(stabilizer) == 1920 and restricted < stabilizer
    return dict(status='PASS_NATIVE_KNIGHT_CLIFFORD_BRIDGE',
        gray_masks=[gray(v) for v in range(16)],board_switch=[f(v) for v in range(16)],
        grid_edges=sorted(grid),knight_edges=sorted(knight),diagonal_edges=sorted(diagonal),
        source_faces=faces,transported_faces=transported,native_labels=source['labels'],
        parity_colors={str(k): v for k, v in parity_colors.items()},grade_fibers=grade_fibers,
        cover_degree=source['cover_degree'],total_ramification=source['total_ramification'],
        vertex_fiber_sizes=dict(collections.Counter(pi.values())),
        clifford_grade_counts=[1,4,6,4,1],signed_switch_action=action,
        unsigned_switch_order=2,signed_adjoint_order=4,unitary_order=8,
        pseudoscalar=[[str(x) for x in row] for row in P.tolist()],
        unitary_numerator=[[str(x) for x in row] for row in N.tolist()],unitary_denominator='sqrt(2)',
        preserves_existing_symplectic_form=False,restricted_projective_order=len(restricted),
        enlarged_projective_order=len(enlarged),symplectic_quotient_order=len(unsigned),
        projective_pauli_kernel_order=16,ovoids=ovoids,ovoid_stabilizer_projective_order=len(stabilizer),
        restricted_unsigned_order=60,gate_on_six_ovoids=gate_on_ovoids,
        old_signed_generator_actions=old_actions,
        enlarged_action_sha256=hashlib.sha256(json.dumps(sorted(enlarged),separators=(',',':')).encode()).hexdigest(),
        boundary='Explicit finite maps in chosen coordinates and existing spinor representation. The switch is an isomorphism between two triangulations, not a deck automorphism of the fixed original surface. Grade counts do not select a real Clifford signature, and no physical spacetime or dynamics are derived.')


if __name__ == '__main__':
    out = build()
    (ROOT/'data/w33_20261102_toroidal_knight_clifford_bridge.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(out['status'],out['restricted_projective_order'],out['enlarged_projective_order'],flush=True)
