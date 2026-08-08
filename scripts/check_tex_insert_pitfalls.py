#!/usr/bin/env python3
"""Scan the manuscript inserts for the LaTeX pitfalls that actually halt our builds.

Compiling the blueprint one error at a time costs a full tectonic run per fault, and the
faults come in families.  This finds every instance of each family in one pass.

CALIBRATION NOTE (worth reading before adding a family).  A fifth family was tried and
removed: "lowercase macro not defined in the preamble" flagged 275 sites of which two were
real -- the inserts define their own operators with \\providecommand, so the check was
99% noise, exactly the failure `scripts/check_rediscovery.py` was calibrated to avoid.
Every family below is precise: it either fires on a real fault or not at all.  When the
heuristic route is this noisy, the right oracle is LaTeX itself:

    tectonic -X compile holonet_machine_blueprint.tex -Z continue-on-errors --keep-logs
    grep -E '^! ' holonet_machine_blueprint.log

which harvests every fault in one run instead of one run per fault.

Families, all observed in analysis/*_insert.tex:

  row-bracket   a row ended with \\\\ and the next row's first cell starts with '[', so
                LaTeX reads it as \\\\[<len>] and reports "Illegal unit of measure".
                Fix: brace the cell, {[13,5,5]}.
  double-sub    x_a^b_c -- two subscripts on one atom, "Double subscript".
                Fix: parenthesise, (x_a^b)_c.
  needs-pkg     an environment used without the package that defines it.
  undef-env     a theorem-like environment used in an insert that neither the insert nor
                the preamble declares.  Note the preamble deliberately declares none:
                22 inserts run their own \\newtheorem, and a preamble declaration would
                collide with all of them.  So each insert must carry its own.
  ctrl-byte     a stray control byte, almost always a TeX control word eaten by a Python
                or shell escape: \\frac written through an unescaped string becomes
                formfeed + "rac", and TeX then reports "Missing $ inserted" some lines
                later, pointing nowhere near the cause.  Two files carried this.
  bare-underscore
                an unescaped _ in TEXT mode, e.g. MISSING_OBSERVABLE in prose.  TeX reads
                it as a subscript and reports "Missing $ inserted".  Added at Pass 4285:
                this checker scanned all 287 inserts and reported zero pitfalls while two
                of them failed to compile for exactly this reason -- a recall gap the
                planted-fault test could not have found, because the family did not exist.

    py -3 scripts/check_tex_insert_pitfalls.py [files...]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BODY = ROOT / "holonet_machine_blueprint_body.tex"

# environment -> the package that must be in the preamble
NEEDS = {"tcolorbox": "tcolorbox", "tikzcd": "tikz-cd", "algorithmic": "algpseudocode",
         "minted": "minted", "forest": "forest", "sidewaystable": "rotating"}

# theorem-like environments that only exist once someone has \newtheorem'd them
THMLIKE = {"theorem", "corollary", "lemma", "proposition", "definition", "remark",
           "example", "conjecture", "claim", "fact", "observation", "notation"}

ROW_BRACKET = re.compile(r"\\\\\s*\n\s*\[")
# a sub, then a sup group, then another sub on the same atom
DOUBLE_SUB = re.compile(r"_(?:\{[^{}]*\}|[A-Za-z0-9])"
                        r"\^(?:\{[^{}]*\}|[A-Za-z0-9])"
                        r"_(?:\{|\\)")
NEWTHM = re.compile(r"\\newtheorem\*?\s*\{([A-Za-z]+)\}")
BEGIN = re.compile(r"\\begin\{([A-Za-z*]+)\}")

# For bare-underscore detection: blank out anything where _ is legal before looking.
_MATH = re.compile(r"\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)", re.S)
# verbatim-like environments take _ literally; flagging them is a false positive, and the
# first version of this family produced one on a certificate hash inside \begin{verbatim}.
_VERB = re.compile(r"\\begin\{(verbatim|lstlisting|minted|alltt)\*?\}.*?"
                   r"\\end\{\1\*?\}", re.S)
_SAFE_CMD = re.compile(r"\\(?:label|ref|eqref|cref|Cref|autoref|input|include|cite|"
                       r"texttt|verb|url|href|path)\s*\{[^}]*\}")
_ESCAPED = re.compile(r"\\_")
_COMMENT = re.compile(r"(?<!\\)%.*")


def bare_underscores(txt: str):
    """Positions of _ that TeX will read as a subscript in text mode."""
    masked = _COMMENT.sub(lambda m: " " * len(m.group()), txt)
    for pat in (_VERB, _MATH, _SAFE_CMD, _ESCAPED):
        masked = pat.sub(lambda m: " " * len(m.group()), masked)
    return [m.start() for m in re.finditer(r"_", masked)]


def _pkgs_of(path: Path) -> set[str]:
    if not path.exists():
        return set()
    txt = path.read_text(encoding="utf-8", errors="replace")
    out: set[str] = set()
    for m in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", txt):
        out.update(p.strip() for p in m.group(1).split(","))
    return out


def includers() -> dict[str, list[Path]]:
    """Which manuscript bodies actually \\input each insert, transitively through the
    generated appendices.

    WHY THIS EXISTS.  Until Pass 4299 the needs-pkg family tested every insert against the
    BLUEPRINT's preamble only.  That made it structurally blind to a missing package in
    any other document, and it duly missed photonic_holonet's absent tcolorbox -- reported
    as a clean scan while the manuscript failed to compile.  A checker that always consults
    the wrong preamble cannot be fixed by better recall testing."""
    inc: dict[str, list[Path]] = {}
    # Start at the TOP-LEVEL manuscripts, not the bodies.  The wrappers are what carry
    # \input of the shared frontier manifest, and an earlier version that began at
    # *_body.tex mapped the two tcolorbox inserts to no manuscript at all -- so the fix
    # for the blueprint-only blindness silently did nothing.
    roots = [p for p in ROOT.glob("*.tex") if not p.name.endswith("_body.tex")]

    def links(p: Path) -> set[str]:
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return set()
        return {Path(m).name.removesuffix(".tex")
                for m in re.findall(r"\\(?:input|include)\{([^}]*)\}", txt)}

    def resolve(stem: str) -> Path | None:
        for cand in (ROOT / f"{stem}.tex", ROOT / "analysis" / f"{stem}.tex",
                     ROOT / "manuscripts" / f"{stem}.tex"):
            if cand.exists():
                return cand
        return None

    for r in roots:
        frontier, seen = list(links(r)), set(links(r))
        while frontier:
            s = frontier.pop()
            inc.setdefault(s, []).append(r)
            f = resolve(s)
            if f is None:
                continue
            for n in links(f):
                if n not in seen:
                    seen.add(n)
                    frontier.append(n)
    return inc


_INCLUDERS = includers()


def preamble_packages(stem: str | None = None) -> set[str]:
    """Packages available to an insert: the union over every manuscript that includes it.
    With no stem, the blueprint's own preamble (the historical behaviour)."""
    if stem is None:
        return _pkgs_of(BODY)
    hosts = _INCLUDERS.get(stem)
    if not hosts:
        return _pkgs_of(BODY)          # unincluded: judge against the default target

    def host_pkgs(root: Path) -> set[str]:
        """A wrapper's packages plus those of every body it inputs."""
        out = _pkgs_of(root)
        txt = root.read_text(encoding="utf-8", errors="replace")
        for m in re.findall(r"\\(?:input|include)\{([^}]*)\}", txt):
            n = Path(m).name.removesuffix(".tex")
            if n.endswith("_body"):
                out |= _pkgs_of(ROOT / f"{n}.tex")
        return out

    out = host_pkgs(hosts[0])
    for h in hosts[1:]:
        out &= host_pkgs(h)            # must work in EVERY host, so intersect
    return out


