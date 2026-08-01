"""Passes 1612-1614 -- the frame incidence kernel IS the Hoffman eigenspace.

Pass 1536/1541 (parallel track) OWNS the [240,195,4]_2 frame code, the 45 octets,
and the observation that the 405 octet resolution cuts are "redundant over Q".
This pass explains WHY, and turns the explanation into a generator.

The chain:

    M          540 x 240 frame/edge incidence (Pass 1390 cross-matching)
    M M^T      = 4I + A_H     iff two distinct frames share at most one edge
    ker(M^T)   = the (-4)-eigenspace of the frame graph H
    col(M)     = ker(M^T)^perp = the space of FREE resolution constraints

Every colour class S of every resolution has chi_S - (1/9)1 in E_{-4}
(Pass 1491, Hoffman-tight).  Hence for ANY w orthogonal to E_{-4},

    <w, chi_S> = (sum w)/9    exactly, for all 9 classes, with no search.

The octet neighbourhoods are one instance.  col(M) is the whole space of them.

Run:  py -3 analysis/w33_pass1612_1614_frame_kernel_and_the_simplex.py
"""

from __future__ import annotations

import itertools
import json
import os
from fractions import Fraction

import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "data",
                   "w33_pass1612_1614_frame_kernel_simplex.json")


# ---------------------------------------------------------------- W(3,3)

def build_w33():
    """40 points / 40 totally isotropic lines of the symplectic GQ(3,3)."""
    F = (0, 1, 2)

    def norm(v):
        """Canonical projective representative over F_3."""
        for x in v:
            if x:
                inv = 1 if x == 1 else 2
                return tuple((inv * y) % 3 for y in v)
        return None

    pts = sorted({norm(v) for v in itertools.product(F, repeat=4) if any(v)})
    assert len(pts) == 40, len(pts)
    idx = {p: i for i, p in enumerate(pts)}

    # symplectic form x0 y1 - x1 y0 + x2 y3 - x3 y2
    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % 3

    # collinear <=> perpendicular and distinct
    A = np.zeros((40, 40), dtype=np.int64)
    for i, p in enumerate(pts):
        for j, q in enumerate(pts):
            if i != j and B(p, q) == 0:
                A[i, j] = 1

    # totally isotropic lines: the 4 points of span(p,q) when B(p,q)=0
    lines = set()
    for i, j in itertools.combinations(range(40), 2):
        if A[i, j]:
            span = {norm(tuple((a * pts[i][k] + b * pts[j][k]) % 3
                               for k in range(4)))
                    for a in F for b in F if (a, b) != (0, 0)}
            lines.add(tuple(sorted(idx[p] for p in span)))
    lines = sorted(lines)
    assert len(lines) == 40, len(lines)
    assert all(len(L) == 4 for L in lines)
    return pts, idx, A, lines


def edge_list(A):
    """The 240 collinear pairs, in a fixed order."""
    E = [(i, j) for i in range(40) for j in range(i + 1, 40) if A[i, j]]
    assert len(E) == 240, len(E)
    return E, {e: k for k, e in enumerate(E)}


def frames_and_M(A, lines, eidx):
    """540 frames = unordered pairs of DISJOINT t.i. lines; M = cross-matching."""
    frames, rows = [], []
    for a, b in itertools.combinations(range(40), 2):
        La, Lb = set(lines[a]), set(lines[b])
        if La & Lb:
            continue
        # GQ axiom: each point of La is collinear with exactly one point of Lb
        match = []
        for p in sorted(La):
            nb = [q for q in sorted(Lb) if A[p, q]]
            assert len(nb) == 1, (p, nb)
            match.append((min(p, nb[0]), max(p, nb[0])))
        assert len(set(match)) == 4
        frames.append((a, b))
        rows.append(sorted(eidx[e] for e in match))
    assert len(frames) == 540, len(frames)
    M = np.zeros((540, 240), dtype=np.int64)
    for f, cols in enumerate(rows):
        M[f, cols] = 1
    return frames, rows, M


def grids(A):
    """The 45 octets: 4x4 grids (K_{4,4} induced subgraphs), from mu-sets."""
    found = set()
    for p in range(40):
        for q in range(p + 1, 40):
            if A[p, q]:
                continue
            B = [r for r in range(40) if A[p, r] and A[q, r]]
            if len(B) != 4:
                continue
            Aside = [r for r in range(40) if all(A[r, b] for b in B)]
            if len(Aside) == 4:
                found.add((tuple(sorted(Aside)), tuple(sorted(B))))
    # each grid found once per ordered choice of part; canonicalise
    canon = {tuple(sorted([a, b])) for a, b in found}
    return sorted(canon)


# ---------------------------------------------------------------- exact rank

def rank_mod(Mat, p):
    """Exact rank of an integer matrix over F_p."""
    Amat = [[int(x) % p for x in row] for row in Mat]
    rows, cols = len(Amat), len(Amat[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if Amat[i][c]), None)
        if piv is None:
            continue
        Amat[r], Amat[piv] = Amat[piv], Amat[r]
        inv = pow(Amat[r][c], p - 2, p)
        Amat[r] = [(x * inv) % p for x in Amat[r]]
        for i in range(rows):
            if i != r and Amat[i][c]:
                f = Amat[i][c]
                Amat[i] = [(x - f * y) % p for x, y in zip(Amat[i], Amat[r])]
        r += 1
        if r == rows:
            break
    return r


