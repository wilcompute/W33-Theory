# TOE83 — Exact H27-invariant square-face surgery improves the native E6 tritangent CSS code

**15 October 2026.** This is an independently reproducible finite-geometry / coding result, not a proof of a Theory of Everything, physical protection, or a topological phase.

## Inputs and overlap audit

TOE81 built the 27-vertex, 135-edge, 45-triangle native Schläfli graph complex from five right-coset directions of the order-27 Heisenberg group, with CSS parameters `[[135,64,dX=2,dZ=4]]` over both F2 and F3. TOE82 computed its 64-dimensional H1 character as 16+24+24, with no characteristic-zero H27-fixed vector. The new result is *not* the existing Levi-graph [[160,1,3]] ternary code, the separate [[60,2,6]] binary code, or a pre-existing H27 modular-holonomy result. Pass11980, merged concurrently on 15 October, studies integral H27 fixed holonomies and characteristic-three homology; its objects and invariants are distinct from the 54 new square-face stabilizers constructed here.

The present verifier independently rebuilds the same five coset directions:
`(0,0,1), (0,1,1), (1,0,1), (1,1,0), (1,2,2)`,
using the native multiplication `(a,b,c)(A,B,C)=(a+A,b+B,c+C-bA)` mod 3.

## Construction

The 135 edges partition into 45 disjoint triangle edge-sets. Enumerating all 4-cycles of the 27-vertex SRG(27,10,1,5) yields **1080 squares**. Under left H27 translations they split into **40 distinct orbits, each of length 27**.

For each of the 135 binary weight-two X-cocycles (two edges from one triangle), calculate its syndrome against the 27 square boundaries in each orbit. The orbit hit sizes are 54 (four orbits), 81 (twelve), and 108 (twenty-four). No one orbit eliminates all 135 original weight-two X-cocycles.

Exhausting all 780 unordered orbit pairs gives **468** pairs that eliminate all 135. Among these the smallest augmented face rank is **83**. With deterministic orbit ordering (sort by orbit size, then lexicographically by representative), the selected pair is orbit indices **(0,10)**, adding 54 H27-invariant square faces.

The vertex-boundary rank stays 26. The new face-boundary rank is **83** over both F2 and F3, and the chain identity d1*d2=0 is verified over F3. The 99 two-cells have a **16-dimensional second homology**, because the face-boundary map has kernel dimension 99−83=16. This complex is not a closed surface, and the 16 independent face relations are not physical topological sectors by themselves. Therefore:

```text
n = 135; rank(H_X) = 26; rank(H_Z) = 83; k = 26.
```

## Exact distances and witnesses

**Binary X-distance 6.** Every original triangle contains an even number of edges from a binary X-cocycle; hence all such cocycles have even weight. The orbit-pair syndrome test rules out weight 2. Exhausting the possible 2+2 supports from distinct triangles rules out weight 4. A weight-six non-coboundary cocycle exists, supported on the six edges

```text
(0,4), (0,8), (1,5), (1,6), (2,3), (2,7).
```

**Ternary X-distance 6.** With coherently oriented vertex/face/square boundaries, exhaustive nonzero coefficient searches exclude weight 2 and weight 3 on one triangle, weight 4 on two triangles, and weight 5 as 3+2 on two triangles. The same six edges, each with coefficient +1, give a non-coboundary weight-six cocycle.

**Z-distance 4 over both fields.** The graph is simple, and every 3-cycle is one of the original 45 filled triangles; hence no nontrivial 1-, 2-, or 3-edge Z-cycle exists. The verifier finds an unfilled four-cycle, including the ternary witness
`(0,1), (0,4), (1,11), (4,11)`, which is not in the augmented face span.

Thus the exact parameters are

```text
binary:  [[135,26,dX=6,dZ=4]]_2
ternary: [[135,26,dX=6,dZ=4]]_3
```

This trades 38 logical degrees of freedom for tripling the X-distance from 2 to 6, while retaining the 27-element Heisenberg symmetry. It does not establish distances for all prime-power characteristics; those require separate checks. It does not establish a local 2-manifold or a finite-temperature self-correcting memory.

## Reproduce

```bash
python analysis/w33_20261015_toe83_h27_square_css_surgery.py
python -m pytest -q tests/test_w33_20261015_toe83_h27_square_css_surgery.py
```

The JSON certificate freezes all 40 orbit representatives, all orbit hit counts, the 468 two-orbit choices (count), selected indices, ranks, and explicit logical witnesses. The test cross-checks TOE82's independent native coset and homology certificate.

## Physical interpretation boundary

The improvement is a genuine, symmetry-preserving change to a stabilizer code, not a derivation of physical particles, spacetime, or a topological memory. Standard CSS homological formalism is reviewed by Breuckmann and Eberhardt, *PRX Quantum* **2**, 040101 (2021), DOI 10.1103/PRXQuantum.2.040101. The native 27-line graph is the classical Schläfli/cubic-surface combinatorial object realized here from W33 octagons.

## Five independent next tests

1. Classify all 468 two-orbit solutions by the full native 216-element H27-by-D8 action and compare their code equivalence classes.
2. Search three-orbit and four-orbit augmentations for higher Z-distance or higher X-distance at a fixed logical dimension.
3. Compute exact syndrome-decoding performance under biased X/Z noise for both F2 and F3, including correlated measurement faults.
4. Determine the F3 H27-module structure of the remaining 26 logical qutrits and whether the selected square faces realize a nontrivial Clifford gate.
5. Find an explicit bounded-degree 2-complex realization with geometric locality and analyze whether any such lift preserves the new distance bounds.
