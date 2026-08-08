#!/usr/bin/env python3
"""Which analysis/*_insert.tex files are not included by ANY manuscript?

The parallel track writes results as standalone LaTeX inserts under analysis/, intended to
be \\input into a manuscript.  Nothing checks that the second half of that actually happens,
so an insert can be written, committed, and never appear in any document -- a finished
write-up that no reader can reach.

    py -3 scripts/find_orphaned_inserts.py            # summary
    py -3 scripts/find_orphaned_inserts.py --list     # every orphan
    py -3 scripts/find_orphaned_inserts.py --topic zeta ihara   # orphans matching topics
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]*)\}")


def main(argv: list[str]) -> int:
    inserts = sorted((ROOT / "analysis").glob("*_insert.tex"))
    stems = {p.stem: p for p in inserts}

    # Every .tex in the repo is a potential includer, not just the top-level manuscripts:
    # an insert may be pulled in by another insert.
    included: set[str] = set()
    for tex in ROOT.rglob("*.tex"):
        try:
            txt = tex.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in INPUT_RE.finditer(txt):
            target = m.group(1).strip()
            name = Path(target).name
            included.add(name[:-4] if name.endswith(".tex") else name)

    orphans = sorted(s for s in stems if s not in included)
    used = len(stems) - len(orphans)
    print(f"  insert files      : {len(stems)}")
    print(f"  included somewhere: {used}")
    print(f"  ORPHANED          : {len(orphans)}")

    if "--list" in argv or "--titles" in argv:
        sec = re.compile(r"\\section\*?\{([^}]*)\}")
        rows = []
        for s in orphans:
            txt = stems[s].read_text(encoding="utf-8", errors="replace")
            m = sec.search(txt)
            rows.append((len(txt), s, m.group(1)[:74] if m else "(no \\section)"))
        rows.sort(reverse=True)
        print(f"\n  {'bytes':>6s}  {'file':46s} section")
        for n, s, ti in rows:
            print(f"  {n:6d}  {s[:46]:46s} {ti}")
    topics = [a.lower() for a in argv if not a.startswith("--")]
    if topics:
        print(f"\n  orphans mentioning {topics}:")
        for s in orphans:
            txt = stems[s].read_text(encoding="utf-8", errors="replace").lower()
            hit = [t for t in topics if t in txt or t in s.lower()]
            if hit:
                title = ""
                m = re.search(r"\\section\*?\{([^}]*)\}",
                              stems[s].read_text(encoding="utf-8", errors="replace"))
                if m:
                    title = m.group(1)[:60]
                print(f"    {s}  {hit}  {title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
