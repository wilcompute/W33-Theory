#!/usr/bin/env python3
"""A search result with no random baseline is not a result.  Pass 4454.

WHY THIS EXISTS
---------------
Pass 4438 measured that 87% of random +/-1 signings of W(3,3) already satisfy the Ramanujan
bound.  Five earlier passes -- 4409, 4418, 4426, 4433, 4437 -- had reported "a Ramanujan
signing was found" as though finding one were the achievement.  Every number in them was
correct.  What was wrong was the implied difficulty, and one line of code would have caught
it at the time:

    generate N random configurations, report what fraction already succeed.

That is the cheapest possible control and it went unrun across twelve searches in five
passes.  Pass 4441 rescored the arc afterwards; this checker exists so the next arc does not
need rescoring.

WHAT IT FLAGS
-------------
A pass that uses SEARCH vocabulary -- "best found", "local search", "optimised", "minimise
rho", "restarts" -- and reports a winning value, without any BASELINE vocabulary anywhere in
the file: "random", "baseline", "null model", "by chance", "fraction", "control".

It WARNS, never blocks.  A search whose baseline is obviously zero (an exhaustive proof, a
construction with a uniqueness theorem) is a legitimate false positive, and blocking on it
would train --no-verify -- the same calibration CLAUDE.md gives check_rediscovery.py.

PLANTED FAULTS
--------------
`--selftest` runs the detector against a search-with-no-baseline, a search-with-baseline, a
pass with no search at all, and a pass whose only "random" is `numpy.random` used to
GENERATE the search rather than to control it.  That last case is the one that matters: a
naive keyword check passes it, and it is exactly the shape all five of my own passes had.

    py -3 scripts/check_search_baseline.py --selftest
    py -3 scripts/check_search_baseline.py analysis/w33_pass44*.py
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SEARCH = re.compile(
    r"\b(best[_ ](?:found|rho|value|score)|local search|simulated anneal\w*|"
    r"restarts?\b|minimis\w+ rho|minimiz\w+ rho|gradient (?:ascent|descent)|"
    r"hill.?climb\w*|optimis(?:ed|ing|ation)|optimiz(?:ed|ing|ation)|"
    r"search(?:ed|ing)? (?:for|over|inside)|witness found)\b", re.I)

# Baseline language must be ABOUT a comparison, not merely the presence of an RNG.
BASELINE = re.compile(
    r"\b(random(?:ly)? (?:sample|sampl\w+|draw\w*|configuration|signing|instance|"
    r"baseline|control|ensemble|guess\w*)|"
    r"baseline|null model|null hypothesis|by chance|at chance|"
    r"fraction (?:that|which|of \w+ that)|what fraction|"
    r"control (?:group|case|run)|compared (?:against|with) random|"
    r"versus random|vs random|against random|"
    r"already (?:satisf\w+|qualif\w+|beat\w*)|"
    r"z[- ]score|sigma from random|standard deviations? from)\b", re.I)

# The trap: numpy's RNG is how you GENERATE a search, not how you control it.
# No trailing \b: `RNG\.` and `rng\.` end in an escaped '.', a non-word literal, so with
# one they could never match. Found by scripts/check_regex_deadends.py, Pass 4742 -- the
# same fault that made a 51,840 statistic read 12.5% when it was 44%.
RNG_ONLY = re.compile(r"(?:\bdefault_rng\b|\bnp\.random\b|\bRNG\.|\brng\.|"
                      r"\brandom\.(?:seed|choice|randint|integers|uniform|permutation|"
                      r"sample)\b)")


def scan(text: str) -> tuple[bool, bool, bool]:
    """(does_search, has_baseline, rng_present)."""
    return (bool(SEARCH.search(text)), bool(BASELINE.search(text)),
            bool(RNG_ONLY.search(text)))


def selftest() -> int:
    cases = [
        ("search, no baseline (the fault)",
         "best_rho = inf\nfor _ in range(4):  # restarts\n"
         "    sel = RNG.integers(0, 2, 40)\n"
         "    # local search\n"
         "print('best found', best_rho)\n", True),
        ("search WITH a baseline",
         "best_rho = inf  # local search with restarts\n"
         "rhos = [f(RNG.integers(0,2,40)) for _ in range(4000)]\n"
         "print('fraction that already beat the bound:', (rhos <= b).mean())\n", False),
        ("no search at all",
         "ev = np.linalg.eigvalsh(A)\nprint('spectrum', ev)\n", False),
        ("RNG present but only to GENERATE the search",
         "import numpy as np\nRNG = np.random.default_rng(1)\n"
         "best = inf\nfor _ in range(8):  # restarts\n"
         "    x = RNG.integers(0, 2, 240)\n"
         "    # hill-climbing\n"
         "print('optimised value', best)\n", True),
        ("baseline phrased as a z-score",
         "# local search for the optimum\n"
         "print(f'optimised {v}, {z:+.2f} sigma from random')\n", False),
    ]
    ok = True
    print("  selftest")
    for name, text, want_flag in cases:
        s, b, r = scan(text)
        flagged = s and not b
        good = flagged == want_flag
        ok &= good
        print(f"    {name:44s} flag={str(flagged):5s} want={str(want_flag):5s} "
              f"{'PASS' if good else 'FAIL'}   (search={s} baseline={b} rng={r})")
    print("""
  The fourth case is the one this checker exists for. An RNG is present, so any check that
  merely greps for "random" passes it -- but the RNG is generating the search, not
  controlling it. All five of the passes that prompted this checker had exactly that shape.""")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    paths = ([Path(f) if Path(f).is_absolute() else ROOT / f for f in a.files]
             or sorted((ROOT / "analysis").glob("w33_pass*.py")))
    flagged, searched = [], 0
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        s, b, r = scan(t)
        if not s:
            continue
        searched += 1
        if not b:
            flagged.append((p.name, r))

    print(f"  passes that perform a search      : {searched}")
    print(f"  ... with NO baseline comparison   : {len(flagged)}"
          f"   ({100 * len(flagged) / max(searched, 1):.0f}%)")
    for name, r in flagged[:30]:
        print(f"    {name[:64]:64s} {'(has an RNG, used to search)' if r else ''}")
    if len(flagged) > 30:
        print(f"    ... and {len(flagged) - 30} more")
    print("""
  WARNS, NEVER BLOCKS. Some of these are legitimate: an exhaustive search over a small space
  needs no baseline, and neither does a construction backed by a uniqueness proof. The point
  is that a search reported WITHOUT one is a claim whose strength has not been measured, and
  measuring it costs a loop.""")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
