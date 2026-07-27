#!/usr/bin/env python3
"""Re-measure MAX_FILES for RESULTS_INDEX.md against the real corpus.

WHY THIS EXISTS.  `analysis/build_results_index.py` carries a calibration table in
its docstring justifying `MAX_FILES = 25`.  That table is void: it was measured on
a corpus that globbed `formal/.lake/packages/`, so 59% of the files it counted were
mathlib and batteries sources.  A cut chosen to separate "result" from "topic" was
tuned on a file population that is mostly not this project.

The cut is not a constant and never was -- the index has a half-life, because a
result the corpus works ON becomes a topic OF the corpus.  So the honest move is
not to pick a new number but to re-run the measurement and print what each cut
actually buys, on the 6,521-file corpus that remains after `.lake` is excluded.

WHAT IS MEASURED, and why these two numbers.

  flag rate   the fraction of pass witnesses that the rediscovery guard would warn
              on.  Pass 328 established the usable ceiling empirically: at >90% a
              guard is noise and gets ignored, which is worse than no guard.

  probes      whether specific central results survive the cut.  A cut that drops
              [[40,10,4]] has failed at its own job regardless of its flag rate --
              that code parameter is the flagship catch.

Run:  py -3 scripts/calibrate_index_cut.py
"""

from __future__ import annotations

import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
sys.path.insert(0, str(ROOT / "scripts"))

import build_results_index as B  # noqa: E402
from check_rediscovery import (  # noqa: E402
    RE_NAMED, RE_ROOT, compounds, noun_number_pairs, results_in)

# THE FLAG RATE MUST USE THE GUARD'S OWN EXTRACTOR, NOT THE INDEX'S.
#
# These are deliberately different grammars and conflating them was my first
# attempt at this measurement.  The index records bare integers so a human can
# grep for `51840`; the guard drops them, because Pass 328 measured that bare
# integers flag 78% of files and carry no signal.  Feeding the index's grammar
# into a flag-rate calculation reports ~96% at every cut -- a number about the
# index, not about the guard, and it would have condemned a guard that is not
# actually that noisy.
#
# The guard also suppresses a hit when the file ALREADY names the prior-art file,
# which is the whole point (cite it and the warning goes away).  Both behaviours
# are reproduced below.

PROBES = ["[[40,10,4]]", "[40,15,8]", "[[240,81,3]]", "51840", "8353", "196883"]
CUTS = [10, 15, 20, 25, 30, 40, 60, 100]


def tokens_of(txt: str) -> set[str]:
    """Exactly the token grammar build_results_index.py uses, per file."""
    toks: set[str] = set()
    for rx in (B.RE_CSS, B.RE_LIN, B.RE_SEQ):
        toks.update(B.norm(m) for m in rx.findall(txt))
    compact = B.norm(txt)
    toks.update(q for q in B.PINNED_RESULTS if q in compact)
    for m in B.RE_INT.findall(txt):
        integer = B.canonical_integer(m)
        if integer not in B.NOISE:
            toks.add(integer)
    toks.update(m.lower() for m in RE_NAMED.findall(txt))
    toks.update(RE_ROOT.findall(txt))
    toks.update(compounds(txt))
    toks.update(noun_number_pairs(txt))
    return toks


def main() -> int:
    files = []
    for g in B.GLOBS:
        for p in ROOT.glob(g):
            if p.is_file() and not any(d in p.parts for d in B.SKIP_DIRS):
                files.append(p)
    files = sorted(set(files))

    # one pass over the corpus; every cut is then a pure filter on these counts
    per_file: dict[str, set[str]] = {}     # index grammar -> decides the cut
    guard_toks: dict[str, set[str]] = {}   # guard grammar -> decides the flag rate
    body: dict[str, str] = {}
    counts: Counter[str] = Counter()
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(ROOT).as_posix()
        toks = tokens_of(txt)
        per_file[rel] = toks
        counts.update(toks)
        if rel.startswith(("analysis/", "passes/", "exploration/")):
            guard_toks[rel] = results_in(txt)
            body[rel] = txt

    # the witnesses the guard actually runs on
    witnesses = [
        r for r in per_file
        if ("w33_pass" in r.rsplit("/", 1)[-1].lower())
        and r in guard_toks
    ]

    owners: dict[str, list[str]] = defaultdict(list)
    for rel, toks in per_file.items():
        for t in toks:
            owners[t].append(rel)

    print(f"corpus              : {len(files)} files "
          f"(.lake excluded -- see build_results_index.py SKIP_DIRS)")
    print(f"pass witnesses      : {len(witnesses)}")
    print(f"distinct tokens     : {len(counts)}")
    print()
    header = f"{'MAX':>5} {'kept':>7} {'unique':>7} {'flag rate':>10}   probes surviving"
    print(header)
    print("-" * (len(header) + 14))

    for cut in CUTS:
        kept = {t for t, n in counts.items() if 1 <= n <= cut or t in B.PINNED_RESULTS}
        uniq = sum(1 for t in kept if counts[t] == 1)
        flagged = 0
        for w in witnesses:
            txt = body[w]
            for t in guard_toks[w]:
                if t not in kept:
                    continue
                # self excluded, and -- as the guard does -- prior art that the
                # file already cites by filename does not warn
                prior = [o for o in owners[t]
                         if o != w and o.rsplit("/", 1)[-1] not in txt]
                if prior:
                    flagged += 1
                    break
        rate = 100.0 * flagged / max(1, len(witnesses))
        alive = [p for p in PROBES if p in kept]
        print(f"{cut:>5} {len(kept):>7} {uniq:>7} {rate:>9.1f}%   "
              f"{len(alive)}/{len(PROBES)}  {' '.join(alive[:3])}")

    print()
    print("probe file-counts on the corrected corpus:")
    for p in PROBES:
        pinned = "  (pinned)" if p in B.PINNED_RESULTS else ""
        print(f"  {p:<16} {counts[p]:>5} files{pinned}")
    print()
    print(f"current setting: MAX_FILES = {B.MAX_FILES}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
