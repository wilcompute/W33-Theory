#!/usr/bin/env python3
"""Pass 4392 -- six certificates that cannot regenerate, and why two of them never could.

The plan for this pass was a sweep for claims DERIVED from parameters but never CONSTRUCTED
-- the caveat Pass 4381 stated about itself and Pass 4389 removed by building H(3,9).  On
the way to writing that sweep the sharper form of the same question appeared:

    a claim is derived rather than measured if nothing can regenerate it.

That is decidable, so it was decided.  `scripts/check_certificates_regenerate.py` re-runs
each pass, captures the `data/*.json` it writes, and compares byte for byte against the
committed one.  Over this session's passes:

    REPRODUCES 31    DRIFTED 6    TIMEOUT 6    NO-CERT 11

`scripts/check_certificates.py` (Pass 2482) passes all six DRIFTED certificates, because it
checks a certificate against its own digest and never re-runs the script that made it.  A
stale certificate is internally perfectly consistent.  That is failure mode 7 in the exact
shape CLAUDE.md describes: the checker runs, reports, and cannot see the fault.

THE SIX SPLIT INTO THREE KINDS, AND ONLY THE THIRD IS BENIGN.

    kind                what drifted                                  can it be fixed?
    line-number         positions in the .tex manuscripts             yes, by recording text
    float-tail          eigenvalues in the 15th decimal place         yes, by rounding
    (there is no third harmless kind; see below)

THE LINE-NUMBER CERTIFICATES WERE NEVER REPRODUCIBLE.  Four of the six record line numbers
inside living manuscripts -- "the claim on line 581 of the blueprint".  The manuscripts are
edited on most passes; today's plain-language boxes alone moved every line below them.  So
those certificates were stale within hours of being written, and would have been stale
whatever anyone did, because they pin a coordinate in a moving document.  This is not an
accident of timing: it is a design fault, and no digest scheme can rescue it.

    A certificate that records WHERE something is expires.  One that records WHAT it says
    does not.

THE FLOAT-TAIL ONES ARE REAL TOO, JUST SMALLER.  `rho = 4.078733846523831` re-runs as
`...846`.  Nothing is wrong with either number and the claim is unaffected -- but the
certificate is not a reproducible artifact, and a reader who re-runs it sees a mismatch and
has to work out that it is harmless.  A certificate whose failures are usually harmless
trains people to ignore its failures.

    py -3 analysis/w33_pass4392_certificates_that_expire.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DRIFT = [
    ("w33_pass4222_4226_zeta_without_regularity.py", "line-number", 58,
     "bucket contents are manuscript line numbers; every .tex edit moves them"),
    ("w33_pass4300_4306_homeless_render_and_params.py", "line-number", 37,
     "flags keyed by (file, line); 'audited 108' is now 114 as files were added"),
    ("w33_pass4301_4306_the_dual_machine.py", "float-tail", 2,
     "point/line spectral radii differ in the 15th decimal"),
    ("w33_pass4307_4311_the_forty_and_a_reading.py", "line-number", 72,
     "per-manuscript line numbers for every occurrence of the forty"),
    ("w33_pass4321_4323_design_space_and_the_flag_machine.py", "float-tail", 11,
     "rho and loc for the four machines, 15th-decimal only"),
    ("w33_pass4370_4373_sixth_failure_mode.py", "line-number", 6,
     "hedged/strong sentence counts over files that have since been edited"),
]

REMEDIES = {
    "line-number": (
        "record the matched TEXT plus a sha256 of the file it came from, never the line "
        "number. The text survives edits elsewhere in the document; the hash says exactly "
        "which version was scanned, so a mismatch is informative instead of inevitable."),
    "float-tail": (
        "round to a declared precision before serialising -- these are spectral radii "
        "known to ~1e-12, and writing 15 digits claims a reproducibility LAPACK does not "
        "promise across builds. Round to 12 and the certificate becomes portable."),
}


def main() -> int:
    print("=" * 78)
    print("Pass 4392 -- certificates that cannot regenerate")
    print("=" * 78)
    print(f"\n  audited this session's passes with "
          f"scripts/check_certificates_regenerate.py\n"
          f"  REPRODUCES 31    DRIFTED 6    TIMEOUT 6    NO-CERT 11\n")
    print(f"  {'kind':12s} {'fields':>6s}  script")
    for script, kind, n, _ in sorted(DRIFT, key=lambda r: (r[1], -r[2])):
        print(f"  {kind:12s} {n:6d}  {script}")

    for kind in ("line-number", "float-tail"):
        rows = [r for r in DRIFT if r[1] == kind]
        print(f"\n  {kind.upper()} -- {len(rows)} certificate(s), "
              f"{sum(r[2] for r in rows)} fields")
        for script, _, _, why in rows:
            print(f"    {script[:58]:58s} {why}")
        print(f"    REMEDY: {REMEDIES[kind]}")

    print("""
  THE FINDING THAT GENERALISES, AND IT IS ABOUT CHECKS RATHER THAN CERTIFICATES.

  `check_certificates.py` verifies a certificate against its own stored digest. Every one
  of these six passes that check. It cannot do otherwise: the digest was computed from the
  bytes on disk, and the bytes on disk have not changed -- the WORLD changed. A check that
  compares an artifact only to itself measures nothing about whether the artifact is still
  true, and it will report clean forever.

  The only check that can see this fault is one that RE-RUNS THE COMPUTATION. That check
  now exists, it ships with a planted fault it must detect, and it is wired into CI as
  advisory (six passes exceed a ninety-second budget, and a timeout is not a defect).

  AND THE HONEST SCOPE OF THIS PASS. It audited THIS SESSION's passes, roughly fifty of
  four thousand. I have not run it over the corpus and I am not extrapolating a rate from
  fifty -- Pass 4388 in this same session generalised from five cases and was refuted at
  two hundred and sixteen. What is established is that six certificates in the recent set
  are stale, that four of them are stale by construction rather than by accident, and that
  every existing check passed all six.""")

    out = {"audited": "this session's passes (~50 of ~4000)",
           "verdicts": {"REPRODUCES": 31, "DRIFTED": 6, "TIMEOUT": 6, "NO-CERT": 11},
           "drift": [{"script": s, "kind": k, "fields": n, "why": w}
                     for s, k, n, w in DRIFT],
           "remedies": REMEDIES,
           "checker": "scripts/check_certificates_regenerate.py (--selftest plants a fault)",
           "why_existing_checks_missed_it": (
               "check_certificates.py compares a certificate to its own digest and never "
               "re-runs the generating script, so a stale certificate is internally "
               "consistent and passes"),
           "scope": ("no rate is extrapolated to the corpus; only this session's passes "
                     "were re-run"),
           "conclusion": ("six certificates cannot regenerate; four record line numbers in "
                          "living manuscripts and were therefore never reproducible, two "
                          "differ only in float tails; a certificate that records WHERE "
                          "something is expires, one that records WHAT it says does not")}
    p = ROOT / "data" / "PART_W33_PASS4392_CERTIFICATES_THAT_EXPIRE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
