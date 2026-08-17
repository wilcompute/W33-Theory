"""Guard: does the EVIDENCE cover the SCOPE the claim asserts?

WARN-ONLY.

Both lanes produced false closures in the same period by different mechanisms, and the one
thing they shared was a claim whose evidence did not reach its scope:

  * this lane generalised a property of BILINEAR FORMS from a carrier that happened to be a
    symplectic polar space (Pass 5752), and asserted a class from two examples (Pass 5800);
  * the other lane verified a GLOBAL orbit from three pre-promoted witness rows, and
    advertised a gcd of 217 that was actually 1 (Pass 6017-6024).

Neither `check_transitivity` nor an integrity audit catches both.  This tests the join.

Two signals, both cheap:

  1. QUANTIFIER GAP.  Universal language -- every, all, always, generic, for all -- beside
     a small number of recorded witnesses.
  2. PROMOTED SUBSET.  A witness count an order of magnitude below a total the same
     certificate records.

    py -3 scripts/check_scope_vs_evidence.py --selftest
    py -3 scripts/check_scope_vs_evidence.py data/YOUR_CERTIFICATE.json
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

UNIVERSAL = re.compile(r"\b(every|all |always|generic|for all|any |never)\b", re.I)
WITNESS = re.compile(r"(witness|sampled|checked|tested|verified_at|instances|examples)", re.I)
TOTAL = re.compile(r"(total|corpus|population|count|cardinality|orbit_total)", re.I)


def walk(doc, key=""):
    if isinstance(doc, dict):
        for k, v in doc.items():
            yield from walk(v, k)
    elif isinstance(doc, list):
        if doc and all(isinstance(x, (int, str)) for x in doc):
            yield key, doc
        else:
            for x in doc:
                yield from walk(x, key)
    else:
        yield key, doc


def findings(doc) -> list[str]:
    out: list[str] = []
    witness, totals, universals = {}, {}, []
    for k, v in walk(doc):
        if isinstance(v, str) and UNIVERSAL.search(v) and len(v) > 30:
            universals.append((k, v[:90]))
        if isinstance(v, int) and WITNESS.search(k):
            witness[k] = v
        elif isinstance(v, list) and WITNESS.search(k):
            witness[k] = len(v)
        if isinstance(v, int) and TOTAL.search(k):
            totals[k] = v
    for wk, wv in witness.items():
        for tk, tv in totals.items():
            if tv > 0 and wv > 0 and wv * 10 <= tv:
                out.append(f"{wk}={wv} witnesses against {tk}={tv} -- the evidence covers "
                           f"{100 * wv / tv:.1f}% of the population")
    if universals and witness:
        mx = max(witness.values())
        if mx <= 5:
            k, txt = universals[0]
            out.append(f"universal language in `{k}` with at most {mx} recorded "
                       f"witnesses: {txt}...")
    return out


def selftest() -> int:
    cases = [
        ("global orbit from 3 promoted rows",
         {"witness_rows": 3, "orbit_total": 240,
          "claim": "the full orbit is closed under every generator"}, True),
        ("generic claim from 2 examples",
         {"examples": 2,
          "conclusion": "every nondegenerate form attains the bound at each exponent"}, True),
        ("honest prose, same coverage gap",
         {"witness_rows": 3, "orbit_total": 240,
          "claim": "three rows verified; the remainder is open"}, True),
        ("full coverage",
         {"tested": 240, "total": 240, "claim": "every element checked"}, False),
        ("no witness fields at all",
         {"note": "every configuration in this family is primitive"}, False),
    ]
    ok = True
    print("  selftest -- quantifier gap and promoted subset\n")
    for name, doc, want in cases:
        got = bool(findings(doc))
        ok &= got == want
        print(f"    {name:40s} got={str(got):5s} want={str(want):5s} "
              f"{'ok' if got == want else 'FAIL'}")
    print("""
  THE THIRD CASE IS DELIBERATE. A certificate recording three witnesses against a
  population of 240 is flagged even when its prose is scrupulous, because the flag is about
  COVERAGE, not wording. The reader decides whether the gap is adequately disclosed; the
  guard only reports that the gap exists.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    total = 0
    files = [Path(a) for a in argv if not a.startswith("-")]
    for f in files:
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for m in findings(doc):
            total += 1
            print(f"  {f.name}\n      {m}")
    print(f"\n  {total} scope/evidence gap(s) in {len(files)} certificate(s)")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
