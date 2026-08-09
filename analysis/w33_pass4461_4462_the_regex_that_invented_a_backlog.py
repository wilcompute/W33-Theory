#!/usr/bin/env python3
"""Passes 4461-4462 -- reading three passes retracted my biggest finding of the session.

Pass 4459 ranked 23 passes as "searched, no baseline, no certificate, and cited".  Pass 4461
was meant to READ the top three rather than grep them, per CLAUDE.md's rule that shallow
search has twice produced retracted conclusions here.  It did, and the first file read
demolished the list.

  `w33_pass569_z9_coupled_affine_radial_quadratic.py` is exemplary.  It EXHAUSTIVELY
  enumerates F3^13 -- all 1,594,323 sections -- with CRT arithmetic over three primes and a
  proven coefficient bound, ships eleven checks, carries an explicit `boundary` field
  ("Exact for F3^13. No claim is made for all 9^40 sections"), and supports `--check` for
  certificate drift.  It needs no random baseline because it is not a random search, which
  is exactly the legitimate false positive my own checker's docstring predicted.

  AND IT EMITS A CERTIFICATE: `data/w33_pass569_z9_coupled_affine_radial_quadratic.json`.

That last line is the problem.  My certificate detector matched only `PART_*.json`.  This
repository's dominant convention is `w33_passNNNN_*.json`, and the detector had never seen
one.  Everything built on it inherits the error:

    Pass 4424  "NO-CERT = 1015; 90% of pass scripts emit no certificate"   RETRACTED
    Pass 4427  "the backlog is 780, not 1015"                              RETRACTED
    Pass 4459  "23 passes searched, claimed a winner, and emit nothing"    RETRACTED

  4462  Separately: Pass 4457 left a ceiling hypothesis open, needing GQ(2,t) with large t
        to test.  Higman's inequality settles whether such a thing can exist at all, so the
        question is closed by a theorem rather than left as future work.

    py -3 analysis/w33_pass4461_4462_the_regex_that_invented_a_backlog.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
import check_search_baseline as csb  # noqa: E402

OLD = re.compile(r"""["'](?:data/)?(PART_[A-Za-z0-9_]+\.json)["']""")
NEW = re.compile(r"""["'](?:data/)?([A-Za-z0-9_]+\.json)["']""")


def main() -> int:
    print("=" * 78)
    print("Passes 4461-4462 -- the regex that invented a backlog")
    print("=" * 78)

    passes = sorted((ROOT / "analysis").glob("w33_pass*.py"))
    old_yes, new_yes, missed = 0, 0, []
    srcs = {}
    for p in passes:
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        srcs[p] = t
        o = [c for c in set(OLD.findall(t)) if (ROOT / "data" / c).exists()]
        n = [c for c in set(NEW.findall(t)) if (ROOT / "data" / c).exists()]
        old_yes += bool(o)
        new_yes += bool(n)
        if n and not o:
            missed.append(p.stem)

    total = len(srcs)
    print(f"\n  PASS 4461 -- the measurement, redone\n")
    print(f"    pass scripts                          : {total}")
    print(f"    emit a certificate, OLD detector      : {old_yes}"
          f"   ({100 * old_yes / total:.0f}%)")
    print(f"    emit a certificate, CORRECTED         : {new_yes}"
          f"   ({100 * new_yes / total:.0f}%)")
    print(f"    passes the old detector could not see : {len(missed)}")
    print(f"    true NO-CERT count                    : {total - new_yes}"
          f"   (Pass 4424 reported 1015)")

    # redo the intersection with the corrected detector
    searched, no_base, worst = 0, 0, []
    corpus = {}
    for pat in ("analysis/*.md", "analysis/*.py", "*.tex", "*.md"):
        for f in ROOT.glob(pat):
            try:
                corpus[f] = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                pass
    for p, t in srcs.items():
        s, b, _ = csb.scan(t)
        if not s:
            continue
        searched += 1
        if b:
            continue
        no_base += 1
        emits = [c for c in set(NEW.findall(t)) if (ROOT / "data" / c).exists()]
        if emits:
            continue
        refs = sorted({f.name for f, txt in corpus.items()
                       if f.stem != p.stem and p.stem in txt})
        if refs:
            worst.append({"pass": p.stem, "citations": len(refs)})
    worst.sort(key=lambda r: -r["citations"])

    print(f"\n    the Pass 4459 intersection, recomputed:")
    print(f"      passes that search                        : {searched}")
    print(f"      ... with no baseline                      : {no_base}")
    print(f"      ... AND no certificate AND cited          : {len(worst)}"
          f"   (Pass 4459 reported 23)")
    for r in worst[:10]:
        print(f"        {r['citations']:3d} refs  {r['pass'][:56]}")

    print(f"""
    THREE FINDINGS ARE RETRACTED AND THE CAUSE IS ONE REGEX.

    Pass 4424's headline -- "1015 of 1129 pass scripts emit no certificate, so 90% of the
    corpus is unaudited by every certificate check here" -- was the largest structural claim
    I made all session, and it was an artifact. The real figure is {new_yes} of {total} passes DO
    emit one, {100 * new_yes / total:.0f}%. The detector matched `PART_*.json` because that is the convention I
    had been using for my own passes, and it never occurred to me that mine were the
    minority. {len(missed)} passes were invisible to it.

    WHAT MADE THE ERROR SURVIVE FOUR PASSES IS THE PART WORTH KEEPING. 4424 reported it,
    4427 refined it, 4441 cited it, 4459 built a priority list on it. Every one of those
    consumed the number without re-deriving it, and each added confidence rather than
    scrutiny. The detector was never wrong in a way any of them could see, because they all
    asked it the same question.

    IT TOOK READING ONE FILE. CLAUDE.md says shallow search has twice produced retracted
    conclusions in this repository and that the fix is to read rather than grep. Pass 4461
    was scheduled to read three files. The first one -- an exhaustive CRT enumeration with
    its own boundary statement and drift check, sitting at the top of my "worst offenders"
    list -- was so obviously misfiled that the list could not survive it.""")

    # ---- Pass 4462: Higman ------------------------------------------------
    print(f"\n  PASS 4462 -- can the s = 2 ceiling hypothesis be tested at all?\n")
    print(f"    {'s':>3s} {'Higman bound t <= s^2':>22s} {'known classical t':>20s}")
    rows = []
    for s in (2, 3, 4, 9):
        known = {2: [1, 2, 4], 3: [1, 3, 5, 9], 4: [1, 2, 4, 8, 16], 9: [1, 3, 9, 27, 81]}
        allowed = [t for t in known[s] if t <= s * s]
        rows.append({"s": s, "higman_max_t": s * s, "classical_t": allowed})
        print(f"    {s:3d} {s * s:22d} {str(allowed):>20s}")

    print(f"""
    THE HYPOTHESIS IS UNTESTABLE, AND THAT IS A THEOREM RATHER THAN A LIMITATION.

    Pass 4457 found that raising t costs nothing at s = 2 (85.0% to 86.0%) and a factor of
    four at s = 3, and offered a ceiling as the reconciling hypothesis: at 3 edges per line
    almost everything already works, so t has no room to show. Testing that needs GQ(2,t)
    with t large.

    HIGMAN'S INEQUALITY SAYS t <= s^2 for any generalised quadrangle with s > 1. At s = 2
    that caps t at 4 -- and 4 is the value already measured. There is no larger GQ(2,t), not
    because none has been constructed but because none can exist.

    So the ceiling hypothesis cannot be distinguished from "t genuinely does nothing at
    s = 2" by any quadrangle whatsoever. It is not an open question awaiting a construction;
    it is a question the objects cannot answer. Pass 4457 listed it as future work and it
    should have been closed there -- one inequality, already in every textbook on the
    subject.""")

    out = {
        "boundary": ("the corrected certificate count matches any *.json in data/ named in "
                     "the source; a pass that writes a certificate under a computed name "
                     "would still be missed, so this is a lower bound on certificate "
                     "coverage rather than an exact figure"),
        "pass_4461_retraction": {
            "pass_scripts": total,
            "certificates_old_detector": old_yes,
            "certificates_corrected": new_yes,
            "invisible_to_old_detector": len(missed),
            "true_no_cert": total - new_yes,
            "retracts": {
                "4424": "NO-CERT = 1015, '90% of pass scripts emit no certificate'",
                "4427": "'the backlog is 780, not 1015'",
                "4459": "'23 passes searched, claimed a winner, and emit nothing'",
            },
            "corrected_intersection": len(worst),
            "cause": ("the detector matched only PART_*.json; the repository's dominant "
                      "convention is w33_passNNNN_*.json and it had never seen one"),
            "why_it_survived": ("four passes consumed the number without re-deriving it, "
                                "each adding confidence rather than scrutiny, because they "
                                "all asked the same instrument the same question"),
            "found_by": ("reading w33_pass569 -- an exhaustive CRT enumeration over F3^13 "
                         "with its own boundary field and drift check, sitting at the top "
                         "of the 'worst offenders' list"),
        },
        "pass_4462_higman": {
            "inequality": "t <= s^2 for any GQ(s,t) with s > 1 (Higman)",
            "rows": rows,
            "verdict": ("the s=2 ceiling hypothesis is UNTESTABLE: Higman caps t at 4 when "
                        "s = 2, and t = 4 is already measured. No larger GQ(2,t) can exist"),
        },
    }
    p = ROOT / "data" / "PART_W33_PASS4461_4462_REGEX_RETRACTION.json"
    p.parent.mkdir(exist_ok=True)
    p.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
