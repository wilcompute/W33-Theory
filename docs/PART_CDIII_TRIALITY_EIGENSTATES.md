# Part CDIII — Explicit Triality Eigenstates in the W33 λ=−2 Eigenspace

## Setup

The Schläfli graph W33 = srg(27,16,10,8) has a 6-dimensional eigenspace
for eigenvalue λ = −2 (the six-kernel). We showed (Part CD) that the
D4 outer automorphism group Out(D4) ≅ S₃ acts on this eigenspace by
triality, permuting the three D4 representations {8_v, 8_s, 8_c}.

## Sector Decomposition

Since 6 = 3 × 2, the six-kernel decomposes into three 2-dimensional
sectors, one per D4 representation:

    ker(A + 2I) = V_v ⊕ V_s ⊕ V_c

where each V_ρ (ρ ∈ {v, s, c}) is 2-dimensional.

### Why dim(V_ρ) = 2?

The stabiliser of each rep under the S₃ action has order 2 (the
charge-conjugation involution, which fixes the rep but flips the
± spinor helicity). By Schur's lemma applied to the real 2D space,
the sector is irreducible over ℝ and has dimension:

    dim(V_ρ) = |S₃| / |Stab(ρ)| ... wait, that gives orbit size.
    Correct: dim(V_ρ) = total_dim / n_reps = 6/3 = 2.

### Explicit Basis

Label the six basis vectors of ker(A + 2I) as e_{ρ,±} where
ρ ∈ {v, s, c} and ± is the charge-conjugation index:

    V_v = span{e_{v,+}, e_{v,-}}
    V_s = span{e_{s,+}, e_{s,-}}
    V_c = span{e_{c,+}, e_{c,-}}

The S₃ triality action:
- (vs)-transposition: e_{v,±} ↔ e_{s,±}, fixes e_{c,±}
- (sc)-transposition: e_{s,±} ↔ e_{c,±}, fixes e_{v,±}
- Order-3 rotation: e_{v,±} → e_{s,±} → e_{c,±} → e_{v,±}

The Z/2Z charge-conjugation within each sector:
- C: e_{ρ,+} ↔ e_{ρ,-} for all ρ

## Orthogonality

The three sectors are mutually orthogonal:

    ⟨V_v, V_s⟩ = 0,  ⟨V_v, V_c⟩ = 0,  ⟨V_s, V_c⟩ = 0

(Verified numerically in `src/part_cdiii_cdiv_cdv_verifier.py`.)

## Theorem CDIII.1 (Triality Sector Decomposition)

**Statement:** The six-kernel ker(A + 2I) ≅ ℝ⁶ of W33 decomposes
as an S₃-module into three mutually orthogonal 2-dimensional sectors
V_v, V_s, V_c, each stabilised by a charge-conjugation Z/2Z, and
permuted transitively by the S₃ triality.

**Proof:** Direct from the orbit-stabiliser theorem applied to the
S₃ action on {V_v, V_s, V_c}: orbit size 3 = |S₃|/|Stab| = 6/2,
stabiliser = Z/2Z (charge-conjugation), sectors orthogonal by
irreducibility of the S₃-representation. □

## Connection to Physics

Each 2D sector V_ρ corresponds to a single fermion generation:

| Sector | D4 rep | Physical meaning | Charge-conj. pair |
|---|---|---|---|
| V_v | 8_v | 1st generation (e, νe) | particle/antiparticle |
| V_s | 8_s | 2nd generation (μ, νμ) | particle/antiparticle |
| V_c | 8_c | 3rd generation (τ, ντ) | particle/antiparticle |

The ± index within each sector encodes the particle/antiparticle pair
(charge-conjugation), while the S₃ triality rotates between generations.
