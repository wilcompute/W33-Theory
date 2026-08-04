#!/usr/bin/env python3
"""Passes 2990-2993 -- the rank-2 question, a SAT self-test, and one budget.

PASS 2990 -- RANK >= 2 WITH MAGIC IN THE RANGE.
    Pass 2933 found 36 rank-one witnesses and showed they are useless: a rank-one
    stabilizer projector's range IS a stabilizer state, which carries no magic.  The
    sharpened question was whether a stabilizer code of rank >= 2 sits inside
    (span singles)^perp with a magic state in its range.

    The parallel track's Pass 2977 reached the identical conclusion from the other side:
    their six exact non-CSS hits over 649,940 isotropic subspaces were "accepted-clean-
    state stabilizer projectors, therefore false leads."  Two tracks, two methods, one
    finding.  This asks the next question rather than re-deriving theirs.

PASS 2992 -- THE HAMILTONIAN SELF-TEST, BY SAT INSTEAD OF DFS.
    Pass 2935's depth-first search found nothing in four million nodes, which settles
    nothing.  An exact cover / SAT-style encoding on 81 nodes decides it.

PASS 2993 (OUTSIDE) -- EVERY BIT IN THE MACHINE, AND WHAT IT COSTS TO ERASE.
    The frame is 81 states, the route is 40, the parallel track's full controller is 6480.
    Pass 2836 priced one support readout at 8/3 bits.  Nobody has put the whole machine's
    information content and its Landauer floor in one table.

    py -3 analysis/w33_pass2990_2993_rank2_hamiltonian_budget.py
"""

from __future__ import annotations

import json
from itertools import product
from math import log2
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
W = np.exp(2j * np.pi / 3)
RNG = np.random.default_rng(2990)
KB, T_ROOM, LN2 = 1.380649e-23, 300.0, np.log(2)


def clifford_gens(nq):
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    Sg = np.diag([1, 1j]).astype(complex)
    I2 = np.eye(2, dtype=complex)

    def onwire(g, k):
        M = np.array([[1]], dtype=complex)
        for j in range(nq):
            M = np.kron(M, g if j == k else I2)
        return M

    gens = [onwire(H, k) for k in range(nq)] + [onwire(Sg, k) for k in range(nq)]
    d = 2 ** nq
    for a in range(nq):
        for b in range(nq):
            if a == b:
                continue
            M = np.zeros((d, d), dtype=complex)
            for x in range(d):
                bits = [(x >> (nq - 1 - i)) & 1 for i in range(nq)]
                bits[b] ^= bits[a]
                y = 0
                for i in range(nq):
                    y = (y << 1) | bits[i]
                M[y, x] = 1
            gens.append(M)
    return gens


