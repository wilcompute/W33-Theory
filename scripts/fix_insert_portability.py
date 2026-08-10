#!/usr/bin/env python3
r"""Add a guarded preamble to manuscript inserts so they compile in any host.

WHY (Pass 1444).  `check_orphan_inserts.py --portability` finds 25 inserts that
use environments or macros only `w33_paper.tex` defines -- `lemma`,
`proposition`, `remark`, `\PSp`, `\Aut`.  Promoted into `photonic_holonet.tex`
they break the build, which is exactly what BT1408 did, twice.

WHY THIS IS A TOOL AND NOT A ONE-LINER.  The last time I fixed a LaTeX problem
with a regex sweep it "fixed" 2,129 legitimate math-mode subscripts across 32
files and broke the manuscript (Pass 1432).  The rule written into CLAUDE.md as
a result is: prove a rewriting transformation on the single known-bad case, then
widen, and report a dry-run count before writing.  This enforces that -- it
refuses to touch anything without an explicit mode, defaults to `--dry-run`, and
`--only NAME` exists so the first application is a single file.

The inserted block is idempotent (`\@ifundefined`, `\providecommand`), so a host
that already defines these keeps its own definitions and re-running is a no-op.

Run:
    py -3 scripts/fix_insert_portability.py                 # dry run, default
    py -3 scripts/fix_insert_portability.py --only BT1134   # prove it on one
    py -3 scripts/fix_insert_portability.py --apply         # widen
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

BLOCK = r"""% HOST-INDEPENDENT PREAMBLE (added by scripts/fix_insert_portability.py).
% This insert may be \input by either root manuscript, and they do not define the
% same environments or macros: w33_paper.tex has lemma/proposition/remark and
% \PSp/\Aut, photonic_holonet.tex has none of them. Define only what is missing,
% so the file is portable and re-running this is a no-op.
\makeatletter
\@ifundefined{theorem}{\newtheorem{theorem}{Theorem}}{}
\@ifundefined{lemma}{\newtheorem{lemma}[theorem]{Lemma}}{}
\@ifundefined{proposition}{\newtheorem{proposition}[theorem]{Proposition}}{}
\@ifundefined{remark}{\newtheorem{remark}[theorem]{Remark}}{}
\@ifundefined{corollary}{\newtheorem{corollary}[theorem]{Corollary}}{}
\@ifundefined{definition}{\newtheorem{definition}[theorem]{Definition}}{}
\makeatother
\providecommand{\PSp}{\mathrm{PSp}}
\providecommand{\PGSp}{\mathrm{PGSp}}
\providecommand{\Aut}{\mathrm{Aut}}
\providecommand{\spec}{\operatorname{spec}}

"""

MARKER = "HOST-INDEPENDENT PREAMBLE"


def targets() -> list[tuple[Path, list[str]]]:
    from check_orphan_inserts import insert_files, manuscript_inputs
    from check_orphan_inserts import _host_only
    HOST_ONLY = _host_only()
    re_env = re.compile(r"\\begin\{(" + "|".join(HOST_ONLY) + r")\}")
    re_mac = re.compile(r"\\(" + "|".join(HOST_ONLY) + r")\b")
    re_guard = re.compile(r"@ifundefined|providecommand|newtheorem")
    included = manuscript_inputs()
    out = []
    for p in insert_files():
        if p.stem in included:
            continue
        t = p.read_text(encoding="utf-8", errors="ignore")
        used = sorted(set(re_env.findall(t)) | set(re_mac.findall(t)))
        if used and not re_guard.search(t):
            out.append((p, used))
    return out


def insert_block(p: Path) -> bool:
    t = p.read_text(encoding="utf-8", errors="ignore")
    if MARKER in t:
        return False
    lines = t.split("\n")
    # place the block after any leading comment header, before the first content
    i = 0
    while i < len(lines) and (lines[i].startswith("%") or not lines[i].strip()):
        i += 1
    lines.insert(i, BLOCK)
    p.write_text("\n".join(lines, encoding="utf-8"), encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    tg = targets()
    only = None
    for i, a in enumerate(argv):
        if a == "--only" and i + 1 < len(argv):
            only = argv[i + 1]
    if only:
        tg = [(p, u) for p, u in tg if only in p.stem]
    apply = "--apply" in argv or only is not None

    print(f"{'APPLY' if apply else 'DRY RUN'}: {len(tg)} insert(s) need a guard")
    for p, used in tg:
        print(f"  {p.relative_to(ROOT)}   needs: {', '.join(used)}")
    if not apply:
        print("\n  nothing written. Re-run with --only NAME to prove it on one file,")
        print("  then --apply to widen. (CLAUDE.md: prove, then widen.)")
        return 0
    n = sum(insert_block(p) for p, _ in tg)
    print(f"\n  wrote guarded preamble into {n} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
