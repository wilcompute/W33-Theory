"""Passes 7098-7105 -- two of my own claims retracted, and a guard I built and then disabled.

  7098  BT820's Choi witnesses are CORRECT.  My Pass 6163 flag was a misreading.
  7099  Why I misread it: I assumed a definition instead of reading the one given.
  7100  The second error underneath the first -- I inferred absence from a truncated grep.
  7101  The forced-arithmetic guard, calibrated: 0.02% firing, and it works.
  7102  The general derived-number test: 13.91% firing.  Built, measured, DISABLED.
  7103  Why a guard that fires on one file in seven is worse than no guard.
  7104  The self-containment check, which does work, and what it caught.
  7105  Scope.

    py -3 analysis/w33_pass7098_7105_two_self_corrections.py
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
    print("Passes 7098-7105 -- two self-corrections and one disabled guard")
    print("=" * 78)

    print("\n  PASS 7098-7099 -- BT820's Choi witnesses are correct\n")
    import numpy as np
    w = np.exp(2j * np.pi / 3)
    F3 = np.array([[1, 1, 1], [1, w, w ** 2], [1, w ** 2, w ** 4]]) / np.sqrt(3)
    X = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
    Z = np.diag([1, w, w ** 2])
    rows = []
    for n, U in (("F3", F3), ("X", X), ("Z", Z)):
        tr = complex(np.trace(U))
        rows.append((n, tr, abs(tr) / 3))
        print(f"    V({n:2s}) = |Tr U|/3 = {abs(tr) / 3:.6f}      Tr U = {tr:+.4f}")
    print("""
    I FLAGGED THESE AT PASS 6163 as suspicious: 1/3 is exactly 1/d, the separable value for
    a qutrit, and two witnesses were exactly 0.0. That reasoning presumed the witness was a
    CHOI-STATE FIDELITY, compared against a separable threshold.

    IT IS NOT. The producer states the definition on its own line 15:

        V(U) = |Tr U| / 3

    a normalised trace, not a fidelity, with no separable threshold anywhere near it. And
    under that definition every value is exactly right: Tr(F3) = i, so V(F3) = 1/3; X and Z
    are TRACELESS, so their witnesses vanish identically. The two zeros I read as missing
    computations are the correct answers, and 1/3 coinciding with 1/d is a coincidence of
    two unrelated normalisations by the same q.

    THE FLAG IS RETRACTED. Nothing in BT820's witness layer is wrong.""")

    print("\n  PASS 7100 -- the error underneath the error\n")
    print("""    I ALSO REPORTED THAT NO PRODUCER EXISTED. It does: analysis/bt820_self_
    entanglement_protocol.py, computing exactly these witnesses. My grep was
    case-insensitive and would have matched; what defeated it was `head -6` on the output.
    The alphabetically-earlier matches were argparse `choices=` in unrelated files, and the
    real hits sat below the cut.

    SO THE FIRST ERROR WAS ONLY POSSIBLE BECAUSE OF THE SECOND. Had I read the producer, the
    definition on line 15 would have prevented the flag. I inferred ABSENCE from a
    TRUNCATED result -- which is not a weak inference, it is an invalid one. A truncated
    search says nothing whatever about what it did not print.

    THE RULE: never conclude "does not exist" from a command whose output was cut. Re-run
    with a count, or without the cut, before the word "no" is used.""")

    print("\n  PASS 7101-7103 -- a guard built, measured, and disabled\n")
    print(f"    {'test':44s} {'fires on':>10s}  {'verdict':>10s}")
    for nm, pct, verdict in (
            ("SRG multiplicities forced by (v,k,lam,mu)", "0.02%", "KEEP"),
            ("transitivity of a claimed equivalence", "0.8%", "KEEP"),
            ("scope vs evidence coverage", "3%", "KEEP"),
            ("general derived-number (a = b+c, b*c, b-c)", "13.91%", "DISABLED")):
        print(f"    {nm:44s} {pct:>10s}  {verdict:>10s}")
    print("""
    THE GENERAL TEST WAS THE OBVIOUS GENERALISATION and it does not work. Written to catch
    any interpreted integer derivable from two others in the same file, it fires on 719 of
    5,169 certificates -- one in seven. Reading the hits explains why: `vertices = 64 is
    also middle_blocks(48) + flags(16)` is a DOCUMENTED DECOMPOSITION, the certificate
    saying what it means. The test cannot distinguish a decomposition a file is explaining
    from an encoding a file is inventing, because syntactically they are the same statement.

    A GUARD THAT FIRES ON ONE FILE IN SEVEN IS WORSE THAN NO GUARD. It is not merely
    unhelpful: it trains the reader to skip the output, which then hides the 0.02% signal
    that the narrow test does carry. So the general test is retained behind --general, off
    by default, with its measured rate written into the source beside it.

    I ONLY KNOW THIS BECAUSE I MEASURED THE FIRING RATE BEFORE SHIPPING IT. The 8/8 selftest
    passed on the general test; selftests establish that a test does what it says, never
    that what it says is worth doing.""")

    print("\n  PASS 7104 -- the check that did work\n")
    print("""    THE SELF-CONTAINMENT CHECK, wired into audit_batch.py as step 1c, asks whether a
    certificate that INTERPRETS numbers also records the parameters those numbers follow
    from. BT1645 does not, and now reports:

        BT1645_monster_moonshine_encoding.json: interprets numbers but records no
        parameters they follow from -- not self-contained, cannot be audited alone

    The same file previously passed intake as "intake clean (3 files)". That is the blind
    spot closed: the harness checked contradiction against certified values and rediscovery
    against the index, but never whether a claim carried enough to be checked at all.""")

    print("\n  PASS 7105 -- scope\n")
    print("""    TWO RETRACTIONS, both mine, neither affecting anyone else's result: BT820's
    witnesses are correct and my flag was wrong; the producer existed and my search was
    truncated. ONE GUARD KEPT (0.02%), ONE DISABLED (13.91%), ONE WIRED IN.

    NOT DONE: alpha(W(3,7)) exact, still running. Whether BT1645's underlying arithmetic is
    sound -- the self-containment flag says it cannot be audited alone, which is not a claim
    that it is wrong.""")

    out = {
        "boundary": (
            "Passes 7098-7100 RETRACT two claims of mine: BT820's Choi witnesses are "
            "correct under the definition its producer states (V(U)=|Tr U|/q, and X, Z are "
            "traceless), and the producer exists -- my report that it did not came from a "
            "truncated grep. Pass 7102 DISABLES a guard I wrote after measuring a 13.91% "
            "firing rate. No claim is made about BT1645's underlying arithmetic"),
        "pass_7098_7099": {
            "retracted": "Pass 6163's flag on bt820 choi_witnesses",
            "definition_given_in_producer": "V(U) = |Tr U| / q",
            "witnesses": {n: {"trace": f"{tr:+.6f}", "V": round(v, 10)}
                          for n, tr, v in rows},
            "why_the_zeros_are_right": "X and Z are traceless, so |Tr U| = 0 exactly",
            "why_1_3_is_not_1_over_d": (
                "Tr(F3) = i exactly, so |Tr F3|/3 = 1/3; the coincidence with the "
                "separable value 1/d is two unrelated normalisations by the same q"),
            "verdict": "BT820 witness layer is CORRECT"},
        "pass_7100": {
            "second_error": "reported no producer exists",
            "actual": "analysis/bt820_self_entanglement_protocol.py",
            "cause": ("head -6 truncated the grep; alphabetically-earlier argparse "
                      "choices= matches filled the window"),
            "rule": "never conclude absence from a command whose output was cut"},
        "pass_7101_7103": {
            "firing_rates": {"srg_forced": "0.02%", "transitivity": "0.8%",
                             "scope_vs_evidence": "3%", "general_derived": "13.91%"},
            "general_test_hits": "719 of 5169 certificates",
            "why_disabled": (
                "cannot distinguish a documented decomposition from an invented encoding "
                "-- syntactically identical"),
            "disposition": "retained behind --general, off by default",
            "lesson": ("a selftest establishes that a test does what it says, never that "
                       "what it says is worth doing; measure the firing rate before "
                       "shipping a guard")},
        "pass_7104": {
            "check": "self-containment, audit_batch step 1c",
            "caught": "BT1645_monster_moonshine_encoding.json",
            "previously": "passed intake as 'intake clean (3 files)'",
            "blind_spot_closed": ("the harness checked contradiction and rediscovery but "
                                  "never whether a claim carried enough to be checked")},
        "pass_7105": {"not_done": ["alpha(W(3,7)) exact -- running",
                                   "whether BT1645's arithmetic is sound"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS7098_7105_TWO_SELF_CORRECTIONS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
