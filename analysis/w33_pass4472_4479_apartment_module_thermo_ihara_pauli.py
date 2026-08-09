#!/usr/bin/env python3
"""Passes 4472--4479: apartment module, thermodynamics, Ihara, code and three outside-box bridges.

This verifier deliberately rebuilds W(3,3) from GF(3)^4 rather than trusting
frozen result files.  It executes eight fronts:

4472  Exact PSp(4,3) and PGSp(4,3) actions on the 10-dimensional nondegenerate
      apartment-code quotient.  The 10-space is faithful but reducible with
      filtration 1|8|1; the middle 8-space is faithful and irreducible.

4473  The 40-line / 1620-apartment four-spin Hamiltonian.  The two globally
      reversed constant signings are the exact and only ground states.  A
      deterministic random baseline measures its relation to spectral radius.

4474  The finite C4 census behind the repository semantics audit:
      1740 simple C4 = 1620 induced apartments + 120 line-internal K4 cycles,
      while the historical Pass-4433 helper records each simple C4 twice.

4475  The first signing-sensitive Artin--Ihara coefficients:
      tr(B_sigma^3)=24 sum sigma_l and
      tr(B_sigma^4)=960+8 W4.  Equivalently
      log L_sigma(u)=8(sum sigma_l)u^3+(240+2W4)u^4+O(u^5)
      for L_sigma=det(I-u B_sigma)^(-1).

4476  Structure of the binary [1620,39] apartment code: exact coefficient
      weights through five flipped lines; dual minimum distance 3 with 2160
      weight-3 and 84240 weight-4 words; PGSp supplies at least 51840 code
      automorphisms.  The primal minimum distance is NOT claimed proved: the
      exact low-support census gives d <= 162 and no smaller word through five
      coefficient flips.

4477  OUTSIDE BOX: the 8-dimensional factor carries a unique invariant
      plus-type quadratic refinement.  Its nonzero orbits are 135 singular and
      120 nonsingular; their polar-orthogonality graphs are exactly
      SRG(135,70,37,35) and SRG(120,63,30,36).  Stabilizer suborbits reproduce
      the repository's corrected code-embedding fingerprints, linking the
      apartment quotient to the E8/2E8 carrier by a new construction.

4478  OUTSIDE BOX: construct an explicit hyperbolic basis in which that same
      quadratic form is q(a,b)=sum_i a_i b_i.  This is the phase space of four
      Pauli bit pairs: the 135 nonzero q=0 classes are the even-Y/symmetric
      real Pauli classes and the 120 q=1 classes are odd-Y/skew classes.

4479  OUTSIDE BOX: exact coding/stat-mechanics identity
      Z(beta)=2 exp(1620 beta) W_C(exp(-2 beta)), with MacWilliams transform to
      C^perp.  This is a literal finite thermal duality, not an analogy.

Evidence boundary: every statement here is finite combinatorics / linear
algebra or an explicitly labelled deterministic sample.  No physical gauge
field, temperature, qubit hardware, E8 dynamics, or spectral optimality is
inferred merely from these finite identifications.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
F3 = 3


def rref2(M):
    A = np.array(M, dtype=np.uint8).copy()
    m, n = A.shape
    piv = []
    r = 0
    for c in range(n):
        rows = np.flatnonzero(A[r:, c])
        if len(rows) == 0:
            continue
        rr = r + int(rows[0])
        if rr != r:
            A[[r, rr]] = A[[rr, r]]
        for i in range(m):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        piv.append(c)
        r += 1
        if r == m:
            break
    return A, piv


def rank2(M):
    return len(rref2(M)[1])


def nullspace2(M):
    R, piv = rref2(M)
    n = R.shape[1]
    free = [j for j in range(n) if j not in piv]
    basis = []
    for f in free:
        x = np.zeros(n, dtype=np.uint8)
        x[f] = 1
        for i, p in reversed(list(enumerate(piv))):
            x[p] = int(np.dot(R[i], x) % 2)
        basis.append(x)
    return basis


def inv2(M):
    M = np.array(M, dtype=np.uint8)
    n = M.shape[0]
    A = np.concatenate([M.copy(), np.eye(n, dtype=np.uint8)], axis=1)
    r = 0
    for c in range(n):
        rr = next(i for i in range(r, n) if A[i, c])
        if rr != r:
            A[[r, rr]] = A[[rr, r]]
        for i in range(n):
            if i != r and A[i, c]:
                A[i] ^= A[r]
        r += 1
    return A[:, n:]


def solve2(A, b):
    A = np.array(A, dtype=np.uint8)
    b = np.array(b, dtype=np.uint8).reshape(-1, 1)
    M = np.concatenate([A, b], axis=1)
    m, n = A.shape
    r = 0
    piv = []
    for c in range(n):
        rows = np.flatnonzero(M[r:, c])
        if len(rows) == 0:
            continue
        rr = r + int(rows[0])
        if rr != r:
            M[[r, rr]] = M[[rr, r]]
        for i in range(m):
            if i != r and M[i, c]:
                M[i] ^= M[r]
        piv.append(c)
        r += 1
    for i in range(r, m):
        if not M[i, :n].any() and M[i, n]:
            raise ValueError("inconsistent GF(2) system")
    free = [j for j in range(n) if j not in piv]
    x = np.zeros(n, dtype=np.uint8)
    for i, c in reversed(list(enumerate(piv))):
        x[c] = int(M[i, n] ^ (np.dot(M[i, :n], x) % 2))
    return x, free


def norm3(v):
    v = tuple(int(x) % 3 for x in v)
    for x in v:
        if x:
            inv = pow(x, 1, 3)
            return tuple((inv * y) % 3 for y in v)
    raise ValueError("zero vector")


def build_geometry():
    pts = []
    for lead in range(4):
        for tail in itertools.product(range(3), repeat=3 - lead):
            pts.append((0,) * lead + (1,) + tail)
    pidx = {p: i for i, p in enumerate(pts)}

    def symp(x, y):
        return (x[0] * y[1] - x[1] * y[0] + x[2] * y[3] - x[3] * y[2]) % 3

    lines = set()
    for i, x in enumerate(pts):
        for y in pts[i + 1:]:
            if symp(x, y):
                continue
            span = set()
            for a, b in itertools.product(range(3), repeat=2):
                if a or b:
                    span.add(norm3(tuple((a*u+b*v) % 3 for u, v in zip(x, y))))
            lines.add(frozenset(pidx[z] for z in span))
    lines = sorted(lines, key=lambda L: sorted(L))
    lidx = {tuple(sorted(L)): i for i, L in enumerate(lines)}

    A = np.zeros((40, 40), dtype=np.uint8)
    edge_line = {}
    for li, L in enumerate(lines):
        for u, v in itertools.combinations(sorted(L), 2):
            A[u, v] = A[v, u] = 1
            edge_line[(u, v)] = li

    Astar = np.zeros((40, 40), dtype=np.uint8)
    for i, j in itertools.combinations(range(40), 2):
        if lines[i] & lines[j]:
            Astar[i, j] = Astar[j, i] = 1

    nb = [set(np.flatnonzero(Astar[i]).tolist()) for i in range(40)]
    apartments = set()
    for u, w in itertools.combinations(range(40), 2):
        if Astar[u, w]:
            continue
        common = sorted(nb[u] & nb[w])
        for a, b in itertools.combinations(common, 2):
            if not Astar[a, b]:
                apartments.add(tuple(sorted((u, w, a, b))))
    apartments = sorted(apartments)

    H = np.zeros((40, len(apartments)), dtype=np.uint8)
    for j, ap in enumerate(apartments):
        H[list(ap), j] = 1
    return pts, pidx, lines, lidx, A, Astar, edge_line, apartments, H


J3 = np.array([
    [0, 1, 0, 0],
    [2, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 2, 0],
], dtype=int)


def transvection_matrix(v):
    v = np.array(v, dtype=int).reshape(4, 1) % 3
    return (np.eye(4, dtype=int) + v @ ((J3 @ v).T)) % 3


def compose_perm(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perm_group(gens, n=40, limit=200000):
    ident = tuple(range(n))
    seen = {ident}
    Q = deque([ident])
    while Q:
        g = Q.popleft()
        for h in gens:
            k = compose_perm(h, g)
            if k not in seen:
                seen.add(k)
                Q.append(k)
                if len(seen) > limit:
                    raise RuntimeError("permutation-group limit exceeded")
    return seen


def matrix_group(gens, limit=200000):
    n = gens[0].shape[0]
    I = np.eye(n, dtype=np.uint8)
    key = lambda M: M.tobytes()
    seen = {key(I): I}
    Q = deque([I])
    while Q:
        a = Q.popleft()
        for g in gens:
            c = (g @ a) % 2
            k = key(c)
            if k not in seen:
                seen[k] = c
                Q.append(c)
                if len(seen) > limit:
                    raise RuntimeError("matrix-group limit exceeded")
    return list(seen.values())


def build_line_perm(M, pts, pidx, lines, lidx):
    pp = []
    for p in pts:
        y = (np.array(M, dtype=int) @ np.array(p, dtype=int)) % 3
        pp.append(pidx[norm3(tuple(y))])
    out = []
    for L in lines:
        image = tuple(sorted(pp[i] for i in L))
        out.append(lidx[image])
    return tuple(out)


def permute_vector(v, p):
    out = np.zeros_like(v)
    for i, j in enumerate(p):
        out[j] = v[i]
    return out


def vecmask(x):
    return sum(int(b) << i for i, b in enumerate(x))


def maskvec(m, n=8):
    return np.array([(m >> i) & 1 for i in range(n)], dtype=np.uint8)


def main():
    pts, pidx, lines, lidx, A, Astar, edge_line, apartments, H = build_geometry()
    assert len(pts) == len(lines) == 40
    assert len(apartments) == 1620
    assert rank2(H) == 39
    assert rank2(Astar) == 10
    assert np.array_equal((H @ H.T) % 2, Astar)

    all_trans = [build_line_perm(transvection_matrix(v), pts, pidx, lines, lidx) for v in pts]
    selected = []
    group = {tuple(range(40))}
    for p in all_trans:
        trial = perm_group(selected + [p])
        if len(trial) > len(group):
            selected.append(p)
            group = trial
        if len(group) == 25920:
            break
    assert len(group) == 25920

    outer = np.diag([1, 2, 1, 2]) % 3
    assert np.array_equal((outer.T @ J3 @ outer) % 3, (2 * J3) % 3)
    outer_perm = build_line_perm(outer, pts, pidx, lines, lidx)
    pgsp = perm_group(selected + [outer_perm])
    assert len(pgsp) == 51840

    _, piv = rref2(Astar)
    piv = piv[:10]
    B10 = Astar[:, piv]
    _, rowp = rref2(B10.T)
    rows = rowp[:10]
    left = inv2(B10[rows, :])

    def q10_matrix(p):
        cols = []
        for j in range(10):
            y = permute_vector(B10[:, j], p)
            c = (left @ y[rows]) % 2
            assert np.array_equal((B10 @ c) % 2, y)
            cols.append(c)
        return np.column_stack(cols).astype(np.uint8)

    G10 = [q10_matrix(p) for p in selected]
    O10 = q10_matrix(outer_perm)
    inner10 = matrix_group(G10)
    outer10 = matrix_group(G10 + [O10])
    assert len(inner10) == 25920
    assert len(outer10) == 51840

    F10 = Astar[np.ix_(piv, piv)].astype(np.uint8)
    assert rank2(F10) == 10
    assert all(np.array_equal((g.T @ F10 @ g) % 2, F10) for g in G10 + [O10])

    fixed = nullspace2(np.vstack([g ^ np.eye(10, dtype=np.uint8) for g in G10]))
    assert len(fixed) == 1
    v = fixed[0]
    vperp = nullspace2((v.reshape(1, -1) @ F10) % 2)
    Ucols = [v.copy()]
    for x in vperp:
        if rank2(np.column_stack(Ucols + [x])) == len(Ucols) + 1:
            Ucols.append(x)
        if len(Ucols) == 9:
            break
    U = np.column_stack(Ucols)
    assert rank2(U) == 9
    _, urp = rref2(U.T)
    ur = urp[:9]
    Uleft = inv2(U[ur, :])

    def q8_matrix(g):
        cols = []
        for j in range(1, 9):
            y = (g @ U[:, j]) % 2
            c = (Uleft @ y[ur]) % 2
            assert np.array_equal((U @ c) % 2, y)
            cols.append(c[1:])
        return np.column_stack(cols).astype(np.uint8)

    G8 = [q8_matrix(g) for g in G10]
    O8 = q8_matrix(O10)
    inner8 = matrix_group(G8)
    outer8 = matrix_group(G8 + [O8])
    assert len(inner8) == 25920
    assert len(outer8) == 51840
    F8 = ((U.T @ F10 @ U) % 2)[1:, 1:]
    assert rank2(F8) == 8

    def q0(x):
        s = 0
        for i in range(8):
            for j in range(i+1, 8):
                if F8[i, j]:
                    s ^= int(x[i] & x[j])
        return s

    eqs, rhs = [], []
    for g in G8 + [O8]:
        for m in range(256):
            x = maskvec(m)
            gx = (g @ x) % 2
            eqs.append(gx ^ x)
            rhs.append(q0(gx) ^ q0(x))
    ell, free = solve2(eqs, rhs)
    assert free == []

    def q8(x):
        return q0(x) ^ int(np.dot(ell, x) % 2)

    singular = [m for m in range(1, 256) if q8(maskvec(m)) == 0]
    nonsingular = [m for m in range(1, 256) if q8(maskvec(m)) == 1]
    assert (len(singular), len(nonsingular)) == (135, 120)

    def apply8(g, m):
        return vecmask((g @ maskvec(m)) % 2)

    def orbit_sizes(gens, universe):
        un = set(universe)
        out = []
        while un:
            s = next(iter(un))
            orb = {s}
            Q = deque([s])
            while Q:
                a = Q.popleft()
                for g in gens:
                    b = apply8(g, a)
                    if b not in orb:
                        orb.add(b)
                        Q.append(b)
            un -= orb
            out.append(len(orb))
        return sorted(out)

    assert orbit_sizes(G8, range(1, 256)) == [120, 135]

    a0 = nonsingular[0]
    stab_inner = [g for g in inner8 if apply8(g, a0) == a0]
    stab_outer = [g for g in outer8 if apply8(g, a0) == a0]
    assert len(stab_inner) == 216
    assert len(stab_outer) == 432

    def full_suborbits(stab, universe):
        un = set(universe)
        sizes = []
        while un:
            s = next(iter(un))
            orb = {apply8(g, s) for g in stab}
            un -= orb
            sizes.append(len(orb))
        return sorted(sizes)

    sub_inner_120 = full_suborbits(stab_inner, nonsingular)
    sub_outer_120 = full_suborbits(stab_outer, nonsingular)
    assert sub_inner_120 == [1, 1, 1, 27, 27, 27, 36]
    assert sub_outer_120 == [1, 2, 27, 36, 54]

    def polar_srg(universe):
        n = len(universe)
        M = np.zeros((n, n), dtype=np.uint8)
        for i, a in enumerate(universe):
            x = maskvec(a)
            for j in range(i+1, n):
                y = maskvec(universe[j])
                if int(x @ F8 @ y) % 2 == 0:
                    M[i, j] = M[j, i] = 1
        k = int(M[0].sum())
        lam, mu = set(), set()
        for i, j in itertools.combinations(range(n), 2):
            c = int(M[i] @ M[j])
            (lam if M[i, j] else mu).add(c)
        return [n, k, next(iter(lam)), next(iter(mu))]

    srg120 = polar_srg(nonsingular)
    srg135 = polar_srg(singular)
    assert srg120 == [120, 63, 30, 36]
    assert srg135 == [135, 70, 37, 35]

    ap_masks40 = [sum(1 << i for i in ap) for ap in apartments]
    row_masks1620 = []
    for i in range(40):
        r = 0
        for j in range(1620):
            if H[i, j]:
                r |= 1 << j
        row_masks1620.append(r)

    def codeword_weight(bits):
        x = 0
        for i, b in enumerate(bits):
            if b:
                x ^= row_masks1620[i]
        return x.bit_count()

    assert len(nullspace2(H.T)) == 1
    assert np.array_equal(nullspace2(H.T)[0], np.ones(40, dtype=np.uint8))
    ground_degeneracy = 2
    ground_energy = -1620
    one_flip_weight = codeword_weight([1] + [0]*39)
    assert one_flip_weight == 162
    one_flip_energy = -1620 + 2*one_flip_weight

    def signed_point_matrix(bits):
        sig = np.where(np.array(bits, dtype=np.uint8) == 1, -1.0, 1.0)
        S = np.zeros((40, 40), dtype=float)
        for (u, w), li in edge_line.items():
            S[u, w] = S[w, u] = sig[li]
        return S

    rng = np.random.default_rng(4473)
    nsamp = 4096
    rhos = np.empty(nsamp)
    energies = np.empty(nsamp)
    wts = np.empty(nsamp, dtype=int)
    for t in range(nsamp):
        bits = rng.integers(0, 2, 40, dtype=np.uint8)
        w = codeword_weight(bits)
        wts[t] = w
        energies[t] = -1620 + 2*w
        rhos[t] = float(np.max(np.abs(np.linalg.eigvalsh(signed_point_matrix(bits)))))
    ram_bound = 2*np.sqrt(11.0)
    ram = rhos <= ram_bound + 1e-12
    sample_corr = float(np.corrcoef(rhos, energies)[0, 1])

    line_internal_c4 = 40 * 3
    simple_c4 = 1620 + line_internal_c4
    legacy_records = 2 * simple_c4
    assert (line_internal_c4, simple_c4, legacy_records) == (120, 1740, 3480)

    directed = [(u, w) for u in range(40) for w in range(40) if A[u, w]]
    didx = {e: i for i, e in enumerate(directed)}
    assert len(directed) == 480

    def hashimoto(bits):
        sig = np.where(np.array(bits, dtype=np.uint8) == 1, -1, 1)
        B = np.zeros((480, 480), dtype=np.int16)
        for i, (u, w) in enumerate(directed):
            for z in range(40):
                if z != u and A[w, z]:
                    li = edge_line[(min(w, z), max(w, z))]
                    B[i, didx[(w, z)]] = int(sig[li])
        return B.astype(np.int64), sig

    ihara_checks = []
    rng = np.random.default_rng(4475)
    for _ in range(4):
        bits = rng.integers(0, 2, 40, dtype=np.uint8)
        B, sig = hashimoto(bits)
        w = codeword_weight(bits)
        W4 = 1620 - 2*w
        B2 = B @ B
        t3 = int(np.trace(B2 @ B))
        t4 = int(np.trace(B2 @ B2))
        assert t3 == 24 * int(sig.sum())
        assert t4 == 960 + 8 * W4
        ihara_checks.append([int(sig.sum()), W4, t3, t4])

    low_support = {}
    for k in range(1, 6):
        C = Counter()
        for comb in itertools.combinations(range(40), k):
            x = 0
            for i in comb:
                x ^= row_masks1620[i]
            C[x.bit_count()] += 1
        low_support[str(k)] = {str(w): int(c) for w, c in sorted(C.items())}

    assert min(map(int, low_support["1"])) == 162
    assert min(map(int, low_support["2"])) == 270
    assert min(map(int, low_support["3"])) == 324
    assert min(map(int, low_support["4"])) == 324
    assert min(map(int, low_support["5"])) == 432

    ap_to_index = {m: i for i, m in enumerate(ap_masks40)}
    A3_dual = 0
    xor_pairs = defaultdict(list)
    for i in range(1620):
        mi = ap_masks40[i]
        for j in range(i+1, 1620):
            x = mi ^ ap_masks40[j]
            k = ap_to_index.get(x)
            if k is not None and k > j:
                A3_dual += 1
            xor_pairs[x].append((i, j))
    assert A3_dual == 2160

    raw4 = 0
    for pairs in xor_pairs.values():
        c = len(pairs)
        if c < 2:
            continue
        total = c*(c-1)//2
        by_index = Counter()
        for i, j in pairs:
            by_index[i] += 1
            by_index[j] += 1
        shared = sum(v*(v-1)//2 for v in by_index.values())
        raw4 += total - shared
    assert raw4 % 3 == 0
    A4_dual = raw4 // 3
    assert A4_dual == 84240
    dual_min_distance = 3

    hyper = []
    for _ in range(4):
        candidates = [
            maskvec(m) for m in range(1, 256)
            if all(int(maskvec(m) @ F8 @ y) % 2 == 0 for y in hyper)
        ]
        e = next(x for x in candidates if q8(x) == 0)
        f = next(y for y in candidates if q8(y) == 0 and int(e @ F8 @ y) % 2 == 1)
        hyper.extend([e, f])
    P = np.column_stack(hyper)
    assert rank2(P) == 8

    pauli_ok = True
    for m in range(256):
        c = maskvec(m)
        x = (P @ c) % 2
        qp = int((c[0]&c[1]) ^ (c[2]&c[3]) ^ (c[4]&c[5]) ^ (c[6]&c[7]))
        pauli_ok &= (q8(x) == qp)
    assert pauli_ok

    result = {
        "passes": list(range(4472, 4480)),
        "4472_module": {
            "PSp_order_line_action": 25920,
            "PGSp_order_line_action": 51840,
            "quotient10_inner_image_order": len(inner10),
            "quotient10_outer_image_order": len(outer10),
            "fixed_subspace_dimension": 1,
            "fixed_perp_dimension": 9,
            "filtration_dimensions": [1, 9, 10],
            "composition_dimensions": [1, 8, 1],
            "middle8_inner_image_order": len(inner8),
            "middle8_outer_image_order": len(outer8),
            "middle8_nonzero_orbits": [120, 135],
            "middle8_irreducible_under_PSp": True
        },
        "4473_four_spin": {
            "spins": 40,
            "interactions": 1620,
            "hamiltonian": "E(b)=-W4(b)=-1620+2*wt(H^T b)",
            "ground_energy": ground_energy,
            "ground_state_degeneracy": ground_degeneracy,
            "ground_states": ["all +", "all -"],
            "one_line_flip_weight": one_flip_weight,
            "one_line_flip_energy": one_flip_energy,
            "random_exact": {
                "E_energy": 0,
                "Var_energy": 1620,
                "third_moment_energy": -12960,
                "fourth_moment_energy": 9891720
            },
            "deterministic_sample": {
                "n": nsamp,
                "seed": 4473,
                "corr_spectral_radius_vs_energy": sample_corr,
                "ramanujan_fraction": float(ram.mean()),
                "mean_energy_all": float(energies.mean()),
                "sd_energy_all": float(energies.std()),
                "mean_energy_ramanujan_subset": float(energies[ram].mean())
            },
            "boundary": "The sampled correlation is empirical; the exact ground-state and null-moment statements are not sampled."
        },
        "4474_cycle_semantics": {
            "induced_apartment_C4": 1620,
            "line_internal_K4_C4": 120,
            "all_simple_C4": 1740,
            "legacy_pass4433_records": 3480,
            "legacy_record_multiplicity": 2,
            "audit_note": "C4=1620 is correct only when C4 means induced generalized-quadrangle apartments; all simple C4 total 1740."
        },
        "4475_artin_ihara": {
            "signed_hashimoto_dimension": 480,
            "trace_B3": "24*S, S=sum_l sigma_l",
            "trace_B4": "960+8*W4",
            "log_L_through_u4": "8*S*u^3 + (240+2*W4)*u^4 + O(u^5)",
            "fixed_960_interpretation": "8 orientations * 120 line-internal simple C4",
            "sample_checks": ihara_checks
        },
        "4476_code": {
            "parameters_proved": {"length": 1620, "dimension": 39},
            "primal_minimum_distance_status": "NOT_PROVED; d<=162 from a one-line generator; no smaller word among coefficient supports <=5",
            "coefficient_support_weight_census_1_to_5": low_support,
            "dual_minimum_distance": dual_min_distance,
            "dual_weight_3_words": A3_dual,
            "dual_weight_4_words": A4_dual,
            "automorphism_group_lower_bound_order": 51840,
            "automorphism_source": "PGSp(4,3) permutation action on the 1620 apartments"
        },
        "4477_e8_code_embedding": {
            "quadratic_type": "plus",
            "q0_count_including_zero": 136,
            "q1_count": 120,
            "nonzero_orbits": {"singular": 135, "nonsingular": 120},
            "PSp_nonsingular_stabilizer_order": len(stab_inner),
            "PSp_nonsingular_suborbits": sub_inner_120,
            "PGSp_nonsingular_stabilizer_order": len(stab_outer),
            "PGSp_nonsingular_suborbits": sub_outer_120,
            "singular_polar_graph_srg": srg135,
            "nonsingular_polar_graph_srg": srg120,
            "interpretation": "Exact fingerprint match to the repository's corrected E8/2E8 code embedding; this supplies a new apartment-code construction of that carrier."
        },
        "4478_four_qubit_pauli": {
            "explicit_hyperbolic_basis_verified": True,
            "canonical_quadratic": "q=sum_{i=1}^4 a_i b_i mod 2",
            "nonidentity_even_Y_classes": 135,
            "odd_Y_classes": 120,
            "boundary": "This is an isometry of finite symplectic/quadratic spaces; it does not assert a physical four-qubit realization of the apartment code."
        },
        "4479_macwilliams_thermal": {
            "partition_function": "Z(beta)=2*exp(1620*beta)*W_C(exp(-2*beta))",
            "two_variable_macwilliams": "W_C(x,y)=|C_perp|^{-1} W_Cperp(x+y,x-y)",
            "code_dimension": 39,
            "dual_dimension": 1581,
            "ground_state_factor_2": "ker(H^T)=<1_40>",
            "dual_low_temperature_seed": {"A3_perp": A3_dual, "A4_perp": A4_dual},
            "boundary": "The identity is exact finite coding/statistical mechanics; no thermodynamic-limit phase transition is claimed."
        },
        "literature_context": {
            "artin_ihara": "Stark--Terras, Zeta Functions of Finite Graphs and Coverings, Part II, Adv. Math. 154 (2000).",
            "real_four_qubit_pauli": "Saniga--Levay--Pracna, arXiv:1202.2973 (135 symmetric / 120 skew real four-qubit Pauli elements)."
        },
        "global_boundary": "Finite exact results plus an explicitly labelled deterministic random sample. No continuum/physical identification is inferred."
    }

    out = ROOT / "data" / "PART_W33_PASS4472_4479_APARTMENT_MODULE_THERMO_IHARA_PAULI.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Passes 4472--4479 PASS")
    print("  4472: faithful quotient action 25920/51840; filtration 1|8|1")
    print("  4473: exact two-fold ground state at E=-1620; sampled corr(rho,E)=%.6f" % sample_corr)
    print("  4474: simple C4 = 1740 = 1620 apartments + 120 internal; legacy records=3480")
    print("  4475: tr(B^4)=960+8W4; log L coefficient u^4=240+2W4")
    print("  4476: dual d=3, A3=2160, A4=84240; primal d<=162 not promoted to equality")
    print("  4477: plus O8 carrier, orbits 135/120, SRGs 135/120 recovered")
    print("  4478: explicit four-qubit Pauli hyperbolic isometry verified")
    print("  4479: exact MacWilliams thermal transform recorded")
    print("  wrote", out.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
