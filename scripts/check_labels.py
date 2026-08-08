#!/usr/bin/env python3
"""Pass 4318 -- duplicate and dangling \\label/\\ref across every manuscript.

The blueprint carried \\label{sec:budget} TWICE. LaTeX resolves every \\ref to the LAST
definition, so three references meaning "the cell budget" silently pointed at a chapter
ninety pages away. It compiled without a single error, because a duplicate label is only a
warning and a warning is not a failure.

Nothing had ever checked w33_paper (477 pages) or photonic_holonet (347).

Per manuscript, following \\input transitively from the top-level file:
  * labels defined more than once   -- every \\ref to them resolves to the last one
  * labels referenced but never defined
  * labels defined but never referenced (reported, not an error: many are anchors)

    py -3 scripts/check_labels.py            # all manuscripts
    py -3 scripts/check_labels.py --strict   # exit 1 on duplicates or dangling refs
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = re.compile(r"\\(?:input|include)\{([^}]*)\}")
LABEL = re.compile(r"\\label\{([^}]*)\}")
REF = re.compile(r"\\(?:ref|eqref|cref|Cref|autoref|pageref)\{([^}]*)\}")


def resolve(stem: str) -> Path | None:
    for c in (ROOT / f"{stem}.tex", ROOT / "analysis" / f"{stem}.tex",
              ROOT / "manuscripts" / f"{stem}.tex",
              ROOT / "paper" / "sections" / f"{stem}.tex"):
        if c.exists():
            return c
    return None


def gather(root: Path):
    """Every file reachable from a manuscript, in inclusion order."""
    out, seen, frontier = [], {root.resolve()}, [root]
    while frontier:
        f = frontier.pop(0)
        out.append(f)
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in INPUT.finditer(txt):
            t = resolve(Path(m.group(1).strip()).name.removesuffix(".tex"))
            if t and t.resolve() not in seen:
                seen.add(t.resolve())
                frontier.append(t)
    return out


def audit(root: Path):
    files = gather(root)
    defs: dict[str, list[str]] = defaultdict(list)
    refs: Counter = Counter()
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for lab in LABEL.findall(txt):
            defs[lab].append(f.name)
        for r in REF.findall(txt):
            refs[r] += 1
    dup = {k: v for k, v in defs.items() if len(v) > 1}
    dangling = sorted(r for r in refs if r not in defs)
    unused = sorted(k for k in defs if k not in refs)
    return files, defs, dup, dangling, unused


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    bad = 0
    for name in ("holonet_machine_blueprint", "w33_paper", "photonic_holonet"):
        root = ROOT / f"{name}.tex"
        if not root.exists():
            continue
        files, defs, dup, dangling, unused = audit(root)
        print(f"\n  {name}")
        print(f"    files reached      : {len(files)}")
        print(f"    labels defined     : {len(defs)}")
        print(f"    DUPLICATE labels   : {len(dup)}")
        print(f"    DANGLING references: {len(dangling)}")
        print(f"    unused labels      : {len(unused)}  (informational)")
        for k, v in sorted(dup.items())[:10]:
            print(f"      dup  {k}  in {sorted(set(v))}")
        for d in dangling[:10]:
            print(f"      ref  {d}  never defined")
        bad += len(dup) + len(dangling)
    print(f"\n  total duplicates + dangling across all manuscripts: {bad}")
    if bad:
        print("""
  A duplicate label is not a LaTeX error, only a warning, so a document can carry one
  through hundreds of compiles. Every \\ref to a duplicated label silently resolves to the
  LAST definition -- which is why this check exists rather than trusting a clean build.""")
    return 1 if (strict and bad) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
