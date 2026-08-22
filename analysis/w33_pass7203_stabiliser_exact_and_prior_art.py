"""Pass 7203 -- the exact q=3 stabiliser, and citing the conjecture I proved.

PRIOR ART, found by searching for the RESULT rather than the topic, as CLAUDE.md demands.
scripts/w33_ovoid_stabiliser_exact.py (Pass 6285-6300) already records

    q=3: alpha(W(3,3)) = 7, stabiliser order 18 EXACT, orbit index 51840/18 = 2880
    q=5: alpha(W(3,5)) = 18, one symplectic fix in 3000 samples

and already states the conjecture

    "max partial ovoids of W(3,q) for odd q have tiny stabilisers, so group-orbit
     constructions cannot work"

THAT CONJECTURE IS EXACTLY WHAT PASS 7192 PROVED. So Pass 7192 is not a discovery, it is a
PROOF OF AN EXISTING CONJECTURE OF THIS REPO, and the conjecture must be cited. What was new
this week is the proof (exact ILPs over orbits, caps of 30/15/15 against a representable 33)
and the sharpening at q=7 and q=9 to |Stab| <= 2. The plateau explanation was already ours.

WHAT THIS PASS ADDS. Pass 6285-6300 called q=3 "PROVED" and q=5 sampled. |Sp(4,3)| = 51840
is small enough to settle q=3 by brute force, so this enumerates the whole group and counts
setwise stabilisers exactly -- confirming or refuting 18, and simultaneously testing the
Pass 7199 bound (72) which must be a multiple of the true order if the method is sound.

    py -3 analysis/w33_pass7203_stabiliser_exact_and_prior_art.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import (  # noqa: E402
    Field, geometry, transvection, matmul, apply, IDENT,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

PRIOR = {"file": "scripts/w33_ovoid_stabiliser_exact.py",
         "pass": "6285-6300",
         "q3_stab": 18, "q3_orbit": 2880,
         "conjecture": ("max partial ovoids of W(3,q) for odd q have tiny stabilisers, "
                        "so group-orbit constructions cannot work")}


def main() -> int:
    print("=" * 78)
    print("Pass 7203 -- exact q=3 stabiliser, and the conjecture Pass 7192 proved")
    print("=" * 78)

    print(f"""
  PRIOR ART CITED. {PRIOR['file']} (Pass {PRIOR['pass']}) already records the exact
  q=3 stabiliser order {PRIOR['q3_stab']} and already CONJECTURES:

      "{PRIOR['conjecture']}"

  Pass 7192 proved that conjecture. It did not discover it. Recording the citation.
""")

    q = 3
    F = Field(q)
    P, idx, adj, B = geometry(F)
    n = len(P)

    # generate Sp(4,3) by closure from transvections
    gens = [transvection(F, p, lam) for p in P for lam in range(1, q)]
    G = {IDENT}
    frontier = [IDENT]
    while frontier:
        nxt = []
        for X in frontier:
            for g in gens:
                Y = matmul(F, X, g)
                if Y not in G:
                    G.add(Y)
                    nxt.append(Y)
        frontier = nxt
    print(f"  |<transvections>| = {len(G)}   (|Sp(4,3)| = 51840)")
    if len(G) != 51840:
        print("  group generation did not reach Sp(4,3) -- aborting rather than guessing")
        return 1

    src = ROOT / "data" / "PART_W33_Q3_PARTIAL_OVOID_7.json"
    O = sorted(idx[tuple(p)] for p in json.loads(src.read_text(encoding="utf-8"))["points"])
    assert all(B(P[a], P[b]) != 0 for a, b in itertools.combinations(O, 2))
    Oset = set(O)
    print(f"  our 7-set: {O}", flush=True)

    stab = [M for M in G if {idx[apply(F, M, P[p])] for p in O} == Oset]
    k = len(stab)
    orbit = len(G) // k
    print(f"\n  |Stab(O)| = {k}   orbit size = {len(G)}/{k} = {orbit}")
    agree = (k == PRIOR["q3_stab"])
    print(f"  prior art says {PRIOR['q3_stab']}, orbit {PRIOR['q3_orbit']} -- "
          f"{'CONFIRMED' if agree and orbit == PRIOR['q3_orbit'] else 'DISAGREES'}")

    # element orders present in the stabiliser
    orders = {}
    for M in stab:
        X, e = M, 1
        while X != IDENT and e <= 64:
            X = matmul(F, X, M)
            e += 1
        orders[e] = orders.get(e, 0) + 1
    print(f"  element orders in Stab(O): {dict(sorted(orders.items()))}")

    bound = 72
    ok = bound % k == 0
    print(f"\n  PASS 7199 CROSS-CHECK. Its upper bound at q=3 was {bound}. A sound upper "
          f"bound\n  must be a multiple of the true order {k}: {bound} % {k} = {bound % k}"
          f" -- {'CONSISTENT' if ok else 'INCONSISTENT, the method is broken'}")
    if ok:
        print(f"  So the Pass 7199 method is sound but loose at q=3 (factor {bound // k}),")
        print(f"  which is exactly why its sharp values at q=7 and q=9 (both 2) matter:")
        print(f"  a bound of 2 leaves only orders 1 and 2 whatever the looseness.")

    out = {
        "boundary": ("exact |Stab| at q=3 by full enumeration of Sp(4,3). CONFIRMS the prior "
                     "art at Pass 6285-6300. Pass 7192 PROVED a conjecture already stated "
                     "there; it did not discover it"),
        "prior_art": PRIOR,
        "recomputed": {"group_order": len(G), "stab_order": k, "orbit": orbit,
                       "element_orders": {str(a): b for a, b in sorted(orders.items())}},
        "confirms_prior_art": agree,
        "pass7199_bound_consistent": ok,
        "what_was_actually_new_this_week": [
            "the PROOF that no order-3 element stabilises the q=7 optimum (exact ILP)",
            "the sharpening |Stab| <= 2 at q=7 and q=9",
            "the certified basin radius 9 at q=9"],
        "what_was_already_ours": [
            "the conjecture that these stabilisers are tiny",
            "the consequence that group-orbit constructions cannot work",
            "the exact q=3 stabiliser order 18"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7203_STAB_EXACT_PRIOR_ART.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
