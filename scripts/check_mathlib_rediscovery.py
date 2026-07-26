#!/usr/bin/env python3
"""Warn when a local Lean declaration duplicates one that already exists in mathlib.

WHY.  scripts/check_rediscovery.py measures duplication WITHIN this corpus and puts
it at 22.9%.  It is structurally blind to the other direction: a local lemma that
re-proves something mathlib already has.  That blindness is not hypothetical --

    formal/W33/Pass491HermitianRealDet.lean hand-proved

        (Mᴴ).det = star M.det

    via `Matrix.det_transpose_eq_det_map`, a constant that no longer exists, while
    mathlib has had

        Matrix.det_conjTranspose : det Mᴴ = star (det M)      [@[simp]]

    with exactly that statement AND the very proof the file was reconstructing.
    The module had been failing for a long time; the fix was to delete the proof.

So the same failure the corpus measures at scale was sitting inside the
formalization layer, pointed at mathlib instead of at this repository, where no
guard was looking.

WHAT IT DOES.  For every `theorem`/`lemma` in formal/W33/, it takes the declaration
NAME and looks for a mathlib declaration whose name matches on the distinctive part
(the last dotted component, normalised).  Name collision is a weak signal on its
own, so it is reported as a candidate to READ, never as a verdict -- identical to
the in-corpus guard's contract, and for the same reason: a guard that blocks trains
people to bypass it.

WHAT IT DOES NOT DO.  It does not compare statements up to defeq; that needs a Lean
environment query, not a text scan, and would be the right next version.  A local
lemma may legitimately restate an upstream one as a named alias -- Pass491 now does
exactly that, deliberately -- so a hit is a prompt to check, not a defect.

Usage:
    py -3 scripts/check_mathlib_rediscovery.py           # scan formal/W33
    py -3 scripts/check_mathlib_rediscovery.py <files>   # scan specific files
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W33 = ROOT / "formal" / "W33"
MATHLIB = ROOT / "formal" / ".lake" / "packages" / "mathlib" / "Mathlib"

DECL = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:protected\s+|private\s+|noncomputable\s+)*"
                  r"(?:theorem|lemma)\s+([A-Za-z_][A-Za-z0-9_.']*)", re.M)

# Names too generic for a collision to mean anything.
NOISE = {"main", "aux", "step", "key", "core", "this", "eq", "def"}


def normalise(name: str) -> str:
    """Distinctive part of a declaration name, lowercased, underscores dropped."""
    tail = name.split(".")[-1]
    return tail.replace("_", "").lower()


def mathlib_index() -> dict[str, list[str]]:
    idx: dict[str, list[str]] = defaultdict(list)
    if not MATHLIB.is_dir():
        return idx
    for p in MATHLIB.rglob("*.lean"):
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(ROOT).as_posix()
        for m in DECL.finditer(txt):
            idx[normalise(m.group(1))].append(f"{m.group(1)}  ({rel})")
    return idx


def main(argv: list[str]) -> int:
    idx = mathlib_index()
    if not idx:
        print("[mathlib guard] mathlib sources not found under formal/.lake; nothing to compare")
        return 0

    files = [Path(a) for a in argv if not a.startswith("-")] or sorted(W33.glob("*.lean"))
    hits = 0
    for p in files:
        if not p.exists():
            continue
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix()
        for m in DECL.finditer(txt):
            local = m.group(1)
            key = normalise(local)
            if key in NOISE or len(key) < 8:
                continue
            # PREFIX match, not exact.  The motivating case is
            #   local   det_conjTranspose_eq_star_det -> detconjtransposeeqstardet
            #   mathlib det_conjTranspose             -> detconjtranspose
            # which are not equal.  An exact-match guard would have missed the very
            # example it exists for, so it matches when one normalised name is a
            # prefix of the other and the shared part is long enough to mean something.
            prior = list(idx.get(key, []))
            if not prior:
                for mk, entries in idx.items():
                    if len(mk) < 12:
                        continue
                    if key.startswith(mk) or mk.startswith(key):
                        prior.extend(entries)
                        if len(prior) >= 4:
                            break
            if not prior:
                continue
            # already citing it is fine -- same suppression as the in-corpus guard
            if any(q.split("  ")[0] in txt for q in prior):
                continue
            if hits == 0:
                print("\n" + "=" * 72)
                print("[mathlib guard] local declarations whose name already exists upstream")
                print("=" * 72)
            hits += 1
            print(f"  {rel}")
            print(f"    {local}")
            for q in prior[:2]:
                print(f"      -> mathlib: {q}")

    if hits:
        print("\n  CANDIDATES, not verdicts -- a name collision is a weak signal, and a")
        print("  local alias for an upstream lemma is legitimate (Pass491 is one, on")
        print("  purpose). But Pass491 also shows the expensive version: a hand proof")
        print("  of Matrix.det_conjTranspose, broken for months against a renamed")
        print("  constant, when deleting it was the fix. Open the mathlib file first.\n")
    else:
        print("[mathlib guard] no local declaration names collide with mathlib")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
