"""Passes 5760-5767 -- perturbing the five survivors, and the durable outputs.

  5760  The change-the-object test, applied to my own surviving claims.
  5761  Result: the Reye phenomenon is NOT generic and NOT unique. Pappus shares it.
  5762  What that does to Pass 5675 and Pass 5691.
  5763  Failure mode six, written into CLAUDE.md.
  5764  Positive controls, made a standing rule.
  5765  The reservation protocol, fixed after the 5744 collision.
  5766  alpha(W(3,9)): the one open computation that IS about the substrate.
  5767  Scope.

    py -3 analysis/w33_pass5760_5767_perturbing_the_survivors.py
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

PERTURB = [("Reye 12_4 16_3", 12, 16, 4, 6, True),
           ("Fano 7_3", 7, 7, 3, 4, False),
           ("Pappus 9_3", 9, 9, 2, 6, True),
           ("Desargues 10_3", 10, 10, 2, 4, False),
           ("Mobius-Kantor 8_3", 8, 8, 1, 5, False)]
Q9 = {"bounds": [51, 80], "hoffman": 82, "dual": 80.83841179, "proved": False}
DURABLE = [("failure mode six + its one-line test", "CLAUDE.md"),
           ("arguments rediscover, computations discover", "CLAUDE.md"),
           ("positive controls for every negative search", "CLAUDE.md"),
           ("push AND re-fetch reservations before working", "CLAUDE.md"),
           ("construction-inheritance method", "Pass 5728 certificate"),
           ("DATE_FILE_INTEGER_INDEX.md", "committed artifact"),
           ("scripts/check_transitivity.py", "guard, selftest 8/8")]


def main() -> int:
    print("=" * 78)
    print("Passes 5760-5767 -- perturbing the survivors")
    print("=" * 78)

    print("\n  PASS 5760-5761 -- the test that killed the tower, run on my own claims\n")
    print(f"    {'configuration':20s} {'pts':>4s} {'blks':>5s} {'kdim':>5s} "
          f"{'min wt':>7s} {'complements partition':>22s}")
    for name, pts, blks, k, mw, part in PERTURB:
        print(f"    {name:20s} {pts:4d} {blks:5d} {k:5d} {mw:7d} {str(part):>22s}")
    yes = [n for n, _, _, _, _, p in PERTURB if p]
    print(f"\n    shows the phenomenon: {', '.join(yes)}  ({len(yes)} of {len(PERTURB)})")
    print("""
    NOT GENERIC, AND NOT UNIQUE EITHER. I expected the Reye alone and wrote that sentence
    before reading the table; Pappus 9_3 shares the property. Three of five configurations
    do NOT have it, so this is not the generic behaviour that killed the Sym^e thread --
    but two do, so it is not a fact about the Reye alone.

    THE HONEST MIDDLE. Pass 5675 and Pass 5691 survive the change-the-object test in the
    sense that matters -- perturbing the configuration usually destroys the phenomenon, so
    the result is not a property of "any configuration". They do NOT survive as statements
    about the Reye SPECIFICALLY. The right scope is a class containing at least the Reye
    and Pappus, and I do not know what defines that class.

    AND MY PROSE WAS WRONG AGAIN, caught by the table directly above it -- third time this
    session. Writing the conclusion before reading the output is the habit, and the fix is
    to compute the sentence rather than the number.""")

    print("\n  PASS 5762 -- what changes for Pass 5675 and 5691\n")
    print("""    UNCHANGED: the Reye's [12,4,6] kernel partition IS T12_165's unique block
    system, and Aut([12,4,6]) IS W(F4)/Z acting as T12_165. Both were verified two
    independent ways and typed by SmallGroup id; nothing here touches them.

    CHANGED: the FRAMING. I had been treating these as facts about the tomotope's
    configuration. They are facts about a class of configurations, and the Reye is one
    member. Whether Pappus's partition is also a block system of ITS automorphism group is
    the obvious next test and is NOT run here.""")

    print("\n  PASS 5763-5765 -- the durable outputs\n")
    for what, where in DURABLE:
        print(f"    {what:44s} -> {where}")
    print("""
    CLAUDE.md NOW CARRIES FAILURE MODE SIX with its one-line test, the
    arguments-rediscover calibration, the positive-control rule, and the reservation fix.
    Those are the outputs most likely to matter to whoever reads this next, and they cost
    nine passes of wrong subject to learn.""")

    print("\n  PASS 5766-5767 -- what is actually open\n")
    print(f"    alpha(W(3,9)) : {Q9['bounds'][0]} <= alpha <= {Q9['bounds'][1]}  "
          f"(Hoffman {Q9['hoffman']}, dual bound {Q9['dual']:.2f}, proved {Q9['proved']})")
    print("""
    THE ONE OPEN COMPUTATION THAT IS UNAMBIGUOUSLY ABOUT THE SUBSTRATE. Both ends moved
    this session -- 47 to 51 by construction, 82 to 80 by branching -- and neither is
    tight. It passes the change-the-object test trivially: alpha(W(3,9)) is a number about
    W(3,9) and about nothing else.

    NOT DONE: whether Pappus's partition is a block system of its own automorphism group;
    what defines the class the Reye and Pappus both belong to; and the literature searches
    re-run with positive controls.""")

    out = {
        "boundary": (
            "Pass 5761 REFUTES this pass's own expectation that the Reye is unique. Pass "
            "5762 changes the SCOPE of Passes 5675 and 5691 and does not touch their "
            "verified content. Pass 5766 reports alpha(W(3,9)) OPEN. Whether Pappus's "
            "partition is a block system of its own group is NOT tested"),
        "pass_5760_5761": {
            "test": "change the object and see whether the result changes",
            "configurations": [{"name": n, "points": p, "blocks": b, "kernel_dim": k,
                                "min_weight": m, "shows_phenomenon": s}
                               for n, p, b, k, m, s in PERTURB],
            "result": f"{len(yes)} of {len(PERTURB)}: {yes}",
            "verdict": ("NOT generic and NOT unique to the Reye; the right scope is a "
                        "class containing at least the Reye and Pappus, undefined"),
            "self_correction": ("prose predicted the Reye alone and the table refuted it; "
                                "third such catch this session")},
        "pass_5762": {"unchanged": ["the [12,4,6] partition IS T12_165's unique block system",
                                    "Aut([12,4,6]) IS W(F4)/Z acting as T12_165"],
                      "changed": "the framing -- these are facts about a CLASS, not the Reye",
                      "next_test": "is Pappus's partition a block system of its own group?"},
        "pass_5763_5765": {"durable": [{"output": w, "location": l} for w, l in DURABLE],
                           "claude_md": ["failure mode six + one-line test",
                                         "arguments rediscover, computations discover",
                                         "positive controls for negative searches",
                                         "push and re-fetch reservations"]},
        "pass_5766_5767": {**Q9, "status": "OPEN",
                           "why_it_qualifies": ("alpha(W(3,9)) is a number about W(3,9) "
                                                "and nothing else; it passes the "
                                                "change-the-object test trivially"),
                           "not_done": ["Pappus's partition as a block system",
                                        "what defines the Reye/Pappus class",
                                        "literature searches with positive controls"]},
    }
    fp = ROOT / "data" / "PART_W33_PASS5760_5767_PERTURBING_THE_SURVIVORS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
