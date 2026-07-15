#!/usr/bin/env python3
"""Pre-commit guard against REDISCOVERY (failure mode 5).

WHY THIS IS A HOOK AND NOT A NOTE. "Search the corpus before claiming anything
new" was already in the standing instructions and in the agent memory. It failed
twice anyway, at a cost of ~19 passes: the rank law (Pass 322) and the CSS code
(Pass 323) were both re-derived while already proved in-repo AND published. An
instruction that has failed twice is not an instruction, it is a wish. So this
runs at commit time, where it cannot be skipped by forgetting.

WHAT IT DOES. For each staged pass/analysis file, it extracts the RESULTS the
file asserts -- distinctive integers, code parameters [[n,k,d]] / [n,k,d], and
slash-sequences -- and looks them up in RESULTS_INDEX.md. If a result already
appears in files the staged file does not cite, it WARNS with the prior locations.

WHY IT WARNS AND DOES NOT BLOCK. A collision is not proof of rediscovery -- the
same integer legitimately recurs (51840 is the group order; every pass may name
it). Blocking would train people to pass --no-verify, which is worse than no
hook. The hook's job is to put the prior file in front of your eyes at the moment
you would otherwise not look. Reading it is still yours.

Usage:
    py -3 scripts/check_rediscovery.py <files...>      # pre-commit passes these
    py -3 scripts/check_rediscovery.py --all           # sweep everything staged
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "RESULTS_INDEX.md"

RE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|$")
RE_FILE = re.compile(r"`([^`]+)`")
RE_CSS = re.compile(r"\[\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]\]")
RE_LIN = re.compile(r"\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]")
RE_INT = re.compile(r"(?<![\d.\-])(\d{3,7})(?![\d.])")
RE_SEQ = re.compile(r"\b\d+(?:/\d+){2,}\b")

# NAMED OBJECTS -- added at Pass 348, which found the blind spot the hard way.
# The guard extracted ZERO tokens from Pass 347, whose rediscovered claim was
# "A2 = the q=3 hexagonal lattice = the GKP base" (already in
# w33_eisenstein_grand_synthesis.py, FACE 4). A2 is not a code parameter, not a
# distinctive integer, not a sequence -- so a numbers-only guard is structurally
# blind to it. Results-as-NAMES rediscover exactly as easily as results-as-NUMBERS.
#
# Kept to a hand-curated lexicon of load-bearing objects, NOT open-ended
# capitalized-word extraction: the Pass 328 calibration showed that a guard which
# flags everything is a guard nobody reads. Each entry is an object this repo
# builds theories ON, so a collision is worth forty seconds of a human's time.
NAMED = [
    "Witting polytope", "GKP tower", "GKP code tower", "Heawood", "doily",
    "Csaszar", "Szilassi", "Barnes-Wall", "Leech", "Golay", "tetracode",
    "Eisenstein tower", "Shephard-Todd", "Weil representation", "Weil module",
    "Smith group", "critical group", "Baer subgeometry", "Singer cycle",
    "extraspecial", "trinification", "Hesse", "Steiner system", "Levi graph",
]
RE_NAMED = re.compile("|".join(re.escape(n) for n in NAMED), re.IGNORECASE)
# lattice/root-system names need word boundaries or they match everything
RE_ROOT = re.compile(r"\b(A2|D4|E6|E7|E8|F4|G2|A_2|D_4|E_6|E_8)\b")

# ---------------------------------------------------------------------------
# COMPOUNDS (Pass 349). Pass 348 measured a floor and called it the floor: the
# rediscovery in Pass 347 collided on "A2", which lives in 169 files and is
# therefore a TOPIC, dropped by the >10-file cut. Named objects alone rescued
# only 4 of 28 tokens.
#
# The floor lifts. Measured over 3,555 files: single atoms are usable (<=10
# files) 24% of the time; CO-OCCURRING PAIRS are usable 80% of the time. And the
# decisive case works -- ('a2','eisenstein') appears in exactly 9 files, so the
# ORIGINAL Pass 347 (recovered from git at 39b09db30, before its citation was
# added) WOULD have been flagged against w33_eisenstein_grand_synthesis.py.
#
# The principle: A PAIR OF TOPICS IS A RESULT. "A2" is what the corpus is about;
# "Eisenstein" is what the corpus is about; "A2 AND Eisenstein in one file" is a
# specific claim someone made. Atoms name the subject, compounds name the work.
ATOMS = [
    "Eisenstein", "Witting", "GKP", "Heawood", "doily", "Csaszar", "Szilassi",
    "Leech", "Golay", "tetracode", "hexagonal", "qutrit", "Weil", "Baer",
    "Singer", "extraspecial", "trinification", "Hesse", "Steiner", "Levi",
    "Smith group", "Barnes-Wall", "Shephard-Todd", "moonshine", "Monster",
    "Koide", "PMNS", "Cabibbo", "tomotope", "Clifford", "Bockstein", "torsor",
]
RE_ATOM = re.compile(r"\b(?:" + "|".join(re.escape(a) for a in ATOMS) + r")\b",
                     re.IGNORECASE)


def compounds(text: str) -> set[str]:
    """Co-occurring pairs of central objects, as sorted 'x+y' tokens."""
    from itertools import combinations
    found = {m.lower() for m in RE_ATOM.findall(text)}
    found |= {m.lower() for m in RE_ROOT.findall(text)}
    return {f"{x}+{y}" for x, y in combinations(sorted(found), 2)}

NOISE = {str(y) for y in range(1900, 2100)} | {
    "100", "1000", "200", "300", "400", "500", "600", "700", "800", "900",
    "128", "256", "512", "1024", "2048", "4096",
}
# results so ubiquitous that a hit carries no signal
SKIP = {"51840", "25920", "196883"}

WATCHED = ("analysis/", "passes/", "exploration/")


def load_index() -> dict[str, list[str]]:
    if not INDEX.exists():
        return {}
    out: dict[str, list[str]] = {}
    for line in INDEX.read_text(encoding="utf-8", errors="ignore").splitlines():
        m = RE_ROW.match(line.strip())
        if m:
            out[re.sub(r"\s+", "", m.group(1))] = RE_FILE.findall(m.group(2))
    return out


def results_in(text: str) -> set[str]:
    """Extract only the token classes that carry SIGNAL.

    CALIBRATED, not guessed. Pass 328 ran this guard over all 172 pass files and
    measured the flag rate per token class:

        everything (incl. bare integers) ...... 97%   <- noise; flags everything
        bare integers, even rare-only ......... 78%   <- still noise
        code parameters [[n,k,d]] / [n,k,d] ... 20%   <- SIGNAL
        slash-sequences ....................... 2%    <- signal, sparse

    A guard that flags 97% of commits is a guard nobody reads -- it fails exactly
    the way the instruction it replaces failed. Bare integers are dropped: the
    same integer legitimately recurs everywhere (a dimension, a count, a group
    order), so its recurrence carries no information. Code parameters are the
    objects a rediscovery actually duplicates, and 20% is a rate a human will
    still look at.
    """
    got: set[str] = set()
    for rx in (RE_CSS, RE_LIN, RE_SEQ):
        got |= {re.sub(r"\s+", "", m) for m in rx.findall(text)}
    # named objects (Pass 348): results-as-NAMES, invisible to the numeric classes
    got |= {m.lower() for m in RE_NAMED.findall(text)}
    got |= {m for m in RE_ROOT.findall(text)}
    # compounds (Pass 349): a pair of topics is a result
    got |= compounds(text)
    return got - SKIP


def main(argv: list[str]) -> int:
    files = [a for a in argv if not a.startswith("-")]
    index = load_index()
    if not index:
        print("[rediscovery] RESULTS_INDEX.md missing or empty; "
              "run: py -3 analysis/build_results_index.py")
        return 0

    hits = 0
    for f in files:
        p = Path(f)
        rel = p.as_posix()
        if not any(w in rel for w in WATCHED) or not p.exists():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for tok in sorted(results_in(txt)):
            prior = [x for x in index.get(tok, []) if x != rel]
            # only warn when the file does NOT already point at the prior art
            prior = [x for x in prior if Path(x).name not in txt]
            if prior:
                if hits == 0:
                    print("\n" + "=" * 72)
                    print("[rediscovery guard] results that already exist elsewhere")
                    print("=" * 72)
                hits += 1
                shown = " ".join(prior[:3]) + (f" (+{len(prior)-3})" if len(prior) > 3 else "")
                print(f"  {rel}")
                print(f"    {tok}  ->  {shown}")

    if hits:
        print("\n  These are CANDIDATES, not verdicts -- the same integer recurs")
        print("  legitimately. But Passes 322/323 lost ~19 passes to exactly this,")
        print("  so: open the prior file and READ it (end to end -- Pass 286 shows")
        print("  shallow reads cause retractions) before asserting novelty.")
        print("  Cite the prior art in the file and this warning goes away.\n")
    return 0        # advisory by design -- see module docstring


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
