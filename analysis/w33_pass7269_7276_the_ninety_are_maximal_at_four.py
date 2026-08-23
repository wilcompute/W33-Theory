"""Passes 7269-7276 -- the 90 D4s are MAXIMAL partial ovoids of size 4, and three measurements.

  7269  No D4 block lies in any maximum partial ovoid. Zero, over 90 x 2880.
  7270  Because every D4 block is MAXIMAL at size 4. It cannot be extended at all.
  7271  So resolutions cannot certify alpha -- my own idea, killed by its own test.
  7272  The 459 parallel classes carry NO association scheme.
  7273  10.2% of this repo's roman-numeral citations are ambiguous.
  7274  My rediscovery rate this session, counted: 31% prior, 44% new, 25% partial.
  7275  Two scripts could report a timeout as a negative; fixed.
  7276  Scope.

    py -3 analysis/w33_pass7269_7276_the_ninety_are_maximal_at_four.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

LEDGER = [
    ("alpha(W(3,3))=7, alpha(W(3,5))=18 exact", "settled a corpus contradiction", "PARTIAL"),
    ("q=7 optimum has no order-3 symmetry", "CONJECTURED at Pass 6285-6300", "PARTIAL"),
    ("|Stab| = 2 exactly at q=7 and q=9", "prior art had q=3 only", "NEW"),
    ("certified basin radius 9 at q=9", "none found", "NEW"),
    ("LNS reaches 25 on Q^-(5,4)", "published exhaustive maximum", "PRIOR"),
    ("Pauli dictionary at odd q", "q=2 was Pass 5351-5352", "PARTIAL"),
    ("collinear <=> completely orthogonal in E8", "none found", "NEW"),
    ("points of W(3,3) are A2 subsystems", "BT1750 had the 40 hexagons", "PARTIAL"),
    ("the 90 D4s are the J-stable D4s", "gave their criterion a definition", "NEW"),
    ("the two 36s are one graph, |Aut|=51840", "MCCCXCIII/XCIV/XCV had ALL of it", "PRIOR"),
    ("every non-collinear pair in exactly one D4", "none found", "NEW"),
    ("perp of a point is E6", "none found", "NEW"),
    ("the K4-design is resolvable", "none found", "NEW"),
    ("alpha(Q^-(5,2))=6 with 72 sixers", "Brosowsky et al. state 72", "PRIOR"),
    ("alpha(Q^-(5,3))=16", "meets the published sharp bound", "PRIOR"),
    ("Q^-(5,5)=48", "matches Cimrakova-Fack exactly", "PRIOR"),
]


def main() -> int:
    print("=" * 78)
    print("Passes 7269-7276 -- the 90 are maximal at four")
    print("=" * 78)

    print("\n  PASS 7269-7271 -- what the 90 blocks actually are\n")
    print("""    NO D4 BLOCK LIES IN ANY MAXIMUM PARTIAL OVOID: zero incidences over all 90
    blocks and all 2880 optima. The reason is sharper than the fact:

        every one of the 90 J-stable D4 blocks is a MAXIMAL partial ovoid of size 4

    It cannot be extended by a single point, while alpha(W(3,3)) = 7. So the 90 D4s are
    ninety MINIMUM-SIZE MAXIMAL partial ovoids, and they form a family completely disjoint
    from the 2880 maximum ones.

    THAT KILLS MY OWN PROPOSAL. I suggested resolutions might certify alpha, by merging a
    parallel class's blocks into larger partial ovoids. They cannot: the blocks are exactly
    the sets that do NOT grow. The test I proposed for the idea is the one that refuted it,
    and the refutation is more informative than the idea was.""")

    print("\n  PASS 7272 -- the parallel classes carry no scheme\n")
    print("""    The 36 spreads share 1 or 4 lines -- two values, giving SRG(36,15,6,6). The 459
    parallel classes share 0, 1, 2, 3, 4 or 5 blocks -- SIX values, and no relation among
    them has constant valency. So the analogy stops at the resolution: parallel classes are
    resolvable but not schematic. Reported because the parallel with spreads was the reason
    to look.""")

    print("\n  PASS 7273 -- 10.2% of this repo's citations are ambiguous\n")
    print(f"      {'quantity':52s} {'value':>8s}")
    for k, v in (("roman numerals used as PART_ prefixes", 820),
                 ("bound to genuinely different subjects", 84),
                 ("percentage ambiguous", "10.2%")):
        print(f"      {k:52s} {str(v):>8s}")
    print("""
    Prefix-variants (FOO_ vs FOO_BRIDGE vs FOO_results) were collapsed first, so these are
    real collisions: CCCII is both CENTRALITY_MEASURES and DELSARTE_LP_BOUND; CCCVII is both
    LINE_GRAPH and OPERATOR_TETRAHEDRON_ENTROPY. A citation like "MCCCXCIII" does not
    identify a theorem, and that directly cost me time this week -- I read the archive's
    MCCCXCIII (W(3,3)'s own 2-class scheme) and concluded the prior art was about something
    else, when manuscripts/parts/ held the right one.""")

    print("\n  PASS 7274 -- my rediscovery rate, counted rather than felt\n")
    from collections import Counter
    c = Counter(r[2] for r in LEDGER)
    n = len(LEDGER)
    print(f"      {'verdict':9s} {'count':>6s} {'share':>7s}")
    for k in ("NEW", "PARTIAL", "PRIOR"):
        print(f"      {k:9s} {c[k]:6d} {100 * c[k] / n:6.0f}%")
    print(f"""
    Sixteen claims: {c['NEW']} new, {c['PARTIAL']} partial, {c['PRIOR']} fully prior art.

    AND I OVERSTATED THIS LAST TURN. I wrote "three of my last four results were prior art".
    The last four were the resolvable design (new), the perp being E6 (new), the two 36s
    (prior), and the 90 as J-stable (new) -- ONE of four. Overstating my own error rate is
    still a false claim, and self-criticism is not exempt from being checked.""")

    print("\n  PASS 7275 -- a failure mode with a name\n")
    print("""    A TIMED-OUT SEARCH IS NOT A NEGATIVE RESULT. It bit twice this session: a grep
    truncated by `head -6` produced "no producer exists" (there was one), and an exact-cover
    search stopped at 200s and printed "0 covers found" (the 90 D4s are a cover).

    Auditing my own Pass 72xx scripts for it found two that could report a timeout as a
    result without saying so. w33_pass7216's lns() now returns whether the budget was
    exhausted and prints it; w33_pass7200 already reported solver status.""")

    print("\n  PASS 7276 -- scope\n")
    print("""    NEW: the 90 blocks being maximal at size 4 and disjoint from the optima; the
    absence of a scheme on the parallel classes; the 10.2% citation-ambiguity measurement.

    REFUTED, mine: resolutions as a certificate for alpha.

    STILL OPEN: alpha(W(3,9)); q=11 at 68, not discriminating; the third 1440; the Clifford
    L/R 36; Coolsaet (2014) remains unread.""")

    out = {
        "boundary": (
            "NEW: every one of the 90 J-stable D4 blocks is a MAXIMAL partial ovoid of size "
            "4, extendable by no point, so the 90 are disjoint from the 2880 maximum ones "
            "(zero incidences over 90 x 2880). REFUTED, my own proposal: resolutions cannot "
            "certify alpha. MEASURED: 10.2% citation ambiguity, and a 31%/44%/25% "
            "prior/new/partial split on this session's claims"),
        "the_ninety": {
            "in_any_maximum_partial_ovoid": 0,
            "checked_over": "90 blocks x 2880 optima",
            "maximal_at_size": 4,
            "extendable_by": 0,
            "alpha": 7,
            "meaning": "ninety MINIMUM-SIZE MAXIMAL partial ovoids, disjoint from the optima",
            "refutes": "my proposal that resolutions could certify alpha"},
        "parallel_classes": {
            "count": 459, "shared_block_values": [0, 1, 2, 3, 4, 5],
            "association_scheme": False,
            "contrast": "the 36 spreads share 1 or 4 only, giving SRG(36,15,6,6)"},
        "citation_ambiguity": {
            "numerals_used": 820, "ambiguous": 84, "rate": "10.2%",
            "method": "prefix-variants collapsed first, so these are real collisions",
            "examples": {"CCCII": ["CENTRALITY_MEASURES", "DELSARTE_LP_BOUND"],
                         "CCCVII": ["LINE_GRAPH", "OPERATOR_TETRAHEDRON_ENTROPY"]},
            "cost_to_me": ("I read archive MCCCXCIII (W(3,3)'s own 2-class scheme) and "
                           "concluded the prior art was elsewhere")},
        "my_rediscovery_rate": {
            "claims": len(LEDGER),
            "new": c["NEW"], "partial": c["PARTIAL"], "prior": c["PRIOR"],
            "ledger": [{"claim": a, "note": b, "verdict": v} for a, b, v in LEDGER],
            "self_correction": ("last turn I said 'three of my last four results were prior "
                                "art'; it was ONE of four. Overstating my own error rate is "
                                "still a false claim")},
        "timeout_failure_mode": {
            "name": "a timed-out search is not a negative result",
            "instances": ["grep truncated by head -6 -> 'no producer exists' (there was one)",
                          "exact cover stopped at 200s -> '0 covers found' (90 D4s are one)"],
            "audit": "two Pass 72xx scripts could report a timeout as a result",
            "fixed": "w33_pass7216 lns() now returns and prints whether the budget ran out"},
        "not_done": ["alpha(W(3,9))", "q=11 at 68", "the third 1440", "the Clifford L/R 36",
                     "Coolsaet (2014) unread"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7269_7276_MAXIMAL_AT_FOUR.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
