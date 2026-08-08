#!/usr/bin/env python3
"""Pass 4376 -- did any inserted box land somewhere that breaks the document?

Pass 4368 inserted plain-language boxes by finding "the first `}` after the heading text".
That is wrong whenever the heading itself contains braces: a section titled
`... $[[(q{+}1)(q^2{+}1), ...]]$ CSS family` has a `}` inside its own math, so the box
landed INSIDE the section argument and produced five LaTeX errors. An earlier insertion in
the same batch orphaned a full stop the same way.

Both are silent until compile time and neither is caught by the pitfall or label checkers,
so this exists as its own guard. Per CLAUDE.md failure mode 7, it ships with planted faults
it must detect.

Two families:
  inside-heading  -- braces are unbalanced between the nearest preceding sectioning
                     command and the box, so the box is inside the heading's argument.
  orphan-punct    -- the box is immediately followed by stray punctuation, which means it
                     was inserted mid-sentence.

    py -3 scripts/check_tex_insertions.py            # all manuscripts
    py -3 scripts/check_tex_insertions.py --selftest # prove it catches planted faults
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODIES = ["holonet_machine_blueprint_body.tex", "w33_paper_body.tex",
          "photonic_holonet_body.tex"]
SEC = re.compile(r"\\(?:sub)*section\*?\{")
BOXES = re.compile(r"\\begin\{(plain|spec|warn)(?:box)?\}")
ORPHAN = re.compile(r"\\end\{(?:plain|spec|warn)(?:box)?\}\s*\n\s*[.,;:]")


def scan_text(t: str):
    """(kind, line, context) for every suspect insertion."""
    out = []
    for m in BOXES.finditer(t):
        starts = [s.start() for s in SEC.finditer(t[:m.start()])]
        if not starts:
            continue
        seg = t[starts[-1]:m.start()]
        if seg.count("{") - seg.count("}") > 0:
            out.append(("inside-heading", t.count("\n", 0, m.start()) + 1,
                        re.sub(r"\s+", " ", seg[:70])))
    for m in ORPHAN.finditer(t):
        out.append(("orphan-punct", t.count("\n", 0, m.start()) + 1,
                    re.sub(r"\s+", " ", t[m.start():m.start() + 60])))
    return out


def selftest() -> int:
    good = (r"\section{A normal heading}" "\n"
            r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\nText.\n")
    planted_inside = (r"\section{Tricky $[[(q{+}1)(q^2{+}1)]]$ family}" "\n"
                      r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\n")
    # simulate the real bug: box inserted after the FIRST } (inside q{+})
    broken = (r"\section{Tricky $[[(q{+}" "\n"
              r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\n"
              r"1)(q^2{+}1)]]$ family}" "\n")
    orphan = (r"\subsection{Heading}" "\n"
              r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\n.\n")
    cases = [("clean", good, 0), ("inside-heading", broken, 1),
             ("orphan-punct", orphan, 1), ("balanced braces in heading", planted_inside, 0)]
    ok = True
    print("  selftest")
    for name, txt, want in cases:
        hits = scan_text(txt)
        got = len(hits)
        good_case = (got == want)
        ok &= good_case
        print(f"    {name:28s} expected {want}  got {got}  "
              f"{'PASS' if good_case else 'FAIL'}"
              + (f"   {hits[0][0]}" if hits else ""))
    print(f"""
  The 'balanced braces in heading' case matters as much as the broken one: a heading may
  legitimately contain braces, and a checker that flags every such heading would be
  switched off inside a week.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    total = 0
    for name in BODIES:
        p = ROOT / name
        if not p.exists():
            continue
        hits = scan_text(p.read_text(encoding="utf-8", errors="replace"))
        total += len(hits)
        print(f"  {name:38s} {len(hits)} suspect insertion(s)")
        for kind, line, ctx in hits:
            print(f"    line {line:6d}  {kind:16s} {ctx}")
    print(f"\n  total: {total}")
    if total:
        print("""
  An insertion inside a heading argument is a compile error; an orphaned full stop is not,
  and will sit in the PDF looking like a typo until someone reads that page.""")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
