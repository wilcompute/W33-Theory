"""
W(3,3) -> 27 connection: a failed prediction, an honest report.
================================================================

I went looking for the deepest non-numerological mathematical fact
under the W(3,3) corpus and predicted the following: since PSp(4,3),
the automorphism group of W(3,3), is famously isomorphic to
W(E_6)/{+/- 1}, the 27 non-neighbours of any vertex of W(3,3) should
form the SCHLAEFLI GRAPH -- the unique SRG(27,16,10,8) whose
automorphism group is W(E_6)/{+/- 1} and whose vertices are the 27
lines on a smooth cubic surface. This would have made "27 = q^3 in
W(3,3)" the same 27 as the cubic-surface 27, by a classical theorem,
with one structural reason for the appearance of E_6 numerics.

The prediction is FALSE. Direct construction shows the 27 non-
neighbours of any W(3,3) vertex form a graph that is regular of
degree 8 (not 16) and is NOT strongly regular -- mu takes both values
0 and 3, lambda is 1. It is NOT the Schlaefli graph, and the W(3,3)
27 and the cubic-surface 27 are DIFFERENT rank-3 actions of related
groups, not the same set.

What this script actually verifies, honestly:

  (1) W(3,3) is SRG(40,12,2,4) by direct construction. TRUE.
  (2) For any vertex v, its 12 neighbours form 4 disjoint triangles
      (the 4 GQ(3,3) lines through v). TRUE, textbook.
  (3) For any vertex v, the induced graph on its 27 non-neighbours
      is 8-regular but NOT strongly regular. PREDICTION FAILED:
      this is NOT the Schlaefli graph.
  (4) PSp(4,3) ~= W(E_6)/{+/- 1} is still a classical theorem, but
      the 40-vertex action of PSp(4,3) on W(3,3) and its 27-line
      action on a cubic surface are DIFFERENT primitive actions of
      the same abstract group, with no direct subgraph-embedding.

I am reporting the failed prediction because:
  - it is the truth, and the brutal truth check already broke the
    cascade's central uniqueness pillar; one more honest negative
    result is the right next step;
  - it shows that even the deepest plausibly-real mathematical claim
    in the corpus (the W(3,3) -> 27 -> E_6 chain) doesn't survive
    direct verification in the form most often asserted;
  - the 8-regular graph that DOES sit on the 27 non-neighbours is
    interesting in its own right and is recorded here for future
    investigation (it has lambda=1, mu in {0, 3}, k=8).
"""

from __future__ import annotations

import json
from itertools import product
from pathlib import Path
from typing import Dict, List, Tuple


# ---------------------------------------------------------------------------
#  Construct W(3,3) from F_3^4 with the standard symplectic form.
# ---------------------------------------------------------------------------

def build_w33() -> Tuple[List[Tuple[int, ...]], List[List[int]]]:
    F = [0, 1, 2]
    nonzero = [v for v in product(F, repeat=4) if any(v)]

    # Reduce to projective points: keep one representative per F_3^* orbit.
    seen = set()
    points: List[Tuple[int, ...]] = []
    for v in nonzero:
        for x in v:
            if x != 0:
                inv = pow(x, -1, 3)
                rep = tuple((c * inv) % 3 for c in v)
                break
        if rep not in seen:
            seen.add(rep)
            points.append(rep)
    assert len(points) == 40

    def omega(a, b):
        return (a[0] * b[2] - a[2] * b[0] + a[1] * b[3] - a[3] * b[1]) % 3

    n = 40
    adj = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = adj[j][i] = 1
    return points, adj


# ---------------------------------------------------------------------------
#  Strongly regular graph parameter check on an arbitrary adjacency matrix.
# ---------------------------------------------------------------------------

def srg_parameters(adj: List[List[int]]) -> Dict[str, object]:
    n = len(adj)
    if n == 0:
        return dict(n=0, regular=False)

    degs = [sum(row) for row in adj]
    k = degs[0]
    if any(d != k for d in degs):
        return dict(n=n, regular=False, degrees=sorted(set(degs)))

    lam_set: set = set()
    mu_set: set = set()
    for i in range(n):
        for j in range(i + 1, n):
            common = sum(adj[i][t] & adj[j][t] for t in range(n))
            if adj[i][j]:
                lam_set.add(common)
            else:
                mu_set.add(common)

    if len(lam_set) <= 1 and len(mu_set) <= 1:
        lam = next(iter(lam_set)) if lam_set else 0
        mu = next(iter(mu_set)) if mu_set else 0
        return dict(
            n=n, k=k, lam=lam, mu=mu,
            is_srg=True,
            srg_params=(n, k, lam, mu),
            regular=True,
        )
    return dict(
        n=n, k=k,
        lam_observed=sorted(lam_set),
        mu_observed=sorted(mu_set),
        is_srg=False,
        regular=True,
    )


