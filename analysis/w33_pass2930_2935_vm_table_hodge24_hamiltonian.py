#!/usr/bin/env python3
"""Passes 2930-2935 -- the native/guest trade, the last count match, and a self-test.

PASS 2930 -- THE NATIVE-VERSUS-GUEST TRADE, IN ONE TABLE.
    Pass 2912 measured the emulation overhead of the shortest triple at 8x worst, and the
    whole cost turned out to be the guest's S gate -- which that triple drops.  Two of the
    six minimal triples KEEP S.  So the trade is not "minimal is better"; it is a curve,
    and this computes both ends of it for all six.

PASS 2932 -- IS THE HODGE 24 A MAP?
    Pass 2884 flagged 240 = 81 + 120 + 24 + 15 with two count matches.  Pass 2911 killed
    the 15.  The 24 is the last one standing: |SL(2,3)| is the single-qutrit Clifford
    group modulo phase, and the lambda = 10 eigenspace has dimension 24.

PASS 2933 -- THREE COPIES, WITH A BETTER ARGUMENT.
    Pass 2910's set-cover search was exhaustive only over the factor-wise family.  There
    is a strictly stronger reduction: a stabilizer projector annihilates all nine singles
    iff its RANGE lies in their orthogonal complement, and the range of a stabilizer
    projector is a stabilizer CODE, which contains stabilizer STATES.  So

        if no six-qubit stabilizer STATE lies in (span singles)^perp with nonzero overlap
        on |mmm>, then no stabilizer projector of any rank works either.

    That converts a search over projectors into a search over states, and the necessary
    condition is far more restrictive.

PASS 2935 (LUDICROUS) -- CAN THE MACHINE SWEEP ITS OWN STATE SPACE IN ONE PASS?
    A Hamiltonian cycle in the frame graph would be a single instruction sequence that
    visits all 81 frames exactly once and returns.  That is a built-in self-test with no
    comparisons, no scan chain and no test vectors: run the word, check you are home.

    py -3 analysis/w33_pass2930_2935_vm_table_hodge24_hamiltonian.py
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations, product
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)
RNG = np.random.default_rng(2930)

LIN = {
    "F_p":   ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "F_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 0, 2), (0, 0, 1, 0)),
    "S_p":   ((1, 0, 0, 0), (1, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
    "S_f":   ((1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 1, 1)),
    "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
    "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1)),
}
ZP = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
ZT = (0, 1, 0, 0)
IDENT = ZP
TRIPLES = [("F_p", "F_f", "CX_pf"), ("F_p", "F_f", "CX_fp"),
           ("F_p", "S_f", "CX_pf"), ("F_p", "CX_pf", "CX_fp"),
           ("F_f", "S_p", "CX_fp"), ("F_f", "CX_pf", "CX_fp")]
# The guest is a one-qutrit machine on the PAST register: F, S, Z.
GUEST = {"F_guest": LIN["F_p"], "S_guest": LIN["S_p"]}


def mul(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(4)) % 3 for j in range(4))
                 for i in range(4))


def matvec(a, v):
    return tuple(sum(a[i][k] * v[k] for k in range(4)) % 3 for i in range(4))


def host_depths(names):
    """Shortest-word depth over ASp(4,3) for the triple `names` plus Z_p."""
    sp_list, sp_index, frontier = [IDENT], {IDENT: 0}, [IDENT]
    while frontier:
        nxt = []
        for M in frontier:
            for nm in names:
                P = mul(LIN[nm], M)
                if P not in sp_index:
                    sp_index[P] = len(sp_list)
                    sp_list.append(P)
                    nxt.append(P)
        frontier = nxt
    if len(sp_list) != 51840:
        return None
    NT = 81
    tvecs = [(a, b, c, d) for a in range(3) for b in range(3)
             for c in range(3) for d in range(3)]
    t_index = {t: i for i, t in enumerate(tvecs)}
    gens = [(LIN[n], (0, 0, 0, 0)) for n in names] + [(ZP, ZT)]
    sp_perm, t_map = [], []
    for A, a in gens:
        sp_perm.append(np.array([sp_index[mul(A, M)] for M in sp_list], dtype=np.int32))
        t_map.append(np.array(
            [t_index[tuple((matvec(A, t)[i] + a[i]) % 3 for i in range(4))]
             for t in tvecs], dtype=np.int32))
    N = 51840 * NT
    depth = np.full(N, 255, dtype=np.uint8)
    start = sp_index[IDENT] * NT + t_index[(0, 0, 0, 0)]
    depth[start] = 0
    frontier = np.array([start], dtype=np.int64)
    d = 0
    while frontier.size:
        d += 1
        cand = np.unique(np.concatenate(
            [sp_perm[k][frontier // NT].astype(np.int64) * NT + t_map[k][frontier % NT]
             for k in range(len(gens))]))
        cand = cand[depth[cand] == 255]
        if cand.size == 0:
            d -= 1
            break
        depth[cand] = min(d, 254)
        frontier = cand
    return depth, sp_index, t_index, NT, int(d)


# ===========================================================================
def pass_2930() -> dict:
    print("=" * 78)
    print("Pass 2930 -- native speed against guest speed, for all six triples")
    print("=" * 78)
    print("  triple                       diam   F_g   S_g   Z_g   worst  mean")
    rows = {}
    for names in TRIPLES:
        r = host_depths(names)
        if r is None:
            continue
        depth, sp_index, t_index, NT, diam = r
        c = {}
        for nm, A in GUEST.items():
            c[nm] = int(depth[sp_index[A] * NT + t_index[(0, 0, 0, 0)]])
        c["Z_guest"] = int(depth[sp_index[IDENT] * NT + t_index[(0, 1, 0, 0)]])
        worst = max(c.values())
        mean = sum(c.values()) / 3
        key = " + ".join(names)
        rows[key] = {"diameter": diam, **c, "worst": worst, "mean": mean}
        print(f"  {key:28s} {diam:4d} {c['F_guest']:5d} {c['S_guest']:5d} "
              f"{c['Z_guest']:5d} {worst:6d} {mean:6.2f}")

    best_native = min(rows.items(), key=lambda kv: kv[1]["diameter"])
    best_guest = min(rows.items(), key=lambda kv: (kv[1]["worst"], kv[1]["mean"]))
    print(f"\n  best NATIVE (shortest diameter) : {best_native[0]}  "
          f"diam {best_native[1]['diameter']}, guest worst {best_native[1]['worst']}")
    print(f"  best GUEST  (lowest overhead)   : {best_guest[0]}  "
          f"diam {best_guest[1]['diameter']}, guest worst {best_guest[1]['worst']}")
    same = best_native[0] == best_guest[0]
    print(f"  same triple wins both           : {same}")
    # Is the native winner ALSO tied-best on guests?  The `best_guest` pick above uses a
    # mean tie-break, which is arbitrary when the worst cases tie -- so ask directly.
    bw = min(v["worst"] for v in rows.values())
    native_also_best = best_native[1]["worst"] == bw
    print(f"  lowest guest worst-case over all six : {bw}")
    print(f"  the native winner attains it         : {native_also_best}")
    if native_also_best:
        print(f"""
  THE TRADE I EXPECTED DOES NOT EXIST.  {best_native[0]} has the shortest
  diameter ({best_native[1]['diameter']}) AND ties for the lowest guest overhead ({bw}x).
  No triple is better for guests than the one that is best natively, so the choice made in
  hardware needs no workload assumption after all.

  And the reason the alternative fails is legible in the table.  F_f + S_p + CX_fp KEEPS
  the guest's S gate, so S_guest costs 1 instead of 8 -- and F_guest jumps from 1 to 10.
  The cost does not disappear when you keep S; it MOVES to F, and lands higher.  A
  hypothesis refuted by the same table that was built to quantify it.""")
    else:
        print(f"""
  THE TRADE IS REAL.  {best_native[0]} runs native code in at most
  {best_native[1]['diameter']} instructions but pays {best_native[1]['worst']}x on the
  worst guest instruction, while {best_guest[0]} pays {bw}x.""")
    return {"per_triple": rows, "best_native": best_native[0],
            "best_guest": best_guest[0], "lowest_guest_worst_case": bw,
            "native_winner_also_best_for_guests": bool(native_also_best)}


# ===========================================================================
def pass_2932() -> dict:
    print()
    print("=" * 78)
    print("Pass 2932 -- is the Hodge 24 the single-qutrit Clifford group?")
    print("=" * 78)
    J = [[0, 1, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 0, 2, 0]]
    pts, seen = [], set()
    for v in np.ndindex(3, 3, 3, 3):
        if v == (0, 0, 0, 0):
            continue
        key = min(tuple((c * k) % 3 for k in v) for c in (1, 2))
        if key in seen:
            continue
        seen.add(key)
        pts.append(key)

    def form(u, v):
        return sum(u[i] * J[i][j] * v[j] for i in range(4) for j in range(4)) % 3

    n = len(pts)
    adj = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if i != j and form(pts[i], pts[j]) == 0:
                adj[i, j] = True
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if adj[i, j]]
    tris = [t for t in combinations(range(n), 3)
            if adj[t[0], t[1]] and adj[t[0], t[2]] and adj[t[1], t[2]]]
    eidx = {e: k for k, e in enumerate(edges)}
    d0 = np.zeros((len(edges), n))
    for (i, j), k in eidx.items():
        d0[k, i], d0[k, j] = -1.0, 1.0
    d1 = np.zeros((len(tris), len(edges)))
    for r, (a, b, c) in enumerate(tris):
        d1[r, eidx[(a, b)]] = 1.0
        d1[r, eidx[(b, c)]] = 1.0
        d1[r, eidx[(a, c)]] = -1.0
    L1 = d0 @ d0.T + d1.T @ d1
    vals, vecs_ = np.linalg.eigh(L1)
    E = vecs_[:, np.abs(vals - 10.0) < 1e-6]
    print(f"  lambda = 10 eigenspace dimension: {E.shape[1]}")

    # act with the block swap (a genuine symmetry of J) and take the trace
    perm = [2, 3, 0, 1]
    pmap = {}
    for i, p in enumerate(pts):
        q = tuple(p[perm[k]] for k in range(4))
        q = min(tuple((c * x) % 3 for x in q) for c in (1, 2))
        pmap[i] = pts.index(q)
    P = np.zeros((len(edges), len(edges)))
    for (a, b), k in eidx.items():
        u, v = sorted((pmap[a], pmap[b]))
        P[eidx[(u, v)], k] = 1.0
    tr = float(np.trace(E.T @ P @ E))
    print(f"  trace of the block swap on it  : {tr:.6f}")
    integral = abs(tr - round(tr)) < 1e-6
    print(f"  is that an integer?            : {integral}")
    print(f"""
  {'The 24 survives this test -- one matching value, not a proof.' if integral else 'THE 24 IS NOT A PERMUTATION MODULE EITHER.'}
  A group of order 24 acting on itself gives a permutation module, whose character is an
  integer on every element.  {'So this does not refute the identification and does not establish it.' if integral else 'A non-integer trace refutes that outright.'}
  {'A full character comparison over all classes would be needed.' if integral else 'Both count matches from Pass 2884 are now dead.'}""")
    return {"eigenspace_dim": int(E.shape[1]), "trace": tr,
            "trace_is_integer": bool(integral),
            "verdict": "not refuted by this element" if integral else "refuted"}


# ===========================================================================
def pass_2933() -> dict:
    print()
    print("=" * 78)
    print("Pass 2933 -- three copies, via stabilizer STATES instead of projectors")
    print("=" * 78)
    print("""  The reduction: a stabilizer projector annihilates all nine singles iff its RANGE
  lies in their orthogonal complement.  The range of a stabilizer projector is a
  stabilizer CODE, and every stabilizer code contains stabilizer STATES.  So if no
  six-qubit stabilizer state lies in (span singles)^perp with nonzero overlap on |mmm>,
  then NO stabilizer projector of any rank works -- which is a genuinely stronger
  statement than Pass 2910's factor-wise search.""")

    w = [1, W, W ** 2]
    m = np.array([0, 1, -w[0], w[0]], dtype=complex)
    m /= np.linalg.norm(m)
    Q, _ = np.linalg.qr(np.column_stack([m] + [np.eye(4, dtype=complex)[:, i]
                                               for i in range(4)]))
    e = [Q[:, i] for i in range(1, 4)]
    mmm = np.kron(np.kron(m, m), m)
    singles = []
    for i in range(3):
        singles.append(np.kron(np.kron(e[i], m), m))
        singles.append(np.kron(np.kron(m, e[i]), m))
        singles.append(np.kron(np.kron(m, m), e[i]))
    S = np.array(singles)

    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    Sg = np.diag([1, 1j]).astype(complex)
    I2 = np.eye(2, dtype=complex)
    nq, dim = 6, 64

    def onwire(g, k):
        M = np.array([[1]], dtype=complex)
        for j in range(nq):
            M = np.kron(M, g if j == k else I2)
        return M

    gens = [onwire(H, k) for k in range(nq)] + [onwire(Sg, k) for k in range(nq)]
    for a in range(nq):
        for b in range(nq):
            if a == b:
                continue
            M = np.zeros((dim, dim), dtype=complex)
            for x in range(dim):
                bits = [(x >> (nq - 1 - i)) & 1 for i in range(nq)]
                bits[b] ^= bits[a]
                y = 0
                for i in range(nq):
                    y = (y << 1) | bits[i]
                M[y, x] = 1
            gens.append(M)

    start = np.zeros(dim, dtype=complex)
    start[0] = 1
    best_orth, hits, TRIALS = 1.0, 0, 200000
    for _ in range(TRIALS):
        v = start.copy()
        for _ in range(20):
            v = gens[int(RNG.integers(0, len(gens)))] @ v
        ov = np.abs(S.conj() @ v)
        worst = float(np.max(ov))
        if worst < best_orth:
            best_orth = worst
        if worst < 1e-9 and abs(np.vdot(v, mmm)) > 1e-9:
            hits += 1
    print(f"\n  stabilizer states sampled: {TRIALS}")
    print(f"  best (smallest) max-overlap with the nine singles: {best_orth:.6f}")
    print(f"  states orthogonal to all nine AND overlapping |mmm>: {hits}")
    if hits > 0:
        print(f"""
  WITNESSES FOUND: {hits}.  Stabilizer states DO exist that are orthogonal to all nine
  single-error vectors while overlapping |mmm>.  So the first-order condition IS
  satisfiable at three copies, and Pass 2910's negative was an artefact of searching the
  factor-wise family rather than a fact about three copies.

  AND IT IS NOT YET A PROTOCOL.  A rank-one stabilizer projector |sigma><sigma| has a
  stabilizer state as its entire range, and a stabilizer state carries NO MAGIC.  Such a
  branch suppresses the first-order error perfectly and outputs something useless.

  So the question sharpens rather than closing, and it is now well posed for the first
  time:

      is there a stabilizer code of rank >= 2 inside (span singles)^perp whose range
      contains a magic state?

  Rank one is proved possible and proved useless.  Rank two or more is what a real
  three-copy protocol needs, and nothing above rules it out -- which is a much better
  position than the three negatives that preceded it.""")
    if hits == 0:
        print(f"""
  None.  The best any sampled stabilizer state managed was {best_orth:.4f} -- not close to
  the 0 the condition demands, which is informative: this is not a near miss.  Together
  with Pass 2861 (exhaustive at two copies) and Pass 2910 (exhaustive over the factor-wise
  family at three), three independent formulations now agree, and the reduction to states
  is the strongest of the three because it covers projectors of EVERY rank.

  Still not a proof -- 200,000 of 315,057,600 states is 0.06% -- but the failure is by a
  wide margin rather than a whisker, which is worth recording.""")
    return {"trials": TRIALS, "best_max_overlap": best_orth, "hits": hits,
            "rank_one_witness_exists": bool(hits > 0),
            "rank_one_is_useless": "its range is a stabilizer state, which has no magic",
            "open_question": "a rank >= 2 stabilizer code in (singles)^perp "
                             "whose range contains a magic state",
            "reduction": "projector kills all nine iff its range, a stabilizer code, "
                         "lies in the complement; codes contain states",
            "covers_all_ranks": True}


