#!/usr/bin/env python3
"""Pass 4285 -- decide which orphaned inserts can safely be pulled into the blueprint.

scripts/find_orphaned_inserts.py found 114 analysis/*_insert.tex files that no manuscript
includes: finished write-ups no reader can reach.  Pulling them in blindly would inject
broken cross-references and undefined macros into a 169-page document, so each candidate is
vetted first.

An insert is SAFE when, taken together with the blueprint's preamble, it has:
  * no \\ref / \\eqref / \\cref to a label defined nowhere in the merged document,
  * no environment or macro the preamble does not provide (reusing the Pass 4231 families),
  * no duplicate \\label already present in the blueprint.

Anything failing those is reported with its reason rather than silently dropped -- the
point is a triage list a human can act on, not a filter that hides work.

    py -3 scripts/vet_inserts_for_blueprint.py             # summary + verdicts
    py -3 scripts/vet_inserts_for_blueprint.py --emit      # write the appendix stub
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "holonet_machine_blueprint_body.tex"
APPENDIX = ROOT / "analysis" / "W33_BLUEPRINT_RECOVERED_APPENDIX.tex"

sys.path.insert(0, str(ROOT / "scripts"))
import check_tex_insert_pitfalls as chk  # noqa: E402
from find_orphaned_inserts import INPUT_RE  # noqa: E402

LABEL = re.compile(r"\\label\{([^}]*)\}")
REF = re.compile(r"\\(?:ref|eqref|cref|Cref|autoref)\{([^}]*)\}")
# ROUTING, not topic-matching.  An early version filtered on words like "port" and
# "clock" and called 102 of 114 blueprint material -- but a file named
# BT1147_w33_paper_matrix_derivation_insert is written for w33_paper.tex, and pouring it
# into the blueprint would bloat that document rather than improve it.  The filename
# convention already records the intended destination; use it.
DEST = [
    ("w33_paper", "w33_paper_body.tex"),
    ("photonic_holonet", "photonic_holonet_body.tex"),
    ("holonet_machine", "holonet_machine_blueprint_body.tex"),
    ("blueprint", "holonet_machine_blueprint_body.tex"),
    ("holonet", "holonet_machine_blueprint_body.tex"),
]
BLUEPRINT_DEST = "holonet_machine_blueprint_body.tex"
# Only used for files whose name carries no destination marker at all.
FALLBACK_TOPICS = ("opcode", "register", "instruction", "rtl", "synthesis", "compiler",
                   "decoder", "controller", "architecture", "hardware")


def route(stem: str, text: str) -> str:
    low = stem.lower()
    for marker, dest in DEST:
        if marker in low:
            return dest
    body = (stem + " " + text).lower()
    if any(t in body for t in FALLBACK_TOPICS):
        return BLUEPRINT_DEST
    return "unrouted"


def collect_labels(paths):
    out = set()
    for p in paths:
        out.update(LABEL.findall(p.read_text(encoding="utf-8", errors="replace")))
    return out


def included_stems():
    """Stems included by some manuscript, EXCLUDING this script's own generated appendix.

    Without that exclusion the tool is not idempotent: the appendix it emits lives under
    analysis/ and \\inputs the recovered inserts, so a second run sees them as already
    included and regenerates an appendix containing only the leftovers -- silently
    dropping the 56 it had just rescued."""
    inc = set()
    for tex in ROOT.rglob("*.tex"):
        if tex.resolve() == APPENDIX.resolve():
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

    body_txt = BODY.read_text(encoding="utf-8", errors="replace")
    body_labels = set(LABEL.findall(body_txt))
    # Labels available once every orphan we might add is present.
    orphan_labels = collect_labels([inserts[s] for s in orphans])
    # Plus labels in inserts the blueprint already reaches, transitively.
    reachable = collect_labels([inserts[s] for s in inserts if s in inc])
    known = body_labels | orphan_labels | reachable

    have, thms = chk.preamble_packages(), chk.preamble_theorems()

    safe, blocked, elsewhere = [], [], {}
    for s in sorted(orphans):
        p = inserts[s]
        txt = p.read_text(encoding="utf-8", errors="replace")
        dest = route(s, txt)
        if dest != BLUEPRINT_DEST:
            elsewhere.setdefault(dest, []).append(s)
            continue
        reasons = []
        dangling = sorted({r for r in REF.findall(txt) if r not in known})
        if dangling:
            reasons.append(f"dangling refs: {dangling[:3]}")
        dup = sorted(set(LABEL.findall(txt)) & body_labels)
        if dup:
            reasons.append(f"duplicate labels: {dup[:3]}")
        pit = [k for _, k, _ in chk.scan(p, have, thms)]
        if pit:
            reasons.append(f"pitfalls: {sorted(set(pit))[:3]}")
        (blocked if reasons else safe).append((s, reasons, len(txt)))

    print(f"  orphaned inserts            : {len(orphans)}")
    print("  routed to other manuscripts (NOT the blueprint's to fix):")
    for d, lst in sorted(elsewhere.items()):
        print(f"    {d:38s} {len(lst)}")
    print(f"  destined for the blueprint  : {len(safe) + len(blocked)}")
    print(f"  SAFE to include now         : {len(safe)}")
    print(f"  blocked, with reasons       : {len(blocked)}")
    print(f"\n  {'file':52s} bytes")
    for s, _, n in sorted(safe, key=lambda t: -t[2]):
        print(f"  {s[:52]:52s} {n:6d}")
    if blocked:
        print("\n  blocked:")
        for s, r, n in sorted(blocked, key=lambda t: -t[2]):
            print(f"  {s[:52]:52s} {n:6d}  {'; '.join(r)[:70]}")

    if "--emit" in argv and safe:
        L = ["% Generated by scripts/vet_inserts_for_blueprint.py -- do not hand-edit.",
             "% Recovered write-ups: finished inserts that no manuscript included.",
             "% Each was vetted for dangling refs, duplicate labels, and LaTeX pitfalls.",
             "",
             "\\section{Recovered write-ups}",
             "\\label{sec:recovered}",
             "",
             "\\begin{plain}",
             "The passes below were written up as standalone sections and committed, but no",
             "manuscript ever included them --- finished work that no reader could reach. A",
             "census found " + str(len(orphans)) + " such orphaned inserts across the repository;",
             "the ones that are blueprint material and pass vetting appear here verbatim.",
             "\\end{plain}",
             ""]
        for s, _, _ in sorted(safe, key=lambda t: t[0]):
            L.append(f"\\input{{analysis/{s}}}%")
        APPENDIX.write_text("\n".join(L) + "\n", encoding="utf-8")
        print(f"\n  wrote {APPENDIX.relative_to(ROOT).as_posix()} "
              f"({len(safe)} inserts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