def induced_subgraph(adj: List[List[int]], vertices: List[int]) -> List[List[int]]:
    m = len(vertices)
    sub = [[0] * m for _ in range(m)]
    idx = {v: i for i, v in enumerate(vertices)}
    for v in vertices:
        for w in vertices:
            if v != w and adj[v][w]:
                sub[idx[v]][idx[w]] = 1
    return sub


def graph_complement(adj: List[List[int]]) -> List[List[int]]:
    n = len(adj)
    comp = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and not adj[i][j]:
                comp[i][j] = 1
    return comp


def is_disjoint_union_of_triangles(adj: List[List[int]]) -> bool:
    """Check whether a graph is a disjoint union of K_3's."""
    n = len(adj)
    if n % 3:
        return False
    seen = [False] * n
    for v in range(n):
        if seen[v]:
            continue
        nbrs = [u for u in range(n) if adj[v][u]]
        if len(nbrs) != 2:
            return False
        a, b = nbrs
        if not adj[a][b]:
            return False
        # The triangle should be the connected component of v
        # so a and b should each have only the other and v as neighbours.
        if sum(adj[a]) != 2 or sum(adj[b]) != 2:
            return False
        if not (adj[a][v] and adj[a][b] and adj[b][v] and adj[b][a]):
            return False
        seen[v] = seen[a] = seen[b] = True
    return all(seen)


# ---------------------------------------------------------------------------
#  Main verification
# ---------------------------------------------------------------------------

def verify_schlafli_bridge() -> Dict[str, object]:
    points, adj = build_w33()

    # (1) W(3,3) parameters
    w33 = srg_parameters(adj)
    assert w33["is_srg"], "W(3,3) construction failed: not SRG"
    assert w33["srg_params"] == (40, 12, 2, 4), f"got {w33['srg_params']}"

    # Pick a base vertex; by symmetry the result is independent of choice.
    v0 = 0
    neighbours = [u for u in range(40) if adj[v0][u]]
    non_neighbours = [u for u in range(40) if u != v0 and not adj[v0][u]]
    assert len(neighbours) == 12
    assert len(non_neighbours) == 27

    # (2) Local graph: 12 neighbours of v0
    local = induced_subgraph(adj, neighbours)
    local_check = srg_parameters(local)
    local_is_4_triangles = is_disjoint_union_of_triangles(local)

    # (3) PREDICTION: 27 non-neighbours = Schlaefli graph SRG(27,16,10,8)
    sub27 = induced_subgraph(adj, non_neighbours)
    sub27_params = srg_parameters(sub27)
    sub27_complement = graph_complement(sub27)
    sub27c_params = srg_parameters(sub27_complement)

    is_schlaefli = (
        sub27_params.get("srg_params") == (27, 16, 10, 8)
        or sub27c_params.get("srg_params") == (27, 16, 10, 8)
    )

    # Verify across multiple vertices that the 8-regular structure is invariant
    cross_check: List[Dict] = []
    for v in range(0, 40, 5):
        nn = [u for u in range(40) if u != v and not adj[v][u]]
        sg = induced_subgraph(adj, nn)
        sp = srg_parameters(sg)
        cross_check.append({
            "vertex": v,
            "k": sp.get("k"),
            "lam_observed": sp.get("lam_observed", [sp.get("lam")] if "lam" in sp else None),
            "mu_observed": sp.get("mu_observed", [sp.get("mu")] if "mu" in sp else None),
            "is_srg": sp.get("is_srg", False),
        })
    all_same_k = len({c["k"] for c in cross_check}) == 1

    return dict(
        title="W(3,3) -> 27 connection: failed prediction, honest report",
        method=(
            "Direct construction of W(3,3) from the symplectic form on F_3^4, "
            "induced subgraph on the 27 non-neighbours of an arbitrary vertex, "
            "computational SRG parameter check on this 27-vertex subgraph."
        ),

        w33_srg_params=list(w33["srg_params"]),

        local_neighbourhood={
            "size": 12,
            "regular": local_check.get("regular"),
            "valency": local_check.get("k"),
            "matches_lambda_2": local_check.get("k") == 2,
            "is_four_disjoint_triangles": local_is_4_triangles,
            "verdict": "TRUE -- textbook fact",
        },

        non_neighbourhood_27_PREDICTION={
            "predicted": "Schlaefli SRG(27,16,10,8) with Aut = W(E_6)/{+-1}",
            "actually_observed": {
                "n": sub27_params.get("n"),
                "k": sub27_params.get("k"),
                "lam_observed": sub27_params.get("lam_observed",
                                                 [sub27_params.get("lam")] if "lam" in sub27_params else None),
                "mu_observed": sub27_params.get("mu_observed",
                                                [sub27_params.get("mu")] if "mu" in sub27_params else None),
                "is_strongly_regular": sub27_params.get("is_srg", False),
            },
            "complement_observed": {
                "k": sub27c_params.get("k"),
                "lam_observed": sub27c_params.get("lam_observed"),
                "mu_observed": sub27c_params.get("mu_observed"),
                "is_strongly_regular": sub27c_params.get("is_srg", False),
            },
            "is_schlaefli": is_schlaefli,
            "verdict": "FALSE -- prediction failed.",
            "explanation": (
                "The 27 non-neighbours of any W(3,3) vertex form an 8-regular "
                "graph with lambda = 1 and mu in {0, 3}. It is NOT strongly "
                "regular and NOT the Schlaefli graph (which is 16-regular). "
                "The 27 here is NOT the cubic-surface 27."
            ),
        },

        vertex_invariance={
            "samples": cross_check,
            "all_give_same_k": all_same_k,
            "common_k": cross_check[0]["k"] if all_same_k else None,
            "comment": (
                "Even though the 27-graph is not SRG, it is the same regular "
                "graph at every vertex, so the structure is genuine -- it is "
                "just not the structure I predicted."
            ),
        },

        classical_fact_that_remains=(
            "PSp(4,3) ~= W(E_6)/{+-1} is still a classical theorem. But the "
            "40-vertex action on W(3,3) and the 27-line action on a cubic "
            "surface are DIFFERENT primitive actions of the same abstract "
            "group, with no direct subgraph embedding of one into the other. "
            "The W(3,3) -> E_6 connection is at the level of abstract "
            "groups, not geometric subobjects."
        ),

        what_actually_holds_up=[
            "W(3,3) is SRG(40,12,2,4); spectrum {12^1, 2^24, (-4)^15}.",
            "Local graph at any vertex is 4 disjoint triangles (4 lines of "
            "GQ(3,3) through that point).",
            "The 27 non-neighbours form a vertex-transitive 8-regular graph "
            "with parameters (k=8, lambda=1, mu in {0, 3}).",
            "PSp(4,3) ~= W(E_6)/{+-1} as abstract groups (classical theorem, "
            "not directly verified here).",
        ],

        what_does_NOT_hold_up=[
            "The 27 inside W(3,3) is NOT the cubic-surface 27 (failed here).",
            "There is no Schlaefli subgraph in W(3,3).",
            "The cascade's '27 = q^3 = E_6 fundamental rep' is therefore not "
            "structurally grounded in W(3,3) -- it is arithmetic coincidence.",
        ],

        honest_status=(
            "I went looking for the deepest non-numerological structural fact "
            "in the W(3,3) corpus, predicted that the 27 non-neighbours of "
            "any vertex would be the Schlaefli graph (which would tie "
            "'27 = q^3' to the cubic-surface 27 by a classical theorem), and "
            "directly verified that the prediction is FALSE. The 27-vertex "
            "subgraph is regular but not SRG. The W(3,3) -> 27 -> E_6 chain "
            "the cascade relies on does not survive direct computation. "
            "Combined with the brutal truth check (equipartition uniqueness "
            "is false), the 594-phase corpus contains: (a) a beautiful "
            "finite geometry, SRG(40,12,2,4); (b) some genuine polynomial "
            "identities for exceptional Lie algebra dimensions; (c) several "
            "post-hoc numerical matches; and (d) NO derivation of the "
            "Standard Model. That is the honest endpoint."
        ),
    )


