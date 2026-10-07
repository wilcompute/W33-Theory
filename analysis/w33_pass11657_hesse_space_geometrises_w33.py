"""Pass 11657: the two-qutrit Hesse space geometrises W(3,3) and its 45 factorisations.

In the 5-dim space of Heisenberg-invariant cubics (Pass 11651; projectively P^4, symmetry G33):
  * LINES of W(3,3) = the 40 stabiliser bases (Lagrangian planes) -> 40 POINTS of P^4 (Pass 11651; Q(4,3) graph).
  * POINTS of W(3,3) = the 40 transvection ticks T_p -> the Weil gate of T_p acts with eigenvalue multiplicities (2, 3):
    40 projective LINES (2-dim eigenspaces) and 40 PLANES (3-dim eigenspaces).  Two tick-lines meet iff p, q are
    collinear in W(3,3); two tick-planes meet in a line iff collinear, else in a point.  So the W33 POINT graph (the
    regular SRG(40,12,2,4)) is the meeting graph of the tick-lines.
  * INCIDENCE: the stabiliser point u_L lies on the tick-line of p iff p lies on L -- 160/160, no false incidences.
    Each tick-line carries the 4 stabiliser points of the Lagrangians through p: a copy of the one-qutrit Hesse sphere
    (p^perp / p is a one-qutrit phase space).
  * FACTORISATIONS: for each of the 90 non-degenerate (hyperbolic) planes P of F3^4, the symplectic involution
    sigma_P = -1 on P, +1 on P^perp (a local parity of the tensor factorisation P + P^perp) acts on the Hesse space as a
    REFLECTION, and sigma_P, sigma_(P^perp) give the same mirror: 45 mirrors = the 45 tensor factorisations of two
    qutrits = the 45 reflections of G33.  SWAP is sigma_P for the antidiagonal plane (the factorisation diagonal +
    antidiagonal), and the local parity of qutrit 2 is sigma_P for P = qutrit 2.
  * The orthogonality graph of the 45 mirrors is SRG(45, 12, 3, 3), the collinearity graph of GQ(4,2): two mirrors are
    orthogonal iff the two factorisations' octets are disjoint -- exactly Pass 11177's collinearity (perfect gates).
    (Commuting of the two involutions is NOT the criterion: it agrees on 1440 of 1980 ordered pairs only.)
  * BURKHARDT: the unique G33-invariant quartic I4 vanishes identically on all 40 tick-planes -- they are the 40 planes
    (j-planes) of the Burkhardt quartic -- and I4 and its gradient vanish at all 45 mirror roots -- they are its 45
    nodes.  So: W(3,3) points (ticks) = j-planes, tensor factorisations = nodes, stabiliser bases = 40 points (off the
    quartic).
Classical background: G33 is the Burkhardt group (45 nodes, 40 j-planes); PSp(4,3) = PSU(4,2), GQ(4,2) = H(3,4).
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass11350_linear_decider as L  # noqa: E402
import w33_pass11651_n_qutrit_hesse_space as H  # noqa: E402

OUT = ROOT / "data" / "w33_pass11657_hesse_space_geometrises_w33.json"


def eigspaces(Rm):
    ev, V = np.linalg.eig(Rm)
    groups = {}
    for i, e in enumerate(ev):
        key = next((k for k in groups if abs(k - e) < 1e-6), e)
        groups.setdefault(key, []).append(i)
    return {len(ids): np.linalg.qr(V[:, ids])[0] for ids in groups.values()}


def inter_dim(A, Bm):
    s = np.linalg.svd(A.conj().T @ Bm, compute_uv=False)
    return int((s > 1 - 1e-8).sum())


def reflection_root(Rm):
    """if some scalar multiple of Rm is a reflection, return its root"""
    for e in np.linalg.eigvals(Rm):
        Mm = Rm / e
        ev = np.linalg.eigvals(Mm)
        if int(np.sum(np.abs(ev - 1) > 1e-6)) == 1:
            ev2, V2 = np.linalg.eig(Mm)
            j = int(np.argmax(np.abs(ev2 - 1)))
            return V2[:, j] / np.linalg.norm(V2[:, j])
    return None


def srg_params(A):
    n = len(A)
    lam = {int((A[i] & A[j]).sum()) for i in range(n) for j in range(n) if i != j and A[i, j]}
    mu = {int((A[i] & A[j]).sum()) for i in range(n) for j in range(n) if i != j and not A[i, j]}
    return dict(n=n, k=sorted(set(A.sum(1).tolist())), lam=sorted(lam), mu=sorted(mu))


def main():
    d, pts, idx, B, wg = H.setup(2)
    D = L.Decider(2)
    Om = D.wl.Om
    I4 = np.eye(4, dtype=np.int64)
    R = lambda U: H.R_of(B, U)  # noqa: E731
    res = dict(pass_id=11657)
    P40 = [v for v in itertools.product(range(3), repeat=4) if any(v) and next(x for x in v if x) == 1]
    E2, E3, mult = [], [], Counter()
    for p in P40:
        p = np.array(p)
        Tp = (I4 + np.outer(p, p @ Om)) % 3
        assert D.is_symplectic(Tp)
        es = eigspaces(R(D.weil(Tp)))
        mult[tuple(sorted(es))] += 1
        E2.append(es[2])
        E3.append(es[3])
    res["tick_eigenspace_dimensions"] = {str(k): v for k, v in mult.items()}
    coll = lambda i, j: (np.array(P40[i]) @ Om @ np.array(P40[j])) % 3 == 0  # noqa: E731
    c2 = Counter((inter_dim(E2[i], E2[j]), bool(coll(i, j))) for i in range(40) for j in range(40) if i != j)
    c3 = Counter((inter_dim(E3[i], E3[j]), bool(coll(i, j))) for i in range(40) for j in range(40) if i != j)
    res["tick_lines_meet_iff_collinear"] = {str(k): v for k, v in c2.items()}
    res["tick_planes_meet_in_line_iff_collinear"] = {str(k): v for k, v in c3.items()}
    A_pts = np.array([[i != j and inter_dim(E2[i], E2[j]) > 0 for j in range(40)] for i in range(40)])
    res["tick_line_meeting_graph"] = srg_params(A_pts)
    lag, bases = H.stabiliser_bases(2)
    U40 = []
    for V in bases:
        u = B.T @ np.kron(np.kron(V[:, 0], V[:, 0]), V[:, 0])
        U40.append(u / np.linalg.norm(u))
    inc = Counter()
    for a, Lg in enumerate(lag):
        for i, p in enumerate(P40):
            on = tuple(p) in Lg
            in2 = np.linalg.norm(E2[i].conj().T @ U40[a]) > 1 - 1e-8
            inc[(on, bool(in2))] += 1
    res["incidence_(p on L, u_L on tick-line of p)"] = {str(k): v for k, v in inc.items()}
    # factorisations: involutions -1 on a hyperbolic plane P
    vecs = [np.array(v) for v in itertools.product(range(3), repeat=4) if any(v)]
    planes = set()
    for u in vecs:
        for v in vecs:
            if (u @ Om @ v) % 3:
                planes.add(frozenset(tuple((a * u + b * v) % 3) for a in range(3) for b in range(3)))
    planes = list(planes)
    roots, pmap = [], {}
    for P in planes:
        Pb = [np.array(x) for x in P if any(x)]
        b1 = Pb[0]
        b2 = next(x for x in Pb if (b1 @ Om @ x) % 3)
        perp = [x for x in vecs if (x @ Om @ b1) % 3 == 0 and (x @ Om @ b2) % 3 == 0]
        c1 = perp[0]
        c2 = next(x for x in perp if (c1 @ Om @ x) % 3)
        Bas = np.stack([b1, b2, c1, c2], 1)
        Binv = L.R._inv_mod3(Bas % 3) % 3
        sig = (Bas @ np.diag([2, 2, 1, 1]) @ Binv) % 3
        assert D.is_symplectic(sig) and not ((sig @ sig - I4) % 3).any()
        r = reflection_root(R(D.weil(sig)))
        assert r is not None
        k = next((i for i, q in enumerate(roots) if abs(abs(np.vdot(r, q)) - 1) < 1e-8), None)
        if k is None:
            roots.append(r)
            k = len(roots) - 1
        pmap.setdefault(k, []).append(P)
    res["hyperbolic_planes"] = len(planes)
    res["distinct_mirrors"] = len(roots)
    res["each_mirror_from_P_and_P_perp"] = all(
        len(v) == 2 and all((np.array(x) @ Om @ np.array(y)) % 3 == 0 for x in v[0] for y in v[1]) for v in pmap.values())
    Rt = np.array(roots)
    Gm = np.abs(Rt.conj() @ Rt.T) ** 2
    res["mirror_overlaps"] = sorted(set(np.round(Gm[~np.eye(len(roots), dtype=bool)], 8).tolist()))
    A_orth = (Gm < 1e-8) & ~np.eye(len(roots), dtype=bool)
    res["mirror_orthogonality_graph"] = srg_params(A_orth)
    # Pass 11177: factorisations are collinear in GQ(4,2) iff their octets (8 projective points of P u P^perp) are
    # disjoint.  Compare with mirror orthogonality and with commuting involutions.
    def proj(x):
        x = np.array(x) % 3
        lead = next(v for v in x if v)
        return tuple((x * lead) % 3)                          # normalise leading entry to 1 (lead^-1 = lead mod 3)
    octet = {k: {proj(x) for P in v for x in P if any(x)} for k, v in pmap.items()}
    sigs = {}
    for k, v in pmap.items():
        P = v[0]
        Pb = [np.array(x) for x in P if any(x)]
        b1 = Pb[0]
        b2 = next(x for x in Pb if (b1 @ Om @ x) % 3)
        perp = [x for x in vecs if (x @ Om @ b1) % 3 == 0 and (x @ Om @ b2) % 3 == 0]
        c1 = perp[0]
        c2 = next(x for x in perp if (c1 @ Om @ x) % 3)
        Bas = np.stack([b1, b2, c1, c2], 1)
        sigs[k] = (Bas @ np.diag([2, 2, 1, 1]) @ (L.R._inv_mod3(Bas % 3) % 3)) % 3
    agree_oct = agree_comm = 0
    for i in range(len(roots)):
        for j in range(len(roots)):
            if i == j:
                continue
            orth = bool(A_orth[i, j])
            agree_oct += orth == (len(octet[i] & octet[j]) == 0)
            agree_comm += orth == (not ((sigs[i] @ sigs[j] - sigs[j] @ sigs[i]) % 3).any())
    res["octet_sizes"] = sorted({len(o) for o in octet.values()})
    res["orthogonal_iff_octets_disjoint_(Pass_11177_GQ42)"] = f"{agree_oct}/{len(roots) * (len(roots) - 1)}"
    res["orthogonal_iff_involutions_commute"] = f"{agree_comm}/{len(roots) * (len(roots) - 1)}"
    # SWAP and local parity
    SW = np.zeros((9, 9))
    for a in pts:
        SW[idx[(a[1], a[0])], idx[a]] = 1
    par2 = np.zeros((9, 9))
    for a in pts:
        par2[idx[(a[0], (-a[1]) % 3)], idx[a]] = 1
    for name, U in (("SWAP", SW), ("parity of qutrit 2", par2)):
        r = reflection_root(R(U))
        res[f"{name}_is_a_reflection"] = r is not None
        res[f"{name}_mirror_among_the_45"] = r is not None and any(abs(abs(np.vdot(r, q)) - 1) < 1e-8 for q in roots)
    # Burkhardt: the unique degree-4 invariant I4 vanishes on every tick-plane (40 j-planes) and is singular at every
    # mirror root (45 nodes)
    Gfull = np.array(H.closure([R(g) for g in wg.values()]))
    rng = np.random.default_rng(3)
    lv = rng.normal(size=5) + 1j * rng.normal(size=5)
    I4 = lambda v: np.mean(((Gfull @ v) @ lv) ** 4)  # noqa: E731

    def grad(v, h=1e-6):
        return np.array([(I4(v + h * e) - I4(v - h * e)) / (2 * h) for e in np.eye(5)])
    x = rng.normal(size=5) + 1j * rng.normal(size=5)
    x /= np.linalg.norm(x)
    sc, gsc = abs(I4(x)), np.linalg.norm(grad(x))
    mp = 0.0
    for Ep in E3:
        for _ in range(3):
            v = Ep @ (rng.normal(size=3) + 1j * rng.normal(size=3))
            mp = max(mp, abs(I4(v / np.linalg.norm(v))) / sc)
    res["Burkhardt_I4_on_tick_planes_rel_max"] = float(mp)
    res["Burkhardt_I4_at_mirror_roots_rel_max"] = float(max(abs(I4(r)) for r in roots) / sc)
    res["Burkhardt_gradI4_at_mirror_roots_rel_max"] = float(max(np.linalg.norm(grad(r)) for r in roots) / gsc)
    res["tick_planes_are_j_planes"] = bool(mp < 1e-10)
    res["mirror_roots_are_nodes"] = bool(res["Burkhardt_I4_at_mirror_roots_rel_max"] < 1e-10 and res["Burkhardt_gradI4_at_mirror_roots_rel_max"] < 1e-8)
    res["I4_at_stabiliser_points_rel"] = float(max(abs(I4(u)) for u in U40) / sc)
    print(res, flush=True)
    json.dump(res, open(OUT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
