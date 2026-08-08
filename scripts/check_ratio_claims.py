#!/usr/bin/env python3
"""Pass 4351 -- every "N times" claim needs a null model, and one of mine had none.

Pass 4343 found I had compared additive gate counts against a MULTIPLICATIVE baseline:
D/A = 2.33 against (B/A) x (C/A) = 2.56, reported as evidence the two fixes "share logic".
Costs add. The right baseline was B + C - A = 235 against a measured 240, which says the
opposite -- the fixes are independent to within measurement noise.

The failure shape is general and cheap to look for: a ratio quoted as evidence, with no
statement of what it would have been under the null hypothesis. This sweeps the manuscripts
for ratio language and separates the ones that name a baseline from the ones that do not.

It is a TRIAGE LIST. A ratio without a stated baseline is not automatically wrong -- often
the baseline is obvious from context -- but it is the shape the error takes, and this
project has now produced one.

    py -3 scripts/check_ratio_claims.py
    py -3 scripts/check_ratio_claims.py --strict   # exit 1 if any lack a baseline
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# A ratio being asserted, not merely a number that happens to divide.
#
# CALIBRATION.  The first version required the noun to follow the ratio immediately and
# reported ZERO across every manuscript -- while the blueprint contains
# "costs $2.00\times$ the cells" three lines from where this was written.  In LaTeX the
# ratio is wrapped in math delimiters and often trailed by punctuation, so the pattern has
# to step over $, }, ~ and a few words before the noun appears.
RATIO = re.compile(
    r"(\d+(?:\.\d+)?)\s*(?:\\times|\\cdot|[x×]\b|-fold)"
    r"[\s$}~,.;:]*(?:the\s+|its\s+|of\s+)*"
    r"(cells?|cost\w*|area|gates?|wires?|time|slower|faster|larger|smaller|"
    r"more|less|decode\w*|logic|power)",
    re.I)
# Words that indicate the writer said what the comparison is AGAINST.
BASELINE = ("baseline", "against", "compared with", "relative to", "versus", " vs ",
            "null model", "would have been", "if the", "predicted", "expected",
            "than the", "over the")


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    targets = sorted(ROOT.glob("*.tex"))
    bare, withb = [], 0
    for f in targets:
        lines = f.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines):
            for m in RATIO.finditer(ln):
                window = " ".join(lines[max(0, i - 3):i + 4]).lower()
                if any(b in window for b in BASELINE):
                    withb += 1
                else:
                    bare.append((f.name, i + 1, m.group(0), ln.strip()[:62]))
    print(f"  ratio claims found          : {withb + len(bare)}")
    print(f"  with a stated baseline      : {withb}")
    print(f"  WITHOUT a stated baseline   : {len(bare)}")
    if bare:
        print(f"\n  {'file':34s} {'line':>6s}  claim")
        for f, ln, hit, ctx in bare[:25]:
            print(f"  {f[:34]:34s} {ln:6d}  {hit}")
            print(f"  {'':34s} {'':6s}  {ctx}")
    print(f"""
  A ratio is a comparison, and a comparison needs a second term.  The specific error this
  check exists for: quoting {2.33:.2f}x against {2.56:.2f}x, where the second number came from
  MULTIPLYING two ratios that describe an ADDITIVE quantity.  Gate counts, cell counts,
  areas and times all add; their ratios do not compose.  The correct null model for two
  independent changes to an additive quantity is inclusion-exclusion, not a product.

  Triage, not verdict: many of the entries above will have an obvious baseline in the
  surrounding paragraph that this keyword scan cannot see.  The value is that a ratio with
  NO baseline anywhere nearby is exactly where the mistake hides.""")
    return 1 if (strict and bare) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
