#!/usr/bin/env python3
"""Fail when a committed PDF is older than the .tex it was built from.

WHY THIS EXISTS.  A stale PDF is the quietest possible lie in this repository.  The
README links compiled PDFs as the primary artifact -- "read the mathematics" points
at w33_paper.pdf, not at the source -- so a reader who follows the link gets whatever
was last built, with no indication that the source has moved on.  Nothing errors,
nothing is red, and the document simply says something the repository no longer says.

Found the hard way on 2026-07-25: photonic_holonet.pdf and
holonet_practical_implications.pdf were both six days behind their sources at the
moment they were linked from the README as the things to read, and five more root
PDFs were behind by hours-to-days.  Two independent causes, both silent -- an agent
concluding no LaTeX engine existed (it did) and skipping the rebuild, and tectonic
compiles from a purged temp directory failing with NO OUTPUT AND EXIT 0.

The comparison is `.tex` LAST COMMIT TIME against `.pdf` last commit time, not
filesystem mtimes: mtimes are meaningless after a fresh clone, and CI always runs on
a fresh clone.

Usage:
    py -3 scripts/check_pdf_staleness.py            # all tracked pdf/tex pairs
    py -3 scripts/check_pdf_staleness.py --linked   # only PDFs the README links
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def commit_time(rel: str) -> int | None:
    """Unix time of the last commit touching `rel`, or None if untracked."""
    out = subprocess.run(
        ["git", "log", "-1", "--format=%at", "--", rel],
        cwd=ROOT, capture_output=True, text=True,
    ).stdout.strip()
    return int(out) if out.isdigit() else None


def tracked_pdfs() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "*.pdf"], cwd=ROOT, capture_output=True, text=True
    ).stdout
    return [line for line in out.splitlines() if line.strip()]


def readme_linked() -> set[str]:
    """PDF paths the README links, which are the ones a reader actually opens."""
    text = (ROOT / "README.md").read_text(encoding="utf-8", errors="ignore")
    return set(re.findall(r"\(([^)]+?\.pdf)\)", text))


def source_for(pdf: str) -> str | None:
    """Locate the .tex a PDF was built from: same dir, then repo root, then papers/."""
    stem = Path(pdf).stem
    for cand in (Path(pdf).with_suffix(".tex"),
                 Path(f"{stem}.tex"),
                 Path("papers") / f"{stem}.tex",
                 Path("manuscripts/tex") / f"{stem}.tex"):
        if (ROOT / cand).exists():
            return cand.as_posix()
    return None


def main(argv: list[str]) -> int:
    only_linked = "--linked" in argv
    linked = readme_linked()
    stale, checked, orphans = [], 0, []

    for pdf in tracked_pdfs():
        if only_linked and pdf not in linked:
            continue
        tex = source_for(pdf)
        if tex is None:
            orphans.append(pdf)
            continue
        t_pdf, t_tex = commit_time(pdf), commit_time(tex)
        if t_pdf is None or t_tex is None:
            continue
        checked += 1
        if t_tex > t_pdf:
            stale.append((pdf, tex, (t_tex - t_pdf) // 86400))

    print(f"checked {checked} pdf/tex pairs"
          + (" (README-linked only)" if only_linked else "")
          + f"; {len(orphans)} PDFs have no locatable source")

    if stale:
        print("\nSTALE -- the PDF is older than the source it claims to be built from:\n")
        for pdf, tex, days in sorted(stale, key=lambda r: -r[2]):
            print(f"  {pdf}")
            print(f"    source {tex} is newer by {days} day(s)")
        print("\nRebuild and re-commit, e.g.:")
        print("  <tectonic> -X compile <file>.tex     # run from the repo root")
        print("  git add -f <file>.pdf docs/pdf/<file>.pdf")
        print("\nSee the tectonic recipe in the agent memory; note that a compile from")
        print("a purged temp directory fails SILENTLY with exit 0, so confirm the")
        print("'note: Writing `...pdf` (N KiB)' line rather than trusting the exit code.")
        return 1

    print("all committed PDFs are at least as new as their sources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
