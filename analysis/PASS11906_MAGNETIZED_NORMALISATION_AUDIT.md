# Pass 11906: magnetized normalisation audit — the level-3 texture of Passes 11904–11905 is exact

Producer: `analysis/w33_pass11906_magnetized_normalisation_audit.py`
Certificate: `data/w33_pass11906_magnetized_normalisation_audit.json`
Regression: `tests/test_w33_pass11906.py` (slow, about 3 min)
Track: Claude.

## Why

Passes 11904 and 11905 used the level-3 texture θ[c/3,0](z, Ω) as a stand-in for magnetized Yukawas. The parallel
track's TOE45 asked for an independent audit of the flux normalisation. Its TOE46 front 4 then computed normalised
flux-(3,3,6) overlaps, but only for equal left/right backgrounds.

## Method

**Wavefunctions.** Normalised zero modes on T² (unit-area convention) for fluxes 3, 3 and 6, with Wilson lines
ζ₁, ζ₂ and ζ₃ = (3ζ₁ + 3ζ₂)/6.

**Yukawas.** Y_ijk are computed as **direct overlap integrals** on a grid; no theta-product formula is assumed. The
relative Wilson line is ζ = ζ₁ − ζ₂.

## Results

| check | result |
|---|---|
| TOE46 cross-check (equal backgrounds, τ = 1.45i): lowest allowed overlap | **0.0031126747** reproduced; forbidden overlaps ≤ 4·10⁻¹⁶ |
| selection rule | k ≡ i + j (mod 3) |
| **exact dictionary**: normalised physical masses (localised Higgs) vs \|θ[c/3,0](3ζ, 6τ)\|, up to a permutation, random τ and ζ | max error **6·10⁻¹⁶** |
| theta-zero law in true normalisation (Re ζ = 1/6; Im ζ/Im τ = 1/3, 1, 5/3) | one mass vanishes (≤ 10⁻¹⁷) and the other two are equal |
| symmetric points ζ = m/6 + kτ/3 (Im ζ/Im τ = 0, 1/3, 2/3) | two masses coincide (≤ 10⁻¹⁰) |
| non-fixed points Im ζ/Im τ = 1/6, 1/2, 5/6 | no coincidence |
| Gaussian invariant m₁m₂/m₀² for generic ν | e^{−(4π/3) Im τ} = e^{−2π Im Ω/9}, to 0.3 % |
| observed-order up ratios (m_c/m_t = 3.6·10⁻³, m_u/m_c = 1.7·10⁻³) | reached at **Im τ = 4.209, ν = 0.1206**, i.e. Im Ω = 25.25 and δ = ν/2 = 0.0603: exactly the Pass 11904 point, found independently |

## Reading

The texture of 11904–11905 **is** the physical magnetized texture, under the dictionary **z = 3ζ** (relative Wilson
line times the flux) and **Ω = 6τ**. So the following hold in true normalisation:
* the theta-zero law ("a massless up quark forces top = charm");
* the symmetric-Wilson-line degeneracy theorem;
* the Gaussian invariant;
* the hierarchy point.

This complements TOE46's equal-background lock, which is the ν = 0 symmetric point here.

## Drafting note (failure mode recorded)

An intermediate draft of this pass claimed two things that turned out false:
* that Re ζ enters only as a phase;
* that the physical masses never vanish.

Both came from scanning only the slice Re ζ = 0, ν ∈ [0,1). A direct test at Re ζ = 1/6 refuted them before commit: the
zeros are there, and the Re-dependence is O(1) near them. The lesson is to state which space a negative scan covered,
as in the corpus rule "READ, don't grep-and-discard".

## Prior art

* Cremades–Ibáñez–Marchesano (hep-th/0404229).
* TOE45 and TOE46 (parallel track).
* Corpus: 11904, 11905.
