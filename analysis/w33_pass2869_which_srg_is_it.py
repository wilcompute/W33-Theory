#!/usr/bin/env python3
"""Pass 2869 -- CORRECTION: proving the ray configuration is W(3,3) and not a lookalike.

Pass 2835 computed the orthogonality graph of the 36 magic rays plus the four coordinate
axes, found SRG(40,12,2,4), and concluded "this IS the W(3,3) collinearity graph".

That inference is not valid, and `docs/index.html` says so explicitly in its Theory
section, in a sentence I had not read:

    "The parameter tuple does not identify W(3,3): Spence classified exactly 28
     nonisomorphic SRG(40,12,2,4) graphs.  The object here is fixed by the displayed
     symplectic construction."

So SRG(40,12,2,4) leaves 28 candidates.  Two of them are generalised quadrangles of order
(3,3): W(3,3) and its dual Q(4,3), which are non-isomorphic for odd q.  Establishing the
Pass 2835 claim therefore needs two more steps, both cheap and both exact:

  1. THE GQ AXIOM, over every line and every point off it -- not just over the one line I
     happened to delete.  This cuts 28 candidates down to 2.
  2. A SPREAD.  W(3,q) always has one; Q(4,q) has a spread only for even q.  At q = 3 a
     spread exists in W(3,3) and does not exist in Q(4,3), so finding ten pairwise
     disjoint lines covering all forty points settles which of the two this is.

The headline result survives -- but it was published one inference short, and the missing
inference was sitting in the project's own encyclopedia.  That is the fifth time this
session, and the first found by reading a section end to end rather than grepping it.

    py -3 analysis/w33_pass2869_which_srg_is_it.py
"""

from __future__ import annotations

import json
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)


def build_forty():
    w = [1, W, W ** 2]
    raw = []
    for mu, nu in product(range(3), repeat=2):
        raw.append([0, 1, -w[mu], w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, 0, -w[mu], -w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, -w[mu], 0, w[nu]])
    for mu, nu in product(range(3), repeat=2):
        raw.append([1, w[mu], w[nu], 0])
    rays = [np.array(r, dtype=complex) / np.linalg.norm(r) for r in raw]
    axes = [np.eye(4, dtype=complex)[i] for i in range(4)]
    return rays + axes


def main() -> int:
    pts = build_forty()
    R = np.array(pts)
    adj = (np.abs(R.conj() @ R.T) ** 2) < 1e-9
    np.fill_diagonal(adj, False)
    n = len(pts)

    print("=" * 78)
    print("Pass 2869 -- which SRG(40,12,2,4) is this?")
    print("=" * 78)

    # ---- the parameters, restated so the whole chain is in one place ----------
    deg = adj.sum(axis=1)
    lam = {int((adj[i] & adj[j]).sum()) for i in range(n) for j in range(n)
           if i < j and adj[i, j]}
    mu = {int((adj[i] & adj[j]).sum()) for i in range(n) for j in range(n)
          if i < j and not adj[i, j]}
    print(f"  SRG parameters: ({n}, {deg[0]}, {lam.pop()}, {mu.pop()})")
    print("  Spence: exactly 28 nonisomorphic graphs share these parameters, so this")
    print("  alone identifies NOTHING.  Two more facts are needed.\n")

    # ---- step 1: the generalised-quadrangle axiom, over EVERY line ------------
    lines = [q for q in combinations(range(n), 4)
             if all(adj[i, j] for i, j in combinations(q, 2))]
    print(f"  lines (4-cliques)                 : {len(lines)}")
    per_point = np.zeros(n, dtype=int)
    for L in lines:
        for p in L:
            per_point[p] += 1
    print(f"  lines through each point          : {sorted(set(per_point.tolist()))}")

    # every edge must lie in exactly one line, or "line" is the wrong word
    edge_lines = {}
    for L in lines:
        for e in combinations(L, 2):
            edge_lines[e] = edge_lines.get(e, 0) + 1
    edge_ok = set(edge_lines.values()) == {1} and len(edge_lines) == int(adj.sum() // 2)
    print(f"  every edge in exactly one line    : {edge_ok}  "
          f"({len(edge_lines)} edges)")

    # THE axiom: for every line L and every point p off L, exactly one point of L is
    # collinear with p.
    worst = set()
    for L in lines:
        Ls = set(L)
        for p in range(n):
            if p in Ls:
                continue
            worst.add(int(sum(adj[p, q] for q in L)))
    gq = worst == {1}
    print(f"  GQ axiom over all {len(lines)} lines x points off them: {sorted(worst)} "
          f"-> {gq}")
    print("  => this is the collinearity graph of a generalised quadrangle of order (3,3).")
    print("     That narrows 28 candidates to exactly TWO: W(3,3) and its dual Q(4,3).\n")

    # ---- step 2: a spread separates W(3,3) from Q(4,3) -----------------------
    # W(3,q) has a spread for every q.  Q(4,q) has a spread only for q even.  At q = 3,
    # finding one settles it.
    print("  searching for a spread: 10 pairwise disjoint lines covering all 40 points")
    line_sets = [frozenset(L) for L in lines]
    spread = []

    def search(covered, start, chosen):
        if len(chosen) == 10:
            return list(chosen)
        for i in range(start, len(line_sets)):
            if line_sets[i] & covered:
                continue
            chosen.append(i)
            got = search(covered | line_sets[i], i + 1, chosen)
            if got:
                return got
            chosen.pop()
        return None

    found = search(frozenset(), 0, [])
    if found:
        spread = [sorted(lines[i]) for i in found]
        cover = set()
        for L in spread:
            cover |= set(L)
        print(f"  SPREAD FOUND: {len(spread)} lines covering {len(cover)} points "
              f"(disjoint: {len(cover) == 40})")
        for L in spread:
            print(f"      {L}")
    else:
        print("  no spread exists")

    is_w33 = bool(gq and edge_ok and found)
    print(f"""
  VERDICT.  The graph is strongly regular with the right parameters (28 candidates), it
  is the collinearity graph of a GQ(3,3) (2 candidates), and it HAS A SPREAD.  Q(4,3) has
  no spread at odd q; W(3,3) does.  Therefore

      the 40 rays are the points of W(3,3):  {is_w33}

  and Pass 2835's claim -- M36 is W(3,3) minus one line -- now rests on the identification
  it needed rather than on a parameter coincidence.

  WHAT I GOT WRONG, AND WHERE IT WAS WRITTEN DOWN.  Pass 2835 said the SRG parameters made
  the graph "the W(3,3) collinearity graph".  docs/index.html states in plain words, in
  its Theory section, that the parameters do not identify the graph and that Spence found
  28 of them.  The blueprint repeated the error in stronger language still -- "there is
  essentially one object in the world with that compatibility pattern" -- which is simply
  false, and is corrected in this batch.""")

    out = {"pass": 2869,
           "srg_parameters": [40, 12, 2, 4],
           "spence_nonisomorphic_count": 28,
           "lines": len(lines),
           "every_edge_in_one_line": bool(edge_ok),
           "gq_axiom_holds": bool(gq),
           "spread_found": bool(found),
           "spread": spread,
           "identified_as_W33": is_w33,
           "prior_art": "docs/index.html Theory section states the Spence count"}
    path = ROOT / "data" / "PART_W33_PASS2869_WHICH_SRG.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
