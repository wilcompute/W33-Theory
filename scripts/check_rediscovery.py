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
    got: set[str] = set()
    for rx in (RE_CSS, RE_LIN, RE_SEQ):
        got |= {re.sub(r"\s+", "", m) for m in rx.findall(text)}
    got |= {m for m in RE_INT.findall(text) if m not in NOISE}
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
