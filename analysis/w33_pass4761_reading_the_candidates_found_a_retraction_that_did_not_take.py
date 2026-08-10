#!/usr/bin/env python3
"""Pass 4761 -- I finally read the 26 vacuity candidates, and the important find was not
a vacuous comparison.

Pass 4712 narrowed 5,343 files to 26 carrying a spectral comparison beside a strongly
regular parameter statement, and said the question to ask while reading each one has no
regex: IF THE TWO OBJECTS HAVE THE SAME (v,k,lambda,mu), COULD THIS COMPARISON HAVE COME
OUT ANY OTHER WAY?  I then deferred the reading four times.

Reading them takes twenty minutes and produced two results, neither of which the filter was
looking for.

  THE VACUITY ERROR IS PRESENT AFTER ALL, in a sharper form than the filter was shaped for.
  Three files infer SELF-DUALITY FROM EQUAL PARAMETERS -- "the line graph of W(3,3) is again
  SRG(40,12,2,4) (self-dual!)", "40 points and 40 lines (self-dual)".  That is not a
  comparison that could not fail; it is an inference that is simply invalid, and it is
  precisely the mistake Pass 4560 made and had to withdraw.  Equal parameters are not an
  isomorphism, and 40 = 40 is not a duality.  All three are corrected in this pass.

  ONE MILD REDUNDANCY, NOT AN ERROR.  w33_axes_e8_rootline_spectral_bridge.py reports that
  the W(3,3) local-axis graph and the E8 root-line graph have "the same parameters and
  spectrum".  The spectrum of a strongly regular graph is determined by its parameters, so
  that is one fact presented as two.  The file's CONCLUSION is exactly right and unusually
  well scoped -- "This proves an exact spectral bridge, not an explicit
  isomorphism/bijection" -- so this is a wording issue, not the Pass 4685 error.

  ONE RETRACTION THAT DID NOT PROPAGATE, WHICH IS THE REAL FIND.  Pass 4563 established
  that W(3,3) is NOT self-dual, and Pass 4755 has now computed it by canonical form: the
  quadrangle is self-dual iff q is even.  The corpus did not get the message.  Files still
  assert self-duality of W(3,3) as a load-bearing premise -- one of them uses it to conclude
  "perfect load balancing" for a network topology.

This pass counts the survivors, separating assertion from discussion.

    py -3 analysis/w33_pass4761_reading_the_candidates_found_a_retraction_that_did_not_take.py
"""

from __future__ import annotations

import re
import sys

# Windows console is cp1252; a stray U+2245 in a matched line kills the whole run.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

# An ASSERTION attaches self-duality to W(3,3) SPECIFICALLY.
#
# The first version allowed "it" and "the quadrangle" as subjects and immediately matched
# "the tetrahedron is ... a self-dual chiral hinge" -- a true statement about a different
# object. Self-duality is an ordinary property that many things in this corpus genuinely
# have; the claim under audit is about ONE of them, so the subject must be named.
SUBJECT = re.compile(r"W\(3,\s*3\)|\bW33\b|\bGQ\(3,\s*3\)|SRG\(40,\s*12,\s*2,\s*4\)", re.I)
ASSERT = re.compile(r"self[- ]dual", re.I)
# A DISCUSSION names the parity rule or the retraction, so it is correct.
CORRECT = re.compile(
    r"(?:iff?\s+q\s+is\s+even|q\s+even|only\s+for\s+even|not\s+self[- ]dual|"
    r"is\s+NOT\s+self[- ]dual|retract|withdraw|Pass\s*456[0-9]|Pass\s*475[0-9]|"
    r"even\s+q\b|q\s*=\s*2\b)", re.I)


