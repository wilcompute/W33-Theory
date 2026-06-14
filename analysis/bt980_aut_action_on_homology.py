#!/usr/bin/env python3
"""
(R1 canonicality) The canonical Aut(W(3,3)) action on the homology H.

BT932 found the vertex E8 witness is symmetry-isolated and called for "a
larger chain-complex symmetry"; BT936 left selector uniqueness unresolved
pending "a chain action of the symmetry group". The canonical such symmetry
is the FULL automorphism group of W(3,3): PSp(4,3) (order 25920), induced by
the symplectic group on the 40 points, acts on the chain complex (it commutes
with A2 = A mod 2) and hence on H = ker(A2)/im(A2) ~ F2^8.

We construct that action explicitly:
  T1  symplectic transvections t_v generate a group acting on the 40 points
      that preserves adjacency (commutes with A2);
  T2  the induced action on H is a homomorphism rho: PSp(4,3) -> GL(8,2);
      we compute the image order and whether it preserves the canonical
      symplectic form B (=> image in Sp(8,2)) and is irreducible;
  T3  E6 c E8 => W(E6) c W(E8)=Aut(E8 lattice); we compare the image to the
      W(E6) action on E8/2E8 to test whether E8 is the canonical equivariant
      definite lift of H (the R1 canonicality question).
"""
from __future__ import annotations

from itertools import combinations, product
import json

import numpy as np


def canon(v):
    for x in v:
        if x % 3:
            c = 1 if x % 3 == 1 else 2
            return tuple((c * y) % 3 for y in v)
    raise ValueError


def f2_rref(M):
    M = (np.array(M, dtype=np.int64) % 2).copy()
    rows, cols = M.shape
    pr = 0
    piv = []
    for c in range(cols):
        r = next((i for i in range(pr, rows) if M[i, c]), None)
        if r is None:
            continue
        M[[pr, r]] = M[[r, pr]]
        for i in range(rows):
            if i != pr and M[i, c]:
                M[i] = (M[i] + M[pr]) % 2
        piv.append(c)
        pr += 1
    return M[:pr], piv


def f2_nullspace(M):
    R, piv = f2_rref(M)
    cols = M.shape[1]
    free = [c for c in range(cols) if c not in piv]
    prow = {c: i for i, c in enumerate(piv)}
    out = []
    for f in free:
        v = np.zeros(cols, dtype=np.int64)
        v[f] = 1
        for c in piv:
            v[c] = R[prow[c], f] % 2
        out.append(v % 2)
    return out


def solve_f2(Aug_cols, target):
    """Solve sum c_j basis_j = target over F2; basis_j are columns.
    Aug_cols: list of F2 vectors (basis). Returns coeff vector or None."""
    n = len(Aug_cols)
    # build matrix [basis^T | target] and reduce; columns are basis vectors
    M = np.array(Aug_cols, dtype=np.int64).T % 2     # 40 x n
    aug = np.concatenate([M, target.reshape(-1, 1) % 2], axis=1)
    rows, cols = aug.shape
    pr = 0
    where = {}
    for c in range(n):
        r = next((i for i in range(pr, rows) if aug[i, c]), None)
        if r is None:
            continue
        aug[[pr, r]] = aug[[r, pr]]
        for i in range(rows):
            if i != pr and aug[i, c]:
                aug[i] = (aug[i] + aug[pr]) % 2
        where[c] = pr
        pr += 1
    coeff = np.zeros(n, dtype=np.int64)
    for c, r in where.items():
        coeff[c] = aug[r, n] % 2
    return coeff


