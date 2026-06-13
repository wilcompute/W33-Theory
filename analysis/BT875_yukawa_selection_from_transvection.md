# BT875 — The Yukawa Selection Rule Is Z₃ Grade Conservation Under the Long-Root Transvection

**Status: PROVEN (machine-verified, `analysis/bt875_yukawa_selection_from_transvection.py`, data `data/bt875_yukawa_selection_from_transvection.json`)**

Closing the BT874 open: Pillar 68's exact mass-texture selection rule
(T[a,b,v]=0 unless the Z₃ grades sum to 0, with grade-g eigenspaces of dim 9
— the CKM/PMNS origin) is now *derived* from the long-root transvection R.

## The derivation

- **T1:** C[27-shell] decomposes under R (the BT874 transvection) into three
  eigenspaces of eigenvalues 1, ω, ω² with **dim 9 each** — exactly Pillar
  68's grade-g eigenspaces.
- **T2 (the rule):** any R-equivariant triple coupling on the matter shell is
  supported on exactly the **9 of 27 grade-triples (g₁,g₂,g₃) with
  g₁+g₂+g₃ ≡ 0 (mod 3)** — the Z₃ Clebsch–Gordan rule (grade-a ⊗ grade-b
  lands in grade-(a+b)). Since R is a substrate symmetry, the Yukawa tensor
  is R-equivariant, so **T[a,b,v] = 0 unless the grades sum to zero** is
  forced. The CKM/PMNS texture is Z₃ momentum conservation in the long-root
  grade.
- **T3:** the within-shell collinear triples (the Yukawa vertices) number
  **36** — matching Pillar 69's "Heisenberg-twisted" triad count (the 45 E₆
  tritangent triads split 9 fiber + 36 twisted). The matter coupling lives on
  these 36, pinned by R-equivariance to grade-conserving generation channels.

## Reading

The fermion mass-texture structure — long the most arbitrary-looking part of
the Standard Model — is here a **consequence of one group element**: the
long-root transvection R (BT874) grades the matter shell 9+9+9, and Z₃
Clebsch–Gordan then forbids all but the grade-conserving Yukawa couplings.
The chain is complete:

```text
master equation → q=3 → W(3,3) → point shell = Heisenberg torsor (BT858)
 → R = long-root transvection = Heisenberg centre (BT874)
 → C[27] = 9⊕9⊕9 grade decomposition (Pillar 68's grades)
 → Yukawa selection rule = Z₃ grade conservation (this packet)
```

so generation count (BT863, Steinberg vanishing), generation chirality
(BT869, polar-pair involution), and generation texture (this) are all
representation-theoretic facts about the order-3 long-root element acting on
the substrate's matter sector — zero free parameters.

## Open

- The exact CKM/PMNS angles from the 36 grade-conserving channels' relative
  weights (Pillar 65/66's optimization, now with the grading derived rather
  than imposed).
- The 9 "fiber" triads (45 − 36) and their role: the diagonal/self-coupling
  generation channels.
