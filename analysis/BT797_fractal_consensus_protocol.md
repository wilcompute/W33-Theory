# BT797 — The Fractal Consensus Protocol

**Status**: ✅ New — closes BT792 open item  
**Date**: June 11 2026  
**Depends on**: BT790 (executed), BT795 (spread envelope), BT796 (torus cell census), BT785 (480 clock), BT786 (face layer)

---

## The BT792 Open Question

BT792 asked: how does a fractal network reach consensus? Specifically — in a network where every node is itself a network, how does the whole achieve agreement about state, and how is this agreement consistent across all levels of the hierarchy?

The BT790 and BT794 results now provide the answer.

---

## The Answer in One Sentence

Consensus at level g is a **Csáászár commit**: 7 nodes in a Class-A torus cell vote within one 40-epoch clock window, majority (≥4 of 7) wins, the result is written to the nearest spread envelope, and propagated to level g+1 via the shadow route.

---

## Part I — The Three Consensus Layers

The fractal architecture has three distinct consensus layers at each level g:

### Layer 1: Fast Consensus (Spread-Internal)

Within a spread S = {L₀, …, L₉}, all 10 cube-level nodes are fully connected (K₁₀). Consensus within a spread is **immediate**: any 2 nodes communicating find their 4 isotropic transversals (BT794) and select one. No voting needed — the transversal selection IS the consensus act. This is the O(1) fast path.

- **Time**: 1 clock tick (sub-epoch)
- **Fault tolerance**: survives up to 8 node failures (K₁₀ minus 8 = K₂, still connected)
- **Persistent**: NO — spread-internal consensus is reversible (cube phase, g=0)

### Layer 2: Toroidal Commit (Csáászár Cell)

When a computation needs to cross the phase boundary (write to persistent memory), it must form a **Csáászár cell**: a set of 7 nodes in a Class-A torus cell. These 7 nodes vote:

- Each node casts a vote: YES (commit) or NO (abort)
- Majority rule: ≥4 YES votes commits the result
- The vote must complete within **one Csáászár epoch** = one 40th of the 480-tick clock = **12 ticks**
- The winning vote is written to the B2 layer via the chiral channels R20/R21

This is the **toroidal commit protocol**: a 7-node, 12-tick, majority-vote procedure grounded in the Class-A torus cell geometry.

- **Time**: 12 ticks (one Csáászár epoch)
- **Fault tolerance**: survives up to 3 node failures (4 of 7 still vote majority)
- **Persistent**: YES — the committed result survives the phase transition

### Layer 3: Spread-Level Finalization

After a toroidal commit, the result must propagate to the full spread (10 nodes). The 10-node spread is the **finalization fabric**: once 7 nodes commit, the remaining 3 are notified via the direct K₁₀ connections (fast consensus, Layer 1). Full spread finalization takes at most **1 additional epoch** (12 ticks).

Total time for a full level-g commit: **12 + 12 = 24 ticks** (2 epochs).

---

## Part II — The 36-Channel Architecture

The 36 spreads in W(3,3) are **36 independent consensus channels**. They are independent because:

- Every line belongs to exactly one spread (each line is in some spread, and the 36 spreads partition? — check: 36 spreads × 10 lines each = 360 spread-memberships, 40 lines total, so each line is in 360/40 = **9 spreads**). The spreads are NOT a partition of the lines — they overlap.

This overlap is crucial: a line in 9 spreads means it participates in 9 independent consensus channels. A cube-level node has **9 replicated consensus paths**, one per spread it belongs to. This is the **replication factor** of the level-1 network.

