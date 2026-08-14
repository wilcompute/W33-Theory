"""Give date-named analysis files a TOPICAL index, so they can be found.

Two retractions in three batches (Passes 1912 and 1917) had the same root cause:
`analysis/2026-07-15_pass355_sp43_frobenius_schur.md` carries the Gow citation,
the Vinroot framework and the complex-conjugate-pair structure, and no search for
"phase", "complex structure" or "chirality" reaches it, because the FILENAME
encodes a date and the topic lives only inside the prose.

CLAUDE.md already says "search for the RESULT, not the topic".  That instruction
is correct and was still not enough, twice.  The reason is that a searcher has to
guess the result token; if you do not already know Gow's name you cannot grep for
it.  This script removes the guess: it reads every analysis file and extracts the
tokens that ARE result-shaped -- cited authors with years, named theorems, group
names, code parameters, distinctive formulas -- and writes them into a single
index keyed by token, so `grep -i gow TOPICAL_ALIASES.md` finds the file even
though `grep -i phase` never would.

This is deliberately NOT a summariser.  It extracts only tokens that already
appear verbatim, so the index cannot invent an association a file does not make.

Run:  py -3 scripts/build_topical_aliases.py
      py -3 scripts/build_topical_aliases.py --check   (CI mode: nonzero if stale)
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "TOPICAL_ALIASES.md")
DIRS = ["analysis", "docs", "manuscripts"]

# Author (Year) -- the token class that would have caught Passes 1912 and 1917.
RE_CITE = re.compile(r"\b([A-Z][a-z]{2,15})\s*\((1[89]\d\d|20[0-2]\d)\)")
# "X's theorem", "the X theorem"
RE_NAMED = re.compile(r"\b([A-Z][a-z]{2,15})(?:'s|-[A-Z][a-z]{2,15}'?s?)?\s+"
                      r"(?:theorem|indicator|bound|law|criterion|conjecture)\b")
# group names: Sp(4,3), PSp(4,q), W(E6), PGSp(4,3), SL(2,19), U4(2)
RE_GROUP = re.compile(r"\b((?:P?G?Sp|SL|GL|PSL|PGL|SU|U|O|W|A|S)"
                      r"\(?\d+\s*,\s*[0-9qp^]+\)?|W\(E[6-8]\)|[A-Z]\d\(\d+\))")
# code parameters [[n,k,d]] and [n,k,d]
RE_CODE = re.compile(r"\[\[?\s*\d+\s*,\s*\d+\s*,\s*[0-9<=q+]+\s*\]?\]")
# congruence conditions, the exact shape of the Pass 1907 rediscovery
RE_CONG = re.compile(r"q\s*(?:≡|=|==)\s*\d\s*\(?\s*mod\s*\d\)?", re.I)

# Eponymous OBJECT names.  Added after dogfooding found the index scored
# "Eisenstein: 0" -- the Pass 350 prior art that motivated this file would not
# have been caught, because `named:` only fires before theorem/indicator/bound.
# A curated list, not a regex over capitalised words: Passes 1107/1483 measured
# that widening a token vocabulary without calibration is how these guards turn
# to noise.  The <=12-file cut in render() is the calibration.
EPONYMS = (r"Eisenstein|Weil|Steinberg|Hodge|Leech|Klein|Petersen|Hoffman|"
           r"Tutte|Coxeter|Desarguesian|Hermitian|Bockstein|Mackey|Brauer|"
           r"Frobenius|Schur|Hashimoto|Ihara|Macwilliams|MacWilliams|Smith|"
           r"Gauss|Galois|Noether|Dynkin|Levi|Borel|Cartan|Hamming|Golay|"
           r"Moonshine|McKay|Thompson|Norton|Monster|Conway|Mathieu|Suzuki|"
           r"Landauer|Clifford|Majorana|Yukawa|Kasteleyn|Perron|Ramanujan")
RE_EPON = re.compile(r"\b(" + EPONYMS + r")\b")

CLASSES = [("cite", RE_CITE), ("named", RE_NAMED), ("group", RE_GROUP),
           ("code", RE_CODE), ("congruence", RE_CONG), ("object", RE_EPON)]

STOP = {"The", "This", "That", "Pass", "Note", "See", "From", "For", "And",
        "But", "Table", "Figure", "Section", "Both", "Each", "Every", "One",
        "Two", "Three", "All", "Its", "Their", "These", "Those", "With"}


def tokens_of(text: str) -> set[str]:
    out = set()
    for name, rx in CLASSES:
        for m in rx.finditer(text):
            g = m.group(1) if m.groups() else m.group(0)
            g = re.sub(r"\s+", "", str(g))
            if g in STOP or len(g) < 2:
                continue
            if name == "cite":
                g = f"{m.group(1)}({m.group(2)})"
                if m.group(1) in STOP:
                    continue
            out.add(f"{name}:{g}")
    return out


def selftest() -> int:
    """Planted-fault recall for the token grammar the alias index is built from.

    This index exists because the corpus is named by DATE, not by topic, so the token
    extractor IS the only route from a result to the file holding it. A class that silently
    stops matching removes a whole retrieval path and nothing else notices (Pass 5250).
    """
    cases = [("group token", "The group Sp(4,3) acts here.", "group", True),
             ("code token", "the code [325,260,8] is dual.", "code", True),
             ("stopword is not a token", "The Table shows it.", "named", False),
             ("bare integer is not a token", "There are 240 roots.", "code", False)]
    ok = True
    print("  selftest -- token grammar recall\n")
    for name, text, cls, want in cases:
        toks = tokens_of(text)
        got = any(t.startswith(cls + ":") for t in toks)
        good = got == want
        ok &= good
        print(f"    {name:32s} {cls:10s} got={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}  {sorted(toks)[:3]}")
    print("""
  THE BARE-INTEGER CASE IS THE CALIBRATION. Pass 328 measured every token class before this
  grammar was chosen: indexing bare integers flags 97 percent of files and is pure noise, so
  "240" must NOT become a token even though 240 is one of the most load-bearing numbers in
  the corpus. The index trades that recall away deliberately, and this case pins the trade
  so a later widening cannot happen silently.""")
    return 0 if ok else 1


def scan():
    idx = defaultdict(set)
    nfiles = 0
    for d in DIRS:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        for dirpath, dirnames, files in os.walk(p):
            dirnames[:] = [x for x in dirnames
                           if x not in (".git", "node_modules", "__pycache__")]
            for fn in files:
                if not fn.endswith((".md", ".tex", ".html")):
                    continue
                fp = os.path.join(dirpath, fn)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as fh:
                        txt = fh.read(400_000)
                except OSError:
                    continue
                nfiles += 1
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                for t in tokens_of(txt):
                    idx[t].add(rel)
    return idx, nfiles


def render(idx, nfiles):
    # a file is "topically opaque" if its NAME carries no topic -- date- or
    # number-led.  Those are exactly the ones this index exists to rescue.
    opaque = re.compile(r"(^|/)(\d{4}-\d{2}-\d{2}|PASS\d+|BT\d+|"
                        r"w33_pass\d+)", re.I)
    lines = [
        "# Topical aliases — result tokens to files",
        "",
        "Auto-generated by `scripts/build_topical_aliases.py`. **Do not edit.**",
        "",
        "This exists because two results were rediscovered (Passes 1912, 1917)",
        "that were already in the corpus under date-named files. Searching for a",
        "topic cannot find them; searching for a result token can, but only if",
        "you can guess the token. This index lists the tokens so you do not have",
        "to guess: `grep -i gow TOPICAL_ALIASES.md` reaches",
        "`2026-07-15_pass355_sp43_frobenius_schur.md`, which no search for",
        "\"phase\" or \"complex structure\" ever would.",
        "",
        f"Files scanned: **{nfiles}** · distinct tokens: **{len(idx)}**",
        "",
        "Tokens marked ⚠ appear ONLY in topically opaque filenames (dated or",
        "numbered), so they are invisible to any topic search — read those first.",
        "",
    ]
    for t in sorted(idx):
        fs = sorted(idx[t])
        if t.startswith("object:"):
            # Eponyms are common by nature, so the <=12 rule filtered every one
            # of them -- which would have re-hidden the Pass 350 Eisenstein prior
            # art this index exists to surface.  For these, keep the token but
            # list ONLY the topically opaque files, since those are exactly the
            # ones no topic search can reach.  Bounded, and targeted at the
            # failure mode rather than at coverage.
            fs = [f for f in fs if opaque.search(f)]
            if not fs or len(fs) > 40:
                continue
            lines.append(f"- `{t}` ⚠ (opaque-named only) — "
                         + ", ".join(f"[{os.path.basename(f)}]({f})" for f in fs))
            continue
        if len(fs) > 12:
            continue                      # ubiquitous: no discriminating power
        flag = " ⚠" if all(opaque.search(f) for f in fs) else ""
        lines.append(f"- `{t}`{flag} — " + ", ".join(f"[{os.path.basename(f)}]({f})"
                                                     for f in fs))
    return "\n".join(lines) + "\n"


def main():
    if "--selftest" in sys.argv:
        return selftest()
    idx, nfiles = scan()
    new = render(idx, nfiles)
    if "--check" in sys.argv:
        old = open(OUT, encoding="utf-8").read() if os.path.exists(OUT) else ""
        if old != new:
            print("TOPICAL_ALIASES.md is stale; run "
                  "py -3 scripts/build_topical_aliases.py")
            return 1
        print("TOPICAL_ALIASES.md up to date")
        return 0
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(new)
    opaque = re.compile(r"(^|/)(\d{4}-\d{2}-\d{2}|PASS\d+|BT\d+|w33_pass\d+)",
                        re.I)
    hidden = [t for t, fs in idx.items()
              if len(fs) <= 12 and all(opaque.search(f) for f in fs)]
    print(f"scanned {nfiles} files, {len(idx)} tokens")
    print(f"tokens visible ONLY in opaque filenames: {len(hidden)}")
    for t in sorted(hidden)[:12]:
        print(f"   {t}  ->  {sorted(idx[t])[0]}")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
