#!/usr/bin/env python3
"""Build RESULTS_INDEX.md -- an inverted index from RESULT to file.

WHY THIS EXISTS. Pass 322 found that ~15 passes re-derived a rank law the repo
had already proved, formalized in Lean, and cited to the literature. Pass 323
found the same for the CSS code. In both cases the searches WERE run and failed,
because this corpus is named by DATE (analysis/2026-07-10_levi_next5.md), not by
topic: "levi"/"next5" carry no rank signal, so no topic-grep can find the proof.

The fix cannot be "remember to search better" -- that was already in the standing
instructions, and it still failed twice. The fix has to be structural: an index
keyed by the one thing a rediscovery always shares with its original -- THE
RESULT ITSELF. A formula, a distinctive integer, a code parameter, a sequence.
Those are identical in both, whatever the file is called.

WHAT IT INDEXES.
  * code parameters   [[40,10,4]], [40,15,8]
  * distinctive integers  >= 3 digits (51840, 25920, 196883, 8353, ...)
  * explicit sequences    25/91/225, 10/50/298
Tokens appearing in more than MAX_FILES files are dropped as non-distinctive
(they identify a topic, not a result). Tokens in exactly one file are the
sharpest signal: they are unique claims.

HOW TO USE IT. Before claiming any result is new:
    grep "<your number or formula>" RESULTS_INDEX.md
If it hits, read those files END TO END (Pass 286: shallow reads caused two
retractions) before writing anything.

Regenerate with:  py -3 analysis/build_results_index.py
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "RESULTS_INDEX.md"

# Named objects live in ONE place -- scripts/check_rediscovery.py -- so the index
# and the guard can never drift apart. Pass 348 found them drifted: the guard had
# been taught named objects while the index had not, so `A2` was extracted from a
# staged file and then looked up in an index that had never heard of it. A guard
# and an index that disagree are worse than either alone.
sys.path.insert(0, str(ROOT / "scripts"))
from check_rediscovery import (  # noqa: E402
    RE_NAMED, RE_ROOT, compounds, noun_number_pairs)

# corpus: the places results actually live (Pass 322 learned analysis/*.md and
# AUDIT_*.md the hard way -- they were NOT in the old "index.html + .tex" rule).
#
# Pass 349 found the far bigger hole: *.py was NEVER indexed. The index covered
# 1,311 files while 2,299 analysis/*.py sat outside it -- roughly two thirds of
# the corpus, including all 173 w33_pass*.py witnesses AND
# w33_eisenstein_grand_synthesis.py, the very file Pass 347 rediscovered. The
# index could not have caught that rediscovery by any token, because it had never
# read the file. Pass 348 blamed the token classes ("A2 is a ubiquitous atom") and
# was looking at the wrong layer: the corpus definition was wrong. Witnesses ARE
# results; a tool that indexes only prose indexes only the write-up.
GLOBS = [
    "docs/index.html",
    "*.tex",
    "analysis/*.md",
    "analysis/*.py",
    "analysis/*.g",
    "passes/*.md",
    "passes/*.py",
    "passes/*.g",
    "exploration/*.py",
    "exploration/*.g",
    "scripts/*.py",
    "scripts/*.g",
    "PASS*.md",
    "AUDIT*.md",
    "BT*.md",
    "PART*.md",
    "formal/**/*.lean",
    "manuscripts/**/*.tex",
    # BUNDLE DIRECTORIES (Pass 5524).  This repository has ~158 top-level bundle
    # directories -- PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01, SP43_TO_WE6_TRUE_FIXED_BUNDLE,
    # the TOE_* deliverables, V22-V26 outputs -- holding .md reports and .json
    # certificates.  Every glob above reads source or prose in a handful of known
    # subtrees, so a bundle's REPORT.md was invisible to the result index while being
    # exactly the kind of file it exists to surface.  SP43_TO_WE6's REPORT.md carries an
    # explicit Sp(4,3) -> W(E6) isomorphism and was unindexed for months.
    #
    # .md only, deliberately.  The bundles also hold thousands of .json certificates and
    # 250 .zip archives; JSON is machine output whose numbers would flood the token
    # grammar, and Pass 328 measured what that costs.  Prose reports are the half a human
    # wrote and the half worth indexing.
    "*_BUNDLE*/**/*.md",
    "*_bundle*/**/*.md",
    "*_deliverable*/**/*.md",
    "V2*_output*/**/*.md",
    "NOTES/*.md",
]

# Above this a token is a topic, not a result.
#
# RE-MEASURED at Pass 1073 with `py -3 scripts/calibrate_index_cut.py`, because
# the previous calibration table here was VOID: it was run against a corpus that
# globbed `formal/.lake/packages/`, so most of the files it counted were mathlib.
# On the corrected 6,530-file corpus, over all 676 pass witnesses, using the
# GUARD's token grammar (not this file's -- they differ deliberately) and honouring
# the guard's "already cites the prior art" suppression:
#
#     MAX   kept   flag rate   code probes surviving
#      10   4871      24.1%     3/6   <- loses 8353 (11 files)
#      15   5282      28.8%     4/6
#      20   5556      29.7%     4/6
#      25   5692      30.9%     4/6   <- current
#      30   5797      31.4%     4/6
#      60   5979      35.9%     4/6
#     100   6054      39.5%     4/6
#
# THE CURVE IS FLAT.  There is no cliff between 15 and 60 -- seven points of flag
# rate and no change at all in which probes survive.  The cut is simply not a
# sensitive parameter any more, and 25 is kept because nothing argues for moving
# it, not because it was found to be optimal.  Everything is far under the Pass 328
# noise line (>90% = a guard nobody reads).
#
# THE HALF-LIFE HAS FULLY RUN for the code parameters, which is the finding that
# actually matters.  [[40,10,4]] lived in 4 files when the index was built, 18 at
# Pass 349, and 34 now; [[240,81,3]] is in 60.  Every code-parameter probe now
# exceeds the cut at ANY usable value, so they survive purely because they are
# PINNED below.  The cut no longer protects the index's flagship catches -- the pin
# set does.  When a new central code object appears, pinning it is not an optional
# tidy-up; it is the only thing that keeps it searchable.
MAX_FILES = 25
# The half-life is now observable, not hypothetical: after the July 15 batch,
# [[40,10,4]] moved from 18 to 27 files and fell just beyond MAX_FILES.  These
# central code objects must remain searchable even after becoming topics.  A
# tiny explicit pin set preserves the index's purpose without raising the noise
# ceiling for every token.
PINNED_RESULTS = {
    "[[40,10,4]]",
    "[40,15,8]",
    "[[240,81,3]]",
    "[240,81,3]",
    "[240,120,3]",
    "[12960,12960,12960,12960]",
    "32/8/4/2/1/1/2/4",
    "360/48/24/12/12/5/10/16x3",
    "48/16x3/16!3^16/2/14+2",
    "192/64x3/960/geometry-boundary",
    "48/6/2/14!3^14/minimal-phase-lift",
    "16/48/2+14/external-binding-abi",
    "48-cycle/16xC3/LOAD-FLIP-LATCH/reversible-logic-switch",  # pragma: allowlist secret
    "96/16xC6/C6-vs-S3-control-boundary",
    "234360/540/90+360+90/6/22of48/0exact/S6-direction",
    "48/16/8/8/16/96/1/46080/1/2/orbit-anchor",
    "228100045392509153077600971330057241",
    "2051277771273019233341050472890368",
    "2028949923625",
    "16231599389",
    # Pass 541: these formulas are structurally distinctive but fall outside
    # the generic number/code/sequence token grammars.  Pins keep the infinite
    # q=3 theorem and its exact agreement locus searchable by result.
    "2(m+[modd])",
    "s_3(m)+[modd]=2",
    "m=3^i+3^j",
}
# `.lake` / `lake-packages` hold MATHLIB, not this corpus.
#
# MEASURED at Pass 1073, and this was never a perf bug alone. `formal/**/*.lean`
# reaches into `formal/.lake/packages/`, so the index was reading 9,369 mathlib and
# batteries source files -- 59% of the 15,890 it globbed. Consequences, both real:
#
#   * 1,146 of 6,723 index rows (17%) cited a mathlib file, and 889 of them cited
#     NOTHING ELSE. Those are the "appears in exactly one file -- the sharpest
#     signal" rows, and they were doctest literals: `[123,543,1000]` out of
#     Mathlib/Data/List/Destutter.lean, `[1,50,100]` out of a Batteries test.
#   * worse, it poisons the CUT. MAX_FILES drops a token as "a topic" once it
#     exceeds 25 files. Mathlib files counted toward that ceiling, so a result
#     genuinely unique to this repo could be pushed over it by unrelated third-party
#     code and silently vanish from the guard -- the exact failure the index exists
#     to prevent, produced by the index itself.
#
# A dependency's source is not a prior claim of this project. Skip it.
SKIP_DIRS = {".git", "node_modules", ".venv", "data", ".lake", "lake-packages"}

RE_CSS = re.compile(r"\[\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]\]")
RE_LIN = re.compile(r"\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]")
# Accept machine, prose, and TeX spellings of the same result.  Pass 358 found
# that `35,697,025` disappeared while `35697025` was searchable; Pass 360 then
# exposed the same blind spot for TeX's `1{,}285{,}608`.  Keep up to nine digits
# and canonicalize both grouping forms before indexing.
RE_INT = re.compile(
    r"(?<![\d.\-])(\d{1,3}(?:(?:,|\{,\})\d{3}){1,2}|\d{3,9})(?!\d)(?!\.\d)"
)
RE_SEQ = re.compile(r"\b\d+(?:/\d+){2,}\b")

# integers that are noise: years, common dimensions, section numbers
NOISE = {str(y) for y in range(1900, 2100)} | {
    "100",
    "1000",
    "200",
    "300",
    "400",
    "500",
    "600",
    "700",
    "800",
    "900",
    "128",
    "256",
    "512",
    "1024",
    "2048",
    "4096",
}


def norm(tok: str) -> str:
    return re.sub(r"\s+", "", tok)


def canonical_integer(tok: str) -> str:
    return tok.replace("{,}", "").replace(",", "")


def main():
    files = []
    for g in GLOBS:
        for p in ROOT.glob(g):
            if p.is_file() and not any(d in p.parts for d in SKIP_DIRS):
                files.append(p)
    files = sorted(set(files))

    index: dict[str, set[str]] = defaultdict(set)

    # Bound the memory. A token in >MAX_FILES files is dropped below anyway, so
    # accumulating its full file list only to discard it is pure waste -- and with
    # compound tokens (a pair of atoms, so quadratically many per file) it was the
    # source of the MemoryError that left this index stale across ~12 passes.
    # Storing MAX_FILES+1 is enough to decide the cut exactly; pinned tokens keep
    # their full list because their file lists are printed.
    #
    # `counts` holds the TRUE per-token file count regardless of the cap. Without
    # it the diagnostic line would report the cap and read as a real measurement --
    # "51840 -> 26 files" when the truth is 200. A tool that silently reports its
    # own truncation as data is worse than one that reports nothing.
    cap = MAX_FILES + 1
    counts: Counter[str] = Counter()

    def add(tok: str, rel: str) -> None:
        fs = index[tok]
        if len(fs) < cap or tok in PINNED_RESULTS:
            fs.add(rel)

    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(ROOT).as_posix()
        # Gather this file's tokens ONCE, deduplicated, so `counts` is a true
        # file count and not a count of textual occurrences.
        toks: set[str] = set()
        for rx in (RE_CSS, RE_LIN, RE_SEQ):
            toks.update(norm(m) for m in rx.findall(txt))
        # A pinned result may deliberately fall outside the generic token
        # grammars (for example a four-orbit profile).  Explicit pins are the
        # small, reviewed exception to the noise-calibrated extractors.
        compact = norm(txt)
        toks.update(q for q in PINNED_RESULTS if q in compact)
        for m in RE_INT.findall(txt):
            integer = canonical_integer(m)
            if integer not in NOISE:
                toks.add(integer)
        # results-as-NAMES (Pass 348) -- same lexicon the guard uses
        toks.update(m.lower() for m in RE_NAMED.findall(txt))
        toks.update(RE_ROOT.findall(txt))
        # compounds (Pass 349): a pair of topics is a result
        toks.update(compounds(txt))
        # noun-number pairs (Pass 1107): 1-2 digit integers are invisible to
        # RE_INT, so a result like "maximum partial ovoid is 7" was unindexable.
        toks.update(noun_number_pairs(txt))

        counts.update(toks)
        for t in toks:
            add(t, rel)

    # Decide the cut on the TRUE count, not on the (capped) stored list.
    kept = {
        t: fs
        for t, fs in index.items()
        if 1 <= counts[t] <= MAX_FILES or t in PINNED_RESULTS
    }
    uniq = {t: fs for t, fs in kept.items() if counts[t] == 1}

    def sort_key(t):
        return (
            (
                0
                if t.startswith("[[")
                else 1 if t.startswith("[") else 2 if "/" in t else 3
            ),
            -len(t),
            t,
        )

    lines = [
        "# RESULTS INDEX — search for the RESULT, not the topic",
        "",
        "*Machine-generated by `analysis/build_results_index.py`. Regenerate after",
        "adding results. Do not hand-edit.*",
        "",
        "## Why this file exists",
        "",
        "This corpus is named by **date**, not by subject — `analysis/2026-07-10_levi_next5.md`",
        "holds a **proved rank law** that no grep for `rank` can find. Pass 322 lost ~15",
        "passes rediscovering it; Pass 323 found the same for `[[40,10,4]]`. Both times the",
        "searches ran and failed. A rediscovery always shares one thing with its original:",
        "**the result itself**. So this indexes results, not topics.",
        "",
        "## How to use it",
        "",
        "**Before claiming anything is new**, grep this file for your number, code",
        "parameter, or sequence. If it hits, read those files *end to end* (Pass 286:",
        "shallow reads caused two retractions) before writing.",
        "This is a presence index, not an endorsement ledger: a hit may be a proof,",
        "a reuse, an obstruction, or an explicit retraction.",
        "When two files state the same result in different language, consult the",
        "human-curated [RESULTS VOCABULARY](RESULTS_VOCABULARY.md) for semantic",
        "aliases, current status, supersessions, and primary artifacts.",
        "",
        f"Indexed **{len(files)}** files; **{len(kept)}** distinctive results",
        f"(a token in >{MAX_FILES} files identifies a topic and is dropped unless explicitly pinned).",
        f"**{len(uniq)}** appear in exactly one file — the sharpest signal.",
        "",
        "## Index",
        "",
        "| result | files |",
        "|---|---|",
    ]
    for t in sorted(kept, key=sort_key):
        fs = sorted(kept[t])
        cell = " · ".join(f"`{f}`" for f in fs[:4])
        if len(fs) > 4:
            cell += f" · *(+{len(fs)-4})*"
        lines.append(f"| `{t}` | {cell} |")
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  files indexed : {len(files)}")
    print(f"  distinctive   : {len(kept)}")
    print(f"  unique (1 file): {len(uniq)}")
    for probe in ("[[40,10,4]]", "[40,15,8]", "51840", "8353", "25920", "196883"):
        n = counts[probe]
        tag = "" if probe in kept else "  (non-distinctive: >%d files)" % MAX_FILES
        print(f"  probe {probe:12s} -> {n} files{tag}")
    # Regression guard for the Pass 1073 defect: a dependency tree must never be
    # indexed as this project's prior art again.
    dep = [p for p in files if ".lake" in p.parts or "lake-packages" in p.parts]
    if dep:
        print(f"  WARNING: {len(dep)} dependency files were indexed as corpus "
              f"(e.g. {dep[0].relative_to(ROOT).as_posix()}) -- check SKIP_DIRS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
