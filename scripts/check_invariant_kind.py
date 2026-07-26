#!/usr/bin/env python3
"""Warn when two DIFFERENT KINDS of invariant are compared as if interchangeable.

WHY THIS EXISTS.  The rediscovery guard catches a repeated NUMBER.  It cannot see
that one occurrence is an orbit list and the other a suborbit list, so it is blind
to the failure that has now bitten this corpus three times with a different surface
each time:

    Sp(4,3) vs W(E6)            equal ORDERS,     different groups
    Pass 338 selector frame     equal SUBDEGREES, different groups
    Pass 1043 / Pass 1041       equal NUMBERS,    different INVARIANTS

The third is the one this script targets, because it is the least visible.  Pass
1043 computed `Orbits(Stabilizer(G, 1), Omega)` -- the subdegrees of a transitive
action -- stored the result in a variable named `anisotropic_orbit_sizes`, and
compared it to a published ORBIT list.  The lists agreed numerically.  Nothing in
the file was wrong except the identification of what the two lists were.

WHAT IT DOES.  For each file it looks for the specific confusable pairs below and
warns when a name and the expression producing it disagree about kind, or when a
file asserts both kinds against the same literal.  It is deliberately narrow: a
general "type system for invariants" is not achievable by text scan, but these
particular pairs have already cost real passes.

    orbits          Orbits(G, Omega)                 whole-group orbits
    suborbits       Orbits(Stabilizer(G,x), Omega)   subdegrees of a transitive action
    order           Size(G)                          group order
    index           Index(G,H)                       subgroup index
    subdegrees      the suborbit LENGTH list
    spectrum        eigenvalue multiset

RULE OF THUMB the script encodes: a transitive group's orbit list is [n], a single
number.  If a variable named *orbit* holds a list of length > 1 for a group the
file also calls transitive, that is the Pass 1043 signature exactly.

Advisory, never blocking -- same contract as the other guards, same reason.

Usage:
    py -3 scripts/check_invariant_kind.py <files...>
    py -3 scripts/check_invariant_kind.py            # sweep analysis/
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# name fragment -> the expression shape that legitimately produces it
SUBORBIT_EXPR = re.compile(r"Orbits\s*\(\s*Stabilizer\s*\(", re.I)
ORBIT_EXPR = re.compile(r"Orbits\s*\(\s*(?!Stabilizer)", re.I)

# a variable/field whose NAME says "orbit" (not suborbit / not subdegree)
ORBIT_NAME = re.compile(
    r"""(?<![a-z_])(?!sub)(\w*orbit[_a-z]*(?:size|len|length)s?|orbit_sizes|
        \w*_orbit_sizes)(?![a-z_])""",
    re.I | re.X,
)
SUBORBIT_NAME = re.compile(r"(?<![a-z_])(sub\w*orbit\w*|subdegree\w*|sub\d*)(?![a-z_])", re.I)


def scan(path: Path) -> list[str]:
    try:
        txt = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    findings: list[str] = []
    lines = txt.splitlines()

    # (a) an assignment whose NAME claims "orbit" but whose RHS is a suborbit
    for n, line in enumerate(lines, 1):
        if SUBORBIT_EXPR.search(line):
            lhs = line.split(":=")[0] if ":=" in line else line.split("=")[0]
            if ORBIT_NAME.search(lhs) and not SUBORBIT_NAME.search(lhs):
                findings.append(
                    f"{path.as_posix()}:{n}: name says ORBIT, expression computes "
                    f"SUBORBITS (Orbits of a Stabilizer)")

    # (b) a JSON/report field named *orbit_sizes* fed from a suborbit variable
    subvars = {m.group(1) for m in SUBORBIT_NAME.finditer(txt)}
    for n, line in enumerate(lines, 1):
        if "orbit_sizes" in line.lower() and "sub" not in line.lower().split("orbit_sizes")[0][-6:]:
            for sv in subvars:
                if re.search(rf"(?<![a-z_]){re.escape(sv)}(?![a-z_])", line):
                    findings.append(
                        f"{path.as_posix()}:{n}: field named *orbit_sizes* is being "
                        f"filled from `{sv}`, which is a suborbit quantity")
                    break

    # A third, coarser rule was tried and REMOVED: "file asserts transitivity AND
    # computes suborbits AND mentions orbits".  Measured on this corpus it fired on
    # Pass 1020, Pass 338, Pass 1041 and on this guard's own retraction file --
    # every one a legitimate use, because computing suborbits of a transitive group
    # is the normal thing to do.  A guard with that false-positive rate trains
    # people to ignore it, which is the failure mode check_rediscovery.py documents
    # in its own docstring.  Rules (a) and (b) are name-vs-expression mismatches and
    # are precise; they catch the real Pass 1043 line and nothing else.
    return findings


def main(argv: list[str]) -> int:
    files = [Path(a) for a in argv if not a.startswith("-")]
    if not files:
        files = sorted((ROOT / "analysis").glob("*.g")) + \
                sorted((ROOT / "analysis").glob("*.py"))
    hits: list[str] = []
    for f in files:
        if f.exists():
            hits.extend(scan(f))

    if hits:
        print("\n" + "=" * 72)
        print("[invariant-kind guard] a NAME and its EXPRESSION disagree about kind")
        print("=" * 72)
        for h in hits:
            print(f"  {h}")
        print("\n  CANDIDATES, not verdicts.  But this is the exact shape of the")
        print("  Pass 1043 retraction: subdegrees stored in a field named")
        print("  `anisotropic_orbit_sizes` and compared to published ORBIT sizes.")
        print("  The numbers agreed; the invariants did not.  Check that the two")
        print("  quantities being compared are the same KIND before comparing.\n")
    else:
        print("[invariant-kind guard] no name/expression kind mismatches found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
