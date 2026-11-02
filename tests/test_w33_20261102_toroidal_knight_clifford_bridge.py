"""Independent finite certificate checks for the native knight/Clifford bridge."""
import collections
import itertools
import json
import pathlib

import numpy as np
import sympy as s

ROOT = pathlib.Path(__file__).resolve().parents[1]


def packet():
    return json.loads((ROOT/'data/w33_20261102_toroidal_knight_clifford_bridge.json').read_text())


def blade_product(a, b):
    inversions = sum(1 for i in range(4) for j in range(i) if a >> i & 1 and b >> j & 1)
    return a ^ b, 2*(inversions % 2)


def test_all_graph_pairs_against_literal_knight_rules():
    d = packet()
    E = {tuple(e) for e in d['knight_edges']}
    for a, b in itertools.combinations(range(16), 2):
        x, y = divmod(a, 4)
        u, v = divmod(b, 4)
        assert ((a, b) in E) == (((u-x) % 4, (v-y) % 4) in {(1,2),(3,2),(2,1),(2,3)})
    A = np.zeros((16,16),dtype=int)
    for a,b in E:
        A[a,b]=A[b,a]=1
    assert np.allclose(np.linalg.eigvalsh(A),[-4]+[-2]*4+[0]*6+[2]*4+[4])


def test_cover_on_every_face_and_each_vertex_link():
    d = packet()
    native = json.loads((ROOT/'data/w33_20261102_chiral_surface_development.json').read_text())
    C = native['completion_table']
    pi = dict(d['native_labels'])
    f = d['board_switch']
    for source,target in zip(d['source_faces'],d['transported_faces']):
        assert target == [f[v] for v in source]
        a,b,c = (pi[v] for v in target)
        assert C[a][b] == c
    for faces in [d['source_faces'],d['transported_faces']]:
        for v in range(16):
            nxt = {}
            for face in faces:
                if v in face:
                    k = face.index(v)
                    nxt[face[(k+1)%3]] = face[(k+2)%3]
            start = next(iter(nxt))
            link = [start]
            while nxt[link[-1]] != start:
                link.append(nxt[link[-1]])
                assert len(link) <= 6
            assert len(link) == 6
            assert collections.Counter(pi[u] for u in link) == {c:2 for c in set(pi.values()) if c != pi[v]}
    assert d['cover_degree'] == 8 and d['total_ramification'] == 16
    assert collections.Counter(pi.values()) == {c:4 for c in set(pi.values())}


def test_switch_is_not_original_surface_deck_map():
    d = packet()
    source = {tuple(sorted(t)) for t in d['source_faces']}
    target = {tuple(sorted(t)) for t in d['transported_faces']}
    assert source != target
    all_faces = source | target
    incidence = collections.Counter(tuple(sorted(e)) for t in all_faces for e in itertools.combinations(t,2))
    assert all(incidence[tuple(e)] == 4 for e in d['diagonal_edges'])


def test_signed_switch_preserves_all_256_clifford_products():
    a = packet()['signed_switch_action']
    for i,j in itertools.product(range(16),repeat=2):
        k,p = blade_product(i,j)
        target,q = blade_product(a[i],a[j])
        assert a[k] == target
        assert (p+a[16+k]) % 4 == (a[16+i]+a[16+j]+q) % 4
    assert collections.Counter(a[i].bit_count() for i in [1,2,4,8]) == {3:4}
    assert all(a[i] == i for i in range(16) if i.bit_count() % 2 == 0)


def test_actual_unitary_and_existing_form_boundary():
    d = packet()
    parse = lambda a:s.Matrix([[s.sympify(x) for x in row] for row in a])
    old = json.loads((ROOT/'data/w33_20261031_unitary_stabilizer_lift.json').read_text())
    N,P,omega = parse(d['unitary_numerator']),parse(d['pseudoscalar']),parse(old['complex_symplectic_form'])
    assert N.conjugate().T*N == 2*s.eye(4)
    assert N**2 == 2*s.I*P and N**4 == -4*s.eye(4) and N**8 == 16*s.eye(4)
    assert N.T*omega*N != 2*omega
    for row in old['gamma_axes'][:4]:
        g = parse(row)
        assert N*g*N.conjugate().T/2 == s.I*P*g
        assert (P*g)**2 == -s.eye(4)


def test_group_orders_by_independent_32_point_permutations():
    from sympy.combinatorics import Permutation, PermutationGroup
    d = packet()
    # Normalize blades to Hermitian axes h_m=i^(k(k-1)/2)e_m.
    q = [m.bit_count()*(m.bit_count()-1)//2 % 4 for m in range(16)]
    def perm(action):
        image = []
        for sign in range(2):
            for m in range(16):
                phase = (action[16+m]+q[m]-q[action[m]]) % 4
                assert phase % 2 == 0
                image.append(action[m]+16*((sign+phase//2) % 2))
        return Permutation(image)
    gens = [perm(a) for a in d['old_signed_generator_actions']]
    assert PermutationGroup(gens).order() == 960
    assert PermutationGroup(gens+[perm(d['signed_switch_action'])]).order() == 11520
    unsigned = [Permutation(a[:16]) for a in d['old_signed_generator_actions']+[d['signed_switch_action']]]
    assert PermutationGroup(unsigned).order() == 720


def test_ovoids_and_native_grade_fibers():
    d = packet()
    def anti(a,b):
        return (a.bit_count()*b.bit_count()-(a & b).bit_count()) % 2 == 1
    ovoids = [list(t) for t in itertools.combinations(range(1,16),5) if all(anti(a,b) for a,b in itertools.combinations(t,2))]
    assert ovoids == d['ovoids'] and len(ovoids) == 6
    assert sorted(d['grade_fibers'].values()) == sorted([[1,0,2,0,1],[0,2,0,2,0],[0,2,0,2,0],[0,0,4,0,0]])
