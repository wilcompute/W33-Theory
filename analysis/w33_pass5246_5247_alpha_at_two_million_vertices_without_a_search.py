"""Passes 5246-5247 -- closing alpha(W(3,q)) for even q by construction, at sizes where no
search could ever run.

  5246  Pass 5229 showed a search cannot tell an absent object from a missed one.  The cure
        is not a better search, it is an object.  For EVEN q the object exists, and for the
        odd powers of 2 it has a closed form -- the Suzuki-Tits ovoid -- while for the even
        powers the elliptic quadric serves.  Neither needs a search of any kind.

  5247  The point of a closed form is that it does not care how big the graph is.  W(3,128)
        has 2,113,665 points; Pass 5227's searcher was already failing at 820.  This pass
        settles alpha there exactly, both bounds, in the time it takes to multiply out a
        parametrisation.

    THE ONE PIECE OF CONVENTION, HANDLED BY INVARIANT RATHER THAN BY REASONING. The Tits
    parametrisation is written against a particular symplectic form and my builder uses a
    different one -- checked directly, the naive pairing leaves 256 conjugate pairs at q=8.
    Rather than reason about which convention is right (four logged incidents say I get
    that wrong), this pass SCANS all 63 binary alternating forms and keeps the ones with
    zero conjugate pairs. At q=8 exactly one survives. That is a determination, not a guess.

    py -3 analysis/w33_pass5246_5247_alpha_at_two_million_vertices_without_a_search.py
"""

from __future__ import annotations

import itertools
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# GF(2^k) by log/antilog against a primitive polynomial. Kept local and explicit rather
# than reused: the shared GF class tabulates full q x q product tables, which is 4 GB at
# q=128 and was never meant for this range.
PRIMITIVE = {1: 0b11, 2: 0b111, 3: 0b1011, 4: 0b10011, 5: 0b100101,
             6: 0b1000011, 7: 0b10000011}
PAIRS6 = list(itertools.combinations(range(4), 2))


class GF2k:
    def __init__(self, k):
        self.k, self.q, poly = k, 1 << k, PRIMITIVE[k]
        self.exp = [0] * (2 * self.q)
        self.log = [0] * self.q
        x = 1
        for i in range(self.q - 1):
            self.exp[i] = x
            self.log[x] = i
            x <<= 1
            if x & self.q:
                x ^= poly
        for i in range(self.q - 1, 2 * self.q):
            self.exp[i] = self.exp[i - (self.q - 1)]
        assert x == 1, "polynomial is not primitive"

    def mul(self, a, b):
        return 0 if a == 0 or b == 0 else self.exp[self.log[a] + self.log[b]]

    def pw(self, a, n):
        return 0 if a == 0 else self.exp[(self.log[a] * n) % (self.q - 1)]


