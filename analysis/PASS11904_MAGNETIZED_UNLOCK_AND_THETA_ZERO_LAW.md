# Pass 11904: the magnetized home unlocks charm–up; a massless up forces top = charm; the remaining heterotic levers

Producer: `analysis/w33_pass11904_magnetized_unlock_and_theta_zero_law.py`
Certificate: `data/w33_pass11904_magnetized_unlock_and_theta_zero_law.json`
Regression: `tests/test_w33_pass11904.py`
Track: Claude.

This pass executes options 2 and 3 of the 11902 report. Option 1 (the new scan) is Pass 11903.

## Option 3: magnetized T⁴ (flux 3 on each torus)

The zero modes at the origin are the level-3 Siegel thetas of Pass 11869, i.e. two qutrits. With a localised Higgs, the
light-pair couplings are θ[(±1/3, a/3), 0](ζ, Ω).

| lever | heterotic ℤ₃ (Passes 11900–11903) | magnetized T⁴ (here) |
|---|---|---|
| a = 0 (local 10), no Wilson line | locked for all moduli | locked for all Ω (evenness; ≤ 4·10⁻¹⁶) |
| a ≠ 0, off-diagonal modulus | split at **third** order in Z₁₂ | split at **first** order in Ω₁₂ (split/s = 2.77–2.78) |
| Wilson line | quantised Pauli displacement: relabels classes, no split | continuous: split at **first** order even at a = 0 (split/ζ = 4.44–4.47) |

**Why the heterotic split is cubic.** In heterotic ℤ₃ the period lattice is Eisenstein, and ω ≡ 1 mod √−3 fixes each
coset. A real period lattice has no such rigidity, so the split appears at linear order.

**Why the magnetized Wilson line works.** A magnetized Wilson line is a continuous Weyl displacement. It breaks θ
evenness, which a finite Pauli shift cannot do.

## The theta-zero law

**Statement.** For genus 1, level 3 and any Ω, θ[a,0](z, Ω) vanishes at z* = ½ + (½ − a)Ω. At that point,
**|θ[a + ⅓](z*)| = |θ[a − ⅓](z*)|**.

**Proof.** Write θ[a'](z*) = e^{iπa'} e^{−iπΩ(½−a)²} Σ_n (−1)ⁿ e^{iπΩ(n+b)²}, with b = a' + ½ − a. The substitution
n → −1−n maps b → 1−b, and the two sums agree up to sign. So b = ½ vanishes, and b = ½ ± ⅓ give equal modulus.

**Numerical check.** Over 30 random Ω and all three zeros, the maximum relative difference is 6.5·10⁻¹⁶. A generic
point has a spread of 0.21, so the check is not vacuous.

**Physical reading.** With a localised Higgs, an **exactly massless up quark forces top = charm**. One identity
explains three earlier observations:
* Pass 11114's Hesse alignments (1,1,ω) → (1,1,0);
* the symmetric Kähler points of Pass 11899, which give (1,1,0);
* the magnetized Wilson-line zeros.

So the up hierarchy cannot come from sitting near a theta zero, where m_c ≈ m_t.

## The Gaussian (near-cusp) regime

For large Im Ω, ln|θ_c| ≈ −π Im Ω (c/3 − δ)² + const. This gives two relations:
* **m_u m_c / m_t² = e^{−2π Im Ω/9}**, independent of the Wilson-line offset δ (verified to 2·10⁻⁶ for δ ≤ 0.1, with
  corrections from the next lattice term growing as δ → ⅙);
* **m_u / m_c = e^{−4π Im Ω δ/3}**.

So the torus area sets the product and the continuous Wilson line sets the split.

Observed-order up ratios (m_c/m_t = 3.6·10⁻³ and m_u/m_c = 1.7·10⁻³, illustrative) are reached exactly at
**Im Ω = 25.25, δ = 0.0603**. That is two parameters for two ratios, so it shows existence, not a prediction.

**The magnetized two-qutrit home can carry the up hierarchy, and the heterotic class of 11901–11903 cannot.**

## Option 2: non-renormalisable × Kähler in the heterotic survivors (closing argument)

The argument has four steps:

1. **Same order.** Pass 11103 found that the charm and up entries arise at the same VEV order: there is no parametric
   gap.
2. **Only the coefficients can differ.** Their coefficients differ only if the family-torus reflection is broken.
3. **Only one source.** With the Wilson-line classes fixed by the local 10 (Pass 11903), the only modulus that breaks it
   is the off-diagonal Kähler modulus. It enters couplings that span a Wilson-line torus, at O(Z₁₂³) (Pass 11900).
4. **Hence m_u/m_c = 1 + O(Z³).** There is no parametric hierarchy.

This is an argument assembled from certified pieces; no new coefficient computation was run.

## Not established

* The magnetized couplings use the generic Siegel theta with characteristic ±⅓ and a single Wilson-line argument. The
  full magnetized Yukawa normalisation is not built: the level is set by the product of fluxes, and Higgs flux 6 makes
  the level-54 theta. The symmetry and scaling statements do not depend on the normalisation.
* No magnetized model with the full Standard-Model spectrum is constructed. Kobayashi et al. have many; this pass makes
  no new model claim.
* The Gaussian fit is illustrative.

## Prior art

* Cremades–Ibáñez–Marchesano (2004): Yukawa couplings in magnetized/intersecting branes, with Wilson-line dependence.
* Abe–Kobayashi–Ohki et al.: magnetized orbifold three-generation models.
* Kikuchi–Kobayashi–Nasu–Takada–Uchida: Siegel-modular magnetized T⁴/T⁶ (arXiv:2309.16447 and JHEP 2024).
* Arkani-Hamed–Schmaltz: split fermions and Gaussian overlaps.
* Corpus: 11103, 11114, 11869, 11899, 11900–11903.
