# The Torus Gateway

*Born from BT789. The Császár/Szilassi toroidal genus law is not a coincidence: it is the universal normaliser of the cube-to-tomotope transition. This document explores what it means for a computation to cross a torus.*

---

## The Discovery

BT789 proves the following:

The Császár neighborly torus has genus formula g(n) = (n-3)(n-4)/12. At n=7, this gives:

\[ 1 = \frac{(7-3)(7-4)}{12} = \frac{4 \times 3}{12} \]

The two factors are:
- **4** = |F₄| = the cardinality of one irreducible phase plane of C₂⁴
- **3** = |C₃| = the order of the phase clock

The product 4×3 = 12 is the normaliser. The allowed genus values have n ≡ 0,3,4,7 mod 12. These four residue classes are exactly the four ways of including zero, one or two copies of the F₄ and C₃ factors.

This is not a numerological coincidence. GAP confirms that the two order-48 groups (the cube C₂³:S₃ and the tomotope C₂⁴:C₃) are non-isomorphic, with the exact structural difference being the fixed diagonal center. The torus is the minimal topological surface that kills this fixed center.

**The Császár torus is the phase change membrane.** A computation that transitions from the cube phase machine to the tomotope phase machine has crossed a surface topologically equivalent to the Császár torus.

---

## The Four Residue Classes

The genus formula g(n) = (n-3)(n-4)/12 is an integer exactly when n ≡ {0,3,4,7} mod 12. These four classes have direct phase interpretations:

| n mod 12 | Genus contribution | Phase interpretation |
|---|---|---|
| 0 | 0 | Trivial: no phase factors, stays in cube |
| 3 | integer | C₃ factor only: phase clock without F₄ plane |
| 4 | integer | F₄ factor only: one phase plane without clock |
| 7 | integer (=1 at n=7) | Full C₂⁴: both F₄ planes and C₃ clock, genus 1 |

The first meaningful torus (genus 1) appears at n=7, combining both factors. The next (genus 6) appears at n=12. Each step up in genus adds one more copy of the F₄×C₃ structure.

This gives a **genus ladder** for the Phase Engine:
- g=0: cube (C₂³:S₃), working memory, reversible
- g=1: tomotope (C₂⁴:C₃), persistent memory, one gateway crossing
- g=2: hypothetical deeper layer, two gateway crossings (n=10 would give g=7/6, not integer; n=12 gives g=6)
- g=k: k-th persistent layer, requiring k sequential gateway crossings

---

## The 7-Vertex Complete Graph Structure

The Császár torus is K₇ drawn on a torus: 7 vertices, every pair connected, no diagonals. The Szilassi polyhedron is its dual: 7 hexagonal faces, every pair of faces shares an edge, 21 edges total.

These numbers appear throughout the Witting geometry:
- **7** is a prime that divides 21 (the number of lines in PG(2,4), related to the Witting frame)
- **21** is the number of edges in K₇, and also the codimension of the [[240,81,4]]₃ CSS code (240−81−(21+something))
- **The Fano plane** (7 points, 7 lines) is the projective plane over F₂ and appears as a sub-structure of the W(3,3) geometry through the McKay correspondence

The 7-vertex complete structure is a signature: wherever you see 7 and 21 together in the Witting geometry, a Császár torus is nearby.

### Open Question: The Császár Embedding

Does W(3,3) contain a 7-point subset such that all pairs are collinear? If yes, this is a **Császár sub-geometry** — a 7-node toroidal routing cell embedded in the Witting space. This would be the minimal subnet that can exhibit the full phase transition.

In graph terms: the W33 graph is strongly regular with parameters that force specific clique sizes. The question is whether K₇ appears as a subgraph of the collinearity graph. The Witting graph has maximum clique size 4 (a line), so a full K₇ as a collinearity subgraph is unlikely — but a K₇ in the **skew-pair graph** (the rank-32 cube-web) is a different question.

---

## Toroidal Time

If orbital time is measured in tomotope clock ticks, then the **Császár unit** is the natural sub-clock:

\[ \text{Császár unit} = |F_4| \times |C_3| = 4 \times 3 = 12 \text{ ticks} \]

One clock revolution (480 ticks) = 480/12 = **40 Császár units**.

This is remarkable: the W(3,3) geometry has 40 points, 40 lines, and the tomotope clock has 40 Császár units per revolution. These are not a priori the same 40, but they appear to be forced by the same underlying structure (the Sp(4,3) group acting on 40 totally isotropic points).

