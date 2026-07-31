#!/usr/bin/env python3
"""Passes 1421--1424: full-Weyl bridge, integral defect, and cover extension.

This self-contained verifier extends the exact Passes 1416--1420 release.
It reconstructs W(3,3), its 540 canonical frame cross-matchings, the signed-turn
operator K, PSp(4,3), and one explicit outer symplectic similitude.

Certified results:
* the frame-cokernel/signed-turn bridge is equivariant for the full
  PGSp(4,3) ~= W(E6) action, not only PSp(4,3);
* the common degree-15 character is evaluated on all 51,840 Weyl elements;
* the integral bridge has Smith invariants 1^10, 3^4, 6 and saturation index
  486 = 2*3^5, so the rational isomorphism is not integral;
* six independently generated exact-cover orbits are disjoint from the sixteen
  C2 orbits and C2/C4 representatives frozen in Pass 1417, raising the certified
  lower bound from 226,800 to 298,080.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.domains import ZZ

Q = 3
OMEGA = np.array(
    [[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]],
    dtype=np.int64,
) % Q
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass1421_1424_outer_integral_cover_extension.json"
PRIOR = ROOT / "data" / "w33_pass1417_exact_cover_orbit_frontier.json"

SAMPLE_COVERS = [
[2,17,20,27,30,33,65,69,79,95,99,103,111,115,119,145,155,158,172,179,183,190,197,207,211,212,224,252,259,268,278,288,294,306,311,322,326,337,349,352,357,364,367,374,382,393,407,411,418,430,436,444,469,479,492,503,509,519,522,534],
[3,9,21,38,44,50,68,70,80,82,84,88,119,131,139,148,151,158,161,172,191,205,212,216,224,237,240,243,251,256,269,279,282,299,306,308,335,337,349,354,373,391,396,397,400,407,418,423,425,444,447,459,465,472,497,501,513,518,524,532],
[7,18,23,47,52,56,59,62,66,92,99,100,114,121,123,145,154,158,161,162,185,189,192,202,204,207,233,249,252,271,276,277,281,298,311,321,327,336,347,349,371,375,394,401,404,420,423,428,440,442,449,457,462,478,494,515,521,523,531,532],
[2,10,35,43,49,54,57,71,79,90,93,107,117,125,132,152,153,159,165,172,177,189,194,205,215,221,222,238,239,256,258,263,269,276,284,286,308,324,332,337,341,348,353,356,364,367,384,392,409,425,427,431,450,469,475,485,487,492,519,527],
[8,23,28,32,47,52,62,71,79,90,93,101,108,122,124,130,135,146,163,167,176,186,192,200,207,212,217,222,232,262,270,276,278,286,287,295,299,302,309,315,343,356,375,379,385,399,408,417,420,434,437,438,454,456,480,481,510,521,527,530],
[9,17,21,28,40,48,53,59,61,64,94,101,113,114,119,139,151,155,156,171,181,190,204,213,215,226,235,250,251,258,265,269,295,301,310,325,332,342,365,368,377,378,389,392,397,409,418,421,437,438,445,452,455,464,471,496,510,520,529,533],
[12,17,21,29,35,39,44,59,78,90,95,107,109,114,118,131,135,139,170,175,181,197,199,206,221,228,240,249,259,265,282,288,294,307,319,325,328,341,342,358,368,378,382,388,409,410,418,427,435,452,455,464,468,479,494,500,501,513,522,530],
]

PRIOR_C2 = [0,15,18,25,33,41,43,51,55,59,95,97,114,119,134,135,168,172,177,185,198,205,210,218,222,256,262,278,283,285,297,305,307,321,330,345,350,368,371,380,385,391,397,401,410,414,432,464,468,488,492,494,499,501,511,512,516,529,530,533]
PRIOR_C4 = [0,9,23,24,37,47,55,61,85,95,99,103,111,119,122,123,132,165,174,181,206,208,216,233,237,248,252,257,281,287,297,307,314,321,328,350,356,368,369,382,390,395,403,408,413,424,430,446,449,461,466,483,487,499,503,511,521,528,531,538]


def norm(v):
    v = tuple(int(x) % Q for x in v)
    if not any(v):
        return None
    for x in v:
        if x:
            inv = 1 if x == 1 else 2
            return tuple((inv * y) % Q for y in v)


def om(u, v):
    return int((np.array(u, dtype=np.int64) @ OMEGA @ np.array(v, dtype=np.int64)) % Q)


def add(u, v):
    return tuple((a + b) % Q for a, b in zip(u, v))


def sc(c, u):
    return tuple((c * a) % Q for a in u)


def pline(p, r):
    return frozenset(
        norm(add(sc(a, p), sc(b, r)))
        for a, b in itertools.product(range(Q), repeat=2)
        if a or b
    )


def compose(p, q):
    return tuple(p[q[i]] for i in range(len(p)))


def perm_order(p):
    seen = [False] * len(p)
    ans = 1
    for i in range(len(p)):
        if not seen[i]:
            j = i
            n = 0
            while not seen[j]:
                seen[j] = True
                n += 1
                j = p[j]
            ans = math.lcm(ans, n)
    return ans


def generate_group(gens, degree):
    identity = tuple(range(degree))
    seen = {identity}
    queue = collections.deque([identity])
    while queue:
        h = queue.popleft()
        for g in gens:
            x = compose(g, h)
            if x not in seen:
                seen.add(x)
                queue.append(x)
    return list(seen)


def rank_mod_p(A, p):
    A = np.asarray(A, dtype=np.int64) % p
    rows, cols = A.shape
    r = 0
    for c in range(cols):
        piv = np.flatnonzero(A[r:, c])
        if len(piv) == 0:
            continue
        i = r + int(piv[0])
        if i != r:
            A[[r, i]] = A[[i, r]]
        A[r, c:] = (A[r, c:] * pow(int(A[r, c]), -1, p)) % p
        factors = A[:, c].copy()
        factors[r] = 0
        nz = np.flatnonzero(factors)
        if len(nz):
            A[nz, c:] = (A[nz, c:] - factors[nz, None] * A[r, c:]) % p
        r += 1
        if r == rows:
            break
    return r


def primitive_integer_columns(nullspace):
    cols = []
    for v in nullspace:
        den = 1
        for x in v:
            den = math.lcm(den, int(x.q))
        arr = [int(x * den) for x in v]
        g = 0
        for x in arr:
            g = math.gcd(g, abs(x))
        if g:
            arr = [x // g for x in arr]
        cols.append(arr)
    return np.array(cols, dtype=object).T


def build_geometry():
    points = sorted({norm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    pidx = {p: i for i, p in enumerate(points)}
    edges = [(i, j) for i, j in itertools.combinations(range(40), 2) if om(points[i], points[j]) == 0]
    eidx = {e: i for i, e in enumerate(edges)}
    eset = set(edges)
    lines = sorted({tuple(sorted(pidx[p] for p in pline(points[i], points[j]))) for i, j in edges})
    lidx = {frozenset(L): i for i, L in enumerate(lines)}

    frames = []
    rows = []
    for a, b in itertools.combinations(range(40), 2):
        L1, L2 = lines[a], lines[b]
        if set(L1).isdisjoint(L2):
            frames.append((a, b))
            matching = []
            for x in L1:
                ys = [y for y in L2 if tuple(sorted((x, y))) in eidx]
                assert len(ys) == 1
                matching.append(eidx[tuple(sorted((x, ys[0])))])
            rows.append(sorted(matching))
    fidx = {f: i for i, f in enumerate(frames)}
    M = np.zeros((540, 240), dtype=np.int64)
    for i, row in enumerate(rows):
        M[i, row] = 1

    A = np.zeros((40, 40), dtype=np.int64)
    N = np.zeros((40, 240), dtype=np.int64)
    d = np.zeros((40, 240), dtype=np.int64)
    for j, (a, b) in enumerate(edges):
        A[a, b] = A[b, a] = 1
        N[a, j] = N[b, j] = 1
        d[a, j] = -1
        d[b, j] = 1

    directed = []
    for a, b in edges:
        directed.extend(((a, b), (b, a)))
    didx = {e: i for i, e in enumerate(directed)}
    adj = [set() for _ in points]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    B = np.zeros((480, 480), dtype=np.int64)
    T = np.zeros_like(B)
    for ei, (a, b) in enumerate(directed):
        for c in adj[b]:
            if c == a:
                continue
            fi = didx[(b, c)]
            B[ei, fi] = 1
            if tuple(sorted((a, c))) in eset:
                T[ei, fi] = 1
    C = 2 * T - B
    R = np.zeros((480, 240), dtype=np.int64)
    for j, (a, b) in enumerate(edges):
        R[didx[(a, b)], j] = 1
        R[didx[(b, a)], j] = -1
    K = R.T @ C @ R

    P = (A - 12 * np.eye(40, dtype=np.int64)) @ (A - 2 * np.eye(40, dtype=np.int64))
    Fnum = d.T @ P @ N
    assert np.all(Fnum % 16 == 0)
    F = Fnum // 16

    def transvection(v):
        vv = np.array(v, dtype=np.int64)
        out = []
        for x in points:
            xx = np.array(x, dtype=np.int64)
            coeff = int((xx @ OMEGA @ vv) % Q)
            out.append(pidx[norm(tuple((xx + coeff * vv) % Q))])
        return tuple(out)

    trans = [transvection(v) for v in points]
    psp = generate_group(trans, 40)
    similitude = np.diag([1, 1, 2, 2]).astype(np.int64)
    outer = tuple(
        pidx[norm(tuple((similitude @ np.array(x, dtype=np.int64)) % Q))]
        for x in points
    )
    return points, edges, lines, frames, rows, lidx, fidx, M, A, N, d, K, P, F, trans, psp, outer, similitude


def edge_action(g, edges, eidx):
    ep = np.empty(240, dtype=np.int16)
    sg = np.empty(240, dtype=np.int8)
    for j, (a, b) in enumerate(edges):
        ga, gb = g[a], g[b]
        ep[j] = eidx[tuple(sorted((ga, gb)))]
        sg[j] = 1 if ga < gb else -1
    return ep, sg


def first16_covers(M):
    row_masks = []
    col_rows = [[] for _ in range(240)]
    for r, row in enumerate(M):
        mask = 0
        for c in np.flatnonzero(row):
            c = int(c)
            mask |= 1 << c
            col_rows[c].append(r)
        row_masks.append(mask)
    col_bits = []
    for rr in col_rows:
        z = 0
        for r in rr:
            z |= 1 << r
        col_bits.append(z)
    conflicts = []
    for row in M:
        z = 0
        for c in np.flatnonzero(row):
            z |= col_bits[int(c)]
        conflicts.append(z)
    all_cols = (1 << 240) - 1
    all_rows = (1 << 540) - 1
    solutions = []

    def search(covered, active, chosen):
        if len(solutions) >= 16:
            return True
        if covered == all_cols:
            solutions.append(tuple(sorted(chosen)))
            return False
        remaining = all_cols ^ covered
        best = None
        best_n = 10**9
        x = remaining
        while x:
            bit = x & -x
            c = bit.bit_length() - 1
            x -= bit
            cand = col_bits[c] & active
            n = cand.bit_count()
            if n == 0:
                return False
            if n < best_n:
                best, best_n = cand, n
                if n == 1:
                    break
        x = best
        while x:
            bit = x & -x
            r = bit.bit_length() - 1
            x -= bit
            if search(covered | row_masks[r], active & ~conflicts[r], chosen + [r]):
                return True
        return False

    search(row_masks[0], all_rows & ~conflicts[0], [0])
    return solutions


def canonical_cover(cov, frame_actions):
    images = np.sort(frame_actions[:, np.array(cov, dtype=np.int16)], axis=1)
    rows = [tuple(map(int, row)) for row in images]
    unique = set(rows)
    return min(unique), len(unique)


def certificate():
    (
        points, edges, lines, frames, rows, lidx, fidx, M, A, N, d, K, P, F,
        trans, psp, outer, similitude,
    ) = build_geometry()
    eidx = {e: i for i, e in enumerate(edges)}
    I240 = np.eye(240, dtype=np.int64)
    P10num = (K + 6 * I240) @ (K - 2 * I240) @ (K - 4 * I240)

    ep_outer, sg_outer = edge_action(outer, edges, eidx)
    U_outer = np.zeros((240, 240), dtype=np.int64)
    S_outer = np.zeros_like(U_outer)
    for j in range(240):
        U_outer[ep_outer[j], j] = 1
        S_outer[ep_outer[j], j] = int(sg_outer[j])

    Lcross = primitive_integer_columns(sp.Matrix(M).nullspace())
    Bcross = sp.Matrix(Lcross)
    _, pivot_rows = Bcross.T.rref()
    pivot_rows = list(pivot_rows)
    Rcross = sp.Matrix([[int(Lcross[i, j]) for j in range(15)] for i in pivot_rows])
    Rinv = np.array(Rcross.inv().tolist(), dtype=np.int64)
    Lcross_i = np.array(Lcross, dtype=np.int64)
    E = np.array(edges, dtype=np.int16)
    edge_idx = -np.ones((40, 40), dtype=np.int16)
    for i, (a, b) in enumerate(edges):
        edge_idx[a, b] = edge_idx[b, a] = i

    def two_characters(g):
        ga = np.fromiter((g[int(a)] for a in E[:, 0]), dtype=np.int16, count=240)
        gb = np.fromiter((g[int(b)] for b in E[:, 1]), dtype=np.int16, count=240)
        ep = edge_idx[ga, gb].astype(np.int16)
        sg = np.where(ga < gb, 1, -1).astype(np.int16)
        inv = np.empty(240, dtype=np.int16)
        inv[ep] = np.arange(240, dtype=np.int16)
        action = Rinv @ Lcross_i[inv[np.array(pivot_rows, dtype=np.int16)], :]
        chi_cross = int(np.trace(action))
        numerator = int(np.sum(sg.astype(np.int64) * P10num[np.arange(240), ep]))
        assert numerator % 768 == 0
        return chi_cross, numerator // 768

    full_distribution = collections.Counter()
    outer_distribution = collections.Counter()
    mismatches = 0
    for h in psp:
        for coset, g in ((0, h), (1, compose(outer, h))):
            pair = two_characters(g)
            full_distribution[pair[0]] += 1
            mismatches += int(pair[0] != pair[1])
            if coset:
                outer_distribution[pair[0]] += 1

    D = smith_normal_form(sp.Matrix(F), domain=ZZ)
    smith = [abs(int(D[i, i])) for i in range(min(D.shape)) if D[i, i] != 0]
    smith_census = collections.Counter(smith)
    saturation_index = math.prod(smith)
    local_ranks = {str(p): rank_mod_p(F, p) for p in (2, 3, 5, 7)}

    frame_actions = np.empty((len(psp), 540), dtype=np.int16)
    for gi, g in enumerate(psp):
        lp = [lidx[frozenset(g[x] for x in L)] for L in lines]
        for i, (a, b) in enumerate(frames):
            frame_actions[gi, i] = fidx[tuple(sorted((lp[a], lp[b])))]

    def exact_cover(cov):
        counts = np.zeros(240, dtype=np.int16)
        for f in cov:
            counts[rows[f]] += 1
        return len(cov) == 60 and np.all(counts == 1)

    prior_payload = json.loads(PRIOR.read_text())
    prior_bound = int(prior_payload["lower_bounds"]["from_16_distinct_C2_orbits_plus_four_other_types"])
    prior_first16 = first16_covers(M)
    known = set()
    for cov in prior_first16 + [tuple(PRIOR_C2), tuple(PRIOR_C4)]:
        canonical, _ = canonical_cover(cov, frame_actions)
        known.add(canonical)

    sample_records = []
    new = {}
    for cov in SAMPLE_COVERS:
        canonical, orbit_size = canonical_cover(cov, frame_actions)
        digest = hashlib.sha256(",".join(map(str, canonical)).encode()).hexdigest()
        images = np.sort(frame_actions[:, np.array(cov, dtype=np.int16)], axis=1)
        target = np.sort(np.array(cov, dtype=np.int16))
        stab_rows = np.flatnonzero(np.all(images == target, axis=1))
        order_census = collections.Counter(perm_order(psp[int(i)]) for i in stab_rows)
        group_type = "C2" if len(stab_rows) == 2 else ("C4" if len(stab_rows) == 4 and 4 in order_census else "other")
        rec = {
            "canonical_sha256": digest,
            "orbit_size": orbit_size,
            "stabilizer_order": len(stab_rows),
            "stabilizer_type": group_type,
            "stabilizer_element_order_census": {str(k): v for k, v in sorted(order_census.items())},
            "new_relative_to_pass1417_C2_C4_frontier": canonical not in known,
        }
        sample_records.append(rec)
        if canonical not in known:
            new[canonical] = rec
    added_orbit_mass = sum(rec["orbit_size"] for rec in new.values())
    extended_bound = prior_bound + added_orbit_mass

    checks = {
        "W33_counts_40_40_240_540": (len(points), len(lines), len(edges), len(frames)) == (40, 40, 240, 540),
        "PSp_order_25920": len(psp) == 25920,
        "outer_is_involution_outside_PSp": compose(outer, outer) == tuple(range(40)) and outer not in set(psp),
        "outer_similitude_multiplier_minus_one": np.array_equal((similitude.T @ OMEGA @ similitude) % 3, (2 * OMEGA) % 3),
        "full_Weyl_order_51840": 2 * len(psp) == 51840,
        "bridge_integral": np.all((d.T @ P @ N) % 16 == 0),
        "bridge_annihilates_matching_image": int(np.max(np.abs(F @ M.T))) == 0,
        "bridge_lands_in_K10": int(np.max(np.abs((K - 10 * I240) @ F))) == 0,
        "outer_K_equivariance": int(np.max(np.abs(S_outer @ K - K @ S_outer))) == 0,
        "outer_bridge_intertwining": int(np.max(np.abs(S_outer @ F - F @ U_outer))) == 0,
        "full_Weyl_character_equality": mismatches == 0,
        "full_character_distribution_locked": dict(sorted(full_distribution.items())) == {-5:36,-2:1440,-1:13635,0:25248,1:7920,2:2160,3:1320,6:80,15:1},
        "outer_coset_distribution_locked": dict(sorted(outer_distribution.items())) == {-5:36,-2:1440,-1:6480,0:9504,1:7920,3:540},
        "outer_involution_trace_three": two_characters(outer) == (3, 3),
        "bridge_rank_Q_15": len(smith) == 15,
        "bridge_smith_1_10_3_4_6_1": smith_census == collections.Counter({1:10,3:4,6:1}),
        "bridge_saturation_index_486": saturation_index == 486,
        "bridge_local_ranks_14_10_15_15": local_ranks == {"2":14,"3":10,"5":15,"7":15},
        "prior_bound_226800_loaded": prior_bound == 226800,
        "prior_first16_reproduced": len(prior_first16) == 16,
        "seven_sample_covers_exact": all(exact_cover(c) for c in SAMPLE_COVERS),
        "six_distinct_new_orbits": len(new) == 6 and all(r["new_relative_to_pass1417_C2_C4_frontier"] for r in new.values()),
        "new_orbit_mass_71280": added_orbit_mass == 71280,
        "extended_cover_lower_bound_298080": extended_bound == 298080,
    }
    checks = {k: bool(v) for k, v in checks.items()}

    payload = {
        "schema": "w33.pass1421_1424.outer_integral_cover_extension.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "passes": {
            "1421": {
                "title": "Full-Weyl frame/signed-turn bridge theorem",
                "result": "The explicit 15-dimensional bridge intertwines the outer symplectic similitude as well as PSp(4,3), hence is PGSp(4,3) ~= W(E6)-equivariant.",
                "group_order": 51840,
                "outer_involution_trace": 3,
            },
            "1422": {
                "title": "Weyl character fingerprint theorem",
                "full_character_value_distribution": {str(k): v for k, v in sorted(full_distribution.items())},
                "outer_coset_character_value_distribution": {str(k): v for k, v in sorted(outer_distribution.items())},
                "character_mismatches": mismatches,
            },
            "1423": {
                "title": "Integral bridge Smith obstruction theorem",
                "smith_invariant_census": {str(k): v for k, v in sorted(smith_census.items())},
                "saturation_index": saturation_index,
                "finite_cokernel": "Z/2 (+) (Z/3)^5",
                "boundary": "The bridge is a rational and full-Weyl module isomorphism, but not an isomorphism of the natural integral lattices.",
            },
            "1424": {
                "title": "Exact-cover orbit lower-bound extension",
                "prior_certified_lower_bound": prior_bound,
                "new_distinct_orbits": len(new),
                "added_orbit_mass": added_orbit_mass,
                "extended_certified_lower_bound": extended_bound,
                "sample_records": sample_records,
                "boundary": "The exact total and complete orbit census remain open.",
            },
        },
        "checks": checks,
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["certificate_sha256"] = hashlib.sha256(canonical.encode()).hexdigest()
    return payload


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, default=OUT)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    payload = certificate()
    text = json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text() != text:
            raise SystemExit("Passes 1421-1424 certificate drift")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({
        "status": payload["status"],
        "checks": sum(payload["checks"].values()),
        "total": len(payload["checks"]),
        "full_weyl_order": payload["passes"]["1421"]["group_order"],
        "smith_index": payload["passes"]["1423"]["saturation_index"],
        "cover_lower_bound": payload["passes"]["1424"]["extended_certified_lower_bound"],
        "certificate_sha256": payload["certificate_sha256"],
    }, sort_keys=True))
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
