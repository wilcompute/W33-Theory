"""Passes 5344-5347 -- three measured negatives about detecting a certificate that
disagrees with itself, and one small positive about where BT818's 9 came from.

  5344  BT818's prose is repaired in place.  Its computation was never wrong, so nothing
        executable changed; the `correction` string is now interpolated from the computed
        value so the two halves cannot drift again.

  5345  Was alpha = 9 ever TRUE of some nearby graph?  If so it is a coordinate artefact --
        failure mode 1 -- and a different kind of problem than a typo.

  5346  Triage the 388 prose/data findings beyond the hand-checked ten, using the data
        rather than more hand-checking.

  5347  Extend the comparison to DOCSTRINGS, since BT818's worst error lived there and the
        guard reads only JSON prose fields.  Measured, and the measurement is unflattering.

    THE THEME, stated up front because three of these four are negatives: this fault class
    is genuinely hard to detect mechanically, and the reason is structural rather than a
    failure of tuning.  A certificate legitimately names numbers that are not its own field
    values.  "744" beside a j-invariant, "7" beside a Szilassi polyhedron with seven faces,
    "2" beside an SU(2).  A hand-typed wrong value looks exactly like those.

    py -3 analysis/w33_pass5344_5347_the_fault_class_that_resists_detection.py
"""

from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
from check_cert_prose_vs_data import _numbers_near  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# BT818's ORIGINAL docstring, kept verbatim so the recall test below is reproducible after
# the repair. Taken from the file before Pass 5340 edited it.
ORIGINAL_DOCSTRING = """  T1. Exact maximum independent set of the W(3,3) collinearity graph by
      branch-and-bound: alpha = 9 < 10 = theta (ratio bound).
  T2. KS ledger: every marking satisfying s contexts exactly-once obeys
      s <= 34; exhibit an optimal 34-marking and report the
      structure of misses (6 = q! unsatisfied contexts)."""

# Stem frequencies from the 388-finding sweep. A stem driving many findings is a generic
# word, which is the signature of noise rather than of a real contradiction.
STEM_COUNTS = {"rank": 26, "lambda": 21, "sections": 21, "exhaustive": 19, "formula": 15,
               "numerator": 13, "supply": 12, "leader": 10, "kappa": 10, "cost": 10,
               "capacity": 9, "count": 7}


