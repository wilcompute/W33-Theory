# Five two-qutrit MUBs that admit no unbiased vector: a proof through the symmetric group S6

*Two-page note. Exact verification: `analysis/w33_strong_umub_exact.py`. Conceptual steps: `w33_sentinel_identity.py`, `w33_doily_s6_kramers.py`, `w33_sentinel_rungs.py`, `w33_pentad_stab_doily.py` (Passes 12636–12639).*

## Statement

Index two-qutrit Paulis W_u = X^{u₁}Z^{u₃} ⊗ X^{u₂}Z^{u₄} by u ∈ F₃⁴, with symplectic form [u, v]. A maximal commuting class is an isotropic plane L (8 nonzero vectors), with a stabiliser basis B_L. Two bases are mutually unbiased iff their planes meet only in 0.

A **pentad** is a set of 5 pairwise trivially-intersecting planes that cannot be enlarged. Up to the Clifford group with its antiunitary coset there is exactly one, and 432 in total.

> **Theorem.** For every pentad, with E its 45 basis states, and every v ∈ C⁹:
>   Σ_{e∈E} (|⟨e|v⟩|² − |v|²/9)² ≥ |v|⁴/9.
> In particular, no vector is unbiased to all five bases: pentads are strongly unextendible. Any four of the five bases do admit unbiased vectors.

## Proof

**1. Twirl.** For a stabiliser basis, Σ_{e∈B_L} |e⟩⟨e| ⊗ |e⟩⟨e| = (1/9) Σ_{u∈L} W_u ⊗ W_u†. With A_e = |e⟩⟨e| − I/9, M := Σ_e A_e ⊗ A_e equals (1/9) Σ_{u covered, u≠0} W_u ⊗ W_u†. The left side of the theorem is (v⊗v)† M (v⊗v), and |v|⁴ = (v⊗v)†Π(v⊗v) with Π = (1 + SWAP)/2. Since SWAP = (1/9) Σ_{all u} W_u ⊗ W_u†, on Sym²(C⁹):

  M = (8 − T)/9,  T = Σ_{u uncovered, u≠0} W_u ⊗ W_u†.

**2. Sentinels.** A pentad covers 20 of the 40 points of PG(3,3). The other 20 are covered **exactly twice** by five *sentinels*: pairs {b, b⊥} of non-degenerate planes, i.e. tensor factorisations C⁹ = C³⊗C³. For a factorisation, Σ_{u∈b∪b⊥, u≠0} W_u ⊗ W_u† = 3S_A + 3S_B − 2, where S_A and S_B swap the first and second tensor factors between the two copies. On Sym², S_A S_B = SWAP = 1, so S_A = S_B =: S. Hence

  M = (13 − 3R)/9,  R = S₁ + S₂ + S₃ + S₄ + S₅.

**3. The symmetric group.** The S_k are involutions with (S_k S_l)³ = 1 and (S_k S_l S_k S_m)² = 1 for distinct indices, the defining relations of the star transpositions (k 6) in S6. The ten conjugates S_k S_l S_k are again factor swaps. The fifteen factorisations so obtained are exactly those whose two factors are exchanged by one antiunitary Clifford involution, a Kramers reversal; together with fifteen frames they form a generalised quadrangle GQ(2,2) with automorphism group S6. Thus R = Σ_{k≤5} (k 6) is the **Jucys–Murphy element** J₆ of this S6 acting on Sym²(C⁹).

**4. Contents.** The eigenvalues of J₆ on an irreducible S_λ are the contents (column − row) of the boxes where 6 can sit. The character of Sym²(C⁹) (45, 27, 18 on identity, transposition, 3-cycle) is 9·χ_(5,1). On (5,1) the possible boxes are (1,5), with content 4 and multiplicity 4, and (2,1), with content −1 and multiplicity 1. So R has eigenvalues 4 (multiplicity 36) and −1 (multiplicity 9), and **spec M = {(13 − 12)/9, (13 + 3)/9} = {1/9, 16/9}**. Hence F ≥ |v|⁴/9. ∎

