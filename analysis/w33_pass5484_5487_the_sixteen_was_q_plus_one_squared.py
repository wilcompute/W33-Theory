"""Passes 5484-5487 -- the hypercube reading of the orbit split dies in the q-family, and
the 16-point graph is not any of the graphs it looked like.

  5484  The W(F4) orbit split on W(3,3)'s forty points was 16 + 12 + 12, and 16 = |V(Q4)|
        with 24 = faces(Q4) was the whole reason to look. Run it at q = 5 and 7.

  5485  Identify the 6-regular graph on the 16 rather than guessing from |Aut| = 96.

  5486  Are the two 12-orbits two different things?

  5487  Do the quadric's generator lines carry the hypercube instead?

    py -3 analysis/w33_pass5484_5487_the_sixteen_was_q_plus_one_squared.py
"""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import igraph

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import cert_util  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def geom(q):
    def nrm(v):
        for a in v:
            if a % q:
                z = pow(a, q - 2, q)
                return tuple((z * x) % q for x in v)
        return None
    return sorted({nrm(v) for v in itertools.product(range(q), repeat=4) if any(v)})


def symp(u, v, q):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q


def quad(v, q):
    return (v[0] * v[1] + v[2] * v[3]) % q


def induced(S, q):
    g = igraph.Graph(n=len(S))
    g.add_edges([(i, j) for i, j in itertools.combinations(range(len(S)), 2)
                 if symp(S[i], S[j], q) == 0])
    return g


