#!/usr/bin/env python3
"""Direct computation that the Suzuki outer block-stabilizer acts outside PSp(4,3).

w33_suz_outer_completes_local_e6_weyl.py constructs the outer-coset element

    h = C * T^{-1},   T = BABABABABABBABABABABBABABA,

shows it fixes the chosen W33 block U and has symplectic multiplier -1, and then
*deduces* that the local 27-decomposition image grows to U4(2):2 = W(E6) from the
published ATLAS stabilizer 2^(1+6).U4(2).2 plus the odd-transitive-set argument.
Its `full_outer_image_51840` check is recorded as True but is not computed there:
nothing in that file evaluates the permutation h induces on the 27.

This file computes that permutation and closes the gap without using the ATLAS
stabilizer structure at all.  Rebuilding the 135135-element orbit with a Schreier
transversal, the 54 orthogonal partners and the 27 complementary decompositions,
we obtain the inner image from Schreier generators and then induce h directly.

Results (exact):
  * h preserves the SRG(27,10,1,5) intersection graph;
  * the permutation h induces is NOT in the inner PSp(4,3) image;
  * adjoining it to the inner image closes at order 51840 = |W(E6)|;
  * that permutation has order 6 and acts without fixed points on the 27.

So the outer completion is a computed fact about this matrix, not only a
classification argument, and the parent certificate's deduction is confirmed by an
independent route.
"""
from __future__ import annotations

from collections import deque
import json
from pathlib import Path

import numpy as np

import w33_suzuki_w33_stabilizer_projective_quotient as Q
import w33_suz_outer_completes_local_e6_weyl as O

base = Q.base
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data' / 'w33_suz_outer_h_acts_outer_on_the_27_direct.json'
P = 3


