#!/usr/bin/env python3
"""Look a pass's own numbers up in CERTIFICATE_RESULTS_INDEX.md before it is committed.

WHY THIS IS A SEPARATE SCRIPT AND NOT AN EDIT TO check_rediscovery.py.  That guard is
self-tested, registered, and reads RESULTS_INDEX.md with a grammar calibrated at Pass
328 and re-measured at Pass 1073.  Adding a second lookup table to it needs a decision
about which grammar owns a collision, and changing a green guard at the end of a pass
is how green guards stop being green.  This does the lookup alongside it instead.

WHAT IT DOES.  Extracts `key@value` tokens from a staged certificate the same way
build_certificate_index.py does, then reports any that already appear in another
certificate.  That is the check whose absence cost this session six passes: Pass
4800's `alpha@18` was in a committed certificate the whole time.

WARN-ONLY, like every guard here.  A shared token is a candidate, not a verdict --
two passes can legitimately report the same number for the same object.

    py -3 scripts/check_certificate_rediscovery.py <certificates>
    py -3 scripts/check_certificate_rediscovery.py --selftest
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "CERTIFICATE_RESULTS_INDEX.md"
sys.path.insert(0, str(ROOT / "scripts"))


def load_index() -> dict[str, list[str]]:
    if not INDEX.is_file():
        return {}
    out = {}
    for tok, files in re.findall(r"\| `([^`]+)` \| (.+) \|",
                                 INDEX.read_text(encoding="utf-8", errors="replace")):
        out[tok] = re.findall(r"`([^`]+)`", files)
    return out


def selftest() -> int:
    from build_certificate_index import tokens
    cases = [
        ("aliased key becomes canonical", {"alpha_exact": 18}, "alpha@18", True),
        ("plain key kept", {"deficit": 8}, "deficit@8", True),
        ("schema field skipped", {"pass": 5556}, "pass@5556", False),
    ]
    ok = True
    print("  selftest -- token extraction matches the index builder\n")
    for name, doc, tok, want in cases:
        got = tok in tokens(doc)
        good = got == want
        ok &= good
        print(f"    {name:32s} {tok:16s} got={str(got):5s} want={str(want):5s} "
              f"{'PASS' if good else 'FAIL'}")
    idx = load_index()
    print(f"\n    index loaded: {len(idx):,} tokens")
    print("""
  IT REUSES build_certificate_index.tokens RATHER THAN REIMPLEMENTING IT. Two copies of a
  token grammar drift, and a lookup that tokenises differently from the index it queries
  returns silence rather than an error -- which is indistinguishable from a clean result.""")
    return 0 if ok and idx else 1


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    from build_certificate_index import tokens
    idx = load_index()
    if not idx:
        print("  no CERTIFICATE_RESULTS_INDEX.md; run build_certificate_index.py first")
        return 0
    files = [Path(a) for a in argv if not a.startswith("-")]
    total = 0
    for f in files:
        if not f.is_file() or f.suffix != ".json":
            continue
        try:
            doc = json.loads(f.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            continue
        # RANK BY FILE-HITS, not by token count (Pass 5637). Firing is near-universal --
        # 70% of certificates carry some shared token -- so `whether` one fired is nearly
        # information-free and only `which` matters. A stem the corpus uses in 1,155
        # places is bookkeeping; a stem it uses in 5 is a result. Pass 5580 ranked stems
        # by DISTINCT TOKENS, saw routing keys on top, and prescribed a blocklist that
        # moved 2 certificates out of 5,056 -- because those tokens live in ten files.
        hits = []
        for t in tokens(doc):
            prior = [x for x in idx.get(t, []) if x != f.name]
            if prior:
                stem = t.split("@")[0]
                hits.append((sum(len(v) for k, v in idx.items()
                                 if k.split("@")[0] == stem), t, prior))
        hits.sort()
        total += len(hits)
        for rank, (reach, t, prior) in enumerate(hits):
            mark = "RARE  " if rank < 3 else "      "
            print(f"  {mark}{f.name}\n        {t}  (stem reaches {reach} file-slots)"
                  f"  already in: "
                  f"{', '.join(prior[:3])}{' ...' if len(prior) > 3 else ''}")
    print(f"\n  {total} token(s) already present elsewhere, over {len(files)} certificate(s)")
    if total:
        print("""
  CANDIDATES, RAREST FIRST. Pass 4800's `alpha@18` sat in a committed certificate while
  six passes re-derived it. Read the RARE ones first: a stem with small reach names a
  quantity, a stem with large reach names bookkeeping. Ranking is the fix that a stem
  blocklist was not -- Pass 5635 A/B'd the blocklist and it moved two certificates.""")
    print("  (zero means nothing unless --selftest passes; run it)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
