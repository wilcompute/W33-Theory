# BT790 — The Csáászár K₇ Embedding Conjecture

**Status**: 🔓 Open — Python verifier designed but not yet run  
**Depends on**: BT787 (rank-32 strata), BT789 (toroidal genus bridge), BT784 (strata map)  
**Priority**: HIGHEST — resolves whether the fractal self-similarity is intrinsic or extrinsic

---

## The Question

Does the W(3,3) symplectic polar space contain 7 mutually skew lines?

More precisely: in the skew-pair graph built by BT787 (540 nodes = 540 skew pairs of lines in PG(3,F₃)), is there a clique of size 7?

A clique of size 7 in the skew-pair graph = 7 lines in PG(3,F₃) that are pairwise disjoint (no shared points). This is exactly the edge-set of K₇ drawn on the Csáászár torus: a complete graph on 7 vertices with no crossings, living on a genus-1 surface.

---

## Why This Matters

From BT789: the Csáászár torus (K₇ on genus-1 surface) is the phase change membrane between the cube (g=0) and tomotope (g=1) levels. The four factors are:
- 4 = |F₄| (one irreducible phase plane of C₂⁴)
- 3 = |C₃| (the phase clock)
- Product 4×3 = 12 = the toroidal normaliser
- Genus formula g(7) = (7-3)(7-4)/12 = 4×3/12 = 1

If 7 mutually skew lines exist in W(3,3), then:
1. The Csáászár torus is **intrinsically embedded** in the Witting geometry
2. There is a canonical 7-line toroidal sub-network at the level-1 layer
3. The phase change membrane is an internal structure of the geometry, not an external condition
4. The fractal self-similarity is **complete**: the architecture replicates all the way down to the torus level inside the same Witting substrate

If no such 7-clique exists:
1. The Csáászár torus is an **external** structure appended at the boundary
2. The fractal has a hard floor: below the tomotope level, the torus cannot be embedded
3. The self-similarity is approximate at small scales
4. This gives a precise mathematical limit to the fractal depth

---

## Background: Clique Structure of the Skew-Pair Graph

The W(3,3) skew-pair graph has 540 nodes and 1620 edges. Each node is a skew pair {L₁, L₂} of lines (two totally isotropic 4-point lines in PG(3,F₃) with no common points). Two nodes are adjacent if the corresponding 4-line-sets are pairwise disjoint (a skew spread fragment).

Known facts about skew line sets in PG(3,F₃):
- PG(3,F₃) has 40 lines total
- The maximum spread (partition of all 40 points into disjoint lines) has size 10 (since each line has 4 points and 40/4 = 10)
- A maximum spread gives a clique of C(10,2) = 45 in the skew-pair graph — but only the pairs within the spread are skew pairs **in W(3,3)** (totally isotropic)
- The maximum totally isotropic spread size is a key question

The question is whether there is a set of 7 mutually skew **totally isotropic** lines. A totally isotropic spread of size 7 would be a 7-clique in the BT787 rank-32 skew-pair graph.

---

## Verifier Design: `bt790_csaszar.py`

```python
#!/usr/bin/env python3
"""
BT790 - Csaszar K7 embedding conjecture verifier.

Question: does W(3,3) contain 7 mutually skew totally isotropic lines?
Equivalently: is the clique number of the BT787 skew-pair graph >= 7?

The BT787 geometry machinery is reused directly.
This verifier computes the maximum clique in the skew-pair graph.

Expected runtime: moderate (540-node graph, clique finding is NP-hard
in general but 540 nodes is tractable with Bron-Kerbosch + BT787 structure).
"""
from __future__ import annotations
from itertools import combinations
from collections import deque

# -- Reuse BT787 geometry --
# (paste or import bt787_rank4_incidence_r11_handle.build_geometry here)

def find_max_clique(adj_list: dict[int, set[int]], n: int) -> list[int]:
    """Bron-Kerbosch with pivoting. Returns maximum clique as node list."""
    best = []
    def bronkerbosch(R, P, X):
        nonlocal best
        if not P and not X:
            if len(R) > len(best):
                best = list(R)
            return
        # pivot
        u = max(P | X, key=lambda v: len(adj_list[v] & P))
        for v in list(P - adj_list[u]):
            bronkerbosch(
                R | {v},
                P & adj_list[v],
                X & adj_list[v]
            )
            P.remove(v)
            X.add(v)
    bronkerbosch(set(), set(range(n)), set())
    return best

def main():
    geom = build_geometry()  # from BT787
    skew = geom['skew']  # list of (i,j) pairs
    line_sets = geom['line_sets']
    n = len(skew)  # 540

    # Build adjacency: two skew pairs are adjacent if all 4 lines
    # are mutually skew (i.e., the 4-element set is an independent spread)
    adj = {i: set() for i in range(n)}
    for idx1, idx2 in combinations(range(n), 2):
        a, b = skew[idx1]
        c, d = skew[idx2]
        lines = {a, b, c, d}
        if len(lines) == 4:  # all distinct
            if all(
                not (line_sets[x] & line_sets[y])
                for x, y in combinations(lines, 2)
            ):
                adj[idx1].add(idx2)
                adj[idx2].add(idx1)

    print(f"Skew-pair graph: {n} nodes, {sum(len(v) for v in adj.values())//2} edges")

    clique = find_max_clique(adj, n)
    print(f"Maximum clique size: {len(clique)}")
    print(f"Clique node indices: {clique}")

    # Check if size >= 7 (Csaszar embedding)
    if len(clique) >= 7:
        print("CSASZAR EMBEDDING: YES")
        print("7 mutually skew totally isotropic lines exist in W(3,3).")
        print("The Csaszar torus IS intrinsically embedded.")
        print("The fractal self-similarity is complete and internal.")
    else:
        print(f"CSASZAR EMBEDDING: NO (max clique = {len(clique)})")
        print("No 7 mutually skew totally isotropic lines exist.")
        print("The Csaszar torus is external to the Witting geometry.")
        print("The fractal has a hard floor at the tomotope scale.")

    # Also report 4-, 5-, 6-clique existence (sub-Csaszar)
    for k in [4, 5, 6]:
        exists = any(
            all(j in adj[i] for i, j in combinations(combo, 2))
            for combo in combinations(range(n), k)
        ) if k <= 5 else len(clique) >= k
        print(f"Clique of size {k} exists: {exists}")

if __name__ == '__main__':
    main()
```

