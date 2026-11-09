# Pass 12639: an exact theorem — every two-qutrit pentad is a strongly unextendible set of 5 MUBs

Claude track. Scripts: `analysis/w33_strong_umub_exact.py` (exact Q(ω) arithmetic), `w33_sos_degree6.py` and `w33_sos_factorisation.py`, with JSON in `data/`. Continues Passes 12636–12638.

**Not a theory of everything.** A finite, exact quantum-information theorem.

## Theorem

Let S be any of the 432 maximal partial spreads of size 5 of W(3,3), i.e. any 5 two-qutrit Pauli classes whose stabiliser bases are mutually unbiased and admit no further Pauli-class MUB. Let E be its 45 basis states. Then for every v ∈ C⁹:

  Σ_{e ∈ E} (|⟨e|v⟩|² − |v|²/9)² ≥ |v|⁴ / 9.

**In particular, no vector is unbiased to all five bases: S is strongly unextendible.** The bound is not tight; the true minimum on the unit sphere is 0.14711.

## Proof

1. **Reduction to an eigenvalue.** F(v) = Σ_e (v†A_e v)² with A_e = |e⟩⟨e| − I/9 is a Hermitian (2,2)-form, F(v) = (v⊗v)† M (v⊗v) with M = Σ_e A_e⊗A_e. On Sym²(C⁹) the representing operator is unique, and |v|⁴ = (v⊗v)†Π(v⊗v) with Π = (I + SWAP)/2. So F ≥ δ|v|⁴ holds for every δ ≤ λ_min(ΠMΠ restricted to Sym²).
2. **Exact computation.** The stabiliser projectors are P = (1/9)Σ_{a,b} ω^{−(ja+kb)} W_u^a W_v^b, with entries in Q(ω). With X = ΠMΠ, the identity **Π(X − Π/9)(X − 16Π/9) = 0** holds **exactly** over Q(ω), checked on four pentads. So the spectrum of X on Sym² lies in {1/9, 16/9}, and numerically the multiplicities are 36 and 9.
3. **All 432.** Clifford unitaries act on M by (U⊗U)·(U⊗U)†, and complex conjugation (the antiunitary coset) acts by entrywise conjugation. Neither changes the spectrum, and together they act transitively on the 432 pentads (one PGSp(4,3)-orbit). ∎

**Companion statement**, proved the same way: every size-8 set (the 135) satisfies F ≥ 4|v|⁴/9, which is tight. Exactly, Π(X − 4Π/9)(X − 16Π/9) = 0. Its 16/9 eigenspace is **exactly the Λ²⊗Λ² of its own tensor factorisation**, and its 4/9 eigenspace is Sym²⊗Sym². For pentads the 9-dimensional eigenspace is not any split's Λ²⊗Λ², so their 36 + 9 decomposition has another origin (open).

## Context

- **Strong unextendibility:** Mandayam, Bandyopadhyay, Grassl and Wootters (arXiv:1302.3709) defined it. Szántó (arXiv:1502.05245) constructs strongly unextendible MUB sets in dimension p², p ≡ 3 (mod 4), of size 8 for p = 3. **The pentads give strongly unextendible sets of only 5 bases in dimension 9**, and no Pauli-class 4-set is strongly unextendible (Pass 12638), so 5 is the minimum among Pauli-class sets.
- **Geometric meaning** (Passes 12634–12636): the 432 pentads are the 432 positive-geometry regions of the real moduli space of marked cubic surfaces (E6 pezzotopes). The two chiralities are exchanged by the Kramers reversal, the Weyl reflection in a double-six root.

## The other rungs (items 2 and 3)

Spectra of the degree-4 certificate operator on Sym², eigenvalue × d (multiplicity):

| set | spectrum | degree-4 bound | degree-6 bound |
|---|---|---:|---:|
| two qubits, size 3 | 1 (9), 9 (1) | 1/4, tight: **proved strongly unextendible** | — |
| three qubits, size 5 | −5 (6), 3 (20), 11 (10) | −5/8, fails | −0.164, fails |
| two qutrits, size 5 | 1 (36), 16 (9) | **1/9, proved exactly** | 1/9 (no gain) |
| two qutrits, size 8 | 4 (36), 16 (9) | **4/9, tight, proved exactly** | — |

The three-qubit size-5 sets are strongly unextendible numerically (min 1/8), but the Hermitian relaxations at degrees 4 and 6 do not certify it. A different method is needed, such as A5 symmetry reduction with non-Hermitian SOS. This is open.

## Item 4: E8

No region count for the real moduli of degree-1 del Pezzo surfaces is known (Pass 12638), so no test is possible this round. The method remains a sign-pattern count over W(E8) chambers with the E8 analogues of the Yoshida products.