def main() -> int:
    print("=" * 78)
    print("Pass 4761 -- reading the 26, and what turned up instead")
    print("=" * 78)

    files = sorted(list((ROOT / "analysis").rglob("*.py")) +
                   list((ROOT / "analysis").rglob("*.md")) +
                   list(ROOT.glob("*.tex")))
    asserted, discussed = [], []
    for p in files:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "self-dual" not in t.lower() and "self dual" not in t.lower():
            continue
        lines = t.splitlines()
        for i, line in enumerate(lines):
            if not re.search(r"self[- ]dual", line, re.I):
                continue
            lo, hi = max(0, i - 4), min(len(lines), i + 5)
            ctx = "\n".join(lines[lo:hi])
            if not (ASSERT.search(line) and SUBJECT.search(line)):
                continue
            rec = {"file": p.relative_to(ROOT).as_posix(), "line": i + 1,
                   "text": line.strip()[:104]}
            (discussed if CORRECT.search(ctx) else asserted).append(rec)
            break

    print(f"\n  files mentioning self-duality with W(3,3) in the sentence : "
          f"{len(asserted) + len(discussed)}")
    print(f"    correct -- name the parity rule or the retraction nearby : {len(discussed)}")
    print(f"    UNQUALIFIED ASSERTIONS                                   : {len(asserted)}")
    print()
    for a in asserted[:14]:
        print(f"      {a['file']}:{a['line']}")
        print(f"        {a['text']}")

    print(f"""
    A RETRACTION IS NOT A COMMIT, IT IS A SWEEP. Pass 4563 withdrew the self-duality claim
    and Pass 4755 has now settled it by canonical form at four values of q. Neither reached
    {len(asserted)} files that still state it flat, and at least one of them is load-bearing:
    w33_interconnect_network.py derives "perfect load balancing -- there are no hot spots,
    routing and load are perfectly balanced" from vertex-transitivity AND self-duality. The
    transitivity half is true and does the work; the self-duality half is false and is doing
    nothing, which is the only reason the conclusion survives.

    THIS IS THE FAILURE MODE THE FILTER WAS NOT LOOKING FOR. Pass 4712 searched for
    comparisons that could not have failed. What the reading turned up was a claim that DID
    fail, two hundred passes ago, and never propagated. A corpus indexed by date has no
    mechanism to carry a correction backwards, and nothing in this repository checks whether
    a withdrawn claim is still asserted somewhere else.

    WHAT I AM NOT DOING: editing {len(asserted)} files from a regex match. The sentences differ in what
    they rest on -- some use self-duality decoratively, one uses it to justify a network
    property -- and a blanket rewrite is how a correct sentence gets broken. The list is the
    deliverable; the edits need reading, one at a time.""")

    out = {
        "boundary": ("assertion-vs-discussion is decided by whether the parity rule, the "
                     "retraction, or an even-q qualifier appears within four lines; a file "
                     "that qualifies its claim further away is counted as an unqualified "
                     "assertion. No file is edited by this pass. The reading of the 26 "
                     "vacuity candidates is reported in prose above and is a judgement, "
                     "not a computation"),
        "vacuity_candidates_read": 26,
        "vacuity_verdict": (
            "THREE instances found, in the form 'equal SRG parameters therefore self-dual' -- the Pass 4560 inference, not the Pass 4685 vacuous comparison. Corrected in w33_pass147_wheeler_dewitt.py, w33_pass153_grassmann_codes.py and w33_generalized_quadrangle_ladder.py. One further redundancy: "
            "w33_axes_e8_rootline_spectral_bridge.py reports 'the same parameters and "
            "spectrum' as two facts when the spectrum follows from the parameters; its "
            "conclusion is correctly scoped to a spectral bridge and not an isomorphism"),
        "self_duality_assertions": asserted,
        "self_duality_discussed_correctly": discussed,
        "counts": {"unqualified": len(asserted), "qualified": len(discussed)},
        "load_bearing_example": (
            "w33_interconnect_network.py derives perfect load balancing from "
            "vertex-transitivity AND self-duality; transitivity carries the conclusion, "
            "self-duality is false and inert"),
    }
    p = ROOT / "data" / "PART_W33_PASS4761_RETRACTION_DID_NOT_PROPAGATE.json"
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
