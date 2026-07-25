#!/usr/bin/env python3
"""Guard: comparisons to measured quantities must be reported in experimental sigma.

Pass 981 audited an arXiv-bound batch whose CKM section reported agreements as
percentages -- "10%", "11%", "34%", "order-correct" -- and concluded the
predictions were successful.  In experimental standard deviations, the unit that
matters when a quantity is measured to parts in 10^4, five of the six were
excluded: theta_12 by 28.8 sigma, theta_13 by 62.9, lambda_W by 35.7.  A 29-sigma
exclusion had been presented as "11% agreement" and scheduled for PRL.

Percent error and sigma error diverge exactly when the measurement is precise,
which is when the claim matters most.  This guard makes the omission visible.

It flags a file when BOTH of the following hold:

  * it compares to experiment -- it mentions PDG, "experimental", "measured",
    or a known observable name; and
  * it quotes an agreement as a percentage or a ratio, and nowhere reports a
    discrepancy in sigma (no "sigma", no unicode sigma, no "standard deviation").

It also carries a small table of precisely-measured constants; if a file states a
numeric prediction for one of them, the guard computes the sigma itself and
reports it, so the number appears even if the author never computed it.

It WARNS, never blocks -- consistent with the other guards in this repository.

Usage:  py -3 scripts/check_sigma_gate.py [files...]
        py -3 scripts/check_sigma_gate.py --staged
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# name -> (central, error, unit).  Only quantities measured precisely enough that
# percent and sigma differ materially.
MEASURED = {
    "theta_12": (13.04, 0.05, "deg"),
    "theta_13": (0.201, 0.011, "deg"),
    "theta_23": (2.38, 0.06, "deg"),
    "delta_cp": (65.5, 3.3, "deg"),
    "lambda_w": (0.2250, 0.0007, ""),
    "cabibbo": (13.04, 0.05, "deg"),
    "alpha_inverse": (137.035999, 0.000001, ""),
    "sin2_theta_w": (0.23122, 0.00004, ""),
}

COMPARES = re.compile(
    r"\b(PDG|experimental(?:ly)?|measured|observed value|world average|"
    r"CODATA|particle data group)\b", re.I)
PERCENTY = re.compile(
    r"(\d+(?:\.\d+)?\s*%|\bpercent\b|\bagreement\b|\bratio\b|\border[- ]correct\b|"
    r"\bwithin\s+\d+(?:\.\d+)?\s*%)", re.I)
SIGMAISH = re.compile(
    r"(sigma|σ|standard deviation|std\.? dev|s\.d\.)", re.I)

NUMBER = r"[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"


def scan_text(name, text):
    findings = []
    compares = bool(COMPARES.search(text))
    percenty = bool(PERCENTY.search(text))
    sigmaish = bool(SIGMAISH.search(text))
    if compares and percenty and not sigmaish:
        findings.append((name, "no-sigma",
                         "compares to experiment and quotes percent/agreement "
                         "but never reports a discrepancy in sigma"))
    # opportunistic: compute sigma for any stated prediction of a known constant
    low = text.lower()
    for key, (central, err, unit) in MEASURED.items():
        probe = key.replace("_", r"[_ θδ]*")
        for mt in re.finditer(probe + r"[^\n]{0,80}?(" + NUMBER + r")", low):
            try:
                val = float(mt.group(1))
            except ValueError:
                continue
            if val == 0 or abs(val - central) < 1e-12:
                continue
            # ignore matches that are just restating the measured value
            if abs(val - central) <= err:
                continue
            sig = abs(val - central) / err
            if sig >= 5:
                findings.append(
                    (name, "excluded",
                     f"{key}: stated {val}{unit} vs measured {central}+-{err}"
                     f"{unit} = {sig:.1f} sigma (EXCLUDED)"))
            break
    return findings


def _staged():
    try:
        out = subprocess.run(["git", "diff", "--cached", "--name-only",
                              "--diff-filter=ACM"], cwd=ROOT,
                             capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return []
    return [ROOT / ln for ln in out.splitlines()
            if ln.endswith((".md", ".py", ".tex", ".json"))]


def main(argv):
    args = [a for a in argv[1:] if a != "--staged"]
    targets = _staged() if "--staged" in argv[1:] else [Path(a) for a in args]
    findings = []
    for p in targets:
        if not p.exists() or p.is_dir():
            continue
        try:
            findings.extend(scan_text(p.name,
                                      p.read_text(encoding="utf-8",
                                                  errors="ignore")))
        except Exception:
            continue
    print(f"[sigma-gate] files scanned: {len(targets)}; findings: {len(findings)}")
    for name, kind, msg in findings:
        print(f"  {name} [{kind}]")
        print(f"    {msg}")
    if findings:
        print()
        print("  Percent agreement and sigma agreement diverge exactly when the")
        print("  measurement is precise.  Pass 981 found a 28.8-sigma exclusion")
        print("  presented as '11% agreement' and scheduled for PRL.  State the")
        print("  discrepancy in experimental sigma before claiming agreement.")
    return 0  # advisory


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
