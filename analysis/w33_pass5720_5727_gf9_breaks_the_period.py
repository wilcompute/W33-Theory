"""Passes 5720-5727 -- GF(9) refutes the period-(q-1) claim and reveals a digit product.

  5720  CORRECTION: the tower wraps at e = p, the CHARACTERISTIC, not e = q.
  5721  And the law is MULTIPLICATIVE over the base-p digits of e.
  5722  Why q = 3,5,7,11 could not have caught this: they are all prime.
  5723  The attainment is still not found in the literature; the bound is.
  5724  DATE_FILE_INTEGER_INDEX.md, published: 191 integers, 614 entries.
  5725  44 corpus files carry a theorem word and a one-line-proof marker.
  5726  S4 wr S2, closed as an open question after four attempts.
  5727  Were the negative results wrong questions?

    py -3 analysis/w33_pass5720_5727_gf9_breaks_the_period.py
"""

from __future__ import annotations

import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

GF9 = [(1, 4), (2, 10), (3, 4), (4, 16), (5, 40)]
PRIME = {3: [4, 10], 5: [4, 10, 20, 35], 7: [4, 10, 20, 35, 56, 84],
         11: [4, 10, 20, 35, 56, 84, 120, 165, 220, 286]}
INDEX = {"file": "DATE_FILE_INTEGER_INDEX.md", "integers": 191, "entries": 614,
         "source_files": 185}
ONELINE = {"files": 44, "examples": ["2026-05-30_c3_fano_triangle_orientation.md",
                                     "2026-07-10_levi_closure.md",
                                     "2026-07-08_pass75_uniqueness_constants_synthesis.md"]}
ATTEMPTS = ["Delsarte coset graph (Pass 5671)", "two-weight structure (Pass 5671)",
            "the GF(2) kernel (Pass 5685)", "module irreducibility (Pass 5715)"]


def digits(e, p):
    out = []
    while e:
        out.append(e % p)
        e //= p
    return out or [0]


def predict(e, p):
    r = 1
    for d in digits(e, p):
        r *= comb(d + 3, 3)
    return r


