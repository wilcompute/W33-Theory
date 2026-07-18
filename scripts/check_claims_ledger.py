#!/usr/bin/env python3
"""Verify the claims ledger in w33_paper.tex against the witness certificates.

WHY. The paper's claims ledger is prose, and prose rots exactly the way the
STATUS box rotted (it once called the rank law "ours" and det(B_p) "open" while
both were settled). This checker makes the ledger self-verifying: every row
that cites a pass witness must have a data/ certificate on disk whose status
field says PASS. Runs fast (reads JSON; never re-runs witnesses), so it can sit
in CI and pre-commit without cost.

WHAT IT CHECKS.
  * every P<nnn> witness tag in the ledger resolves to >= 1 data/w33_pass*.json
  * each resolved certificate has "status": "PASS"
  * rows marked \textsc{killed} are EXEMPT from the PASS requirement on the
    claim itself (the witness that performed the kill must still PASS)
It does not judge the mathematics -- only that the paper's paper trail exists
and is green.

Usage:  py -3 scripts/check_claims_ledger.py        (exit 1 on any failure)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "w33_paper.tex"
DATA = ROOT / "data"


def main() -> int:
    tex = PAPER.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"\\paragraph\{Claims ledger\.\}(.*?)\\end\{tabular\}",
                  tex, re.S)
    if not m:
        print("[claims-ledger] no ledger found in w33_paper.tex")
        return 1
    block = m.group(1)
    rows = [ln for ln in block.splitlines() if "&" in ln and "P3" in ln
            or ("&" in ln and re.search(r"P\d{3}", ln))]
    failures, checked = [], 0
    for ln in rows:
        tags = re.findall(r"P(\d{3})", ln)
        if not tags:
            continue
        for tag in tags:
            hits = sorted(DATA.glob(f"w33_pass{tag}_*.json"))
            # Release-engineering artifacts (attestations, transport manifests)
            # carry pipeline-state vocabularies (e.g. READY_FOR_PR_VALIDATION),
            # not witness PASS/FAIL. Pass 430 found the third stream's
            # w33_pass399_release_attestation.json correctly reddening the
            # ledger through no fault of the mathematics. Witness certificates
            # only:
            hits = [h for h in hits if "attestation" not in h.name
                    and "release_manifest" not in h.name]
            if not hits:
                failures.append(f"P{tag}: no certificate data/w33_pass{tag}_*.json")
                continue
            for h in hits:
                try:
                    status = json.loads(h.read_text(encoding="utf-8")).get("status")
                except Exception as e:
                    failures.append(f"P{tag}: {h.name} unreadable ({e})")
                    continue
                checked += 1
                if status != "PASS":
                    failures.append(f"P{tag}: {h.name} status={status!r}")
    print(f"[claims-ledger] rows scanned: {len(rows)}; certificates checked: "
          f"{checked}; failures: {len(failures)}")
    for f in failures:
        print(f"  FAIL {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
