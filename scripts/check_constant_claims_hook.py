#!/usr/bin/env python3
"""Pre-commit WARNING (never blocks): staged files that claim "<prediction> (obs: X +- s ..." are run through the fair null of
Passes 12504/12512 -- the experimental tension and the fraction of random 13-integer alphabets (plus the leaf 1) that reach the measured
value within the same window by an expression of at most 3 integer leaves.

    py -3 scripts/check_constant_claims_hook.py <files...>

A claim prints as EXCLUDED (> 3 sigma), NOT EVIDENCE (>= 5% of random alphabets reach it) or RARE.  Exit code is always 0: like
check_rediscovery.py, blocking would train --no-verify; the warning names the audit to read (analysis/PASS12506_12513_QUANTUM_BRIDGES.md
section 12512, scripts/check_constant_claim.py for a single claim).
"""
import bisect
import os
import random
import re
import sys

PAT = re.compile(r"([0-9]+\.?[0-9]*)\s*\(obs:?\s*([0-9]+\.?[0-9]*)\s*(?:±|\+-|\+/-)\s*([0-9]+\.?[0-9]*)")


def main(files):
    claims = []
    for f in files:
        try:
            t = open(f, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        for m in PAT.finditer(t):
            pred, obs, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
            if s > 0 and obs > 0:
                claims.append((f, t.count("\n", 0, m.start()) + 1, pred, obs, s))
    if not claims:
        return 0
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "analysis"))
    from w33_mdl_shortest import build_expressions
    rng = random.Random(1)
    vals = [sorted(build_expressions([1] + sorted(rng.sample(range(2, 41), 13)), max_cost=3).keys()) for _ in range(40)]
    for f, line, pred, obs, s in claims:
        w = max(abs(pred / obs - 1), s / obs)
        hit = sum(1 for v in vals if (lambda i: i < len(v) and v[i] <= obs * (1 + w))(bisect.bisect_left(v, obs * (1 - w))))
        p = hit / len(vals); tension = abs(pred - obs) / s
        verdict = "EXCLUDED" if tension > 3 else "NOT EVIDENCE" if p >= 0.05 else "RARE"
        print(f"constant-claim [{verdict}] {f}:{line}: pred {pred:g} vs obs {obs:g}+-{s:g} ({tension:.2f} sigma), "
              f"random alphabets reaching it: {p:.0%}")
    print("constant-claim: warnings only; see scripts/check_constant_claim.py and Pass 12512")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
