#!/usr/bin/env python3
"""Full-corpus rediscovery sweep -- the merge list the per-commit guard cannot produce.

scripts/check_rediscovery.py is a PRE-COMMIT hook: it sees only the files being
staged, warns, and never blocks.  That is right for a hook and useless for the
question "how much of the corpus is already duplicated?"  Pass 328 answered that
once by hand (21% of 173 pass files asserted a code parameter existing elsewhere,
uncited).  This script answers it continuously, over everything, and emits the
artifact the hook cannot: a RANKED MERGE LIST.

It reuses the guard's own extraction so the two cannot drift apart -- same
tokeniser, same index, same "already cites the prior file" suppression.

Output (data/rediscovery_sweep.json + a printed summary):

  * per-file collision counts       -- which files are most likely rediscoveries
  * per-token duplication            -- which RESULTS are asserted in the most
                                        mutually-unciting places
  * the merge list                   -- token -> the files that assert it while
                                        citing none of the others

A row in the merge list is a CANDIDATE, not a verdict; the same integer recurs
legitimately.  Its value is that it is finite and rankable, so the corpus can be
de-duplicated top-down instead of one accidental collision at a time.

KNOWN CONFOUND, stated rather than hidden: the PER-FILE ranking is dominated by
synthesis documents (master_synthesis_v*, THE_SELECTION_LAYER.md, refinement
bridges), which legitimately name many results at once and so collide with
everything.  A high per-file count is evidence of breadth, not of rediscovery.
The PER-RESULT ranking is the actionable one -- it asks "how many files assert
this same result while citing none of the others", which is the question Pass 328
measured by hand.
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_rediscovery as guard  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "rediscovery_sweep.json"


def watched_files() -> list[Path]:
    out: list[Path] = []
    for w in guard.WATCHED:
        d = ROOT / w
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and p.suffix in {".py", ".md", ".g", ".tex", ".json"}:
                out.append(p)
    return out


def main() -> int:
    index = guard.load_index()
    if not index:
        print("[sweep] RESULTS_INDEX.md missing or empty; "
              "run: py -3 analysis/build_results_index.py")
        return 1

    files = watched_files()
    per_file: Counter[str] = Counter()
    per_token: Counter[str] = Counter()
    merge: dict[str, set[str]] = defaultdict(set)
    scanned = 0

    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        try:
            txt = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        scanned += 1
        for tok in guard.results_in(txt):
            prior = [x for x in index.get(tok, []) if x != rel]
            # same suppression as the hook: a file that names the prior art is fine
            prior = [x for x in prior if Path(x).name not in txt]
            if prior:
                per_file[rel] += 1
                per_token[tok] += 1
                merge[tok].add(rel)
                merge[tok].update(prior)

    colliding = len(per_file)
    pct = (100.0 * colliding / scanned) if scanned else 0.0

    # rank the merge list by how many mutually-unciting files share the token
    ranked = sorted(
        ({"result": t, "files": sorted(f)} for t, f in merge.items() if len(f) > 1),
        key=lambda r: (-len(r["files"]), r["result"]),
    )

    payload = {
        "schema": "w33.rediscovery_sweep.v1",
        "scanned_files": scanned,
        "files_with_uncited_collisions": colliding,
        "percent_colliding": round(pct, 1),
        "top_files": [{"file": f, "collisions": n} for f, n in per_file.most_common(30)],
        "top_results": [{"result": t, "uncited_files": n}
                        for t, n in per_token.most_common(30)],
        "merge_list_size": len(ranked),
        "merge_list": ranked[:200],
        "reading": (
            "A row is a CANDIDATE, not a verdict: the same integer recurs "
            "legitimately. The value of the list is that it is finite and ranked, "
            "so the corpus can be de-duplicated top-down rather than one "
            "accidental collision at a time."
        ),
    }
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")

    print(f"scanned                {scanned}")
    print(f"with uncited collisions {colliding}  ({pct:.1f}%)")
    print(f"merge-list rows         {len(ranked)}")
    print("\ntop colliding files:")
    for f, n in per_file.most_common(12):
        print(f"  {n:4d}  {f}")
    print("\nmost duplicated results:")
    for t, n in per_token.most_common(12):
        print(f"  {n:4d}  {t}")
    print(f"\nwrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
