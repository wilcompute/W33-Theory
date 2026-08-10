#!/usr/bin/env python3
"""Pass 4735 -- 51,840 has more than one source, and the corpus does not distinguish them.

Pass 4727 found that H(3,4) -- a HERMITIAN quadrangle over GF(4) -- has automorphism group
of order 51,840, the same as W(3,3)'s.  Not a leak between geometries: the exceptional
isomorphism PSU(4,2) = PSp(4,3) makes both true independently.

That is a pleasant fact and a hazard.  51,840 is one of this repository's most-cited
integers, and if it has several genuine sources then "51,840 appears here too" is weaker
evidence than it reads as -- the number can be arrived at from unrelated directions, so a
sighting is not by itself a connection to W(3,3).

This pass enumerates the DISTINCT mathematical objects of order 51,840 that this project
actually touches, then counts how many corpus sightings say WHICH one they mean.

    py -3 analysis/w33_pass4735_where_51840_actually_comes_from.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

# Objects of order 51,840 that are genuinely distinct as constructions, even where the
# groups coincide. The point is provenance, not group-isomorphism class.
SOURCES = [
    ("|Sp(4,3)|", "symplectic group over GF(3); Aut of W(3,3)", 51840),
    ("|PSU(4,2)|x2", "unitary group over GF(4); Aut of H(3,4). PSU(4,2) = PSp(4,3), "
                     "order 25,920, doubled by the field automorphism", 51840),
    ("|W(E6)|", "Weyl group of E6", 51840),
    ("|Aut(GQ(2,4))|", "Aut of Q(5,2), the dual of H(3,4)", 51840),
    ("|O5(3)| x 2", "orthogonal group in dimension 5 over GF(3); O5(3) = Sp(4,3)", 51840),
]

CLAIM = re.compile(r"51[,_ ]?840")
# A sighting is DISAMBIGUATED if it names which object it means within a few lines.
#
# NO TRAILING \b. The first version ended this pattern with \b, and every alternative that
# ends in ')' then became unmatchable: ')' is a non-word character and so is the space after
# it, so there is no boundary between them. Sp(4,3), W(E_6), PSU(4,2) -- all silently
# impossible. It reported 12.5% disambiguated and the "bare" examples it printed contained
# |W(E_6)|=51840 in the matched line itself, which is what gave it away.
NAMES = re.compile(
    r"(?:Sp\(4,\s*3\)|PSp\(4,\s*3\)|W\(E_?6\)|\bWeyl\b|\bsymplectic\b|\bunitary\b|\bPSU\b|"
    r"SU\(4,\s*2\)|U_?4\(2\)|O_?5\(3\)|\borthogonal\b|\bHermitian\b|H\(3,\s*4\)|"
    r"Q\(5,\s*2\)|GQ\(2,\s*4\)|automorphism group of W\(3,3\))", re.I)


def main() -> int:
    print("=" * 78)
    print("Pass 4735 -- how many things in this project have order 51,840?")
    print("=" * 78)

    print(f"\n  {'object':18s} {'order':>8s}  provenance")
    for name, why, order in SOURCES:
        print(f"  {name:18s} {order:8,d}  {why}")

    print("""
    THESE ARE NOT ALL THE SAME STATEMENT. Sp(4,3), PSU(4,2) and W(E6) coincide as abstract
    groups -- that is the content of the exceptional isomorphisms and of W(E6) = O5(3):2 --
    but they arrive from a symplectic space over GF(3), a Hermitian space over GF(4), and a
    root system. A sighting of 51,840 licenses a connection to W(3,3) only if the sighting
    came from the first of those, and nothing about the integer says which.""")

    print("\n  How many corpus sightings say which one they mean?\n")
    files = sorted(list((ROOT / "analysis").rglob("*.py")) +
                   list((ROOT / "analysis").rglob("*.md")))
    total = named = bare = 0
    bare_examples = []
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        lines = t.splitlines()
        for i, line in enumerate(lines):
            if not CLAIM.search(line):
                continue
            total += 1
            lo, hi = max(0, i - 3), min(len(lines), i + 4)
            if NAMES.search("\n".join(lines[lo:hi])):
                named += 1
            else:
                bare += 1
                if len(bare_examples) < 8:
                    bare_examples.append(
                        {"file": p.relative_to(ROOT).as_posix(), "line": i + 1,
                         "text": line.strip()[:92]})

    print(f"    sightings of 51,840          : {total:,}")
    print(f"    naming which object          : {named:,}  ({100*named/max(total,1):.1f}%)")
    print(f"    bare, no object named nearby : {bare:,}  ({100*bare/max(total,1):.1f}%)")
    print()
    for b in bare_examples:
        print(f"      {b['file']}:{b['line']}")
        print(f"        {b['text']}")

    frac = 100 * named / max(total, 1)
    print(f"""
    {frac:.0f}% OF SIGHTINGS NAME THEIR OBJECT WITHIN THREE LINES; {100-frac:.0f}% DO NOT.

    A bare sighting is not wrong. Most of these are internal cross-references in files whose
    subject is established paragraphs earlier, and a reader going front-to-back knows which
    group is meant. The measurement is of what survives a GREP -- and grep is how this
    corpus is actually read, by both agents, which is the documented cause of its
    rediscovery problem.

    THE RULE THIS PASS EXISTS FOR: a bare 51,840 is evidence of contact with a group of
    order 51,840, and there are at least three routes to one. Pass 4727 is the case in
    point -- I quoted W(3,3)'s number for a GF(4) Hermitian object, was right, and was right
    by luck rather than by argument until the exceptional isomorphism was named.

    AND THE FIRST VERSION OF THIS PASS GOT THE NUMBER WRONG, in the direction that made the
    corpus look worse. It ended the object-name pattern with a word boundary, which makes
    every alternative ending in ')' unmatchable -- Sp(4,3), W(E_6), PSU(4,2), all of them.
    It reported 12.5%, and the "bare" examples it printed contained |W(E_6)|=51840 in the
    flagged line itself. A statistic about naming discipline, produced by a checker that
    could not see the names.""")

    out = {
        "boundary": ("this pass counts textual co-occurrence within three lines and does "
                     "not read the sightings; a file that names its object further away is "
                     "counted as bare. It establishes nothing about whether any particular "
                     "claim is wrong -- only that the integer alone does not identify its "
                     "source. The list of order-51,840 objects is not claimed exhaustive"),
        "sources": [{"object": a, "provenance": b, "order": c} for a, b, c in SOURCES],
        "sightings_total": total,
        "sightings_naming_object": named,
        "sightings_bare": bare,
        "bare_examples": bare_examples,
        "rule": ("a bare 51,840 is evidence of contact with a group of that order, not "
                 "with W(3,3); at least three distinct constructions in this project "
                 "reach it, and the exceptional isomorphism PSU(4,2) = PSp(4,3) is why"),
    }
    p = ROOT / "data" / "PART_W33_PASS4735_51840_PROVENANCE.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