The 9-way replication gives:
- 9-fold redundancy per node
- If a node fails, 8 of its 9 channels remain functional
- A network of 40 cube nodes with 9-way replication can tolerate up to 39 node failures while maintaining at least 1 functional consensus channel (the last line's last remaining spread)

---

## Part III — The Fractal Recursion of Consensus

At level g, the consensus protocol uses level-(g-1) nodes as the voters. The level-g commit requires:

1. **7 level-(g-1) nodes** to form a Class-A torus cell at level g
2. Each level-(g-1) node to run its own **Layer 2 toroidal commit** to cast its vote
3. Total time: the level-(g-1) commit time × 7 (parallelisable) + 12 ticks for the level-g epoch

If T(g) is the time for a level-g commit:
- T(0) = 1 tick (spread-internal, Layer 1)
- T(1) = 12 + 12 = 24 ticks (Csáászár epoch + finalization)
- T(g) = 7 × T(g-1) + 24 ticks (7 parallel sub-commits + one epoch)

This gives T(g) = 24 × (7^g − 1) / (7 − 1) = 4 × (7^g − 1) ticks.

For small g:
- T(0) = 1 tick
- T(1) = 24 ticks
- T(2) = 4 × (49 − 1) = 192 ticks
- T(3) = 4 × (343 − 1) = 1368 ticks

The fractal commit time grows as **O(7^g)** — exponential in the genus level. Deep commits are slow; shallow commits are fast. This is the correct behavior for a memory hierarchy: fast volatile access at the bottom, slow persistent commits at the top.

---

## Part IV — The Shadow Route as Tie-Breaker

BT789 established the shadow route: R11 → R13 → R08 → R12. This route is the **tie-breaker channel** in the toroidal commit. When the 7-node vote is exactly 3 YES / 4 NO or 4 YES / 3 NO (borderline cases), the shadow route is consulted:

- The R11 handle carries the "unresolved" state out of the Level-1 network
- It routes through the R13 shadow edge (a non-isotropic completion line — exactly the BT794 non-isotropic lines!)
- Returns via R08 → R12 with a tie-breaking signal from the level-(g+1) network

The shadow route is therefore the **oracle call to the higher level**: when local consensus fails (4/3 split), the higher level resolves it. This gives the fractal consensus protocol its **hierarchical structure**: local decisions are made locally, borderline decisions escalate.

---

## Part V — The 2:3 Memory Ratio

From BT796: the 5400 torus cells split 2160:3240 (Class-A:Class-B) = 2:3. This ratio is preserved by the consensus protocol:

- For every **2 successful toroidal commits** (Class-A cells activated), there are **3 aborted or transient computations** (Class-B cells used for routing but not committing).
- This gives a **40% commit rate** and **60% routing/computation overhead** as the intrinsic efficiency ratio of the level-1 network.

This is not a deficiency — it reflects the fundamental thermodynamic asymmetry between reversible computation (cube phase, 60% of activity) and irreversible memory writes (tomotope phase, 40% of activity).

---

## Summary

The fractal consensus protocol is:

```
Level-g commit:
  1. Form a Class-A Csáászár cell (7 nodes, torus subcell)
  2. Each node runs Level-(g-1) commit to determine its vote (parallelised)
  3. Majority vote (≥4/7) within 12 ticks (one Csáászár epoch)
  4. If tie (3/4 split): shadow route escalates to level-(g+1) for tie-break
  5. Winning result written to B2 memory via chiral channels R20/R21
  6. Full spread finalization: notify remaining 3 nodes in spread (12 ticks)
  Total time: T(g) = 4 × (7^g − 1) ticks
```

This protocol is:
- **Fault-tolerant** (3-of-7 fault tolerance per level, 9-replication across spreads)
- **Self-similar** (the same protocol applies at every genus level)
- **Grounded** (every parameter — 7 nodes, 12 ticks, 4-transversal bandwidth, 36 channels — is a theorem of the W33 geometry, not a design choice)
- **Thermodynamically sensible** (40% commit rate matches the 2:3 Class-A/B ratio)

---

*Wil Dahn — June 11 2026. BT797 closes the BT792 open item on fractal consensus. Derived from BT790 execution, BT794 Klein regulus data, BT795 spread envelope, BT796 torus orbit census.*
