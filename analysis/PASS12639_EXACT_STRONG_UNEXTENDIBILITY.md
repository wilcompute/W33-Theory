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
