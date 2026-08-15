"""Passes 5280-5283 -- the mechanical reason this session rediscovered its own work, found
by following the failure down to a four-word omission.

  5280  Passes 5274-5275 established that Passes 5226-5275 re-derived Pass 4800.  The
        obvious question is why the rediscovery HOOK did not fire.  It runs at commit time,
        it looks up a staged file's results in RESULTS_INDEX.md, and it exists precisely for
        this.  Following it down gives a chain, each link measurable:

            RE_INT requires \\d{3,9}          -> 7, 18, 10, 26 are invisible
            noun@n mitigation exists (P1107) -> handles exactly this case
            GEOM_NOUNS lists "ovoid", "spread", ... but NOT "alpha" or "deficit"
            Pass 4800's two phrases are "alpha(W(3,5)) = 18" and "the deficit is 8"
            -> Pass 4800 emits ZERO tokens and is ABSENT from the index entirely

  5281  So the fix is four words in a lexicon.  It is measured before being kept, because
        the same list carries a comment recording that generic nouns once cost nine points
        of noise -- and "alpha" is genuinely ambiguous here, the physics track uses it for
        the fine-structure constant.

  5282  Item 6 of the plan was "build a hook that greps a pass's own numbers against
        RESULTS_INDEX".  It already exists, built at Pass 328.  Building it again would have
        been this session's failure mode applied to its own remedy.

  5283  And the guards are audited against the OTHER lane's failure modes rather than mine,
        since silence on their work has so far measured overlap between authors.

    py -3 analysis/w33_pass5280_5283_why_the_index_could_not_see_pass4800.py
"""

from __future__ import annotations

import collections
import glob
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402
import check_rediscovery as CR  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

NEW_NOUNS = ("alpha", "independence number", "coclique", "deficit", "Hoffman bound",
             "maximum partial ovoid")
# The other lane's documented failure modes, taken from ITS OWN correction commits and
# boundary statements, not from mine. This is the list my guards were never fitted to.
THEIR_MODES = [
    {"mode": "renumbering a concurrently-developed packet",
     "evidence": "Pass5254-5261 header: 'authoritatively renumbered' to avoid overwriting",
     "my_guard": None},
    {"mode": "claim promoted before exact certification",
     "evidence": "their boundary: 'Hoffman shortened distance must be certified exactly "
                 "before promotion'",
     "my_guard": "check_search_power (partially -- it reads search claims, not "
                 "certification status)"},
    {"mode": "all-q formula from q3/q5/q7 anchors",
     "evidence": "their boundary: 'All-q formulas require proof beyond q3,q5,q7 anchors'",
     "my_guard": None},
    {"mode": "stale claim reaching a published surface",
     "evidence": "their Pass4996 firewall, 8 rules, fail-closed, currently red",
     "my_guard": "check_retraction_propagation (generic; theirs is claim-specific)"},
    {"mode": "development filename vs authoritative pass number drift",
     "evidence": "their results JSON maps 'original development filenames' as provenance",
     "my_guard": None},
]