## Addendum: a conceptual proof — the doily's S6 and a Jucys–Murphy element (`w33_sentinel_identity.py`, `w33_doily_s6_kramers.py`)

The spectrum {1/9, 16/9} is a fact about the symmetric group S6. All steps were checked numerically: the first two on all 432 pentads, the rest on one pentad, which suffices by Clifford transitivity.

1. **Twirl identity.** For a stabiliser basis, Σ_e P_e⊗P_e = (1/9)Σ_{g∈G_L} g⊗g†. Hence M = (1/9)Σ_{u covered} W_u⊗W_u†. With SWAP = (1/9)Σ_{all u} W_u⊗W_u†, this gives **M = (8 − T_U)/9 on Sym²**, where T_U sums over the 40 uncovered Pauli vectors.
2. **The sentinel double cover** (Pass 12523; checked on 432/432). A pentad's 20 uncovered points are covered exactly twice by **5 sentinel splits** {b, b⊥}. Each contributes 3S_A + 3S_B − 2, and S_A = S_B on Sym². Hence **M = (13 − 3R)/9 with R = S₁ + … + S₅**, a sum of five factor-swap involutions.
3. **The doily's S6.** The five sentinel swaps satisfy the star-transposition presentation of S6: t² = 1, (t_k t_l)³ = 1 and (t_k t_l t_k t_m)² = 1, all to 10⁻⁸ in floating point. The 10 conjugates t_k t_l t_k are also swap operators of splits. **The resulting 15 transpositions are the swap operators of exactly the 15 splits whose factors the codeword's Kramers reversal θ exchanges**: 1 of the 36 θ's matches, and that is θ's whole swapped set. These 15 splits and 15 frames form the doily GQ(2,2) of Pass 12523, whose automorphism group is S6 ≅ Sp(4,2). **So R = (1 6) + … + (5 6) is the Jucys–Murphy element J₆.**
4. **Representation theory.** On Sym²(C⁹) the character is 45 / 27 / 18 on identity / transposition / 3-cycle, consistent with 9·χ_(5,1). The identification is forced: J₆'s eigenvalues on an irreducible are the contents of its corner boxes, and (5,1) is the only partition of 6 whose corners have contents in {4, −1}. Together with dimension 45, this gives 9·(5,1). J₆ acts on (5,1) with eigenvalues the contents of the corner boxes: 4 at box (1,5), multiplicity 4, and −1 at box (2,1), multiplicity 1. So R has eigenvalues 4 (multiplicity 36) and −1 (multiplicity 9), and **M = (13 − 3R)/9 has spectrum {1/9, 16/9}**. ∎

The pentad's 9-dimensional block (item 1) is thus ker(R + 1): the one box of each standard representation where the sixth letter sits in the second row. The size-8 sets are the degenerate case: their uncovered set is a single split, R = S_A, and the spectrum is {(8 − 4)/9, (8 + 8)/9} = {4/9, 16/9}.

**Status.** Steps 1–2 are algebraic identities verified on all 432 pentads. Step 3's relations and split identifications are checked numerically, as exact matrix identities up to 10⁻⁸, on one pentad. Step 4 is standard (Okounkov–Vershik). An independent exact replay is requested from the other track.

## Addendum 2: the sentinel principle across rungs, and the pentad's S5 (`w33_sentinel_rungs.py`, `w33_pentad_stab_doily.py`)

**One formula.** On Sym²(C^d), M = (d − 1 − T_U)/d with T_U summed over the uncovered Pauli vectors. Certification works exactly when the uncovered set is covered uniformly by tensor factorisations:

| set | uncovered points | factorisation cover | spec M |
|---|---:|---|---|
| two qubits, size 3 | 6 | 1 split, covered once | {1/4, 9/4}: proved |
| two qutrits, size 8 | 8 | 1 split, covered once | {4/9, 16/9}: proved |
| two qutrits, size 5 | 20 | 5 splits, covered twice (doily S6, J₆) | {1/9, 16/9}: proved |
| three qubits, size 5 | 28 | none; not a quadric set of any of the 64 forms | contains −5/8: fails |

**The pentad's S5.** Its stabiliser in PSp(4,3) has order 120 and acts faithfully on the 5 sentinels as the full S5, preserving the doily's 15 splits. It is the stabiliser of the doily letter shared by the sentinels. **Write-up:** `analysis/NOTE_STRONG_UNEXTENDIBILITY_PROOF.md` (two pages).

**Item 5 (E8): not attempted.** The degree-1 del Pezzo region count remains unknown, and computing it needs the E8 analogue of the Yoshida sign-pattern machinery.
