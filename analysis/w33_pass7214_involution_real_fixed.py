"""Pass 7214 -- redo of Pass 7213, whose control caught a real bug in my construction.

WHAT PASS 7213 GOT WRONG. It built the projectivity M from a frame by setting the i-th COLUMN
of M to lam_i * f_i. That is correct only when the frame's first four points are the STANDARD
basis. They are points of O, so the correct map is

    M  =  Fm . diag(lam) . A^{-1}

with A the matrix whose columns are the frame points and Fm the matrix whose columns are
their images. Pass 7213 effectively used A = I, so its M sent the standard basis where the
frame should have gone, and no such map stabilised anything.

THE CONTROL CAUGHT IT, which is the point of having one. At q=3 the true stabilizer is 18
(Pass 7203, by enumerating all 51,840 elements of Sp(4,3)), so a working method must realise
nontrivial automorphisms there. Pass 7213 realised 0 of 71 and its q=7/q=9 verdicts were
therefore void -- it printed them anyway, which is a reporting bug fixed here: this script
refuses to print a verdict when the control fails.

THE QUESTION, unchanged. Pass 7199 bounds Stab(O) by Aut of the edge-coloured complete graph
on O, giving |Aut| = 2 at q=7 and q=9. Is that one nontrivial automorphism induced by a
symplectic similitude (|Stab| = 2) or combinatorial only (|Stab| = 1)?

    py -3 analysis/w33_pass7214_involution_real_fixed.py
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_pass7187_q9_orbit_attack import Field, geometry  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SOURCES = {3: "data/PART_W33_Q3_PARTIAL_OVOID_7.json",
           7: "data/PART_W33_Q7_LNS_OVOID_33.json",
           9: "data/PART_W33_Q9_LNS_OVOID_51.json"}


class LA:
    """4x4 linear algebra over GF(q), matrices as row-tuples."""

    def __init__(self, F):
        self.F = F

    def mul(self, A, Bm):
        F = self.F
        return tuple(tuple(self._dot(A[i], [Bm[k][j] for k in range(4)])
                           for j in range(4)) for i in range(4))

    def _dot(self, xs, ys):
        F = self.F
        t = 0
        for x, y in zip(xs, ys):
            t = F.add[t][F.mul[x][y]]
        return t

    def inv(self, A):
        F = self.F
        M = [list(A[i]) + [1 if i == j else 0 for j in range(4)] for i in range(4)]
        r = 0
        for c in range(4):
            piv = next((i for i in range(r, 4) if M[i][c]), None)
            if piv is None:
                return None
            M[r], M[piv] = M[piv], M[r]
            iv = F.inv[M[r][c]]
            M[r] = [F.mul[x][iv] for x in M[r]]
            for i in range(4):
                if i != r and M[i][c]:
                    f = M[i][c]
                    M[i] = [F.add[M[i][j]][F.neg[F.mul[f][M[r][j]]]] for j in range(8)]
            r += 1
        return tuple(tuple(M[i][4:]) for i in range(4))

    def apply(self, M, p):
        F = self.F
        img = tuple(self._dot(M[i], p) for i in range(4))
        lead = next((x for x in img if x), None)
        if lead is None:
            return None
        iv = F.inv[lead]
        return tuple(F.mul[x][iv] for x in img)

    def solve(self, A, target):
        """coordinates of target in the basis given by the COLUMNS of A."""
        Ai = self.inv(A)
        if Ai is None:
            return None
        return [self._dot(Ai[i], target) for i in range(4)]


def cols_to_matrix(vecs):
    """matrix whose COLUMNS are the given 4-vectors, as row-tuples."""
    return tuple(tuple(vecs[j][i] for j in range(4)) for i in range(4))


def graph_autos(k, colour):
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher, categorical_edge_match
    G = nx.Graph()
    G.add_nodes_from(range(k))
    for i in range(k):
        for j in range(i + 1, k):
            G.add_edge(i, j, c=colour[(i, j)])
    gm = GraphMatcher(G, G, edge_match=categorical_edge_match("c", None))
    return list(gm.isomorphisms_iter())


def realise(F, la, P, idx, B, O, a, n):
    """Is the permutation a of O induced by a symplectic similitude? Return M or None."""
    k = len(O)
    for quad in itertools.combinations(range(k), 4):
        A = cols_to_matrix([P[O[i]] for i in quad])
        if la.inv(A) is None:
            continue
        Fm = cols_to_matrix([P[O[a[i]]] for i in quad])
        if la.inv(Fm) is None:
            continue
        for fifth in range(k):
            if fifth in quad:
                continue
            c = la.solve(A, P[O[fifth]])
            if c is None or any(x == 0 for x in c):
                continue
            d = la.solve(Fm, P[O[a[fifth]]])
            if d is None or any(x == 0 for x in d):
                continue
            lam = [F.mul[d[i]][F.inv[c[i]]] for i in range(4)]
            D = tuple(tuple(lam[i] if i == j else 0 for j in range(4)) for i in range(4))
            M = la.mul(la.mul(Fm, D), la.inv(A))
            # similitude test
            mu, ok = None, True
            for u, v in itertools.combinations(range(min(n, 40)), 2):
                bu = B(P[u], P[v])
                iu, iv = la.apply(M, P[u]), la.apply(M, P[v])
                if iu is None or iv is None:
                    ok = False
                    break
                bv = B(iu, iv)
                if bu == 0:
                    if bv != 0:
                        ok = False
                        break
                    continue
                cand = F.mul[bv][F.inv[bu]]
                if mu is None:
                    mu = cand
                elif cand != mu:
                    ok = False
                    break
            if not ok or mu is None:
                continue
            if {idx[la.apply(M, P[p])] for p in O} == set(O):
                return M
    return None


def main() -> int:
    print("=" * 78)
    print("Pass 7214 -- Pass 7213 redone, after its control caught my bug")
    print("=" * 78)

    results = {}
    for q in (3, 7, 9):
        fp = ROOT / SOURCES[q]
        if not fp.is_file():
            continue
        F = Field(q)
        la = LA(F)
        P, idx, adj, B = geometry(F)
        n = len(P)
        O = sorted(idx[tuple(p)] for p in json.loads(fp.read_text(encoding="utf-8"))["points"])
        Oset = set(O)
        t = {x: len(adj[x] & Oset) for x in range(n) if x not in Oset}
        k = len(O)
        colour = {}
        for i in range(k):
            for j in range(i + 1, k):
                tr = adj[O[i]] & adj[O[j]]
                colour[(i, j)] = tuple(sorted(t.get(x, -1) for x in tr))
        autos = graph_autos(k, colour)
        nontriv = [a for a in autos if any(a[i] != i for i in range(k))]
        cap = 30
        got = 0
        for a in nontriv[:cap]:
            if realise(F, la, P, idx, B, O, a, n) is not None:
                got += 1
        tested = min(len(nontriv), cap)
        results[q] = {"aut": len(autos), "nontrivial": len(nontriv),
                      "tested": tested, "realised": got}
        print(f"\n  q={q}: |O| = {k}, |Aut(coloured graph)| = {len(autos)}, "
              f"{len(nontriv)} nontrivial")
        print(f"    tested {tested}, realised by a symplectic similitude: {got}",
              flush=True)

    ctrl = results.get(3)
    ok = bool(ctrl and ctrl["realised"] > 0)
    print(f"\n  CONTROL AT q=3 (true |Stab| = 18, Pass 7203): "
          f"{ctrl['realised'] if ctrl else 'n/a'} of {ctrl['tested'] if ctrl else 0} realised")
    print(f"  control {'PASSES' if ok else 'FAILS'}")

    if not ok:
        print("""
  NO VERDICT IS PRINTED FOR q=7 OR q=9. The method cannot detect symplectic maps where
  they are known to exist, so its silence elsewhere means nothing. Pass 7213 printed
  conclusions in exactly this situation; that is the reporting bug being fixed here.""")
    else:
        for q in (7, 9):
            if q in results:
                r = results[q]
                verdict = ("|Stab(O)| = 2, the involution IS symplectic" if r["realised"]
                           else "|Stab(O)| = 1, the automorphism is combinatorial only")
                print(f"  q={q}: {verdict}")

    out = ROOT / "data" / "PART_W33_PASS7214_INVOLUTION_FIXED.json"
    out.write_text(json.dumps(
        {"boundary": ("decides whether the Aut-bounding automorphism is symplectic. NO "
                      "verdict is issued unless the q=3 control, where |Stab| = 18 is known "
                      "exactly, detects symplectic maps"),
         "fixes": ("Pass 7213 built M with the frame treated as the standard basis; the "
                   "correct map is Fm . diag(lam) . A^{-1}. It also printed verdicts after "
                   "its own control failed"),
         "control_passes": ok, "results": results}, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
