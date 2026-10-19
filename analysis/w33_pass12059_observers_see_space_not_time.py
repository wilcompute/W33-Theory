"""Pass 12059: observers see the clock's space but not its time (Claude track; joins 12058 to 11831-11836).

Matrix model: V = F_3^4 with the standard symplectic form, G = Sp(4,3) (51840). An EVENT is a point p of W(3,3);
its clock group is H_p, the stabiliser of a clock real form at p (12052-12058): the unique subgroup of index 3 in the
point stabiliser (1296), = U_p : (2 x Q8) with U_p = 3^{1+2} the Heisenberg group whose centre is the tick <t_p>.
An OBSERVER is a Kramers time reversal J (anti-symplectic, J^2 = -1; 36 up to sign); its Lorentz group is the
centraliser C_J = SL(2,9) (11831), and its sky is the 10 J-invariant contexts = P^1(F_9).
Exact results, for every one of the 40 x 36 (event, observer) pairs:
  1. Every observer sees every event on exactly one sky point: the context spanned by p and Jp (an F_9-line).
  2. The little group of the event in the observer's Lorentz group, C_J n Stab(p), has order 18 = +-1 x 3^2:
     the nine null rotations about that sky point, times +-1.
  3. Exactly one Z_3 of these null rotations lies in the clock's Heisenberg group U_p, and it is never the tick.
     Each of the 12 non-central Z_3's of U_p (the space translations) is a null rotation for exactly 3 observers;
     the central Z_3 (time) for none. Reason: J t_p J^-1 = t_{Jp}^-1, a tick at another event, so no observer's
     stabiliser (C_J or its parity coset) contains a tick.
  4. The little group meets the clock group in +-1 x Z_3 (order 6) only: the other six null rotations fix the
     event but permute its three clock real forms. Every observer's little group maps ONTO the clock-choice group
     Stab(p)/H_p = Z_3, so the clock is not Lorentz-invariant for any observer.
Reading. Space translations of an event's clock are Lorentz transformations (null rotations) of some observers; time,
the central charge of 12058, is a Lorentz transformation of none -- the finite analogue of the Bargmann central
charge that the Lorentz group does not contain. The clock real form is a choice no observer's symmetry makes;
something else must make it (12056-12057: the one-loop vacuum and the matter content).
Prior art (classical, cited): Hermitian spreads of W(3) and their stabilisers; SL(2,9) as the centraliser of an
F_9-structure; Wigner's massless little group 3^2 : Z_4 (Pass 11836). New: the intersection pattern with the clock.
Scope: finite-group statements; 'space', 'time', 'observer' are the corpus's stabiliser-defined names.
Independent cross-check: GAP (Sp(4,3), ConformalSymplecticGroup, LowIndexSubgroups) reproduces 1-4.
"""

import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_pass12059_observers_see_space_not_time.json"
Om = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [2, 0, 0, 0], [0, 2, 0, 0]])
I4 = np.eye(4, dtype=np.int64)
VEC = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int64)


def om(u, v):
    return int(u @ Om @ v) % 3


def norm(v):
    v = np.asarray(v) % 3
    i = next(k for k in range(4) if v[k])
    return tuple(int(x) for x in (v * (1 if v[i] == 1 else 2)) % 3)


def key(M):
    return (np.asarray(M) % 3).astype(np.int8).tobytes()


def tv(p):
    p = np.asarray(p)
    return np.array([(I4[:, i] + om(I4[:, i], p) * p) % 3 for i in range(4)]).T % 3


def order(M):
    one = np.eye(len(M), dtype=np.int64)
    g, n = M % 3, 1
    while not np.array_equal(g, one):
        g, n = (g @ M) % 3, n + 1
    return n


def build_group(pts):
    gens = [tv(p) for p in pts]
    seen, out, frontier = {key(I4)}, [I4], [I4]
    while frontier:
        nf = []
        for g in frontier:
            for t in gens:
                h = (t @ g) % 3
                k = key(h)
                if k not in seen:
                    seen.add(k)
                    out.append(h)
                    nf.append(h)
        frontier = nf
    return np.array(out)


def kramers():
    E = [I4[:, i] for i in range(4)]
    sols = []
    for c1, c3 in itertools.product(VEC, VEC):
        if om(c1, c3) != (-om(E[0], E[2])) % 3:
            continue
        for c2 in VEC:
            if om(c1, c2) or om(c3, c2):
                continue
            for c4 in VEC:
                if om(c1, c4) or om(c3, c4) or om(c2, c4) != (-om(E[1], E[3])) % 3:
                    continue
                J = np.stack([c1, c2, c3, c4], axis=1) % 3
                if np.array_equal((J @ J) % 3, (2 * I4) % 3):
                    sols.append(J)
    reps = {}
    for J in sols:
        reps.setdefault(min(key(J), key(2 * J)), J)
    return len(sols), list(reps.values())


