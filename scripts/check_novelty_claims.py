#!/usr/bin/env python3
"""Refuse to let a novelty claim through without checking the encyclopedia.

Built at Pass 2743 after a MEASURED failure rate, not a hypothetical one. Five claims
in one session were overturned by documents the author had not read:

    Pass 2650  "two order-51840 groups" -- in photonic_holonet_body.tex's ABSTRACT
    Pass 2651  the fractal branching     -- the paper's own BT827 theorem, 40-ary
    Pass 2652  the E6 cubic's space      -- the paper states 27 = 3(x)3(x)3
    Pass 2674  the E8 > A2+E6 branching  -- the paper explicitly warns against it
    Pass 2742  the Jordan ladder         -- docs/index.html Pillars 128-130

Every one was findable by a single grep of a file the author's own notes say to read
first. `check_rediscovery.py` guards code parameters and `build_certificate_index.py`
guards certificate values; neither looks at prose novelty assertions, and neither reads
the encyclopedia.

This does one thing: when a file asserts novelty, it extracts the distinctive tokens near
that assertion and greps them against docs/index.html and the manuscripts -- the three
documents that produced all five failures.

WARNS, never blocks, matching the repo's standing policy.

Usage:
    py -3 scripts/check_novelty_claims.py <files...>
    py -3 scripts/check_novelty_claims.py --all-session analysis/w33_pass27*.md
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The documents that produced all five measured failures.
ENCYCLOPEDIA = [
    ROOT / "docs" / "index.html",
    ROOT / "photonic_holonet_body.tex",
    ROOT / "w33_paper_body.tex",
]

# Phrases that assert novelty.  Deliberately narrow: matching "new" alone would flag
# every file in the repo, which is the noise failure both other guards were calibrated
# away from.
NOVELTY = re.compile(
    r"(appears? to be absent|not in the corpus|no prior art|new to (?:me|this repo|the repo)"
    r"|nobody has (?:stated|noticed|said)|has never been|is not stated|unstated elsewhere"
    r"|does not appear to be new|first time|novel(?:ty)? claim)",
    re.I,
)

# Tokens worth grepping: named algebras/groups, capitalised multiword terms, and
# distinctive integers.  Small integers are excluded -- they flag everything.
TOKEN = re.compile(
    r"\b([A-Z][A-Za-z]*(?:_?\d)?(?:\([^)]{1,12}\))?"     # J_3(O), E_6, SRG(40,...)
    r"|[A-Z][a-z]{3,}(?:\s+[A-Z][a-z]{3,}){0,2}"          # Albert Algebra, Jordan Ladder
    r"|\d{3,9})\b"                                        # distinctive integers
)

STOPWORDS = {
    "The", "This", "That", "Pass", "Passes", "Not", "And", "But", "For", "With",
    "What", "Which", "Where", "When", "Its", "Their", "Recorded", "Scope", "Still",
    "Prior", "Open", "Verified", "Proved", "Measured", "Built",
}


def load_encyclopedia() -> dict[str, str]:
    out = {}
    for p in ENCYCLOPEDIA:
        if p.exists():
            try:
                out[p.name] = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass
    return out


def check(path: Path, enc: dict[str, str]) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except Exception:
        return []
    problems = []
    for ln, line in enumerate(lines, 1):
        if not NOVELTY.search(line):
            continue
        # tokens on this line and the one before it
        window = " ".join(lines[max(0, ln - 2):ln + 1])
        toks = {t for t in TOKEN.findall(window) if t not in STOPWORDS and len(t) > 2}
        hits = []
        for tok in sorted(toks):
            for name, body in enc.items():
                if tok in body:
                    hits.append(f"{tok!r} occurs in {name}")
                    break
        if hits:
            problems.append(
                f"  {path.name}:{ln}\n"
                f"    novelty asserted: {line.strip()[:96]}\n"
                + "".join(f"      but {h}\n" for h in hits[:6])
            )
    return problems


def _safe(t: str) -> str:
    """cp1252 consoles cannot print most of this repo's mathematical notation.
    Added Pass 2743 after the guard itself crashed on U+2102."""
    return t.encode("ascii", "replace").decode("ascii")


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    paths = [Path(a) for a in args] or sorted((ROOT / "analysis").glob("w33_pass27*.md"))
    enc = load_encyclopedia()
    if not enc:
        print("check_novelty_claims: no encyclopedia files found; nothing to check")
        return 0

    print(f"checking {len(paths)} file(s) against {', '.join(enc)}")
    allp = []
    for p in paths:
        allp.extend(check(p, enc))
    if allp:
        print(f"\n{len(allp)} novelty claim(s) with encyclopedia hits - review, not a block:\n")
        for p in allp:
            print(_safe(p))
    else:
        print("no novelty claim collides with the encyclopedia.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
