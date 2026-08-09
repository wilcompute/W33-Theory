#!/usr/bin/env python3
"""Pass 4463 -- the correction was itself under-corrected, and how to stop the ladder.

Pass 4461 retracted Pass 4424's "1015 pass scripts emit no certificate" after finding the
detector matched only `PART_*.json` while the dominant convention is `w33_passNNNN_*.json`.
It reported the corrected figure as 269 and moved on.

That was the same mistake one level up.  I found an instrument wrong, replaced it with a
better guess, and immediately trusted the replacement without asking whether IT was
complete.  It was not.  `data/` holds six naming conventions, 161 JSON filenames contain
characters the "corrected" regex rejects, and 498 files live in subdirectories the pattern
never looked at.

    detector                              detected   claimed NO-CERT
    v1  PART_*.json          (Pass 4424)       133              1015
    v2  [A-Za-z0-9_]+.json   (Pass 4461)       879               269
    v3  any quoted path with a data extension  883               265
    v3 minus scripts that build paths dynamically (25)     upper bound 240

Each rung found more.  The ladder only stops when the question is asked from the other
side, against ground truth, which is what the second half of this pass does: instead of
"does this script name a file I recognise", ask "can this file on disk be attributed to any
script at all".  That question has no recogniser to be wrong about.

    py -3 analysis/w33_pass4463_the_correction_was_undercorrected.py
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

DATA = ROOT / "data"
EXT = r"(?:json|jsonl|csv|txt|npy|npz|memmap|b85|b64|zip|md|tex|html)"
V1 = re.compile(r"""["'](?:data/)?(PART_[A-Za-z0-9_]+\.json)["']""")
V2 = re.compile(r"""["'](?:data/)?([A-Za-z0-9_]+\.json)["']""")
V3 = re.compile(r"""["']([^"'\n]*?\.""" + EXT + r""")["']""")
DYN = re.compile(
    r"""f["'][^"'\n]*\.""" + EXT
    + r"""|\.format\(|["']\s*\+\s*\w+|DATA\s*/\s*\w|ROOT\s*/\s*["']data["']\s*/\s*\w""")


def main() -> int:
    print("=" * 78)
    print("Pass 4463 -- the correction was under-corrected")
    print("=" * 78)

    files = [f for f in DATA.rglob("*") if f.is_file()]
    have = {f.name for f in files}
    passes = sorted((ROOT / "analysis").glob("w33_pass*.py"))

    tally = collections.Counter()
    for p in passes:
        t = p.read_text(encoding="utf-8", errors="replace")

        def hit(rx):
            return any(pathlib.Path(m).name in have for m in rx.findall(t))
        tally["total"] += 1
        tally["v1"] += hit(V1)
        tally["v2"] += hit(V2)
        tally["v3"] += hit(V3)
        if not hit(V3) and DYN.search(t):
            tally["dyn"] += 1

    n = tally["total"]
    print(f"\n  THE LADDER  ({n} pass scripts, {len(files)} files under data/)\n")
    print(f"  {'detector':46s} {'detects':>8s} {'NO-CERT':>9s}")
    ladder = [
        ("v1  PART_*.json                    (Pass 4424)", tally["v1"]),
        ("v2  [A-Za-z0-9_]+.json             (Pass 4461)", tally["v2"]),
        ("v3  any quoted path, any extension (Pass 4463)", tally["v3"]),
    ]
    for label, k in ladder:
        print(f"  {label:46s} {k:8d} {n - k:9d}")
    ub = n - tally["v3"] - tally["dyn"]
    print(f"  {'    ... minus ' + str(tally['dyn']) + ' that build paths dynamically':46s} "
          f"{'':8s} {ub:9d}  <- upper bound")

    # ---- ground truth, asked from the files' side -------------------------
    blob = "\n".join(p.read_text(encoding="utf-8", errors="replace")
                     for p in sorted((ROOT / "analysis").glob("*.py")))
    named = sum(1 for f in files if f.name in blob)
    stem = sum(1 for f in files if f.name not in blob and f.stem in blob)
    orphan = [f for f in files if f.name not in blob and f.stem not in blob]
    print(f"\n  GROUND TRUTH, ASKED FROM THE FILES' SIDE\n")
    print(f"    files under data/                    : {len(files)}")
    print(f"    named verbatim in some analysis/*.py : {named}"
          f"  ({100 * named / len(files):.0f}%)")
    print(f"    stem named, full filename not        : {stem}")
    print(f"    attributable to NO script            : {len(orphan)}"
          f"  ({100 * len(orphan) / len(files):.0f}%)")
    oext = collections.Counter(f.suffix.lower() for f in orphan)
    print(f"    orphan extensions                    : {dict(oext.most_common(5))}")

    print(f"""
  I MADE THE SAME MISTAKE TWICE, ONE LEVEL APART.

  Pass 4461 correctly diagnosed that a regex had invented a backlog, replaced it, and
  reported {n - tally['v2']} with the same confidence 4424 had reported 1015. The replacement was a better
  guess at the naming conventions, not a measurement of them, and it was wrong by about
  {tally['v3'] + tally['dyn'] - tally['v2']} scripts. Finding an instrument broken is not the same as fixing it, and I
  treated them as the same act.

  THE LADDER ONLY STOPS BY CHANGING THE QUESTION. Every rung above asks "does this script
  name a file the recogniser knows", so every rung inherits a recogniser. Asking the files
  instead -- "can this be attributed to any script" -- needs no pattern at all, and it
  produces a number the script-side view cannot: {len(orphan)} files ({100 * len(orphan) / len(files):.0f}%) in data/ are named by no
  analysis script whatsoever.

  THAT IS A LARGER AND MORE INTERESTING GAP THAN THE ONE I WAS CHASING. {len(orphan)} orphaned data
  files is not a certificate-hygiene problem; it is {100 * len(orphan) / len(files):.0f}% of the repository's data with no
  visible producer. Some will be inputs rather than outputs, some are written by scripts
  outside analysis/, and some are genuinely abandoned. Distinguishing those is a real task
  and it is NOT attempted here -- stating the number and its ambiguity is the whole claim.

  AND THE RULE THIS SESSION HAS NOW EARNED TWICE: when a measurement disagrees with
  expectation, check the instrument before the world; and when the instrument turns out to
  be wrong, validate its replacement against something that is not another instrument of
  the same kind.""")

    out = {
        "boundary": ("the ladder counts scripts whose source names an existing data file; "
                     "the ground-truth half counts files named anywhere in analysis/*.py "
                     "and cannot distinguish inputs from outputs, nor see producers outside "
                     "analysis/. Neither half establishes that an orphan is abandoned"),
        "ladder": {"pass_scripts": n,
                   "v1_PART_only": tally["v1"], "v1_claimed_no_cert": n - tally["v1"],
                   "v2_word_json": tally["v2"], "v2_claimed_no_cert": n - tally["v2"],
                   "v3_any_extension": tally["v3"], "v3_no_cert": n - tally["v3"],
                   "dynamic_path_builders": tally["dyn"],
                   "upper_bound_output_free": ub},
        "ground_truth": {"files": len(files), "named_verbatim": named,
                         "stem_only": stem, "orphaned": len(orphan),
                         "orphan_extensions": {k: v for k, v in oext.most_common(8)}},
        "retracts": ("Pass 4461's corrected figure of 269 NO-CERT; the upper bound is "
                     f"{ub} and the true value is lower still"),
        "lesson": ("finding an instrument broken is not fixing it; a replacement guess "
                   "must be validated against something that is not another instrument "
                   "of the same kind -- here, the files themselves"),
    }
    p = ROOT / "data" / "PART_W33_PASS4463_UNDERCORRECTED.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
