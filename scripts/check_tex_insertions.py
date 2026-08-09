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

Four families.  The last two were added at Pass 4391, each after it shipped -- w33_paper
went from 484 pages to 172 and this checker reported zero the whole time, because neither
fault family existed yet.  That is failure mode 7 exactly, twice in one batch.

  inside-heading  -- braces are unbalanced between the nearest preceding sectioning
                     command and the box, so the box is inside the heading's argument.
  orphan-punct    -- the box is immediately followed by stray punctuation, which means it
                     was inserted mid-sentence.
  in-option-list  -- (4391) the box sits inside an environment's `[...]` option
                     list.  A box went into
                     `\begin{tcolorbox}[..., title=\textbf{The Final Theorem}` because the
                     insertion guard only asked whether the preceding command name was
                     alphabetic.  `\textbf` is alphabetic.  tcolorbox then read the prose
                     as a comma-separated key list.  Brace depth was balanced throughout,
                     so the inside-heading family could not see it.
  control-char    -- (4391) a raw control byte in the source.  Git Bash rewrote `\\b` inside
                     a quoted heredoc to `\b`, which Python read as BACKSPACE, so ten boxes
                     were written as chr(8) + "egin{plainbox}".  Invisible in every editor
                     and in every diff.

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
ENVOPT = re.compile(r"\\begin\{([A-Za-z*]+)\}\s*\[")
CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")


def _option_spans(t: str) -> list[tuple[int, int, str]]:
    """(start, end, env) for every `\\begin{env}[ ... ]` optional-argument group.

    Calibration note.  The first version of this family asked "is the command owning the
    brace group before the box a sectioning command?", which flagged 128 boxes in the live
    manuscripts -- every one of them legitimate, sitting after an \\end{...} or a \\textbf
    in running text.  A check with 128 false positives is a check nobody runs.  The actual
    fault is narrower and exactly detectable: the box is inside an OPTION LIST, where its
    prose gets parsed as comma-separated keys.
    """
    spans = []
    for m in ENVOPT.finditer(t):
        i = t.index("[", m.start())
        depth, brace, k = 0, 0, i
        while k < len(t):
            c = t[k]
            if c == "{":
                brace += 1
            elif c == "}":
                brace -= 1
            elif brace == 0 and c == "[":
                depth += 1
            elif brace == 0 and c == "]":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        if k < len(t):
            spans.append((i, k, m.group(1)))
    return spans


def scan_text(t: str):
    """(kind, line, context) for every suspect insertion."""
    out = []
    spans = _option_spans(t)
    for m in BOXES.finditer(t):
        line = t.count("\n", 0, m.start()) + 1
        starts = [s.start() for s in SEC.finditer(t[:m.start()])]
        if starts:
            seg = t[starts[-1]:m.start()]
            if seg.count("{") - seg.count("}") > 0:
                out.append(("inside-heading", line, re.sub(r"\s+", " ", seg[:70])))
                continue
        for a, b, env in spans:
            if a < m.start() < b:
                out.append(("in-option-list", line,
                            f"inside the [...] of \\begin{{{env}}} -- the prose will be "
                            f"parsed as keys"))
                break
    for m in ORPHAN.finditer(t):
        out.append(("orphan-punct", t.count("\n", 0, m.start()) + 1,
                    re.sub(r"\s+", " ", t[m.start():m.start() + 60])))
    for m in CONTROL.finditer(t):
        out.append(("control-char", t.count("\n", 0, m.start()) + 1,
                    f"byte 0x{ord(m.group()):02x} at column "
                    f"{m.start() - t.rfind(chr(10), 0, m.start())}"))
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
    # Pass 4391's two live faults, replanted from scratch (no shared bytes with the
    # originals, per the recall-test pattern in scripts/test_checker_recall.py).
    not_heading = (r"\begin{tcolorbox}[colback=blue!5!white," "\n"
                   r"  title=\textbf{The Final Theorem}" "\n"
                   r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\n]\n")
    control = (r"\section{A normal heading}" "\n\n" + chr(8) + "egin{plainbox}\n"
               "Body.\n" r"\end{plainbox}" "\n")
    after_label = (r"\subsection{Heading}\label{sec:x}" "\n"
                   r"\begin{plainbox}" "\nBody.\n" r"\end{plainbox}" "\nText.\n")
    cases = [("clean", good, 0), ("inside-heading", broken, 1),
             ("orphan-punct", orphan, 1), ("balanced braces in heading", planted_inside, 0),
             ("in-option-list", not_heading, 1), ("control-char", control, 1),
             ("box after \\label (legitimate)", after_label, 0)]
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
