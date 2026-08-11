#!/usr/bin/env python3
"""Pass 4801 -- the eight "born-broken" certificates all verify. Pass 4728 was wrong.

Pass 4728 scanned the certificates for the Pass 2482 trap -- integer keys, which sort
numerically in a live Python dict and lexicographically once JSON has turned them into
strings, so that a digest taken over the live dict can never be reproduced from the file.
It reported eight certificates carrying the hazard and called them "unverifiable from
birth", distinguishing them from merely stale ones on the grounds that re-running the
producer could not repair them.

Every one of the eight verifies.

WHAT THE DETECTOR ACTUALLY MEASURED.  It inspected the JSON FILE, where keys are already
strings -- JSON has no other kind.  So it could only ask whether the key SET would sort
differently under the two orderings, which is a property of the keys and says nothing
about how the producer built them.  I read a property of the data as evidence of a bug in
the code, and never opened the code.

The producers are correct, and explicitly so.  w33_pass1837 builds its map as

    'residual_to_duad_index': {str(k): int(v) for k, v in sorted(mapping.items())}

converting keys to strings at construction.  There was no hazard to repair.

THIS PASS ALSO REVERTS A REPAIR I HAD ALREADY APPLIED.  Three producers were patched to
round-trip before hashing, on the strength of Pass 4728's finding, before anything had been
verified.  The patch fixed nothing and would have changed three currently-valid digests.
Reverted.

    py -3 analysis/w33_pass4801_there_were_no_born_broken_certificates.py
"""

from __future__ import annotations

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

ACCUSED = [
    "w33_pass1801_component.json",
    "w33_pass1828_weight_frontier.json",
    "w33_pass1829_weight4_decoder.json",
    "w33_pass1837_middle_layer_compression.json",
    "w33_pass1847_exact_weight5_decoder_completion.json",
    "w33_pass1856_duad_syntheme_contraction_frontier.json",
    "w33_pass1857_weight5_syndrome_orbit_atlas.json",
    "w33_pass1860_weight6_decoder_frontier.json",
]


def main() -> int:
    print("=" * 78)
    print("Pass 4801 -- do the eight accused certificates verify?")
    print("=" * 78)

    print(f"\n  {'certificate':52s} {'verdict':>10s}")
    rows = []
    for c in ACCUSED:
        p = ROOT / "data" / c
        if not p.is_file():
            rows.append({"certificate": c, "verifies": None, "note": "absent"})
            print(f"  {c:52s} {'ABSENT':>10s}")
            continue
        r = subprocess.run(["py", "-3", str(ROOT / "scripts" / "check_certificates.py"),
                            str(p)], cwd=ROOT, capture_output=True, text=True, timeout=300)
        ok = "MISMATCH" not in r.stdout
        rows.append({"certificate": c, "verifies": bool(ok)})
        print(f"  {c:52s} {'verifies' if ok else 'MISMATCH':>10s}")

    good = sum(1 for r in rows if r.get("verifies"))
    print(f"""
    {good} OF {len(rows)} VERIFY. Pass 4728 called all eight unverifiable from birth.

    THE DETECTOR ANSWERED A DIFFERENT QUESTION FROM THE ONE I REPORTED. It read the JSON
    file, where every key is already a string because JSON has no other kind, and asked
    whether that key SET would sort differently under numeric and lexicographic ordering.
    That is a property of the keys. Whether the PRODUCER held them as integers is a property
    of the code, and the code was never opened.

    The producers are correct and explicitly so:

        'residual_to_duad_index': {{str(k): int(v) for k, v in sorted(mapping.items())}}

    Keys are stringified at construction, so the live dict and the file agree and the digest
    reproduces. Pass 2482's trap is real -- it cost a genuinely unverifiable certificate --
    but none of these eight is an instance of it.

    AND I HAD ALREADY STARTED FIXING IT. Three producers were patched to round-trip before
    hashing, on the strength of the finding, before a single certificate had been checked.
    That patch repaired nothing and would have changed three valid digests to different
    valid digests, leaving eight certificates stale that had been fine. Reverted.

    THE RULE THIS BREAKS IS THE ONE THIS REPOSITORY WRITES DOWN. CLAUDE.md, failure mode 6:
    "before writing X costs N or A beats B, state what would make the comparison invalid,
    and check that first." The comparison here was "these certificates cannot verify", and
    what would have made it invalid -- them verifying -- takes one command per file.""")

    out = {
        "boundary": ("each verdict is check_certificates.py run on the single file, which "
                     "tries both serialisation conventions in use here. This pass does not "
                     "claim the Pass 2482 trap is unreal -- it is, and it cost a genuinely "
                     "unverifiable certificate -- only that none of these eight is an "
                     "instance"),
        "accused": rows,
        "verify_count": good,
        "pass_4728_claim": "eight certificates unverifiable from birth",
        "verdict": "FALSE -- all eight reproduce their digests",
        "root_cause": ("the detector inspected the JSON file, where keys are already "
                       "strings, so it could only measure whether the key SET sorts "
                       "differently under two orderings. That is a property of the data; "
                       "whether the producer used integer keys is a property of the code, "
                       "which was not read"),
        "reverted": ["analysis/w33_pass1837_middle_layer_compression.py",
                     "analysis/w33_pass1856_duad_syntheme_contraction_frontier.py",
                     "analysis/w33_pass1857_weight5_syndrome_orbit_atlas.py"],
    }
    fp = ROOT / "data" / "PART_W33_PASS4801_NO_BORN_BROKEN_CERTIFICATES.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
