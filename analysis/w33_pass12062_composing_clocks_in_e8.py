"""Pass 12062: composing clocks in E8 -- the real-form algebra of two times (Claude track; continues 12052-12056).

Inner involutions of E8 are theta_h, h in E8/2E8, and theta_h theta_h' = theta_{h+h'}: in the 12052 root model the
product's parity vector on the 240 roots is the XOR of the two. The 120 clock involutions (E8(-24), 3 at each of the
40 points) and the 135 split ones (E8(8), 3 at each of the 45 factorisations) are classified by their even root sets.
Exact composition table for clocks c at p and c' at q (all 120 x 120 ordered pairs):
  1. Same event: the three clocks at p and the identity form a Klein four-group, c1 c2 = c3. (The three clock
     choices of 12059-12060 multiply like the quaternion units i, j, k modulo sign.)
  2. Jointly measurable events (p, q collinear; their context is {p, q, r, s}): every product is a SPLIT involution;
     the 9 products are exactly the 9 split involutions of the 3 factorisations that contain r and s, with r and s in
     different hyperbolic lines. Two compatible times compose to a factorisation of the two-qutrit system.
  3. Non-collinear events (hyperbolic line {p, q, r, s}): 6 products are the clocks at r and s (all three at each),
     and 3 are the split involutions of the factorisation <p, q> + <p, q>^perp.
Reading. Real forms compose like a finite algebra of times. One event carries a Klein group of clocks; two
compatible clocks give a split (two-factor) real form, never a time; incompatible clocks give the times of the two
remaining events of their hyperbolic line, or the factorisation they span.
Scope: statements about inner involutions in the 12052 model; theta_h theta_h' = theta_{h+h'} is classical.
"""

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass12053_gate_sets_and_real_forms import setup  # noqa: E402

OUT = ROOT / "data" / "w33_pass12062_composing_clocks_in_e8.json"


def main():
    checks, res = {}, {}
    Adj, invs, tick, fib = setup()
    A = Adj.astype(bool)

    def even(s):
        return frozenset(x for x in range(40) if not s[fib[x]].any())

    def kind(s):
        return {240: "identity", 128: "clock", 112: "split"}.get(240 - int(s.sum()), "other")

    clocks = [s for k, s in invs if k == "clock"]
    splits = [s for k, s in invs if k == "split"]
    centre_of = {}
    cp = {}
    for s in clocks:
        ev = even(s)
        p = next(x for x in range(40) if frozenset(np.nonzero(A[x])[0]) == ev)
        centre_of[s.tobytes()] = p
        cp.setdefault(p, []).append(s)
    fac_of = {s.tobytes(): even(s) for s in splits}
    checks["120 clocks (3 per point), 135 splits (3 per factorisation of 8 points)"] = (
        len(clocks) == 120 and all(len(v) == 3 for v in cp.values()) and len(splits) == 135
        and Counter(Counter(fac_of.values()).values()) == Counter({3: 45}))

    def line_through(p, q):  # isotropic line: p, q and the two points collinear to both and to each other
        c = [z for z in range(40) if A[z, p] and A[z, q]]
        rs = [z for z in c if all(A[z, y] for y in c if y != z)]
        return rs

    def hyp_line(p, q):  # {p,q}^perp^perp
        perp = [z for z in range(40) if A[z, p] and A[z, q]]
        return [z for z in range(40) if z not in (p, q) and all(A[z, y] for y in perp)]

    def split_lines(f):  # the two hyperbolic lines of a factorisation (8 points, two mutually perp 4-sets)
        f = sorted(f)
        a = f[0]
        H1 = {a} | {z for z in f if z != a and not A[a, z]}
        return H1, set(f) - H1

    same_ok = col_ok = far_ok = True
    tally = Counter()
    for p in range(40):
        a, b, c = cp[p]
        same_ok &= {(a ^ b).tobytes(), (a ^ c).tobytes(), (b ^ c).tobytes()} == {c.tobytes(), b.tobytes(), a.tobytes()}
        for q in range(40):
            if q == p:
                continue
            prods = [x ^ y for x in cp[p] for y in cp[q]]
            kinds = Counter(kind(x) for x in prods)
            if A[p, q]:
                rs = line_through(p, q)
                facs = Counter(fac_of[x.tobytes()] for x in prods if kind(x) == "split")
                sep = all(len(rs) == 2 and any(rs[0] in H and rs[1] not in H for H in split_lines(f)) for f in facs)
                col_ok &= kinds == Counter(split=9) and len(facs) == 3 and set(facs.values()) == {3} and sep and \
                    all(p not in f and q not in f for f in facs)
                tally["collinear"] += 1
            else:
                hl = hyp_line(p, q)
                cl = Counter(centre_of[x.tobytes()] for x in prods if kind(x) == "clock")
                sp = {fac_of[x.tobytes()] for x in prods if kind(x) == "split"}
                fac = frozenset([p, q] + hl) | frozenset(z for z in range(40) if A[z, p] and A[z, q])
                far_ok &= kinds == Counter(clock=6, split=3) and len(hl) == 2 and dict(cl) == {hl[0]: 3, hl[1]: 3} and sp == {fac}
                tally["far"] += 1
    res["pairs"] = dict(tally)
    checks["same event: the 3 clocks and 1 form a Klein four-group (c1 c2 = c3)"] = bool(same_ok)
    checks["collinear p,q: all 9 products split = the 9 involutions of the 3 factorisations separating r and s"] = bool(col_ok)
    checks["non-collinear p,q: 6 products = the clocks at r, s (3 each); 3 = the splits of <p,q> + <p,q>^perp"] = bool(far_ok)
    checks = {k: bool(v) for k, v in checks.items()}
    res["checks"] = checks
    res["all_checks_pass"] = all(checks.values())
    OUT.write_text(json.dumps(res, indent=2))
    print(json.dumps(checks, indent=1), res["all_checks_pass"])
    return res


if __name__ == "__main__":
    main()
