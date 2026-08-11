#!/usr/bin/env python3
"""Pass 4810 -- how much of this session was correcting this session?

I have twice told the user a ratio from memory -- "three of my last five passes corrected
an earlier pass of mine" -- which is exactly the habit that produced the errors being
corrected.  The number is computable from git.

WHAT IS BEING MEASURED, precisely, because "self-correction" is vague enough to produce any
answer you like.  A commit counts as a self-correction if its message asserts that an
EARLIER claim of this lane is wrong: refuted, false, retracted, withdrawn, "was wrong",
"did not hold", "could not have failed".  A commit that merely fixes a bug in a script does
NOT count -- fixing a typo in a regex is maintenance; withdrawing a published claim is a
correction.

The distinction matters because the two have different implications. A high bug rate means
the code is being written fast. A high retraction rate means the CLAIMS are being written
ahead of the evidence, and that is the thing worth knowing.

    py -3 analysis/w33_pass4810_the_self_correction_census.py
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# A CLAIM being withdrawn, not a bug being fixed.
RETRACT = re.compile(
    r"\brefut(?:e|ed|es|ation)\b|\bis FALSE\b|\bwas wrong\b|\bwere wrong\b|"
    r"\bretract(?:ed|ion)?\b|\bwithdraw(?:n|s)?\b|\bdid not hold\b|"
    r"\bcould not have failed\b|\bnever propagated\b|\bwas a coincidence\b|"
    r"\bprediction (?:failed|falsified)\b|\bthere were no\b|\bI had been wrong\b",
    re.I)
# a bug in a tool, not a claim
BUGFIX = re.compile(
    r"\bfix(?:ed|es)?\b|\bbug\b|\bbroke(?:n)?\b|\btypo\b|\bcrash\b|\bencoding\b|"
    r"\bfalse positive\b|\bunmatchable\b|\bself-test\b", re.I)


def main() -> int:
    print("=" * 78)
    print("Pass 4810 -- census of this session's self-corrections")
    print("=" * 78)

    r = subprocess.run(
        ["git", "log", "--author=Wil", "--since=2026-08-10 09:00",
         "--format=%h%x00%s%x00%b%x01"],
        cwd=ROOT, capture_output=True, text=True, timeout=300)
    commits = [c for c in r.stdout.split("\x01") if c.strip()]
    rows = []
    for c in commits:
        parts = c.strip().split("\x00")
        if len(parts) < 2:
            continue
        sha, subject = parts[0], parts[1]
        body = parts[2] if len(parts) > 2 else ""
        full = subject + "\n" + body
        if subject.lower().startswith(("passes ", "pass ")) and "reserved" in subject:
            kind = "reservation"
        elif RETRACT.search(full):
            kind = "self-correction"
        elif BUGFIX.search(full):
            kind = "bugfix"
        else:
            kind = "result"
        rows.append({"sha": sha, "kind": kind, "subject": subject[:88]})

    kinds = {}
    for x in rows:
        kinds[x["kind"]] = kinds.get(x["kind"], 0) + 1
    substantive = [x for x in rows if x["kind"] != "reservation"]
    corr = [x for x in rows if x["kind"] == "self-correction"]

    print(f"\n  commits in window            : {len(rows)}")
    for k in ("reservation", "result", "bugfix", "self-correction"):
        print(f"    {k:18s} {kinds.get(k, 0):4d}")
    pct = 100 * len(corr) / max(len(substantive), 1)
    print(f"\n  substantive commits          : {len(substantive)}")
    print(f"  of those, self-corrections   : {len(corr)}  ({pct:.0f}%)")

    print("\n  The self-corrections:\n")
    for x in corr:
        print(f"    {x['sha']}  {x['subject']}")

    print(f"""
    {pct:.0f}% OF SUBSTANTIVE COMMITS CONTAIN A WITHDRAWAL. That is not the same as {pct:.0f}% BEING
    withdrawals, and the difference matters. Reading the list: "W(3,q) over any prime power
    and self-duality settled at q=4 and q=5" is a RESULT whose body also records that the
    first version of its isomorphism test was wrong. "Duality does not preserve having an
    ovoid" is a result whose body records a KeyError. The classifier keys on the message,
    and most of these messages carry both a finding and a correction.

    So the honest reading is: {len(corr)} commits withdrew something, almost all of them while also
    delivering something. A count of commits that were ONLY corrections would be much
    smaller, and a count of CLAIMS withdrawn is the number I actually care about and have
    not computed -- several of these commits withdrew two.

    I have twice quoted this ratio from memory as "three of five", which is both wrong and
    the exact habit that produced the claims being withdrawn.

    WHAT THE NUMBER DOES AND DOES NOT SAY. It does not say the session went badly: every one
    of these was caught by a computation the original pass had itself named as missing, and
    the alternative to a high correction rate is not a low one -- it is the same claims
    standing uncorrected. Pass 4761 found a retraction that had sat unpropagated for two
    hundred passes; that is what the corpus looks like when the rate is zero.

    It does say the claims were being written a step ahead of the evidence, consistently.
    The pattern in every case was the same: state the result, name the check that would
    falsify it, publish, then run the check. Running it first costs nothing extra -- the
    computation is the same computation -- and would have converted {len(corr)} retractions into
    {len(corr)} results that were right the first time.

    BUGFIXES ARE COUNTED SEPARATELY ON PURPOSE. A wrong regex is maintenance; a withdrawn
    claim is a correction, and conflating them would let a high bug rate hide behind a
    respectable-sounding total, or the reverse.""")

    out = {
        "boundary": ("classification is by commit-message keywords over commits in this "
                     "session's window, so it measures what the messages SAY. A silent "
                     "correction -- a claim quietly edited without a commit saying so -- is "
                     "invisible to this, and would be the more worrying kind. The bugfix/"
                     "self-correction split is a judgement encoded as two keyword sets"),
        "commits": len(rows),
        "by_kind": kinds,
        "substantive": len(substantive),
        "self_corrections": len(corr),
        "self_correction_pct": round(pct, 1),
        "corrections": corr,
        "previously_claimed_from_memory": "three of my last five passes",
        "lesson": ("in every case the falsifying computation was named by the pass that "
                   "made the claim; running it before publishing costs nothing extra"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4810_SELF_CORRECTION_CENSUS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
