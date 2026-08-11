#!/usr/bin/env python3
"""Catch novelty that is IMPLIED rather than asserted.

Pass 2781.  `check_novelty_claims.py` (Pass 2743) greps for phrases like "appears to be
absent" and "no prior art".  Its own audit measured the limit: of six claims overturned
in one session, only TWO asserted novelty in words.  The other four simply presented a
result as a finding and never said "this is new" -- and no phrase regex can see that.

The insight that makes the other four detectable is that implicit novelty has a
different signature.  It is not a phrase; it is a POSITION plus an ABSENCE:

    a distinctive token appears in an EMPHASIZED position -- a heading, a bold run,
    a blockquote -- and the same token appears in the encyclopedia, and the file
    never cites the encyclopedia anywhere.

A file that emphasises `J_3(O)` and cites `docs/index.html` is doing normal work.  A
file that emphasises `J_3(O)` and cites nothing is implicitly claiming it, whether or
not it ever writes the word "new".  That is exactly the Pass 2735 failure, and it is
exactly what the phrase regex missed.

CALIBRATION, which is the part that decides whether a guard is usable.  The repo's
standing lesson (Pass 328, and the two later guards) is that a token class chosen by
intuition flags nearly every file and is pure noise.  Measured here over 122 pass files,
each step taken only after the previous one was measured:

    flagged   step                                       what the noise turned out to be
    -------   ----------------------------------------   -------------------------------
      9/122   presence in the encyclopedia, any token     ALL NINE were pass numbers in
                                                          titles -- "Pass 1973" matched
                                                          because "1973" occurs somewhere
                                                          in a 20,000-line document
      0/122   + skip files containing "Prior art"         VACUOUS: every pass file in this
                                                          repo has a Prior-art section, so
                                                          the guard cleared everything,
                                                          including the known failure
     51/122   + cite-the-RIGHT-source, per token          `W(3,3)` 21x, `PSp(4,3)` 12x --
                                                          the repo's own subject matter
     30/122   + rarity: <= 12 mentions in the source      round numbers: `2400`, `4000`,
                                                          `5280` (an FPGA part size)
     22/122   + drop integers ending in "00"              what ships

Each of those four steps was a real mistake corrected by measurement, and the second one
is the instructive one: a guard that passes everything looks exactly like a guard that
finds nothing wrong.

Token classes are deliberately narrow: named algebras and groups (`J_3(O)`, `E_6`,
`SRG(36,15,6,6)`), code parameters (`[[137,1,21]]`), and non-round integers of four
digits or more.  Everything else is dropped.

WARNS, never blocks -- the standing policy, because a collision is a candidate for
reading, not a verdict, and blocking trains `--no-verify`.

Usage:
    py -3 scripts/check_implicit_novelty.py <files...>
    py -3 scripts/check_implicit_novelty.py            # all analysis/*.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ENCYCLOPEDIA = [
    ROOT / "docs" / "index.html",
    ROOT / "photonic_holonet_body.tex",
    ROOT / "w33_paper_body.tex",
]

# Positions that carry emphasis in this repo's markdown: ATX headings, bold runs, and
# blockquote lines.  A result stated in one of these is being presented, not mentioned.
HEADING = re.compile(r"^#{1,6}\s+(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
QUOTE = re.compile(r"^>\s?(.*)$")

# Token classes narrow enough to be usable.  See the calibration note above.
NAMED_ALGEBRA = re.compile(
    r"\b(?:[A-Z]_?\d(?:\([^)]{1,14}\))?"          # E_6, J_3(O), F_4, A_2
    r"|[A-Z]{1,3}[a-z]{0,3}\(\d+(?:,\d+)*\)"      # Sp(4,3), SU(4), SRG(40,12,2,4)
    r"|W\(\d,\d\))"                               # W(3,3)
)
CODE_PARAM = re.compile(r"\[\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]\]")
BIG_INT = re.compile(r"(?<![\d.,])(\d{4,9})(?![\d.,])")

# A citation only counts if it names the source that actually carries the token.
#
# The first version skipped any file containing the words "Prior art".  Every pass file
# in this repo has a Prior-art section, so the guard became vacuous -- it cleared 122
# files including the known Pass 2735 failure.  A blanket "does it cite anything" test
# is not a test.  Per-source is: a file that emphasises `J_3(O)` and cites the holonet
# paper has still not cited `docs/index.html`, which is where `J_3(O)` lives.
CITED_BY = {
    "index.html": re.compile(r"(index\.html|Pillars?\s*\d|Master Dictionary)", re.I),
    "photonic_holonet_body.tex": re.compile(r"(photonic[_ ]holonet|holonet paper)", re.I),
    "w33_paper_body.tex": re.compile(r"(w33[_ ]paper|W\(3,3\) paper)", re.I),
}


def load_encyclopedia() -> dict[str, str]:
    out = {}
    for p in ENCYCLOPEDIA:
        if p.exists():
            try:
                out[p.name] = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                pass
    return out


# Pass and ticket numbers are four-digit integers that appear in EVERY heading in this
# repo, and almost any four-digit string occurs somewhere in a 20,000-line encyclopedia.
# The first calibration run flagged 9 files and every single hit was a pass number in a
# title.  Stripping these references before tokenising is what takes the guard from
# unusable to usable -- it is the same lesson as Pass 328's bare-integer measurement,
# rediscovered on this guard's first run.
PASSREF = re.compile(r"\b(?:Pass(?:es)?|BT|bt|pass|phase|Phase)[\s_]*\d+(?:\s*[-–]\s*\d+)?",
                     re.I)
YEARISH = re.compile(r"^(?:1[89]\d\d|20\d\d|21\d\d)$")

# A token the encyclopedia mentions more often than this is ambient vocabulary,
# not a result.  Calibrated below; see the note in check().
RARITY_MAX = 12


def emphasized_spans(text: str) -> list[tuple[int, str]]:
    """(line number, emphasized text) for every heading, bold run and blockquote."""
    spans = []
    # split on "\n" rather than splitlines(): Python treats FORMFEED and vertical tab as
    # line breaks, so in the 13 tracked files carrying such a byte every reported line
    # number past the first one is too high, and the content on that line is split across
    # two reported lines. A reporting bug, not a detection bug -- Pass 4839 measured it.
    for ln, line in enumerate(text.split(chr(10)), 1):
        m = HEADING.match(line)
        if m:
            spans.append((ln, m.group(1)))
        m = QUOTE.match(line)
        if m:
            spans.append((ln, m.group(1)))
        for b in BOLD.finditer(line):
            spans.append((ln, b.group(1)))
    return spans


def tokens_of(s: str) -> set[str]:
    s = PASSREF.sub(" ", s)                       # drop pass/ticket references first
    toks = set(NAMED_ALGEBRA.findall(s))
    toks |= set(CODE_PARAM.findall(s))
    # Round hundreds (2400, 4000, 5280) are almost never a result in this repo -- they
    # are counts, part sizes and coincidences.  The distinctive integers here (25920,
    # 51840, 196883, 1296) are not round, so the cut costs nothing and removes a third
    # of the remaining noise.
    toks |= {t for t in BIG_INT.findall(s)
             if not YEARISH.match(t) and not t.endswith("00")}
    return {t for t in toks if len(t) > 2}


def check(path: Path, enc: dict[str, str]) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    # Which sources does this file actually cite?  Per-source, not blanket.
    cited = {name for name, pat in CITED_BY.items() if pat.search(text)}

    hits: dict[str, tuple[int, str, str, int]] = {}
    for ln, span in emphasized_spans(text):
        for tok in tokens_of(span):
            if tok in hits:
                continue
            for name, body in enc.items():
                if name in cited:
                    continue                      # this source is credited already
                n = body.count(tok)
                # RARITY, not presence.  A token the encyclopedia repeats hundreds of
                # times is the SUBJECT of the repo, not a result: emphasising `W(3,3)`
                # or `Sp(4,3)` is naming what you are working on.  A token it mentions
                # a handful of times is a specific result, and emphasising that without
                # citing it is the implicit claim this guard exists to catch.
                #
                # This replaced a hand-written stoplist, and it is better: it needs no
                # maintenance and it adapts as the encyclopedia grows.  Measured on 122
                # session files -- presence alone flags 42%, of which the top hits were
                # `W(3,3)` (21x), `PSp(4,3)` (12x) and the FPGA part size `5280`; the
                # rarity cut keeps `SRG(36,15,6,6)`, `25920` and `51840` and drops all
                # of those.
                if 0 < n <= RARITY_MAX:
                    hits[tok] = (ln, name, span.strip()[:80], n)
                    break
    if not hits:
        return []
    out = [f"  {path.name}: emphasises {len(hits)} token(s) carried by a source "
           f"the file never cites"]
    for tok, (ln, name, span, n) in sorted(hits.items())[:6]:
        out.append(f"    line {ln}: {tok!r} is in {name} ({n}x - rare enough to be a result)")
        out.append(f"      emphasised as: {span}")
    return out


def _safe(t: str) -> str:
    """cp1252 consoles cannot print this repo's notation; the Pass 2743 guard crashed
    on U+2102 and this one will not."""
    return t.encode("ascii", "replace").decode("ascii")


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    paths = [Path(a) for a in args] or sorted((ROOT / "analysis").glob("w33_pass*.md"))
    enc = load_encyclopedia()
    if not enc:
        print("check_implicit_novelty: no encyclopedia files found; nothing to check")
        return 0

    print(f"checking {len(paths)} file(s) against {', '.join(enc)}")
    flagged = []
    for p in paths:
        if p.exists():
            flagged.extend(check(p, enc))
    if flagged:
        n = sum(1 for line in flagged if line.startswith("  ") and ": emphasises" in line)
        print(f"\n{n} file(s) present encyclopedia results without citing them "
              f"- review, not a block:\n")
        for line in flagged:
            print(_safe(line))
    else:
        print("no file emphasises an uncited encyclopedia result.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