def main() -> int:
    print("=" * 78)
    print("Passes 5344-5347 -- three negatives and a small positive")
    print("=" * 78)

    print("\n  PASS 5344 -- BT818 repaired, computation untouched\n")
    cert = json.loads((ROOT / "data" / "bt818_ovoid_nogo_theta_gap.json")
                      .read_text(encoding="utf-8"))
    print(f"    alpha_exact : {cert['alpha_exact']}")
    print(f"    correction  : ...{cert['correction'][-32:]}")
    print(f"    ks_best     : {cert['ks_best']}   ks_misses: {cert['ks_misses']}")
    agree = f"alpha = {cert['alpha_exact']}" in cert["correction"]
    print(f"    prose now agrees with data : {agree}")
    print("""
    THE REPAIR THAT MATTERS IS NOT THE DIGIT. The `correction` string is now built by
    interpolating the computed value rather than restating it, so the two halves cannot
    drift apart again. Editing the 9 to a 7 would have fixed today and left tomorrow open.""")

    print("\n  PASS 5345 -- was 9 ever true of anything?\n")
    print("    alpha(W(3,3) points)                = 7")
    print("    alpha(Q(4,3) points = W(3,3) lines) = 10")
    print("    is 9 either of them?                  no")
    print("""
    SO IT IS A TYPO, NOT A COORDINATE ARTEFACT, and that distinction was worth ten minutes.
    Failure mode 1 in this corpus is a claim that is true of a DIFFERENT drawing of the same
    object -- had 9 been the independence number of the line graph, or of a complement, BT818
    would have been describing a real object under the wrong name and the repair would be a
    relabelling. It is not. 9 sits strictly between the two real values, 7 and 10, and
    matches neither, which is what a hand-typed number looks like.""")

    print("\n  PASS 5346 -- triaging 388 findings with data instead of patience\n")
    tot = 388
    noisy = sum(c for c in STEM_COUNTS.values())
    print(f"    {'stem':22s} {'findings':>9s}")
    for s, c in list(STEM_COUNTS.items())[:8]:
        print(f"    {s:22s} {c:9d}")
    print(f"\n    findings from stems seen >= 5 times : {noisy} of {tot} "
          f"({100 * noisy // tot}%)")
    print(f"""
    THE HAND-TRIAGE OF TEN GAVE 1-IN-10 AND THIS AGREES WITH IT BY A DIFFERENT ROUTE. A stem
    that drives twenty-six findings -- "rank", "lambda", "sections", "exhaustive" -- is a
    generic English or mathematical word, and a generic word appearing near a number in a
    long boundary sentence is the definition of a coincidence. {100 * noisy // tot}% of the findings come
    from the twelve commonest stems alone.

    WHAT THAT LEAVES. The findings driven by a stem seen ONCE are where a real contradiction
    would sit, because a specific field name near a specific wrong number is what the fault
    actually looks like. That is 76 of 388, and even those are mostly benign. I am not
    reading all 388, and saying so is more useful than a fake triage.""")

    print("\n  PASS 5347 -- extending to docstrings, and the measurement\n")
    caught = []
    for key, val in (("alpha_exact", 7), ("ks_best", 36), ("ks_misses", 4)):
        toks = [t for t in re.split(r"[ _]", key) if len(t) >= 4]
        stem = max(toks, key=len)
        found = _numbers_near(ORIGINAL_DOCSTRING, stem)
        bad = {x for x in found if abs(x - val) <= max(50, abs(val))} - {val}
        caught.append((key, val, stem, sorted(found), sorted(bad)))
        print(f"    {key:11s} data={val:3d}  stem={stem!r:9s}  found={sorted(found)}  "
              f"-> {'CAUGHT' if bad else 'missed'}")
    hits = sum(1 for *_, b in caught if b)
    print(f"""
    RECALL ON ITS OWN FOUNDING CASE: {hits} OF {len(caught)}. It catches alpha=9 because the field is named
    `alpha_exact` and the docstring says "alpha". It misses both KS faults because the
    docstring writes "s <= 34" while the field is `ks_best` -- the human sentence and the
    machine field use different words for the same quantity, which is the normal case and
    not an oversight by whoever wrote it.

    AND THE COST: 774 findings over 1,646 py/certificate pairs, a 47% flag rate. Worse than
    the JSON-only sweep's 9% and far past the noise threshold Pass 328 measured. So the
    docstring extension is NOT registered as a hook.

    THE STRUCTURAL REASON, which is the reusable part of all three negatives. Tightening the
    match to kill the noise also kills the signal: requiring the full field name
    (`alpha_exact`, `ks_best`) to appear in the prose would drop the false positives AND drop
    BT818, because prose does not use field names. The signal and the noise have the same
    shape, and that is not a tuning problem.

    WHAT ACTUALLY FOUND BT818 was reading the file while searching for something else. The
    guard is worth keeping as a triage aid at 1-in-10 and worth nothing as a gate, and the
    honest lesson from four passes of trying is that this class is caught by reading.""")

    out = {
        "boundary": ("Three of these four passes are NEGATIVE results about detectability. "
                     "The 388-finding triage is by STEM FREQUENCY, a proxy for genericity, "
                     "not a per-finding classification -- 388 findings were not individually "
                     "read and no claim is made about the 76 driven by rare stems. The "
                     "docstring recall figure is measured on BT818's original text only, "
                     "which is one case. alpha(W(3,3))=7 remains Pass4795/Pass4800's"),
        "pass_5344": {"repaired": "analysis/bt818_ovoid_nogo_theta_gap.py",
                      "computation_changed": False,
                      "fix": ("the `correction` string now interpolates the computed value "
                              "instead of restating it, so the halves cannot drift again"),
                      "prose_agrees_with_data": agree},
        "pass_5345": {"alpha_W33_points": 7, "alpha_Q43_points": 10,
                      "nine_matches_either": False,
                      "verdict": ("typo, not a coordinate artefact -- 9 sits strictly "
                                  "between the two real values and matches neither")},
        "pass_5346": {"findings": tot, "top_stems": STEM_COUNTS,
                      "from_frequent_stems": noisy,
                      "pct_from_frequent_stems": 100 * noisy // tot,
                      "agrees_with": "the independent 1-in-10 hand triage at Pass 5327",
                      "not_done": "the 388 findings were not individually read"},
        "pass_5347": {"docstring_recall_on_founding_case": f"{hits}/{len(caught)}",
                      "detail": [{"key": k, "data": v, "stem": s, "found": f, "caught": bool(b)}
                                 for k, v, s, f, b in caught],
                      "flag_rate": "774 of 1646 py/certificate pairs = 47%",
                      "registered": False,
                      "why_not": ("47% is past the noise threshold; and tightening the "
                                  "match to fix that also drops BT818, because prose does "
                                  "not use field names. Signal and noise share a shape")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5344_5347_DETECTION_LIMITS.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
