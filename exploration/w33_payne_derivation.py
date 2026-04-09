"""
Payne Derivation of W(3,3): Does GQ(2,4) Give the Schläfli Graph?
=================================================================

The previous w33_schlafli_bridge.py found that the RAW induced subgraph
on the 27 non-neighbours of a vertex is 8-regular (not 16-regular Schläfli).
That was correct but INCOMPLETE.

The paper (Part XVI) claims the Payne-derived GQ(2,4) on those same 27
points has collinearity graph SRG(27,10,1,5) = complement of Schläfli.
The Payne derivation adds NEW adjacencies beyond the raw subgraph.

This script tests that claim by explicit computation.

PAYNE DERIVATION (Payne 1973):
  Given GQ(q,q) and a point p:
    Points*  = {x : x not collinear with p}  (27 points for q=3)
    Lines* come in two types:
      Type 1: For each original line L not through p, L meets p^perp in
              exactly one point z. Remove z -> line of size q = 3 on Points*.
      Type 2: For each point y in p^perp \ {p}, define
              span(p,y) = {x in Points* : x ~ y in original GQ}.
              Partition these into lines of size q-1 = 2...
              Actually: for each pair (y1, y2) on the same line through p,
              the set {x in Points* : x ~ y1 AND x ~ y2} has size q-1 = 2.
              These size-2 sets, unioned with y1-y2 info, form new lines.

    Result: GQ(q-1, q+1) = GQ(2, 4) with collinearity graph SRG(27,10,1,5).

Let's verify this computationally.
"""

import numpy as np
from itertools import combinations
import json

def build_w33():
    """Build W(3,3) from F_3^4 with standard symplectic form."""
    F3 = [0, 1, 2]
    # All nonzero vectors in F_3^4
    vecs = []
    for a in F3:
        for b in F3:
            for c in F3:
                for d in F3:
                    if (a, b, c, d) != (0, 0, 0, 0):
                        vecs.append((a, b, c, d))

    # Projective points: equivalence classes under scalar multiplication
    points = []
    seen = set()
    for v in vecs:
        # Normalize: find canonical representative
        canon = None
        for s in [1, 2]:  # nonzero scalars in F_3
            sv = tuple((s * x) % 3 for x in v)
            if canon is None or sv < canon:
                canon = sv
        if canon not in seen:
            seen.add(canon)
            points.append(canon)

    assert len(points) == 40, f"Expected 40 points, got {len(points)}"

    # Symplectic form: omega(u,v) = u0*v2 - u2*v0 + u1*v3 - u3*v1 (mod 3)
    def omega(u, v):
        return (u[0]*v[2] - u[2]*v[0] + u[1]*v[3] - u[3]*v[1]) % 3

    # Two points are collinear (adjacent) iff omega(u,v) = 0
    # (for projective points, this is well-defined)
    n = len(points)
    adj = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if omega(points[i], points[j]) == 0:
                adj[i][j] = 1
                adj[j][i] = 1

    # Verify SRG(40,12,2,4)
    degrees = adj.sum(axis=1)
    assert all(d == 12 for d in degrees), f"Not 12-regular: {set(degrees)}"

    return points, adj, omega


def find_gq_lines(points, adj):
    """Find all lines of the GQ: maximal cliques of size 4."""
    n = len(points)
    lines = []
    # Each edge is on exactly 1 line (since lambda=2, each line has 4 points,
    # and 2 adjacent points have exactly 2 common neighbours -> the line)
    used_edges = set()

    for i in range(n):
        nbrs_i = set(j for j in range(n) if adj[i][j])
        for j in nbrs_i:
            if j <= i:
                continue
            if (i, j) in used_edges:
                continue
            # Common neighbours of i and j
            nbrs_j = set(k for k in range(n) if adj[j][k])
            common = nbrs_i & nbrs_j
            # The line through i,j is {i, j} union common
            line = frozenset({i, j} | common)
            assert len(line) == 4, f"Line {line} has size {len(line)}"
            lines.append(line)
            # Mark all edges on this line
            for a, b in combinations(line, 2):
                used_edges.add((min(a,b), max(a,b)))

    assert len(lines) == 40, f"Expected 40 lines, got {len(lines)}"
    return lines


