"""Pass 7277 -- the Eisenstein fibration is one member of a TOWER. The Gaussian case gives W(3,2).

THE IDEA. Pass 7217 built W(3,3) from E8 using a fixed-point-free element J of ORDER 3: J
makes the root lattice a Z[omega]-module, and Z[omega]/(1-omega) = F_3, so the quotient is
F_3^4 and its 40 projective points are W(3,3). Nothing in that argument is special to 3.

An order-d fixed-point-free element makes E8 a module over Z[zeta_d], and the quotient by the
prime above the relevant rational prime is a small F_p-space. Running the possible d:

    d   element        det(I-M)   quotient   nonzero   roots per class
    2   c^15               256    F_2^8          255   240/255 < 1, no fibration
    3   c^10                81    F_3^4           80   3     -> 40 projective points
    4   (not a c power)     16    F_2^4           15   16    -> 15 projective points
    5   c^6                 25    F_5^2           24   10    -> 6 projective points

So d=3 gives 40 points and d=4 gives FIFTEEN -- and W(3,2) has exactly 15 points. If the
induced geometry is W(3,2), the fibration is not an Eisenstein accident; it is the d=3 member
of a family, and the smallest symplectic quadrangle sits inside E8 the same way.

d=4 IS NOT A POWER OF THE COXETER ELEMENT (4 does not divide h = 30), so it has to be found
by search: order 4, trace 0, det(I-M) = 2^4 = 16. Such an element satisfies M^2 = -I exactly,
which makes the alternating form immediate:

    A(x,y) = (Mx, y)     is antisymmetric, because (Mx,y) = (M^2 x, My) = -(x, My)

-- cleaner than the order-3 case, where A(x,y) = (Jx,y) - (x,Jy) had to be antisymmetrised
by hand.

VERIFIED, NOT ASSUMED: the induced graph must be the W(3,2) collinearity graph SRG(15,6,1,3),
or nothing is claimed.

    py -3 analysis/w33_pass7277_the_gaussian_fibration.py
"""

from __future__ import annotations

import itertools
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import (  # noqa: E402
    CARTAN, roots_in_root_basis, simple_reflection, order_of,
)