def main(write=True):
    A = base.parse_meataxe(ROOT / 'data/atlas/2SuzG1-f3r12B0.m1')
    B = base.parse_meataxe(ROOT / 'data/atlas/2SuzG1-f3r12B0.m2')
    C = base.parse_meataxe(ROOT / 'data/atlas/2Suzd2G1-f3r12aB0.m1')
    gens = [A, B]
    invgens = [Q.inv3(A), Q.inv3(B)]
    U1 = base.U1 % P
    J = base.J % P
    I12 = np.eye(12, dtype=np.int64)
    k0 = base.rref_key(U1)

    # orbit with Schreier transversal, and a deterministic sample of stabilizer elements
    keys = [k0]
    subs = [np.array(k0, dtype=np.int64)]
    T = [I12]
    Ti = [I12]
    index = {k0: 0}
    q = deque([0])
    sample = []
    seen_sample = set()
    while q:
        ix = q.popleft()
        S = subs[ix]
        for gi, g in enumerate(gens):
            kz = base.rref_key((S @ g) % P)
            j = index.get(kz)
            Tg = (T[ix] @ g) % P
            if j is None:
                j = len(keys)
                index[kz] = j
                keys.append(kz)
                subs.append(np.array(kz, dtype=np.int64))
                T.append(Tg)
                Ti.append((invgens[gi] @ Ti[ix]) % P)
                q.append(j)
            elif len(sample) < 120:
                s = (Tg @ Ti[j]) % P
                kk = Q.matkey(s)
                if kk not in seen_sample and not np.array_equal(s, I12):
                    seen_sample.add(kk)
                    sample.append(s)
    assert len(subs) == 135135

    partner_keys = [k for k, S in zip(keys, subs) if np.all((U1 @ J @ S.T) % P == 0)]
    partners = [np.array(k, dtype=np.int64) for k in partner_keys]
    assert len(partners) == 54
    pindex = {k: i for i, k in enumerate(partner_keys)}
    comp = [pindex[base.rref_key(base.perp_basis(np.vstack([U1, V])))] for V in partners]
    pairs = []
    pair_of = {}
    for i in range(54):
        if i < comp[i]:
            pid = len(pairs)
            pairs.append((i, comp[i]))
            pair_of[i] = pair_of[comp[i]] = pid
    assert len(pairs) == 27

    def induced27(s):
        p = [pindex[base.rref_key((V @ s) % P)] for V in partners]
        assert sorted(p) == list(range(54))
        return tuple(pair_of[p[a]] for a, _ in pairs)

    dec = [(partners[a], partners[b]) for a, b in pairs]
    adj = np.zeros((27, 27), dtype=np.uint8)
    for i in range(27):
        Ai, Bi = dec[i]
        for j in range(i + 1, 27):
            Aj, Bj = dec[j]
            sig = tuple(sorted([base.intersection_dim(Ai, Aj), base.intersection_dim(Ai, Bj),
                                base.intersection_dim(Bi, Aj), base.intersection_dim(Bi, Bj)]))
            if sig == (2, 2, 2, 2):
                adj[i, j] = adj[j, i] = 1
    assert base.srg_params(adj) == (27, 10, 1, 5)

    gp, psp = Q.greedy_perm_generators([induced27(s) for s in sample], 25920)
    assert len(psp) == 25920

    M = np.eye(12, dtype=np.int64)
    for ch in O.TRANS_WORD:
        M = M @ (A if ch == 'A' else B) % P
    h = C @ Q.inv3(M) % P
    assert base.rref_key(U1 @ h % P) == k0
    assert O.multiplier(h, J) == 2

    ph = induced27(h)
    inner = ph in psp
    full = Q.perm_closure(gp + [ph], cap=51840)
    order = 1
    x = ph
    ident = tuple(range(27))
    while x != ident:
        x = Q.perm_comp(x, ph)
        order += 1
    fixed = sum(1 for i in range(27) if ph[i] == i)

    assert Q.graph_preserved(ph, adj)
    assert not inner
    assert len(full) == 51840

    out = {
        'schema': 'w33.suz_outer_h_acts_outer_on_the_27_direct.v1', 'status': 'PASS',
        'headline': 'The outer-coset block stabilizer h = C T^{-1} of w33_suz_outer_completes_local_e6_weyl is induced '
                    'directly on the 27 complementary three-W33 decompositions. It preserves the SRG(27,10,1,5) graph, '
                    'lies outside the inner PSp(4,3) image, and closes the local image at 51840 = |W(E6)|. Its '
                    'permutation has order 6 and no fixed points. The parent certificate recorded '
                    'full_outer_image_51840 as a classification deduction; this is the computation.',
        'orbit': {'embedded_W33s': len(subs), 'orthogonal_partners': len(partners), 'decompositions': len(pairs)},
        'inner_image': {'group': 'PSp(4,3)', 'order': len(psp), 'generators_used': len(gp)},
        'outer_element': {'word': O.TRANS_WORD, 'multiplier_mod3': 2, 'fixes_U': True,
                          'permutation_on_27': list(ph), 'permutation_order': order, 'fixed_points_on_27': fixed,
                          'preserves_local_graph': True, 'inside_inner_PSp': inner},
        'closure': {'order_with_h': len(full), 'identification': 'U4(2):2 = W(E6)'},
        'relation_to_parent': 'independent of the ATLAS stabilizer shape and of the odd-transitive-set argument; only '
                              'the vendored matrices and this orbit computation are used',
        'boundary': 'Exact finite computation for the vendored ATLAS representation. It does not make the outer '
                    'similitude a physically available operation.',
        'checks': {'orbit_135135': len(subs) == 135135, 'decompositions_27': len(pairs) == 27,
                   'inner_image_25920': len(psp) == 25920, 'h_preserves_graph': True,
                   'h_outside_inner_image': not inner, 'closure_51840': len(full) == 51840,
                   'h_order_six_fixed_point_free': order == 6 and fixed == 0}}
    if write:
        OUT.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))
    return out


if __name__ == '__main__':
    main(True)
