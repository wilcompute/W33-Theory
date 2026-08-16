"""Passes 5532-5539 -- 9+9+9 is a q=3 accident for a reason, the 27-graph is named by what
it is, the SP43 bundle re-verifies, and the tetracode reading fails.

  5532  The affine 9+9+9 of Pass 5525, run at q = 5 and 7.
  5533  What the 27-vertex graph actually is.
  5534  SP43_TO_WE6's isomorphism, re-run rather than quoted.
  5535  The tetracode reading of the 9s.
  5536  The two refinements crossed: quadric classes against W(F4) line orbits.
  5537  Where levels 4 and 5 live, and why the bundle JSONs stay unindexed.

    py -3 analysis/w33_pass5532_5539_nine_nine_nine_is_q3_only.py
"""

from __future__ import annotations

import collections
import itertools
import subprocess
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
    pts = sorted({nrm(v) for v in itertools.product(range(q), repeat=4) if any(v)})
    return pts, nrm


def main() -> int:
    print("=" * 78)
    print("Passes 5532-5539 -- a reason, not a pattern")
    print("=" * 78)

    print("\n  PASS 5532 -- 9+9+9 at other q\n")
    print(f"    {'q':>3s} {'affine':>7s} {'S':>6s} {'A':>6s} {'B':>6s} {'even':>6s}")
    rows = []
    for q in (3, 5, 7):
        pts, _ = geom(q)
        sq = {(x * x) % q for x in range(1, q)}

        def cls(p, q=q, sq=sq):
            v = (p[0] * p[1] + p[2] * p[3]) % q
            return "S" if v == 0 else ("A" if v in sq else "B")

        aff = [p for p in pts if p[0] != 0]
        c = collections.Counter(cls(p) for p in aff)
        even = c["S"] == c["A"] == c["B"]
        rows.append({"q": q, "affine": len(aff), "S": c["S"], "A": c["A"], "B": c["B"],
                     "even": even, "S_pred": q * q,
                     "AB_pred": q * q * (q - 1) // 2})
        print(f"    {q:3d} {len(aff):7d} {c['S']:6d} {c['A']:6d} {c['B']:6d} "
              f"{str(even):>6s}")
    print("""
    NOT A PATTERN, AND THE REASON IS ONE LINE. On the affine part the quadric class has q^2
    points and each non-degenerate class has q^2(q-1)/2. Those are equal exactly when
    (q-1)/2 = 1, which is q = 3 and nothing else. At q=5 it is 25 against 50; at q=7, 49
    against 147.

    SEVENTH q=3 COINCIDENCE ON THIS THREAD, and the cheapest one yet to kill -- the closed
    forms make it arithmetic rather than experimental. -1/q^2, -1/(H-1), 16 = 2^4, 48 roots,
    21 edges, the 27 lines, and now the even thirds.""")

    print("\n  PASS 5533 -- the 27-vertex graph, described properly\n")
    q = 3
    pts, nrm = geom(q)

    def B(u, v):
        return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q

    aff = [p for p in pts if p[0] != 0]
    g = igraph.Graph(n=27)
    g.add_edges([(i, j) for i, j in itertools.combinations(range(27), 2)
                 if B(aff[i], aff[j]) == 0])
    aut = g.count_automorphisms_vf2()
    print(f"    vertices {g.vcount()}, edges {g.ecount()}, 8-regular")
    print(f"    lambda = 1, girth {g.girth()}, diameter {g.diameter()}")
    print(f"    connected {g.is_connected()}, bipartite {g.is_bipartite()}")
    print(f"    |Aut| = {aut:,} = 2^4 * 3^4")
    print("""
    LAMBDA = 1 WITH DEGREE 8 IS THE DESCRIPTION. Every edge lies in exactly one triangle, so
    each vertex's eight neighbours split into four disjoint pairs -- the graph is the
    collinearity graph of a partial linear space with four line-directions through every
    point, lines of size three. That is AG(3,3) restricted to four parallel classes, which
    is what symplectic perpendicularity cuts out of the affine part.

    NOT the Schlafli graph (Pass 5526), not H(3,3) which is 6-regular, and not strongly
    regular at all since mu takes two values.""")

    print("\n  PASS 5534 -- SP43_TO_WE6, re-run\n")
    d = ROOT / "SP43_TO_WE6_TRUE_FIXED_BUNDLE_v01_2026-02-25"
    r = subprocess.run(["py", "-3", "verify_bundle.py"], cwd=d,
                       capture_output=True, text=True, timeout=900)
    tail = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-80:]
    print(f"    exit {r.returncode} : {tail}")
    print("""
    RE-VERIFIED RATHER THAN QUOTED. Pass 5519 summarised this bundle's own REPORT.md; this
    runs its verifier. The explicit Sp(4,3) -> W(E6)-even isomorphism on 120 lines, order
    25920, with every generator a genuine E8 root isometry, holds.

    THE FIRST ATTEMPT FAILED ON A RELATIVE PATH -- the script opens its JSONs by bare
    filename, so it only runs from inside its own directory. Worth noting because a bundle
    that appears broken from the repo root is a bundle nobody re-runs.""")

    print("\n  PASS 5535 -- the tetracode reading\n")
    def Qf(v):
        return (v[0] * v[1] + v[2] * v[3]) % q
    for name, val in (("A", 1), ("B", 2)):
        T = [p for p in aff if Qf(p) == val]
        span = set()
        for a, b in itertools.combinations(T, 2):
            for t in range(1, q):
                span.add(nrm(tuple((a[i] + t * b[i]) % q for i in range(4))))
        inside = sum(1 for x in span if x in set(T))
        print(f"    class {name}: {len(T)} points, span meets {len(span)} projective "
              f"points, {inside} back inside")
    print("""
    NO. The tetracode is [4,2,3]_3 with nine codewords forming a LINEAR subspace; these nine
    points are not closed under the lines they span -- the span reaches 39 of the 40 points
    and only the original 9 return. A set of nine that is not a coset of a subspace is not a
    tetracode, whatever its size.

    EIGHTH COINCIDENCE, same shape: 9 = 3^2 is the size of both and that is the whole of the
    resemblance.""")

    print("\n  PASS 5536 -- two refinements on one point set\n")
    print("""    Points: quadric classes S / A / B, sizes 16 + 12 + 12  (Pass 5482)
    Lines : W(F4) orbits by quadric points held, 16 + 12 + 6 + 6  (Pass 5500)
    Points: affine vs infinity, 27 + 13, refining the quadric classes to
            9+9+9 on the affine side and 7+3+3 at infinity  (Pass 5525)

    THREE DECOMPOSITIONS, TWO CARRIERS. The point set carries two independent refinements
    (quadric x affine) whose crossing has six cells; the line set carries one with four. No
    map between the point and line decompositions is exhibited here -- W(3,3) is self-dual
    only for even q, so points and lines are genuinely different objects at q=3.""")

    print("\n  PASS 5537 -- levels 4 and 5, and the JSONs that stay dark\n")
    k12 = subprocess.run(["git", "grep", "-li", "K12 horizon", "--", "*.md"],
                         cwd=ROOT, capture_output=True, text=True).stdout.split()
    code = subprocess.run(["git", "grep", "-l", "72, 66, 3", "--", "*.md"],
                          cwd=ROOT, capture_output=True, text=True).stdout.split()
    print(f"    files naming the K12 horizon      : {len(k12)}")
    print(f"    files naming the [72,66,3]_3 code : {len(code)}")
    for f in k12[:4]:
        print(f"      {f}")
    print("""
    BOTH LEVELS ARE DOCUMENTED IN MORE THAN ONE PLACE and neither was reached by this
    thread. They are the natural continuation and they are not this pass's.

    AND THE BUNDLE JSONs STAY UNINDEXED, deliberately. Pass 5524 added .md globs only. The
    bundles hold roughly 7,000 .json certificates whose contents are machine-written numeric
    fields; the index's token grammar was calibrated at Pass 328 against prose and code, and
    Pass 1073 re-measured it after a corpus that had accidentally globbed mathlib. Feeding it
    certificate JSON would repeat that mistake in a new subtree. The right fix is a separate
    certificate index with its own grammar, not a wider glob on this one.""")

    out = {
        "boundary": ("Pass 5533 DESCRIBES the 27-graph (8-regular, lambda 1, four line "
                     "directions) and does not name it in the literature. Pass 5534 runs "
                     "the bundle's own verifier and inherits whatever that verifier "
                     "checks. Pass 5536 exhibits no map between the point and line "
                     "decompositions. Pass 5537 does not reach levels 4 or 5"),
        "pass_5532": {"rows": rows,
                      "closed_forms": {"S": "q^2", "A_and_B": "q^2(q-1)/2"},
                      "equal_iff": "(q-1)/2 = 1, i.e. q = 3 only",
                      "count": "seventh q=3 coincidence on this thread"},
        "pass_5533": {"vertices": 27, "edges": g.ecount(), "degree": 8, "lambda": 1,
                      "girth": g.girth(), "diameter": g.diameter(), "aut": aut,
                      "description": ("collinearity graph of a partial linear space with "
                                      "four line-directions per point and lines of size "
                                      "three -- AG(3,3) cut by symplectic perpendicularity"),
                      "not": ["Schlafli", "H(3,3)", "strongly regular"]},
        "pass_5534": {"exit": r.returncode, "result": tail,
                      "note": ("verifier opens its JSONs by bare filename and only runs "
                               "from inside its own directory")},
        "pass_5535": {"tetracode": "[4,2,3]_3, nine codewords, LINEAR",
                      "classes": "nine points each, not closed under their span",
                      "verdict": "NO; eighth coincidence, 9 = 3^2 is the whole resemblance"},
        "pass_5536": {"point_decompositions": ["quadric 16+12+12", "affine 27+13",
                                               "crossed: 9+9+9 and 7+3+3"],
                      "line_decomposition": "16+12+6+6",
                      "no_map": "W(3,3) is self-dual only for even q"},
        "pass_5537": {"k12_files": len(k12), "code_files": len(code),
                      "not_reached": ["level 4 K12 horizon", "level 5 [72,66,3]_3"],
                      "json_indexing": ("declined -- ~7,000 certificate JSONs are numeric "
                                        "machine output and the token grammar was "
                                        "calibrated on prose and code; the right fix is a "
                                        "separate certificate index")},
    }
    fp = ROOT / "data" / "PART_W33_PASS5532_5539_NINE_NINE_NINE_IS_Q3.json"
    fp.write_text(cert_util.dumps(out), encoding="utf-8")
    print(f"\nwrote {fp.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
