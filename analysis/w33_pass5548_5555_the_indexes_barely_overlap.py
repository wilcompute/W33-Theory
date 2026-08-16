"""Passes 5548-5555 -- the two indexes share 37 tokens out of 132,276, the q=3 collision
rate is measured at 2x, and three more verifiers are repaired.

  5548  How much of the certificate index was already reachable through RESULTS_INDEX.
  5549  The alpha=18 query, and why my first lookup missed it.
  5550  The q=3 collision rate, measured rather than asserted.
  5551  Three verifier traps patched; the certificate index wired into the guard.

    py -3 analysis/w33_pass5548_5555_the_indexes_barely_overlap.py
"""

from __future__ import annotations

import itertools
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Substrate quantities as closed forms in q, all taken from this thread's own passes.
QUANTS = {
    "points": lambda q: (q + 1) * (q * q + 1),
    "quadric": lambda q: (q + 1) ** 2,
    "nonsing_half": lambda q: (q ** 3 - q) // 2,
    "hoffman": lambda q: q * q + 1,
    "flags": lambda q: q * (q * q - 1) * (q + 1) // 2,
    "linedeg": lambda q: q * (q - 1) // 2,
    "ptdeg": lambda q: q + 1,
    "affine": lambda q: q ** 3,
    "hyperplane": lambda q: q * q + q + 1,
    "q_squared": lambda q: q * q,
    "AB_class": lambda q: q * q * (q - 1) // 2,
    "lines": lambda q: (q + 1) * (q * q + 1),
}