def find_order4(Rarr, gens, I8, seed=4):
    rng = random.Random(seed)
    rootset = set(map(tuple, Rarr.tolist()))
    for _ in range(400000):
        M = I8.copy()
        for _ in range(rng.randrange(2, 16)):
            M = M @ gens[rng.randrange(8)]
        o = order_of(M, 40)
        if o is None or o % 4:
            continue
        Mc = np.linalg.matrix_power(M, o // 4)
        if order_of(Mc, 6) != 4 or int(np.trace(Mc)) != 0:
            continue
        if not np.array_equal(Mc @ Mc, -I8):
            continue
        if int(round(np.linalg.det(np.eye(8) - Mc))) != 16:
            continue
        if set(map(tuple, (Rarr @ Mc.T).tolist())) == rootset:
            return Mc
    return None


def main() -> int:
    print("=" * 78)
    print("Pass 7277 -- the Gaussian fibration: E8 -> W(3,2)")
    print("=" * 78)

    R = roots_in_root_basis()
    Rarr = np.array(R, dtype=np.int64)
    G = CARTAN
    I8 = np.eye(8, dtype=np.int64)
    gens = [simple_reflection(i) for i in range(8)]

    M = find_order4(Rarr, gens, I8)
    if M is None:
        print("\n  no order-4 fixed-point-free element found -- aborting")
        return 1
    print(f"\n  order-4 element found: M^2 = -I, trace 0, det(I-M) = 16, preserves the roots")

    # class map. (I-M)(I+M)... for M^2=-I we have (I-M)(I-M) = I - 2M + M^2 = -2M,
    # so (I-M)^2 = -2M and the quotient by (I-M) is killed by 2: it IS an F_2 space.
    N = I8 - M
    sq = N @ N
    print(f"    (I-M)^2 = -2M ? {np.array_equal(sq, -2 * M)}   "
          f"-> the quotient is killed by 2, hence an F_2 space")

    # class of v: solve via the adjugate, exactly (det = 16)
    adj = np.rint(16 * np.linalg.inv(N.astype(float))).astype(np.int64)
    assert np.allclose(adj @ N, 16 * np.eye(8), atol=1e-6), "adjugate not integral"

    classes: dict[tuple, list[int]] = {}
    for i, v in enumerate(Rarr):
        classes.setdefault(tuple(int(x) % 16 for x in (adj @ v)), []).append(i)
    sizes = sorted({len(v) for v in classes.values()})
    print(f"\n  root classes mod (I-M): {len(classes)}   fibre sizes {sizes}")
    if len(classes) != 15 or sizes != [16]:
        print("  NOT 15 classes of 16 -- the fibration is wrong, nothing claimed")
        return 1
    print(f"    15 classes of exactly 16 roots  (F_2^4 has 15 nonzero vectors)")

    # alternating form A(x,y) = (Mx, y)
    # THE FORM. (Mx,y) is antisymmetric over Z, but in characteristic 2 that is not
    # enough -- it must also DESCEND to the quotient, and it does not: it gives
    # degrees 6,7,9,10. Testing candidates, the one that is well defined mod (I-M)
    # AND regular is A(x,y) = ((I+M)x, y), where (I+M) = 2(I-M)^{-1}.
    A_int = G + M.T @ G
    print("\n  A(x,y) = ((I+M)x, y) -- the form that DESCENDS mod (I-M).")
    print("    (Mx,y) alone is antisymmetric but NOT well defined on classes.")

    keys = sorted(classes)
    reps = [Rarr[classes[k][0]] for k in keys]
    Adj = np.zeros((15, 15), dtype=np.int64)
    for i in range(15):
        for j in range(i + 1, 15):
            if int(reps[i] @ A_int @ reps[j]) % 2 == 0:
                Adj[i, j] = Adj[j, i] = 1
    deg = sorted({int(Adj[i].sum()) for i in range(15)})
    ev = Counter(np.linalg.eigvalsh(Adj.astype(float)).round(6))
    print(f"  induced graph: degrees {deg}")
    print(f"    spectrum {dict(sorted((float(a), b) for a, b in ev.items()))}")
    # ev is a Counter: iterating it yields KEYS, not multiplicities. Expand it.
    spec = sorted(round(float(k)) for k, n in ev.items() for _ in range(n))
    is_w32 = deg == [6] and spec == sorted([6] + [1] * 9 + [-3] * 5)
    print(f"    W(3,2) collinearity graph SRG(15,6,1,3)? {is_w32}")

    verdict = ""
    if is_w32:
        # the analogue of the Pass 7219 theorem
        ok = True
        cols = Counter()
        for i in range(15):
            for j in range(i + 1, 15):
                ips = Counter(int(Rarr[a] @ G @ Rarr[b])
                              for a in classes[keys[i]] for b in classes[keys[j]])
                cols[(bool(Adj[i, j]), tuple(sorted(ips.items())))] += 1
        print(f"\n  inner-product distribution between two fibres (256 pairs each):")
        for (coll, sig), n in sorted(cols.items(), key=lambda kv: -kv[1]):
            lab = "COLLINEAR" if coll else "non-collinear"
            print(f"    {lab:14s} x{n:3d}  {dict(sig)}")
        verdict = ("the Gaussian order-4 fibration of E8 gives W(3,2), so the Eisenstein "
                   "case is the d=3 member of a family")
        print(f"\n  -> {verdict}")
    else:
        verdict = "the order-4 quotient does NOT give W(3,2); nothing claimed"
        print(f"\n  -> {verdict}")

    out = {"boundary": ("tests whether a fixed-point-free order-4 element of W(E8) yields "
                        "W(3,2) the way the order-3 one yields W(3,3). Claims nothing unless "
                        "the induced graph is verified to be SRG(15,6,1,3)"),
           "order4_element": {"M2_is_minus_I": True, "trace": 0, "det_I_minus_M": 16},
           "classes": len(classes), "fibre_sizes": sizes,
           "induced_degrees": deg, "is_W32": bool(is_w32), "verdict": verdict}
    fp = ROOT / "data" / "PART_W33_PASS7277_GAUSSIAN_FIBRATION.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
