"""Passes 9861-9884 -- the frame-relation structure, and two findings that died under sampling.

  9861  V_2's 4095 classes are all frames, and frames can be compared. What is the relation?
  9862  At 14 classes: exactly TWO relation types. Clean.
  9863  At 14 classes: the relation depends only on the SUM class. 25 shared sums, 0 clashes.
  9864  Both looked like structure. Both are FALSE.
  9865  At 34 classes: THREE relation types, not two.
  9866  At 34 classes: 6 sum classes carry disagreeing relations. The sum law is refuted.
  9867  What actually survives.
  9868  The methodological point, which is the real content of this pass.
  9869  Scope.

WHY THIS IS WRITTEN UP AT ALL. Nothing here is a breakthrough. Two clean-looking findings
were obtained, believed, and then killed by increasing the sample from 14 to 34 -- before
publication rather than after. The pass exists so the killed versions are on record next to
the reason they died.

    py -3 analysis/w33_pass9861_9884_two_findings_that_did_not_survive.py
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

SMALL = {"classes": 14, "pairs": 91, "relation_types": 2,
         "shared_sum_classes": 25, "disagreements": 0}
LARGE = {"classes": 34, "pairs": 561, "relation_types": 3,
         "shared_sum_classes": 102, "disagreements": 6}
TYPES = [({0: 288, 2: 256, 4: 32}, 247), ({0: 264, 2: 288, 4: 24}, 194),
         ({0: 480, 4: 96}, 120)]


def main() -> int:
    print("=" * 78)
    print("Passes 9861-9884 -- two findings that did not survive sampling")
    print("=" * 78)

    print("\n  PASS 9861 -- the question\n")
    print("""    Every one of V_2's 4095 nonzero classes is type 8, and a type-8 class IS a
    frame: 24 mutually orthogonal antipodal pairs of norm-8 vectors. So V_2 is a group of
    4096 frames, and any two of them can be compared by the multiset of |inner products|
    between their 24 representatives -- 576 numbers per pair.""")

    print("\n  PASS 9862-9863 -- what 14 classes said\n")
    for k, v in SMALL.items():
        print(f"      {k:24s} {v}")
    print("""
    Two relation types, cleanly separated -- one with |ip| in {0,4} only, one with {0,2,4}.
    And the relation appeared to depend ONLY on the sum class: 25 sum classes were reached
    by more than one pair, and not one of them disagreed. A group carrying a two-valued
    function of the difference is a real structure, so this looked like a finding.""")

    print("\n  PASS 9864-9866 -- what 34 classes did to it\n")
    for k, v in LARGE.items():
        print(f"      {k:24s} {v}")
    print("\n      relation types actually present:\n")
    for d, n in TYPES:
        print(f"        {str(d):28s} x {n}")
    print("""
    BOTH FINDINGS ARE FALSE.

      "two relation types" -- there are at least THREE. The third type,
      {0:264, 2:288, 4:24}, accounts for 35% of pairs at n=34 and simply did not occur in
      the first 91 pairs.

      "depends only on the sum class" -- REFUTED. Six sum classes carry two different
      relations. At n=14 there were 25 shared sums and zero clashes; at n=34 there are 102
      shared sums and six clashes. The clean result was an artifact of not having enough
      pairs to hit a counterexample.""")

    print("\n  PASS 9867 -- what survives\n")
    print("""    Three things, all still checked:

      * V_2's 4095 nonzero classes are all frames. That rests on the type-4 census and the
        vanishing of q, not on any of the above.
      * Every observed relation has |ip| contained in {0, 2, 4}. No pair produced any other
        value across 561 comparisons.
      * The 24-number profile of a frame against a SINGLE representative of another class
        determines the full 576-pair relation. Verified across the sample, and it is what
        makes the relation cheap to evaluate.

    What is NOT known: how many relation types exist, what they mean, and whether the
    apparent proportions (44 / 35 / 21 per cent) survive a fourth increase in sample size.
    Given the record above, they should not be trusted.""")

    print("\n  PASS 9868 -- the methodological point\n")
    print("""    Two findings, both clean, both wrong, both killed by the same move: more data.
    The n=14 sample produced zero counterexamples to a law that has six of them at n=34.

    Neither was caught by reasoning. Both were caught by resampling before writing. That is
    the only reason this pass reports a structure question rather than a false theorem, and
    it is the second time in this line of work that a control has overturned a result --
    the first being the type-4 baseline at Pass 9701-9724, where a random-generator control
    disagreed with a published number.

    The operational rule this suggests: when a combinatorial law holds with zero exceptions
    on a sample assembled for convenience, the sample size IS the result until it is varied.""")

    out = {
        "boundary": (
            "A structure question about V_2's 4095 frames, and TWO FINDINGS THAT DID NOT "
            "SURVIVE. At 14 classes the pairwise frame relation took exactly two values and "
            "appeared to depend only on the sum class (25 shared sums, 0 disagreements). At "
            "34 classes there are THREE relation types and SIX disagreeing sum classes. Both "
            "findings are false and were killed before publication by increasing the sample"),
        "question": ("every nonzero class of V_2 is type 8, hence a frame; V_2 is a group of "
                     "4096 frames, and any two are compared by the multiset of |inner "
                     "products| between their 24 representatives"),
        "small_sample": SMALL,
        "large_sample": LARGE,
        "relation_types_at_34": [{"profile": d, "count": n} for d, n in TYPES],
        "killed": {
            "two_relation_types": ("FALSE -- there are at least three; the third accounts for "
                                   "35% of pairs at n=34 and did not occur in the first 91"),
            "depends_only_on_sum_class": ("REFUTED -- six sum classes carry two different "
                                          "relations. Zero clashes at n=14, six at n=34")},
        "survives": [
            "V_2's 4095 nonzero classes are all frames (rests on the type-4 census and q)",
            "every observed relation has |ip| in {0,2,4}, across 561 comparisons",
            ("the 24-number profile against a SINGLE representative determines the full "
             "576-pair relation, which makes the relation cheap to evaluate")],
        "not_known": ("how many relation types exist, what they mean, and whether the "
                      "observed 44/35/21 per cent proportions survive further sampling -- "
                      "given the record above they should not be trusted"),
        "methodological_point": (
            "two clean findings, both wrong, both killed by more data rather than by "
            "reasoning. Second time in this line that a control overturned a result -- the "
            "first was the type-4 baseline at Pass 9701-9724. Operational rule: when a "
            "combinatorial law holds with ZERO exceptions on a sample assembled for "
            "convenience, the sample size IS the result until it is varied"),
    }
    fp = ROOT / "data" / "PART_W33_PASS9861_9884_SAMPLING.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
