"""Passes 9701-9724 -- two corrections to my own last pass, and the invariant that survives.

  9701  CORRECTION 1: the random baseline was 48, not 24. The control predicts 48.
  9702  Why I got it wrong: a totally singular subspace is not drawn from the whole space.
  9703  CORRECTION 2: "V_2 is one of the nine Type II codes" is VACUOUS as stated.
  9704  Witt's theorem: every maximal totally singular subspace is O(q)-equivalent.
  9705  So no property of the quadratic form alone can pick one out.
  9706  WHAT SURVIVES, AND IS STRONGER: type is Co0-invariant, and Co0 is tiny inside O(q).
  9707  V_2 holds ZERO type-4 classes where a generic generator holds 48. Controlled.
  9708  AND THE LENGTH-8 RESULT STANDS -- for a reason that says why 24 fails.
  9709  The open question, restated so it is actually well-posed.
  9710  Scope.

WHY THIS PASS EXISTS. Pass 9601-9624 reported that V_2 holds no type-4 classes "against 24
expected at random" and described V_2 as "a Type II code of length 24, one of the nine".
Running the obvious control -- take random maximal totally singular subspaces and count --
returned 48, 48, 48, 48, 60, 72. The control disagreed with my stated baseline, which is
how both errors surfaced.

    py -3 analysis/w33_pass9701_9724_two_corrections_and_a_sharper_invariant.py
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

N_ALL = 2 ** 24 - 1
N_SING = 8390655
N_TYPE4 = 98280
NZ = 4095
CONTROL = [60, 48, 48, 48, 48, 72]
CO0 = 8315553613086720000


def o_plus_order(n, q=2):
    o = 2 * q ** (n * (n - 1)) * (q ** n - 1)
    for i in range(1, n):
        o *= q ** (2 * i) - 1
    return o


def main() -> int:
    print("=" * 78)
    print("Passes 9701-9724 -- two corrections, and the invariant that survives")
    print("=" * 78)

    print("\n  PASS 9701-9702 -- CORRECTION 1: the baseline\n")
    wrong = NZ * N_TYPE4 / N_ALL
    right = NZ * N_TYPE4 / N_SING
    print(f"      published baseline : {NZ} * {N_TYPE4} / {N_ALL} = {wrong:.1f}")
    print(f"      correct baseline   : {NZ} * {N_TYPE4} / {N_SING} = {right:.1f}")
    print(f"      control returned   : {CONTROL}, mode {max(set(CONTROL), key=CONTROL.count)}")
    print(f"""
    V_2 is TOTALLY SINGULAR, so its 4095 nonzero classes are drawn from the {N_SING}
    singular classes, not from all {N_ALL}. Type-4 classes are denser inside the singular
    locus than in the whole space, and the correct baseline is {right:.0f}.

    THE CORRECTED BASELINE PREDICTS THE CONTROL AND THE PUBLISHED ONE DOES NOT. That is what
    exposed the error: four of six random generators returned exactly 48.

    The finding is unchanged in direction and SHARPER in size -- V_2 holds 0 where 48 is
    expected, not 0 where 24 is expected.""")

    print("\n  PASS 9703-9705 -- CORRECTION 2: 'one of the nine' is vacuous\n")
    Oq = o_plus_order(12)
    print(f"      |O_24^+(2)| = {Oq:.3e}")
    print(f"      |Co0|       = {CO0:.3e}")
    print(f"      index       = {Oq / CO0:.3e}")
    print("""
    Pass 9601-9624 called V_2 "a Type II code of length 24, one of the nine". As stated that
    says nothing. By WITT'S EXTENSION THEOREM the orthogonal group is transitive on totally
    singular subspaces of a given dimension, so EVERY maximal totally singular 12-space of
    Lambda/2Lambda is equivalent to every other under O(q). Pick any frame and any of them
    becomes a doubly-even self-dual code; pick another frame and it becomes a different one.

    The nine-fold classification is of CO-ORDINATIZED codes -- codes up to monomial
    equivalence -- not of abstract subspaces of a quadratic space. So "which of the nine" is
    not a property of V_2 at all. It is a property of the pair (V_2, frame).

    That also disposes of the hedge I wrote. I said the identification "needs a coordinate
    frame that Leech/2Leech does not canonically have", as though a frame were merely
    missing. It is worse than missing: without one the question is not well-posed.""")

    print("\n  PASS 9706-9707 -- what survives, and why it is stronger\n")
    print(f"""    Co0 sits inside O(q) with index about {Oq / CO0:.1e}. The quadratic form is
    preserved by all of O(q); the LEECH TYPE function is preserved only by Co0. So type is a
    vastly finer invariant than the form, and a type statement is exactly the kind of thing
    that CAN distinguish subspaces the form cannot.

        V_2 holds 0 type-4 classes.   A generic generator holds 48.

    Controlled directly: six random maximal totally singular subspaces gave {CONTROL}.
    Zero is not what a generator does. That is the real result, it is Co0-invariant, and it
    is untouched by either correction -- indeed the corrected baseline doubles the gap.""")

    print("\n  PASS 9708 -- and the length-8 result stands, for a reason that explains 24\n")
    print("""    The same objection would seem to sink the E8 claim, which identified V_2 there
    as the extended Hamming code [8,4,4]. It does not, and the reason is precisely the one
    given when the claim was made: at length 8 there is exactly ONE doubly-even self-dual
    code. Every frame gives the same answer, so the identification is FRAME-INDEPENDENT.

    So the two cases separate cleanly, and the separation is the content:

        length 8   classification is a singleton -> frame-independent -> IDENTIFIED
        length 24  nine classes -> frame-dependent -> NOT a property of the subspace

    The E8 loop E8 -> filtration -> [8,4,4] -> Construction A -> E8 is unaffected.""")

    print("\n  PASS 9709 -- the open question, restated so it is well-posed\n")
    print("""    The wrong question was "which of the nine Type II codes is V_2".
    The right questions are:

      * How many maximal totally singular subspaces of Lambda/2Lambda contain NO type-4
        class? The control shows they are rare; the count is not known here.
      * Is Co0 transitive on them? If it is, "the type-4-free generator" is a single
        Co0-orbit and V_2 is canonically that object.
      * Does a type-4-free generator have a distinguished frame of its own? Every one of
        V_2's 4095 nonzero classes is type 8, and a type-8 class IS a frame -- 24 mutually
        orthogonal norm-8 vectors up to sign. So V_2 supplies 4095 frames intrinsically.
        Whether they agree, and what code V_2 becomes in one of its OWN frames, is the
        well-posed version of the question I asked badly.""")

    out = {
        "boundary": (
            "TWO CORRECTIONS to Pass 9601-9624. (1) The random baseline for type-4 classes in "
            "a totally singular 12-space is 48, not 24: such a subspace draws from the "
            "8390655 SINGULAR classes, not all 16777215. Six random generators returned "
            "60,48,48,48,48,72 -- the corrected baseline predicts the control, the published "
            "one does not. (2) 'V_2 is one of the nine Type II codes' is VACUOUS: by Witt, "
            "O(q) is transitive on maximal totally singular subspaces, so every generator is, "
            "under some frame. WHAT SURVIVES AND IS STRONGER: the type function is "
            "Co0-invariant and Co0 has index ~2e64 in O(q), so type is far finer than the "
            "form -- and V_2 holds ZERO type-4 classes where a generic generator holds 48. "
            "The length-8 identification as [8,4,4] STANDS, because uniqueness there makes it "
            "frame-independent"),
        "correction_1_baseline": {
            "published": round(wrong, 1), "correct": round(right, 1),
            "why": ("V_2 is totally singular, so its classes are drawn from the singular "
                    "locus, where type-4 classes are denser"),
            "control": CONTROL, "control_mode": max(set(CONTROL), key=CONTROL.count),
            "how_it_surfaced": ("the control disagreed with the published baseline; the "
                                "corrected one predicts it"),
            "effect_on_finding": "unchanged in direction, and the gap doubles"},
        "correction_2_vacuous_claim": {
            "claim": "V_2 is a Type II code of length 24, one of the nine",
            "why_vacuous": ("Witt's extension theorem makes O(q) transitive on maximal "
                            "totally singular subspaces, so EVERY generator becomes a "
                            "doubly-even self-dual code under a suitable frame"),
            "the_nine_classify": "co-ordinatized codes up to monomial equivalence",
            "so": "'which of the nine' is a property of the pair (V_2, frame), not of V_2",
            "also_corrects": ("the hedge that a frame was merely 'missing'. Without one the "
                              "question is not well-posed at all")},
        "what_survives": {
            "invariant": "the Leech type function, preserved by Co0 and not by O(q)",
            "O_24_plus_2_order": Oq, "Co0_order": CO0, "index": Oq / CO0,
            "result": "V_2 holds 0 type-4 classes; a generic generator holds 48",
            "status": "Co0-invariant, controlled, and untouched by both corrections"},
        "length_8_stands": {
            "why": ("at length 8 there is exactly ONE doubly-even self-dual code, so every "
                    "frame gives the same answer and the identification is frame-INDEPENDENT"),
            "separation": {"length_8": "singleton -> frame-independent -> IDENTIFIED",
                           "length_24": "nine classes -> frame-dependent -> not a property"},
            "loop_unaffected": "E8 -> filtration -> [8,4,4] -> Construction A -> E8"},
        "well_posed_questions": [
            "how many maximal totally singular subspaces of Lambda/2Lambda are type-4-free",
            "whether Co0 is transitive on them, which would make V_2 canonical",
            ("what code V_2 becomes in one of its OWN frames -- every one of its 4095 nonzero "
             "classes is type 8, and a type-8 class IS a frame, so V_2 supplies 4095 frames "
             "intrinsically")],
    }
    fp = ROOT / "data" / "PART_W33_PASS9701_9724_CORRECTIONS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
