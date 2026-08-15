"""Passes 5266-5267 -- a guard written this session found a rediscovery this session, in my
own work, of my own earlier work.

  5266  check_spectral_overreach.py was built at Pass 5253 out of the Pass 5228
        counterexample.  Swept over the full corpus it returns six candidates.  Two are its
        own self-test fixtures.  One is a hierarchy-spectrum sentence.  The other three are
        the finding, and they point at Passes 4795 and 4800 -- both MINE, both ~450 passes
        earlier, and between them they already contain most of what Passes 5226 through
        5263 spent this session establishing.

  5267  So: what of the last twenty passes is actually new?  Subtracting honestly, and
        recording the answer whether or not it is flattering.

    THE UNCOMFORTABLE PART, stated first.  Pass 4795 found alpha(W(3,3)) = 7, noticed
    7 = q^2-q+1, and wrote down the falsifiable consequence: alpha(W(3,5)) should be 21.
    Pass 4800 computed alpha(W(3,5)) = 18 exhaustively and titled itself "the deficit law is
    false".  Pass 5226 rediscovered the 7.  Pass 5249 re-proposed q^2-q+1 as a candidate.
    Pass 5263 re-refuted it with the same number, 18.  The corpus had the whole arc already.

    py -3 analysis/w33_pass5266_5267_my_own_guard_caught_my_own_rediscovery.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# What this session claimed, against what the corpus already held. Data, not prose, so the
# verdict column cannot drift from the evidence (Pass 4923).
LEDGER = [
    {"claim": "alpha(W(3,3)) = 7", "session_pass": 5226, "prior": 4795,
     "verdict": "REDISCOVERED", "note": "Pass 4795 computed it and named q^2-q+1"},
    {"claim": "alpha(W(3,5)) = 18", "session_pass": 5262, "prior": 4800,
     "verdict": "REDISCOVERED", "note": "Pass 4800 had it exhaustively in 2,075 s"},
    {"claim": "q^2-q+1 is refuted as an equality", "session_pass": 5263, "prior": 4800,
     "verdict": "REDISCOVERED", "note": "Pass 4800's title IS this refutation"},
    {"claim": "Hoffman deficit is exactly q at odd q", "session_pass": 5228, "prior": 4800,
     "verdict": "REFUTED IN REPO ALREADY",
     "note": "true at q=3 only; Pass 4800 killed the general law with the q=5 deficit 8"},
    {"claim": "alpha(W(3,q)) = q^2+1 for q = 2, 4", "session_pass": 5247, "prior": 4800,
     "verdict": "REDISCOVERED", "note": "Pass 4800's rows carry alpha=5 and alpha=17"},
    {"claim": "polarity <=> q an odd power of 2; Sz(q) stabiliser",
     "session_pass": 5265, "prior": 4793,
     "verdict": "REDISCOVERED", "note": "caught BEFORE publishing, by corpus search"},
    # --- and what survives ---
    {"claim": "alpha(W(3,q)) = q^2+1 constructed at q = 8,16,32,64,128,256",
     "session_pass": 5247, "prior": None, "verdict": "NEW",
     "note": "Pass 4800 reached q=4; these are 2.1 billion verified pairs at q=256"},
    {"claim": "W(3,3) and Q(4,3) are cospectral with alpha 7 and 10",
     "session_pass": 5228, "prior": None, "verdict": "NEW",
     "note": "Pass 4800 has the W side only; the Q side makes it a counterexample to "
             "alpha being spectrally determined"},
    {"claim": "H(3,9)/Q(5,3) share Hoffman 28 by duality-invariance of st+1",
     "session_pass": 5248, "prior": None, "verdict": "NEW",
     "note": "a second, non-cospectral mechanism for the same split"},
    {"claim": "MILP settles alpha(W(3,5)) in 75 s where exhaustive took 2,075 s",
     "session_pass": 5262, "prior": 4800, "verdict": "NEW METHOD, OLD RESULT",
     "note": "27x faster and it scales; the number itself is Pass 4800's"},
    {"claim": "the symplectic form is determined by scanning all 63 alternating forms",
     "session_pass": 5246, "prior": None, "verdict": "NEW",
     "note": "removes a convention-assumption step that has failed five times"},
    {"claim": "19 guards self-tested; two new guards; cross-lane reconciliation",
     "session_pass": 5250, "prior": None, "verdict": "NEW", "note": ""},
]


def main() -> int:
    print("=" * 78)
    print("Passes 5266-5267 -- the guard caught me")
    print("=" * 78)

    print("\n  PASS 5266 -- what the full-corpus sweep actually returned\n")
    print("""    Six candidates over 7,113 files. Triaged by hand, because a guard that reads
    sentences produces candidates and never verdicts:

      2  scripts/check_spectral_overreach.py     its OWN self-test fixtures -- noise, and
                                                 a guard should not scan itself
      1  w33_pass4097_4104_..._rg_engine.py      "hierarchy_spectrum" prose, not a claim
                                                 about alpha -- a false positive
      1  w33_BREAKTHROUGH_alpha_q3_anomaly.py    "Hoffman NOT tight, q = 3 ANOMALY"
      2  w33_pass4800_the_deficit_law_is_false.py "refutes Pass 4795's proposal that the
                                                 Hoffman deficit at odd q equals q"

    THE LAST TWO ARE NOT FALSE POSITIVES AND THEY ARE NOT ABOUT SOMEBODY ELSE. Pass 4795
    and Pass 4800 are mine, from roughly 450 passes ago, and between them they hold:

        alpha(W(3,3)) = 7                          Pass 4795
        the observation that 7 = q^2 - q + 1       Pass 4795
        the falsifiable prediction alpha(W(3,5)) = 21   Pass 4795, stated explicitly
        alpha(W(3,5)) = 18, exhaustive, 2,075 s    Pass 4800
        "the deficit from Hoffman is exactly q is FALSE"   Pass 4800, in the title

    Every one of those was re-derived this session as though new.""")

    print("\n  PASS 5267 -- the honest subtraction\n")
    old = [r for r in LEDGER if r["verdict"].startswith(("REDISCOVERED", "REFUTED"))]
    new = [r for r in LEDGER if r["verdict"] == "NEW"]
    meth = [r for r in LEDGER if r["verdict"].startswith("NEW METHOD")]
    print(f"    {'claim':58s} {'pass':>5s} {'prior':>6s}  verdict")
    for r in LEDGER:
        pr = str(r["prior"]) if r["prior"] else "--"
        print(f"    {r['claim'][:58]:58s} {r['session_pass']:5d} {pr:>6s}  {r['verdict']}")

    print(f"""
    {len(old)} REDISCOVERED, {len(new)} NEW, {len(meth)} NEW METHOD ON AN OLD RESULT.

    THE CORRECTION THAT MATTERS. Pass 5228 wrote "the gap is exactly q" of the q=3 case. In
    context that is a statement about q=3 and is true there, but it is the exact sentence
    Pass 4800 exists to refute as a general law, and writing it without the citation invites
    the general reading. The record now says: the deficit is 3 at q=3 and 8 at q=5, it is
    not q, and Pass 4800 established that before this session began.

    WHY THE CORPUS SEARCH DID NOT CATCH IT EARLIER, which is the reusable part. I searched
    for "ovoid", for "Hoffman", for the group orders. I did not search for the NUMBER 18,
    and 18 is the result. CLAUDE.md says this in as many words -- search for the RESULT, not
    the topic -- and the one search that would have worked is the one I did not run. The
    Suzuki check at Pass 5265 DID work, and it worked precisely because I searched for 29120
    and for the order formula rather than for the word.

    AND THE GUARD FOUND IT, WHICH IS THE ONE CHEERFUL FACT HERE. check_spectral_overreach
    was built at Pass 5253 for a different purpose entirely -- to stop anyone claiming a
    spectral bound DETERMINES alpha. Pointed at the whole corpus it landed on the two files
    that made this session's arc redundant. It did not detect the rediscovery; it detected
    prose about the Hoffman bound, and the prior art was attached to it. That is what these
    tools are for: they put the adjacent file in front of you.

    WHAT SURVIVES, AND IT IS NOT NOTHING. The even-q construction reaching q=256 with 2.1
    billion pairs verified goes far past Pass 4800's q=4. The cospectral pair W(3,3)/Q(4,3)
    is a genuine counterexample to alpha being spectrally determined, and Pass 4800 has only
    the W side of it. The MILP route is 27 times faster than the exhaustive search that
    produced the same 18. The form-determination scan removes an assumption step with five
    logged failures. Those are real, and they are smaller than the session looked.""")

    out = {
        "boundary": ("This is a self-audit of THIS session's passes against prior in-repo "
                     "work. The triage of the six sweep candidates is by hand -- 2 are the "
                     "guard's own fixtures and 1 is a false positive on unrelated prose, "
                     "so the guard's precision here is 3 of 6 and that number is from one "
                     "sweep. 'NEW' means not found in the corpus by the searches described, "
                     "which is not proof of novelty -- Pass 328 measured a 21 pct uncited "
                     "collision rate and nothing here lowers it"),
        "pass_5266": {"sweep": {"files": 7113, "candidates": 6},
                      "triage": {"own_fixtures": 2, "false_positive": 1,
                                 "genuine_prior_art": 3},
                      "prior_art": {
                          "pass_4795": ["alpha(W(3,3)) = 7", "noticed 7 = q^2-q+1",
                                        "predicted alpha(W(3,5)) = 21, explicitly"],
                          "pass_4800": ["alpha(W(3,5)) = 18 exhaustive in 2075 s",
                                        "deficit-q law FALSE, in the title",
                                        "rows for q = 2,3,4,5 with alpha 5,7,17,18"]}},
        "pass_5267": {"ledger": LEDGER,
                      "rediscovered": len(old), "new": len(new),
                      "new_method_old_result": len(meth),
                      "correction": ("Pass 5228's 'the gap is exactly q' is true at q=3 "
                                     "and is NOT a general law -- Pass 4800 refuted the "
                                     "general form with the q=5 deficit of 8, before this "
                                     "session began. Cite 4800 wherever the deficit is "
                                     "discussed"),
                      "why_missed": ("searched for the topic -- ovoid, Hoffman, group "
                                     "orders -- and not for the RESULT, the number 18. "
                                     "The Suzuki check at Pass 5265 searched for 29120 and "
                                     "succeeded, which is the same lesson in the "
                                     "affirmative")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5266_5267_REDISCOVERY_AUDIT.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