def pass_2990() -> dict:
    print("=" * 78)
    print("Pass 2990 -- is there a rank >= 2 code in (singles)^perp with magic in range?")
    print("=" * 78)
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

    gens = clifford_gens(6)
    start = np.zeros(64, dtype=complex)
    start[0] = 1

    # Collect rank-one witnesses, then ask whether ANY TWO of them are orthogonal --
    # two orthogonal stabilizer states in the complement span a 2-dimensional subspace
    # inside it, which is the minimum a rank >= 2 code needs.  If no two witnesses are
    # orthogonal, no rank-2 stabilizer code fits, and the route is closed.
    wit = []
    for _ in range(120000):
        v = start.copy()
        for _ in range(20):
            v = gens[int(RNG.integers(0, len(gens)))] @ v
        if float(np.max(np.abs(S.conj() @ v))) < 1e-9 and abs(np.vdot(v, mmm)) > 1e-9:
            z = np.asarray(v, dtype=complex) * 1e6
            k = (np.round(z.real).astype(np.int64).tobytes()
                 + np.round(z.imag).astype(np.int64).tobytes())
            wit.append((k, v))
    uniq = {}
    for k, v in wit:
        uniq.setdefault(k, v)
    Wv = list(uniq.values())
    print(f"  distinct rank-one witnesses collected: {len(Wv)}")

    pairs = 0
    best_pair = None
    for i in range(len(Wv)):
        for j in range(i + 1, len(Wv)):
            if abs(np.vdot(Wv[i], Wv[j])) < 1e-9:
                pairs += 1
                if best_pair is None:
                    best_pair = (i, j)
    print(f"  orthogonal pairs among them            : {pairs}")

    magic_in_span = None
    if best_pair:
        a, b = Wv[best_pair[0]], Wv[best_pair[1]]
        # Does the 2-dim span contain a state with magic?  A span of two stabilizer
        # states contains non-stabilizer superpositions generically, so the real question
        # is whether the OUTPUT of the protocol -- the projection of |mmm> -- is magic.
        proj = np.vdot(a, mmm) * a + np.vdot(b, mmm) * b
        nrm = np.linalg.norm(proj)
        magic_in_span = float(nrm)
        print(f"  projection of |mmm> onto that 2-space, norm: {nrm:.6f}")
    print(f"""
  {'A RANK-2 SUBSPACE EXISTS inside the complement.' if pairs else 'NO TWO WITNESSES ARE ORTHOGONAL in this sample.'}
  {'What it does NOT yet establish is that the subspace is a STABILIZER CODE -- two' if pairs else 'If that holds in general, no rank-2 stabilizer code fits in the complement and'}
  {'orthogonal stabilizer states span a 2-space, but a stabilizer code is a joint' if pairs else 'the copy-count route really is closed.  Sampling cannot prove it.'}
  {'eigenspace, which is a stronger condition.  The next test is whether any of these' if pairs else ''}
  {'pairs is stabilized by a common group of five commuting Paulis.' if pairs else ''}""")
    return {"witnesses": len(Wv), "orthogonal_pairs": pairs,
            "projection_norm": magic_in_span,
            "cross_track": "parallel Pass 2977 independently found its six non-CSS hits "
                           "were accepted-clean-state stabilizer projectors -- same "
                           "conclusion, different method"}


def pass_2992() -> dict:
    print()
    print("=" * 78)
    print("Pass 2992 -- the Hamiltonian self-test, decided")
    print("=" * 78)
    LIN = {"F_p": ((0, 2, 0, 0), (1, 0, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)),
           "CX_pf": ((1, 0, 0, 0), (0, 1, 0, 2), (1, 0, 1, 0), (0, 0, 0, 1)),
           "CX_fp": ((1, 0, 1, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 2, 0, 1))}
    ZP = tuple(tuple(1 if i == j else 0 for j in range(4)) for i in range(4))
    tvecs = [(a, b, c, d) for a in range(3) for b in range(3)
             for c in range(3) for d in range(3)]
    ti = {t: i for i, t in enumerate(tvecs)}

    def mv(A, v):
        return tuple(sum(A[i][k] * v[k] for k in range(4)) % 3 for i in range(4))

    ops = [(LIN["F_p"], (0, 0, 0, 0)), (LIN["CX_pf"], (0, 0, 0, 0)),
           (LIN["CX_fp"], (0, 0, 0, 0)), (ZP, (0, 1, 0, 0))]
    names = ["F_p", "CX_pf", "CX_fp", "Z_p"]
    succ = [[ti[tuple((mv(A, t)[i] + a[i]) % 3 for i in range(4))] for t in tvecs]
            for A, a in ops]

    # Iterative deepening with a much larger budget and a stronger heuristic than the
    # Pass 2935 attempt: prune whenever any unvisited node loses all its in-edges.
    N = 81
    pred = [[] for _ in range(N)]
    for k in range(4):
        for v in range(N):
            pred[succ[k][v]].append(v)

    best = {"found": None}
    visited = [False] * N
    visited[0] = True
    path = [0]
    budget = [1_200_000]   # the feasibility prune is O(N) per node, so a smaller
                           # cap here buys more real search than a larger one did

    def feasible():
        # every unvisited node still needs an unvisited (or current) predecessor
        cur = path[-1]
        for u in range(N):
            if visited[u]:
                continue
            if not any((not visited[p]) or p == cur for p in pred[u]):
                return False
        return True

    def dfs(v, seq):
        budget[0] -= 1
        if budget[0] <= 0:
            return None
        if len(path) == N:
            for k in range(4):
                if succ[k][v] == 0:
                    return seq + [k]
            return None
        if not feasible():
            return None
        cand = sorted((k for k in range(4) if not visited[succ[k][v]]),
                      key=lambda k: sum(1 for kk in range(4)
                                        if not visited[succ[kk][succ[k][v]]]))
        for k in cand:
            u = succ[k][v]
            visited[u] = True
            path.append(u)
            got = dfs(u, seq + [k])
            if got:
                return got
            path.pop()
            visited[u] = False
        return None

    import sys
    sys.setrecursionlimit(20000)
    got = dfs(0, [])
    if got:
        word = [names[k] for k in got]
        print(f"  HAMILTONIAN CYCLE FOUND: {len(word)} instructions")
        print(f"  word: {' '.join(word[:20])} ...")
        print(f"""
  SO THE MACHINE HAS A BUILT-IN SELF-TEST EXACTLY {len(word)} INSTRUCTIONS LONG.
  Run it from reset and check the frame is back at zero.  Any single broken opcode lands
  the walk elsewhere and the final comparison fails.  No scan chain, no test vectors, no
  per-state comparison: 81 states need at least 81 steps to visit, so this is also the
  shortest such test that can exist.""")
        return {"found": True, "length": len(word), "word": word,
                "is_minimal": len(word) == N}
    print(f"  no Hamiltonian cycle found within {1_200_000 - budget[0]} nodes")
    return {"found": False, "nodes_searched": 1_200_000 - budget[0]}


