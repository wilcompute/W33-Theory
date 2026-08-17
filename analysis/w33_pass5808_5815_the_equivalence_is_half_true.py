"""Passes 5808-5815 -- the equivalence is refuted; only one direction survives.

  5808  Three counterexamples: unique block system does NOT imply a kernel partition.
  5809  The surviving direction, and its evidence.
  5810  Real Desargues is primitive and agrees -- the one prediction that held.
  5811  Why the fake configurations accidentally supported the wrong claim.
  5812  How fast this was refuted, and what made it fast.
  5813  alpha(W(3,9)) under (1,3)-swaps: slow, unfinished, reported as such.
  5814  What is left of the class.
  5815  Scope.

    py -3 analysis/w33_pass5808_5815_the_equivalence_is_half_true.py
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

DATA = [
    {"name": "Reye 12_4 16_3", "pts": 12, "point_group": 576, "primitive": False,
     "systems": 1, "kdim": 4, "partition": True, "predicted": True, "agrees": True},
    {"name": "Pappus 9_3", "pts": 9, "point_group": 108, "primitive": False,
     "systems": 1, "kdim": 2, "partition": True, "predicted": True, "agrees": True},
    {"name": "Fano 7_3", "pts": 7, "point_group": 168, "primitive": True,
     "systems": 0, "kdim": 3, "partition": False, "predicted": False, "agrees": True},
    {"name": "Desargues 10_3 (REAL)", "pts": 10, "point_group": 120, "primitive": True,
     "systems": 0, "kdim": 4, "partition": False, "predicted": False, "agrees": True},
    {"name": "Mobius-Kantor 8_3 (REAL)", "pts": 8, "point_group": 48, "primitive": False,
     "systems": 1, "kdim": 0, "partition": False, "predicted": True, "agrees": False},
    {"name": "Z8 lines {i,i+2,i+4}", "pts": 8, "point_group": 1152, "primitive": False,
     "systems": 1, "kdim": 0, "partition": False, "predicted": True, "agrees": False},
    {"name": "three parallel triples/9", "pts": 9, "point_group": 279936,
     "primitive": False, "systems": 1, "kdim": 6, "partition": False,
     "predicted": True, "agrees": False},
]


def main() -> int:
    print("=" * 78)
    print("Passes 5808-5815 -- the equivalence is half true")
    print("=" * 78)

    print("\n  PASS 5808-5809 -- all seven configurations\n")
    print(f"    {'configuration':26s} {'pts':>4s} {'|G|':>8s} {'prim':>6s} "
          f"{'sys':>4s} {'kdim':>5s} {'part':>6s} {'agrees':>7s}")
    for d in DATA:
        print(f"    {d['name']:26s} {d['pts']:4d} {d['point_group']:8d} "
              f"{str(d['primitive']):>6s} {d['systems']:4d} {d['kdim']:5d} "
              f"{str(d['partition']):>6s} {str(d['agrees']):>7s}")
    bad = [d["name"] for d in DATA if not d["agrees"]]
    print(f"\n    counterexamples: {len(bad)} -- {', '.join(bad)}")
    print("""
    THE EQUIVALENCE I CLAIMED AT PASS 5800 IS FALSE. Three configurations have exactly one
    nontrivial block system and NO kernel partition. Mobius-Kantor and the Z8 configuration
    have kernel dimension ZERO -- there is nothing for top-weight words to be -- and the
    nine-point triple configuration has a six-dimensional kernel with 27 top-weight words
    that do not partition anything.

    SO 'UNIQUE BLOCK SYSTEM ==> KERNEL PARTITION' IS DEAD, with three witnesses.

    ONE DIRECTION SURVIVES AND IS UNREFUTED ON ALL SEVEN POINTS:

        kernel top-weight words complement to a partition
                          ==>
        the point action has a unique nontrivial block system

    The Reye and Pappus have the partition and have exactly one system. The five without a
    partition are either primitive (Fano, Desargues) or have one system without producing
    the partition -- neither contradicts the implication, because the implication says
    nothing about configurations lacking the partition.""")

    print("\n  PASS 5810-5811 -- the real Desargues, and why the fakes misled\n")
    print("    real Desargues 10_3: |Aut| = 120 (matches published), PRIMITIVE, 0 systems")
    print("    kernel dim 4, ten top-weight words, no partition -- PREDICTION HELD")
    print("""
    THE ONE PREDICTION THAT WORKED was on the configuration I had previously faked. My fake
    'Desargues' had |Aut| = 4 and failed the kernel test; the real one has |Aut| = 120, is
    primitive, and fails it too. The fake agreed with the conjecture BY ACCIDENT -- it
    failed for having almost no symmetry, not for being primitive.

    AND THE FAKE MOBIUS-KANTOR IS WHERE THE DAMAGE WAS. It had |Aut| = 1 and failed the
    kernel test, which looked consistent. The real one has |Aut| = 48, one block system,
    and STILL fails -- which is a counterexample the fake was hiding. Bad inputs did not
    just weaken the survey; they concealed the refutation.""")

    print("\n  PASS 5812 -- how fast, and why\n")
    print("""    ONE BATCH. Pass 5800 claimed the equivalence on three configurations; Pass
    5808 refutes it on three more. What made it fast was building the objects the
    conjecture makes PREDICTIONS about -- configurations with exactly one block system,
    where the claim says a partition must appear -- rather than gathering more
    configurations of whatever kind.

    A CONJECTURE THAT SURVIVES ONLY CONFIRMING CASES HAS NOT BEEN TESTED. Three of the
    seven here were chosen because the claim forced an answer on them, and all three broke
    it.""")

    print("\n  PASS 5813 -- alpha(W(3,9)) under (1,3)-swaps\n")
    print("""    Launched and still in its early phase at cutoff -- 42 after the first
    iterations, well below the 51 that three (1,2)-searches reach. The (1,3) neighbourhood
    is far more expensive per move, so a fair comparison needs it to run to completion.
    NO RESULT, and specifically no claim that the changed neighbourhood does or does not
    beat 51.""")

    print("\n  PASS 5814-5815 -- what is left\n")
    print("""    A ONE-WAY IMPLICATION with two positive instances and five non-contradicting
    ones, which is much weaker than what Pass 5800 asserted and is still not nothing: it
    says the kernel partition is a SUFFICIENT condition for imprimitivity with a unique
    system, and the Reye and Pappus are the cases where it fires.

    NOT DONE: a configuration with TWO OR MORE block systems -- none of the seven has one,
    so the sharpest test of the surviving direction is still unavailable; a proof; and
    alpha(W(3,9)) under the new neighbourhood.""")

    out = {
        "boundary": (
            "Pass 5808 REFUTES the equivalence claimed at Pass 5800 with three "
            "counterexamples. The surviving direction is unrefuted on seven "
            "configurations and is NOT proved. Pass 5813 reports a search as unfinished "
            "with no result. No configuration with two or more block systems was found, "
            "so the sharpest test remains unrun"),
        "pass_5808_5809": {
            "configurations": DATA,
            "refuted": "unique block system ==> kernel partition",
            "counterexamples": bad,
            "survives": ("kernel top-weight words complement to a partition ==> the point "
                         "action has a unique nontrivial block system"),
            "evidence": "unrefuted on all seven; two positive instances"},
        "pass_5810_5811": {
            "real_desargues": {"aut": 120, "primitive": True, "systems": 0,
                               "kdim": 4, "partition": False, "prediction_held": True},
            "fake_damage": ("the fake Desargues agreed by accident -- it failed for having "
                            "almost no symmetry, not for being primitive; the fake "
                            "Mobius-Kantor (|Aut| = 1) CONCEALED a counterexample that the "
                            "real one (|Aut| = 48, one system, still fails) exposes")},
        "pass_5812": {"time_to_refutation": "one batch",
                      "method": ("build the objects the conjecture makes PREDICTIONS "
                                 "about, not more objects of whatever kind"),
                      "lesson": ("a conjecture that survives only confirming cases has not "
                                 "been tested; three chosen adversarially, all three broke it")},
        "pass_5813": {"neighbourhood": "(1,3)-swap", "status": "UNFINISHED, no result",
                      "observed": "42 in the early phase, against 51 from (1,2)-searches",
                      "caveat": "the (1,3) move is far more expensive; comparison needs completion"},
        "pass_5814_5815": {
            "remaining_claim": ("the kernel partition is SUFFICIENT for imprimitivity with "
                                "a unique block system"),
            "strength": "two positive instances, five non-contradicting",
            "not_done": ["a configuration with two or more block systems",
                         "a proof", "alpha(W(3,9)) under the new neighbourhood"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5808_5815_THE_EQUIVALENCE_IS_HALF_TRUE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
