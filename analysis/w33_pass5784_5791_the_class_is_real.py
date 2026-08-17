"""Passes 5784-5791 -- the kernel-finds-the-block-system class is real, with two members.

  5784  Pappus: unique block system, and the char-2 kernel finds it. Same as the Reye.
  5785  The class, characterised: a UNIQUE nontrivial block system, recovered by the kernel.
  5786  Why the three-word shape predicted it.
  5787  alpha(W(3,9)): iterated local search, a third search class.
  5788  51 again -- three classes, three plateaus, one number.
  5789  What the plateau means and does not mean.
  5790  Fano, Desargues, Mobius-Kantor: why they fail.
  5791  Scope.

    py -3 analysis/w33_pass5784_5791_the_class_is_real.py
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

CLASS = [
    {"name": "Reye 12_4 16_3", "points": 12, "kernel_dim": 4, "top_words": 3,
     "group_order": 576, "transitive_id": 165, "levi_aut": 576, "self_dual": False,
     "block_systems": 1, "block_shape": "3 blocks of 4", "kernel_finds_it": True},
    {"name": "Pappus 9_3", "points": 9, "kernel_dim": 2, "top_words": 3,
     "group_order": 108, "transitive_id": 18, "levi_aut": 216, "self_dual": True,
     "block_systems": 1, "block_shape": "3 blocks of 3", "kernel_finds_it": True},
]
FAILS = [("Fano 7_3", 7, 3, "no partition from top words"),
         ("Desargues 10_3", 10, 2, "no partition from top words"),
         ("Mobius-Kantor 8_3", 8, 1, "kernel dim 1, only one nonzero word")]
Q9 = {"searches": [("plain random restarts", 51, "67s"),
                   ("perp-seeded restarts", 51, "28s"),
                   ("iterated local search, ruin-and-recreate", 51, "1s")],
      "bounds": [51, 80], "hoffman": 82, "dual": 80.83841179}


def main() -> int:
    print("=" * 78)
    print("Passes 5784-5791 -- the class is real")
    print("=" * 78)

    print("\n  PASS 5784-5785 -- both members, side by side\n")
    print(f"    {'configuration':16s} {'pts':>4s} {'kdim':>5s} {'top':>4s} "
          f"{'|G|':>5s} {'T-id':>6s} {'self-dual':>10s} {'block systems':>14s} "
          f"{'kernel finds it':>16s}")
    for c in CLASS:
        print(f"    {c['name']:16s} {c['points']:4d} {c['kernel_dim']:5d} "
              f"{c['top_words']:4d} {c['group_order']:5d} T{c['transitive_id']:<5d} "
              f"{str(c['self_dual']):>10s} {c['block_systems']:14d} "
              f"{str(c['kernel_finds_it']):>16s}")
    print("""
    BOTH HAVE EXACTLY ONE NONTRIVIAL BLOCK SYSTEM, AND IN BOTH THE CHARACTERISTIC-2
    KERNEL RECOVERS IT. Pappus's point-preserving subgroup has order 108 and acts on the
    nine points as T9_18, imprimitive with a single block representative of size 3 -- and
    that system is exactly the partition the kernel's three top-weight words complement to.

    THAT IS THE CLASS, and it is a sharper statement than Pass 5675 could make from one
    example: not "the Reye's kernel knows its group", but

        for a configuration whose automorphism group has a UNIQUE nontrivial block
        system, the GF(2) kernel's top-weight words complement to that system.

    UNIQUENESS IS DOING THE WORK IN BOTH CASES. A kernel cannot choose among several
    systems; where there is exactly one, there is nothing to choose. That was the argument
    at Pass 5675 for why the Reye result was not a coincidence, and it now has a second
    instance rather than being a story about one object.""")

    print("\n  PASS 5786 -- why the shape predicted it\n")
    print("    Reye  : 3 top-weight words -> 3 blocks of 4")
    print("    Pappus: 3 top-weight words -> 3 blocks of 3")
    print("""
    THREE WORDS, THREE BLOCKS, BOTH TIMES. Pass 5768 flagged the three-word structure as
    the shared invariant before the block-system test was run, and the count carried
    straight through: the number of top-weight codewords equals the number of blocks. That
    is what made the shape predictive rather than decorative.""")

    print("\n  PASS 5790 -- and why the other three fail\n")
    for name, pts, k, why in FAILS:
        print(f"    {name:20s} {pts:3d} points, kernel dim {k}   {why}")
    print("""
    THEY FAIL AT THE FIRST STEP, not the second. In none of the three do the top-weight
    words complement to a partition at all, so the block-system question never arises.
    Whether that is because their groups have no unique block system, or several, or none,
    is NOT tested here -- the kernel condition fails first and I did not go past it.""")

    print("\n  PASS 5787-5789 -- alpha(W(3,9)), a third search class\n")
    print(f"    {'method':44s} {'best':>5s} {'time to reach it':>18s}")
    for m, b, t in Q9["searches"]:
        print(f"    {m:44s} {b:5d} {t:>18s}")
    print(f"\n    bounds: {Q9['bounds'][0]} <= alpha <= {Q9['bounds'][1]}  "
          f"(Hoffman {Q9['hoffman']}, dual {Q9['dual']:.2f})")
    print("""
    THREE SEARCH CLASSES, THREE PLATEAUS, THE SAME NUMBER. Iterated local search with
    ruin-and-recreate reached 51 in ONE SECOND where plain restarts took 67 and seeded
    restarts 28 -- a large speed-up and no improvement in quality. That is the informative
    part: the difficulty is not that 51 is hard to find, it is that nothing above 51 is
    being found by any neighbourhood these searches explore.

    WHAT IT DOES NOT MEAN. It is NOT evidence that alpha = 51. All three methods share the
    same (1,2)-swap neighbourhood, so they are three variations on one search, not three
    independent attacks -- and a shared blind spot would look exactly like this. The honest
    reading is that the local-search family is exhausted and the next attempt must change
    the neighbourhood or the formulation, not the restart policy.""")

    out = {
        "boundary": (
            "Pass 5785 characterises a class with TWO members and does not prove the "
            "implication in general. Pass 5790 reports that three configurations fail the "
            "KERNEL condition and does NOT test their block systems. Pass 5789 explicitly "
            "declines to read the 51 plateau as evidence that alpha = 51; alpha(W(3,9)) "
            "remains OPEN at 51 <= alpha <= 80"),
        "pass_5784_5785": {
            "members": CLASS,
            "statement": ("for a configuration whose automorphism group has a UNIQUE "
                          "nontrivial block system, the GF(2) kernel's top-weight words "
                          "complement to that system"),
            "evidence": "two instances, Reye and Pappus, both verified in GAP",
            "why_uniqueness_matters": ("a kernel cannot choose among several systems; "
                                       "where there is exactly one there is nothing to "
                                       "choose")},
        "pass_5786": {"reye": {"top_words": 3, "blocks": "3 of size 4"},
                      "pappus": {"top_words": 3, "blocks": "3 of size 3"},
                      "prediction": ("the three-word shape was flagged at Pass 5768 before "
                                     "the block test; the count of top-weight words equals "
                                     "the number of blocks in both")},
        "pass_5790": {"failures": [{"name": n, "points": p, "kernel_dim": k, "reason": w}
                                   for n, p, k, w in FAILS],
                      "note": ("they fail the KERNEL condition first; their block systems "
                               "are not tested")},
        "pass_5787_5789": {
            "searches": [{"method": m, "best": b, "time": t} for m, b, t in Q9["searches"]],
            "bounds": Q9["bounds"], "hoffman": Q9["hoffman"], "dual": Q9["dual"],
            "status": "OPEN",
            "reading": ("ILS reached 51 in 1s versus 67s and 28s -- a large speed-up with "
                        "no quality gain; the difficulty is not finding 51"),
            "explicit_non_claim": ("this is NOT evidence that alpha = 51; all three methods "
                                   "share the (1,2)-swap neighbourhood, so they are three "
                                   "variations on one search and would share a blind spot"),
            "next": "change the neighbourhood or the formulation, not the restart policy"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5784_5791_THE_CLASS_IS_REAL.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
