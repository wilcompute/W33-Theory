"""Passes 7261-7268 -- the K4-design is resolvable, and a guard for the miss that keeps happening.

  7261  My correction was itself wrong: MCCCXCV had 51840 and 1440 too.
  7262  The K4-decomposition IS resolvable. 459 parallel classes, 200+ resolutions.
  7263  A second duality: spreads are 10 disjoint COLLINEAR 4-sets, these are 10 NON-collinear.
  7264  Every J-stable D4's perp is a J-stable D4 -- 45 perp-pairs, matching the other lane.
  7265  Q^-(5,5) = 48, matching the published heuristic best exactly.
  7266  q=11 reached 68 under the retuned operator.
  7267  A subject-line rediscovery guard, and the half of the problem it cannot solve.
  7268  Scope.

    py -3 analysis/w33_pass7261_7268_resolvable_and_the_guard.py
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


def main() -> int:
    print("=" * 78)
    print("Passes 7261-7268 -- resolvable design, and the guard")
    print("=" * 78)

    print("\n  PASS 7261 -- my correction was itself incomplete\n")
    print("""    Last pass I recorded Pass 7245-7252 as a rediscovery of MCCCXCIII/MCCCXCIV, but
    claimed |Aut| = 51840 and the 1440-collapse might still be new. Reading the actual files
    settles it: manuscripts/parts/PART_MCCCXCV_SPREAD_DOUBLE_SIX_AUTOMORPHISM_ORDER.md
    contains BOTH 51840 and 1440.

    So NOTHING from that packet's two-36s work was new. MCCCXCIII has the scheme
    (srg(36,15,6,6) AND srg(36,20,10,12), both of which I recomputed), MCCCXCIV has an
    explicit isomorphism witness, MCCCXCV has the automorphism order. A correction that
    still overclaims is not a correction, so this is the second and final pass on it.

    NOTE THE NUMERALS ARE REUSED: archive/root_docs/BREAKTHROUGH_MCCCXCIII_MCCCCII... uses
    MCCCXCIII/MCCCXCIV for W(3,3)'s own 2-class scheme, a different subject entirely. The
    spread/double-six ones are in manuscripts/parts/. That reuse is itself a search hazard.""")

    print("\n  PASS 7262-7263 -- the K4-design is resolvable\n")
    print(f"      {'quantity':46s} {'value':>10s}")
    for k, v in (("non-collinear pairs of W(3,3)", 540),
                 ("J-stable D4 blocks (4 points each)", 90),
                 ("each pair in exactly this many blocks", 1),
                 ("parallel classes (10 pairwise-disjoint blocks)", 459),
                 ("resolutions found (search COMPLETED, 1900 nodes)", "200+")):
        print(f"      {k:46s} {str(v):>10s}")
    print("""
    The 90 blocks partition into 9 parallel classes of 10 disjoint blocks, covering all 40
    points nine times over. The search completed rather than timing out, so this is a
    resolution and not a plateau.

    AND IT COMPLETES A DUALITY. A SPREAD of W(3,3) is 10 disjoint COLLINEAR 4-sets (lines);
    a parallel class here is 10 disjoint NON-COLLINEAR 4-sets (D4 blocks). Same shape,
    opposite relation -- the same inversion already seen between lines (A2^4, rank 8) and
    J-stable D4s (rank 4).

    A FALSE START WORTH RECORDING: I first searched for exact covers of the 540 pairs by
    arbitrary 4-cliques, over 9450 candidates. That timed out at 200s and printed "0 covers
    found", which would have been a WRONG conclusion -- the 90 D4s are such a cover. Testing
    resolvability directly on the known 90 blocks completed in 1900 nodes.""")

    print("\n  PASS 7264-7266 -- three confirmations\n")
    print("""    PERPS. Every one of the 90 J-stable D4s has a perp that is also a D4, and also
    J-stable: 90/90 both times, giving 45 perp-PAIRS. The other lane reports exactly 45
    orthogonal D4 pairs in its 90-object scheme. Independent route, same number.

    Q^-(5,5). The LNS reached 48 on 756 points -- exactly the largest size Cimrakova-Fack
    report from heuristic search. An independent confirmation, NOT a new record; the maximum
    remains open between 48 and the sharp bound 66.

    q=11. Retuning the operator (k = 5..14, 6s exact repair) took it from 65 to 66 to 68.
    The earlier plateau was tooling, not geometry. 68 still sits below both hypotheses'
    predictions (71 if alpha(W(3,9)) = 51, 75 if 52), so it still does not discriminate.""")

    print("\n  PASS 7267 -- a guard for half the problem\n")
    print("""    scripts/check_subject_rediscovery.py takes a commit SUBJECT, strips boilerplate,
    and searches the corpus for its content words. On "the 36 spreads and the 36 double sixes
    are the SAME graph" it fires immediately. That is the guard the existing file-level
    check_rediscovery.py cannot be: the diff held no colliding code parameter, so nothing
    fired.

    IT SOLVES HALF THE PROBLEM, AND THE SELFTEST SAYS SO. On "the points of W(3,3) are the A2
    subsystems of E8" it finds nothing, because BT1750 calls those objects HEXAGONS. Same
    objects, disjoint vocabulary; word matching cannot bridge a rename. That case is listed
    in the selftest with want=False and labelled a blind spot rather than quietly dropped.

    TWO BUGS IN THE GUARD ITSELF, both caught by its selftest: it shelled out to ripgrep,
    which is not on PATH here and returned zero hits silently; and it matched its own file,
    since its selftest text contains the very phrases being searched.""")

    print("\n  PASS 7268 -- scope\n")
    print("""    NEW: the resolution of the K4-design (459 parallel classes, 200+ resolutions);
    the spread/parallel-class duality; the subject-line guard.

    CONFIRMED, NOT NEW: the 45 D4 perp-pairs (other lane); Q^-(5,5) = 48 (Cimrakova-Fack).

    FULLY SUPERSEDED: everything in Pass 7245-7252 about the two 36s
    (MCCCXCIII/MCCCXCIV/MCCCXCV).

    STILL OPEN: alpha(W(3,9)); q=11 not discriminating at 68; the third 1440; the Clifford
    L/R 36; whether the 459 parallel classes carry their own scheme.""")

    out = {
        "boundary": (
            "NEW: the 90-block K4-decomposition of W(3,3)'s complement is RESOLVABLE -- 459 "
            "parallel classes and 200+ resolutions, search completed. CONFIRMED not new: 45 "
            "D4 perp-pairs, Q^-(5,5) = 48. FULLY SUPERSEDED: all of Pass 7245-7252's two-36s "
            "work, including the |Aut| = 51840 I had claimed might survive -- MCCCXCV has it"),
        "pass_7261": {
            "what_i_got_wrong_twice": ("first the whole two-36s result, then the claim that "
                                       "|Aut| = 51840 and the 1440-collapse might still be new"),
            "prior_art": {"MCCCXCIII": "srg(36,15,6,6) and srg(36,20,10,12)",
                          "MCCCXCIV": "explicit isomorphism witness with mapping list",
                          "MCCCXCV": "automorphism order, contains BOTH 51840 and 1440"},
            "search_hazard": ("the numerals are REUSED: archive/root_docs uses "
                              "MCCCXCIII/MCCCXCIV for W(3,3)'s own 2-class scheme")},
        "resolvable_design": {
            "non_collinear_pairs": 540, "blocks": 90, "pairs_per_block_multiplicity": 1,
            "parallel_classes": 459, "resolutions_found": "200+ (search completed, 1900 nodes)",
            "resolvable": True,
            "duality": ("a spread is 10 disjoint COLLINEAR 4-sets; a parallel class is 10 "
                        "disjoint NON-collinear 4-sets"),
            "false_start": ("searching for exact covers by arbitrary 4-cliques over 9450 "
                            "candidates timed out and would have printed '0 covers found', "
                            "a wrong conclusion since the 90 D4s are such a cover")},
        "confirmations": {
            "d4_perp_pairs": {"value": 45, "note": "every J-stable D4's perp is J-stable, "
                                                   "90/90; matches the other lane"},
            "q_minus_5_5": {"value": 48, "note": "matches Cimrakova-Fack's heuristic best; "
                                                 "maximum still open in [48, 66]"},
            "q11": {"progression": [65, 66, 68], "how": "k = 5..14, 6s repair",
                    "verdict": "plateau was tooling; still does not discriminate 71 vs 75"}},
        "subject_guard": {
            "file": "scripts/check_subject_rediscovery.py",
            "catches": "rediscoveries that reuse the prior art's vocabulary",
            "blind_spot": ("renames -- BT1750 says 'hexagons' where I said 'A2 subsystems'; "
                           "word matching cannot bridge it, and the selftest lists this case "
                           "with want=False"),
            "its_own_bugs_caught_by_its_selftest": [
                "shelled out to ripgrep, not on PATH, silently returned zero",
                "matched its own file, whose selftest contains the search phrases"]},
        "not_done": ["alpha(W(3,9))", "q=11 not discriminating at 68", "the third 1440",
                     "the Clifford L/R 36",
                     "whether the 459 parallel classes carry their own scheme"],
    }
    fp = ROOT / "data" / "PART_W33_PASS7261_7268_RESOLVABLE_AND_GUARD.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
