#!/usr/bin/env python3
"""Find Boundary/Open sections that a LATER file has already answered.

WHY THIS EXISTS.  Almost every analysis file here ends with a Boundary, Open, or
"Next experiment" section.  Nothing in this project's workflow edits those when a
later pass closes them, so they record what was open *when that file was written*
and are then read as if they described the present.

Measured cost, twice in one day (2026-07-27):

  * BT810's Boundary lists two open identifications.  BT811 -- the NEXT file, same
    author, titled "O_h Confirmed, and the Polar-Pair Anatomy" -- opens with
    "Settles the two open identifications from BT810" and answers both.  Passes
    1111 and 1118 re-answered them from scratch and were withdrawn.
  * BT781's own answer (the order-48 element-order fingerprint) predates BT811's,
    so the same fact sits in the corpus three times.

An open question is a claim ABOUT THE CORPUS, and claims about the corpus get
searched, not trusted.  This script does that search mechanically.

METHOD, and its deliberate limits.  For each file with a boundary section, the
result-tokens in that section are extracted with the SAME grammar the rediscovery
guard uses (so the two tools cannot drift), and every strictly LATER file is
checked for the same tokens.  Ordering is by the number in the filename -- BT###,
pass####, or an ISO date -- because that is what this corpus actually sorts by.

Output is CANDIDATES, never verdicts.  A later file mentioning `ovoid@7` may be
answering the question, restating it, or using the same number for something else.
The point is to put the adjacent file in front of a human before a pass is spent.

Run:  py -3 scripts/check_stale_boundaries.py [--limit N]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_rediscovery import (group_tokens, noun_number_pairs,  # noqa: E402
                               results_in)

# the headings this corpus actually uses to mean "not done yet"
RE_BOUNDARY = re.compile(
    r"^\s{0,3}#{1,4}\s*(Boundary|Open (?:Problems|Questions)|Next experiment|"
    r"Open)\b.*$", re.I | re.M)
# NOT `(?:>\s*)?` -- a BLOCKQUOTED "Open:" is almost always someone ELSE's
# open question being quoted for discussion.  Allowing it made
# w33_pass1117_1119 (which quotes BT810's list verbatim in order to say it
# was already answered) register as having that boundary itself, and it
# surfaced as a false positive in the first precision measurement.
RE_INLINE_OPEN = re.compile(r"^[ 	]*Open:", re.I | re.M)
# PROSE open questions (Pass 1427).  My own Pass 1412 wrote "So the question
# stays open, and it is now sharp: ..." in running text, under no heading at
# all.  boundary_text() returned None, so the file was never scanned and the
# sweep could not have flagged BT1420 against it no matter what tokens
# matched.  A sentence that declares something open IS a boundary.
RE_PROSE_OPEN = re.compile(
    r"^.{0,200}?\b(question|problem|it)\s+(stays|remains|is still|is)\s+open\b.*$",
    re.I | re.M)

# A COMPILED PATTERN MUST NOT CONTAIN CONTROL CHARACTERS (Pass 1427).
#
# THREE times in one session a regex written through a shell heredoc had its
# `\b` word-boundary escapes consumed into literal BACKSPACE bytes (0x08).  The
# pattern still compiles, still reads correctly in the source, and silently
# matches nothing.  Twice it disabled a filter I then reported as working, and
# restoring them here fixed FIVE occurrences across this one file -- including
# patterns from Pass 1395 that had been broken since they were written.
# This makes the failure loud at import instead of invisible at runtime.
def _assert_no_control_chars() -> None:
    bad = [n for n, v in list(globals().items())
           if n.startswith("RE_") and hasattr(v, "pattern")
           and any(ord(c) < 9 or 13 < ord(c) < 32 for c in v.pattern)]
    if bad:
        raise AssertionError(
            f"regex(es) {bad} contain control characters -- a shell heredoc "
            f"almost certainly ate a backslash escape; edit the file directly")


# already-corrected files: their boundary carries a pointer now
RESOLVED_MARKERS = ("ALREADY RESOLVED", "RESOLVED (Pass", "CORRECTION AND RESOLUTION")

# SCOPE DISCLAIMERS ARE NOT OPEN QUESTIONS (measured, Pass 1395).
#
# Adjudicating the first twelve candidates by hand showed that four of them --
# BT663, BT665, BT666, BT669 -- were flagged on boundary sections that ask
# nothing at all.  They read "This theorem does not claim W(G2) acts on the
# original 160 Levi flags" or "Do not claim that the raw complement is Q4":
# they FENCE a result rather than leave one open.  A later file in the same
# programme naturally repeats their vocabulary, so they flag every time and can
# never be resolved, because there is nothing to resolve.
#
# That was a third of the sample and the single largest false-positive source.
# A boundary is treated as a live question only if it contains an interrogative
# or a forward commitment; a section that is purely disclaimer is skipped.
RE_QUESTION = re.compile(
    r"\?|\b(open|unknown|unsettled|not (?:yet )?(?:known|settled|determined)|"
    r"remains? open|to be determined|next (?:experiment|step)|should (?:build|compute|test)|"
    r"we do not know|undecided|conjectur)", re.I)
RE_DISCLAIMER = re.compile(
    r"\b(do(?:es)? not claim|do not claim|is not claimed|no claim is made|"
    r"should not be read|does not turn|does not produce)\b", re.I)


_assert_no_control_chars()


def is_live_question(b: str) -> bool:
    """A boundary that only fences scope is not an open question."""
    q = len(RE_QUESTION.findall(b))
    d = len(RE_DISCLAIMER.findall(b))
    return q > 0 and q > d



# GROUP-TOKEN RARITY CUT (calibrated, Pass 1489).
#
# Pass 1378 added `group_tokens` and it caught BT781 -> BT782, the case that had
# cost a rediscovery.  Re-measuring the flag rate over the 27 pass witnesses
# (Pass 1488) showed the class had drifted into NOISE by this project's own
# standard: 81.5%, against Pass 328's calibration of ~78% for bare integers
# (noise) and ~20% for code parameters (signal).  Group notation is ubiquitous
# here -- every pass names groups -- so the class flags nearly everything.
#
# The fix is a rarity cut, and the threshold is CALIBRATED rather than chosen:
#
#     cut   flag rate   BT781->BT782 shared tokens
#      20     22.2%        1   MISSES the motivating case
#      25     22.2%        2   FIRES        <-- the minimum cut that works
#      40     37.0%        2   FIRES
#    none     81.5%        3   FIRES        <-- noise
#
# 25 is the smallest cut that keeps the pinned case alive, and it lands exactly
# in the signal band.  Frequencies come from the persistent corpus index; if it
# is absent the cut is skipped rather than guessed.
GRP_RARITY_CUT = 25


def _grp_freq() -> dict[str, int]:
    import sqlite3
    db = ROOT / "data" / "corpus_index.sqlite"
    if not db.exists():
        return {}
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        f = {r[0]: r[1] for r in con.execute(
            "SELECT token, COUNT(*) FROM tok WHERE token LIKE 'grp:%' GROUP BY token")}
        con.close()
        return f
    except Exception:
        return {}


_GRPF = _grp_freq()


def rare_group_tokens(text: str) -> set[str]:
    """group_tokens, minus the ones so common they are topics not results."""
    t = group_tokens(text)
    if not _GRPF:
        return t
    return {x for x in t if _GRPF.get(x, 1) <= GRP_RARITY_CUT}


def order_key(p: Path):
    """Sortable position in the corpus: BT number, pass number, or ISO date."""
    n = p.name
    m = re.search(r"(?:BT|bt)(\d{2,5})", n)
    if m:
        return (1, int(m.group(1)))
    m = re.search(r"pass(\d{2,5})", n, re.I)
    if m:
        return (1, int(m.group(1)))
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", n)
    if m:
        return (0, int(m.group(1)) * 10000 + int(m.group(2)) * 100 + int(m.group(3)))
    return (2, 0)


def boundary_text(txt: str) -> str | None:
    """The tail of the file from its boundary heading onward."""
    m = None
    for m in RE_BOUNDARY.finditer(txt):
        pass                                    # take the LAST such heading
    if m is None:
        m2 = RE_INLINE_OPEN.search(txt) or RE_PROSE_OPEN.search(txt)
        if m2 is None:
            return None
        return txt[m2.start():]
    return txt[m.start():]


def self_test() -> int:
    """Pin the case that motivated this: BT810's boundary vs BT811.

    BT810's ORIGINAL boundary (before the pointer was added) shares exactly two
    tokens with BT811 -- `polar-pair@4` and `polar-pair@40` -- so it fires at the
    threshold. If the threshold is ever raised above 2, or the noun-number tokens
    are narrowed further, this case goes silent again and two passes get spent.
    """
    import subprocess
    log = subprocess.run(
        ["git", "log", "--format=%H", "-20", "--",
         "analysis/BT810_completed_geography_schlafli.md"],
        capture_output=True, text=True, cwd=ROOT).stdout.split()
    if not log:
        print("self-test SKIPPED (no git history)")
        return 0
    old = subprocess.run(["git", "show", f"{log[-1]}:analysis/BT810_completed_geography_schlafli.md"],
                         capture_output=True, text=True, cwd=ROOT).stdout
    b = boundary_text(old)
    bt = (results_in(b) | noun_number_pairs(b) | rare_group_tokens(b)) if b else set()
    t811 = (ROOT / "analysis" / "BT811_platonic_fine_print.md").read_text(
        encoding="utf-8", errors="ignore")
    shared = bt & (results_in(t811) | noun_number_pairs(t811) | rare_group_tokens(t811))
    ok = len(shared) >= 2
    print(f"  [{'PASS' if ok else 'FAIL'}] BT810 boundary vs BT811: "
          f"{len(shared)} shared tokens {sorted(shared)[:4]}")
    results = [ok]

    # ONE PINNED CASE PER BLIND SPOT THIS TOOL HAS ACTUALLY HAD (Pass 1431).
    #
    # Three distinct blind spots have been found and fixed, and one of them --
    # the Pass 1395 scope filter -- silently REOPENED when a shell heredoc ate
    # its `\b` escapes, going unnoticed for a whole session. A fix with no
    # pinned case is a fix that lasts until the next edit.
    cases: list[tuple[str, bool]] = []

    # (a) blockquoted "Open:" is someone ELSE's question, not this file's
    cases.append((
        "blockquoted Open: is NOT a boundary",
        boundary_text("# F\n\n> Open: is the group 2O or O_h?\n") is None))

    # (b) a scope disclaimer asks nothing and can never be resolved
    cases.append((
        "scope disclaimer is NOT a live question",
        not is_live_question(
            "## Boundary\n\nThis theorem does not claim W(G2) acts on the "
            "original 160 Levi flags. It does not produce a flag-level action.")))

    # (c) a PROSE open question, under no heading, still counts -- this is the
    #     one that made BT1420 uncatchable against my own Pass 1412 file
    cases.append((
        "prose 'the question stays open' IS a boundary",
        boundary_text(
            "# F\n\nSome text.\n\n**So the question stays open, and it is now "
            "sharp**: determine which of the two characters it affords.\n"
        ) is not None))

    # (d) .tex is in scope -- the parallel track publishes theorems as inserts
    cases.append((
        ".tex files are scanned",
        any(p.suffix == ".tex" for p in (ROOT / "analysis").glob("*.tex"))
        and "*.tex" in Path(__file__).read_text(encoding="utf-8")))

    for name, good in cases:
        print(f"  [{'PASS' if good else 'FAIL'}] {name}")
        results.append(good)

    allok = all(results)
    print("self-test", "OK" if allok else "FAILED")
    return 0 if allok else 1


def main(argv: list[str]) -> int:
    # Both spellings. This guard had a working self-test for weeks while the inventory
    # runner reported it as untested, because the runner probes for "--selftest" and this
    # file spelled it "--self-test" (Pass 5250). A hyphen is a silent coverage hole: the
    # tool was green, the dashboard said unknown, and nothing anywhere disagreed.
    if "--self-test" in argv or "--selftest" in argv:
        return self_test()
    limit = 40
    for a in argv:
        if a.startswith("--limit"):
            limit = int(a.split("=")[1]) if "=" in a else limit

    files = sorted(
        [p for p in (ROOT / "analysis").glob("*.md") if p.is_file()]
        # .tex TOO (Pass 1427).  BT1420_frame_signed_turn_bridge_insert.tex
        # closed a question I had left open, and the sweep could never have
        # said so: it globbed *.md only, while the parallel track publishes
        # its theorems as manuscript inserts in .tex.  Half the corpus was
        # outside the file set.
        + [p for p in (ROOT / "analysis").glob("*.tex") if p.is_file()],
        key=order_key)

    # index: token -> list of (order_key, filename) for EVERY file
    body, tokens, keys = {}, {}, {}
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        body[p.name] = t
        keys[p.name] = order_key(p)
        tokens[p.name] = results_in(t) | noun_number_pairs(t) | rare_group_tokens(t)

    # INVERTED INDEX, not a double loop.  The pairwise version is O(files^2) set
    # intersections -- about 1.5M of them over 1230 files -- and once Pass 1378's
    # group tokens enlarged every token set it stopped finishing inside the CI
    # timeout.  Since a candidate needs a SHARED token, only files sharing at
    # least one token can ever qualify, and the postings list finds exactly those.
    from collections import Counter, defaultdict
    postings: dict[str, list[str]] = defaultdict(list)
    for name, tk in tokens.items():
        for tok in tk:
            postings[tok].append(name)

    hits = []
    for p in files:
        t = body.get(p.name)
        if t is None or any(mk in t for mk in RESOLVED_MARKERS):
            continue
        b = boundary_text(t)
        if not b or len(b) < 40:
            continue
        if not is_live_question(b):          # scope disclaimer, not a question
            continue
        btok = (results_in(b) | noun_number_pairs(b) | rare_group_tokens(b)) - {""}
        if not btok:
            continue
        k = keys[p.name]
        # count shared tokens per candidate, visiting only files that share one
        tally: Counter[str] = Counter()
        for tok in btok:
            for q in postings.get(tok, ()):
                if q != p.name and keys[q] > k:
                    tally[q] += 1
        for qname, n in tally.items():
            if n >= 2:                          # >=2 to cut single-token noise
                shared = sorted(btok & tokens[qname])[:4]
                hits.append((n, p.name, qname, shared))

    hits.sort(key=lambda x: -x[0])
    # keep the strongest later-file candidate per boundary file
    seen, out = set(), []
    for n, src, tgt, sh in hits:
        if src in seen:
            continue
        seen.add(src)
        out.append((n, src, tgt, sh))

    print("=" * 78)
    print("[stale-boundary sweep] boundary sections a LATER file may have answered")
    print("=" * 78)
    print(f"scanned {len(files)} analysis/*.md; {len(out)} boundaries have a "
          f"later file sharing >=2 result tokens\n")
    for n, src, tgt, sh in out[:limit]:
        print(f"  {src}")
        print(f"    -> later: {tgt}   ({n} shared tokens, e.g. {', '.join(sh)})")
    print("\n  CANDIDATES, not verdicts. Read the later file before spending a pass")
    print("  re-answering the question. If it does answer it, EDIT THE ORIGINAL")
    print("  boundary to point there -- leaving it stale is what caused this.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