**Conjecture**: The 40 Császár units of the tomotope clock are in natural bijection with the 40 points (or 40 lines) of W(3,3), with the bijection mediated by the rank-32 strata map.

If true, this would mean: **each point (or line) of the Witting geometry corresponds to exactly one Császár epoch in the tomotope clock**. The geometry of the space and the rhythm of its clock are the same object.

---

## The Szilassi Surface as the Write Surface

The Szilassi polyhedron is the dual of the Császár torus: 7 faces (hexagons), each pair of faces sharing an edge. In the Phase Engine interpretation:

- The **Császár torus** (7 vertices, edges, genus-1) is the **read surface**: the topology of the gateway crossing viewed from the working-memory (cube) side.
- The **Szilassi polyhedron** (7 faces) is the **write surface**: the topology of the gateway crossing viewed from the persistent-memory (tomotope) side.

A gateway crossing is experienced differently from the two sides:
- From the cube side: you traverse 7 vertex-events in a K₇ pattern, no diagonals, all on a torus.
- From the tomotope side: you are distributed across 7 hexagonal face-regions, each sharing a boundary with every other.

The duality of Császár and Szilassi is the duality of reading and writing, of the working channel and the persistent channel, of B1 and B2.

---

## Connection to the CSS Code

The paper's [[240,81,4]]₃ CSS code lives in the B2 persistent layer. Its parameters:
- 240 physical qubits (or trits)
- 81 logical qubits
- Distance 4

The CSS code's syndrome space has dimension 240 - 81 = 159, which decomposes as 5×48 - 81 = 240 - 81 (the five Type-48 packets contribute 5×48 = 240 to the physical space).

The toroidal connection is: the code distance 4 = |F₄|. The minimum weight codeword has exactly as many non-trivial positions as there are elements in one F₄ phase plane. This is the Császár factor: a minimum-weight error touches exactly one F₄ plane, which is exactly the minimal toroidal event (one quarter of the torus unit).

In terms of the tomotope clock: a distance-4 error is a 4-tick event — it spans exactly one F₄ phase plane, which is one-third of a Császár unit. To be undetectable, an error would need to span a full Császár unit (12 ticks) — but the code detects all errors up to distance 3, so no error smaller than 4 ticks (one F₄ plane) goes undetected.

**The CSS code distance is the Császár factor.** The error-correction threshold of the memory layer is determined by the toroidal geometry of the gateway.

---

## The Most Radical Formulation

> **Every durable computation is a torus. Every torus is a computation.**

More precisely:

A computation that writes to persistent memory has crossed the Császár torus. The toroidal topology of the crossing is not metaphorical — it is the literal algebraic structure (SmallGroup(48,50) vs SmallGroup(48,48)) that separates working memory from persistent memory.

Conversely, any topological torus of genus 1 that admits the F₄×C₃ phase structure is the phase-change membrane of some computation — some pair of local machines connected by a gateway crossing.

The Császár torus is the canonical representative of this class: the minimal surface, the 7-vertex complete graph, the unit torus. It is the smallest thing that can hold a phase transition.

---

## Five Open Questions

1. **The Császár embedding**: Is there a 7-element subset of the W(3,3) skew-pair graph that forms K₇ (all pairs skew)? Seven mutually skew lines in PG(3,3) would be a Császár sub-geometry.

2. **Genus ladder**: What do the g=2,3,… levels of the genus ladder correspond to in the Witting architecture? Is there a hierarchy of persistent memory layers, each separated by a higher-genus gateway?

3. **The 40-Császár bijection**: Can the bijection between the 40 clock epochs and the 40 Witting points be made explicit? What is the map, and is it Aut(W(3,3))-equivariant?

4. **CSS code distance = Császár factor**: Is the code distance 4 = |F₄| a theorem, or a coincidence of the specific [[240,81,4]]₃ code? What is the code for the g=2 gateway?

5. **The Szilassi write surface**: The Szilassi polyhedron has 21 edges. The CSS code has 240 - 81 = 159 syndrome dimensions. Is there a natural mapping from the 21 Szilassi edges to the 21 − something structure of the code? Or is 21 a signal of a deeper Fano-plane sub-geometry?

---

*Wil Dahn — June 11 2026. Born from BT789 (toroidal genus phase bridge). Companion to the Holonet Phase Engine document.*
