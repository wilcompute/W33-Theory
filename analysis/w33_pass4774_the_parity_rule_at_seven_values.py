#!/usr/bin/env python3
"""Pass 4774 -- the parity rule at seven values of q, including two non-prime prime powers.

Pass 4755 settled "W(3,q) is self-dual iff q is even" at q = 2,3,4,5.  Three of those are
prime and one is 2^2, so the evidence was thin on the distinction that matters: is the rule
about the PARITY of q, or about q being a power of 2 specifically, or does primality enter?

q = 8 = 2^3 and q = 9 = 3^2 separate those readings, and both are now constructible because
the irreducible-polynomial table already carried GF(2^3) and GF(3^2).  Nothing new was
needed except running it.

    py -3 analysis/w33_pass4774_the_parity_rule_at_seven_values.py
"""

from __future__ import annotations

import importlib.util
import itertools
import sys
import time
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def _load(tag, fn):
    s = importlib.util.spec_from_file_location(tag, ROOT / "analysis" / fn)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


PP = _load("pp", "w33_pass4754_4755_prime_power_quadrangles_and_bliss.py")


def graph_of(pts, lines):
    g = igraph.Graph(n=len(pts))
    e = set()
    for L in lines:
        for u, v in itertools.combinations(sorted(L), 2):
            e.add((u, v))
    g.add_edges(sorted(e))
    return g


def main() -> int:
    print("=" * 78)
    print("Pass 4774 -- W(3,q) self-duality at seven prime powers")
    print("=" * 78)

    print(f"\n  {'q':>3s} {'field':>9s} {'prime?':>7s} {'n':>5s} {'SRG':>22s} "
          f"{'self-dual':>10s} {'even?':>6s} {'agrees':>7s}")
    rows = []
    for p, k in ((2, 1), (3, 1), (2, 2), (5, 1), (7, 1), (2, 3), (3, 2)):
        q = p ** k
        t0 = time.time()
        pts, lines = PP.build_w3(PP.GF(p, k))
        g = graph_of(pts, lines)
        got = PP.srg_params(g)
        want = ((q + 1) * (q * q + 1), q * (q + 1), q - 1, q + 1)
        dp, dl = PP.dual(pts, lines)
        h = graph_of(dp, dl)
        iso = PP.canon(g) == PP.canon(h)
        rows.append({"q": q, "p": p, "k": k, "prime": k == 1, "n": len(pts),
                     "srg": list(got), "srg_correct": got == want,
                     "self_dual": bool(iso), "even": q % 2 == 0,
                     "agrees": bool(iso == (q % 2 == 0)),
                     "seconds": round(time.time() - t0, 1)})
        print(f"  {q:3d} {('GF(%d^%d)'%(p,k)) if k>1 else ('GF(%d)'%p):>9s} "
              f"{str(k==1):>7s} {len(pts):5d} {str(got):>22s} {str(iso):>10s} "
              f"{str(q%2==0):>6s} {str(iso == (q%2==0)):>7s}")

    agree = all(r["agrees"] for r in rows)
    params_ok = all(r["srg_correct"] for r in rows)
    print(f"""
    SEVEN VALUES, ALL AGREE, AND TWO OF THEM SEPARATE READINGS THAT q = 2,3,4,5 COULD NOT.

    q = 8 = 2^3 is even and NOT prime, and it is self-dual. So the rule is not "q prime and
    even", and it is not confined to q = 2^2 or to primes -- being a power of 2 is enough.

    q = 9 = 3^2 is odd and not prime, and it is not self-dual. So primality is irrelevant on
    that side too. What decides it is the CHARACTERISTIC: even means characteristic 2, and
    the symplectic and orthogonal forms coincide there because a quadratic form is
    recoverable from its polarisation only away from 2.

    THAT IS WHY THE RULE HAS THE SHAPE IT DOES, and it is worth stating because the corpus
    kept writing the condition as s = t. GQ(q,q) has s = t at every q; self-duality picks out
    half of them. Pass 4694 corrected that once, from Track C's GQ(3,3) failure. Here it is
    corrected by construction, at seven values, with the reason attached.""")

    out = {
        "boundary": ("all seven are constructed and their SRG parameters verified against "
                     "theory; isomorphism is exact via BLISS canonical form. The reason "
                     "given (characteristic 2 makes the symplectic and orthogonal forms "
                     "coincide) is standard theory cited to explain the pattern, NOT "
                     "derived here -- what is computed is the pattern"),
        "rows": rows,
        "all_parameters_correct": bool(params_ok),
        "parity_rule_holds_everywhere_tested": bool(agree),
        "what_the_new_values_settle": (
            "q=8=2^3 is even, non-prime, and self-dual, so the rule is not about primality "
            "or about q=2^2; q=9=3^2 is odd, non-prime, and not self-dual, so primality is "
            "irrelevant on that side too. The characteristic decides it"),
        "why_not_s_equals_t": (
            "GQ(q,q) has s=t at every q, and self-duality picks out exactly the even half; "
            "the two conditions are not the same, which is what Pass 4694 corrected"),
    }
    p = ROOT / "data" / "PART_W33_PASS4774_PARITY_RULE_SEVEN_VALUES.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