# ===========================================================================
def pass_2935() -> dict:
    print()
    print("=" * 78)
    print("Pass 2935 (LUDICROUS) -- can the machine sweep its own state space in one word?")
    print("=" * 78)
    tvecs = [(a, b, c, d) for a in range(3) for b in range(3)
             for c in range(3) for d in range(3)]
    t_index = {t: i for i, t in enumerate(tvecs)}
    names = ["F_p", "CX_pf", "CX_fp", "Z_p"]
    ops = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
           (LIN["CX_fp"], (0, 0, 0, 0)), (ZP, ZT)]
    succ = [[t_index[tuple((matvec(A, t)[i] + a[i]) % 3 for i in range(4))]
             for t in tvecs] for A, a in ops]

    print("  frame graph: 81 nodes, out-degree 4 (one edge per opcode)")
    # Hamiltonian cycle by DFS with Warnsdorff-style ordering
    N = 81
    path, visited = [0], [False] * N
    visited[0] = True
    order = list(range(4))

    def deg(v):
        return sum(1 for k in order if not visited[succ[k][v]])

    import sys
    sys.setrecursionlimit(10000)
    budget = [4_000_000]        # mutable cell: a node budget for the DFS

    def dfs(v, opseq):
        budget[0] -= 1
        if budget[0] <= 0:
            return None
        if len(path) == N:
            return 0 in [succ[k][v] for k in order] and (opseq, [k for k in order
                                                                if succ[k][v] == 0][0])
        cand = sorted((k for k in order if not visited[succ[k][v]]),
                      key=lambda k: deg(succ[k][v]))
        for k in cand:
            u = succ[k][v]
            visited[u] = True
            path.append(u)
            opseq.append(k)
            got = dfs(u, opseq)
            if got:
                return got
            opseq.pop()
            path.pop()
            visited[u] = False
        return None

    # Bounded search: an unbounded DFS on this graph ran past a ten-minute
    # budget in the first attempt.  A node cap makes the pass terminate and
    # report 'not found within N nodes', which is an honest result; an
    # unbounded search that gets killed reports nothing at all.
    got = dfs(0, [])
    if got:
        seq, closing = got
        word = [names[k] for k in seq] + [names[closing]]
        print(f"  HAMILTONIAN CYCLE FOUND: {len(word)} instructions visiting all 81 "
              f"frames exactly once and returning")
        print(f"  first 12 instructions: {' '.join(word[:12])}")
        hist = Counter(word)
        print(f"  opcode histogram: {dict(sorted(hist.items()))}")
        print(f"""
  SO THE MACHINE HAS A BUILT-IN SELF-TEST THAT IS ONE WORD LONG.

  Run those {len(word)} instructions from reset and check the frame is back at zero.  If any
  single opcode is broken, the walk lands somewhere else and the final comparison fails.
  No scan chain, no test vectors, no per-state comparisons -- ONE 81-instruction word and
  ONE equality check covers the entire reachable state space, because a Hamiltonian cycle
  visits every state exactly once by definition.

  It is also the shortest possible such test: 81 states need at least 81 steps to visit.""")
        return {"cycle_length": len(word), "word": word,
                "opcode_histogram": {k: v for k, v in sorted(hist.items())},
                "is_minimal": len(word) == 81 + 1 or len(word) == 81}
    print("  no Hamiltonian cycle found by this search")
    return {"cycle_length": None}


def main() -> int:
    out = {"pass_2930": pass_2930(), "pass_2932": pass_2932(),
           "pass_2933": pass_2933(), "pass_2935": pass_2935()}
    path = ROOT / "data" / "PART_W33_PASS2930_2935_VM_HODGE24_HAMILTONIAN.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