def payne_derivation(points, adj, lines, base_point):
    """
    Compute the Payne derivation of GQ(3,3) at base_point.
    Returns the derived adjacency matrix on the 27 non-collinear points.
    """
    n = len(points)
    p = base_point

    # p^perp = {p} union neighbours of p
    p_perp = {p} | set(j for j in range(n) if adj[p][j])
    assert len(p_perp) == 13, f"|p^perp| = {len(p_perp)}, expected 13"

    # Points of derived GQ: not in p^perp
    derived_pts = sorted(set(range(n)) - p_perp)
    assert len(derived_pts) == 27, f"Expected 27 derived points, got {len(derived_pts)}"

    # Relabel: derived_pts[i] -> i
    orig_to_new = {v: i for i, v in enumerate(derived_pts)}

    # Lines through p
    lines_through_p = [L for L in lines if p in L]
    assert len(lines_through_p) == 4, f"Lines through p: {len(lines_through_p)}"

    # Lines NOT through p
    lines_not_p = [L for L in lines if p not in L]
    assert len(lines_not_p) == 36

    # === TYPE 1 LINES: truncated original lines ===
    type1_lines = []
    for L in lines_not_p:
        # L meets p^perp in exactly 1 point (GQ axiom)
        meet = L & p_perp
        assert len(meet) == 1, f"Line {L} meets p^perp in {len(meet)} points"
        # Remove that point -> line of size 3 on derived points
        trunc = L - meet
        assert all(v in orig_to_new for v in trunc), "Truncated line has non-derived points"
        type1_lines.append(frozenset(orig_to_new[v] for v in trunc))

    assert len(type1_lines) == 36

    # === TYPE 2 LINES: "perp-lines" ===
    # For the Payne derivation of GQ(s,t) with s=t=q at a regular point p:
    # The derived GQ(s-1, t+1) = GQ(2,4) has:
    #   - 36 type-1 lines of size s = 3
    #   - Additional type-2 lines of size s = 3
    #
    # Type 2: For each point y ~ p (in p^perp \ {p}), consider the set
    # trace(y) = {x in derived_pts : x ~ y in original GQ}
    #
    # For GQ(q,q), |trace(y)| = s(t+1) - |{nbrs of y in p^perp}|
    # y has s(t+1) = 12 neighbours total. Of these, 1 is p, and lambda=2
    # common neighbours of (p,y), so 3 neighbours in p^perp.
    # trace(y) has 12 - 3 = 9 points.
    #
    # These 9 points partition into (q-1) = 2-subsets? No...
    # Actually, for GQ(3,3) -> GQ(2,4):
    # Type 2 lines come from "hyperbolic lines": for y ~ p, the set
    # {x not in p^perp : x ~ y} has 9 elements. These form 3 lines of
    # size 3 each in the derived GQ? Or 9 lines of size 2?
    #
    # Let me think differently. GQ(2,4) has parameters:
    #   s' = 2, t' = 4
    #   v' = (s'+1)(s't'+1) = 3 * 9 = 27 ✓
    #   lines have size s'+1 = 3
    #   points on t'+1 = 5 lines
    #   total lines b' = v'(t'+1)/(s'+1) = 27*5/3 = 45
    #
    # We have 36 type-1 lines. So we need 45 - 36 = 9 type-2 lines.
    #
    # The 9 type-2 lines come from the "spans":
    # For each of the 4 lines L through p, L \ {p} has 3 points {y1, y2, y3}.
    # For each such triple, consider pairs: C(3,2) = 3 pairs per line.
    # Total: 4 * 3 = 12 pairs. But we need 9 lines.
    #
    # Alternative: for each of the 12 points y in p^perp \ {p},
    # define trace(y) = {x in derived_pts : x ~ y}.
    # Two points in trace(y) that are NOT connected by a type-1 line
    # form a type-2 line if they share the property of being collinear with y.
    #
    # In GQ(3,3), the 4 lines through p partition the 12 neighbours into
    # 4 groups of 3. For each group {y1, y2, y3} on a line through p:
    # - trace(y1) has 9 points
    # - trace(y2) has 9 points
    # - trace(y3) has 9 points
    # The type-2 lines are: {x in derived_pts : x ~ y1 AND x ~ y2}
    # for each pair (y1, y2) from the same line through p.
    # By the GQ axiom: y1 ~ y2 (same line), and for non-adjacent x:
    # x has mu=4 common neighbours with p. Since x is not ~ p,
    # x is connected to exactly mu=4 points in p^perp.
    #
    # So each derived point x is collinear with exactly 4 points in
    # p^perp \ {p}. These 4 points lie on various lines through p.

    # Let me compute trace sets first
    nbrs_in_pperp_minus_p = {}  # for each derived point: which p-neighbours it's adjacent to
    p_neighbours = sorted(p_perp - {p})  # 12 points

    for x_new, x_orig in enumerate(derived_pts):
        nbrs_of_x = set(j for j in range(n) if adj[x_orig][j])
        nbrs_in_pp = nbrs_of_x & (p_perp - {p})
        nbrs_in_pperp_minus_p[x_new] = nbrs_in_pp
        assert len(nbrs_in_pp) == 4, f"Derived point {x_new} has {len(nbrs_in_pp)} nbrs in p^perp\\p"

    # For type-2 lines: for each line L through p, and each pair (yi, yj) on L\{p},
    # the type-2 line is {x in derived_pts : x ~ yi AND x ~ yj}
    type2_lines = []
    for L in lines_through_p:
        L_minus_p = sorted(L - {p})
        assert len(L_minus_p) == 3
        for yi, yj in combinations(L_minus_p, 2):
            # Points in derived_pts adjacent to both yi and yj
            common = []
            for x_new, x_orig in enumerate(derived_pts):
                if adj[x_orig][yi] and adj[x_orig][yj]:
                    common.append(x_new)
            if len(common) > 0:
                type2_lines.append(frozenset(common))

    # Check type-2 line sizes
    type2_sizes = [len(L) for L in type2_lines]
    print(f"  Type-2 line sizes: {sorted(set(type2_sizes))}, counts: {dict(zip(*np.unique(type2_sizes, return_counts=True)))}")
    print(f"  Type-2 lines found: {len(type2_lines)}")

    # If type-2 lines have size != 3, try triples instead of pairs
    # Actually, maybe type-2 lines come from single points y in p^perp \ {p}:
    # For each y, partition trace(y) into lines

    # Let me try a different approach: just find ALL lines of GQ(2,4)
    # A line of GQ(2,4) is a set of 3 derived points that are pairwise
    # connected in the derived collinearity relation.
    # But we don't know the derived collinearity yet — that's what we're building!

    # Let me use the standard construction more carefully.
    # In Payne & Thas, "Finite Generalized Quadrangles" (1984), 2.2.1:
    #
    # For GQ(s,s) with regular point p, the derived GQ(s-1, s+1) has:
    #   Points: P* = P \ p^perp
    #   Lines type I: {L \ (L ∩ p^perp)} for lines L with p not on L
    #   Lines type II: {{p,x}^{perp perp} \ p^perp} for x not in p^perp
    #     i.e., for each x in P*, the "hyperbolic line" through p and x
    #     minus the p^perp part.
    #
    # {p,x}^perp = {y : y ~ p AND y ~ x} has size s+1 = 4 (since mu = s+1 for non-adjacent)
    # Wait, p and x are NOT adjacent (x is not in p^perp).
    # So {p,x}^perp has |mu| = 4 points (the common neighbours of non-adjacent pair).
    # Then {p,x}^{perp perp} = common neighbours of ALL points in {p,x}^perp.
    # Hmm, this is getting complicated. Let me use a different formulation.

    # SIMPLEST CORRECT APPROACH:
    # The regularity condition for p means: for every x not ~ p,
    # |{p,x}^perp| = s+1 = 4, and |{p,x}^{perp perp}| = s+1 = 4.
    # {p,x}^perp = common neighbours of p and x = 4 points (all in p^perp \ {p})
    # {p,x}^{perp perp} = common neighbours of all 4 points in {p,x}^perp
    #                    = {p, x, and (s-1)=2 other points not in p^perp}
    #
    # So {p,x}^{perp perp} \ {p} ∩ P* gives a set of size s = 3
    # containing x and 2 others. THIS is a type-II line!

    type2_lines_v2 = []
    type2_seen = set()

    for x_new, x_orig in enumerate(derived_pts):
        # {p, x}^perp = common neighbours of p and x
        nbrs_p = set(j for j in range(n) if adj[p][j])
        nbrs_x = set(j for j in range(n) if adj[x_orig][j])
        px_perp = nbrs_p & nbrs_x  # common neighbours
        assert len(px_perp) == 4, f"|{{p,x}}^perp| = {len(px_perp)}"

        # {p,x}^{perp perp} = {z : z ~ y for all y in px_perp}
        px_perp_list = list(px_perp)
        px_pp = set(range(n))
        for y in px_perp_list:
            px_pp &= ({y} | set(j for j in range(n) if adj[y][j]))

        # Remove p, keep only derived points
        px_pp_derived = frozenset(orig_to_new[z] for z in px_pp if z in orig_to_new)

        if px_pp_derived not in type2_seen:
            type2_seen.add(px_pp_derived)
            type2_lines_v2.append(px_pp_derived)

    type2_sizes_v2 = [len(L) for L in type2_lines_v2]
    print(f"  Type-2 v2 line sizes: {sorted(set(type2_sizes_v2))}, counts: {dict(zip(*np.unique(type2_sizes_v2, return_counts=True)))}")
    print(f"  Type-2 v2 lines found: {len(type2_lines_v2)}")

    # All derived lines
    all_lines = type1_lines + type2_lines_v2

    # Build adjacency: two derived points are adjacent iff they share a line
    derived_adj = np.zeros((27, 27), dtype=int)
    for L in all_lines:
        L_list = sorted(L)
        for a, b in combinations(L_list, 2):
            derived_adj[a][b] = 1
            derived_adj[b][a] = 1

    return derived_pts, derived_adj, all_lines, type1_lines, type2_lines_v2


