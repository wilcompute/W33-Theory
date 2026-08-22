"""Pass 7218 -- the 42 E8 roots over a maximum partial ovoid of W(3,3). What are they?

THE SETUP, built and verified in Pass 7217. Taking J = c^10 where c is the E8 Coxeter element
(order 30, so J has order 3; no E8 exponent 1,7,11,13,17,19,23,29 is divisible by 3, so J is
fixed-point-free and det(I-J) = 3^4 = 81), the root lattice becomes a Z[omega]-module of rank
4. Since J^2 + J + I = 0 gives (I-J)(I-J^2) = 3I, the class of v mod (I-J) is exactly
(I-J^2)v mod 3 -- no floating point anywhere. That yields

    80 classes of exactly 3 roots,  40 projective classes of exactly 6,

and with the ALTERNATING form A(x,y) = (Jx,y) - (x,Jy) -- the E8 form itself is symmetric and
gives the wrong graph -- the induced graph on the 40 classes has degree 12 and spectrum
12^1 2^24 (-4)^15, i.e. it IS the W(3,3) collinearity graph SRG(40,12,2,4).

THE QUESTION. alpha(W(3,3)) = 7, so a maximum partial ovoid pulls back to 42 roots, and 42 is
the root count of both A6 and D5 x A1. Is the preimage a root SUBSYSTEM of E8?

The test is closure under reflection: for roots r, s in the set, s - (s,r)r must be in the set
(the E8 form is normalised so roots have norm 2). If it closes, a purely combinatorial
extremal problem in a finite geometry is selecting a Lie-theoretic object. If it does not,
42 = |A6| is a numerical coincidence and is recorded as one -- this repo has a documented
history of exactly that failure mode, and the honest outcome is worth as much as the pretty
one.

    py -3 analysis/w33_pass7218_what_are_the_42_roots.py
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import numpy as np  # noqa: E402
from w33_pass7217_ovoid_pullback_to_e8 import (  # noqa: E402
    CARTAN, roots_in_root_basis, simple_reflection, order_of,
)


def build():
    R = roots_in_root_basis()
    Rarr = np.array(R, dtype=np.int64)
    G = CARTAN
    I8 = np.eye(8, dtype=np.int64)
    cox = I8.copy()
    for i in range(8):
        cox = cox @ simple_reflection(i)
    J = np.linalg.matrix_power(cox, 10)
    assert order_of(J, 8) == 3
    assert int(round(np.linalg.det(I8 - J))) == 81
    K = I8 - J @ J

    def cls(v):
        return tuple(int(x) % 3 for x in (K @ v))

    classes = {}
    for i, v in enumerate(Rarr):
        classes.setdefault(cls(v), []).append(i)
    classes.pop((0, 0, 0, 0), None)
    proj = {}
    for c, mem in classes.items():
        key = min(c, tuple((2 * x) % 3 for x in c))
        proj.setdefault(key, []).extend(mem)
    assert len(proj) == 40 and {len(v) for v in proj.values()} == {6}
    A_int = (J.T @ G) - (G @ J)
    return Rarr, G, J, proj, A_int


def main() -> int:
    print("=" * 78)
    print("Pass 7218 -- the 42 roots over a maximum partial ovoid")
    print("=" * 78)

    Rarr, G, J, proj, A_int = build()
    keys = sorted(proj)
    reps = [Rarr[proj[k][0]] for k in keys]
    Adj = np.zeros((40, 40), dtype=np.int64)
    for i in range(40):
        for j in range(i + 1, 40):
            if int(reps[i] @ A_int @ reps[j]) % 3 == 0:
                Adj[i, j] = Adj[j, i] = 1
    ev = Counter(np.linalg.eigvalsh(Adj.astype(float)).round(6))
    print(f"\n  W(3,3) recovered: degree {int(Adj[0].sum())}, "
          f"spectrum {dict(sorted((float(a), b) for a, b in ev.items()))}")
    assert int(Adj[0].sum()) == 12

    # maximum partial ovoid = maximum independent set, computed in THIS labelling
    import networkx as nx
    Gx = nx.Graph()
    Gx.add_nodes_from(range(40))
    for i in range(40):
        for j in range(i + 1, 40):
            if Adj[i, j]:
                Gx.add_edge(i, j)
    best = max(nx.find_cliques(nx.complement(Gx)), key=len)
    print(f"  maximum partial ovoid in this labelling: {len(best)} points "
          f"(alpha(W(3,3)) = 7)")
    assert len(best) == 7

    idxs = sorted(i for p in best for i in proj[keys[p]])
    S = Rarr[idxs]
    print(f"\n  preimage: {len(S)} roots   (7 x 6 = 42)")

    # closure under reflection
    Sset = {tuple(int(x) for x in v) for v in S}
    closed = True
    generated = set(Sset)
    frontier = list(Sset)
    while frontier:
        nxt = []
        for a in frontier:
            av = np.array(a, dtype=np.int64)
            for b in list(generated):
                bv = np.array(b, dtype=np.int64)
                c = bv - int(bv @ G @ av) * av
                tc = tuple(int(x) for x in c)
                if tc not in generated:
                    generated.add(tc)
                    nxt.append(tc)
        frontier = nxt
    closed = (generated == Sset)
    print(f"  closed under reflection? {closed}")
    print(f"  reflection closure has {len(generated)} roots "
          f"(started from {len(Sset)})")

    verdict = ""
    if closed:
        rank = np.linalg.matrix_rank(S.astype(float))
        print(f"  RANK of the span: {rank}")
        named = {42: "A6 (42 roots, rank 6) or D5 x A1 (40+2, rank 6)"}
        verdict = (f"the 42 roots ARE a root subsystem of rank {rank}; "
                   f"{named.get(42, '')}")
        print(f"  -> {verdict}")
    else:
        cnt = len(generated)
        known = {240: "all of E8", 126: "E7", 72: "E6", 60: "D... ", 42: "A6"}
        verdict = (f"NOT a subsystem: the 42 roots generate {cnt} roots under "
                   f"reflection ({known.get(cnt, 'unnamed')}), so 42 = |A6| is a "
                   f"numerical coincidence here")
        print(f"  -> {verdict}")

    # what the 42 roots DO look like: inner-product distribution
    ip = Counter()
    for a, b in itertools.combinations(range(len(S)), 2):
        ip[int(S[a] @ G @ S[b])] += 1
    print(f"\n  inner-product distribution among the 42 roots: {dict(sorted(ip.items()))}")
    # compare with a random 42-subset for calibration
    rs = np.random.RandomState(7218)
    ipr = Counter()
    pick = rs.choice(240, 42, replace=False)
    for a, b in itertools.combinations(pick, 2):
        ipr[int(Rarr[a] @ G @ Rarr[b])] += 1
    print(f"  the same for a RANDOM 42 roots:               {dict(sorted(ipr.items()))}")

    out = {"boundary": ("the fibration is verified by recovering SRG(40,12,2,4); the "
                        "subsystem question is answered by reflection closure, and a "
                        "negative answer is reported as a coincidence, not smoothed over"),
           "fibration_verified": True, "preimage_size": int(len(S)),
           "closed_under_reflection": bool(closed),
           "reflection_closure_size": int(len(generated)),
           "inner_products": {str(k): v for k, v in sorted(ip.items())},
           "random_control": {str(k): v for k, v in sorted(ipr.items())},
           "verdict": verdict}
    fp = ROOT / "data" / "PART_W33_PASS7218_FORTYTWO_ROOTS.json"
    fp.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
