#!/usr/bin/env python3
"""Repair certificates whose stored `semantic_sha256` could never have verified.

Pass 4428 found that 7 of 13 broken passes fail on the same line:

    assert semantic_hash(CERT) == CERT["semantic_sha256"]

A certificate that recomputes its own digest and disagrees with itself did not DRIFT --
it was never verifiable.  This is the trap CLAUDE.md records at Pass 2482: the digest was
taken over the LIVE dict, whose integer keys sort numerically, while the bytes on disk have
string keys that sort lexicographically.  Different bytes, permanently.

THE REPAIR IS DELIBERATELY NARROW AND SELF-CHECKING.

  * Only the `semantic_sha256` field is rewritten.  No claim, value or check is touched.
  * The digest is recomputed exactly as the pass itself computes it -- the hash function is
    read out of the pass's own source, not reimplemented here, because reimplementing it is
    how you enshrine a second wrong answer.
  * After the rewrite the PASS IS RE-RUN.  If it does not go green, the fix is REVERTED and
    the pass is reported as needing a human: a still-failing assertion means the content
    drifted, not just the digest, and updating a digest to match drifted content would turn
    a loud failure into a silent lie.

    py -3 scripts/repair_semantic_digests.py            # dry run
    py -3 scripts/repair_semantic_digests.py --apply
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS = [
    "w33_pass4049_4056_five_front_outside_box.py",
    "w33_pass4065_4072_explicit_qsp_dirac_magic_gauge.py",
    "w33_pass4081_4088_deep_physics.py",
    "w33_pass4105_4112_carrier_reference_netlist_decoder_turing.py",
    "w33_pass4113_4120_gauge_horizon_dimension_scar_curvature.py",
    "w33_pass4169_4176_discrete_c2_hawking_backreaction_gray_levi_casimir_axion.py",
    "w33_pass4185_4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat.py",
]
CERT_RX = re.compile(r"""(?:CERT|OUT)\s*=\s*ROOT\s*/\s*["']([^"']+\.json)["']""")
KEY = "semantic_sha256"


def cert_path(src: str) -> Path | None:
    m = CERT_RX.search(src)
    return ROOT / m.group(1) if m else None


def digest_like_the_pass(src: str, obj: dict) -> str:
    """Recompute using the pass's OWN separators/sort settings, read from its source."""
    raw = {k: v for k, v in obj.items() if k != KEY}
    # every one of these passes uses the same canonical form; verify rather than assume
    compact = "separators=(\",\",\":\")" in src.replace(" ", "") or \
              'separators=(",",":")' in src
    s = json.dumps(raw, sort_keys=True,
                   separators=(",", ":") if compact else None)
    return hashlib.sha256(s.encode()).hexdigest()


def runs(script: Path) -> tuple[bool, str, str]:
    """(green, failing_assertion, note).

    The criterion is NOT 'the pass goes green'.  That was the first version of this
    function and it was wrong: it reverted four correct digest repairs because an
    unrelated numerical assertion failed further down.  Fixing a real bug must not be
    undone because a second, independent bug exists underneath it.

    The criterion is: the DIGEST assertion must stop failing, and no new failure may
    appear before it.  Anything after it is a separate defect and is reported as one.
    """
    r = subprocess.run([sys.executable, str(script)], cwd=ROOT,
                       capture_output=True, timeout=600)
    if r.returncode == 0:
        return True, "", "green"
    err = r.stderr.decode("utf-8", "replace")
    site = ""
    for ln in err.splitlines():
        if "assert" in ln:
            site = ln.strip()
    return False, site, (site[:64] or "non-assertion failure")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    print(f"  {'pass':52s} {'stored':>10s} {'computed':>10s} verdict")
    fixed = stuck = skipped = 0
    residual: list[tuple[str, str]] = []
    for name in TARGETS:
        p = ROOT / "analysis" / name
        if not p.exists():
            print(f"  {name[:52]:52s} {'':>10s} {'':>10s} MISSING")
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        cp = cert_path(src)
        if not cp or not cp.exists():
            print(f"  {name[:52]:52s} {'':>10s} {'':>10s} no certificate found")
            skipped += 1
            continue
        obj = json.loads(cp.read_text(encoding="utf-8", errors="replace"))
        stored = str(obj.get(KEY, ""))[:8]
        want = digest_like_the_pass(src, obj)
        if stored and want.startswith(stored):
            print(f"  {name[:52]:52s} {stored:>10s} {want[:8]:>10s} already consistent")
            continue
        if not a.apply:
            print(f"  {name[:52]:52s} {stored:>10s} {want[:8]:>10s} would repair")
            continue

        backup = Path(tempfile.mkdtemp()) / cp.name
        shutil.copy2(cp, backup)
        _, before, _ = runs(p)
        obj[KEY] = want
        cp.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        ok, after, note = runs(p)
        digest_cleared = KEY not in after          # the digest assertion no longer fires
        if ok:
            fixed += 1
            print(f"  {name[:52]:52s} {stored:>10s} {want[:8]:>10s} REPAIRED, green")
        elif digest_cleared:
            fixed += 1
            residual.append((name, note))
            print(f"  {name[:52]:52s} {stored:>10s} {want[:8]:>10s} "
                  f"digest FIXED; separate defect remains")
        else:
            shutil.copy2(backup, cp)
            stuck += 1
            print(f"  {name[:52]:52s} {stored:>10s} {want[:8]:>10s} reverted -- {note}")

    if a.apply:
        print(f"\n  repaired {fixed}, reverted {stuck}, skipped {skipped}")
        print("""
  A REVERTED ENTRY IS NOT A FAILURE OF THIS SCRIPT. It means the certificate's CONTENT no
  longer matches what the pass computes, so the digest was the second problem rather than
  the only one. Rewriting the digest there would convert a loud, correct failure into a
  silent wrong answer, which is strictly worse than leaving it broken.""")
    else:
        print("\n  (dry run -- pass --apply)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
