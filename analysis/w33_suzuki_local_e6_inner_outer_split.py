#!/usr/bin/env python3
"""Local E6 symmetry seen by one embedded W33 inside the Suzuki 12-space.

Parent certificate ``w33_suzuki_w33_e6_incidence_tower.py`` proves that the
135135 embedded full W(3,3) subspaces form the Suzuki orbit, that a fixed W33
has 54 orthogonal W33 partners paired by complement into 27 decompositions,
and that those 27 vertices carry SRG(27,10,1,5), whose complement is the
Schlaefli graph.

This file computes the *actual induced group* of the W33 stabilizer on those
27 decompositions.  Two explicit Schreier loops in the 135135-subspace orbit
generate a transitive permutation group of order 25920.  Thus the Suzuki
stabilizer realizes the inner U4(2) ~= PSp(4,3) half of the local E6 symmetry.

The final index-two comparison uses two published classifications, recorded as
external inputs rather than recomputed here:
  * ATLAS: the degree-135135 Suzuki action has point stabilizer
      2^(1+6).U4(2), with |U4(2)|=25920 and Out(U4(2))=2;
  * the automorphism group of the 27-line cubic-surface/Schlaefli graph is
      W(E6) ~= U4(2):2, order 51840.

Why the normal 2-core is invisible on the local 27-set: the computed U4(2)
image is transitive on 27 vertices.  In the published point stabilizer
2^(1+6).U4(2), the normal 2-group has equal-size orbits on any transitive
quotient.  Its orbit size is a power of two dividing 27, hence one.  Therefore
the 27-point action factors through U4(2).  Since the explicit image already
has order 25920, it is the full induced image.  The outer factor of W(E6) is
not supplied by the Suzuki point stabilizer.

This is finite group/geometry only; no physical E6 gauge symmetry is inferred.
"""
from __future__ import annotations

import importlib.util
import json
from collections import deque
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_suzuki_local_e6_inner_outer_split.json"
P = 3


