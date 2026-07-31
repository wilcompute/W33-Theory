#!/usr/bin/env python3
"""Flag files that generalise from a DETERMINISTIC enumeration order.

WHY THIS EXISTS (measured, Pass 1428).  Pass 1411 concluded that the stabilisers
of exact covers are "diagonal" -- that none fixes a frame.  The evidence was six
covers.  All six came from ONE depth-first search, and a DFS visits solutions in
an order determined by the problem encoding, not by any notion of typicality.
Re-running the same search across twelve RANDOMISED orders immediately produced
`C2`-stabilised covers fixing twelve frames each, refuting the conclusion:

    one DFS order      C4, C2xC2, C4xC2        0 fixed frames    (6 covers)
    randomised orders  + C2                   12 fixed frames    (24 covers)

The mathematics was right and the sampling was wrong, which is the harder failure
to notice: every individual computation checked out.

WHAT IT FLAGS.  Files that (a) enumerate solutions, (b) truncate to the first few,
and (c) never randomise.  That is a CANDIDATE pattern, not a defect -- plenty of
files truncate only for display, and plenty enumerate exhaustively so order is
irrelevant.  The measured population over analysis/ and scripts/ is ~152 files,
far too many to be all wrong; the point is to make the question askable at the
moment someone writes "sampled ... therefore".

The sharpest sub-signal is (d): a generalising word near the truncation.

Run:  py -3 scripts/check_sampler_bias.py [files...]   (default: analysis/, scripts/)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RE_ENUM = re.compile(
    r"\bdef solve\b|\bbacktrack\b|exact.?cover|Algorithm X|dancing links"
    r"|itertools\.(?:permutations|combinations)\b", re.I)
RE_TRUNC = re.compile(r"\[:\s*\d+\]|len\(\w+\)\s*>=\s*\d+|\bbreak\b", re.I)
RE_RAND = re.compile(r"\brandom\.|\bshuffle\b|\bseed\b|\brng\b", re.I)
# the tell that a truncated sample is being turned into a general statement
RE_GENERALISE = re.compile(
    r"(?i)\b(sampled|every|all |always|never|uniformly|in general|therefore"
    r"|so a |conclude)\b")


def scan(paths: list[Path]) -> list[tuple[Path, bool]]:
    out = []
    for p in paths:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if RE_ENUM.search(t) and RE_TRUNC.search(t) and not RE_RAND.search(t):
            out.append((p, bool(RE_GENERALISE.search(t))))
    return out


def main(argv: list[str]) -> int:
    if argv:
        paths = [Path(a) for a in argv if Path(a).suffix == ".py"]
    else:
        paths = sorted(list((ROOT / "analysis").glob("*.py"))
                       + list((ROOT / "scripts").glob("*.py")))
    hits = scan(paths)
    strong = [p for p, g in hits if g]
    print("=" * 74)
    print("[sampler bias] enumerate + truncate + no randomisation")
    print("=" * 74)
    print(f"scanned {len(paths)} files")
    print(f"  deterministic-order samplers      : {len(hits)}")
    print(f"  ...that also generalise in prose  : {len(strong)}   <- read these")
    for p in strong[:30]:
        print(f"    {p.relative_to(ROOT)}")
    print("\n  CANDIDATES, not defects. Truncating for display is fine; so is an")
    print("  exhaustive search, where order cannot matter. What is NOT fine is")
    print("  'the sampled X all have property P, therefore X has property P'")
    print("  when the sample came from one search order. Randomise, then claim.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
