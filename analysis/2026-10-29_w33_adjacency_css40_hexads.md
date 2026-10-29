# W33 point-adjacency CSS [[40,8,6]] and 240 geometric minimum-logical hexads

**Date:** October 29, 2026. **Source:** `analysis/w33_20261029_adj_squarezero_css40.py`. **Tests:** `tests/test_w33_20261029_adj_squarezero_css40.py`. **Frozen data:** `data/w33_20261029_adj_squarezero_css40.json`.

## Scope and priority

This is a new **explicit integration/certificate within W33-Theory**, not a claim to have invented binary adjacency codes, strongly regular graph theory, or CSS theory. The `SRG(40,12,2,4)` graphs, their binary adjacency codes and the fact that multiple nonisomorphic graphs share the parameters have prior literature: Spence (2000), DOI `10.37236/1500`; Crnković et al. (2016), *Self-orthogonal codes from the strongly regular graphs on up to 40 vertices*, DOI `10.3934/amc.2016026`.

The distinguished graph here is **specifically** the collinearity graph of the symplectic generalized quadrangle `W(3,3)`, constructed from the 40 one-dimensional subspaces of `F_3^4` with symplectic form `<u,v>=u0*v2-u2*v0+u1*v3-u3*v1`. A different SRG with the same parameters need not have the same 2-rank or CSS code.

No evidence of a physical photon, gauge coupling selection, Lorentzian geometry, gravity, biological or cryptographic randomness, or a real photonic syndrome threshold follows from the finite calculations.

## 1. A self-orthogonal square-zero boundary on the 40 original points

Let `A` be the 40-by-40 **binary point-adjacency matrix**. Its 40 rows each have weight12, and the verified strongly regular parameters are

```text
(v,k,lambda,mu)=(40,12,2,4).
A^2=(k-mu) I+(lambda-mu) A+mu J
   =8 I-2 A+4 J
   =0  (mod 2).
rank_F2(A)=16.
```

Thus `A=A^T`, `A A^T=0`; choosing both binary CSS check spaces as `row_F2(A)` gives a true commuting stabilizer space with

```text
n=40, rank(H_X)=rank(H_Z)=16, k=40-16-16=8.
```

**Important correction to potential confusion:** this is NOT the binary 40-by-40 **point-line incidence** `B` from the 2026-07-15 Pass78 report. That matrix is not self-orthogonal: independently, `rank_F2(B)=25` and `B B^T=A (mod2)`. The graph's adjacency `A`, not the incidence matrix `B`, supports the construction.

## 2. Exact distance and full stabilizer weight enumerator

Exhaustively enumerate all binary subsets of 40 vertices of Hamming weight 1 through 6. A subset indicator `x` commutes with all X/Z checks precisely when `A x=0`. The code counts are

```text
w=1..5: 0 nonzero kernel vectors;
w=6:   240 kernel vectors.
```

Independently, enumerate all `2^16=65,536` words in the rowspace of `A` via Gray code. Its complete weight distribution is

```text
1 + 45 t^8 + 1120 t^12 + 15570 t^16 + 32064 t^20
  + 15570 t^24 + 1120 t^28 + 45 t^32 + t^40.
```

The smallest nonzero stabilizer weight is8. Therefore **every weight-six kernel word is nontrivial logical**, and no smaller nontrivial logical exists, proving the binary CSS parameters

```text
[[40,8,6]]_2,   d_X=d_Z=6.
```

In the ideal error-correction model this corrects any two arbitrary Pauli errors (distance6), and any erasure of up to five known positions. It does NOT supply a compatible photon-mode gate set, dynamical error model, syndrome-extraction depth, fault-tolerance threshold or a 40-photon implementation. It is separate from the earlier ternary 240-link `[[240,81,3]]_3` construction and the 28-point CSS code.

## 3. Every minimum logical is *exactly* a pair of intersecting W33 lines

The graph has 40 totally isotropic four-point lines; each point belongs to four lines. For any unordered pair of distinct lines `L1,L2` meeting at `p`, define a six-point support

```text
X(L1,L2)=(L1 union L2) minus {p}
        =L1 symmetric_difference L2.
```

There are `40*binom(4,2)=240` such unordered incident line pairs. Their indicators are in `ker_F2(A)`. This follows directly from the generalized quadrangle's unique-point-on-line incidence rule: the six points form two disjoint triangles, and every other point has 0 or 2 neighbors in the six-point set.

**Independent exhaustive witness:** enumerate all 240 geometric six-point supports, all 240 binary weight-six kernel vectors, and verify **set equality**, not merely coincident counts. Each original vertex lies in 36 of the 240 supports. This gives an explicit, automorphism-natural geometry of the complete minimum-logical shell.

The fact that there are 240 such hexads, 240 W33 collinearity edges and 240 E8 roots is *not* by itself a canonical, equivariant edge/root identification. These are different acted-on sets; their stabilizers and incidence must be compared before any proposed natural correspondence.

## 4. An exact graph-state entanglement/coding bridge

For the pure stabilizer graph state corresponding to adjacency `A`, the von Neumann entanglement entropy (in ebits) across an exact vertex bipartition `S,bar S` is `rank_F2 A[S,bar S]`. Directly:

- Each of the **40 isotropic lines** (size4) has cross-rank4: **4 ebits**.
- Each of the **240 minimum-logical six-point hexads** has cross-rank5: **5 ebits**.
- All cuts are bounded above by global rank`A=16` ebits.

Why is rank5 natural for a six-point hexad? Because its indicator is a binary kernel vector and each vertex has exactly two neighbors within the hexad, the six cross-boundary adjacency columns obey one nontrivial sum relation. Hence the rank is at most5; the exact census proves it is **exactly** 5 for all 240.

This is a useful conceptual bridge between algebraic CSS logical support and bipartite entanglement **in one finite graph-state model**. It does **not** establish a gravitational area law, black-hole entropy, holographic dynamics, Penrose real structure, or finite-speed propagation.

## 5. Audit of the October 29 parallel research landscape

The newest `master` commits report a comprehensive finite closure/metric program, exact native coercivity at one Bloch character, a gauge-covariant finite overlap operator, no-go results in string hypercharge/tachyon searches, and a reserved finite graph-state area-law track. The present result avoids duplication by focusing on the **CSS code of the binary point-adjacency matrix** and its full weight-six logical shell.

- The Pass12392 packet supplies one **single-momentum exact** physical stiffness bound >0.000548, not a uniform torus or infinite-volume photon gap.
- Pass12402–12409 classify *finite-field* Hodge closure and interpret some metric types as Lorentzian-like. The field is finite: there is no real ordering, experimentally calibrated light speed, or physically selected time coordinate in that result.
- Other tracks' heterotic hypercharge and tachyon counterexamples are **conditional on the scanned models, Wilson lines, and chirality criteria**; none is a theorem ruling out all string compactifications.
- The existing twistor/Conwell code `[[28,15,3]]_2` is a distinct code with different point set, distance and check operators. The 40-point adjacency construction here is not a claimed consequence of the Penrose transform.

## 6. A crucial GF(9) characteristic-three counterexample to the parallel closure theorem

The latest Pass12410–12417 mathematical report correctly repaired an earlier **all-odd-q** overstatement, but its replacement **trace-zero** test contains a further field-characteristic exception. For `q ≡ 1 (mod 4)` with `char F_q = 3` (beginning at `F9`), the scalar bivector constitutive operator `kappa=i I6`, `i²=-1` satisfies `kappa²=-I`, is symmetric for the wedge pairing, and has `tr kappa = 6i = 0` in characteristic three. Its `+i/-i` eigenvalue multiplicities are `(6,0)`, not the balanced `(3,3)` of a four-dimensional metric Hodge star. Hence **trace zero is not sufficient for metric closure over F9**, despite being a valid shortcut over split fields of characteristic at least five.

The test is reproduced by `analysis/w33_20261029_f9_hodge_trace_counterexample.py` and the corrected statement is patched in `analysis/PASS12410_12417_CLOSURE_PROOF_ALPHA_ENTANGLEMENT_CEILING_TPRIME.md`. The robust split-field condition is balanced eigenspace multiplicities (or characteristic polynomial `(T²+1)³`), not merely the trace. The previous exhaustive `q=3` calculation, `q=5,13` tests, and the non-split case are **not** contradicted. Nothing in this finite-field correction constructs a real Lorentzian physical spacetime.

## Validation and synchronization

The producer is written using standard-library Python only. It verifies the literal projective symplectic point set, integer SRG common-neighbor counts, all `40^2` binary commutators, full 65,536-word stabilizer distribution, all vertex subsets through size6, all 240 two-line supports, and exact graph-state cut ranks. A six-test targeted pytest suite controls the output.

The main Windows checkout may be dirty and must not be reset, cleaned, force-pushed or overwritten. The designated clean independent research worktree can safely fast-forward to published `master` and run these tests on the user's Windows device. Syncing that worktree does not assert that parallel edits in the main checkout were discarded or automatically committed.

## Five new independent next experiments

1. **Symmetry-realized logical Clifford gates:** explicitly compute W(3,3)'s point-permutation automorphisms on the eight-dimensional homology `ker A/im A` and determine its symplectic logical representation, including whether any Clifford gates are physically transversally implementable.
2. **Pauli-plus-erasure decoding:** construct explicit syndromes and a weight-two ideal decoder for the `[[40,8,6]]_2` adjacency CSS code, then independently enumerate its erasure failure patterns and candidate optical loss cost.
3. **Physical observables:** map an actual native Maxwell flux operator into the eight-dimensional adjacency homology and test whether a gauge-invariant nontrivial intertwiner exists; do not equate binary stabilizer coordinates with optical modes without such a map.
4. **Entanglement/geometry falsifier:** classify graph-state cut-rank distributions under the true W33 automorphism orbits, contrast the 40 line and 240 hexad cuts, and test whether any bounded-degree sequence of growing W(3,q) geometries has a nontrivial continuum scaling limit.
5. **Independent native/string verification:** test the finite Hodge-closure group's real-form caveats, the claimed exact local coercivity inverse witness, and the 65-pairing hidden-sector obstruction against independent exact implementations before attaching experimental meaning.