*Exactness.* The identity Π(X − Π/9)(X − 16Π/9) = 0 for X = ΠMΠ was checked in exact arithmetic over Q(ω) on four pentads. Clifford unitaries act on M by conjugation with U ⊗ U and complex conjugation by entrywise conjugation, so the spectrum is the same for all 432.

## Remarks

- **The same mechanism, with one factorisation.** A weakly unextendible set of 8 two-qutrit MUBs (135 of them: the 24 entangled stabiliser bases of a factorisation fall into 3 such sets) has its uncovered points equal to a single factorisation. Then R = S and spec M = {4/9, 16/9}, a tight bound: min F = 4/9. Szántó constructs size-8 strongly unextendible sets in dimension p² (arXiv:1502.05245). The two-qubit unextendible triples of Mandayam, Bandyopadhyay, Grassl and Wootters (arXiv:1302.3709) are the case d = 4, with spec M = {1/4, 9/4}.
- **Where it stops.** Three-qubit unextendible 5-sets have uncovered sets with no factorisation cover (8 = 2·4 is unbalanced), and the Hermitian bound is negative there (−5/8 at degree 4).
- **Symmetry.** A pentad's stabiliser (order 120) is the S5 fixing the sixth letter of this S6. It acts faithfully on the five sentinels.
- **Geometry.** The 432 pentads are the 432 real regions of the moduli space of marked cubic surfaces (positive geometries; Early, Geiger, Panizzut, Sturmfels and Yun, arXiv:2306.13604). The Kramers reversal is the Weyl reflection exchanging the two chiralities.

## The general mechanism (sentinel theorem, d = p²)

**Theorem (sentinel principle).** Let S be a maximal partial spread of W(3,p) (a weakly unextendible set of two-qupit Pauli MUBs in C^{p²}). Suppose its uncovered points are covered exactly m times by s splits {b_k, b_k⊥}, i.e. tensor factorisations, with swap involutions S_k on Sym²(C^{p²}). Then on Sym²:

  M = (d − 1 + 2s/m − (2p/m)·R)/d,  R = S₁ + … + S_s,  d = p²,

so that

  F(v) ≥ δ|v|⁴ with δ = (d − 1 + 2s/m − (2p/m)·λ_max(R))/d.

*Proof.* As in steps 1–2 above: Σ_{u∈⟨b⟩, u≠0} W_u⊗W_u† = p·S_A − 1 for a p-dimensional factor, and S_A = S_B on Sym². ∎

**Instances.**

| case | (p, s, m) | spectrum of R | δ |
|---|---|---|---|
| two-qutrit pentads | (3, 5, 2) | R = J₆ of the doily S6, spec {4, −1} | 1/9 |
| two-qutrit size-8 sets | (3, 1, 1) | R = S, spec {±1} | 4/9 |
| two-ququint size-24 sets | (5, 1, 1) | R = S | 16/25 |
| two-ququint size-22 sets | (5, 2, 1) | R = S₁ + S₂, spec ⊂ {2, 0, −2} | 8/25 |
| general one-split case | (p, 1, 1) | R = S | (p − 1)²/p² |

In the random d = 25 sample (Pass 12640), every certified set was of this form and every non-uniform set failed: δ* ≤ 0 for all 20 of them.

## Operational corollary (the other track, `analysis/2026-11-09_umub_operational_margin.md`)

From Σ_j (p_j − 1/9)² ≥ δ_k over the 9k outcomes, **some outcome deviates by at least √(δ_k/9k)**. That is 1/(9√5) ≈ 0.0497 for the pentads and 1/(9√2) ≈ 0.0786 for the size-8 sets. With calibrated measurement errors of operator norm ≤ ε, the deviation survives up to ε, which gives a finite-shot witness that a prepared pure state cannot be unbiased to all five bases. Exact Z[ω] replay of all 603 maximal partial spreads: the other track's 7332f3b48.
