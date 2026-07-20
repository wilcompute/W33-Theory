#!/usr/bin/env python3
"""Guard: causal claims in certificates must be marked derived or unverified.

Twice in one session this programme wrote a causal explanation that merely
fitted the data and was later retracted:

  * Passes 506/507 said the factorial law's m! "is what Newton's identities
    divide by".  Unsound -- Newton computes e_k FROM the power sums, and the
    p_m are primary traces with no division, so no factorial can enter that
    way.  Retracted in Pass 508.
  * Pass 487 explained the failure region by "Newton's identity divides by k,
    and that costs more over Z[zeta_9]".  Contradicted by Pass 508: the
    failure deviates BELOW the factorial law, i.e. MORE cancellation, which is
    the opposite sign.

Both were caught late, after the claim had propagated into the papers.  This
guard makes the check routine: any certificate string that asserts a mechanism
must either cite a proof or be explicitly tagged as a candidate.

It WARNS, never blocks -- an unmarked causal sentence is a prompt to look, not
a verdict.  (Blocking trains --no-verify; see the rediscovery guard.)

Usage:  py -3 scripts/check_mechanism_claims.py [files...]
        (default: every data/w33_pass*.json)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# language that asserts a cause rather than reporting a measurement
CAUSAL = re.compile(
    r"\b(because|mechanism|the reason|explains?|explanation|signature of|"
    r"driven by|arises? from|accounts? for|is due to|comes? from)\b",
    re.I,
)

# language that marks a claim as proved, or as an acknowledged guess
HEDGED = re.compile(
    r"\b(proof|proved|proven|QED|theorem|candidate|conjectur|unverified|"
    r"not proved|unproven|not identified|we do not know|suspect|"
    r"retract|hypothes|measured, not|observation, not)\b",
    re.I,
)


# Keys whose values are QUOTATIONS from elsewhere in the corpus, not claims
# the certificate is making.  Pass 512's triage report quotes the very claims
# this guard flags, so without this the guard re-flags its own worklist and
# reports 41 findings that are all one finding.  A quotation is not an
# assertion.
QUOTED_KEYS = re.compile(r"(^|\.)(sample|samples|quote|quoted|excerpt)s?(\[|$)")


def scan(path: Path):
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # a malformed certificate is its own problem
        return [(path.name, "<unreadable>", f"{type(exc).__name__}: {exc}")]
    flagged = []

    def walk(node, key_path):
        if isinstance(node, str):
            if QUOTED_KEYS.search(key_path):
                return
            if CAUSAL.search(node) and not HEDGED.search(node):
                flagged.append((path.name, key_path, node[:200]))
        elif isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{key_path}.{k}" if key_path else k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{key_path}[{i}]")

    walk(doc, "")
    return flagged


def main(argv):
    targets = ([Path(a) for a in argv[1:]] if len(argv) > 1
               else sorted((ROOT / "data").glob("w33_pass*.json")))
    flagged = []
    for p in targets:
        if p.exists():
            flagged.extend(scan(p))
    print(f"[mechanism-claims] certificates scanned: {len(targets)}; "
          f"unmarked causal claims: {len(flagged)}")
    # The Windows console is cp1252; certificate text routinely carries Greek
    # and subscripts, and an UnprintableError here would kill an ADVISORY
    # guard.  Degrade the characters, never the check.
    def safe(s):
        return s.encode("ascii", "backslashreplace").decode("ascii")

    for name, key, text in flagged:
        print(f"  {safe(name)} [{safe(key)}]")
        print(f"    {safe(text)}")
    if flagged:
        print()
        print("  These assert a CAUSE.  Each should either cite a proof, or")
        print("  say plainly that it is a candidate/unverified.  A claim that")
        print("  merely fits the data is an observation, not a mechanism --")
        print("  Passes 487 and 506/507 both had to be retracted for exactly")
        print("  this, after the wording had reached the papers.")
    return 0  # advisory only


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
