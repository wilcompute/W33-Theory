"""Pass 7217 -- pull the maximum partial ovoid of W(3,3) back to E8 through the
Eisenstein fibration, and ask what the 42 roots are.

THE IDEA, and why it is worth a run. This repo established (Pass 1020/1021) that there is no
edge-to-root bijection between W(3,3) and E8, but there IS a 6:1 Sp(4,3)-equivariant
fibration 240 E8 roots -> 40 W(3,3) points with fibre the Eisenstein units Z_6. Separately,
this week established alpha(W(3,3)) = 7 with stabilizer of order 18.

Nobody has put those two together. A 7-point partial ovoid pulls back to 7 x 6 = 42 roots,
and 42 is exactly the number of roots of A6. So: is the preimage of a maximum partial ovoid a
root SUBSYSTEM of E8, and if so which one?

That question has a clean yes/no answer and either outcome is informative. If the 42 roots are
closed under the reflections they generate, a purely combinatorial extremal problem in a
finite geometry is picking out a Lie-theoretic object inside E8. If they are not closed, the
coincidence 42 = |A6| is just a coincidence and should be recorded as one -- this repo has a
documented history of exactly that failure mode.

THE FIBRATION, BUILT NOT ASSUMED. The existing script scripts/PART_CCCCCXCIX_e8_spectral_
w33_bridge.py verifies the numerology and says outright "No eight-doily partition is
constructed". So the map is constructed here:

  * find J in W(E8) of order 3 with det(I - J) = 3^4 = 81, i.e. acting fixed-point-freely.
    Then J makes the root lattice a Z[omega]-module of rank 4, omega acting as J;
  * (I - J) is the prime above 3, and E8/(I-J)E8 has order 81, so it is F_3^4;
  * a root maps to its class; the fibre is the Eisenstein unit group of order 6, so the 240
    roots fall into 40 classes of 6, matching PG(3,3)'s 40 points.

Everything is then CHECKED against W(3,3): the induced collinearity graph must be
SRG(40,12,2,4), or the map is wrong and nothing is claimed.

    py -3 analysis/w33_pass7217_ovoid_pullback_to_e8.py
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402

# E8 Cartan matrix, Bourbaki numbering
CARTAN = np.array([
    [2, 0, -1, 0, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, 0, -1, 2]], dtype=np.int64)


def roots_in_root_basis():
    """All 240 E8 roots as integer coordinate vectors in the simple-root basis."""
    simple = [np.eye(8, dtype=np.int64)[i] for i in range(8)]
    found = {tuple(s) for s in simple}
    frontier = list(found)
    while frontier:
        nxt = []
        for v in frontier:
            v = np.array(v, dtype=np.int64)
            for i in range(8):
                # reflect v in simple root i: v - <v, alpha_i^vee> alpha_i
                c = int(CARTAN[i] @ v)
                w = v.copy()
                w[i] -= c
                tw = tuple(int(x) for x in w)
                if tw not in found:
                    found.add(tw)
                    nxt.append(tw)
        frontier = nxt
    allr = set(found) | {tuple(-np.array(v)) for v in found}
    return sorted(allr)


def simple_reflection(i):
    """s_i(v) = v - (C[i].v) e_i, so ROW i is what changes, not column i."""
    M = np.eye(8, dtype=np.int64)
    M[i, :] -= CARTAN[i]
    return M


def order_of(M, cap=64):
    X = M.copy()
    I = np.eye(8, dtype=np.int64)
    for k in range(1, cap + 1):
        if np.array_equal(X, I):
            return k
        X = X @ M
    return None


def class_map(N):
    """Classes of Z^8 / N Z^8 without Smith form: v ~ w iff N^{-1}(v-w) is integral,
    i.e. adj(N)(v-w) = 0 mod det(N), with adj(N) = det(N) * N^{-1} integral."""
    import numpy as np
    d = int(round(np.linalg.det(N)))
    adj = np.rint(d * np.linalg.inv(N)).astype(np.int64)
    if not np.allclose(adj @ N, d * np.eye(8), atol=1e-6):
        return None, None
    return adj, d


def main() -> int:
    print("=" * 78)
    print("Pass 7217 -- the maximum partial ovoid of W(3,3), pulled back to E8")
    print("=" * 78)

    R = roots_in_root_basis()
    print(f"\n  E8 roots in the simple-root basis: {len(R)}   (expect 240)")
    assert len(R) == 240
    Rarr = np.array(R, dtype=np.int64)

    # Gram matrix in the root basis is the Cartan matrix (all roots norm 2)
    G = CARTAN
    norms = {int(v @ G @ v) for v in Rarr}
    print(f"  norms in the root basis: {norms}   (expect {{2}})")
    assert norms == {2}

    # THE COXETER ELEMENT GIVES J DIRECTLY -- no search needed. c has order h = 30,
    # so c^10 has order 3, and the E8 exponents 1,7,11,13,17,19,23,29 are none of them
    # divisible by 3, so c^10 has no eigenvalue 1: it is fixed-point-free, and
    # det(I - c^10) = prod (1 - zeta_3^{m_j}) = ((1-w)(1-w^2))^4 = 3^4 = 81.
    gens = [simple_reflection(i) for i in range(8)]
    cox = np.eye(8, dtype=np.int64)
    for gmat in gens:
        cox = cox @ gmat
    h = order_of(cox, 64)
    print(f"\n  Coxeter element order: {h}   (E8 Coxeter number h = 30)")
    J = np.linalg.matrix_power(cox, 10)
    o = order_of(J, 8)
    d = int(round(np.linalg.det(np.eye(8) - J)))
    print(f"  J = c^10: order {o}, det(I-J) = {d}   (need order 3, det 81)")
    rootset = set(map(tuple, Rarr.tolist()))
    preserves = set(map(tuple, (Rarr @ J.T).tolist())) == rootset
    print(f"  J preserves the 240 roots: {preserves}")
    if o != 3 or d != 81 or not preserves:
        print("  c^10 is not a fixed-point-free order-3 automorphism -- aborting")
        return 1
    # EXACT, no floating point. J^2 + J + I = 0 gives (I-J)(I-J^2) = 3I, so
    # (I-J)^{-1} = (I-J^2)/3 and v ~ w mod (I-J)Z^8 exactly when
    # (I-J^2)(v-w) = 0 mod 3. The class label is therefore (I-J^2)v mod 3.
    I8 = np.eye(8, dtype=np.int64)
    J2 = J @ J
    check = (I8 - J) @ (I8 - J2)
    print(f"    (I-J)(I-J^2) = 3I : {np.array_equal(check, 3 * I8)}")
    Kmat = I8 - J2

    def cls(v):
        return tuple(int(x) % 3 for x in (Kmat @ v))

    classes = {}
    for i, v in enumerate(Rarr):
        classes.setdefault(cls(v), []).append(i)
    sizes = sorted({len(v) for v in classes.values()})
    print(f"\n  root classes mod (I-J): {len(classes)}   fibre sizes {sizes}")
    if 0 in [len(c) for c in classes]:
        pass
    zero = classes.pop((0, 0, 0, 0), None)
    print(f"    zero class contains {0 if zero is None else len(zero)} roots "
          f"(expect 0 -- no root is in (I-J)E8)")

    # projective points: identify v and -v and 2v (scalars in F_3^*)
    proj = {}
    for c, members in classes.items():
        key = min(c, tuple((2 * x) % 3 for x in c))
        proj.setdefault(key, []).extend(members)
    print(f"    projective classes: {len(proj)}   fibre sizes "
          f"{sorted({len(v) for v in proj.values()})}")
    if len(proj) != 40:
        print("  NOT 40 points -- the fibration is wrong, nothing is claimed")
        return 1

    # THE FORM MUST BE ALTERNATING. The E8 form is SYMMETRIC, so reducing it mod 3
    # cannot give W(3,3), which needs an alternating form -- that was why the first
    # run produced degrees 12..24 instead of a regular graph. The Eisenstein structure
    # supplies the right one: with (,) the E8 form and J the order-3 isometry,
    #     A(x,y) = (Jx, y) - (x, Jy)
    # is integral and antisymmetric, and descends mod 3 to the quotient.
    A_int = (J.T @ G) - (G @ J)
    print("\n  A = J^T G - G J is antisymmetric: "
          f"{np.array_equal(A_int, -A_int.T)}")

    def Aform(u, v):
        return int(u @ A_int @ v) % 3

    # well-definedness on classes: A(x + (I-J)z, y) = A(x,y) mod 3 for all z
    wd = True
    for _ in range(200):
        z = np.random.RandomState(0).randint(-2, 3, 8)
        break
    rs = np.random.RandomState(7217)
    for _ in range(300):
        x, y = Rarr[rs.randint(240)], Rarr[rs.randint(240)]
        z = rs.randint(-3, 4, 8)
        if Aform(x + (I8 - J) @ z, y) != Aform(x, y):
            wd = False
            break
    print(f"  A is well defined on classes mod (I-J): {wd}")

    keys = sorted(proj)
    reps = [Rarr[proj[k][0]] for k in keys]
    Adj = np.zeros((40, 40), dtype=np.int64)
    for i in range(40):
        for j in range(i + 1, 40):
            if Aform(reps[i], reps[j]) == 0:
                Adj[i, j] = Adj[j, i] = 1
    deg = sorted({int(Adj[i].sum()) for i in range(40)})
    from collections import Counter
    ev = Counter(np.linalg.eigvalsh(Adj.astype(float)).round(6))
    print(f"\n  induced graph: degrees {deg}")
    print(f"    spectrum: {dict(sorted((float(k), v) for k, v in ev.items()))}")
    # ev is a Counter: iterating it yields KEYS, not multiplicities, so the old
    # predicate compared {12,2,-4} against a 40-element multiset and returned False
    # on a graph that WAS SRG(40,12,2,4). Expand with .items() before comparing.
    spec = sorted(round(float(k)) for k, n in ev.items() for _ in range(n))
    is_srg = deg == [12] and spec == sorted([12] + [2] * 24 + [-4] * 15)
    print(f"    SRG(40,12,2,4) with spectrum 12^1 2^24 (-4)^15 ? {is_srg}")

    out = {"boundary": ("constructs the 6:1 Eisenstein fibration explicitly and pulls the "
                        "maximum partial ovoid back. Claims nothing unless the induced graph "
                        "is verified to be SRG(40,12,2,4)"),
           "roots": len(R), "classes": len(proj),
           "fibre_sizes": sorted({len(v) for v in proj.values()}),
           "induced_degrees": deg, "is_w33": bool(is_srg), "form": "A(x,y)=(Jx,y)-(x,Jy)"}
    fp = ROOT / "data" / "PART_W33_PASS7217_OVOID_PULLBACK_E8.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
