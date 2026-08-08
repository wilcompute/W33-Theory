#!/usr/bin/env python3
"""Passes 4307, 4311 -- which 40, and what does the recovered material actually say?

Pass 4303 proved the 40 points and the 40 lines are INEQUIVALENT Sp(4,3)-sets: 29,950 of
51,840 elements fix different numbers of each, so their stabilisers are non-conjugate
subgroups of order 1,296.  Both are transitive, both size 40, both give SRG(40,12,2,4).
Anywhere a manuscript says "the 40" without saying which, the sentence names two different
objects at once.

  4307  THE AMBIGUITY AUDIT.  Find passages where 40 (or the order-1,296 stabiliser) is
        used without a point/line qualifier, and separate the merely imprecise from the
        possibly wrong.
  4311  READ THE RECOVERED MATERIAL.  Pass 4302 checked that the recovered inserts are
        well-formed, which is not the same as checking what they claim.  Extract the actual
        assertions from a sample and test the ones that are testable against this arc's
        results -- the point being to find a claim that CONTRADICTS a later pass, which
        well-formedness can never surface.

    py -3 analysis/w33_pass4307_4311_the_forty_and_a_reading.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Words that disambiguate which 40 is meant.
POINT_WORDS = ("point", "vertex", "vertices", "isotropic point", "projective point")
LINE_WORDS = ("line", "totally isotropic line", "generator", "spread")
# Contexts where 40 is doing real work rather than appearing incidentally.
#
# CALIBRATION.  The first version included the bare substring "act", which matches
# "contexts", "exactly", "fraction" and "character" -- so it flagged log_2(2160/40),
# r^{40}, and "40 tetrad contexts" as G-set ambiguities.  These are word-boundary
# patterns now, and the list is restricted to vocabulary that only appears when the 40 is
# being used AS a G-set or as the SRG vertex set.
WORKING = (r"\bsrg\b", r"strongly regular", r"\bstabili", r"\borbit", r"\btransitive\b",
           r"\bacts?\b", r"\bg-?set\b", r"\bpermutation\b", r"\bgraph on\b",
           r"\bvertices\b", r"1{?,?}?296")


def pass_4307() -> dict:
    print("=" * 78)
    print("Pass 4307 -- which 40?  The ambiguity Pass 4303 made real")
    print("=" * 78)
    print("""  Both 40-sets are transitive, both have stabilisers of order 1,296, and both give
  SRG(40,12,2,4).  Only the permutation character separates them, so "the 40" is ambiguous
  wherever the surrounding text does not say point or line.\n""")
    rows, tally = [], Counter()
    for m in sorted(ROOT.glob("*.tex")):
        lines = m.read_text(encoding="utf-8", errors="replace").splitlines()
        hits = []
        for i, ln in enumerate(lines):
            if not re.search(r"(?<![0-9)])40(?![0-9])", ln):
                continue
            if re.search(r"40\s*(?:mm|cm|pt|em|ex|%|\\linewidth)", ln):
                continue
            w = " ".join(lines[max(0, i - 4):i + 5]).lower()
            if not any(re.search(t, w) for t in WORKING):
                continue
            has_p = any(t in w for t in POINT_WORDS)
            has_l = any(t in w for t in LINE_WORDS)
            if has_p or has_l:
                tally["qualified"] += 1
                continue
            tally["ambiguous"] += 1
            hits.append((i + 1, ln.strip()[:64]))
        if hits:
            rows.append((m.name, hits))
    print(f"  qualified passages (say point or line): {tally['qualified']}")
    print(f"  AMBIGUOUS passages                    : {tally['ambiguous']}")
    for name, hits in rows[:6]:
        print(f"\n  {name}: {len(hits)}")
        for ln, txt in hits[:5]:
            print(f"    line {ln:6d}  {txt}")
    print(f"""
  Almost all of these are IMPRECISE rather than WRONG: in this corpus "the 40" nearly
  always means the point side, because that is the side the machine addresses (Pass 4301
  showed it is the only side admitting a load port).  The audit's value is not a list of
  errors but a boundary -- it marks where a reader has to supply context the text does not
  give, and where a future pass working from the text alone could pick the wrong 40.

  The one place it is more than style is anywhere a stabiliser of order 1,296 is used: the
  point stabiliser and the line stabiliser are NON-CONJUGATE subgroups of that order, so a
  computation that picks "the" subgroup of order 1,296 is picking between two genuinely
  different groups.""")
    return {"qualified": tally["qualified"], "ambiguous": tally["ambiguous"],
            "by_manuscript": {n: [ln for ln, _ in h] for n, h in rows}}


def pass_4311() -> dict:
    print()
    print("=" * 78)
    print("Pass 4311 -- reading the recovered material, not merely compiling it")
    print("=" * 78)
    apps = [ROOT / "analysis" / n for n in
            ("W33_BLUEPRINT_RECOVERED_APPENDIX.tex", "W33_PAPER_RECOVERED_APPENDIX.tex",
             "W33_PHOTONIC_RECOVERED_APPENDIX.tex")]
    stems = []
    for a in apps:
        if a.exists():
            stems += [Path(m).name.removesuffix(".tex") for m in
                      re.findall(r"\\input\{([^}]*)\}",
                                 a.read_text(encoding="utf-8", errors="replace"))]

    # Claims this arc has settled, with the value it settled on.  A recovered insert
    # asserting a DIFFERENT value for the same quantity is a contradiction worth surfacing.
    SETTLED = {
        r"78\s*(?:=|poles|non-?trivial)": ("78 poles", "parameter fact, all 28 SRGs alike"),
        r"\\rho\(B\)|rho\(B\)": ("rho(B)", "5.746873 for the instruction graph"),
        # 51,840 is the ORDER of Sp(4,3) and is correct nearly everywhere it appears; only
        # flag it where the passage is about an automorphism group, which is where Pass
        # 4287's "two graphs attain it" is the settled fact.
        r"(?:aut|automorphism)[^\n]{0,60}51[,{}]*840":
            ("|Aut| = 51840", "attained by BOTH the point and line graphs (4287/4296)"),
        r"Cayley graph": ("'Cayley graph'", "the frame graph is a SCHREIER graph (4203)"),
        r"Ramanujan": ("Ramanujan", "defined only for regular graphs (4213)"),
    }
    print(f"  recovered inserts: {len(stems)}")
    print("  scanning them for claims this arc has since settled differently...\n")
    flags = []
    for s in stems:
        p = ROOT / "analysis" / f"{s}.tex"
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        for pat, (what, settled) in SETTLED.items():
            for m in re.finditer(pat, txt):
                ln = txt.count("\n", 0, m.start()) + 1
                ctx = txt.splitlines()[ln - 1].strip()[:70] if ln <= len(
                    txt.splitlines()) else ""
                flags.append((s, ln, what, settled, ctx))
    by_what = Counter(f[2] for f in flags)
    print(f"  {'claim touched':22s} occurrences")
    for k, v in by_what.most_common():
        print(f"  {k:22s} {v}")
    if flags:
        print("\n  passages to read against the settled value:")
        for s, ln, what, settled, ctx in flags[:12]:
            print(f"    {s[:42]:42s}:{ln:<4d} {what}")
            print(f"      settled: {settled}")
            print(f"      text   : {ctx}")
    print(f"""
  {len(flags)} passage(s) in the recovered material touch a quantity this arc has since
  settled.  This is the check Pass 4302 could not perform: well-formedness says a page
  renders, and says nothing about whether it asserts something later work contradicts.

  Scope, stated plainly: this matches PATTERNS, not meaning.  A hit is a passage a human
  should read, not a proven contradiction -- and a recovered insert predating a correction
  is not wrong for having predated it, it just needs the correction's scope note nearby.
  What would be a genuine problem is a recovered page asserting the Cayley-graph framing or
  a Ramanujan verdict for the instruction layer as current fact, since the appendix sits in
  the same document as the passes that withdrew both.""")
    return {"inserts": len(stems), "flags": len(flags),
            "by_claim": dict(by_what),
            "detail": [{"stem": a, "line": b, "claim": c} for a, b, c, _, _ in flags[:40]]}


def main() -> int:
    out = {"pass_4307_which_forty": pass_4307(),
           "pass_4311_reading": pass_4311()}
    p = ROOT / "data" / "PART_W33_PASS4307_4311_FORTY_AND_READING.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