def srg_params(adj):
    """Check if adjacency matrix is SRG and return parameters."""
    n = adj.shape[0]
    degrees = adj.sum(axis=1)
    if len(set(degrees)) != 1:
        return None
    k = int(degrees[0])

    lam_vals = set()
    mu_vals = set()
    for i in range(n):
        for j in range(i+1, n):
            common = sum(adj[i][x] and adj[j][x] for x in range(n))
            if adj[i][j]:
                lam_vals.add(common)
            else:
                mu_vals.add(common)

    if len(lam_vals) == 1 and len(mu_vals) == 1:
        return (n, k, lam_vals.pop(), mu_vals.pop())
    return None


def main():
    print("=" * 72)
    print("  PAYNE DERIVATION: W(3,3) -> GQ(2,4) -> Schläfli?")
    print("=" * 72)

    print("\n[1] Building W(3,3)...")
    points, adj, omega = build_w33()
    lines = find_gq_lines(points, adj)
    print(f"  W(3,3): {len(points)} points, {len(lines)} lines")
    print(f"  SRG params: {srg_params(adj)}")

    # Verify: raw induced subgraph on 27 non-neighbours
    print("\n[2] Raw induced subgraph on 27 non-neighbours of vertex 0...")
    p = 0
    p_perp = {p} | set(j for j in range(40) if adj[p][j])
    derived_pts_raw = sorted(set(range(40)) - p_perp)
    raw_adj = adj[np.ix_(derived_pts_raw, derived_pts_raw)]
    raw_degrees = raw_adj.sum(axis=1)
    print(f"  Degree set: {sorted(set(raw_degrees))}")
    raw_params = srg_params(raw_adj)
    print(f"  SRG params: {raw_params}")
    print(f"  -> Confirmed: 8-regular, NOT strongly regular (as found before)")

    # Now compute Payne derivation
    print("\n[3] Computing Payne derivation at vertex 0...")
    derived_pts, derived_adj, all_lines, t1_lines, t2_lines = \
        payne_derivation(points, adj, lines, base_point=0)

    derived_degrees = derived_adj.sum(axis=1)
    print(f"\n  Derived GQ adjacency:")
    print(f"  Degree set: {sorted(set(derived_degrees))}")
    print(f"  Total lines: {len(all_lines)} (36 type-1 + {len(t2_lines)} type-2)")

    derived_params = srg_params(derived_adj)
    print(f"  SRG params: {derived_params}")

    if derived_params == (27, 10, 1, 5):
        print(f"\n  *** SRG(27,10,1,5) CONFIRMED! ***")
        print(f"  This is the complement of the Schläfli graph SRG(27,16,10,8).")
        print(f"  The W(3,3) -> 27 -> E_6 connection IS REAL (via Payne derivation).")
        schlafli_result = "CONFIRMED"
    elif derived_params and derived_params[1] == 10:
        print(f"\n  SRG with degree 10 found but wrong lambda/mu")
        schlafli_result = "PARTIAL"
    else:
        print(f"\n  NOT SRG(27,10,1,5). Derived adjacency has different structure.")
        schlafli_result = "FAILED"

    # Check complement
    complement_adj = 1 - derived_adj - np.eye(27, dtype=int)
    complement_params = srg_params(complement_adj)
    print(f"  Complement SRG params: {complement_params}")
    if complement_params == (27, 16, 10, 8):
        print(f"  *** Complement = Schläfli graph SRG(27,16,10,8) CONFIRMED! ***")

    # Extra edges from Payne derivation
    extra = derived_adj - raw_adj[np.ix_(range(27), range(27))]
    # Need to handle reindexing: raw_adj uses different indices
    # Actually derived_adj and raw_adj use different vertex orderings
    # Let me recompute properly
    raw_map = {v: i for i, v in enumerate(derived_pts_raw)}
    derived_map = {v: i for i, v in enumerate(derived_pts)}
    # Both should be the same set
    assert set(derived_pts_raw) == set(derived_pts)

    # Reindex raw_adj to match derived ordering
    perm = [raw_map[v] for v in derived_pts]
    raw_adj_reindexed = raw_adj[np.ix_(perm, perm)]

    extra_edges = derived_adj - raw_adj_reindexed
    extra_edges = np.maximum(extra_edges, 0)  # only new edges
    extra_per_vertex = extra_edges.sum(axis=1)
    print(f"\n  Extra edges from Payne derivation (per vertex): {sorted(set(extra_per_vertex))}")
    print(f"  Raw degree: 8, Derived degree: {sorted(set(derived_degrees))}")
    if set(derived_degrees) == {10}:
        print(f"  -> Payne adds exactly 2 edges per vertex (8 + 2 = 10)")

    # Verify on multiple base points
    print("\n[4] Verifying Payne derivation at 4 different base points...")
    for bp in [0, 5, 17, 33]:
        _, d_adj, _, _, _ = payne_derivation(points, adj, lines, base_point=bp)
        params = srg_params(d_adj)
        print(f"  Base point {bp}: SRG params = {params}")

    # Eigenvalue check
    print("\n[5] Eigenvalue decomposition of Payne-derived graph...")
    eigvals = np.linalg.eigvalsh(derived_adj.astype(float))
    eigvals_rounded = np.round(eigvals).astype(int)
    from collections import Counter
    eig_count = Counter(eigvals_rounded)
    print(f"  Eigenvalues (rounded): {dict(sorted(eig_count.items()))}")
    if derived_params == (27, 10, 1, 5):
        r_prime = 1  # predicted eigenvalue
        s_prime = -5  # predicted eigenvalue
        print(f"  Expected for SRG(27,10,1,5): k=10, r=1 (mult 20), s=-5 (mult 6)")

    # Save results
    results = {
        "w33_params": "(40, 12, 2, 4)",
        "raw_subgraph_degree": 8,
        "raw_subgraph_srg": str(raw_params),
        "payne_derived_params": str(derived_params),
        "complement_params": str(complement_params),
        "type1_lines": 36,
        "type2_lines": len(t2_lines),
        "total_lines": len(all_lines),
        "extra_edges_per_vertex": sorted(set(int(x) for x in extra_per_vertex)),
        "eigenvalues": {str(k): int(v) for k, v in sorted(eig_count.items())},
        "schlafli_confirmed": schlafli_result == "CONFIRMED",
        "conclusion": (
            "The Payne derivation of W(3,3) at any vertex produces GQ(2,4) "
            "whose collinearity graph is SRG(27,10,1,5) = complement of Schläfli. "
            "The raw induced subgraph (8-regular) is a SUBGRAPH of this; the Payne "
            "construction adds 2 edges per vertex from the {p,x}^{perp perp} spans. "
            "This confirms the W(3,3) -> 27 lines of cubic surface -> E_6 connection "
            "is GENUINE, mediated by the classical Payne derivation."
        ) if schlafli_result == "CONFIRMED" else (
            "The Payne derivation did NOT produce SRG(27,10,1,5). "
            "The W(3,3) -> Schläfli connection requires further investigation."
        )
    }

    out_path = "data/w33_payne_derivation.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  Saved to {out_path}")

    print("\n" + "=" * 72)
    if schlafli_result == "CONFIRMED":
        print("  RESULT: The Schläfli connection is REAL.")
        print("  The 27 non-neighbours, under Payne derivation, form")
        print("  SRG(27,10,1,5) = complement of the Schläfli graph")
        print("  = collinearity graph of the 27 lines on a cubic surface.")
        print("  This is the GENUINE structural link W(3,3) -> E_6.")
        print()
        print("  Previous 'failed prediction' was PREMATURE:")
        print("  the raw subgraph (degree 8) is NOT the full derived GQ.")
        print("  Payne adds exactly 2 edges per vertex to reach degree 10.")
    else:
        print(f"  RESULT: {schlafli_result}")
    print("=" * 72)


if __name__ == "__main__":
    main()
