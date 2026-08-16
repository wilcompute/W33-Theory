#!/usr/bin/env python3
"""Flag "|X| = |Y|, therefore X is Y" -- an order match written as an identification.

WHY THIS EXISTS, with two measured instances in this repository.

  * BT159 states "<forbidden pocket> has order 1152 = |W(F4)|" and concludes it
    "recovers the same F4/tomotope/24-cell symmetry". Its OWN certificate carries the
    generated group's element-order distribution {1:1, 2:27, 3:80, 4:84, 6:432,
    8:144, 12:384}. W(F4)'s is {1:1, 2:139, 3:80, 4:228, 6:464, 8:144, 12:96}.
    Twenty-seven involutions against a hundred and thirty-nine. Same order, different
    group, and the refutation was already inside the file.

  * Pass 5476 nearly repeated it: |Sp(4,3)|/|W(F4)| = 51840/1152 = 45 exactly, which
    is Lagrange satisfied perfectly. W(F4) still does not embed in Sp(4,3).

THE STRUCTURAL POINT. The orders that recur in this corpus -- 96, 192, 288, 384, 576,
1152, 25920, 51840 -- are smooth 2^a 3^b numbers, and this substrate has several
unrelated 2,3-group towers. Matching orders between two of them is close to
guaranteed and carries almost no information. The null hypothesis for any such
coincidence is arithmetic.

WHAT THIS CATCHES: an order equality adjacent to identification language -- "is",
"equals", "recovers", "the same", "therefore" -- naming a group. What it does NOT
catch: an order stated alongside an actual test, because those name the test and are
suppressed.

CHEAP CHECKS THAT SETTLE IT, in increasing cost: element-order spectrum, centre
order, derived subgroup order, then IsomorphismGroups. The first is usually enough
and is usually already computed.

    py -3 scripts/check_order_coincidence.py <files>
    py -3 scripts/check_order_coincidence.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# A named group, loosely: W(X), a classical family, or a bare capitalised group name.
GROUP = (r"(?:W\(\s*[A-Z]_?\d*\s*\)|Sz\(\d+\)|Sp\(\d+,\d+\)|PSp\(\d+,\d+\)|"
         r"S?[LOU]\(\d+,\d+\)|GO\d*[+-]?\(\d+\)|A\d+|S\d+|M\d+|"
         r"[A-Z][A-Za-z]*\(\d+(?:,\d+)?\))")
IDENT = (r"(?:\bis\b|\bequals?\b|\brecovers?\b|\bthe same\b|\btherefore\b|"
         r"\bmust be\b|\bgives\b|\bidentif(?:y|ies|ied)\b|=)")

RULES = {
    "order_equals_group": re.compile(
        r"order\s*(?:of\s*)?\S{0,12}\s*=\s*\|\s*" + GROUP + r"\s*\|", re.I),
    "order_then_identification": re.compile(
        r"\|\s*" + GROUP + r"\s*\|.{0,40}" + IDENT + r".{0,40}" + GROUP, re.I | re.S),
    "same_order_therefore_same": re.compile(
        r"(?:same|equal|matching)\s+order.{0,50}" + IDENT, re.I | re.S),
}

# An actual test having been run suppresses the finding.
SAFE = re.compile(
    r"(?:IsomorphismGroups|element[- ]order spectrum|order spectrum|"
    r"derived subgroup|centre order|center order|not isomorphic|"
    r"is NOT|order match|coincidence|divisibility is not|does not embed|"
    r"structure description|conjugacy class)", re.I)


def scan_text(text: str) -> list[tuple[str, int, str]]:
    out = []
    # split("\n"), not splitlines(): the latter treats formfeed as a line break and
    # shifts every reported line number past such a byte (Pass 4929).
    lines = text.split("\n")
    for name, rx in RULES.items():
        for m in rx.finditer(text):
            lo = max(0, m.start() - 300)
            if SAFE.search(text[lo:m.end() + 300]):
                continue
            ln = text.count("\n", 0, m.start()) + 1
            snip = lines[ln - 1].strip()[:100] if ln - 1 < len(lines) else ""
            out.append((name, ln, snip))
    return out


def selftest() -> int:
    cases = [
        ("planted: BT159's exact sentence",
         "<forbidden pocket> has order 1152 = |W(F4)|, so it recovers the same "
         "F4 symmetry.", True),
        ("planted: same order therefore same",
         "They have the same order and therefore are the same group.", True),
        ("clean: order stated WITH a test",
         "The stabiliser has order 1152 = |W(F4)| and IsomorphismGroups confirms "
         "it.", False),
        ("clean: order match named as such",
         "order 1152 = |W(F4)| is an order match, not an identification.", False),
        ("clean: explicit negative",
         "|Sp(4,3)|/|W(F4)| = 45 exactly, but W(F4) does not embed.", False),
        ("clean: spectra compared",
         "Both have order 1152; the element-order spectrum differs, so they are "
         "not isomorphic.", False),
        ("clean: unrelated prose",
         "The ovoid has q^2+1 points and Hoffman caps alpha there.", False),
    ]
    ok = True
    print("  selftest -- order-match-as-identification recall\n")
    for name, text, want in cases:
        got = bool(scan_text(text))
        good = got == want
        ok &= good
        print(f"    {name:36s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE FOUR CLEAN CASES ARE THE DESIGN. Stating an order alongside a real test, or naming
  the coincidence as a coincidence, or reporting the negative, must not flag -- those are
  the behaviours this guard exists to encourage, and firing on them would punish the fix.

  ITS LIMIT: it reads sentences. A file that silently assumes two groups are the same
  without saying so is invisible, and a file that says it carefully while being wrong is
  invisible too. What decides these is an element-order spectrum, which is cheap and
  usually already computed -- BT159 had published its own and nobody compared.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [Path(a) for a in argv if not a.startswith("-")]
    total = 0
    for f in files:
        if not f.is_file() or f.resolve() == Path(__file__).resolve():
            continue
        try:
            hits = scan_text(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for name, ln, snip in hits:
            total += 1
            try:
                rel = f.resolve().relative_to(ROOT).as_posix()
            except ValueError:
                rel = f.as_posix()
            print(f"  {rel}:{ln}  [{name}]\n      {snip}")
    print(f"\n  {total} order-coincidence claim(s) in {len(files)} file(s)")
    if total:
        print("""
  CANDIDATES. The settling check is the element-order spectrum -- cheap, and usually
  already computed. BT159 published its own spectrum next to the claim it refutes.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
