#!/usr/bin/env python3
"""Pass 4375 -- failure mode 6, applied to the corpus rather than to this session.

Pass 4372 named "the untested premise": a comparison, ratio or price computed before
checking the comparison was licensed.  All three instances were from this session, in a
corpus four thousand passes deep.  Two readings: either the mode is new, or it is old and
nobody was looking.  The second is far likelier, and the difference matters because a mode
that has been operating unnoticed has a backlog.

The shape has a searchable signature.  Every instance took the form "A and B are both X,
therefore ..." where the two objects turned out not to be comparable in the way the
sentence needed:

  * two carriers compared for what they admit, before checking the operation acts on either
  * a machine priced for a property it already had
  * a detector compared against a reference it cannot have at runtime

So look for equality-of-size, equality-of-count and same-as claims, and check whether the
passage says anything about the objects being comparable beyond the count.

    py -3 analysis/w33_pass4375_untested_premises_retroactive.py
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cert_util  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

# "both have N", "the same N", "also N", "matches", "coincides" -- counting arguments.
COUNTING = re.compile(
    r"\b(both (?:have|are|carry|give)|the same (?:size|order|number|count|dimension)|"
    r"also has|matches the|coincid\w+|equal(?:s|ly)? in (?:size|number|order)|"
    r"same cardinality|identical (?:size|count|order))\b", re.I)
# Language showing the writer checked comparability, not just the count.
LICENSED = re.compile(
    r"\b(character|conjugat\w+|isomorph\w+|equivariant|stabiliser|stabilizer|"
    r"permutation character|G-set|gset|as (?:a )?G-set|non-conjugate|inequivalent|"
    r"up to isomorphism|structure|bijection)\b", re.I)


def main() -> int:
    print("=" * 78)
    print("Pass 4375 -- untested premises in the older corpus")
    print("=" * 78)
    print("""  CLAUDE.md already carries the rule this looks for -- 'two transitive G-sets of
  equal size are isomorphic iff their permutation characters agree; comparing sizes proves
  nothing'. It was written after three errors in the 1612-1989 arc. Failure mode 6 is the
  same disease in a wider setting, so the sweep is really asking: did the rule get applied
  outside the case that produced it?\n""")

    rows, by_file = [], Counter()
    for f in sorted((ROOT / "analysis").glob("*.md")):
        try:
            lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, ln in enumerate(lines):
            if not COUNTING.search(ln):
                continue
            window = " ".join(lines[max(0, i - 4):i + 5])
            if LICENSED.search(window):
                continue
            rows.append((f.name, i + 1, ln.strip()[:74]))
            by_file[f.name] += 1

    print(f"  counting claims with no comparability language nearby: {len(rows)}")
    print(f"  files involved                                       : {len(by_file)}")
    print(f"\n  {'file':52s} count")
    for name, n in by_file.most_common(10):
        print(f"  {name[:52]:52s} {n}")
    print("\n  a sample, to show what the signature actually catches:")
    for name, ln, txt in rows[:10]:
        print(f"    {name[:40]:40s}:{ln:<5d} {txt}")

    print(f"""
  {len(rows)} passages assert that two things share a count without any nearby language about
  whether they are comparable in the way the argument needs.

  THIS IS A TRIAGE LIST AND ITS PRECISION IS LOW BY CONSTRUCTION.  Most counting statements
  are perfectly sound -- an author may simply be reporting two numbers, and the licence may
  sit in a paragraph the four-line window does not reach.  What the list is for is the
  opposite direction: the three errors of this session all had this signature, so a passage
  with the signature AND a conclusion drawn from it is where mode 6 lives.

  THE HONEST ANSWER TO THE QUESTION THIS PASS ASKED.  I cannot conclude from this that the
  older corpus contains N untested premises, because I have not read {len(rows)} passages. What
  I can conclude is narrower and still useful: the signature is COMMON, the existing G-set
  rule was written for one instance of it, and nothing in the repository was checking for
  the general shape until now. That is the backlog, and it is a reading task rather than a
  computation.""")

    out = {"flagged": len(rows), "files": len(by_file),
           "top_files": dict(by_file.most_common(12)),
           # Pass 4429: the TEXT is the durable record; the line number is navigation
           # only, and the digest says which version of the file was scanned.
           "sample": [{"file": a, "line": b, "text": c,
                       "source": cert_util.source_digest(ROOT / "analysis" / a)}
                      for a, b, c in rows[:40]],
           "precision": "low by construction; a triage list, not a verdict",
           "conclusion": "the signature is common and was unchecked; quantifying the real "
                         "backlog needs reading, not more grepping"}
    p = ROOT / "data" / "PART_W33_PASS4375_UNTESTED_PREMISES.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