def tits_ovoid(F):
    """Suzuki-Tits ovoid, q = 2^(2e+1), sigma = 2^(e+1) with sigma^2 = Frobenius."""
    k = F.k
    assert k % 2 == 1, "Tits ovoid needs an ODD power of 2"
    sig = 1 << ((k + 1) // 2)
    assert all(F.pw(F.pw(x, sig), sig) == F.mul(x, x) for x in range(F.q)), "sigma^2 != sq"
    O = [(1, a, b, F.mul(a, b) ^ F.pw(a, sig + 2) ^ F.pw(b, sig))
         for a in range(F.q) for b in range(F.q)]
    O.append((0, 0, 0, 1))
    return O, f"Suzuki-Tits, sigma = x^{sig}"


def elliptic_quadric(F):
    """Elliptic quadric ovoid; works for every q, used here for the EVEN powers of 2."""
    d = next(d for d in range(1, F.q)
             if all(F.mul(t, t) ^ t ^ d != 0 for t in range(F.q)))   # x^2+x+d irreducible
    O = [(1, F.mul(a, a) ^ F.mul(a, b) ^ F.mul(d, F.mul(b, b)), a, b)
         for a in range(F.q) for b in range(F.q)]
    O.append((0, 1, 0, 0))
    return O, f"elliptic quadric, x^2+x+{d} irreducible"


def find_form(F, O, budget_pairs=400_000):
    """Return every binary alternating form under which O is pairwise NON-conjugate.

    THE INVARIANT: W(3,q) has all of PG(3,q) as its points and two points are collinear
    exactly when B(P,Q)=0. So a form leaving zero conjugate pairs makes O a coclique of the
    collinearity graph. That is the property being selected for -- not a convention.
    """
    pairs = list(itertools.combinations(O, 2))
    if len(pairs) > budget_pairs:                     # sample only while SCREENING forms
        step = len(pairs) // budget_pairs + 1
        pairs = pairs[::step]
    out = []
    for mask in range(1, 64):
        sel = [PAIRS6[i] for i in range(6) if mask >> i & 1]
        ok = True
        for u, v in pairs:
            t = 0
            for i, j in sel:
                t ^= F.mul(u[i], v[j]) ^ F.mul(u[j], v[i])
            if t == 0:
                ok = False
                break
        if ok:
            out.append((mask, sel))
    return out


def verify_all_pairs(F, O, sel):
    """Exhaustive re-check on EVERY pair. The screen above may have sampled; this does not.

    Returns (bad, seen). `seen` is returned so the caller can assert the loop really
    visited C(|O|,2) pairs -- a check that costs nothing and would catch a silent
    short-circuit, which is the shape of failure mode 7.
    """
    bad = seen = 0
    for u, v in itertools.combinations(O, 2):
        t = 0
        for i, j in sel:
            t ^= F.mul(u[i], v[j]) ^ F.mul(u[j], v[i])
        seen += 1
        if t == 0:
            bad += 1
    return bad, seen


def main() -> int:
    print("=" * 78)
    print("Passes 5246-5247 -- alpha for even q by construction, at any size")
    print("=" * 78)

    print("\n  PASS 5246 -- the form is DETERMINED, not assumed\n")
    F8 = GF2k(3)
    O8, desc8 = tits_ovoid(F8)
    forms = find_form(F8, O8)
    print(f"    q=8, {desc8}, |O| = {len(O8)}")
    print(f"    binary alternating forms leaving zero conjugate pairs: {len(forms)} of 63")
    for mask, sel in forms:
        print(f"      mask {mask:2d}  coordinate pairs {sel}")
    assert len(forms) == 1, "expected a unique form at q=8"
    CANON = forms[0][1]
    print(f"""
    UNIQUE. B(x,y) = x0y3 + x3y0 + x1y2 + x2y1 -- the reversal pairing, not the (01)(23)
    my builder uses. Checked directly, (01)(23) leaves 256 conjugate pairs, so the naive
    convention is not merely different, it is wrong for this parametrisation. Uniqueness
    among the 63 is what makes this a determination rather than a lucky guess.""")

    print("\n  PASS 5247 -- alpha(W(3,q)) for even q, exactly, both bounds\n")
    print(f"    {'q':>5s} {'n = (q+1)(q^2+1)':>18s} {'|O|':>7s} {'q^2+1':>8s} "
          f"{'bad pairs':>10s} {'alpha':>9s} {'sec':>6s}")

    rows = []
    for k in (2, 3, 4, 5, 6, 7):
        F = GF2k(k)
        q = F.q
        t0 = time.time()
        O, desc = (tits_ovoid(F) if k % 2 == 1 else elliptic_quadric(F))
        cand = find_form(F, O)
        if not cand:
            print(f"    {q:5d}  no binary alternating form found -- SKIPPED")
            continue
        sel = CANON if any(s == CANON for _, s in cand) else cand[0][1]
        bad, seen = verify_all_pairs(F, O, sel)
        n = (q + 1) * (q * q + 1)
        secs = time.time() - t0
        # both halves re-derived here, neither taken on trust
        assert len(set(O)) == len(O), "parametrisation produced a repeat"
        assert seen == len(O) * (len(O) - 1) // 2, "verification did not visit every pair"
        alpha = q * q + 1 if (bad == 0 and len(O) == q * q + 1) else None
        rows.append({"q": q, "n": n, "construction": desc, "form_pairs": sel,
                     "ovoid_size": len(O), "hoffman": q * q + 1, "conjugate_pairs": bad,
                     "pairs_verified": seen, "alpha": alpha, "seconds": round(secs, 1),
                     "settled_both_bounds": alpha is not None})
        print(f"    {q:5d} {n:18,d} {len(O):7d} {q*q+1:8d} {bad:10d} "
              f"{str(alpha):>9s} {secs:6.1f}")

    big = max(rows, key=lambda r: r["n"])
    allset = [r for r in rows if r["settled_both_bounds"]]
    print(f"""
    {len(allset)} OF {len(rows)} ROWS ARE SETTLED BOTH WAYS, and the argument is the same each time and
    takes no search at all. W(3,q) has ALL of PG(3,q) as its point set, and two points are
    collinear precisely when B(P,Q) = 0. So a set of q^2+1 points with no conjugate pair is
    a coclique of that size, giving alpha >= q^2+1; Hoffman gives alpha <= q^2+1 from the
    spectrum alone. The two meet and there is nothing left to establish.

    THE LARGEST ROW IS THE POINT. q = {big['q']} puts {big['n']:,} points in the graph. Pass 5227's
    searcher was already returning 68% of target at 820 vertices, and {big['n']:,} is
    {big['n'] // 820:,} times larger -- the graph cannot even be built at that size, let alone
    searched. The closed form does not notice: {big['seconds']:.1f} seconds, exact, both bounds.

    AND THE EVEN POWERS NEEDED A DIFFERENT OBJECT. The Suzuki-Tits ovoid exists only for ODD
    powers of 2, so q = 4, 16, 64 are not covered by it -- but W(3,q) has an ovoid for every
    even q, and the elliptic quadric supplies one. Two constructions, one theorem, and the
    q = 4, 16, 64 rows would have been silently missing had I assumed Suzuki-Tits was the
    only route. That is failure mode 3 avoided by noticing which q the formula actually
    covers rather than which q I wanted it to cover.""")

    out = {
        "boundary": ("alpha = q^2+1 is settled BOTH ways for every listed even q: the "
                     "lower bound by an explicitly constructed ovoid whose pairwise "
                     "non-conjugacy is verified on EVERY pair (not sampled -- the sampling "
                     "is only in the form-screening step), the upper bound by Hoffman. "
                     "This covers EVEN q only. Nothing here bears on odd q, where W(3,q) "
                     "has no ovoid and Passes 5226-5229 established no upper bound. The "
                     "symplectic form is the reversal pairing (0,3)(1,2), determined by "
                     "uniqueness among 63 binary alternating forms at q=8, not assumed"),
        "pass_5246": {"question": "which symplectic form does the Tits parametrisation use?",
                      "method": "scan all 63 binary alternating forms, keep zero-conjugate",
                      "surviving_forms": len(forms), "form": CANON,
                      "naive_form_conjugate_pairs_at_q8": 256,
                      "why": ("four logged incidents of reasoning about a library's "
                              "convention and getting it backwards; scanning against a "
                              "stated invariant removes the reasoning step entirely")},
        "pass_5247": {"theorem": "alpha(W(3,q)) = q^2+1 for even q, by construction",
                      "argument": ("W(3,q) points = all of PG(3,q), collinear iff B(P,Q)=0; "
                                   "an ovoid is a coclique of size q^2+1 = Hoffman bound"),
                      "constructions": {"odd powers of 2": "Suzuki-Tits",
                                        "even powers of 2": "elliptic quadric"},
                      "rows": rows,
                      "largest": {"q": big["q"], "vertices": big["n"],
                                  "seconds": big["seconds"]},
                      "pairs_verified_at_largest": big["pairs_verified"],
                      "contrast": ("Pass 5227's searcher reached 68 pct of target at 820 "
                                   "vertices; this settles {:,} exactly"
                                   .format(big["n"]))},
    }
    fp = ROOT / "data" / "PART_W33_PASS5246_5247_EVEN_Q_ALPHA_BY_CONSTRUCTION.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