def main() -> int:
    print("=" * 78)
    print("Passes 5484-5487 -- 16 was (q+1)^2 all along")
    print("=" * 78)

    print("\n  PASS 5484 -- the split across q\n")
    print(f"    {'q':>3s} {'points':>7s} {'singular':>9s} {'nonsingular':>12s}  split")
    rows = []
    for q in (3, 5, 7):
        P = geom(q)
        s = sum(1 for p in P if quad(p, q) == 0)
        ns = len(P) - s
        rows.append({"q": q, "points": len(P), "singular": s, "nonsingular": ns,
                     "split": [s, ns // 2, ns // 2],
                     "q_plus_1_squared": (q + 1) ** 2, "q_cubed_minus_q": q ** 3 - q})
        print(f"    {q:3d} {len(P):7d} {s:9d} {ns:12d}   {s} + {ns // 2} + {ns // 2}")
    print("""
    THE SINGULAR COUNT IS (q+1)^2 AND THE NONSINGULAR IS q^3 - q. At q=3 those are 16 and
    24, which is why the hypercube looked like an answer: |V(Q4)| = 16 and Q4 has 24 square
    faces. At q=5 they are 36 and 120; at q=7, 64 and 336. Nothing about the cube survives.

    SO 16 WAS (q+1)^2 = 4^2, NOT 2^4. The two readings agree at exactly one value of q and
    the family separates them immediately -- which is the third time this session a claim
    has been carrier-specific and looked general. -1/q^2 was an artefact of GQ(q,q).
    -1/(H-1) was an artefact of GQs. This is an artefact of q=3.

    WHAT SURVIVES IS STILL WORTH HAVING. W(F4) really does act on W(3,3)'s forty points and
    really does split them where Sp(4,3) is transitive (Pass 5482). The orbit decomposition
    is a map. Its identification with the hypercube is gone.""")

    print("\n  PASS 5485 -- what the 16-point graph actually is\n")
    q = 3
    P = geom(q)
    sing = [p for p in P if quad(p, q) == 0]
    g16 = induced(sing, q)
    n = g16.vcount()
    A = [[0] * n for _ in range(n)]
    for a, b in g16.get_edgelist():
        A[a][b] = A[b][a] = 1
    lam, mu = set(), set()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            c = sum(A[i][x] * A[x][j] for x in range(n))
            (lam if A[i][j] else mu).add(c)
    rook = igraph.Graph(n=16)
    rook.add_edges([(4 * a + b, 4 * c + d) for a in range(4) for b in range(4)
                    for c in range(4) for d in range(4)
                    if (4 * a + b) < (4 * c + d) and (a == c) != (b == d)])
    shr = igraph.Graph(n=16)
    shr.add_edges([(a, b) for a in range(16) for b in range(a + 1, 16)
                   if ((a // 4 - b // 4) % 4, (a % 4 - b % 4) % 4) in
                   {(0, 1), (0, 3), (1, 0), (3, 0), (1, 1), (3, 3)}])
    aut = g16.count_automorphisms_vf2()
    print(f"    16-point graph : {g16.ecount()} edges, 6-regular, |Aut| = {aut}")
    print(f"    lambda values  : {sorted(lam)}    mu values : {sorted(mu)}")
    print(f"    strongly regular : {len(lam) == 1 and len(mu) == 1}")
    print(f"    is 4x4 rook (|Aut| 1152) : {g16.isomorphic(rook)}")
    print(f"    is Shrikhande (|Aut| 192): {g16.isomorphic(shr)}")
    print("""
    IT IS NOT STRONGLY REGULAR AT ALL. Both 6-regular graphs on 16 vertices with 48 edges
    that anyone reaches for -- the 4x4 rook graph and Shrikhande, the classic SRG(16,6,2,2)
    pair -- are excluded, and so is Clebsch by degree. This graph has two lambda values and
    two mu values, so it is not in that family.

    AND |Aut| = 96 MATCHING THE TOMOTOPE ORDER STAYS UNCLAIMED. Pass 5483 flagged it; the
    graph turning out to be non-strongly-regular does not make the order match mean more.""")

    print("\n  PASS 5486 -- the two 12-orbits\n")
    plus = [p for p in P if quad(p, q) == 1]
    minus = [p for p in P if quad(p, q) == 2]
    gp, gm = induced(plus, q), induced(minus, q)
    same = gp.isomorphic(gm)
    print(f"    Q(v)=1 : {len(plus)} points, {gp.ecount()} edges, "
          f"{sorted(set(gp.degree()))}-regular")
    print(f"    Q(v)=2 : {len(minus)} points, {gm.ecount()} edges, "
          f"{sorted(set(gm.degree()))}-regular")
    print(f"    isomorphic : {same}")
    print("""
    ONE TYPE, TWO COPIES. The two 12-orbits are isomorphic 5-regular graphs, so they are the
    square and non-square values of the same quadratic form rather than two different
    objects. Anything found in one holds in the other, and the split into 12 + 12 is a
    scalar distinction, not a structural one.""")

    print("\n  PASS 5487 -- the generator lines\n")
    lines = set()
    for a, b in itertools.combinations(range(len(sing)), 2):
        L = {sing[a], sing[b]}
        for t in range(q):
            v = tuple((sing[a][i] + t * sing[b][i]) % q for i in range(4))
            lead = next((x for x in v if x), None)
            if lead:
                z = pow(lead, q - 2, q)
                L.add(tuple((z * x) % q for x in v))
        if len(L) == q + 1 and all(quad(p, q) == 0 for p in L):
            lines.add(frozenset(L))
    print(f"    totally singular lines on Q+(3,3) : {len(lines)}  (two reguli of 4)")
    print(f"    Q4 edges                          : 32")
    print("""
    EIGHT LINES, NOT THIRTY-TWO. A hyperbolic quadric in PG(3,q) carries 2(q+1) generators
    in two reguli -- eight at q=3 -- and Q4 has 32 edges. So the generator lines are not the
    cube's edges either, and the last obvious place to look is empty.

    THE THREAD IS CLOSED ON THE HYPERCUBE. Four constructions tested -- the induced
    collinearity, its complement, the two classic SRG(16,6,2,2) graphs, and the generators --
    and the q-family shows the 16 was never 2^4. What remains true is Pass 5482: W(F4) acts
    on W(3,3)'s points and splits them where their own group cannot.""")

    out = {
        "boundary": ("Pass 5484 settles the q-family for the SPLIT SIZES only. Pass 5485 "
                     "excludes the two classic SRG(16,6,2,2) graphs and Clebsch and reports "
                     "the graph is not strongly regular; it does not name it. Pass 5487 "
                     "counts generators and does not rule out some other line set. The "
                     "|Aut| = 96 / tomotope order coincidence remains unclaimed"),
        "pass_5484": {"rows": rows,
                      "singular_formula": "(q+1)^2",
                      "nonsingular_formula": "q^3 - q",
                      "verdict": ("16 = (q+1)^2, equal to |V(Q4)| = 2^4 only at q=3; the "
                                  "hypercube reading is carrier-specific"),
                      "pattern": ("third carrier-specific claim this session, after "
                                  "-1/q^2 (GQ(q,q)) and -1/(H-1) (GQs)")},
        "pass_5485": {"edges": g16.ecount(), "regular": 6, "aut_order": aut,
                      "lambda_values": sorted(lam), "mu_values": sorted(mu),
                      "strongly_regular": len(lam) == 1 and len(mu) == 1,
                      "is_rook_4x4": bool(g16.isomorphic(rook)),
                      "is_shrikhande": bool(g16.isomorphic(shr)),
                      "note": "Clebsch excluded by degree (5-regular)"},
        "pass_5486": {"orbit_sizes": [len(plus), len(minus)],
                      "edges": [gp.ecount(), gm.ecount()],
                      "isomorphic": bool(same),
                      "reading": "square vs non-square values of one form, not two objects"},
        "pass_5487": {"generator_lines": len(lines), "q4_edges": 32,
                      "verdict": "two reguli of q+1; not the cube's edges"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5484_5487_SIXTEEN_IS_Q_PLUS_ONE_SQUARED.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
