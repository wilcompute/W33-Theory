#!/usr/bin/env python3
r"""Find regex alternatives that can never match.  Pass 4742.

WHY THIS EXISTS
---------------
Pass 4735 reported that 12.5% of 51,840 sightings name their object.  The real figure is
44%.  The pattern ended in `\b`, and every alternative ending in `)` -- `Sp(4,3)`,
`W(E_6)`, `PSU(4,2)` -- became unmatchable, because `)` is a non-word character and so is
the space after it, so there is no boundary between them.  The checker produced a statistic
about naming discipline while structurally unable to see the names.

That is a bug class, not an incident: a `\b` adjacent to a non-word character is a dead end,
and it fails SILENTLY.  The regex compiles, runs, and returns fewer matches.  Nothing in a
test suite distinguishes "no matches because the corpus is clean" from "no matches because
the pattern cannot match."

WHAT IT DOES
------------
Extracts every `re.compile` pattern in a file, splits it on top-level alternation, and for
each alternative asks whether a leading or trailing `\b` sits against a literal non-word
character.  Those are reported as dead ends.

    py -3 scripts/check_regex_deadends.py --selftest
    py -3 scripts/check_regex_deadends.py [paths...]
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NONWORD = set(r"()[]{}.,:;!?/\\|+*=<>\"'%$#@~^&- ")


def split_alternatives(pat: str):
    """Split on | at paren depth 0, outside character classes."""
    out, buf, depth, incls, i = [], [], 0, False, 0
    while i < len(pat):
        c = pat[i]
        if c == "\\" and i + 1 < len(pat):
            buf.append(pat[i:i + 2])
            i += 2
            continue
        if incls:
            if c == "]":
                incls = False
        elif c == "[":
            incls = True
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "|" and depth == 0:
            out.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    out.append("".join(buf))
    return out


def dead_ends(pattern: str):
    r"""Alternatives whose \b sits against a LITERAL non-word character.

    THE DISTINCTION THAT MAKES THIS WORK, and that the first version got wrong: an
    ESCAPED paren `\)` is a literal ')' in the subject text, so `\)\b` can never match.
    A bare `)` is a group close -- pure syntax, matching nothing -- so `(?:alpha|beta)\b`
    is perfectly fine, because the character actually preceding the boundary is 'a'.

    Treating the two the same flags every well-formed `\b(?:...)\b` in the repository.
    The first version did exactly that and reported 124 hits, nearly all of them correct
    patterns -- the same confusion of syntax for content that produced the bug it hunts.
    """
    bad = []
    for alt in split_alternatives(pattern):
        core = alt.strip()
        if core.endswith(r"\b"):
            for frag in _terminal_fragments(core[:-2], last=True):
                t = re.search(r"(\\?)(.)$", frag)
                if t and t.group(1) == "\\" and t.group(2) in NONWORD:
                    bad.append(("trailing", frag[-40:]))
        if core.startswith(r"\b"):
            for frag in _terminal_fragments(core[2:], last=False):
                h = re.match(r"(\\?)(.)", frag)
                if h and h.group(1) == "\\" and h.group(2) in NONWORD:
                    bad.append(("leading", frag[:40]))
    return bad


def _terminal_fragments(core: str, last: bool):
    r"""The pieces of text that can sit adjacent to a \b, looking through group syntax.

    A trailing \b after `(?:A|B|C)` applies to whichever of A, B, C matched, so each must
    be examined -- this is exactly the case the 51,840 pattern hit, where two of three
    alternatives ended in an escaped paren and the third did not.
    """
    core = core.strip()
    if not core:
        return []
    if last and core.endswith(")"):
        depth = 0
        for i in range(len(core) - 1, -1, -1):
            if core[i] == ")" and (i == 0 or core[i - 1] != "\\"):
                depth += 1
            elif core[i] == "(" and (i == 0 or core[i - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    inner = re.sub(r"^\(\?[:=!<]*P?<?\w*>?", "", core[i:-1]).lstrip("(")
                    return [a.strip() for a in split_alternatives(inner) if a.strip()]
        return [core]
    if (not last) and core.startswith("("):
        depth = 0
        for i, c in enumerate(core):
            if c == "(" and (i == 0 or core[i - 1] != "\\"):
                depth += 1
            elif c == ")" and (i == 0 or core[i - 1] != "\\"):
                depth -= 1
                if depth == 0:
                    inner = re.sub(r"^\(\?[:=!<]*P?<?\w*>?", "", core[:i + 1])[:-1]
                    return [a.strip() for a in split_alternatives(inner) if a.strip()]
        return [core]
    return [core]


PATTERN_RE = re.compile(r"re\.compile\(\s*((?:r?[\"'][^\"']*[\"']\s*)+)", re.S)
STRING_RE = re.compile(r"r?[\"']([^\"']*)[\"']")


def scan_file(p: Path):
    t = p.read_text(encoding="utf-8", errors="replace")
    out = []
    # A raw control byte in a source file is always a mistake, and this one is specific:
    # a shell heredoc collapses the two characters \b into a single 0x08 BACKSPACE. The
    # regex still compiles -- it now requires a literal backspace in the subject text, so
    # the alternative can never match. Invisible to the \b analysis below, because there
    # is no \b left to analyse. Found in this repository's own layer checker, where it had
    # silently disabled four vocabulary tokens.
    for i, line in enumerate(t.splitlines(), 1):
        for ch, name in (("\x08", "backspace (was \\b)"), ("\x0c", "formfeed (was \\f)"),
                         ("\x07", "bell (was \\a)"), ("\x0b", "vtab (was \\v)")):
            if ch in line:
                out.append({"line": i, "kind": f"CONTROL BYTE: {name}",
                            "fragment": line.replace(ch, "<CTRL>").strip()[:60]})
    for m in PATTERN_RE.finditer(t):
        parts = STRING_RE.findall(m.group(1))
        pat = "".join(parts)
        if r"\b" not in pat:
            continue
        for kind, frag in dead_ends(pat):
            ln = t[:m.start()].count("\n") + 1
            out.append({"line": ln, "kind": kind, "fragment": frag})
    return out


PLANT_BAD = '''
NAMES = re.compile(r"\\b(?:Sp\\(4,3\\)|W\\(E_?6\\)|Weyl)\\b", re.I)
'''
PLANT_GOOD = '''
NAMES = re.compile(r"(?:Sp\\(4,3\\)|W\\(E_?6\\)|\\bWeyl\\b)", re.I)
'''
PLANT_GOOD2 = '''
WORDS = re.compile(r"\\b(?:alpha|beta|gamma)\\b")
'''
# a heredoc-mangled \b: the two characters collapsed into one 0x08 byte
PLANT_CTRL = 'TOK = re.compile(r"' + chr(8) + 'alpha' + chr(8) + '")\n"'


def selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="rx_"))
    cases = [("planted: trailing \\b after )", PLANT_BAD, True),
             ("planted: heredoc-mangled \\b (0x08)", PLANT_CTRL, True),
             ("clean: \\b moved inside", PLANT_GOOD, False),
             ("clean: all-word alternatives", PLANT_GOOD2, False)]
    ok = True
    print("  selftest -- planted-fault recall\n")
    for name, src, want in cases:
        f = tmp / (name.split(":")[0].replace(" ", "_") + ".py")
        f.write_text(src, encoding="utf-8")
        got = bool(scan_file(f))
        good = got == want
        ok &= good
        print(f"    {name:34s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print(r"""
  The two clean cases matter more than the planted one. The first is the SAME pattern with
  \b moved inside the word-only alternatives, which is the actual fix -- a checker that
  still flagged it would be reporting on the presence of \b next to a paren anywhere in the
  line. The second is an ordinary correct pattern that must stay silent.

  ITS LIMIT: it reasons about literal characters only. A \b against a character class or a
  backreference may or may not be a dead end depending on what that class contains, and
  those are not analysed.""")
    import shutil
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    paths = [Path(p) for p in a.paths] if a.paths else sorted(
        list((ROOT / "scripts").glob("*.py")) + list((ROOT / "analysis").rglob("*.py")))
    total = 0
    for p in paths:
        if not p.is_file() or p.suffix != ".py":
            continue
        for h in scan_file(p):
            total += 1
            rel = p.relative_to(ROOT).as_posix() if ROOT in p.parents else p.name
            print(f"  {rel}:{h['line']}  {h['kind']} \\b against a non-word literal")
            print(f"      ...{h['fragment']}")
    print(f"\n  {total} unmatchable alternatives")
    if total == 0:
        print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
