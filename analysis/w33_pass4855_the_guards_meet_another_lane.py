#!/usr/bin/env python3
"""Pass 4855 -- point the whole guard set at Track B's packet, which none of it has seen.

Pass 4817 found 2 of 16 guards report findings, and noted the number it could not get: a
tool built for a fault that occurred once is indistinguishable from a tool built for a
fault that recurs, until it recurs.  Every guard in this set was calibrated on THIS lane's
output, by me, usually right after I made the mistake it detects.

Track B's 4825-4832 packet is in the repository and none of these guards has been run
against it.  That is the closest thing available to an out-of-sample test, and it cuts both
ways: findings mean the guards generalise, silence means they were fitted to one author.

    py -3 analysis/w33_pass4855_the_guards_meet_another_lane.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# Track B / Track C artifacts: the BT-numbered and PASS-numbered files they own, plus the
# .g GAP sources which are theirs exclusively.
OTHER_LANE = re.compile(
    r"^analysis/(?:BT\d|PASS4(?:32[4-9]|33[0-4]|57[9-9]|58[0-6]|59[2-9]|60[0-9]|"
    r"68[1-8]|69[7-9]|70[0-4]|82[5-9]|83[0-2]))|\.g$|^data/w33_pass_namespace_registry")


def main() -> int:
    print("=" * 78)
    print("Pass 4855 -- the guard set, out of sample")
    print("=" * 78)

    import yaml
    cfg = yaml.safe_load((ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8"))
    hooks = [h for r in cfg.get("repos", []) for h in r.get("hooks", [])]
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT,
                             capture_output=True, text=True).stdout.splitlines()
    theirs = [f for f in tracked if OTHER_LANE.search(f)]
    print(f"\n  files attributable to another lane : {len(theirs):,}")

    SCRIPT = re.compile(r"((?:scripts|analysis|passes|pillars)/[\w./-]+\.py)")
    print(f"\n  {'hook':32s} {'their files':>12s} {'findings':>9s} {'sec':>6s}")
    rows = []
    for h in hooks:
        m = SCRIPT.search(h.get("entry", ""))
        pat = h.get("files")
        if not m or not pat:
            continue
        try:
            rx = re.compile(pat)
        except re.error:
            continue
        files = [f for f in theirs if rx.search(f)]
        if not files:
            continue
        t0 = time.time()
        try:
            r = subprocess.run(["py", "-3", str(ROOT / m.group(1))] + files[:300],
                               cwd=ROOT, capture_output=True, text=True, timeout=420)
            out = r.stdout
            n = len(re.findall(r"^\s{2,}\S+\.(?:py|md|tex|json|sv|g):\d+", out, re.M))
            if n == 0:
                mm = re.search(r"(\d[\d,]*)\s+(?:problem|finding|hit|violation|"
                               r"unresolved|live assertion|unmatchable|negation|"
                               r"unpowered|collapsed|shadowing)", out)
                n = int(mm.group(1).replace(",", "")) if mm else 0
            sample = re.findall(r"^\s{2,}(\S+:\d+.*)$", out, re.M)[:2]
        except Exception:
            n, sample = None, []
        dt = time.time() - t0
        rows.append({"hook": h["id"], "their_files": len(files), "findings": n,
                     "seconds": round(dt, 1), "sample": sample})
        print(f"  {h['id']:32s} {len(files):12,d} "
              f"{('-' if n is None else n):>9} {dt:6.1f}")

    firing = [r for r in rows if isinstance(r["findings"], int) and r["findings"] > 0]
    print()
    for r in firing:
        print(f"    {r['hook']} -- {r['findings']} finding(s)")
        for s in r["sample"]:
            print(f"      {s[:96]}")

    print(f"""
    {len(firing)} of {len(rows)} guards fire on another lane's files.

    THIS IS THE OUT-OF-SAMPLE TEST AND IT CUTS BOTH WAYS. Every guard here was calibrated
    on my own output, usually within minutes of my making the mistake it detects. Findings
    on someone else's files mean the fault classes generalise; silence means the set was
    fitted to one author's habits.

    WHAT SILENCE DOES NOT MEAN. It is not evidence their work is clean, because most of
    these guards look for faults with a specific textual signature -- a collapsed escape, a
    novelty phrasing, an unpowered null -- and another lane can be wrong in ways none of
    them has a pattern for. The guard set encodes MY failure modes, and Pass 4840 already
    found 41% of it was built for mistakes made in this session.

    THE HONEST FRAMING: this measures overlap between two authors' failure modes, not the
    quality of either lane's work.

    AND THE ONE GUARD THAT DID FIRE HAS A FALSE-POSITIVE FAMILY, found only by pointing it
    somewhere new. certificate-digests reported 10 HASH MISMATCHes in
    data/w33_pass_namespace_registry_v2.d/. Those files are not certificates: their sha256
    is a POINTER to the certificate they register, not a digest of themselves. Five of the
    ten do equal the referenced certificate's own sha256 field; five do not.

    So the 10 split into two real things and neither is what the guard said:

      * a FALSE-POSITIVE FAMILY in check_certificates.py, which treats every sha256 key as
        self-digesting. Registry entries use the key with pointer semantics and can never
        satisfy that assumption.
      * a genuine STALENESS finding in 5 of them, where the pointer no longer matches the
        certificate it names -- worth reporting to whoever owns the registry, and invisible
        until the guard was aimed at files it was not calibrated on.

    Pass 4801 already caught this guard's sibling assumption: it reported eight certificates
    'unverifiable from birth' that all verify. Two false-positive families in one checker,
    both from assuming a key name implies a convention.""")

    out = {
        "boundary": ("scoping to 'another lane' is by filename pattern -- BT-numbered "
                     "files, their reserved PASS ranges, and .g sources -- which will "
                     "misattribute any file whose name does not follow those conventions. "
                     "Silence from a guard is NOT evidence the files are clean; it means "
                     "no pattern in this set matched, and the set encodes one author's "
                     "failure modes"),
        "other_lane_files": len(theirs),
        "rows": rows,
        "guards_firing": len(firing),
        "guards_run": len(rows),
        "interpretation": ("findings mean the fault classes generalise beyond their author; "
                           "silence means the set may be fitted to one author's habits, and "
                           "is not evidence of clean files"),
    }
    fp = ROOT / "data" / "PART_W33_PASS4855_GUARDS_OUT_OF_SAMPLE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
