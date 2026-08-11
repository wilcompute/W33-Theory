#!/usr/bin/env python3
"""Pass 4804 -- the novelty guard was blind to more than half the claims, and the half it
now sees is mostly not what it wants.

Pass 4802 found check_novelty_claims.py could not match "is the first X" -- the commonest
way anyone in this corpus asserts priority -- and fired instead on "does not appear to be
new", which is an author DISCLAIMING it.  Both were fixed.  This runs the corrected guard
over all 1,705 analysis markdown files and asks what the fix actually bought.

47 novelty claims collide with the encyclopedia.  26 of them were invisible before, so the
guard's earlier clean runs covered 45% of what it was supposed to cover.

BUT THE 26 ARE NOT 26 REDISCOVERIES, and saying so would repeat this session's most common
mistake.  "First" in this corpus is used two ways:

    LITERATURE priority   "the first time the W(3,3) substrate has been studied as ..."
    INTERNAL sequencing   "the first objectwise lift of BT1362", "Q6 is the first
                          super-Ramanujan crossing", "the first recursion depth whose ..."

Only the first kind is a novelty claim in the sense the guard exists for.  The second is an
ordering statement about this project's own objects and is not asserting priority over
anyone.  A guard that reports them together inflates its own yield and trains the reader to
skim it, which is how the rediscovery guard got ignored the first time.

    py -3 analysis/w33_pass4804_the_novelty_guard_saw_half.py
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

s = importlib.util.spec_from_file_location(
    "nc", ROOT / "scripts" / "check_novelty_claims.py")
NC = importlib.util.module_from_spec(s)
s.loader.exec_module(NC)

NEWLY_VISIBLE = re.compile(
    r"(?:is|are|appears? to be|seems? to be|remains?) the first\b"
    r"|we are the first|for the first time|hitherto (?:unknown|unnoticed|unstated)", re.I)

# an INTERNAL "first" names one of this project's own objects
INTERNAL = re.compile(
    r"\bBT\d{3,4}\b|\bPass\s*\d{3,4}\b|\bQ\d\b|\bq\^?\d\b|\brecursion depth\b|"
    r"\bin the chain\b|\bof the chain\b|\bthis (?:chain|ladder|arc|track)\b|"
    r"\bfeedback pass\b|\bcrossing\b|\blift of\b", re.I)


def main() -> int:
    print("=" * 78)
    print("Pass 4804 -- what did fixing the novelty guard actually buy?")
    print("=" * 78)

    enc = NC.load_encyclopedia()
    files = sorted((ROOT / "analysis").rglob("*.md"))
    rows = []
    for p in files:
        for h in NC.check(p, enc):
            m = re.search(r"novelty asserted: (.*)", h)
            line = (m.group(1) if m else "").strip()
            new = bool(NEWLY_VISIBLE.search(line))
            internal = bool(INTERNAL.search(line))
            rows.append({"file": p.name, "line": line[:110],
                         "newly_visible": new, "internal_sequencing": internal})

    total = len(rows)
    newly = [r for r in rows if r["newly_visible"]]
    lit = [r for r in newly if not r["internal_sequencing"]]
    internal = [r for r in newly if r["internal_sequencing"]]

    print(f"\n  encyclopedia sources          : {len(enc)}")
    print(f"  files scanned                 : {len(files):,}")
    print(f"  novelty claims with enc hits  : {total}")
    print(f"    visible before Pass 4802    : {total - len(newly)}")
    print(f"    newly visible               : {len(newly)}")
    print(f"      of those, LITERATURE priority : {len(lit)}")
    print(f"      of those, INTERNAL sequencing : {len(internal)}")

    print("\n  Literature-priority claims the guard could not see before:\n")
    for r in lit[:10]:
        print(f"    {r['file']}")
        print(f"      {r['line'][:100]}")

    print(f"""
    THE GUARD WAS SEEING {100*(total-len(newly))//max(total,1)}% OF WHAT IT CLAIMED TO COVER, and the missing half is
    the phrasing this corpus actually uses. That is the finding.

    BUT {len(internal)} OF THE {len(newly)} NEW HITS ARE INTERNAL SEQUENCING, not priority claims. "The
    first objectwise lift of BT1362" and "Q6 is the first super-Ramanujan crossing" order
    this project's own objects; they assert nothing against anyone's literature. Reporting
    them as novelty claims would inflate the guard's yield and train the reader to skim it,
    which is precisely how the rediscovery guard came to be ignored the first time.

    SO THE HONEST NUMBER IS {len(lit)}, not {len(newly)}, and those {len(lit)} are worth reading. Each one
    asserts priority over the field on a token the encyclopedia already contains -- which
    is a collision, not a verdict: the encyclopedia containing "Higgs" says nothing about
    whether a particular chain construction is new.

    THE GUARD SHOULD LEARN THIS SPLIT rather than have it applied downstream by hand. Not
    done here: the INTERNAL pattern above is a first cut written from ten examples, and
    baking a ten-example heuristic into a shared guard is how the "does not appear to be
    new" inversion got in.""")

    out = {
        "boundary": ("collision with the encyclopedia is not evidence a claim is false -- "
                     "the encyclopedia containing a token says nothing about whether a "
                     "specific construction is new. The literature/internal split is a "
                     "heuristic written from ten examples and is applied HERE, not baked "
                     "into the guard, precisely because a ten-example heuristic in a shared "
                     "guard is how the previous inversion got in"),
        "files_scanned": len(files),
        "total_hits": total,
        "visible_before_4802": total - len(newly),
        "newly_visible": len(newly),
        "newly_visible_literature": len(lit),
        "newly_visible_internal": len(internal),
        "coverage_before_pct": round(100 * (total - len(newly)) / max(total, 1), 1),
        "literature_claims": lit,
        "note": ("the guard's earlier clean runs covered less than half the novelty "
                 "assertions in this corpus, because the commonest phrasing was "
                 "unmatchable"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4804_NOVELTY_GUARD_COVERAGE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
