#!/usr/bin/env python3
"""Pass 4841 -- I read the sixteen literature-priority collisions. None of them is one.

Pass 4804 ran the corrected novelty guard over 1,705 analysis files, found 47 novelty
claims colliding with the encyclopedia, split them into "internal sequencing" and
"literature priority" with a ten-example heuristic, and reported 16 of the latter as worth
reading.  It then said so four more times without reading them.

Reading them takes ten minutes.  All sixteen are internal.

    1  "For the first time, the substrate is being treated as a DYNAMICAL ..."
    2  "the first time the W(3,3) substrate has been studied as a DYNAMICAL system
        rather than as a static counting object"          <- this project studied it
                                                             statically before; internal
    4  "the first bona fide finite CSS matrix code IN THE K12/F12 CHAIN"
    6  "the first structural explanation IN THIS PACKET"
    8  "the first fair same-degree tournament IN THE PACKET"
   12  "is the first FILE to assert the full parameter string. Four minutes apart"
   14  "the first q=5 pair IN THE PROGRAMME"

Several say so in the sentence.  The rest mean it: "the first exact local CSS layer", "the
first dimensionful anchor", "the first route to a decision" all order this project's own
results.  Not one asserts priority over anybody's literature.

WHAT THAT MEANS FOR THE GUARD.  Over the whole corpus, the explicit-novelty detector finds
ZERO explicit priority assertions.  Its 47 hits are 47 non-instances of the thing it exists
to catch, and my "16 worth reading" was a heuristic that had not been checked against the
text it was summarising.

WHAT IT MEANS FOR THE CORPUS, which is the better half.  This repository does not claim
priority in sentences.  CLAUDE.md already says the dangerous form is implicit framing --
"four of the six failures were implicit framing, which no regex sees" -- and the reading
turns that from a caveat into the whole story: there is no explicit half to catch.

    py -3 analysis/w33_pass4841_i_read_the_sixteen_and_none_is_a_priority_claim.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# read one by one; the verdict column is a judgement, the evidence column is the text
READING = [
    ("2026-05-31_BREAKTHROUGH_CHAIN_summary", "internal", "first time THIS work treats it dynamically"),
    ("2026-05-31_substrate_quantum_signature", "internal", "'rather than as a static counting object' -- prior state is this project's"),
    ("BT1056_chain_native_Q_operator", "internal", "'first concrete W33 chain' -- the chain is ours"),
    ("BT1872_BT1874_summary", "internal", "'IN THE K12/F12 CHAIN'"),
    ("BT1872_dual_face_Z_checks", "internal", "'first exact local CSS layer' -- layer of our construction"),
    ("BT3670_BT3686 (explanation)", "internal", "'IN THIS PACKET'"),
    ("BT3670_BT3686 (glue closure)", "internal", "'of the projector lattice' -- ours"),
    ("BT3715_BT3721", "internal", "'IN THE PACKET'"),
    ("BT4169_BT4176", "internal", "'N=29 is the first below 5 percent' -- mesh ordering"),
    ("BT781_cube_tomotope_48_split", "internal", "'we compared against published generators for the first time'"),
    ("BT867_cache_split_transport", "internal", "'of the holonet's control plane' -- ours"),
    ("CANON_240_81_3", "internal", "'the first FILE to assert' -- repo file ordering, 'four minutes apart'"),
    ("PASS4495_4502_RESERVATION", "internal", "'u^5 is the first coefficient' -- series index"),
    ("PASS456_Q5_COLLISION_ANATOMY", "internal", "'IN THE PROGRAMME'"),
    ("w33_pass1928_1933", "internal", "'first dimensionful anchor' -- in our sequence"),
    ("w33_pass2496_2501", "internal", "'first route to a decision' -- our attempts"),
]


def main() -> int:
    print("=" * 78)
    print("Pass 4841 -- reading the sixteen")
    print("=" * 78)

    print(f"\n  {'file':44s} {'verdict':>9s}  why")
    for f, v, why in READING:
        print(f"  {f[:44]:44s} {v:>9s}  {why[:60]}")

    lit = [r for r in READING if r[1] == "literature"]
    internal = [r for r in READING if r[1] == "internal"]
    print(f"\n    literature-priority claims : {len(lit)}")
    print(f"    internal sequencing        : {len(internal)}")

    prev = ROOT / "data" / "PART_W33_PASS4804_NOVELTY_GUARD_COVERAGE.json"
    total = json.loads(prev.read_text(encoding="utf-8"))["total_hits"] if prev.exists() else 47

    print(f"""
    {len(lit)} OF {len(READING)}. Pass 4804 called these "the honest number" after splitting 26 newly
    visible hits with a ten-example heuristic; reading them says the honest number is {len(lit)}.

    THE HEURISTIC WAS KEYED TO THE WRONG MARKER. It looked for repo-object names -- BT####,
    Pass NNNN, Q6 -- and treated their absence as evidence of a literature claim. But this
    corpus marks internal scope with PHRASES: "in the packet", "in the chain", "in the
    programme", "in this work". Those carry exactly the same meaning and none of the
    tokens.

    SO THE GUARD FINDS NO EXPLICIT PRIORITY ASSERTIONS IN {total} HITS ACROSS 1,705 FILES.
    That is a result about the corpus, not only about the guard: this repository does not
    claim priority in sentences. Every "first" in it orders its own work.

    WHICH CONFIRMS CLAUDE.md'S OWN CAVEAT AND PROMOTES IT. The file already notes that four
    of the six rediscoveries that motivated this guard were implicit framing, "which no
    regex sees". The reading turns that from a limitation into the whole picture: there is
    no explicit half. A guard for explicit novelty assertions is guarding a door this
    corpus does not use.

    I AM NOT PROPOSING TO DELETE IT. Absence of explicit claims today is not a guarantee
    about tomorrow, the guard is cheap, and a corpus that starts making priority claims is
    exactly when one would want it. But its yield should be recorded as zero rather than
    quoted as 47 or 16, and the rediscovery risk here lives somewhere no regex reaches.""")

    out = {
        "boundary": ("the verdict column is a JUDGEMENT made by reading each sentence and "
                     "its surrounding paragraph; another reader could disagree on one or "
                     "two. What is not a judgement is that seven of the sixteen state their "
                     "internal scope explicitly -- 'in the packet', 'in the programme', "
                     "'the first FILE' -- and those are quoted"),
        "read": [{"file": f, "verdict": v, "why": w} for f, v, w in READING],
        "literature_priority_claims": len(lit),
        "internal_sequencing": len(internal),
        "pass_4804_estimate": 16,
        "corrects": ("Pass 4804's heuristic keyed on repo-object tokens (BT####, Pass NNNN) "
                     "and missed that this corpus marks internal scope with phrases -- 'in "
                     "the packet', 'in the chain', 'in the programme' -- which carry the "
                     "same meaning and none of the tokens"),
        "conclusion": ("the explicit-novelty guard finds zero explicit priority assertions "
                       "across 1,705 files; this corpus does not claim priority in "
                       "sentences, and the rediscovery risk is entirely implicit framing, "
                       "which CLAUDE.md already names as the half no regex sees"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4841_READING_THE_SIXTEEN.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
