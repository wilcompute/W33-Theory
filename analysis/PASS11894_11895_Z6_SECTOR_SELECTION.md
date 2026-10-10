# Passes 11894–11895: the ℤ₆ W(3,3) sector: flat modulus, one-loop SU(3)×SU(2)×U(1), and why the matter is wrong

Producer: `analysis/w33_pass11894_11895_z6_sector_selection.py`
Certificate: `data/w33_pass11894_11895_z6_sector_selection.json` (10/10 checks)
Regression: `tests/test_w33_pass11894_11895.py`
Track: Claude.

## Setting

Pass 11893 showed that the order-3 heterotic sector has no Standard Model at its radiative vacuum. This pass moves to
order six, where the corpus's flagship Standard Models live.

The order-6 twist is ℤ₆ = (A₈-class ℤ₃, the W(3,3) twist) × σ. Here σ is the D₈ "parity": +1 on the five CZ₃ zero-phase
levels {xy = 0} and −1 on the other four. These are the flagship holonomies of w33_paper §79.81–79.86.

**The local four-dimensional content:**
* gauge algebra s(u₅ ⊕ u₄), dimension 40;
* planes 1 and 2 (rotation 1/6) carry the σ-odd 44 of the 84, which is the ℤ₆ grade-1 space;
* plane 3 (rotation 2/3, the qutrit plane where the corpus finds the Higgs) carries the σ-even 40.

## 11894: the flat modulus survives at order six, in the family planes

**The family planes.** For (S(GL₅×GL₄), σ-odd 44):
* the generic stabiliser is 0;
* a generic element has a 4-dimensional commuting subspace;
* so the moduli dimension is 44 − 40 = 4, a Vinberg Cartan with the order-6 regular-element degrees (12, 18, 24, 30),
  the same as order 3.

**Flatness.** A Kempf–Ness flow to a minimal vector reaches |μ| ≈ 10⁻¹⁰. The Cartan through it lies in μ⁻¹(0) to about
5·10⁻⁹. On it the vector-mass traces are constant: Σe = 10, Σe² = 4. **The Siegel modulus survives at order six, in the
family planes.**

**The qutrit plane** (σ-even 40) has a 2-dimensional generic stabiliser, hence only 2-dimensional moduli.

## 11895: one loop selects SU(3)×SU(2)×U(1), with the wrong matter

**The vacuum.** The bosonic one-loop function F = Σe² log e on the order-6 Cartan has global minimum **−3 log 3** in all
runs, with spectrum 0¹² (1/3)²⁷ 1¹. At the polished point the unbroken compact algebra has:
* dimension 12, rank 4;
* a 1-dimensional centre;
* ideals of dimensions 1, 3 and 8.

**That is SU(3) × SU(2) × U(1), the Standard Model gauge group, selected dynamically**, which is a first for this
programme.

**On C⁹:**
* the 5 splits as 3 + 2, Georgi–Glashow-shaped;
* the 4 splits as 3 + 1, the Pati–Salam "lepton as fourth colour" split;
* so the SU(3) is the **diagonal** of a GG colour and a PS colour. The U(1) charges are 0 on both triplets, −½ on the
  doublet and +1 on the singlet.

**Matter**, from 3-forms, so charges add over three indices:

| sector | content |
|---|---|
| each family plane (44) | 2(3,1)₊₁ + (3,1)₋₁ + (3,2)₊½ + (3,2)₋½ + **(6,2)₋½** + **(8,1)₀** + 3(1,1)₀ |
| qutrit plane (40) | (3,1)₊₁ + (3,1)₋₁ + **(6,1)₊₁** + (3,2)₊½ + 2(3,2)₋½ + **(8,1)₀** + 2(1,1)₀ |

Dimensions check: 44 = 6+3+6+6+12+8+3 and 40 = 3+3+6+6+12+8+2. There are colour sextets and octets, and **no colour-singlet SU(2) doublet
at all**, so no lepton doublet. **The right gauge group with the wrong matter: no Standard Model in the untwisted ℤ₆
sector at this vacuum.**

## The mechanism, and the fix it points to

**Why the exotics appear.** They come from the *diagonal* colour. With one SU(3) acting on two triplets, 3-forms produce
3⊗3 = 6 ⊕ 3̄ and 3⊗3̄ = 8 ⊕ 1. Standard-Model matter requires colour to act on a single triplet.

**Why one loop chooses the diagonal.** Michel's maximal-isotropy logic favours the larger diagonal stabiliser, which
locks the two triplets together.

**What breaks it.** The flagship's CZ₃ Wilson line, with multiplicities 5 + 2 + 2 on C⁹, splits the 4 as 2 + 2, so it
explicitly breaks that locking. The corpus already finds Standard Models with these Wilson lines.

**The concrete next test:** run the flat-direction and one-loop machinery with the Wilson line included, on the flagship's
actual 4d gauge group and projected matter. This determines whether vacuum selection keeps exactly SU(3)×SU(2)×U(1) with
Standard-Model matter.

## Scope

* Untwisted sector only.
* The local (fixed-point) gauge group, without Wilson lines.
* Bosonic one loop only.
* σ is fixed as the CZ₃-cross parity of §79.81–79.83.
* The (3̄ versus 3) labels in the table come from Casimir values; conjugate pairs are not resolved.

## Prior art

* Vinberg θ-groups and Springer regular elements.
* Kempf–Ness.
* Michel's conjecture.
* Pati–Salam (1974) and Georgi–Glashow (1974).
* Corpus: w33_paper §79.81–79.86 (flagship CZ₃ and θ₃ holonomies), Passes 11714, 11879–11893.
