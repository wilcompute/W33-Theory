#!/usr/bin/env python3
"""Flag a certificate whose PROSE fields contradict its own COMPUTED fields.

WHY THIS EXISTS.  BT818's certificate carries

    "alpha_exact": 7                                    <- the computation, correct
    "correction":  "... alpha = 9"                      <- the prose, wrong

and in the same file a docstring claiming a Kochen-Specker ledger of s <= 34 with
6 misses, against its own fields ks_best = 36 and ks_misses = 4.  Two contradictions,
one file, and in both the DATA is right and the PROSE is wrong.

THAT ASYMMETRY IS THE WHOLE POINT.  The computed field is produced by the code and is
usually correct.  The prose field is typed by hand, is the half a human reads, and is
the half that gets quoted into the next pass -- which is exactly how alpha = 9
travelled from BT818 into w33_MCCCLI_spectral_graph_breakthrough.py while the public
page, reading the data, correctly says 7.

Every existing certificate guard in this repo checks a certificate against something
EXTERNAL: check_certificates verifies a self-digest, check_stale_boundaries compares
one file to later files, check_rediscovery compares results to an index.  None of them
looks INSIDE a certificate to ask whether it agrees with itself.

METHOD.  For every numeric field `k: v` in a certificate, scan its prose fields for the
same key-word followed by a DIFFERENT number.  A match is reported as a candidate.
Deliberately narrow: only keys whose name also appears in the prose are compared, so a
prose sentence mentioning an unrelated number is not flagged.

    py -3 scripts/check_cert_prose_vs_data.py <files>
    py -3 scripts/check_cert_prose_vs_data.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Fields that are prose by convention in this corpus.
PROSE_KEYS = ("boundary", "theorem", "correction", "note", "notes", "reading",
              "statement", "consequence", "conclusion", "summary", "verdict",
              "status", "why", "purpose", "search_note", "negative_result")


def _numbers_near(text: str, word: str) -> set[int]:
    """Integers ASSERTED of `word` -- reached through a relational operator, not merely
    sitting nearby.

    CALIBRATED, not guessed. The first version took any integer within 60 characters and
    flagged 3,756 of 4,971 certificates: 75%, which is the noise regime Pass 328 measured
    and warned about by name. The false positives were all generic stems -- `rank_d1 = 2775`
    flagged because some sentence said "rank" within sixty characters of a "2".

    What separates BT818's real fault from that noise is a RELATION. Its prose says
    "alpha = 9" and "ks best <= 34"; the noise says "rank" and, elsewhere in the sentence,
    "2". So the number must be reached from the word through =, <=, >=, is, of, or a colon,
    with little between them.
    """
    out: set[int] = set()
    rel = r"(?:\s*(?:=|==|<=|>=|:|\bis\b|\bare\b|\bof\b|\bequals\b)\s*)"
    rx = re.compile(re.escape(word) + r"[^.;\n]{0,20}?" + rel + r"(\d{1,9})(?![\w.])",
                    re.I)
    for m in rx.finditer(text):
        out.add(int(m.group(1)))
    return out


def _flat(obj, prefix=""):
    """Yield (dotted_key, value) for scalar leaves."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _flat(v, f"{prefix}.{k}" if prefix else str(k))
    elif isinstance(obj, (int, float, str, bool)) or obj is None:
        yield prefix, obj


def scan_obj(doc) -> list[tuple[str, str, int, set[int]]]:
    """Return (numeric_key, prose_key, data_value, contradicting_prose_values)."""
    if not isinstance(doc, dict):
        return []
    nums = {k: v for k, v in _flat(doc)
            if isinstance(v, bool) is False and isinstance(v, int)}
    prose = {k: v for k, v in _flat(doc)
             if isinstance(v, str) and len(v) > 12
             and k.split(".")[-1].lower() in PROSE_KEYS}
    out = []
    for nk, nv in nums.items():
        leaf = nk.split(".")[-1]
        # The key must be nameable in prose. Use the LONGEST token, not the first: a key
        # like `ks_best` has a 2-character first token, and taking it skipped exactly the
        # BT818 Kochen-Specker case this guard was built from (its own self-test caught
        # that, which is the argument for writing the self-test before the sweep).
        toks = [t for t in re.split(r"[ _]", leaf) if len(t) >= 4]
        if not toks:
            continue
        stem = max(toks, key=len)
        for pk, pv in prose.items():
            found = _numbers_near(pv, stem)
            if not found:
                continue
            if nv not in found:
                bad = {x for x in found if abs(x - nv) <= max(50, abs(nv))} - {nv}
                if bad:
                    out.append((nk, pk, nv, bad))
    return out


def selftest() -> int:
    cases = [
        ("planted: BT818 shape",
         {"alpha_exact": 7, "correction": "the true value is alpha = 9 here"}, True),
        ("planted: ks ledger shape",
         {"ks_best": 36, "boundary": "every marking obeys ks best <= 34"}, True),
        ("clean: prose agrees with data",
         {"alpha_exact": 7, "correction": "the maximum is alpha = 7, not 10"}, False),
        ("clean: prose names no number",
         {"alpha_exact": 7, "boundary": "alpha is exhaustive and settled"}, False),
        ("clean: unrelated number in prose",
         {"alpha_exact": 7, "boundary": "the graph has 40 vertices"}, False),
        ("clean: no prose field at all", {"alpha_exact": 7, "rows": [1, 2]}, False),
    ]
    ok = True
    print("  selftest -- prose-versus-data contradiction recall\n")
    for name, doc, want in cases:
        got = bool(scan_obj(doc))
        good = got == want
        ok &= good
        print(f"    {name:34s} flagged={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    print("""
  THE 'UNRELATED NUMBER' CASE IS WHAT KEEPS THIS USABLE. A boundary sentence saying "the
  graph has 40 vertices" beside a field alpha_exact=7 must NOT flag -- the number is not
  about that field. Matching requires the FIELD'S OWN NAME to appear near the number, which
  is why alpha_exact=7 versus "alpha = 9" fires and alpha_exact=7 versus "40 vertices" does
  not.

  ITS LIMIT, and it is real: numbers only. A certificate whose prose is wrong in WORDS --
  "the bound is attained" over data showing it is not -- is invisible here. That class is
  what check_spectral_overreach reads, and neither tool covers the other's half.""")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    files = [Path(a) for a in argv if not a.startswith("-")]
    total = 0
    for f in files:
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        for nk, pk, nv, bad in scan_obj(doc):
            total += 1
            try:
                rel = f.resolve().relative_to(ROOT).as_posix()
            except ValueError:
                rel = f.as_posix()
            print(f"  {rel}\n      data {nk} = {nv}   but prose {pk} says "
                  f"{sorted(bad)}")
    print(f"\n  {total} prose/data contradiction(s) in {len(files)} certificate(s)")
    if total:
        print("""
  CANDIDATES. In BT818 the DATA was right and the PROSE was wrong, which is the usual
  direction: the field is computed, the sentence is typed. Check which half is correct
  before editing either -- and note that the prose is the half that gets quoted onward.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