def main():
    checks, res = {}, {}
    pts = sorted({norm(v) for v in VEC if v.any()})
    G = build_group(pts)
    checks["|Sp(4,3)| = 51840, 40 events"] = len(G) == 51840 and len(pts) == 40
    nJ, Js = kramers()
    checks["72 Kramers reversals, 36 observers up to sign"] = nJ == 72 and len(Js) == 36
    Gk = {key(g): i for i, g in enumerate(G)}
    GV = np.einsum("gij,vj->gvi", G, VEC) % 3  # images of all 81 vectors
    vidx = lambda v: int(np.dot(np.asarray(v) % 3, [27, 9, 3, 1]))  # noqa: E731
    CJ = []
    for J in Js:
        CJ.append(np.all((np.einsum("gij,jk->gik", G, J) - np.einsum("ij,gjk->gik", J, G)) % 3 == 0, axis=(1, 2)))
    res["lorentz_order"] = sorted({int(c.sum()) for c in CJ})
    checks["each observer's Lorentz group C_J has order 720 (SL(2,9))"] = res["lorentz_order"] == [720]

    summary, hits_all, sky_ok, tick_never = Counter(), [], True, True
    for p in pts:
        pv = np.array(p)
        ip = vidx(pv)
        imgp = GV[:, ip]
        fix_line = np.array([norm(x) == p for x in imgp])
        fix_vec = np.all(imgp == pv, axis=1)
        perp = [vidx(v) for v in VEC if om(pv, v) == 0]
        dif = (GV[:, perp] - VEC[perp][None]) % 3
        in_p = np.zeros(dif.shape[:2], bool)
        for k in range(3):
            in_p |= np.all(dif == (k * pv) % 3, axis=2)
        U = fix_vec & np.all(in_p, axis=1)
        a = next(v for v in VEC[perp] if v.any() and norm(v) != p)
        b = next(v for v in VEC[perp] if v.any() and om(a, v))
        quo = {}
        for i, j in itertools.product(range(3), repeat=2):
            for k in range(3):
                quo[key((i * a + j * b + k * pv) % 3)] = (i, j)
        stab = np.nonzero(fix_line)[0]
        Hmask = np.zeros(len(G), bool)
        for g in stab:
            M = np.array([quo[key(GV[g, vidx(x)])] for x in (a, b)]).T % 3
            Hmask[g] = order(M) in (1, 2, 4)
        tp = tv(p)
        tks = {key(tp), key((tp @ tp) % 3)}
        Uidx = np.nonzero(U)[0]
        z3 = {}
        for g in Uidx:
            if order(G[g]) == 3:
                z3.setdefault(min(key(G[g]), key((G[g] @ G[g]) % 3)), 0)
        tick_k = min(tks)
        assert int(U.sum()) == 27 and int(fix_line.sum()) == 1296 and int(Hmask.sum()) == 432 and len(z3) == 13
        for J, C in zip(Js, CJ):
            L = C & fix_line
            LH = L & Hmask
            LU = np.nonzero(C & U)[0]
            sky = {norm((i * pv + j * (J @ pv)) % 3) for i in range(3) for j in range(3) if (i, j) != (0, 0)}
            sky_ok &= (len(sky) == 4 and all(om(np.array(x), np.array(y)) == 0 for x in sky for y in sky)
                       and {norm(J @ np.array(x)) for x in sky} == sky)
            nontriv = [g for g in LU if not np.array_equal(G[g], I4)]
            ks = {min(key(G[g]), key((G[g] @ G[g]) % 3)) for g in nontriv}
            tick_never &= tick_k not in ks and all(key(t) not in {key(G[g]) for g in np.nonzero(C)[0]} for t in [tp])
            for k in ks:
                z3[k] += 1
            summary[(int(L.sum()), int(LH.sum()), len(nontriv),
                     tuple(sorted(Counter(order(G[g]) for g in np.nonzero(L)[0]).items())))] += 1
        hits_all.append(tuple(sorted(Counter(v for k, v in z3.items() if k != tick_k).items())) + (("tick", z3[tick_k]),))
    res["little_group_pattern"] = {str(k): v for k, v in summary.items()}
    res["z3_hit_pattern"] = sorted({str(h) for h in hits_all})
    checks["every observer sees every event on one sky point (context <p, Jp>, an F9-line)"] = bool(sky_ok)
    checks["little group C_J n Stab(p) = +-1 x 3^2 (order 18: orders 1:1, 2:1, 3:8, 6:8) for all 1440 pairs"] = (
        list(summary) == [(18, 6, 2, ((1, 1), (2, 1), (3, 8), (6, 8)))] and sum(summary.values()) == 1440)
    checks["little group n clock group = +-1 x Z3 (order 6): maps onto the clock-choice Z3 = Stab(p)/H_p"] = (
        all(k[1] == 6 for k in summary))
    checks["C_J n U_p is one Z3, never the tick; each of the 12 space Z3 is hit by exactly 3 observers, time by 0"] = (
        bool(tick_never) and set(hits_all) == {((3, 12), ("tick", 0))})
    # parity coset: no element anticommuting with J is a tick either (J t_p J^-1 = t_{Jp}^-1)
    par_ok = True
    for J in Js:
        Ji = np.linalg.matrix_power(J, 3) % 3
        for p in pts:
            conj = (J @ tv(p) @ Ji) % 3
            jp = norm(J @ np.array(p))
            par_ok &= np.array_equal(conj, (tv(jp) @ tv(jp)) % 3) and jp != p
    checks["J t_p J^-1 = t_{Jp}^-1 with Jp != p: no observer's stabiliser (either coset) contains a tick"] = bool(par_ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