def main():
    res = {}
    pts, idx, A, lines = build_w33()
    E, eidx = edge_list(A)
    frames, rows, M = frames_and_M(A, lines, eidx)
    print(f"W(3,3): 40 points, {len(lines)} lines, {len(E)} edges, "
          f"{len(frames)} frames")

    # ---- Pass 1612 : M M^T = 4I + A_H, so ker(M^T) = E_{-4}(H)
    G = M @ M.T
    off = G - np.diag(np.diag(G))
    max_share = int(off.max())
    print(f"\n[1612] max edges shared by two distinct frames : {max_share}")
    AH = (off > 0).astype(np.int64)
    identity = 4 * np.eye(540, dtype=np.int64)
    is_4I_plus_A = bool(np.array_equal(G, identity + AH))
    print(f"       M M^T == 4I + A_H                        : {is_4I_plus_A}")
    deg = sorted(set(AH.sum(1).tolist()))
    print(f"       H degrees                                : {deg}")

    evH = np.linalg.eigvalsh(AH.astype(float))
    spec = {}
    for x in evH:
        k = round(x)
        spec[k] = spec.get(k, 0) + 1
    print(f"       spec(H)                                  : "
          f"{sorted(spec.items(), reverse=True)}")

    rq = int(np.linalg.matrix_rank(M.astype(float)))
    r2, r3 = rank_mod(M, 2), rank_mod(M, 3)
    rbig = rank_mod(M, 1000003)
    dim_Eneg4 = spec.get(-4, 0)
    print(f"\n       rank_Q(M)   = {rq}   (= {rbig} mod a large prime)")
    print(f"       rank_F2(M)  = {r2}   <- parallel track's [240,195,4]")
    print(f"       rank_F3(M)  = {r3}")
    print(f"       540 - dim E_(-4) = 540 - {dim_Eneg4} = {540 - dim_Eneg4}")
    print(f"       col(M) == E_(-4)^perp                     : "
          f"{rq == 540 - dim_Eneg4}")
    print(f"       mod-2 rank DEFICIENCY = {rq} - {r2} = {rq - r2}")

    res["pass1612"] = {
        "max_shared_edges": max_share,
        "MMT_is_4I_plus_AH": is_4I_plus_A,
        "spec_H": {str(k): v for k, v in sorted(spec.items(), reverse=True)},
        "rank_Q_M": rq, "rank_F2_M": r2, "rank_F3_M": r3,
        "dim_E_minus4": dim_Eneg4,
        "colM_equals_Eperp": rq == 540 - dim_Eneg4,
        "mod2_deficiency": rq - r2,
    }

    # ---- Pass 1613 : the octet cuts, and the generator that produces them
    oct8 = grids(A)
    print(f"\n[1613] grids (octets) found                     : {len(oct8)}")
    K = np.zeros((len(oct8), 240), dtype=np.int64)
    for o, (P, Q) in enumerate(oct8):
        for p in P:
            for q in Q:
                assert A[p, q], "grid part not complete"
                K[o, eidx[(min(p, q), max(p, q))]] = 1
    wts = sorted(set(K.sum(1).tolist()))
    cover = sorted(set(K.sum(0).tolist()))
    print(f"       octet edge-weights                       : {wts}")
    print(f"       times each edge is covered               : {cover}")

    # N(o) = frames meeting octet o in >0 edges; parallel track reports 0 or 2
    inter = M @ K.T                       # 540 x 45, |matching(f) cap octet o|
    sizes = sorted(set(inter.flatten().tolist()))
    Nsz = sorted(set((inter == 2).sum(0).tolist()))
    print(f"       |frame cap octet| values                 : {sizes}")
    print(f"       frames meeting a fixed octet twice       : {Nsz}")

    # THE POINT: is chi_{N(o)} orthogonal to E_{-4}?  Project and measure.
    w_, V_ = np.linalg.eigh(AH.astype(float))
    Eneg = V_[:, np.abs(w_ + 4) < 1e-6]           # 540 x 315
    worst = 0.0
    for o in range(len(oct8)):
        chi = (inter[:, o] == 2).astype(float)
        worst = max(worst, float(np.linalg.norm(Eneg.T @ chi)))
    print(f"       max ||P_(-4) chi_N(o)||                  : {worst:.3e}")

    # and the generator: every column of M is such a w, by construction
    colworst = float(np.abs(Eneg.T @ M.astype(float)).max())
    print(f"       max |P_(-4) (column of M)|               : {colworst:.3e}")

    res["pass1613"] = {
        "n_octets": len(oct8), "octet_weights": wts, "edge_multiplicity": cover,
        "frame_octet_intersections": sizes,
        "frames_meeting_octet_twice": Nsz,
        "max_proj_octet_nbhd_on_Eminus4": worst,
        "max_proj_M_columns_on_Eminus4": colworst,
        "free_constraint_space_dim": rq,
    }

    # ---- Pass 1614 : a resolution is a regular 8-simplex in E_{-4}
    n, k, ncls = 540, 60, 9
    nrm2 = Fraction(k) - Fraction(k * k, n)
    ip = Fraction(0) - Fraction(k * k, n)
    print(f"\n[1614] centred class vector norm^2               : {nrm2} "
          f"= {float(nrm2):.4f}")
    print(f"       pairwise inner product (classes disjoint) : {ip} "
          f"= {float(ip):.4f}")
    print(f"       regular simplex needs ip = -norm^2/(c-1)  : "
          f"{ip == -nrm2 / (ncls - 1)}")
    print(f"       => 9 vectors of equal norm, equal angle, summing to 0")
    print(f"          i.e. a REGULAR 8-SIMPLEX inscribed in E_(-4) "
          f"(dim {dim_Eneg4})")

    res["pass1614"] = {
        "centred_norm_sq": [nrm2.numerator, nrm2.denominator],
        "pairwise_inner_product": [ip.numerator, ip.denominator],
        "is_regular_simplex": ip == -nrm2 / (ncls - 1),
        "ambient_dim": dim_Eneg4, "simplex_dim": ncls - 1,
    }

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(res, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
