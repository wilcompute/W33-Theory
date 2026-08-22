"""Pass 7213 -- is the |Stab| <= 2 involution actually a symplectic map?

THE GAP. Pass 7199 bounded Stab(O) by embedding it into Aut of the edge-coloured complete
graph on O, and got |Aut| = 2 at q=7 and q=9. That leaves the stabilizer at order 1 or 2, and
which one is not decided: a graph automorphism preserving a combinatorial invariant need NOT
come from a symplectic map. Pass 7203 pinned q=3 exactly (18) by enumerating Sp(4,3), but
|Sp(4,7)| = 276,595,200 and |Sp(4,9)| = 3,443,212,800, so enumeration is out.

THE METHOD, which needs no group enumeration at all. A projectivity of PG(3,q) is determined
by a FRAME -- five points in general position. So take a frame inside O, apply the unique
nontrivial graph automorphism pi to it, and build the one projectivity M carrying frame to
image. Explicitly, with e5 = sum c_i e_i and f5 = sum d_i f_i (all coefficients nonzero by
general position), M sends e_i to (d_i/c_i) f_i, which is forced.

Then two checks decide it:

    1. is M a SIMILITUDE of the symplectic form -- B(Mu,Mv) = mu * B(u,v) for a fixed mu?
       (a projectivity preserves W(3,q) exactly when it is; plain invariance is too strong,
        since projective points absorb scalars)
    2. does M map O onto O setwise?

If both hold the stabilizer has order exactly 2 and the involution is real. If either fails
for every frame, pi is combinatorial only and the stabilizer is TRIVIAL. Either way the
bound becomes an equality.

CONTROL: the same computation is run at q=3, where Pass 7203 established |Stab| = 18 by brute
force. The method must find symplectic maps there. If it finds none at q=3 it is broken and
its q=7 verdict is discarded.

    py -3 analysis/w33_pass7213_is_the_involution_real.py
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


def graph_automorphisms(k, colour):
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher, categorical_edge_match
    G = nx.Graph()
    G.add_nodes_from(range(k))
    for i in range(k):
        for j in range(i + 1, k):
            G.add_edge(i, j, c=colour[(i, j)])
    gm = GraphMatcher(G, G, edge_match=categorical_edge_match("c", None))
    return list(gm.isomorphisms_iter())


def rank_of(F, rows):
    M = [list(r) for r in rows]
    r = 0
    for c in range(4):
        piv = next((i for i in range(r, len(M)) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = F.inv[M[r][c]]
        M[r] = [F.mul[x][iv] for x in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [F.add[M[i][j]][F.neg[F.mul[f][M[r][j]]]] for j in range(4)]
        r += 1
    return r


def solve_coords(F, basis, target):
    """write target = sum c_i basis_i over GF(q); returns None if not solvable."""
    M = [[basis[j][i] for j in range(4)] + [target[i]] for i in range(4)]
    r = 0
    where = {}
    for c in range(4):
        piv = next((i for i in range(r, 4) if M[i][c]), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        iv = F.inv[M[r][c]]
        M[r] = [F.mul[x][iv] for x in M[r]]
        for i in range(4):
            if i != r and M[i][c]:
                f = M[i][c]
                # range(5): the augmented column must be eliminated too
                M[i] = [F.add[M[i][j]][F.neg[F.mul[f][M[r][j]]]] for j in range(5)]
        where[c] = r
        r += 1
    if r < 4:
        return None
    return [M[where[c]][4] for c in range(4)]


def main() -> int:
    print("=" * 78)
    print("Pass 7213 -- is the |Stab| <= 2 involution a real symplectic map?")
    print("=" * 78)

    results = {}
    for q in (3, 7, 9):
        fp = ROOT / SOURCES[q]
        if not fp.is_file():
            continue
        F = Field(q)
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
        autos = graph_automorphisms(k, colour)
        nontrivial = [a for a in autos if any(a[i] != i for i in range(k))]
        print(f"\n  q={q}: |O| = {k}, graph automorphisms = {len(autos)} "
              f"({len(nontrivial)} nontrivial)", flush=True)

        realised = 0
        witness = None
        for a in nontrivial[:40]:
            # find a frame inside O: 4 independent points + a 5th in general position
            found = False
            for quad in itertools.combinations(range(k), 4):
                basis = [P[O[i]] for i in quad]
                if rank_of(F, basis) != 4:
                    continue
                for fifth in range(k):
                    if fifth in quad:
                        continue
                    c = solve_coords(F, basis, P[O[fifth]])
                    if c is None or any(x == 0 for x in c):
                        continue
                    fbasis = [P[O[a[i]]] for i in quad]
                    if rank_of(F, fbasis) != 4:
                        continue
                    d = solve_coords(F, fbasis, P[O[a[fifth]]])
                    if d is None or any(x == 0 for x in d):
                        continue
                    lam = [F.mul[d[i]][F.inv[c[i]]] for i in range(4)]
                    cols = [[F.mul[lam[i]][fbasis[i][r]] for r in range(4)]
                            for i in range(4)]
                    M = tuple(tuple(cols[i][r] for i in range(4)) for r in range(4))
                    found = True
                    break
                if found:
                    break
            if not found:
                continue

            def apply(M, p):
                img = tuple(F.dot(M[i], p) for i in range(4))
                lead = next((x for x in img if x), None)
                if lead is None:
                    return None
                iv = F.inv[lead]
                return tuple(F.mul[x][iv] for x in img)

            # similitude test: B(Mu,Mv) = mu * B(u,v) for a single fixed mu
            mu = None
            ok = True
            for u, v in itertools.combinations(range(min(n, 60)), 2):
                bu = B(P[u], P[v])
                iu = apply(M, P[u])
                iv2 = apply(M, P[v])
                if iu is None or iv2 is None:
                    ok = False
                    break
                bv = B(iu, iv2)
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
            img = {idx[apply(M, P[p])] for p in O}
            if img == Oset:
                realised += 1
                witness = (M, mu)

        print(f"    nontrivial automorphisms realised by a symplectic similitude: "
              f"{realised} of {len(nontrivial)}")
        exact = 1 + realised
        results[q] = {"aut_bound": len(autos), "nontrivial": len(nontrivial),
                      "realised": realised, "stab_order_from_this": exact}
        if q == 3:
            print(f"    CONTROL: Pass 7203 proved |Stab| = 18 at q=3 by enumerating Sp(4,3).")
            print(f"    This method finds {realised} of {len(nontrivial)} nontrivial "
                  f"automorphisms realised.")
            ctrl_ok = realised > 0
            print(f"    control {'PASSES' if ctrl_ok else 'FAILS'} -- "
                  f"{'symplectic maps are detected' if ctrl_ok else 'method detects none, so its q=7/q=9 verdicts are DISCARDED'}")
            results[q]["control_passes"] = ctrl_ok
        else:
            if realised:
                print(f"    -> |Stab(O)| = 2 exactly: the involution IS symplectic.")
            else:
                print(f"    -> the automorphism is COMBINATORIAL ONLY; "
                      f"|Stab(O)| = 1, the stabilizer is TRIVIAL.")

    ctrl = results.get(3, {}).get("control_passes")
    print(f"\n  VERDICT SUMMARY (valid only if the q=3 control passed: {ctrl})\n")
    for q, r in sorted(results.items()):
        print(f"    q={q}: Aut bound {r['aut_bound']}, "
              f"{r['realised']}/{r['nontrivial']} realised -> "
              f"|Stab| = {r['stab_order_from_this']}"
              + ("  [q=3 true value is 18, so this method LOWER-bounds]" if q == 3 else ""))

    out = ROOT / "data" / "PART_W33_PASS7213_INVOLUTION_REAL.json"
    out.write_text(json.dumps(
        {"boundary": ("decides whether the nontrivial automorphism bounding Stab(O) is "
                      "realised by a symplectic similitude. Valid only if the q=3 control "
                      "detects symplectic maps, since Pass 7203 proved |Stab|=18 there"),
         "method": ("a projectivity is determined by a frame; build the unique map on a "
                    "frame inside O and test (a) similitude of B, (b) O mapped onto O"),
         "results": results, "control_passes": ctrl}, indent=2), encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
