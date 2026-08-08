#!/usr/bin/env python3
"""Passes 4294-4295 -- route every orphaned insert to its manuscript, not just the blueprint.

Pass 4285 recovered the 57 orphans destined for the machine blueprint and left 27 routed
elsewhere plus 30 with no destination marker at all.  Those other manuscripts have exactly
the same gap and nobody has looked at them; the unrouted ones are worse, because they are
invisible to author and census alike.

This generalises scripts/vet_inserts_for_blueprint.py to every manuscript:

  * route by filename convention, which records the intended destination;
  * for files with no marker, classify by content against each manuscript's own vocabulary
    rather than guessing -- and report the ones that match nothing, because "belongs
    nowhere" is a real answer that should be visible rather than silently dropped;
  * vet each candidate (dangling refs, duplicate labels, Pass 4231 pitfall families);
  * emit one recovered-work appendix per manuscript.

    py -3 scripts/route_orphaned_inserts.py            # report
    py -3 scripts/route_orphaned_inserts.py --emit     # write the appendices
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_tex_insert_pitfalls as chk  # noqa: E402

INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")
LABEL = re.compile(r"\\label\{([^}]*)\}")
REF = re.compile(r"\\(?:ref|eqref|cref|Cref|autoref)\{([^}]*)\}")

# manuscript body -> (filename marker, generated appendix)
BOOKS = {
    "holonet_machine_blueprint_body.tex": (
        ("holonet_machine", "blueprint", "holonet"),
        ROOT / "analysis" / "W33_BLUEPRINT_RECOVERED_APPENDIX.tex"),
    "w33_paper_body.tex": (
        ("w33_paper",),
        ROOT / "analysis" / "W33_PAPER_RECOVERED_APPENDIX.tex"),
    "photonic_holonet_body.tex": (
        ("photonic_holonet",),
        ROOT / "analysis" / "W33_PHOTONIC_RECOVERED_APPENDIX.tex"),
}
APPENDICES = {v[1].resolve() for v in BOOKS.values()}
# Pass 4300 read the six that previously matched nothing.  None is a dead draft: each
# carries a section heading and a result (cubic leakage ratios, Levi versus phase-cover
# homology, cubic leakage as an Ihara shadow, the tetrahedral Hodge clock, the
# six-carrier/four-cell split, five Levi frontiers).  They sit beside the blueprint's Ihara
# and Levi material, so the vocabulary is widened to reach them rather than leaving genuine
# findings unreachable on a technicality about filenames.
FALLBACK = {
    "holonet_machine_blueprint_body.tex": ("opcode", "register", "instruction", "rtl",
                                           "synthesis", "compiler", "decoder",
                                           "controller", "architecture", "hardware",
                                           "ihara", "levi", "leakage", "carrier",
                                           "hodge clock", "codec"),
    "w33_paper_body.tex": ("theorem", "lemma", "cohomolog", "character", "irreducible",
                           "lattice", "weyl", "root system", "moonshine"),
    "photonic_holonet_body.tex": ("photon", "optical", "waveguide", "oam", "laser",
                                  "interferomet", "mode", "loss"),
}


def existing_placement():
    """Where each insert already sits, from the generated appendices.

    Placement is STICKY.  Filename routing is reliable; content routing is a guess, and
    re-guessing an insert that is already placed churns the manuscripts for no gain -- the
    first version of this tool moved three inserts out of the blueprint on a vocabulary
    count, which is not a reason to relocate finished work."""
    out = {}
    for book, (_, appendix) in BOOKS.items():
        if not appendix.exists():
            continue
        txt = appendix.read_text(encoding="utf-8", errors="replace")
        for m in INPUT_RE.finditer(txt):
            out[Path(m.group(1).strip()).name.removesuffix(".tex")] = book
    return out


_PLACED = existing_placement()


def route(stem: str, text: str):
    if stem in _PLACED:
        return _PLACED[stem], "already placed"
    low = stem.lower()
    for book, (markers, _) in BOOKS.items():
        for m in markers:
            if m in low:
                return book, "filename"
    body = (stem + " " + text).lower()
    scores = {b: sum(body.count(t) for t in toks) for b, toks in FALLBACK.items()}
    best = max(scores, key=lambda b: scores[b])
    return (best, "content") if scores[best] else (None, "none")


def included_stems():
    inc = set()
    for tex in ROOT.rglob("*.tex"):
        if tex.resolve() in APPENDICES:
            continue
        try:
            txt = tex.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in INPUT_RE.finditer(txt):
            n = Path(m.group(1).strip()).name
            inc.add(n[:-4] if n.endswith(".tex") else n)
    return inc


def main(argv: list[str]) -> int:
    inserts = {p.stem: p for p in sorted((ROOT / "analysis").glob("*_insert.tex"))}
    inc = included_stems()
    orphans = [s for s in inserts if s not in inc]

    all_labels = set()
    for p in inserts.values():
        all_labels |= set(LABEL.findall(p.read_text(encoding="utf-8", errors="replace")))
    book_labels = {}
    for b in BOOKS:
        t = (ROOT / b).read_text(encoding="utf-8", errors="replace")
        book_labels[b] = set(LABEL.findall(t))
        all_labels |= book_labels[b]

    have, thms = chk.preamble_packages(), chk.preamble_theorems()

    by_book: dict[str, list] = {b: [] for b in BOOKS}
    blocked, homeless = [], []
    how = Counter()
    for s in sorted(orphans):
        p = inserts[s]
        txt = p.read_text(encoding="utf-8", errors="replace")
        book, why = route(s, txt)
        how[why] += 1
        if book is None:
            homeless.append(s)
            continue
        reasons = []
        dang = sorted({r for r in REF.findall(txt) if r not in all_labels})
        if dang:
            reasons.append(f"dangling refs {dang[:2]}")
        dup = sorted(set(LABEL.findall(txt)) & book_labels[book])
        if dup:
            reasons.append(f"duplicate labels {dup[:2]}")
        pit = sorted({k for _, k, _ in chk.scan(p, have, thms)})
        if pit:
            reasons.append(f"pitfalls {pit[:2]}")
        if reasons:
            blocked.append((s, book, reasons))
        else:
            by_book[book].append(s)

    print(f"  insert files              : {len(inserts)}")
    print(f"  orphaned                  : {len(orphans)}")
    print(f"  already placed (sticky)   : {how['already placed']}")
    print(f"  routed by filename        : {how['filename']}")
    print(f"  routed by content (guess) : {how['content']}")
    print(f"  matched nothing (homeless): {len(homeless)}\n")
    for b in BOOKS:
        print(f"  {b:38s} {len(by_book[b]):4d} recoverable")
    print(f"  {'blocked (see below)':38s} {len(blocked):4d}")

    if blocked:
        print("\n  blocked:")
        for s, b, r in blocked:
            print(f"    {s[:46]:46s} -> {b.split('_')[0]:10s} {'; '.join(r)[:52]}")
    if homeless:
        print(f"\n  homeless ({len(homeless)}) -- no filename marker and no vocabulary match:")
        for s in homeless:
            print(f"    {s}")

    if "--emit" in argv:
        for b, (_, appendix) in BOOKS.items():
            stems = by_book[b]
            if not stems:
                continue
            L = ["% Generated by scripts/route_orphaned_inserts.py -- do not hand-edit.",
                 "% Finished inserts that no manuscript included, recovered and vetted.",
                 "",
                 "\\section{Recovered write-ups}",
                 f"\\label{{sec:recovered-{b.split('_')[0]}}}",
                 ""]
            for s in stems:
                L.append(f"\\input{{analysis/{s}}}%")
            appendix.write_text("\n".join(L) + "\n", encoding="utf-8")
            print(f"\n  wrote {appendix.relative_to(ROOT).as_posix()} ({len(stems)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