def main() -> int:
    print("=" * 78)
    print("Passes 5720-5727 -- GF(9) breaks the period")
    print("=" * 78)

    print("\n  PASS 5720 -- CORRECTION\n")
    print(f"    {'e':>3s} {'rank over GF(9)':>16s} {'dim Sym^e':>10s} {'base-3 digits':>14s}")
    for e, r in GF9:
        print(f"    {e:3d} {r:16d} {comb(e + 3, 3):10d} {str(digits(e, 3)[::-1]):>14s}")
    print("""
    PASS 5713 CLAIMED PERIOD q-1. At q=9 that would put the wrap at e=9. It is at e=3.

    THE WRAP IS AT THE CHARACTERISTIC, NOT AT q. GF(9) has characteristic 3, so the
    Frobenius map is x -> x^3, and sf^3 = Frobenius(sf) is again a form of rank 4. For a
    PRIME q the characteristic equals q and the two statements coincide -- which is exactly
    why q = 3, 5, 7, 11 could not distinguish them. Every verification I ran was at a prime.""")

    print("\n  PASS 5721 -- and the law is a digit product\n")
    print(f"    {'e':>3s} {'measured':>9s} {'digit product':>14s} {'digits (base 3)':>16s}")
    ok = True
    for e, r in GF9:
        p = predict(e, 3)
        ok &= p == r
        print(f"    {e:3d} {r:9d} {p:14d} {str(digits(e, 3)[::-1]):>16s}   "
              f"{'match' if p == r else 'MISMATCH'}")
    print(f"""
    ALL {len(GF9)} MATCH. Writing e in base p and taking the product of dim Sym^(digit):

        rank( sf^e )  =  PRODUCT over base-p digits d of e  of  C(d+3, 3)

    e=4 is (1,1) in base 3, giving 4 x 4 = 16. e=5 is (1,2), giving 4 x 10 = 40. e=3 is
    (1,0), giving 4 x 1 = 4 -- the wrap. The prime case is the special case where e < p has
    a single digit and the product collapses to C(e+3,3).

    THIS IS THE SHAPE OF A STEINBERG TENSOR PRODUCT, where a twisted module factors over
    base-p digits of the highest weight. I am naming the shape and NOT claiming the
    theorem: this is verified at five exponents at one non-prime q, and the identification
    with Steinberg is a resemblance I have not proved.""")

    print("\n  PASS 5722 -- what the prime verifications were worth\n")
    for q, ranks in PRIME.items():
        print(f"    q={q:2d}: {ranks}   (all single-digit, e < p = q)")
    print("""
    NOT WRONG, BUT BLIND TO THE STRUCTURE. Ten agreeing rungs at q=11 confirmed attainment
    and told me nothing about the digit law, because at a prime every e < q has one digit.
    A single composite q was worth more than four primes, and I ran the primes first
    because they were easier.""")

    print("\n  PASS 5723 -- the literature, again\n")
    print("    the BOUND rank(A^(*p)) <= C(p+d-1, p) is classical; at d = 4 it is C(e+3,3)")
    print("    the ATTAINMENT for symplectic forms: searched again, NOT FOUND")
    print("""    So the standing attribution is unchanged from Pass 5704: the bound is not
    mine, the attainment and now the digit law are measurements. Whether the digit law is
    classical is a THIRD literature question I am recording as open rather than answering,
    since the Steinberg resemblance makes it likely.""")

    print("\n  PASS 5724-5725 -- two artifacts\n")
    print(f"    {INDEX['file']}: {INDEX['integers']} integers, {INDEX['entries']} entries, "
          f"over {INDEX['source_files']} date-named files")
    print(f"    one-line-proof filter: {ONELINE['files']} files carry both a theorem word")
    print(f"      and a one-line-proof marker -- the claims to search FIRST")
    print("""
    THE FILTER IS THE SESSION'S OWN LESSON, MADE MECHANICAL. Two of my eight claims were
    classical and both had one-line proofs (Pass 5717). Forty-four corpus files match the
    same pattern. That is a work list, not a verdict -- a one-line proof is a reason to
    search, not evidence of rediscovery.""")

    print("\n  PASS 5726-5727 -- S4 wr S2, closed as open\n")
    for a in ATTEMPTS:
        print(f"    tried: {a}")
    print("""
    FOUR ATTEMPTS, ALL NEGATIVE, AND I AM STOPPING. Why S4 wr S2 appears as the
    automorphism group of the tomotope's 16-face graph is recorded as an OPEN QUESTION
    rather than attacked a fifth time. This repo's own guidance is that a claim naming no
    object is not a claim; the converse discipline is that four failed approaches to one
    object is a signal about the question, not an invitation to try harder.

    AND THE COMMON SHAPE OF ALL FOUR IS WORTH NAMING: each asked "where inside this object
    is the structure hiding" -- in a coset graph, a code, a kernel, a submodule. If
    S4 wr S2 is not intrinsic to the object but inherited from how the object was
    CONSTRUCTED, every internal search fails for the same reason, and the next attempt
    should look at the construction rather than the result.""")

    out = {
        "boundary": (
            "Pass 5720 CORRECTS Pass 5713's period-(q-1) claim: the wrap is at the "
            "characteristic. Pass 5721's digit law is verified at five exponents at ONE "
            "non-prime q and is NOT proved; the Steinberg identification is a named "
            "resemblance, not a claim. Pass 5723 leaves the attainment and the digit law "
            "as open literature questions. Pass 5725's 44 files are a work list, not "
            "findings. Pass 5726 CLOSES S4 wr S2 as open rather than solving it"),
        "pass_5720": {"claim_corrected": "Pass 5713's period q-1",
                      "truth": "the tower wraps at e = p, the characteristic",
                      "gf9": [{"e": e, "rank": r, "dim_sym": comb(e + 3, 3)} for e, r in GF9],
                      "why_missed": "q = 3,5,7,11 are all prime, where p = q"},
        "pass_5721": {"law": "rank(sf^e) = product over base-p digits d of e of C(d+3,3)",
                      "verified": [{"e": e, "measured": r, "predicted": predict(e, 3)}
                                   for e, r in GF9],
                      "all_match": ok,
                      "resemblance": ("the shape of a Steinberg tensor product; NAMED, not "
                                      "claimed -- five exponents at one composite q")},
        "pass_5722": {"prime_runs": {str(q): r for q, r in PRIME.items()},
                      "lesson": ("one composite q was worth more than four primes; I ran "
                                 "the primes first because they were easier")},
        "pass_5723": {"bound": "classical, rank(A^(*p)) <= C(p+d-1,p)",
                      "attainment": "NOT FOUND",
                      "digit_law": "open literature question, likely classical via Steinberg"},
        "pass_5724_5725": {**INDEX, "one_line_filter": ONELINE,
                           "status": "work list, not verdicts"},
        "pass_5726_5727": {"attempts": ATTEMPTS, "status": "OPEN, closed to further attempts",
                           "common_shape": ("all four asked where INSIDE the object the "
                                            "structure hides; if S4 wr S2 is inherited "
                                            "from the CONSTRUCTION rather than intrinsic, "
                                            "every internal search fails identically")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5720_5727_GF9_BREAKS_THE_PERIOD.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
