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

# already-corrected files: their boundary carries a pointer now
RESOLVED_MARKERS = ("ALREADY RESOLVED", "RESOLVED (Pass", "CORRECTION AND RESOLUTION")


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
        m2 = RE_INLINE_OPEN.search(txt)
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
    bt = (results_in(b) | noun_number_pairs(b) | group_tokens(b)) if b else set()
    t811 = (ROOT / "analysis" / "BT811_platonic_fine_print.md").read_text(
        encoding="utf-8", errors="ignore")
    shared = bt & (results_in(t811) | noun_number_pairs(t811) | group_tokens(t811))
    ok = len(shared) >= 2
    print(f"  [{'PASS' if ok else 'FAIL'}] BT810 boundary vs BT811: "
          f"{len(shared)} shared tokens {sorted(shared)[:4]}")
    print("self-test", "OK" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return self_test()
    limit = 40
    for a in argv:
        if a.startswith("--limit"):
            limit = int(a.split("=")[1]) if "=" in a else limit

    files = sorted(
        [p for p in (ROOT / "analysis").glob("*.md") if p.is_file()],
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
        tokens[p.name] = results_in(t) | noun_number_pairs(t) | group_tokens(t)

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
        btok = (results_in(b) | noun_number_pairs(b) | group_tokens(b)) - {""}
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