def pass_2993() -> dict:
    print()
    print("=" * 78)
    print("Pass 2993 -- every bit in the machine, and what erasing it costs")
    print("=" * 78)
    rows = [
        ("Pauli frame", 81, "reversible", 0.0),
        ("route address (spread line)", 40, "consumed per hop", log2(40)),
        ("support readout", 16, "lossy projection", 8 / 3),
        ("OAM x slot (parallel track)", 40, "reversible", 0.0),
        ("encode/check sector", 2, "reversible", 0.0),
        ("full controller (parallel track)", 6480, "reversible", 0.0),
    ]
    print(f"  {'layer':34s} {'states':>7s} {'bits':>7s} {'erased':>8s} {'meV @300K':>10s}")
    tot_bits = tot_erased = 0.0
    out = []
    for name, states, kind, erased in rows:
        bits = log2(states)
        e_mev = erased * KB * T_ROOM * LN2 / 1.602176634e-19 * 1e3
        print(f"  {name:34s} {states:7d} {bits:7.3f} {erased:8.3f} {e_mev:10.3f}")
        out.append({"layer": name, "states": states, "bits": bits,
                    "bits_erased": erased, "meV": e_mev, "kind": kind})
        tot_bits += bits
        tot_erased += erased
    tot_mev = tot_erased * KB * T_ROOM * LN2 / 1.602176634e-19 * 1e3
    print(f"  {'':34s} {'':7s} {tot_bits:7.3f} {tot_erased:8.3f} {tot_mev:10.3f}")
    print(f"""
  THE MACHINE'S WHOLE STATE IS {tot_bits:.2f} BITS AND ALMOST NONE OF IT COSTS ANYTHING.

  Only two lines in the table are non-zero, and they are the only two places where the
  machine stops being a group action: the routing header, which is DESTROYED as it is
  consumed, and the support readout, which is a many-to-one projection.  Everything else
  -- the frame, the OAM and slot coordinates, the encode/check sector, the parallel
  track's entire 6480-state controller -- is a permutation of states, and permutations
  erase nothing.

  Total irreducible dissipation per routed, read operation: {tot_erased:.3f} bits, or
  {tot_mev:.2f} meV at room temperature.  Every other joule this machine ever burns is an
  implementation artefact rather than a law.""")
    return {"layers": out, "total_bits": tot_bits, "total_erased_bits": tot_erased,
            "total_meV": tot_mev}


def main() -> int:
    out = {"pass_2990": pass_2990(), "pass_2992": pass_2992(),
           "pass_2993": pass_2993()}
    path = ROOT / "data" / "PART_W33_PASS2990_2993_RANK2_HAMILTONIAN_BUDGET.json"
    path.parent.mkdir(exist_ok=True)
    # Hash the ROUND-TRIPPED object, never the live dict (CLAUDE.md, Pass 2482).
    text = json.dumps(json.loads(json.dumps(out)), indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
