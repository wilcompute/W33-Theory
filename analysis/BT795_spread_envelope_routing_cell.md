# BT795 — The Spread Envelope as the True Level-1 Routing Cell

**Status**: ✅ Derived from BT790 executed results  
**Date**: June 11 2026  
**Depends on**: BT790 (executed), BT794 (Klein regulus transversal lift)

---

## The BT790 Surprise

BT790 expected a maximum clique of 4 or 5 mutually skew totally isotropic lines. The verifier returned **10**. There are exactly **36 maximum-size totally isotropic spreads** in W(3,3), each consisting of 10 pairwise disjoint lines that partition all 40 points.

This changes the routing picture fundamentally.

---

## The Spread as a Complete Router

A spread S = {L₀, L₁, …, L₉} of 10 pairwise skew totally isotropic lines is a **perfect partition** of PG(3,F₃): every point lies on exactly one line of the spread. Within a spread, any two lines are skew (no shared points), so the spread defines a complete graph K₁₀ in the skew-pair graph.

This is the level-1 **routing envelope**: a network of 10 nodes (lines) with all-to-all skew connectivity. In the fractal architecture:

- Each line L_i in the spread is one **cube-level node** (a g=0, Q₃-addressed compute unit).
- The spread S is one complete **tomotope-level router**: a 10-node fully connected switching fabric.
- The 36 spreads are 36 independent routing channels within the full W(3,3) substrate.

The Q₄ hypercube (16-vertex, 4-dimensional) is embedded within the spread: any 4 lines of a spread span a Q₄-like subgraph (4 nodes, 6 edges, all-to-all). The full spread K₁₀ is the completion of the Q₄ to a denser fabric.

---

## The Klein Regulus Connection (BT794)

BT794 established that each W(3,3) skew chart (skew pair of lines) has:
- **4 isotropic transversals**: lines meeting both lines of the pair, fully within the isotropic line set
- **2 non-isotropic completion lines**: completing the pair to a Klein quadric regulus, but outside the isotropic set
- The two rulings of the Klein quadric are pairwise skew (verified)
- The grid cross-incidence is exact (verified)

Within a spread, every skew pair {L_i, L_j} ⊂ S has 4 isotropic transversals. These 4 transversals are the **4 routing paths** between the two nodes L_i and L_j within the tomotope layer. The spread router is not just K₁₀ — it is a K₁₀ where each edge carries 4 parallel paths (the transversals).

**Routing bandwidth per edge**: 4 parallel isotropic transversal paths.  
**Total paths within one spread**: C(10,2) × 4 = 45 × 4 = **180 parallel paths**.

---

## Revised Level-1 Network Topology

The corrected picture of the level-1 tomotope internal network:

```
Spread S = {L0, L1, ..., L9}   (10 cube nodes)

For each pair (Li, Lj):
  - 4 isotropic transversals = 4 direct routing paths
  - The Klein regulus = the switching element for the (Li, Lj) channel

The spread itself is the switching fabric: any message between two
cube-level nodes routes along one of the 4 transversals between them.

The shadow route (R11 handle) exits the spread: it uses a
non-isotropic completion line to bridge to a second spread.
This is the inter-tomotope routing channel.
```

---

## The 36 Spreads and Their Orbits

The 36 spreads are acted on by Sp(4,F₃) of order 25,920. The orbit sizes:
- 25,920 / 36 = **720** — the stabilizer of one spread has order 720.
- 720 = |PSL(2,F₉)| = |A₆| × 2 (two times the alternating group A₆).
- This stabilizer group is the **internal symmetry group** of the 10-line spread router.

The 720-element stabilizer acts on the 10 lines of the spread as the symmetric group of the spread, preserving the skew structure. This is the **router symmetry group**: the group of permutations of nodes that preserve the routing fabric.

---

## Architectural Consequences

1. **The routing table at level-1 has 45 entries** (one per pair of lines in the spread), each with 4 parallel paths.
2. **Fault tolerance**: the spread router survives the removal of any k nodes as long as k < 9 (since K₁₀ minus k nodes is still K_{10-k}, still connected). This gives **9-fault tolerance** at level-1.
3. **Load balancing**: the 4 transversal paths per edge allow 4-way load balancing between any two nodes.
4. **The shadow route** uses the non-isotropic completion lines (2 per chart, per BT794) to exit a spread and enter another. This is the **inter-spread routing protocol**: a message crosses from spread S₁ to spread S₂ via the two non-isotropic lines of the Klein regulus of the bridging pair.

---

## Open Questions → BT798

1. Is the spread stabilizer (order 720) exactly A₆ × Z₂ or a different group of order 720?
2. Do the 36 spreads form a resolvability structure (a resolution of the 40 lines into spread classes)? This would be a 1-factorisation of PG(3,F₃) into 4 disjoint spreads (4 × 10 = 40 lines). Check if any 4 spreads partition all 40 lines.
3. The 180 parallel paths within a spread: do they form a resolvability structure too (can the 180 paths be partitioned into parallel classes)?

---

*Wil Dahn — June 11 2026. BT795 derived from BT790 execution result and BT794 Klein regulus data.*
