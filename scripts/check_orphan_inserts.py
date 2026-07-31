#!/usr/bin/env python3
"""Find manuscript inserts that no manuscript actually includes.

WHY THIS EXISTS (measured, Pass 1428).  This corpus writes "manuscript-ready"
LaTeX inserts as a standard output of a pass.  Asked whether a refactor had
dropped one, the answer was no -- but the check turned up something much worse:

    manuscript-insert .tex files in analysis/ : 201
    referenced by NO manuscript               : 179   (89%)

Eighty-nine percent of them are orphans.  The promotion step, not the
mathematics, is where work stops.  An insert that no manuscript inputs is
invisible to every reader, cannot be compiled by CI, and will be silently
rediscovered later -- it has all the costs of a result and none of the reach.

This is deliberately NOT fatal.  Many inserts are drafts, superseded, or
intentionally parked, and a hook that fails the build on 179 pre-existing files
is a hook people disable.  It reports, and it reports the NEW ones loudly,
because an orphan created today is the one still fixable today.

Run:  py -3 scripts/check_orphan_inserts.py [--new-only] [--limit N]
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# every file a \input could plausibly be resolved from
MANUSCRIPTS = ["w33_paper.tex", "w33_paper_body.tex",
               "photonic_holonet.tex", "photonic_holonet_body.tex",
               "W33_FOR_EVERYONE.tex"]
RE_INPUT = re.compile(r"\\(?:input|include)\{([^}]+)\}")


def manuscript_inputs() -> set[str]:
    """Every stem any manuscript pulls in, following one level of wrapper."""
    seen: set[str] = set()
    for name in MANUSCRIPTS:
        p = ROOT / name
        if not p.exists():
            continue
        for m in RE_INPUT.findall(p.read_text(encoding="utf-8", errors="ignore")):
            seen.add(Path(m).stem)
    return seen


def insert_files() -> list[Path]:
    """.tex files under analysis/ that look like manuscript inserts."""
    return sorted(p for p in (ROOT / "analysis").glob("*.tex") if p.is_file())


def recently_added(days: int = 14) -> set[str]:
    try:
        out = subprocess.run(
            ["git", "log", f"--since={days}.days", "--diff-filter=A",
             "--name-only", "--format="],
            capture_output=True, text=True, cwd=ROOT, timeout=120).stdout
    except Exception:
        return set()
    return {Path(l).stem for l in out.split() if l.endswith(".tex")}


def portability(paths: list[Path], limit: int = 40) -> int:
    r"""Would this insert COMPILE if promoted into a manuscript that lacks the
    w33_paper preamble?

    WHY (Pass 1436).  Promoting BT1408 into both manuscripts broke the Holonet
    build twice in a row: first "Environment lemma undefined", then "Undefined
    control sequence" for \Aut.  w33_paper.tex defines lemma/proposition/remark
    and \PSp/\Aut; photonic_holonet.tex defines none of them.  An insert that
    compiles in one host silently breaks the other, and the failure only appears
    at promotion time.

    So rather than promote the 15 recent orphans blind -- which would repeat that
    bug 15 times -- this reports which of them are PORTABLE.  The fix, when one
    is not, is the guarded preamble BT1408 now carries:

        \makeatletter \@ifundefined{lemma}{\newtheorem{lemma}...}{} \makeatother
        \providecommand{\PSp}{\mathrm{PSp}}
    """
    # macros/environments w33_paper.tex provides and photonic_holonet.tex does not
    HOST_ONLY = ["lemma", "proposition", "remark", "corollary", "definition",
                 "PSp", "Aut", "spec", "FF", "W"]
    RE_ENV = re.compile(r"\\begin\{(" + "|".join(HOST_ONLY) + r")\}")
    RE_MAC = re.compile(r"\\(" + "|".join(HOST_ONLY) + r")\\b")
    RE_GUARD = re.compile(r"@ifundefined|providecommand|newtheorem")
    bad = []
    for q in paths:
        try:
            t = q.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        used = set(RE_ENV.findall(t)) | set(RE_MAC.findall(t))
        if used and not RE_GUARD.search(t):
            bad.append((q, sorted(used)))
    print("=" * 74)
    print("[insert portability] would this compile in a host without the")
    print("                     w33_paper preamble?")
    print("=" * 74)
    print(f"checked {len(paths)} inserts")
    print(f"  use host-only macros WITHOUT a guard : {len(bad)}  <- would break")
    for q, used in bad[:limit]:
        print(f"    {q.relative_to(ROOT)}")
        print(f"       needs: {', '.join(used[:6])}")
    print("\n  Fix pattern (as used in BT1408):")
    print(r"    \makeatletter \@ifundefined{lemma}{\newtheorem{lemma}...}{} \makeatother")
    print(r"    \providecommand{\PSp}{\mathrm{PSp}}")
    print()
    return 0


def main(argv: list[str]) -> int:
    limit = 40
    for a in argv:
        if a.startswith("--limit"):
            limit = int(a.split("=")[1]) if "=" in a else limit
    if "--portability" in argv:
        # ALL inserts, not just orphans (Pass 1458). BT1509 is PROMOTED and uses
        # \PSp with no guard; it compiled only because BT1408 precedes it in the
        # wrapper and happens to provide the macro. A promoted insert that breaks
        # a host is strictly worse than an orphan that does -- it is in a live
        # build -- so scanning only orphans had the scope exactly backwards.
        return portability(insert_files(), limit)
    included = manuscript_inputs()
    files = insert_files()
    orphans = [p for p in files if p.stem not in included]
    fresh = recently_added()
    new_orphans = [p for p in orphans if p.stem in fresh]

    print("=" * 74)
    print("[orphan inserts] manuscript inserts that no manuscript includes")
    print("=" * 74)
    print(f"insert .tex files under analysis/ : {len(files)}")
    print(f"included by a manuscript          : {len(files) - len(orphans)}")
    print(f"ORPHANED                          : {len(orphans)}"
          f"  ({100*len(orphans)//max(1,len(files))}%)")
    if new_orphans:
        print(f"\n  ADDED IN THE LAST 14 DAYS AND STILL ORPHANED: {len(new_orphans)}")
        for p in new_orphans[:limit]:
            print(f"    {p.relative_to(ROOT)}")
        print("  ^ these are the ones still cheap to fix.")
    if "--new-only" not in argv:
        print(f"\n  all orphans (first {limit}):")
        for p in orphans[:limit]:
            print(f"    {p.relative_to(ROOT)}")
    print("\n  ADVISORY, never fatal. An orphan may be a draft, superseded, or")
    print("  deliberately parked. But an insert no manuscript inputs reaches no")
    print("  reader and will be rediscovered; promote it or say why not.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