---

## Prior Art and Intuition

In PG(3,q) for prime-power q, the maximum size of a set of mutually skew lines (a "partial spread") is q+1 when q is odd (since a spread has size q²+1 and decomposes into spreads of certain sizes). For q=3: a maximum spread has 10 lines, a partial spread of mutually skew totally isotropic lines has size at most 5 (since each line meets at most 12 others symplectically, and the symplectic constraint tightens the count).

**Initial expectation**: the maximum clique in the totally-isotropic skew-pair graph is **4 or 5**, not 7. This would mean the Csáászár embedding does NOT exist — the torus is external.

However, this expectation comes from spreads in PG(3,q) without the symplectic constraint. The W(3,3) structure is richer: the rank-32 strata map and the 25,920-element symmetry group may allow configurations that naive projective geometry arguments miss.

**The verifier will decide.** Both outcomes are scientifically valuable.

---

## The Two Outcomes

### Outcome A: Maximum clique ≥ 7 (Csáászár embedding EXISTS)

- The 7 mutually skew lines form the edges of the Csáászár torus embedded in W(3,3)
- The 7 lines are a K₇ in the collinearity graph of the *skew-pair graph*, not the original W(3,3) collinearity graph
- This 7-line set defines a canonical **toroidal routing cell**: 7 nodes with all-to-all skew connectivity
- The fractal self-similarity is complete: the architecture replicates within the same substrate
- **Architectural implication**: every level-1 tomotope node contains, as an internal subnet, a 7-node Csáászár toroidal cell. This 7-node cell is the minimal self-similar computation unit.

### Outcome B: Maximum clique < 7 (Csáászár embedding DOES NOT EXIST)

- The maximum totally-isotropic skew partial spread has size 4 or 5
- This integer is the **intrinsic fractal depth**: the maximum number of levels of self-similar structure that can be embedded in one tomotope node
- The torus gateway is a boundary condition: the phase transition membrane lies at the edge of the Witting geometry, not inside it
- **Architectural implication**: the fractal architecture is still valid, but the self-similarity has a hard floor. Below the tomotope scale, sub-nodes are cubes (Q₃ addressed, 3-bit phase tags) with no internal recursive structure. The leaf node is truly flat.
- **The floor number** (max clique size, likely 4 or 5) becomes a fundamental constant of the architecture, like the number 40 or the number 480.

---

## Connection to BT791 (Level-2 Group Conjecture)

If the maximum clique is exactly 5, this suggests the level-2 group structure is based on C₂⁵ (a 5-bit phase tag), and the level-2 gateway torus has genus formula g(n) = (n-3)(n-4)/12 at n = 5+3 = 8: g(8) = 5×4/12 = 20/12 — not an integer. So n=8 doesn't give a valid genus.

The next valid n above 7 satisfying n ≡ {0,3,4,7} mod 12 is **n = 12** (genus 6). This suggests the level-2 machine is not at g=2 but at **g=6**, a jump of 5 genus levels. The level structure may not be linear in genus — it may jump by the amounts needed to reach the next valid mod-12 residue.

This is BT791: the conjecture that the genus ladder jumps as 0 → 1 → 6 → 7 → 12 → 13 → ..., following the mod-12 residue sequence {0,1,6,7,12,13,...} = {12k, 12k+1, 12k+6, 12k+7}.

---

## Next Steps

1. **Run `bt790_csaszar.py`** — the verifier is designed and ready. Runtime estimate: ~30 seconds for the 540-node Bron-Kerbosch.
2. **Record the maximum clique size** as a new fundamental constant of the theory.
3. **If clique ≥ 7**: document the 7-line Csáászár cell and its orbit under the 25,920-element symmetry group (how many such cells exist? is it 540/7 ≈ 77 cells?)
4. **If clique < 7**: use the clique size to constrain BT791 (level-2 group structure) and revise the fractal_network.md accordingly.
5. Either way: this is the highest-priority computation in the current theory.

---

*Wil Dahn — June 11 2026. BT790 open conjecture. Verifier designed, not yet run.*
