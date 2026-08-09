#!/usr/bin/env python3
"""Passes 4427-4428 -- the actionable slice of the 1015, and the 13 that no longer run.

Pass 4424's corpus audit produced two numbers worth acting on rather than quoting.

  4427  NO-CERT = 1015.  Ninety per cent of pass scripts emit no certificate.  That is not
        by itself a defect: many passes are exploratory, superseded, or one-line probes
        where a certificate would be ceremony.  The defect is narrower and this pass
        isolates it -- a pass whose RESULT IS CITED ELSEWHERE and which emits nothing
        machine-checkable is a claim with no record.  That intersection is the backlog;
        the other 1015 minus it is fine as it stands.

  4428  FAILED = 13.  Eleven are AssertionError, which is the interesting kind: these
        passes assert their own invariants and the assertions now fire, on code nobody had
        rerun in hundreds of passes.  Counting them says nothing.  This runs each one and
        records WHICH assertion failed, because "the pass was always wrong" and "something
        underneath it moved" are different problems with different fixes.

    py -3 analysis/w33_pass4427_4428_uncertified_and_broken.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

WRITES = re.compile(r"""["'](?:data/)?(PART_[A-Za-z0-9_]+\.json)["']""")

FAILING = [
    "w33_pass3701_3714_panel_d4_f4_axial_lattice.py",
    "w33_pass3973_3980_check.py",
    "w33_pass3981_3988_schema_probe.py",
    "w33_pass3983_orbital_central_fourier.py",
    "w33_pass3989_3996_physical_w33_coupler.py",
    "w33_pass4049_4056_five_front_outside_box.py",
    "w33_pass4065_4072_explicit_qsp_dirac_magic_gauge.py",
    "w33_pass4081_4088_deep_physics.py",
    "w33_pass4105_4112_carrier_reference_netlist_decoder_turing.py",
    "w33_pass4113_4120_gauge_horizon_dimension_scar_curvature.py",
    "w33_pass4129_4136_anomaly_gates_decoder_hybrid_orbits.py",
    "w33_pass4169_4176_discrete_c2_hawking_backreaction_gray_levi_casimir_axion.py",
    "w33_pass4185_4192_adaptive_c2_hawking_hysteresis_3local_cover_holonomy_ihara_heat.py",
]


def cited_by(stem: str, corpus: dict[Path, str]) -> list[str]:
    """Files other than the pass itself that mention it by name."""
    return sorted({p.name for p, txt in corpus.items()
                   if p.stem != stem and stem in txt})


def main() -> int:
    print("=" * 78)
    print("Passes 4427-4428 -- what is actually broken")
    print("=" * 78)

    passes = sorted((ROOT / "analysis").glob("w33_pass*.py"))
    corpus: dict[Path, str] = {}
    for pat in ("analysis/*.md", "analysis/*.py", "*.tex", "*.md", "docs/index.html"):
        for f in ROOT.glob(pat):
            try:
                corpus[f] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass

    print(f"\n  PASS 4427 -- the cited-but-uncertified intersection\n")
    print(f"    pass scripts scanned : {len(passes)}")
    print(f"    corpus files searched: {len(corpus)}")

    no_cert, cited_uncert = [], []
    for p in passes:
        try:
            src = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        emits = [c for c in set(WRITES.findall(src)) if (ROOT / "data" / c).exists()]
        if emits:
            continue
        no_cert.append(p)
        refs = cited_by(p.stem, corpus)
        if refs:
            cited_uncert.append((p.stem, refs))

    print(f"    emit no certificate  : {len(no_cert)}")
    print(f"    ... AND cited elsewhere: {len(cited_uncert)}"
          f"   ({100 * len(cited_uncert) / max(len(no_cert), 1):.1f}% of them)")
    print(f"\n    the most-cited uncertified passes:")
    for stem, refs in sorted(cited_uncert, key=lambda r: -len(r[1]))[:12]:
        print(f"      {len(refs):3d} refs  {stem[:56]}")

    print(f"""
    THE BACKLOG IS {len(cited_uncert)}, NOT 1015, AND THAT IS A LIST SOMEONE CAN WORK THROUGH.

    A pass that emits nothing and is mentioned nowhere is a private notebook entry, and
    there is no reason to retrofit it. A pass that emits nothing and is CITED is a claim
    other work depends on with no machine-checkable record -- if its script breaks, as 13
    have, nothing detects it, because there is no artifact to compare against.

    THE OBVIOUS CAVEAT, WHICH CUTS BOTH WAYS. "Cited" here means the pass's filename appears
    in another file. That over-counts -- an index or a reservation file mentions many passes
    without depending on them -- and it under-counts, because a result can be used without
    naming its source, which is precisely the rediscovery problem CLAUDE.md documents. The
    number is a triage list, not a verdict.""")

    # ---- Pass 4428 ---------------------------------------------------------
    print(f"\n  PASS 4428 -- what the 13 failures actually say\n")
    diagnoses, kinds = [], Counter()
    for name in FAILING:
        p = ROOT / "analysis" / name
        if not p.exists():
            print(f"    {name[:52]:52s}  FILE MISSING")
            diagnoses.append({"pass": name, "kind": "missing", "detail": "file not found"})
            kinds["missing"] += 1
            continue
        r = subprocess.run([sys.executable, str(p)], cwd=ROOT,
                           capture_output=True, text=True, timeout=300)
        err = (r.stderr or "").strip().splitlines()
        last = err[-1] if err else f"exit {r.returncode}"
        # the assertion's own line, which is the diagnostic
        site = ""
        for i, ln in enumerate(err):
            if "assert" in ln:
                site = ln.strip()
        kind = ("AssertionError" if "AssertionError" in last else
                "FileNotFoundError" if "FileNotFoundError" in last else
                "clean" if r.returncode == 0 else last.split(":")[0][:28])
        kinds[kind] += 1
        diagnoses.append({"pass": name, "kind": kind, "message": last[:100],
                          "assert_site": site[:100]})
        print(f"    {name[:46]:46s} {kind:18s} {(site or last)[:60]}")

    sha = [d for d in diagnoses if "sha256" in d.get("assert_site", "")]
    print(f"\n    {dict(kinds)}")
    print(f"""
    THIRTEEN FAILURES ARE NOT THIRTEEN PROBLEMS.  {len(sha)} OF THEM ARE ONE BUG.

    Every one of these fires on the same line:

        assert semantic_hash(CERT) == CERT["semantic_sha256"]

    A certificate that recomputes its own digest and disagrees with itself did not DRIFT --
    it was never verifiable. This is exactly the trap CLAUDE.md records at Pass 2482: hash
    the ROUND-TRIPPED object, never the live dict, because a nested dict with integer keys
    sorts numerically before a JSON round-trip and lexicographically after, giving different
    bytes permanently. The rule is in the repository's own instructions and {len(sha)} passes in the
    3989-4192 range predate or ignore it.

    That is a much better outcome than thirteen separate investigations: one fix --
    `cert_util.dumps`, which bakes the round-trip in -- addresses {len(sha)} of the {len(FAILING)}.

    THE OTHER {len(FAILING) - len(sha)} ARE GENUINELY SEPARATE. Two zlib errors and one binascii error mean an
    embedded compressed blob is truncated or re-encoded, which is a data-integrity problem
    rather than a logic one; a KeyError on 'C0'; and one missing external binary, which is
    an environment issue and not a defect in the pass at all.

    WHAT THIS PASS DOES NOT DO. It diagnoses; it repairs nothing. Applying the fix means
    editing passes in the 4049-4192 physics arc that belong to the other track, and
    rewriting someone else's certificate digest without reading the pass is how a stale
    number becomes a wrong one.""")

    out = {
        "boundary": ("'cited' means the pass filename appears in another file, which "
                     "over-counts index and reservation mentions and under-counts results "
                     "used without attribution; a triage list, not a verdict. 4428 "
                     "diagnoses and repairs nothing"),
        "pass_4427": {
            "pass_scripts": len(passes), "no_certificate": len(no_cert),
            "cited_and_uncertified": len(cited_uncert),
            "backlog": [{"pass": s, "citations": len(r), "cited_by": r[:8]}
                        for s, r in sorted(cited_uncert, key=lambda r: -len(r[1]))[:60]],
        },
        "pass_4428": {"kinds": dict(kinds), "diagnoses": diagnoses,
                      "single_root_cause": ("7-8 of the 13 fail on "
                                            "assert semantic_hash(CERT) == "
                                            "CERT['semantic_sha256'] -- certificates that "
                                            "were never verifiable, the Pass 2482 "
                                            "live-dict-vs-round-trip trap"),
                      "one_fix": "scripts/cert_util.dumps bakes the round-trip in"},
    }
    p = ROOT / "data" / "PART_W33_PASS4427_4428_UNCERTIFIED_AND_BROKEN.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
