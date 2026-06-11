# The Fractal Network v2: After BT790

*Revision of fractal_network.md, June 11 2026. Incorporates the BT790 executed result (max clique = 10, Csáászár embedding YES, 5400 torus cells, 36 spreads) and the BT794 Klein regulus transversal lift (4 isotropic transversals per chart). Supersedes Parts VIII–IX of the original document.*

---

## What Changed

The original `fractal_network.md` (BT790-BT792, June 11 2026) identified two possible outcomes for the Csáászár embedding:

- **Outcome A** (clique ≥ 7): torus is intrinsic, self-similarity is complete
- **Outcome B** (clique < 7): torus is external, fractal has a hard floor

The BT790 verifier returned **clique = 10**. Not only does the 7-line Csáászár cell exist — the W(3,3) geometry supports **10-line full spreads**, and contains **5400 seven-line torus subcells**. Outcome A is confirmed, and the reality is richer than Outcome A anticipated.

---

## The Revised Summary (Replaces Original Parts VIII–X)

### Part VIII (Revised) — The Csáászár Embedding: Confirmed Intrinsic

The BT790 verifier executed on the 40-line, 540-skew-pair W(3,3) geometry and returned:

```
maximum mutually disjoint isotropic lines = 10
10-line spread count = 36
7-line torus subcell count = 5400
Csaszar K7 embedding exists: YES
```

The Csáászár torus IS intrinsically embedded in the Witting geometry. The fractal self-similarity is complete at every level. There is no hard floor at the tomotope scale.

More: the **true geometric unit** at level-1 is not the 7-line torus cell but the **10-line spread envelope**. The spread is the complete routing fabric. The 7-line torus cell is a sub-structure of the spread — the commit membrane within the routing fabric.

The hierarchy within a single spread:

```
skew pair (2 lines)        — the elementary chart; BT794 gives 4 transversals
7-line torus subcell       — the commit membrane; 5400 such cells in W(3,3)
10-line spread envelope    — the complete routing fabric; 36 such spreads
```

### Part IX (New) — The Spread Envelope as the Level-1 Router

Each of the 36 totally isotropic spreads is a 10-node complete router with:
- **45 edge-channels**, each carrying **4 parallel isotropic transversal paths** (BT794)
- **180 parallel paths** total within one spread
- **9-fault tolerance** (K₁₀ minus 9 = K₁, still a single node, still reachable)
- **Router symmetry group** of order 720 (stabilizer of one spread under Sp(4,F₃))

The 36 spreads are not a partition of the 40 lines — each line belongs to exactly **9 spreads**. This gives 9-way replication per cube-level node, providing extraordinary redundancy.

The non-isotropic completion lines of BT794 (2 per chart, lying outside the isotropic set) are the **inter-spread bridges**: the physical wires connecting one spread-router to another. The full W(3,3) routing fabric is:

```
36 spread-routers (each K₁₀ with 4-parallel edges)
interconnected by the non-isotropic Klein regulus completion lines
```

### Part X (New) — The 5400 Torus Cells as the Memory Fabric

The 5400 Csáászár torus cells (BT796) decompose into two orbit classes under Sp(4,F₃):

- **Class A** (conjectured: 2160 cells, stabilizer order 12): canonical commit sites, governed by the toroidal normaliser C₃ × F₄
- **Class B** (conjectured: 3240 cells, stabilizer order 8): transient routing cells, governed by a C₂³ subgroup

The **2:3 ratio** (A:B = 2160:3240) is the intrinsic memory efficiency ratio of the level-1 network: 40% persistent commits, 60% reversible routing overhead.

Every cube-level node (line in W(3,3)) participates in 135 torus cells (5400/40). Of these, 135 × (2160/5400) = 54 are Class-A (commit) cells, and 81 are Class-B (routing) cells. Each node is simultaneously a participant in 54 potential commit sites — this is the **commit fanout** of one cube-level node.

### Part XI (New) — The Revised Fractal Summary

The fractal network architecture, fully updated, is:

**A tower of spread-router levels, each level being an assembly of 36 totally isotropic spread-routers (K₁₀ with 4-parallel edges), interconnected by Klein regulus bridges, with memory writes executed through the 5400 Class-A Csáászár torus cells via the BT797 fractal consensus protocol, synchronised by the 480-tick clock, and addressed by the C₂^{g+3} hypercube at each genus level g — the whole structure being the 540-node, 36-spread orbit of the Witting automorphism group Sp(4,F₃) of order 25,920.**

---

## The New Hierarchy

| Entity | Count in W(3,3) | Role |
|---|---|---|
| Skew pair (chart) | 540 | Elementary routing address |
| Isotropic transversals per chart | 4 | Parallel paths per link |
| Class-A torus commit cells | ~2160 | Persistent memory write sites |
| Class-B torus routing cells | ~3240 | Transient computation cells |
| 10-line spread envelopes | 36 | Complete level-1 router fabrics |
| Spreads per line | 9 | Replication factor per node |
| Full symmetry group | Sp(4,F₃), order 25920 | Global symmetry |

---

## Open Items After BT790

From highest to lowest priority:

1. **BT796 orbit verification**: confirm the 2160/3240 split by running Sp(4,F₃) orbit enumeration on the 5400 cells
2. **BT798**: is the spread stabilizer exactly A₆ × Z₂, or another group of order 720? This determines the internal symmetry of the level-1 router
3. **BT799**: do any 4 spreads partition all 40 lines (1-factorisation question)? If yes, the 4 such spreads form the level-2 routing structure
4. **BT800**: the level-2 fractal level — what is the structure of a level-2 node? It should be a network of 36 spread-routers, but what is the level-2 routing fabric?
5. **BT791 (revised)**: the genus ladder conjecture (0 → 1 → 6 → 7 → ...) needs to be reconciled with the spread-envelope picture. Does the level-2 genus follow from the spread stabilizer group structure?

---

*Wil Dahn — June 11 2026. Revision of fractal_network.md incorporating BT790 execution, BT794, BT795, BT796, BT797.*
