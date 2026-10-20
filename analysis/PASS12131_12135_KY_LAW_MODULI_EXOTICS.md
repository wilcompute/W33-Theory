# Passes 12131–12135: the k_Y law, S002's moduli and tachyons, exotics to quartic order, A8 down sector, a third line on S002

Claude track. Producer: `analysis/w33_pass12131_to_12135_kY_law_moduli_exotics.py`. Drivers and frozen outputs:
`analysis/search_drivers_12131/`.

## 12131: k_Y = 5/3 + 4n from lattice self-duality

**Argument.**

1. Let q = a_L/2 + y be the charge vector, and λ a colour fundamental weight.
2. Suppose every state of the lattice spectrum has quantised charge.
3. Then q ± λ pairs integrally with all of Λ = E8×E8.
4. Λ is self-dual, so **q ± λ ∈ Λ**.
5. Its norm N = ½ + y² + ⅔ is even, so k_Y = 2y² = 2N − 7/3 = **5/3 + 4n**.

This is Schellekens's 1990 self-duality reasoning (cited in 11024), specialised to these models.

**Checks.**

- All 51 fraction-free hypercharges of 12126 satisfy it: q ± λ ∈ Λ with N ∈ {4, 6, 8, 10, 12, 18, 36}.
- **k_Y = 5/3 ⇔ q ± λ is a root.** Enumerating all 480 roots gives exactly 24 admissible hypercharges per model.
- None of those 24 yields the SM spectrum, in 5 of 5 models. So a fraction-free k_Y = 5/3 is impossible in these
  models, not merely unfound.

## 12132: S002's one-loop potential and tachyons

**Engines.** The potential uses the 11106 engine; the tachyon search uses the 11107 enumerator. Controls: model 2 gives
Δ = −0.2113 at Im T = 1, and nothing at large radius.

**Potential.**

| T_WL (T\* = ρ) | 3i | 2.5i | 2i | 1.75i | 1.5i | 1.25i | i | 0.8i |
|---|---|---|---|---|---|---|---|---|
| Λ/M⁴ | 1475 | 1037 | 678 | 528 | 398 | 289 | 199 | 145 |

| T\* (T_WL = 2i) | ρ | i | 1.5i | 2i |
|---|---|---|---|---|
| Λ/M⁴ | 678 | 708 | 821 | 1030 |

- Λ > 0 everywhere sampled.
- It falls monotonically as the Wilson-line tori shrink. There is no T-duality turnaround, so T_WL = i is not a minimum.
- Among the family-modulus points, Λ is lowest at T\* = ρ.

**Tachyons.** S002 is **tachyon-free along the whole sampled imaginary axis (3i … 0.7i)**. That is unlike every A8
survivor of 11106/11107, which were all tachyonic by Im T_WL = 1 except model 77.

Off the axis a tachyon appears:

- on the arc |T_WL| = 1, between 80° and 75°: 56 states, with Δ = −0.012 at 75°, −0.029 at 70° and −0.043 at 65°;
- at ρ, Δ = −1/18.

So the Λ values at the arc point (183) and at ρ (124) are void.

**Reading.** The Wilson-line moduli roll toward small radius with Λ > 0. No minimum was found, and the dilaton tadpole
remains.

## 12133: exotic masses up to quartic order

**Rules.** ψψ⟨s⟩ terms use all rules. ψψ⟨s₁⟩⟨s₂⟩ terms use gauge and space-group rules only. So a lift is an upper
bound, and a state that stays light is robust.

| model | light pairs, trilinear | light pairs, up to quartic |
|---|---|---|
| T115 | 7 | **1** (a vector-like lepton-doublet pair) |
| S002 | 41 | 12, including 9 pairs of charge ±1/3 that stay massless |

T115 is therefore one Dirac lepton doublet away from an exotic-free spectrum at this order.

## 12134: down-sector mixing in the 104 A8 models

The models' own nsosm hypercharge is used, with local couplings as in 11098.

- **11098 is reproduced exactly:** no tree-level down Yukawa in 77 models, rank 3 in 27.
- **Vector-like mixing changes no rank.** In the 77 models, no D-type state (chiral or vector-like) has a Q·D·H coupling.
- Local trilinear singlet couplings lift all vector-like d^c pairs in only 8 of the 92 models that have them.

## 12135 (negative): a third Wilson line on S002

I tried 250 candidates; 78 load. None gives first-E8 SU(3)×SU(2)×U(1): the groups are A1, A1+A1, A1+A1+A1, A2 and
A2+A1+A1. S002's Yukawa mechanism and T115's gauge group are not combined by one more line.
