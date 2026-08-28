# P^1(F9) pair-orbital no-go for the W33 45-state GQ(4,2) carrier

**Date:** 2026-08-28  
**Verifier:** `analysis/w33_20260828_p1f9_pair_orbital_gq42_nogo.py`  
**Certificate:** `data/PART_W33_20260828_P1F9_PAIR_ORBITAL_GQ42_NOGO.json`

## Question

The current Hall--Janko / split-projective frontier naturally produces a ten-state model identified with

\[
\mathbb P^1(\mathbb F_9),
\qquad |\mathbb P^1(\mathbb F_9)|=10.
\]

Its unordered pairs form a 45-element set. W33 already has a distinguished 45-state carrier whose graph is the point graph of `GQ(4,2)`, namely

\[
\operatorname{SRG}(45,12,3,3).
\]

The cardinality match

\[
\binom{10}{2}=45
\]

therefore motivates a direct test. Does the W33 45-state graph arise as a natural projective orbital relation on the pair set of `P^1(F9)`?

## Exact answer

\[
\boxed{\text{No.}}
\]

The script constructs `F9=F3[i]/(i^2+1)`, all 720 Möbius transformations in `PGL(2,9)`, and their induced degree-45 action on unordered pairs.

For one pair, the `PGL(2,9)` stabilizer has order 16 and subdegrees

\[
\boxed{1,16,8,8,8,4}.
\]

All five nontrivial orbitals are self-paired, so there are only

\[
2^5-1=31
\]

nonempty undirected orbital fusions to test. The only connected nontrivial strongly regular graphs among them are

\[
\boxed{\operatorname{SRG}(45,16,8,4)}
\]

and its complement

\[
\boxed{\operatorname{SRG}(45,28,15,21)}.
\]

The degree-16 graph is exactly the triangular graph `T(10)`: two pair-vertices are adjacent iff the underlying 2-subsets intersect.

Neither

\[
\operatorname{SRG}(45,12,3,3)
\]

nor its complement

\[
\operatorname{SRG}(45,32,22,24)
\]

occurs.

Dropping to `PSL(2,9)` does not rescue the bridge. The pair stabilizer has order 8 and subdegrees

\[
\boxed{1,8,8,8,8,4,2,2,4}.
\]

After pairing transpose orbitals there are seven undirected atoms and hence 127 fusions. Their complete SRG census is

\[
2\times(45,2,1,0),
\quad
2\times(45,42,39,42),
\quad
1\times(45,16,8,4),
\quad
1\times(45,28,15,21).
\]

Again the GQ(4,2) parameters never occur.

Finally, a `PGammaL(2,9)`-invariant pair relation would in particular be `PGL(2,9)`-invariant, so the same no-go covers the semilinear enlargement.

## Interpretation

This closes the cheapest and most natural version of the open `P^1(F9)` / 45-state transport question.

The ten-state projective carrier and the W33 45-state GQ carrier have the same pair cardinality, but their natural orbital algebras are incompatible:

\[
\boxed{
\binom{\mathbb P^1(\mathbb F_9)}2
\not\cong_{m orbital}
GQ(4,2).
}
\]

That is exactly the kind of false bridge the repository's evidence firewall is designed to catch.

## Boundary

The theorem does **not** prove that no map of any kind exists between the two 45-element sets. It rules out the canonical symmetry-preserving pair-orbital construction under `PGL(2,9)`, `PSL(2,9)`, and therefore `PGammaL(2,9)`. A symmetry-breaking map, a different indexing object than unordered pairs, or a larger construction with auxiliary labels remains logically possible and would require its own explicit intertwiner.
