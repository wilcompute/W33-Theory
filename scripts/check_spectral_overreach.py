#!/usr/bin/env python3
"""Flag claims that a SPECTRAL bound DETERMINES a combinatorial quantity.

WHY THIS EXISTS.  Passes 5228-5229 built a counterexample rather than quoting one:
W(3,3) and Q(4,3) are dual generalised quadrangles of order (3,3), so their
collinearity graphs are both SRG(40,12,2,4) -- literally the same spectrum, hence
literally the same Hoffman bound of 10.  And

    alpha(Q(4,3)) = 10        the bound is attained
    alpha(W(3,3)) =  7        the bound is slack

Two graphs, one spectrum, two independence numbers.

So "the Hoffman bound gives alpha" is false as stated, and it is false in this corpus,
on the substrate this corpus is about, at the smallest interesting q.  A second
instance follows from H(3,9)/Q(5,3), which are NOT cospectral yet share the bound 28
because st+1 is invariant under the duality that swaps s and t -- one attains it, one
cannot.

THE SLACK IS NOT "EXACTLY q", AND THIS FILE SAID THAT IT WAS IN ITS FIRST VERSION.
Pass 4800 refuted that law ~450 passes ago with alpha(W(3,5)) = 18, a deficit of 8
rather than 5.  The deficit is 3 at q=3 and 8 at q=5; it is neither q nor constant,
and Pass 4800 owns the refutation.  This guard found that file during the Pass 5274
corpus sweep -- which is how its own docstring came to be corrected by it.

WHAT THIS ACTUALLY CATCHES, and it is narrow on purpose.  Language asserting that a
spectral quantity DETERMINES, EQUALS, or GIVES a combinatorial one.  Not language
that BOUNDS it -- "Hoffman gives alpha <= 10" is correct and must never be flagged,
because that is the true content of the bound and flagging it would train people to
ignore this guard.  The distinction being tested is determination versus bounding,
which is a verb, not a topic.

    py -3 scripts/check_spectral_overreach.py <files>
    py -3 scripts/check_spectral_overreach.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SPECTRAL = r"(?:hoffman|ratio bound|spectral bound|spectrum|eigenvalue[s]?|delsarte)"
QUANTITY = r"(?:alpha|independence number|clique number|chromatic number|coclique)"
# Determination verbs ONLY. "bounds", "caps", "limits", "<=" are correct usage.
DETERMINES = r"(?:determines?|equals?|gives? the|is exactly|fixes|pins down|=)"

RULES = {
    "spectral_determines_combinatorial": re.compile(
        SPECTRAL + r".{0,60}\b" + DETERMINES + r"\b.{0,40}" + QUANTITY,
        re.I | re.S),
    "combinatorial_determined_by_spectral": re.compile(
        QUANTITY + r".{0,50}(?:is|are)\s+(?:determined|fixed|given)\s+by.{0,40}" + SPECTRAL,
        re.I | re.S),
    "cospectral_implies_equal_alpha": re.compile(
        r"cospectral.{0,80}(?:same|equal|identical).{0,30}" + QUANTITY,
        re.I | re.S),
}

# Phrases that make a sentence CORRECT rather than an over-read. Presence of any of
# these in the local window suppresses the finding.
SAFE = re.compile(
    r"(?:<=|\\le\b|\\leq\b|at most|upper bound|bounds?\b|caps?\b|not attained|"
    r"need not|slack|is not a spectral invariant|does not determine)", re.I)


def scan_text(text: str) -> list[tuple[str, int, str]]:
    out = []
    # split("\n"), not splitlines(): the latter treats formfeed and vertical tab as line
    # breaks and shifts every reported line number past such a byte (Pass 4929).
    lines = text.split("\n")
    for name, rx in RULES.items():
        for m in rx.finditer(text):
            lo = max(0, m.start() - 200)
            window = text[lo:m.end() + 200]
            if SAFE.search(window):
                continue
            ln = text.count("\n", 0, m.start()) + 1
            snippet = lines[ln - 1].strip()[:100] if ln - 1 < len(lines) else ""
            out.append((name, ln, snippet))
    return out


def selftest() -> int:
    cases = [
        ("planted: spectrum determines alpha",
         "The spectrum determines alpha for these graphs.", True),
        ("planted: alpha determined by eigenvalues",
         "alpha is determined by the eigenvalues of the graph.", True),
        ("planted: cospectral implies same alpha",
         "Two cospectral graphs have the same independence number.", True),
        ("clean: Hoffman BOUNDS alpha",
         "Hoffman gives alpha <= 10 for this graph.", False),
        ("clean: explicit upper bound",
         "The spectral bound is an upper bound on alpha, at most 26.", False),
        ("clean: the correct negative",
         "alpha is not a spectral invariant; the spectrum determines alpha "
         "in neither direction.", False),
        ("clean: unrelated prose",
         "The ovoid has q^2+1 points and the polarity is a coset walk.", False),
    ]
    ok = True
    print("  selftest -- determination-versus-bounding recall\n")
    for name, text, want in cases:
        got = bool(scan_text(text))
        good = got == want
        ok &= good
        print(f"    {name:38s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE TWO CLEAN BOUND CASES ARE WHY THIS GUARD IS USABLE. "Hoffman gives alpha <= 10" is
  the CORRECT statement of the ratio bound and appears throughout this corpus; a checker
  that flagged it would fire on every legitimate use and be switched off within a day. What
  is flagged is the verb -- determines, equals, is fixed by -- not the topic.

  ITS LIMIT, and it is a real one: this reads sentences, not mathematics. A pass that
  computes alpha correctly and describes it loosely gets flagged, and a pass that is
  genuinely wrong while phrasing it carefully does not. It is a prompt to check, never a
  verdict -- the counterexample it is built on took two lanes and four passes to assemble,
  and no regex was going to find it.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [Path(a) for a in argv if not a.startswith("-")]
    total = 0
    for f in files:
        if not f.is_file():
            continue
        # Do not scan self: this file contains planted fixtures by construction, and a
        # checker flagging its own test data is noise that trains people to ignore it
        # (2 of 6 candidates in the Pass 5274 full-corpus sweep were exactly this).
        if f.resolve() == Path(__file__).resolve():
            continue
        try:
            hits = scan_text(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for name, ln, snip in hits:
            total += 1
            try:
                rel = f.resolve().relative_to(ROOT).as_posix()
            except ValueError:
                rel = f.as_posix()
            print(f"  {rel}:{ln}  [{name}]\n      {snip}")
    print(f"\n  {total} candidate spectral over-read(s) in {len(files)} file(s)")
    if total:
        print("""
  These are CANDIDATES. The counterexample behind this guard is Pass 5228: W(3,3) and
  Q(4,3) are both SRG(40,12,2,4) with alpha 7 and 10. If a flagged sentence means "bounds",
  reword it; if it means "determines", it is claiming something that substrate refutes.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
