"""Guard: is the "encoded" number actually FORCED by parameters already present?

WARN-ONLY.

The Aug 18 batch passed `scripts/audit_batch.py` clean while claiming that W(3,3)'s
adjacency multiplicities 1, 24, 15 "encode Monster moonshine" -- 24 as the Leech lattice
rank, 15 as the number of supersingular primes.  They encode neither.  For a strongly
regular graph the multiplicities are DETERMINED by (v, k, lambda, mu):

    f, g = [ (v-1) -+ (2k + (v-1)(lambda-mu)) / sqrt((lambda-mu)^2 + 4(k-mu)) ] / 2

and at (40,12,2,4) that is exactly 24 and 15.  Any SRG with those parameters has them, and
32 other feasible parameter sets share a multiplicity of 15 or 24.

The existing harness checks REDISCOVERY (has this number appeared before?) and certificate
vocabulary.  Neither catches a number that is meaningful-looking but arithmetically forced.
This does.

Two tests:

  1. SRG MULTIPLICITY.  A certificate recording SRG parameters and multiplicities is checked
     against the closed form.  If they match, any interpretive claim about those
     multiplicities is reading meaning into forced arithmetic.
  2. ENCODING LANGUAGE.  Interpretive vocabulary -- encodes, means, corresponds to, is the
     -- attached to a number that also appears as a derived quantity in the same file.

    py -3 scripts/check_forced_arithmetic.py --selftest
    py -3 scripts/check_forced_arithmetic.py data/YOUR_CERTIFICATE.json
"""

from __future__ import annotations

import json
import re
import sys
from math import isqrt
from pathlib import Path

ENCODING = re.compile(r"\b(encodes?|encoding|means|meaning|corresponds? to|is the\b|"
                      r"signature|witness(?:es)? that)\b", re.I)


def srg_multiplicities(v, k, lam, mu):
    """Closed form. Returns (r, s, f, g) or None if the parameters are infeasible."""
    D = (lam - mu) ** 2 + 4 * (k - mu)
    if D < 0:
        return None
    s0 = isqrt(D)
    if s0 * s0 != D or s0 == 0:
        return None
    num = 2 * k + (v - 1) * (lam - mu)
    if num % s0:
        return None
    f = ((v - 1) - num // s0) // 2
    g = ((v - 1) + num // s0) // 2
    if f + g != v - 1 or f < 0 or g < 0:
        return None
    return ((lam - mu) + s0) // 2, ((lam - mu) - s0) // 2, f, g


def walk(doc, key=""):
    if isinstance(doc, dict):
        for a, b in doc.items():
            yield from walk(b, a)
    elif isinstance(doc, list):
        if doc and all(isinstance(x, int) and not isinstance(x, bool) for x in doc):
            yield key, doc
        else:
            for x in doc:
                yield from walk(x, key)
    else:
        yield key, doc


KEYNUM = re.compile(r"mult[_a-z]*_(\d+)", re.I)


def findings(doc) -> list[str]:
    out: list[str] = []
    nums, lists, texts = {}, {}, []
    # BT1645 stores multiplicities inside KEY NAMES ("r_2_mult_24"), not as values.
    # Harvest those too, or the guard misses the case that motivated it.
    keymults = []
    for k, _ in walk(doc):
        m = KEYNUM.search(k or "")
        if m:
            keymults.append(int(m.group(1)))
    if keymults:
        lists.setdefault("multiplicities_from_keys", sorted(keymults))
    for k, v in walk(doc):
        kl = k.lower()
        if isinstance(v, int) and not isinstance(v, bool):
            nums.setdefault(kl, v)
        elif isinstance(v, list):
            lists.setdefault(kl, v)
        elif isinstance(v, str) and ENCODING.search(v):
            texts.append((k, v[:110]))

    def pick(*names):
        for nm in names:
            for kk, vv in nums.items():
                if kk == nm or kk.endswith("_" + nm):
                    return vv
        return None

    v = pick("v", "vertices", "points", "order")
    k = pick("k", "degree", "valency")
    lam = pick("lambda", "lam")
    mu = pick("mu")
    if None not in (v, k, lam, mu):
        res = srg_multiplicities(v, k, lam, mu)
        if res:
            r, s, f, g = res
            for lk, lv in lists.items():
                if "multipl" in lk and sorted(x for x in lv if x != 1) == sorted([f, g]):
                    out.append(
                        f"multiplicities {lv} are FORCED by SRG({v},{k},{lam},{mu}) -- the "
                        f"closed form gives {f} and {g}. Any interpretive claim about them "
                        f"is reading meaning into forced arithmetic")
    if texts and out:
        kk, tt = texts[0]
        out.append(f"and the file carries interpretive language in `{kk}`: {tt}...")
    return out


def selftest() -> int:
    cases = [
        ("the Aug 18 moonshine claim",
         {"v": 40, "k": 12, "lambda": 2, "mu": 4, "multiplicities": [1, 24, 15],
          "note": "24 encodes the Leech lattice rank"}, True),
        ("same SRG, multiplicities stated without interpretation",
         {"v": 40, "k": 12, "lambda": 2, "mu": 4, "multiplicities": [1, 24, 15]}, True),
        ("SRG parameters with no multiplicities recorded",
         {"v": 40, "k": 12, "lambda": 2, "mu": 4, "note": "24 encodes something"}, False),
        ("multiplicities that do NOT match the closed form",
         {"v": 40, "k": 12, "lambda": 2, "mu": 4, "multiplicities": [1, 20, 19]}, False),
        ("no SRG data at all",
         {"note": "the number 24 encodes the Leech lattice rank"}, False),
        ("multiplicities hidden in KEY NAMES, as BT1645 does",
         {"v": 40, "k": 12, "lambda": 2, "mu": 4,
          "spectrum": {"k_12_mult_1": "vacuum", "r_2_mult_24": "Leech rank",
                       "s_neg4_mult_15": "supersingular primes"}}, True),
    ]
    ok = True
    print("  selftest -- forced SRG multiplicities and encoding language\n")
    for name, doc, want in cases:
        got = bool(findings(doc))
        ok &= got == want
        print(f"    {name:48s} got={str(got):5s} want={str(want):5s} "
              f"{'ok' if got == want else 'FAIL'}")
    print("""
  THE SECOND CASE IS DELIBERATE. Multiplicities matching the closed form are flagged even
  when the prose is silent, because the flag is about the NUMBERS BEING DERIVED, not about
  the wording. A later reader is the one at risk of reading meaning into them.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    total = 0
    files = [Path(a) for a in argv if not a.startswith("-")]
    for f in files:
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for m in findings(doc):
            total += 1
            print(f"  {f.name}\n      {m}")
    print(f"\n  {total} forced-arithmetic finding(s) in {len(files)} certificate(s)")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