def main():
    pts = sorted({canon(v) for v in product(range(3), repeat=4) if any(v)})
    idx = {p: i for i, p in enumerate(pts)}
    n = 40

    def symp(x, y):
        return (x[0]*y[2] - x[2]*y[0] + x[1]*y[3] - x[3]*y[1]) % 3

    A = np.zeros((n, n), dtype=np.int64)
    for i, j in combinations(range(n), 2):
        if symp(pts[i], pts[j]) == 0:
            A[i, j] = A[j, i] = 1
    A2 = A % 2

    # homology: basis of ker(A2) = im-basis (16) + reps (8)
    ker = f2_nullspace(A2)
    imrows = A2.T % 2
    Rim, piv_im = f2_rref(imrows)
    im_basis = [Rim[i].copy() for i in range(len(piv_im))]   # 16
    reps = []
    cur = list(im_basis)
    for z in ker:
        Rc, pc = f2_rref(np.array(cur))
        r = z.copy() % 2
        for k, c in enumerate(pc):
            if r[c]:
                r = (r + Rc[k]) % 2
        if r.any():
            reps.append(z.copy() % 2)
            cur.append(z.copy() % 2)
    reps = reps[:8]
    cycle_basis = im_basis + reps          # 24 vectors, basis of ker(A2)

    def proj_H(z):
        """class of a cycle z in H = F2^8 (coords w.r.t. reps)."""
        c = solve_f2(cycle_basis, z % 2)
        return c[16:24] % 2                # last 8 = rep coords

    # canonical symplectic form B on H: B(rep_i,rep_j) = (rep_i^T A rep_j)/2 %2
    B = np.array([[int((reps[i] @ A @ reps[j]) // 2) % 2 for j in range(8)]
                  for i in range(8)], dtype=np.int64) % 2

    # ---- symplectic transvections generate the action ----
    def transvection_perm(v):
        v = np.array(v) % 3
        perm = [0]*n

        def sform(x, y):
            return (x[0]*y[2]-x[2]*y[0]+x[1]*y[3]-x[3]*y[1]) % 3
        for i, p in enumerate(pts):
            pv = np.array(p) % 3
            lam = sform(pv, v)
            img = tuple((pv + lam*v) % 3)
            perm[i] = idx[canon(img)]
        return perm

    # a generating set of transvections
    gens_v = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1),
              (1, 1, 0, 0), (1, 0, 1, 0), (0, 1, 0, 1), (1, 1, 1, 1)]
    perms = []
    for v in gens_v:
        p = transvection_perm(v)
        # verify graph automorphism (commutes with A2)
        P = np.eye(n, dtype=np.int64)[p]
        assert np.array_equal((P @ A @ P.T) % 2, A2), f"t_{v} not auto"
        perms.append(p)
    print(f"T1 built {len(perms)} symplectic transvections; all preserve "
          f"adjacency (commute with A2).")

    def rho(perm):
        """8x8 F2 matrix: action of the permutation on H."""
        cols = []
        for z in reps:
            zp = np.zeros(n, dtype=np.int64)
            zp[perm] = z            # permute coordinates (push-forward)
            cols.append(proj_H(zp % 2))
        return np.array(cols, dtype=np.int64).T % 2     # columns = images

    gen_mats = [rho(p) for p in perms]
    # check each preserves B: g^T B g = B
    pres = all(np.array_equal((g.T @ B @ g) % 2, B) for g in gen_mats)
    # check invertible over F2
    inv = all(len(f2_rref(g)[1]) == 8 for g in gen_mats)
    print(f"T2 rho generators: invertible={inv}, preserve B (symplectic)="
          f"{pres}")

    # close the group in GL(8,2)
    def matkey(m):
        return tuple(int(x) for x in (m % 2).flatten())
    seen = {}
    frontier = [np.eye(8, dtype=np.int64)]
    seen[matkey(frontier[0])] = True
    while frontier:
        nf = []
        for m in frontier:
            for g in gen_mats:
                p = (m @ g) % 2
                k = matkey(p)
                if k not in seen:
                    seen[k] = True
                    nf.append(p)
        frontier = nf
        if len(seen) > 2_000_000:
            print("  (group too large, aborting closure)")
            break
    order = len(seen)
    print(f"T2 image of <transvections> on H has order {order} "
          f"(|PSp(4,3)|=25920, |Sp(8,2)|=47377612800)")

    # irreducibility quick test: does any proper nonzero F2-subspace stay
    # invariant under all gens? (test all 1-dim and the radical-free check)
    irred = is_irreducible_f2(gen_mats)
    print(f"T2 action on F2^8 irreducible: {irred}")

    # T3 reading
    print("T3 E6 c E8 => W(E6) c W(E8)=Aut(E8); the canonical definite lift")
    print("   of H would be E8 carrying this same image as the W(E6) action")
    print("   on E8/2E8. Image order divides |W(E6)|=51840 and embeds in")
    print(f"   Sp(8,2) (T2 pres={pres}); matching it to W(E6)<W(E8) is the")
    print("   remaining canonicality step.")

    out = {
        "theorem": "(R1) canonical Aut(W33) action on homology H",
        "generators": len(perms),
        "image_order_on_H": order,
        "preserves_symplectic_B": bool(pres),
        "invertible": bool(inv),
        "irreducible_F2": bool(irred),
        "psp43_order": 25920,
        "note": "canonical large chain-complex symmetry (BT932 next target); "
                "image in Sp(8,2); E6<E8 framing for the definite lift",
    }
    with open("data/bt980_aut_action_on_homology.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nwrote data/bt980_aut_action_on_homology.json")


def cyclic_span_dim(v0, gens, dim=8):
    span = [v0 % 2]
    frontier = [v0 % 2]
    while frontier:
        nf = []
        for v in frontier:
            for g in gens:
                w = (g @ v) % 2
                if not in_span_f2(w, span):
                    span.append(w % 2)
                    nf.append(w % 2)
        frontier = nf
    return len(span)


def is_irreducible_f2(gens, dim=8):
    """RIGOROUS: a module is irreducible iff EVERY nonzero vector generates
    the whole module (cyclic span = full). If any nonzero vector has a
    proper cyclic span, that span is a proper invariant subspace."""
    import numpy as np
    for start in range(1, 1 << dim):
        v0 = np.array([(start >> i) & 1 for i in range(dim)], dtype=np.int64)
        if cyclic_span_dim(v0, gens, dim) < dim:
            return False          # found a proper invariant subspace
    return True


def in_span_f2(w, span):
    if not span:
        return not w.any()
    M = np.array(span + [w], dtype=np.int64) % 2
    r_with = len(f2_rref(M)[1])
    r_without = len(f2_rref(np.array(span, dtype=np.int64) % 2)[1])
    return r_with == r_without


if __name__ == "__main__":
    main()