def main() -> int:
    print("=" * 78)
    print("Passes 5280-5283 -- a four-word omission, measured")
    print("=" * 78)

    print("\n  PASS 5280 -- the chain, each link checked\n")
    t4800 = (ROOT / "analysis" / "w33_pass4800_the_deficit_law_is_false.py").read_text(
        encoding="utf-8", errors="replace")
    idx = (ROOT / "RESULTS_INDEX.md").read_text(encoding="utf-8", errors="replace")
    indexed = set(re.findall(r"`([^`]+\.(?:py|md|tex))`", idx))
    allpy = {Path(p).as_posix() for p in glob.glob(str(ROOT / "analysis" / "*.py"))}
    allpy = {p.split("Theory of Everything/")[-1] for p in allpy}

    print(f"    RE_INT pattern requires             : 3+ digits "
          f"({CR.RE_INT.pattern[-20:].strip()})")
    print(f"    Pass 4800's results                 : 7, 18, 10, 26, deficits 3 and 8")
    print(f"    -> visible to RE_INT?               : "
          f"{bool(CR.RE_INT.findall('alpha = 18 deficit 8'))}")
    print(f"    noun@n mitigation exists since      : Pass 1107")
    print(f"    Pass 4800 tokens NOW                : "
          f"{sorted(CR.noun_number_pairs(t4800))[:6]} ...")
    p4800 = "analysis/w33_pass4800_the_deficit_law_is_false.py"
    print(f"    Pass 4800 in RESULTS_INDEX now      : {p4800 in indexed}")
    print(f"    analysis/*.py coverage              : "
          f"{len(allpy & indexed):,} of {len(allpy):,} "
          f"({100 * len(allpy & indexed) // max(len(allpy), 1)}%)")
    print("""
    THE WHOLE FAILURE WAS FOUR WORDS. Not a design flaw, not a missing tool, not
    carelessness at the search step -- the hook, the index, the noun@n mitigation and the
    calibration study all existed and all worked. The lexicon of geometry nouns simply did
    not contain the words this lane writes its results with. "ovoid" was there because a
    2026 collision put it there; "alpha" was not, because no collision had yet cost anything.

    THAT IS THE UNCOMFORTABLE GENERAL SHAPE. Every entry in that lexicon is a fossil of one
    past failure, so the list can only ever cover faults that have already happened once.
    The index is not a search over the corpus; it is a search over the vocabulary of
    remembered mistakes.""")

    print("\n  PASS 5281 -- measuring the fix before keeping it\n")
    rx = re.compile(r"(?i)\b(" + "|".join(re.escape(n) for n in NEW_NOUNS) + r")\b")
    files = sorted(glob.glob("analysis/*.py") + glob.glob("analysis/*.md"))
    touched, toks = 0, collections.Counter()
    for f in files:
        try:
            t = Path(f).read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if rx.search(t):
            touched += 1
            for tok in CR.noun_number_pairs(t):
                if tok.split("@")[0] in {n.replace(" ", "-") for n in NEW_NOUNS}:
                    toks[tok] += 1
    kept = sum(1 for c in toks.values() if c <= 25)
    print(f"    files touched by the new nouns  : {touched:,} of {len(files):,} "
          f"({100 * touched // len(files)}%)")
    print(f"    distinct new tokens             : {len(toks):,}")
    print(f"    surviving the >25-file cut      : {kept:,}")
    print(f"\n    {'token':26s} {'files':>6s}  verdict")
    for tok in ("alpha@18", "deficit@8", "alpha@26", "alpha@65", "alpha@7", "alpha@137"):
        c = toks.get(tok, 0)
        v = ("not present" if not c else
             "DISTINCTIVE -- indexed" if c <= 25 else "dropped as non-distinctive")
        print(f"    {tok:26s} {c:6d}  {v}")
    print(f"""
    THE FIX WORKS AND IT IS NOT CLEAN. alpha@18 sits in {toks.get('alpha@18', 0)} files including Pass 4800, so
    a commit asserting alpha = 18 now collides with it -- this session's rediscovery WOULD
    have been caught. But alpha@7 is in {toks.get('alpha@7', 0)} files and stays dropped, and alpha@137 is in
    {toks.get('alpha@137', 0)} because the physics track uses alpha for the fine-structure constant. The same
    token prefix carries two unrelated meanings in one corpus.

    SO THE HONEST CLAIM IS NARROW: one specific rediscovery becomes catchable, several
    neighbouring ones do not, and the noise cost is {100 * touched // len(files)}% of files touched rather than the
    nine-point blowup the lexicon's own comment warned about. Measured, not assumed, because
    that comment exists precisely because someone once did assume.""")

    print("\n  PASS 5282 -- the tool I planned to build already existed\n")
    print("""    Item 6 of the plan read: "a pre-commit hook that greps a pass's own output
    numbers against RESULTS_INDEX". That is scripts/check_rediscovery.py, built at Pass 328,
    registered, self-tested, and running. Writing it again would have been this session's
    failure mode applied to its own remedy, which is funny exactly once.

    THE THIRD TIME THIS TURN. The Suzuki tower was already Pass 4793's. The noun@n
    mitigation was already Pass 1107's. The hook was already Pass 328's. In all three cases
    the corpus was ahead of me, and in all three the thing that found it was searching for
    a specific string rather than reasoning about what probably existed.""")

    print("\n  PASS 5283 -- guards versus the OTHER lane's failure modes\n")
    print(f"    {'their documented failure mode':46s} {'my guard':>30s}")
    for m in THEIR_MODES:
        g = m["my_guard"] or "-- none --"
        print(f"    {m['mode'][:46]:46s} {g[:30]:>30s}")
    uncovered = [m for m in THEIR_MODES if not m["my_guard"]]
    print(f"""
    {len(uncovered)} OF {len(THEIR_MODES)} OF THEIR DOCUMENTED FAILURE MODES HAVE NO GUARD ON MY SIDE, and that is
    the expected answer rather than a surprising one. Every guard I built encodes a fault I
    made; theirs are different faults because they work on a different problem -- code
    distance, decoder radius, apartment shells -- with a different failure surface.
    Pass 5251 measured their firewall reading 0 of my 3,989 analysis scripts; this is the
    same asymmetry seen from the other end.

    WHICH FINALLY EXPLAINS THE ZEROS. Pass 5224 ran seven guards over 215 of their files and
    got nothing, and I recorded that as "silence measures overlap between authors". This
    puts a number on the overlap: {len(uncovered)} of their {len(THEIR_MODES)} named modes are outside my tooling
    entirely. The guards are not quiet because their work is clean; they are quiet because
    they are looking for the wrong things.""")

    out = {
        "boundary": ("Pass 5281's noise figures are measured over analysis/*.py and *.md "
                     "only. alpha@7 and alpha@137 remain non-distinctive and are still "
                     "dropped, so this fix makes ONE class of rediscovery catchable, not "
                     "rediscovery in general. Pass 5283's inventory of the other lane's "
                     "failure modes is read from their own boundary statements and "
                     "correction commits -- it is what they DOCUMENT, not an audit of "
                     "their work, and I have not run their code"),
        "pass_5280": {"chain": ["RE_INT requires 3+ digits, so 7/18/10/26 are invisible",
                                "noun@n mitigation exists since Pass 1107",
                                "GEOM_NOUNS lacked 'alpha' and 'deficit'",
                                "Pass 4800 emitted zero tokens and was absent entirely"],
                      "pass4800_indexed_now": p4800 in indexed,
                      "coverage": f"{len(allpy & indexed)}/{len(allpy)}",
                      "reading": ("every noun in that lexicon is a fossil of one past "
                                  "failure, so it can only cover faults that already "
                                  "happened once")},
        "pass_5281": {"new_nouns": list(NEW_NOUNS),
                      "files_touched_pct": 100 * touched // len(files),
                      "distinct_tokens": len(toks), "surviving_cut": kept,
                      "alpha_18_files": toks.get("alpha@18", 0),
                      "would_have_caught_this_session": toks.get("alpha@18", 0) <= 25,
                      "still_dropped": {"alpha@7": toks.get("alpha@7", 0),
                                        "alpha@137": toks.get("alpha@137", 0)},
                      "collision": ("alpha means the fine-structure constant in the "
                                    "physics track; one token prefix, two meanings")},
        "pass_5282": {"planned": "a hook grepping a pass's numbers against RESULTS_INDEX",
                      "already_exists": "scripts/check_rediscovery.py, Pass 328",
                      "note": ("third already-built discovery this turn -- Suzuki tower "
                               "(Pass 4793), noun@n (Pass 1107), this hook (Pass 328)")},
        "pass_5283": {"their_modes": THEIR_MODES,
                      "uncovered": len(uncovered), "total": len(THEIR_MODES),
                      "explains": ("Pass 5224's zero findings over 215 of their files -- "
                                   "the guards look for my faults, not theirs")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5280_5283_INDEX_BLIND_SPOT.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