def load_parent():
    path = ROOT / "analysis" / "w33_suzuki_w33_e6_incidence_tower.py"
    spec = importlib.util.spec_from_file_location("tower", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def invp(M):
    M = np.array(M, dtype=np.int64) % P
    n = M.shape[0]
    X = np.concatenate([M, np.eye(n, dtype=np.int64)], axis=1)
    for c in range(n):
        p = next(i for i in range(c, n) if X[i, c])
        X[[c, p]] = X[[p, c]]
        X[c] = X[c] * pow(int(X[c, c]), -1, P) % P
        for i in range(n):
            if i != c and X[i, c]:
                X[i] = (X[i] - X[i, c] * X[c]) % P
    return X[:, n:] % P


def compose(p, q):
    """Apply p and then q."""
    return tuple(q[p[i]] for i in range(len(p)))


def perm_order(p):
    ident = tuple(range(len(p)))
    x = ident
    for n in range(1, 200):
        x = compose(x, p)
        if x == ident:
            return n
    raise AssertionError("permutation order bound exceeded")


def closure(gens, limit=100000):
    ident = tuple(range(len(gens[0])))
    seen = {ident}
    q = deque([ident])
    while q:
        x = q.popleft()
        for g in gens:
            y = compose(x, g)
            if y not in seen:
                seen.add(y)
                q.append(y)
                assert len(seen) <= limit
    return seen


def main(write=True):
    T = load_parent()
    A = T.parse_meataxe(ROOT / "data/atlas/2SuzG1-f3r12B0.m1")
    B = T.parse_meataxe(ROOT / "data/atlas/2SuzG1-f3r12B0.m2")
    gens = [A, B]
    U = np.array(T.U1, dtype=np.int64)
    J = np.array(T.J, dtype=np.int64)

    # Rebuild the complete 135135 W33 orbit, now retaining a transporter from
    # U to every orbit point.  The deterministic ordering fixes the Schreier
    # witness indices below.
    seed = T.rref_key(U)
    eye = np.eye(12, dtype=np.int64)
    index = {seed: 0}
    bases = [np.array(seed, dtype=np.int64)]
    trans = [eye]
    parent = [None]
    edgegen = [None]
    q = deque([0])
    while q:
        i = q.popleft()
        for gi, g in enumerate(gens):
            key = T.rref_key(bases[i] @ g % P)
            if key not in index:
                j = len(bases)
                index[key] = j
                bases.append(np.array(key, dtype=np.int64))
                trans.append(trans[i] @ g % P)
                parent.append(i)
                edgegen.append(gi)
                q.append(j)
    assert len(bases) == 135135

    # The 54 orthogonal partners and their complement involution give the local
    # 27 decompositions from the parent theorem.
    partners = [M for M in bases if np.all(U @ J @ M.T % P == 0)]
    assert len(partners) == 54
    pkeys = {T.rref_key(M) for M in partners}
    pairs = set()
    for V in partners:
        W = T.perp_basis(np.vstack([U, V]))
        a, b = sorted((T.rref_key(V), T.rref_key(W)))
        assert a in pkeys and b in pkeys
        pairs.add((a, b))
    pairs = sorted(pairs)
    assert len(pairs) == 27
    partner_to_pair = {}
    for i, (a, b) in enumerate(pairs):
        partner_to_pair[a] = i
        partner_to_pair[b] = i
    assert len(partner_to_pair) == 54

    def induced_perm(h):
        out = []
        for a, _ in pairs:
            z = T.rref_key(np.array(a, dtype=np.int64) @ h % P)
            assert z in partner_to_pair
            out.append(partner_to_pair[z])
        assert len(set(out)) == 27
        return tuple(out)

    # Two deterministic non-tree Schreier loops.  These indices are witnesses,
    # not assumptions: each target is recomputed and checked below.
    witness_edges = [(115535, 0, 117702), (131880, 1, 129735)]
    perms = []
    loops = []
    for i, gi, expected_j in witness_edges:
        g = gens[gi]
        key = T.rref_key(bases[i] @ g % P)
        j = index[key]
        assert j == expected_j
        h = trans[i] @ g @ invp(trans[j]) % P
        assert T.rref_key(U @ h % P) == seed
        p = induced_perm(h)
        perms.append(p)
        loops.append({"source": i, "generator": gi, "target": j,
                      "permutation_order": perm_order(p)})

    H = closure(perms)
    assert len(H) == 25920
    orbit = {0}
    qq = deque([0])
    while qq:
        x = qq.popleft()
        for p in perms:
            y = p[x]
            if y not in orbit:
                orbit.add(y)
                qq.append(y)
    assert len(orbit) == 27

    # Recheck the local graph and verify every generated permutation preserves it.
    adj = np.zeros((27, 27), dtype=bool)
    for i in range(27):
        Ai, Bi = (np.array(x, dtype=np.int64) for x in pairs[i])
        for j in range(i + 1, 27):
            Aj, Bj = (np.array(x, dtype=np.int64) for x in pairs[j])
            s = tuple(sorted([T.intersection_dim(Ai, Aj), T.intersection_dim(Ai, Bj),
                              T.intersection_dim(Bi, Aj), T.intersection_dim(Bi, Bj)]))
            if s == (2, 2, 2, 2):
                adj[i, j] = adj[j, i] = True
    assert T.srg_params(adj) == (27, 10, 1, 5)
    for p in perms:
        assert np.array_equal(adj[np.ix_(p, p)], adj)

    # Published stabilizer arithmetic.  For Suz (not its scalar double cover),
    # |Suz| / 135135 = 3317760 = 128 * 25920.
    suz_order = 448345497600
    stab_order = suz_order // 135135
    assert stab_order == 3317760 == 128 * 25920

    out = {
      "schema": "w33.suzuki_local_e6_inner_outer_split.v1",
      "status": "PASS",
      "headline": "For one full W33 in the Suzuki 135135-subspace orbit, the stabilizer action on its 27 complementary three-W33 decompositions contains a transitive group of order 25920 generated by two explicit Schreier loops. Using the published ATLAS point-stabilizer 2^(1+6).U4(2), the normal 2-core must act trivially on this transitive odd 27-set, so the full induced image is U4(2) ~= PSp(4,3), order 25920. The full Schlaefli/cubic-surface graph automorphism group is W(E6) ~= U4(2):2, order 51840; its outer factor is therefore absent from the Suzuki W33 stabilizer.",
      "orbit": {"embedded_W33s": 135135, "orthogonal_partners": 54,
                 "complement_pairs": 27, "local_srg": [27, 10, 1, 5]},
      "schreier_witnesses": loops,
      "computed_induced_subgroup": {"order": len(H), "transitive_degree": len(orbit),
                                    "identification": "U4(2) ~= PSp(4,3)"},
      "published_inputs": {
        "ATLAS_degree_135135_point_stabilizer": "2^(1+6).U4(2)",
        "Suz_order": suz_order,
        "point_stabilizer_order": stab_order,
        "U4_2_order": 25920,
        "Out_U4_2_order": 2,
        "Schlaefli_graph_full_automorphism": "W(E6) ~= U4(2):2, order 51840"
      },
      "normal_2_core_argument": "The point stabilizer is transitive on the computed 27-set. A normal 2-subgroup has equal-size orbits forming blocks; the orbit size is a power of 2 dividing 27, hence 1. Thus the 2^(1+6) core is in the kernel and the action factors through U4(2). The explicit 25920 subgroup saturates that quotient.",
      "outer_split": {"inner_realized": 25920, "full_E6_Weyl": 51840,
                      "missing_index": 2,
                      "meaning": "The local E6 incidence carrier is fully present, but the Suzuki W33 stabilizer realizes only the inner PSp(4,3) half of its graph symmetry."},
      "boundary": "The computation is finite group/geometry. The ATLAS stabilizer structure and classical Schlaefli/W(E6) automorphism identification are published external inputs. No physical E6 gauge symmetry or dynamical enhancement is inferred.",
      "checks": {"orbit_135135": True, "partners_54": True, "pairs_27": True,
                 "two_schreier_loops": True, "image_order_25920": True,
                 "image_transitive_27": True, "local_srg_27_10_1_5": True,
                 "stabilizer_factor_128_times_25920": True}
    }
    if write:
        OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
    return out


if __name__ == "__main__":
    main(True)
