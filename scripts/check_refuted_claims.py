#!/usr/bin/env python3
"""Guard: flag text that restates a claim this repository has already refuted.

The rediscovery guard catches results that already EXIST here. This one catches
the sharper failure: results that already exist here *and were shown to be
false*. A refutation is only worth the pass that produced it if the next document
cannot quietly reassert the claim.

The registry below is deliberately small and hand-maintained. Each entry names
the claim, the pattern that betrays it, the certificate that refutes it, and the
one-line reason. Adding an entry is part of writing a retraction pass.

It WARNS, never blocks -- the same convention as the other guards here, because
a pattern match is a prompt to look, not a verdict. A document may legitimately
quote a refuted claim in order to correct it, which is exactly why the guard
prints the refuting certificate rather than an error.

Usage:  py -3 scripts/check_refuted_claims.py [files...]
        py -3 scripts/check_refuted_claims.py --staged
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# claim -> (regex, refuting certificate, why it is false)
REGISTRY = [
    (
        "Phi_4(3) determines the 3-primary coalescence rank",
        re.compile(r"(not a coincidence|canonical 3-adic depth|double confirmation)",
                   re.I),
        "data/w33_pass1004_cross_track_verification.json",
        "T(8) collides mod 3 exactly as W(3,3) does, so Phi_4(3) = 10 identically, "
        "yet its rank is 7 and k-r is 8. Same prime, different rank: the "
        "cyclotomic value cannot determine the rank. Use "
        "rank_{F_p}((A-kI)(A-rI)), a classical SRG p-rank.",
    ),
    (
        "deformation-Burnside bridge (gluing rank = antipodal pair count)",
        re.compile(r"deformation[- ]burnside|gluing rank\s*=\s*\(q\^?2\s*-\s*1\)/2",
                   re.I),
        "data/w33_pass808_flatblock_gluing_correction.json",
        "the flat-block gluing is (Z/2)^{(q-1)^2/2}, and (q-1)^2/2 never equals "
        "(q^2-1)/2. The apparent match came from gluing unsaturated images with a "
        "faulty Smith routine.",
    ),
    (
        "CKM angles derived parameter-free from W(3,3)",
        re.compile(r"parameter[- ]free.{0,40}CKM|CKM.{0,40}zero fitting", re.I),
        "data/w33_pass981_arxiv_batch_intake_audit.json",
        "in experimental sigma five of six quantities are excluded (theta_12 by "
        "28.8, theta_13 by 62.9); and the source derives theta_12 four times and "
        "reports the closest, which is fitting.",
    ),
    (
        "A5 splits the 240 edges into four orbits of 60",
        re.compile(r"four orbits of 60|4\s*(?:x|orbits of)\s*60", re.I),
        "data/w33_pass982_a5_edge_orbits_refutation.json",
        "17 verified A5 subgroups all give (60,60,30,30,20,20,10,10). "
        "240 = 4*60 satisfies orbit counting, but divisibility is not freeness.",
    ),
    (
        "[W(E8):Sp(4,3)] = 480",
        re.compile(r"\[?W\(E_?8\)\s*:\s*Sp\(4,\s*3\)\]?\s*=\s*480|index\D{0,20}480", re.I),
        "data/w33_pass981_arxiv_batch_intake_audit.json",
        "the index is 696729600/51840 = 13440. The real coincidence is "
        "|W(E6)| = 51840 = |Sp(4,3)| -- E6, not E8.",
    ),
    (
        "five orthogonal E8 sublattices inside Leech",
        re.compile(r"5\s*(?:x|orthogonal).{0,30}E_?8|40\s*=\s*5\s*[x*]\s*8", re.I),
        "data/w33_pass981_arxiv_batch_intake_audit.json",
        "five orthogonal rank-8 sublattices span rank 40 > 24 = rank(Leech). "
        "The standard fact is E8^3.",
    ),
    (
        "PDG closed forms that do not evaluate to their stated value",
        re.compile(r"(1/\(q\^?-5\)|12/q!|k\^?2 \+ \(k-1\)\^?2)", re.I),
        "data/w33_pass1008_constant_table_audit.json",
        "these closed forms do not evaluate to the values printed beside them: "
        "q^5 = 243 not 125, 12/q! = 2 not 67, v_EW*sqrt((1-3/13)/2) = 152.56 not "
        "80.44, k^2+(k-1)^2+lambda = 267 not 137. Re-derive before quoting.",
    ),
]


def scan(path: Path):
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []
    out = []
    for claim, pat, cert, why in REGISTRY:
        m = pat.search(text)
        if m:
            line = text[:m.start()].count("\n") + 1
            out.append((path.name, line, claim, cert, why, m.group(0)[:60]))
    return out


def _staged():
    try:
        res = subprocess.run(["git", "diff", "--cached", "--name-only",
                              "--diff-filter=ACM"], cwd=ROOT,
                             capture_output=True, text=True, timeout=120).stdout
    except Exception:
        return []
    return [ROOT / ln for ln in res.splitlines()
            if ln.endswith((".md", ".py", ".tex"))]


def main(argv):
    args = [a for a in argv[1:] if a != "--staged"]
    targets = _staged() if "--staged" in argv[1:] else [Path(a) for a in args]
    findings = []
    for p in targets:
        if p.exists() and p.is_file():
            findings.extend(scan(p))
    print(f"[refuted-claims] files scanned: {len(targets)}; "
          f"matches: {len(findings)}")
    for name, line, claim, cert, why, snippet in findings:
        print(f"  {name}:{line}  matched {snippet!r}")
        print(f"    claim   : {claim}")
        print(f"    refuted : {cert}")
        print(f"    reason  : {why}")
    if findings:
        print()
        print("  These phrases match claims this repository has already refuted.")
        print("  If the document is correcting the claim, ignore this. If it is")
        print("  asserting it, read the certificate before publishing.")
    return 0  # advisory


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
