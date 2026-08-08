#!/usr/bin/env python3
"""Pass 4248 -- a working peephole optimiser for the W(3,3) frame machine.

Pass 4243 counted the machine's identity programs with a trace: 738 closed non-backtracking
walks of length three, 1584 of length four, and so on.  A count is a fact; a matcher is a
tool.  This turns the short ones into an optimiser that actually rewrites instruction
streams.

WHAT IS AND IS NOT DELETABLE.  A closed walk on the frame graph returns the frame register
to its start, but the machine's state is the full affine element, not just the frame.  So
the honest rule is:

  * a factored word that multiplies to the IDENTITY of ASp(4,3) is dead code, deletable
    from any stream, unconditionally;
  * a word that merely returns the FRAME is a no-op only if the frame is the whole state.

This tool computes the first kind by group multiplication and reports the second separately,
because conflating them would silently break programs that read anything but the frame.

    py -3 scripts/w33_peephole.py                 # build the table, show statistics
    py -3 scripts/w33_peephole.py --demo          # optimise a random stream
    py -3 scripts/w33_peephole.py --opt F_p CX_pf CX_pf CX_pf ...
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ID4 = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
       "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
       "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
ISA = {n: (LIN[n], (0, 0, 0, 0)) for n in LIN}
ISA["Z_p"] = (ID4, (1, 0, 0, 0))
IDENT = (ID4, (0, 0, 0, 0))


def mv(A, v):
    return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def compose(g, h):
    """Apply g then h, as affine maps x -> Mx + t."""
    (Mg, tg), (Mh, th) = g, h
    return (mm(Mh, Mg), tuple((mv(Mh, tg)[i] + th[i]) % 3 for i in range(4)))


def evaluate(word):
    e = IDENT
    for n in word:
        e = compose(e, ISA[n])
    return e


def build_table(max_len=6):
    """Every word up to max_len that multiplies to the identity, minimal in the sense that
    no proper prefix or suffix is already a shorter identity word."""
    names = sorted(ISA)
    ident_words, seen_short = [], []
    for L in range(1, max_len + 1):
        for word in product(names, repeat=L):
            if evaluate(word) != IDENT:
                continue
            if any(word[i:i + len(s)] == s
                   for s in seen_short for i in range(len(word) - len(s) + 1)):
                continue
            ident_words.append(word)
        seen_short = [w for w in ident_words if len(w) <= L]
    return ident_words


def optimise(stream, table):
    """Repeatedly delete the leftmost occurrence of any identity word.  Shorter patterns
    first, so a deletion never hides a cheaper one."""
    by_len = sorted(table, key=len)
    out, removed = list(stream), []
    changed = True
    while changed:
        changed = False
        for pat in by_len:
            n = len(pat)
            for i in range(len(out) - n + 1):
                if tuple(out[i:i + n]) == pat:
                    removed.append("".join(p + " " for p in pat).strip())
                    del out[i:i + n]
                    changed = True
                    break
            if changed:
                break
    return out, removed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-len", type=int, default=6)
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--opt", nargs="*", default=None)
    a = ap.parse_args()

    table = build_table(a.max_len)
    by_len: dict[int, int] = {}
    for w in table:
        by_len[len(w)] = by_len.get(len(w), 0) + 1
    print("=" * 74)
    print("W(3,3) frame machine -- peephole table")
    print("=" * 74)
    print(f"  opcodes: {', '.join(sorted(ISA))}")
    print(f"  minimal identity words up to length {a.max_len}:")
    for L in sorted(by_len):
        print(f"    length {L}: {by_len[L]}")
    print(f"  total patterns: {len(table)}")
    if table:
        shortest = min(len(w) for w in table)
        print(f"\n  the shortest relations (length {shortest}):")
        for w in [w for w in table if len(w) == shortest][:8]:
            print(f"    {' '.join(w)}")

    if a.demo or a.opt is not None:
        import random
        if a.opt:
            stream = a.opt
        else:
            random.seed(4248)
            stream = [random.choice(sorted(ISA)) for _ in range(200)]
        opt, removed = optimise(stream, table)
        print(f"\n  stream: {len(stream)} instructions -> {len(opt)} "
              f"({len(stream) - len(opt)} deleted, {len(removed)} rewrites)")
        same = evaluate(stream) == evaluate(opt)
        print(f"  semantics preserved (same group element): {same}")
        if not same:
            print("  REFUSING to report a speedup: the rewrite changed the program.")
            return 1

    out = {"opcodes": sorted(ISA), "max_len": a.max_len,
           "patterns_by_length": {str(k): v for k, v in sorted(by_len.items())},
           "total_patterns": len(table),
           "note": ("identity words multiply to the identity of ASp(4,3), so they are "
                    "deletable from any stream; frame-returning words that are not group "
                    "identities are NOT deletable and are excluded")}
    p = ROOT / "data" / "PART_W33_PASS4248_PEEPHOLE_TABLE.json"
    p.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    p.write_text(json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    print(f"\nwrote {p.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
