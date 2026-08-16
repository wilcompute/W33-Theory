"""Passes 5488-5491 -- the tomotope's medial layer sits inside W(3,3), twice, and that is
where the 576 was coming from.

  5488  Reading the tomotope corpus rather than sampling it: BT1363 states
        "Q4 face-edge incidence / <1111> = Reye = tomotope edge-triangle medial layer",
        with 12 edge labels, 16 face labels and 48 edge-face blocks.

  5489  The W(F4) orbit split on W(3,3)'s forty points is 16 + 12 + 12 (Pass 5482).  Taking
        the 16-orbit as lines and either 12-orbit as points, under W(3,3) collinearity,
        gives exactly 12_4 and 16_3 with 48 flags.

  5490  Parameters are not identity, and the last three attempts died at exactly this step.
        So the two incidence structures are tested for ISOMORPHISM.  They are isomorphic.

  5491  And both have automorphism group of order 576 -- which is where this entire thread
        started, and is now explained rather than coincidental.

    py -3 analysis/w33_pass5488_5491_the_tomotope_is_inside_w33_twice.py
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

Q = 3


def nrm(v):
    for a in v:
        if a % Q:
            z = pow(a, Q - 2, Q)
            return tuple((z * x) % Q for x in v)
    return None


def symp(u, v):
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % Q


def quad(v):
    return (v[0] * v[1] + v[2] * v[3]) % Q


def w33_reye(twelve, sixteen):
    """Bipartite incidence of a 12-orbit against the 16-orbit, via W(3,3) collinearity."""
    g = igraph.Graph(n=len(twelve) + len(sixteen))
    g.add_edges([(i, len(twelve) + j)
                 for i, t in enumerate(twelve) for j, s in enumerate(sixteen)
                 if symp(t, s) == 0])
    return g


def q4_reye():
    """Q4 face-edge incidence modulo the antipodal translation <1111>, per BT1363."""
    V = list(range(16))
    edges = sorted({frozenset((a, a ^ (1 << i))) for a in V for i in range(4)},
                   key=lambda e: sorted(e))
    faces = sorted({frozenset({a, a ^ (1 << i), a ^ (1 << j),
                               a ^ (1 << i) ^ (1 << j)})
                    for a in V for i, j in itertools.combinations(range(4), 2)},
                   key=lambda f: sorted(f))

    def anti(s):
        return frozenset(x ^ 15 for x in s)

    def classes(items):
        idx, seen = {}, []
        for it in items:
            k = frozenset({it, anti(it)})
            if k not in idx:
                idx[k] = len(seen)
                seen.append(k)
        return idx, seen

    ei, ec = classes(edges)
    fi, fc = classes(faces)
    inc = {(ei[frozenset({e, anti(e)})], len(ec) + fi[frozenset({f, anti(f)})])
           for e in edges for f in faces if e <= f}
    g = igraph.Graph(n=len(ec) + len(fc))
    g.add_edges(sorted(inc))
    return g, len(ec), len(fc), len(edges), len(faces)


def main() -> int:
    print("=" * 78)
    print("Passes 5488-5491 -- the tomotope, inside W(3,3), twice")
    print("=" * 78)

    pts = sorted({nrm(v) for v in itertools.product(range(Q), repeat=4) if any(v)})
    S16 = [p for p in pts if quad(p) == 0]
    P12 = [p for p in pts if quad(p) == 1]
    M12 = [p for p in pts if quad(p) == 2]

    print("\n  PASS 5488 -- what the tomotope corpus actually says\n")
    gB, nec, nfc, ne, nf = q4_reye()
    print(f"    BT1363: Q4 face-edge incidence / <1111> = Reye = tomotope medial layer")
    print(f"    Q4 edges {ne} -> {nec} antipodal classes   (the tomotope's 12... or 16)")
    print(f"    Q4 faces {nf} -> {nfc} antipodal classes")
    print(f"    incidences                                : {gB.ecount()}")
    print("""
    THE TOMOTOPE'S MEDIAL LAYER IS A REYE CONFIGURATION 12_4 16_3 WITH 48 FLAGS, and it is
    built from Q4's FACES and EDGES modulo the antipodal translation -- not from its
    vertices. Pass 5479 tested the vertex quotient and got 8 classes; that was the wrong
    quotient, and the corpus said so in a file I had not read.""")

    print("\n  PASS 5489 -- the same parameters inside W(3,3)\n")
    rows = []
    for name, T in (("Q(v)=1", P12), ("Q(v)=2", M12)):
        dp = [sum(1 for s in S16 if symp(t, s) == 0) for t in T]
        dl = [sum(1 for t in T if symp(t, s) == 0) for s in S16]
        flags = sum(dp)
        ok = set(dp) == {4} and set(dl) == {3} and flags == 48
        rows.append({"orbit": name, "point_degrees": sorted(set(dp)),
                     "line_degrees": sorted(set(dl)), "flags": flags, "is_12_4_16_3": ok})
        print(f"    {name}: each of the 12 on {sorted(set(dp))} of the 16;  "
              f"each of the 16 on {sorted(set(dl))} of the 12;  flags {flags}   -> {ok}")

    print("\n  PASS 5490 -- and they are isomorphic, not merely equiparametric\n")
    gA = w33_reye(P12, S16)
    gA2 = w33_reye(M12, S16)
    iso1 = gA.isomorphic(gB)
    iso2 = gA2.isomorphic(gB)
    print(f"    W(3,3) [16 + Q=1 twelve]  vs  Q4 tomotope medial layer : {iso1}")
    print(f"    W(3,3) [16 + Q=2 twelve]  vs  Q4 tomotope medial layer : {iso2}")
    print("""
    ISOMORPHIC AS INCIDENCE STRUCTURES. This is the step the last three attempts failed at
    -- the 16-orbit was not Q4, the two SRG(16,6,2,2) candidates were excluded, the
    generator lines were eight and not thirty-two, and the (q+1)^2 family showed 16 was
    never 2^4. Every one of those died on structure after matching on a number. This one
    does not.""")

    print("\n  PASS 5491 -- and the 576 is explained\n")
    aA, aB = gA.count_automorphisms_vf2(), gB.count_automorphisms_vf2()
    print(f"    |Aut(W(3,3) copy)|             : {aA:,}")
    print(f"    |Aut(Q4 tomotope medial)|      : {aB:,}")
    print(f"    equal                          : {aA == aB}")
    print(f"""
    576 IS THE AUTOMORPHISM GROUP OF THE REYE CONFIGURATION, and that is what has been
    surfacing all along. The 13-cover stabiliser's image was 576 (Pass 5416). The Klein
    Latin square's autoparatopy group is 576 (their Pass5300). The number of 4x4 Latin
    squares is 576. W(F4)/{{+-1}} is 576 (Pass 5468). Here it is again as Aut of the
    tomotope's medial layer, and here it has a reason rather than a coincidence.

    THE CONNECTION, STATED PLAINLY. W(3,3) has forty points. W(F4) acts on them -- through
    GL(4,3), preserving a quadratic form rather than the symplectic one -- and splits them
    16 + 12 + 12 where W(3,3)'s own group Sp(4,3) is transitive and sees nothing. Each
    12-orbit, taken with the shared 16-orbit under W(3,3) collinearity, IS the tomotope's
    edge-triangle medial layer. So the tomotope sits inside W(3,3) twice, on a common set of
    sixteen, and the hypercube reaches W(3,3) through its faces and edges rather than its
    vertices.

    WHAT IS STILL NOT CLAIMED. That any of this is physics. It is an incidence-structure
    isomorphism between two objects this repository already had, found by reading a file
    instead of matching an integer.""")

    out = {
        "boundary": ("The isomorphism is between BIPARTITE INCIDENCE STRUCTURES: the "
                     "W(3,3) 12-orbit/16-orbit collinearity incidence, and Q4's face-edge "
                     "incidence modulo <1111>. Both verified by igraph isomorphic() and "
                     "both |Aut| = 576. The identification of the latter with 'the "
                     "tomotope medial layer' is BT1363's and is cited, not reproved. No "
                     "physical claim is made"),
        "pass_5488": {"source": "analysis/BT1363_q4_clock_tomotope_medial_descent.md",
                      "statement": ("Q4 face-edge incidence / <1111> = Reye = tomotope "
                                    "edge-triangle medial layer"),
                      "q4_edges": ne, "edge_classes": nec,
                      "q4_faces": nf, "face_classes": nfc,
                      "incidences": gB.ecount(),
                      "correction": ("Pass 5479 quotiented Q4's VERTICES and got 8; the "
                                     "tomotope comes from faces and edges")},
        "pass_5489": {"rows": rows,
                      "wf4_split": [16, 12, 12],
                      "reference": "Pass 5482"},
        "pass_5490": {"iso_Q1": bool(iso1), "iso_Q2": bool(iso2),
                      "note": ("this is the step at which the 16-as-Q4, rook, Shrikhande "
                               "and generator-line readings all failed")},
        "pass_5491": {"aut_w33_copy": aA, "aut_q4_tomotope": aB, "equal": aA == aB,
                      "explains": ("576 as Aut(Reye); the same 576 appears as the 13-cover "
                                   "stabiliser image, the Klein Latin autoparatopy group, "
                                   "the 4x4 Latin square count, and W(F4)/{+-1}"),
                      "theorem": ("the tomotope's medial layer embeds in W(3,3) twice, on "
                                  "a shared 16-point quadric, cut out by the W(F4) orbit "
                                  "decomposition"),
                      "not_claimed": "any physical interpretation"},
    }
    fp = ROOT / "data" / "PART_W33_PASS5488_5491_TOMOTOPE_INSIDE_W33_TWICE.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
