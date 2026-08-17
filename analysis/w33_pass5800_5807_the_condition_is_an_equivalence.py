"""Passes 5800-5807 -- the class condition is an equivalence, and two of my inputs were fake.

  5800  On every valid case: kernel-partition <=> unique nontrivial block system.
  5801  Fano is the decisive case -- PRIMITIVE, and it fails both sides.
  5802  CORRECTION: my "Desargues" and "Mobius-Kantor" were not those configurations.
  5803  What that does to Pass 5761 and Pass 5790.
  5804  alpha(W(3,9)) with a (1,3)-swap neighbourhood.
  5805  The reservation audit: no silent loss across six blocks.
  5806  What is now established, and on how many points.
  5807  Scope.

    py -3 analysis/w33_pass5800_5807_the_condition_is_an_equivalence.py
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

VALID = [
    {"name": "Reye 12_4 16_3", "levi_aut": 576, "point_group": 576, "primitive": False,
     "block_systems": 1, "kernel_partition": True, "agrees": True},
    {"name": "Pappus 9_3", "levi_aut": 216, "point_group": 108, "primitive": False,
     "block_systems": 1, "kernel_partition": True, "agrees": True},
    {"name": "Fano 7_3", "levi_aut": 336, "point_group": 168, "primitive": True,
     "block_systems": 0, "kernel_partition": False, "agrees": True},
]
BOGUS = [
    {"label": "Desargues 10_3", "measured_aut": 4, "real_aut": 120,
     "verdict": "not the Desargues configuration"},
    {"label": "Mobius-Kantor 8_3", "measured_aut": 1, "real_aut": ">1",
     "verdict": "trivial automorphism group; not that configuration"},
]
RESERVATIONS = [("5744-5751", "wilcompute"), ("5752-5759", "Wil"), ("5760-5767", "Wil"),
                ("5768-5775", "Wil"), ("5776-5783", "wilcompute"), ("5784-5791", "Wil")]


def main() -> int:
    print("=" * 78)
    print("Passes 5800-5807 -- the condition is an equivalence")
    print("=" * 78)

    print("\n  PASS 5800-5801 -- both properties, tested independently\n")
    print(f"    {'configuration':16s} {'|Aut Levi|':>11s} {'|point grp|':>12s} "
          f"{'primitive':>10s} {'block sys':>10s} {'kernel part':>12s} {'agrees':>7s}")
    for c in VALID:
        print(f"    {c['name']:16s} {c['levi_aut']:11d} {c['point_group']:12d} "
              f"{str(c['primitive']):>10s} {c['block_systems']:10d} "
              f"{str(c['kernel_partition']):>12s} {str(c['agrees']):>7s}")
    print("""
    THREE FOR THREE, AND FANO IS THE ONE THAT MATTERS. Fano's point action is PRIMITIVE --
    zero nontrivial block systems, by GAP -- and its kernel's top-weight words do not
    complement to a partition. Both sides fail together. The Reye and Pappus each have
    exactly one block system and each has the partition. So on every case where the
    question is well posed:

        kernel top-weight words complement to a partition
                          <=>
        the point action has a UNIQUE nontrivial block system

    A PRIMITIVE COUNTEREXAMPLE IS WORTH MORE THAN ANOTHER POSITIVE. Two agreeing positives
    could both be instances of some third thing; a case where both sides fail together, for
    a group with no block system at all, is the first evidence that the two properties are
    tracking each other rather than co-occurring.""")

    print("\n  PASS 5802-5803 -- and two of my inputs were not what I labelled them\n")
    print(f"    {'label I used':22s} {'|Aut| measured':>15s} {'|Aut| actual':>13s}  verdict")
    for b in BOGUS:
        print(f"    {b['label']:22s} {b['measured_aut']:15d} {str(b['real_aut']):>13s}  "
              f"{b['verdict']}")
    print("""
    THE DESARGUES CONFIGURATION HAS |Aut| = 120. Mine measured 4. The Mobius-Kantor
    configuration does not have a trivial automorphism group; mine measured 1. Neither
    incidence list is the configuration I named it after -- they are some 10_3 and some
    8_3, written from memory and never checked.

    SO PASS 5761's "TWO OF FIVE" AND PASS 5790's FAILURE TABLE ARE BOTH OVERSTATED. The
    real count is two of THREE valid configurations showing the phenomenon, with the third
    (Fano) failing both sides in agreement. The two bogus rows contributed nothing except
    the false impression of a broader survey.

    CAUGHT BY A SANITY CHECK I SHOULD HAVE RUN AT INPUT: an automorphism group order is a
    published fact about a named configuration, and comparing it costs one lookup.""")

    print("\n  PASS 5804 -- alpha(W(3,9)) with the neighbourhood changed\n")
    print("""    A (1,3)-swap search -- drop one vertex, add three -- was launched, which is
    the change Pass 5789 said was needed after three (1,2)-searches all plateaued at 51.
    It had not passed its early phase at cutoff, so I have no result to report. Recording
    it as LAUNCHED AND UNFINISHED rather than describing a plateau I did not observe.""")

    print("\n  PASS 5805 -- the reservation audit\n")
    print(f"    {'block':14s} first committed on origin by")
    for b, who in RESERVATIONS:
        mark = "  <-- collided, renumbered" if who != "Wil" else ""
        print(f"    {b:14s} {who}{mark}")
    print("""
    NO SILENT LOSS ACROSS SIX BLOCKS. My four are on origin under my name; the two that
    collided are on origin under the other lane's, and both were renumbered rather than
    overwritten. The two collisions cost renumbering and nothing else.""")

    print("\n  PASS 5806-5807 -- what is established, and on how much\n")
    print("""    ESTABLISHED: an equivalence between a code property and a group property,
    verified on THREE configurations -- two positive, one primitive negative. That is a
    small sample and the statement is a conjecture with three data points, not a theorem.

    NOT DONE: a proof in either direction; the Desargues and Mobius-Kantor configurations
    tested for real; and alpha(W(3,9)) under the changed neighbourhood.""")

    out = {
        "boundary": (
            "Pass 5800 establishes an equivalence on THREE configurations and does not "
            "prove it. Pass 5802 CORRECTS Pass 5761 and Pass 5790, whose Desargues and "
            "Mobius-Kantor rows used incidence lists that are not those configurations. "
            "Pass 5804 reports a search as launched and unfinished, with no result"),
        "pass_5800_5801": {
            "configurations": VALID,
            "equivalence": ("kernel top-weight words complement to a partition <=> the "
                            "point action has a unique nontrivial block system"),
            "agreement": "3 of 3 valid cases",
            "decisive_case": ("Fano is PRIMITIVE -- zero block systems -- and fails the "
                              "kernel test too; both sides fail together"),
            "why_it_matters": ("a primitive counterexample is worth more than another "
                               "positive: two positives could share a third cause")},
        "pass_5802_5803": {
            "bogus_inputs": BOGUS,
            "corrects": ["Pass 5761's 'two of five'", "Pass 5790's failure table"],
            "real_count": "two of THREE valid configurations, with Fano agreeing negatively",
            "root_cause": "incidence lists written from memory and never sanity-checked",
            "the_check": ("compare |Aut| against the published order for a named "
                          "configuration; costs one lookup")},
        "pass_5804": {"neighbourhood": "(1,3)-swap: drop one, add three",
                      "motivation": "three (1,2)-searches all plateaued at 51",
                      "status": "LAUNCHED AND UNFINISHED -- no result at cutoff"},
        "pass_5805": {"blocks": [{"block": b, "first_on_origin": w} for b, w in RESERVATIONS],
                      "verdict": ("no silent loss; two collisions, both renumbered rather "
                                  "than overwritten")},
        "pass_5806_5807": {
            "established": ("an equivalence between a code property and a group property, "
                            "on three configurations"),
            "status": "conjecture with three data points, not a theorem",
            "not_done": ["a proof in either direction",
                         "the real Desargues and Mobius-Kantor configurations",
                         "alpha(W(3,9)) under the changed neighbourhood"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5800_5807_THE_CONDITION_IS_AN_EQUIVALENCE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