def main() -> int:
    print("=" * 78)
    print("Passes 5548-5555 -- 37 shared out of 132,276")
    print("=" * 78)

    cert = (ROOT / "CERTIFICATE_RESULTS_INDEX.md").read_text(encoding="utf-8",
                                                             errors="replace")
    res = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8", errors="replace")
    ctoks = set(re.findall(r"\| `([^`]+)` \|", cert))
    rtoks = set(re.findall(r"\| `([^`]+)` \|", res))

    print("\n  PASS 5548 -- how much was already reachable\n")
    print(f"    RESULTS_INDEX tokens  : {len(rtoks):,}")
    print(f"    certificate tokens    : {len(ctoks):,}")
    print(f"    shared                : {len(rtoks & ctoks):,}")
    print(f"    certificate-only      : {len(ctoks - rtoks):,}")
    print(f"""
    THIRTY-SEVEN. Out of {len(ctoks):,} certificate tokens, {len(rtoks & ctoks)} were already reachable through the
    prose-and-code index. The two indexes are effectively disjoint, which answers the
    question the overlap was meant to answer: the certificates were not a duplicate view of
    the corpus, they were an unindexed half of it.

    THAT IS ALSO THE HONEST CAVEAT ON THE 132,276. Disjointness at that scale means the two
    grammars are measuring different things, not that 132,239 new RESULTS appeared. Most
    certificate tokens are field values -- the grammar drops schema keys and >25-file tokens
    but cannot tell a one-off finding from a one-off field name.""")

    print("\n  PASS 5549 -- the alpha=18 lookup\n")
    has18 = "alpha@18" in ctoks
    hasexact7 = "alpha_exact@7" in ctoks
    print(f"    `alpha@18` in the certificate index       : {has18}")
    print(f"    `alpha_exact@7` in the certificate index  : {hasexact7}")
    print("""
    MY FIRST QUERY ASKED FOR alpha_exact@18 AND FOUND NOTHING, which briefly looked like the
    index failing on the exact value that cost this session six passes. It is not. BT818
    stores its value under `alpha_exact` and Pass 4800 stores its under `alpha`, inside a
    `rows` list -- so the tokens are alpha_exact@7 and alpha@18, and both are indexed.

    THE INDEX WOULD HAVE CAUGHT IT. What it cannot do is know that two passes calling the
    same quantity by two key names are talking about the same thing. That is the same
    vocabulary problem the noun@n grammar has in the rediscovery guard, one layer down, and
    it is not solvable by indexing harder.""")

    print("\n  PASS 5550 -- the q=3 collision rate\n")
    names = sorted(QUANTS)
    pairs = list(itertools.combinations(names, 2))
    rows = []
    for q in (3, 5, 7):
        c = sum(1 for a, b in pairs if QUANTS[a](q) == QUANTS[b](q))
        rows.append({"q": q, "collisions": c, "pairs": len(pairs)})
        print(f"    q={q}: {c} of {len(pairs)} pairs coincide  ({100 * c // len(pairs)}%)")
    r3 = rows[0]["collisions"]
    r5 = max(rows[1]["collisions"], 1)
    print(f"""
    TWICE AS MANY AT q=3 AS AT q=5, on {len(pairs)} pairs of substrate quantities taken from this
    thread's own closed forms. That is a real effect and a small one -- {r3} collisions against
    {rows[1]['collisions']} -- and it is much smaller than the eight coincidences this thread actually chased.

    SO THE COLLISION RATE DOES NOT EXPLAIN THE FAILURE RATE. Pairs of substrate quantities
    rarely collide even at q=3; what collided were substrate quantities against OUTSIDE
    objects -- 2^4, F4's roots, Csaszar's edges, the cubic surface's lines, the tetracode.
    The hazard is not internal arithmetic, it is the size of the space of famous small
    integers, and no amount of internal measurement bounds that.""")

    print("\n  PASS 5551 -- three more verifiers, and the guard\n")
    print("""    Patched, same one-line fix as SP43's: os.chdir to the script's own
    directory before opening JSONs by bare filename.

      archive/dirs/CE2_OUTER_TWIST_TO_WEIL_BRIDGE_BUNDLE_v01/verify_bridge.py
      archive/dirs/SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25/verify_bundle.py
      archive/dirs/WE6_to_PSp43_WORD_LIFT_BUNDLE_v01 (1)/verify_word_lift.py

    ALL THREE ARE ARCHIVED COPIES, so the live cost was only SP43's -- but an archived
    verifier that cannot run is an archived result that cannot be rechecked, which is worse
    than no archive.

    THE GUARD WIRING IS NOT DONE. check_rediscovery reads RESULTS_INDEX.md and would need a
    second lookup table plus a decision about which grammar owns a collision. That is a real
    change to a self-tested guard and it is not something to bolt on at the end of a pass;
    recorded as open rather than half-done.""")

    out = {
        "boundary": ("Pass 5548 compares token SETS between two indexes with deliberately "
                     "different grammars; disjointness measures the grammars as much as the "
                     "corpora. Pass 5550's collision rate is over 12 hand-chosen closed "
                     "forms from this thread, not a corpus census. Pass 5551 patches three "
                     "ARCHIVED verifiers and does NOT wire the certificate index into "
                     "check_rediscovery"),
        "pass_5548": {"results_index_tokens": len(rtoks),
                      "certificate_tokens": len(ctoks),
                      "shared": len(rtoks & ctoks),
                      "certificate_only": len(ctoks - rtoks),
                      "reading": ("the certificates were an unindexed half of the corpus, "
                                  "not a duplicate view; but disjointness at this scale "
                                  "means different grammars, not 132,239 new results")},
        "pass_5549": {"alpha_18_indexed": has18, "alpha_exact_7_indexed": hasexact7,
                      "my_error": "queried alpha_exact@18; the token is alpha@18",
                      "limit": ("the index cannot know that two passes calling one quantity "
                                "by two key names mean the same thing")},
        "pass_5550": {"rows": rows, "pairs": len(pairs), "quantities": names,
                      "ratio_q3_to_q5": round(r3 / r5, 1),
                      "conclusion": ("internal collisions are rare even at q=3; the eight "
                                     "coincidences chased were substrate quantities against "
                                     "OUTSIDE objects, which no internal measurement bounds")},
        "pass_5551": {"patched": ["CE2_OUTER_TWIST_TO_WEIL_BRIDGE_BUNDLE_v01/verify_bridge.py",
                                  "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25/verify_bundle.py",
                                  "WE6_to_PSp43_WORD_LIFT_BUNDLE_v01 (1)/verify_word_lift.py"],
                      "all_archived": True,
                      "guard_wiring": "NOT done -- needs a second lookup table and a "
                                      "grammar-precedence decision; recorded as open"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5548_5555_INDEXES_BARELY_OVERLAP.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