def preamble_theorems() -> set[str]:
    if not BODY.exists():
        return set()
    return set(NEWTHM.findall(BODY.read_text(encoding="utf-8", errors="replace")))


def scan(path: Path, have: set[str], thms: set[str]) -> list[tuple[int, str, str]]:
    txt = path.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()

    def ctx(pos: int) -> tuple[int, str]:
        ln = txt.count("\n", 0, pos)
        return ln + 1, (lines[ln].strip()[:62] if ln < len(lines) else "")

    hits: list[tuple[int, str, str]] = []
    for m in re.finditer(r"[\x00-\x08\x0b\x0c]", txt):
        ln, c = ctx(m.start())
        hits.append((ln, f"ctrl-byte:0x{ord(m.group()):02x}", c))
    for m in ROW_BRACKET.finditer(txt):
        ln, c = ctx(m.end() - 1)
        hits.append((ln, "row-bracket", c))
    for m in DOUBLE_SUB.finditer(txt):
        ln, c = ctx(m.start())
        hits.append((ln, "double-sub", c))
    seen_lines: set[int] = set()
    for pos in bare_underscores(txt):
        ln, c = ctx(pos)
        if ln not in seen_lines:
            seen_lines.add(ln)
            hits.append((ln, "bare-underscore", c))
    # Judge each insert against the preamble(s) of the manuscript(s) that include it,
    # not against a single hard-coded document.
    have = preamble_packages(path.stem) or have
    for env, pkg in NEEDS.items():
        if pkg in have:
            continue
        m = re.search(r"\\begin\{" + env + r"\}", txt)
        if m:
            ln, c = ctx(m.start())
            hits.append((ln, f"needs-pkg:{pkg}", c))

    local = set(NEWTHM.findall(txt)) | thms
    seen: set[str] = set()
    for m in BEGIN.finditer(txt):
        env = m.group(1)
        if env not in THMLIKE or env in local or env in seen:
            continue
        seen.add(env)
        ln, c = ctx(m.start())
        hits.append((ln, f"undef-env:{env}", c))
    return hits


def main(argv: list[str]) -> int:
    have, thms = preamble_packages(), preamble_theorems()
    files = ([Path(a) for a in argv] if argv
             else sorted((ROOT / "analysis").glob("*_insert.tex")))
    total = 0
    for f in files:
        hits = scan(f, have, thms)
        if not hits:
            continue
        total += len(hits)
        try:
            label = f.resolve().relative_to(ROOT).as_posix()
        except ValueError:                       # a file outside the repo, e.g. a probe
            label = f.as_posix()
        print(f"\n{label}")
        for ln, kind, c in sorted(hits):
            print(f"  line {ln:5d}  {kind:22s} {c}")
    print(f"\nscanned {len(files)} files, {total} pitfalls")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
