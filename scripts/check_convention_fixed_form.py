#!/usr/bin/env python3
"""Flag a bilinear/quadratic form, basis, or composition order fixed by CONVENTION.

WHY THIS EXISTS, and it is the most-repeated fault in this lane's record.

  * Composition direction -- FOUR incidents. Of five ways to compose two canonical
    labellings and their inverses, all five are permutations, all five survive a
    canonical-form comparison, and exactly one is an isomorphism.
  * Key name implies convention -- FOUR incidents in one checker.
  * Symplectic form -- Pass 5246. The Tits parametrisation is written against the
    reversal pairing (0,3)(1,2); my builder uses (0,1)(2,3). Assuming produced 256
    conjugate pairs at q=8.
  * AND THEN AGAIN IN PASS 5272, one pass after the guard family was built. The
    vectorised rewrite hardcoded the form Pass 5246 had DETERMINED for Suzuki-Tits
    and applied it to the elliptic quadric, where it is wrong. q=64 caught it.

The fix that works is never "reason more carefully about the convention". It is to
BUILD ALL THE CANDIDATES AND KEEP THE ONE THAT SATISFIES AN INVARIANT YOU CAN STATE.
Pass 5246 scans all 63 binary alternating forms; exactly one survives, and that is a
determination rather than a guess. This guard looks for the places where that scan
was skipped.

WHAT IT CATCHES: a form/basis/order chosen with language of assumption -- "standard",
"the usual", "by convention", "as usual", "we take", "WLOG" -- near a form, basis,
pairing, or composition. What it does NOT catch: a form that is scanned, solved for,
or checked against an invariant, because those name the invariant and are suppressed.

    py -3 scripts/check_convention_fixed_form.py <files>
    py -3 scripts/check_convention_fixed_form.py --selftest
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

OBJECT = (r"(?:symplectic form|bilinear form|quadratic form|alternating form|"
          r"\bbasis\b|\bpairing\b|composition (?:order|direction)|"
          r"orientation|sign convention|inner product)")
ASSUMED = (r"(?:standard|usual|conventional|by convention|as usual|we take|we use|"
           r"take the|the obvious|canonical choice|WLOG|without loss of generality|"
           r"assume(?:d|s)?)")

RULES = {
    "form_fixed_by_convention": re.compile(
        ASSUMED + r".{0,50}" + OBJECT, re.I | re.S),
    "object_described_as_standard": re.compile(
        OBJECT + r".{0,40}\b(?:is|are)\s+(?:the\s+)?" + ASSUMED, re.I | re.S),
}

# Language that names an invariant or a scan. Its presence means the choice was
# DETERMINED, not assumed, and the finding is suppressed.
SAFE = re.compile(
    r"(?:scan(?:ned|ning)?\s+all|all 63|determined by|solved for|"
    r"keep the one|satisfies the invariant|verified against|both candidates|"
    r"exactly one survives|checked against|re-?derive)", re.I)


def scan_text(text: str) -> list[tuple[str, int, str]]:
    out = []
    # split("\n") not splitlines(): the latter treats formfeed as a line break and shifts
    # every reported line number past such a byte (Pass 4929).
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
        ("planted: standard symplectic form",
         "We use the standard symplectic form throughout.", True),
        ("planted: WLOG basis",
         "WLOG take the basis to be ordered this way.", True),
        ("planted: usual composition order",
         "Composition order is the usual one for this library.", True),
        ("clean: form was SCANNED",
         "We scan all 63 binary alternating forms and keep the one with no "
         "conjugate pair; exactly one survives.", False),
        ("clean: determined by invariant",
         "The symplectic form is determined by the invariant that O is a coclique.", False),
        ("clean: both candidates built",
         "We build both candidates for the composition order and keep the one "
         "that is an isomorphism.", False),
        ("clean: unrelated prose",
         "The ovoid has q^2+1 points and Hoffman caps alpha at the same number.", False),
    ]
    ok = True
    print("  selftest -- assumption-versus-determination recall\n")
    for name, text, want in cases:
        got = bool(scan_text(text))
        good = got == want
        ok &= good
        print(f"    {name:36s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE THREE CLEAN CASES ARE THE WHOLE DESIGN. Naming a scan, an invariant, or a
  build-both-and-test suppresses the finding, because those are exactly the practices this
  guard exists to encourage. A checker that fired on them would punish the fix.

  ITS LIMIT: it reads how a choice is DESCRIBED, not whether the choice is right. Code that
  silently hardcodes a form with no comment at all is invisible to it -- and that is
  precisely how Pass 5272 reintroduced the fault, in a rewrite that carried no prose. The
  honest reading is that this catches the documented half of the failure mode.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [Path(a) for a in argv if not a.startswith("-")]
    total = 0
    for f in files:
        if not f.is_file():
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
    print(f"\n  {total} convention-fixed choice(s) in {len(files)} file(s)")
    if total:
        print("""
  CANDIDATES, not verdicts. The fix is never to reason harder about the convention: build
  every candidate and keep the one satisfying an invariant you can state. Pass 5246 scans
  all 63 binary alternating forms and exactly one survives.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
