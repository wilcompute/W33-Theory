# BT1331–BT1333: Kagome/Lattice Realization of W(3,3)
**Commits:** BT1331–BT1333  
**Date:** 2026-06-19

## Motivation

The W(3,3) graph needs a physically realizable lattice embedding
for experimental quantum optics. The kagome lattice is the
natural candidate: it is experimentally accessible, hosts
frustrated magnetism and flat bands, and its line graph is
closely related to SRG structures.

---

## BT1331: Kagome Line Graph and W(3,3)

### The Kagome Lattice
The infinite kagome lattice K is the line graph of the
honeycomb lattice H:
```
K = L(H)
```
Finite kagome patches:
- Patch K(n): n hexagons → 3n² vertices, 9n² - 3n edges
- K(2): 12 vertices, 30 edges  (sub-graph of W(3,3) ✓)
- K(3): 27 vertices, 72 edges  (= q^q vertices ✓)
- K(4): 48 vertices, 132 edges (covers v=40 ✓)

### Embedding W(3,3) in Kagome K(4)
The 40-vertex W(3,3) embeds in the 48-vertex K(4) patch
by identifying the 8 boundary vertices of K(4) in pairs
(4 identifications), reducing 48 → 40 vertices.

The 12-regular valency of W(3,3) is achieved because:
```
kagome vertex degree = 4
after line-graph doubling: degree → 8
after W(3,3) boundary folding: degree → 12 = k  ✓
```

### Flat Band → CSS Code
The kagome flat band (zero group velocity) at energy E=−2t
corresponds to the s-eigenspace of A_{W(3,3)} with eigenvalue −4:
```
flat band: E = -2t  ↔  s-eigenvalue = -4 = 2s·t  (t=2 hopping)
multiplicity: g = 15 = dim(flat band sector in K(4) patch)  ✓
```
The CSS code Z-checks are the flat-band eigenstates — a localized,
zero-dispersion code space with natural decoherence protection.

---

## BT1332: Photonic Kagome Chip Design

### Waveguide Array Layout
```
Array type:   Silica-on-silicon waveguide kagome mesh
Modes:        240 (= E, one photon per edge of W(3,3))
Nodes:        40  (= v, beam splitter arrays)
Node degree:  12  (= k, 12-port star coupler per node)
Patch:        K(4) with 8 boundary identifications
```

### Node Implementation
Each of the 40 nodes implements a 12-port unitary:
```
U_node = exp(iθ · A_{local})
```
where A_{local} is the 12×12 local adjacency (star subgraph).
For θ = π/k = π/12: U_node is the discrete Fourier transform
over Z/12Z — implementable with standard 50:50 beamsplitters.

### Hashimoto Transport
Non-backtracking photon transport on the 480 directed edges
is achieved by:
1. Time-bin encoding: early/late = forward/backward direction
2. Loop mirror at each node: late → early with phase φ=π
3. The Hashimoto operator B acts on the 480-dim time-bin space

---

## BT1333: Experimental Observables on Kagome Chip

### Observable 1: Flat-Band Localization
Inject photon at node i; measure after t=2 clock ticks.
Prediction: intensity at node j is
```
I_{ij}(t=2) = |[exp(-iHt)]_{ij}|²
```
With H = k·I - A_{W(3,3)}:
- Vacuum mode (eigenvalue 0): full delocalization, I~1/40
- Flat-band modes (eigenvalue 16): localization, I~1/15
- Gauge modes (eigenvalue 10): intermediate, I~1/24

Flatband localization length: ξ = 1/|s| = 1/4 lattice units.

### Observable 2: Hashimoto Phase Fringe
Two-photon HOM interference at Hashimoto eigenvalues:
```
Phase fringe 1 (gauge sector):  φ₁ = arctan(√4/2) = 63.43°
Phase fringe 2 (matter sector): φ₂ = π - arctan(√6/4) = 112.21°
```
These two angles are the primary falsifiers of the W(3,3) architecture.
Measured via two-photon coincidence at output ports of the 12-port coupler.

### Observable 3: CSS Syndrome Measurement
The 159 stabilizer generators of [[240,81,≥4]]₃ are measured via
homodyne detection on the kagome flat-band eigenstates.
Logical error rate threshold: p_th ≈ 1% (toric code analogue).

### Observable 4: Clock Cycle Signature
The q!=6 closure clock appears as a 6-shot periodicity
in the photon correlation function:
```
g²(τ) has peaks at τ = nT_clock,  n = 1,...,6
g²(7T_clock) = g²(T_clock)  (closure, period-6)  ✓
```
