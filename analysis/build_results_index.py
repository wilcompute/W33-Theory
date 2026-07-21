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
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "RESULTS_INDEX.md"

# Named objects live in ONE place -- scripts/check_rediscovery.py -- so the index
# and the guard can never drift apart. Pass 348 found them drifted: the guard had
# been taught named objects while the index had not, so `A2` was extracted from a
# staged file and then looked up in an index that had never heard of it. A guard
# and an index that disagree are worse than either alone.
sys.path.insert(0, str(ROOT / "scripts"))
from check_rediscovery import RE_NAMED, RE_ROOT, compounds  # noqa: E402

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
]

# Above this a token is a topic, not a result.
#
# RE-TUNED at Pass 349, because the Pass 328 calibration that produced 10 was run
# against an index missing two thirds of the corpus (*.py was never globbed). On
# the real 5,815-file corpus, measured flag rate over the 173 pass witnesses:
#
#     MAX   flag rate   [[40,10,4]] survives?
#      10      31%        no   <- the flagship catch is DROPPED
#      20      39%        yes
#      25      39%        yes
#      30      43%        yes
#      60      51%        yes
#
# 25 buys back [[40,10,4]] (18 files) at no extra noise over 20, and stays far
# under the Pass 328 noise line (>90% = a guard nobody reads).
#
# THE INDEX HAS A HALF-LIFE, and this is what it looks like. [[40,10,4]] lived in
# 4 files when the index was built and lives in 18 now; [40,15,8] lives in 29 and
# is a topic at any usable cut. A result the corpus works ON becomes a topic OF
# the corpus -- so the index loses the power to flag a result exactly as that
# result becomes central. The cut must be re-measured as the corpus grows; it is
# not a constant.
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
SKIP_DIRS = {".git", "node_modules", ".venv", "data"}

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
    for p in files:
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(ROOT).as_posix()
        for rx in (RE_CSS, RE_LIN, RE_SEQ):
            for m in rx.findall(txt):
                index[norm(m)].add(rel)
        # A pinned result may deliberately fall outside the generic token
        # grammars (for example a four-orbit profile).  Explicit pins are the
        # small, reviewed exception to the noise-calibrated extractors.
        compact = norm(txt)
        for pinned in PINNED_RESULTS:
            if pinned in compact:
                index[pinned].add(rel)
        for m in RE_INT.findall(txt):
            integer = canonical_integer(m)
            if integer not in NOISE:
                index[integer].add(rel)
        # results-as-NAMES (Pass 348) -- same lexicon the guard uses
        for m in RE_NAMED.findall(txt):
            index[m.lower()].add(rel)
        for m in RE_ROOT.findall(txt):
            index[m].add(rel)
        # compounds (Pass 349): a pair of topics is a result
        for c in compounds(txt):
            index[c].add(rel)

    kept = {
        t: fs
        for t, fs in index.items()
        if 1 <= len(fs) <= MAX_FILES or t in PINNED_RESULTS
    }
    uniq = {t: fs for t, fs in kept.items() if len(fs) == 1}

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
        hits = kept.get(probe) or index.get(probe) or set()
        tag = "" if probe in kept else "  (non-distinctive: >%d files)" % MAX_FILES
        print(f"  probe {probe:12s} -> {len(hits)} files{tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
