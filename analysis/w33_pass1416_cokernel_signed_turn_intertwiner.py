#!/usr/bin/env python3
"""Pass 1416: explicit frame-cokernel / signed-turn intertwiner.

This verifier rebuilds W(3,3), the canonical 540x240 frame cross-matching
matrix M, and the signed-turn operator K in one common edge ordering.  It then
constructs the natural point-edge bridge that closes Pass 1412's open module
question.

All claims are finite exact matrix identities.  No physics interpretation is
used or asserted.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
from math import gcd
from pathlib import Path
from functools import reduce

import numpy as np

Q = 3
OMEGA = np.array([[0,0,1,0],[0,0,0,1],[-1,0,0,0],[0,-1,0,0]], dtype=np.int64) % Q
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1416_cokernel_signed_turn_intertwiner.json"


def norm(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv*y) % Q for y in v)


def om(u, v):
    return int((np.array(u, dtype=np.int64) @ OMEGA @ np.array(v, dtype=np.int64)) % Q)


def canon_edge(a, b):
    return (a, b) if a < b else (b, a)


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def invperm(p):
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def generated_group(gens):
    identity = tuple(range(len(gens[0])))
    gens = list(gens) + [invperm(g) for g in gens]
    seen = {identity}
    todo = collections.deque([identity])
    while todo:
        h = todo.popleft()
        for g in gens:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                todo.append(x)
    return sorted(seen)


def rank_mod(A, p):
    A = np.array(A, dtype=np.int64) % p
    m, n = A.shape
    r = 0
    for c in range(n):
        piv = np.flatnonzero(A[r:, c])
        if not len(piv):
            continue
        i = r + int(piv[0])
        if i != r:
            A[[r, i]] = A[[i, r]]
        A[r] = (A[r] * pow(int(A[r, c]), -1, p)) % p
        nz = np.flatnonzero(A[:, c])
        nz = nz[nz != r]
        if len(nz):
            A[nz] = (A[nz] - A[nz, c, None] * A[r]) % p
        r += 1
        if r == m:
            break
    return r


def gcd_entries(A):
    return reduce(gcd, (abs(int(x)) for x in A.ravel() if x), 0)


def build_geometry():
    points = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    pidx = {p:i for i,p in enumerate(points)}
    edges = [(i,j) for i,j in itertools.combinations(range(40),2) if om(points[i],points[j]) == 0]
    eidx = {e:i for i,e in enumerate(edges)}
    eset = set(edges)

    def span_line(i, j):
        p, r = points[i], points[j]
        ans = set()
        for a, b in itertools.product(range(Q), repeat=2):
            if a or b:
                y = tuple((a*p[k] + b*r[k]) % Q for k in range(4))
                ans.add(pidx[norm(y)])
        return frozenset(ans)

    lines = sorted({span_line(i,j) for i,j in edges}, key=lambda s: tuple(sorted(s)))
    lidx = {L:i for i,L in enumerate(lines)}
    frames = [(i,j) for i,j in itertools.combinations(range(40),2) if lines[i].isdisjoint(lines[j])]
    fidx = {f:i for i,f in enumerate(frames)}

    def transvection(v):
        vv = np.array(v, dtype=np.int64)
        out = []
        for x in points:
            y = (np.array(x, dtype=np.int64) + om(x,v)*vv) % Q
            out.append(pidx[norm(tuple(y))])
        return tuple(out)

    # A deterministic four-transvection generating set for PSp(4,3).
    gen_vecs = [(1,1,0,2), (1,2,1,1), (1,2,2,0), (0,1,0,1)]
    G = generated_group([transvection(v) for v in gen_vecs])
    assert len(G) == 25920

    def line_perm(g):
        return tuple(lidx[frozenset(g[i] for i in L)] for L in lines)

    line_actions = [line_perm(g) for g in G]
    base = frames[0]
    L1, L2 = sorted(lines[base[0]]), sorted(lines[base[1]])
    stab = [(g,lp) for g,lp in zip(G,line_actions) if {lp[base[0]],lp[base[1]]} == set(base)]
    assert len(stab) == 48

    invariant = []
    for q in itertools.permutations(L2):
        matching = frozenset(canon_edge(L1[i], q[i]) for i in range(4))
        if all(frozenset(canon_edge(g[a],g[b]) for a,b in matching) == matching for g,_ in stab):
            invariant.append(matching)
    assert len(invariant) == 1
    base_matching = invariant[0]

    matchings = [None] * 540
    for g,lp in zip(G,line_actions):
        fr = tuple(sorted((lp[base[0]],lp[base[1]])))
        image = frozenset(canon_edge(g[a],g[b]) for a,b in base_matching)
        k = fidx[fr]
        if matchings[k] is None:
            matchings[k] = image
        else:
            assert matchings[k] == image
    assert all(x is not None for x in matchings)

    M = np.zeros((540,240), dtype=np.int64)
    for r,matching in enumerate(matchings):
        for e in matching:
            assert e in eidx
            M[r,eidx[e]] = 1

    A = np.zeros((40,40), dtype=np.int64)
    N = np.zeros((40,240), dtype=np.int64)       # unsigned point-edge incidence
    d = np.zeros((40,240), dtype=np.int64)       # oriented point-edge incidence
    for j,(a,b) in enumerate(edges):
        A[a,b] = A[b,a] = 1
        N[a,j] = N[b,j] = 1
        d[a,j] = -1
        d[b,j] = 1

    directed = []
    for a,b in edges:
        directed.extend(((a,b),(b,a)))
    didx = {e:i for i,e in enumerate(directed)}
    nbr = [set() for _ in points]
    for a,b in edges:
        nbr[a].add(b); nbr[b].add(a)
    B = np.zeros((480,480), dtype=np.int8)
    T = np.zeros_like(B)
    for i,(a,b) in enumerate(directed):
        for c in nbr[b]:
            if c == a:
                continue
            j = didx[(b,c)]
            B[i,j] = 1
            if canon_edge(a,c) in eset:
                T[i,j] = 1
    C = 2*T - B
    R = np.zeros((480,240), dtype=np.int8)
    for j,(a,b) in enumerate(edges):
        R[didx[(a,b)],j] = 1
        R[didx[(b,a)],j] = -1
    K = (R.T @ C @ R).astype(np.int64)

    return points, edges, lines, frames, G, M, A, N, d, K


def certificate():
    points, edges, lines, frames, G, M, A, N, d, K = build_geometry()
    I40 = np.eye(40, dtype=np.int64)
    I240 = np.eye(240, dtype=np.int64)

    Pm_num = (A - 12*I40) @ (A - 2*I40)            # 96 E_{-4}
    P10_num = (K + 6*I240) @ (K - 2*I240) @ (K - 4*I240)  # 768 E_{10}

    # Unsigned quotient projector and orientation-twisted bridge.
    Cnum = N.T @ Pm_num @ N
    Fnum = d.T @ Pm_num @ N
    c_content = gcd_entries(Cnum)
    f_content = gcd_entries(Fnum)
    Cint = Cnum // c_content
    Fint = Fnum // f_content

    checks = {
        "counts_40_240_40_540": (len(points),len(edges),len(lines),len(frames)) == (40,240,40,540),
        "psp_order_25920": len(G) == 25920,
        "canonical_matching_rows_distinct": len({tuple(np.flatnonzero(row)) for row in M}) == 540,
        "every_edge_covered_nine_times": set(map(int,M.sum(axis=0))) == {9},
        "rank_M_Q_225": int(np.linalg.matrix_rank(M.astype(float), tol=1e-8)) == 225,
        "rank_M_F2_195": rank_mod(M,2) == 195,
        "signed_turn_intertwining": np.max(np.abs(K @ d.T - d.T @ (6*I40 - A))) == 0,
        "point_projector_exact": np.max(np.abs(Pm_num @ Pm_num - 96*Pm_num)) == 0,
        "K10_projector_exact": np.max(np.abs(P10_num @ P10_num - 768*P10_num)) == 0,
        "unsigned_projector_content_16": c_content == 16,
        "bridge_content_16": f_content == 16,
        "Cint_projector_scale_48": np.max(np.abs(Cint @ Cint - 48*Cint)) == 0,
        "frame_rows_annihilated_by_Cint": np.max(np.abs(M @ Cint)) == 0,
        "Cint_rank_Q_15": int(np.linalg.matrix_rank(Cint.astype(float), tol=1e-8)) == 15,
        "Cint_image_equals_cokernel_dual": rank_mod(np.vstack([M,Cint]),1000003) == 240,
        "bridge_descends_through_cokernel": np.max(np.abs(Fint @ M.T)) == 0,
        "bridge_lands_in_K10": np.max(np.abs((K-10*I240) @ Fint)) == 0,
        "bridge_rank_Q_15": int(np.linalg.matrix_rank(Fint.astype(float), tol=1e-8)) == 15,
        "bridge_rank_F2_14": rank_mod(Fint,2) == 14,
        "bridge_square_zero_F2": np.max((Fint @ Fint) % 2) == 0,
        "bridge_image_inside_M_image_F2": rank_mod(np.vstack([M,Fint.T]),2) == 195,
        "bridge_rowspace_inside_M_image_F2": rank_mod(np.vstack([M,Fint]),2) == 195,
        "partial_isometry_left": np.max(np.abs(Fnum @ Fnum.T - 1536*P10_num)) == 0,
        "partial_isometry_right": np.max(np.abs(Fnum.T @ Fnum - 1536*Cnum)) == 0,
    }
    checks = {k:bool(v) for k,v in checks.items()}

    raw = {
        "M_sha256": hashlib.sha256(M.astype(np.int8).tobytes()).hexdigest(),
        "K_sha256": hashlib.sha256(K.astype(np.int16).tobytes()).hexdigest(),
        "Cint_sha256": hashlib.sha256(Cint.astype(np.int16).tobytes()).hexdigest(),
        "Fint_sha256": hashlib.sha256(Fint.astype(np.int16).tobytes()).hexdigest(),
    }
    digest = hashlib.sha256(json.dumps(raw,sort_keys=True,separators=(",",":")).encode()).hexdigest()

    return {
        "schema":"w33.pass1416.cokernel_signed_turn_intertwiner.v1",
        "status":"PASS" if all(checks.values()) else "FAIL",
        "theorem":(
            "Let M be the 540x240 canonical frame cross-matching matrix, N the unsigned "
            "point-edge incidence, d the oriented point-edge incidence, A the W33 adjacency "
            "matrix, and K the signed-turn operator. Then K d^T=d^T(6I-A). With "
            "P=(A-12I)(A-2I)=96E_{-4}, the integral matrix F=d^T P N/16 annihilates "
            "im(M^T), has rational rank 15, and has image ker(K-10I). Hence it induces an "
            "explicit PSp(4,3)-equivariant isomorphism coker(M) tensor Q -> ker(K-10I)."
        ),
        "mod2_refinement":(
            "F mod 2 has rank 14 and square zero. Its kernel on the 45-dimensional modular "
            "cokernel has dimension 31, leaving a canonical 14-dimensional quotient. This "
            "selects the nontrivial 14 in the reduction of the rational 15; the second "
            "isomorphic 14 remains in the 31-dimensional kernel with factors 1,1,1,6,8,14."
        ),
        "key_identities":{
            "intertwiner":"K d^T = d^T(6I-A)",
            "point_projector":"P^2=96P",
            "cokernel_projector":"C=(N^T P N)/16; C^2=48C; MC=0",
            "bridge":"F=(d^T P N)/16; FM^T=0; (K-10I)F=0",
            "partial_isometry":"Fnum Fnum^T=1536 P10num and Fnum^T Fnum=1536 Cnum",
        },
        "dimensions":{
            "rank_M_Q":225,"rank_M_F2":195,
            "cokernel_Q":15,"cokernel_F2":45,
            "rank_F_Q":15,"rank_F_F2":14,"kernel_of_induced_F_mod2":31,
        },
        "checks":checks,
        "matrix_hashes":raw,
        "certificate_sha256":digest,
        "boundary":(
            "The result is an exact finite-module bridge. It does not identify the two "
            "15-dimensional subspaces as literal coordinate subspaces: one uses the unsigned "
            "edge action and the other the orientation-signed edge action. The theorem is the "
            "natural equivariant intertwiner between those actions."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    payload = certificate()
    text = json.dumps(payload, sort_keys=True, separators=(",",":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Pass 1416 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({"status":payload["status"],"checks":sum(payload["checks"].values()),"total":len(payload["checks"]),"certificate":payload["certificate_sha256"]}))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