def main() -> None:
    out = verify_schlafli_bridge()
    print("=" * 72)
    print("  W(3,3) -> 27 connection: failed prediction, honest report")
    print("=" * 72)
    print()
    print(f"  W(3,3) SRG params:        {tuple(out['w33_srg_params'])}  (verified)")
    print()
    loc = out["local_neighbourhood"]
    print(f"  Local graph (12 nbrs):    2-regular = {loc['matches_lambda_2']}, "
          f"4 disjoint triangles = {loc['is_four_disjoint_triangles']}  ({loc['verdict']})")
    print()
    pred = out["non_neighbourhood_27_PREDICTION"]
    obs = pred["actually_observed"]
    print(f"  27 non-neighbours of v0:")
    print(f"     predicted:             {pred['predicted']}")
    print(f"     actually:              k={obs['k']}, lambda={obs['lam_observed']}, "
          f"mu={obs['mu_observed']}, is_SRG={obs['is_strongly_regular']}")
    print(f"     verdict:               {pred['verdict']}")
    print()
    vi = out["vertex_invariance"]
    print(f"  Vertex-invariance:        all 8 sampled vertices give k={vi['common_k']}")
    print()
    print("-" * 72)
    print("  WHAT ACTUALLY HOLDS UP:")
    for s in out["what_actually_holds_up"]:
        print(f"    + {s}")
    print()
    print("  WHAT DOES NOT HOLD UP:")
    for s in out["what_does_NOT_hold_up"]:
        print(f"    - {s}")
    print()
    print("  HONEST STATUS:")
    print(f"    {out['honest_status']}")
    print()

    out_path = Path(__file__).resolve().parents[1] / "data" / "w33_schlafli_bridge.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, default=str)
    print(f"  Saved to {out_path}")


if __name__ == "__main__":
    main()
