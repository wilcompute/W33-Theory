# Pass 11896: the flagship tension: with the CZ₃ Wilson line, the flat directions are Standard-Model charged

Producer: `analysis/w33_pass11896_flagship_tension.py`
Certificate: `data/w33_pass11896_flagship_tension.json` (5/5 checks)
Regression: `tests/test_w33_pass11896.py`
Track: Claude.

## Setting

The flagship's holonomies (w33_paper §79.81–79.86, Pass 79.85's scope correction) are:
* the order-two θ₃ = σ′, with a 5 + 4 split;
* the order-three CZ₃ Wilson line W₃ = diag(ω^{xy}), with a 5 + 2 + 2 split.

They commute, and their joint multiplicities are (3,2,1,1,1,1); this is reproduced here. The local gauge algebra is the
joint centraliser **su(3) ⊕ su(2) ⊕ u(1)⁵** (16-dimensional).

## Matter (untwisted, projected by both holonomies)

**Family plane:** σ′-odd and W₃-invariant 3-forms, 16 states. The block labels are A (3), B (2), and single levels
c, d, e, f.

| type | representation | reading |
|---|---|---|
| AAB | (3̄,2) | quark doublet (conjugate convention) |
| A c e, A d f | 2 × (3,1) | the two antiquark singlets |
| B c d, B e f | 2 × (1,2) | lepton / Higgs doublets |

This is a family missing e^c. It is consistent with the corpus's finding that families are split between untwisted and
twisted sectors (Holotrade 3caf15e, Pass 11714).

**Qutrit plane:** 14 states.

## The tension

**Flat points break the Standard Model.** A Kempf–Ness flow (|μ| ≤ 10⁻¹¹) reaches flat points in both planes. In every
trial the unbroken group is small:

| plane | unbroken dimension at a flat point (of 16) |
|---|---|
| family | 2 |
| qutrit | 4 |

**SU(3)×SU(2) is always broken.**

**What this means.** In the flagship, the Siegel-type flat direction is carried by Standard-Model-charged fields. A
Standard-Model vacuum must sit at its origin. The vacuum-selection mechanism of Passes 11884–11895 needs nonzero flat
vevs, so it cannot act in the visible untwisted sector without breaking the Standard Model.

**Combined with the earlier passes:**

| sector | flat Siegel modulus | one-loop vacuum | Standard Model |
|---|---|---|---|
| ℤ₃ heterotic (11893) | yes (4-dim) | trinification | no (wrong 27) |
| ℤ₆ local, no Wilson line (11894–11895) | yes (4-dim) | SU(3)_diag×SU(2)×U(1) | no (sextets, octets, no leptons) |
| ℤ₆ flagship with CZ₃ (this pass) | carried by SM-charged fields | must sit at the origin | group yes, near-family matter |

**Within the visible untwisted sector, the modulus and the Standard Model exclude each other.** Where the modulus is
free, the matter is wrong. Where the matter is close to right, the modulus is frozen.

## The way out this points to

The modulus has to live where the Standard Model doesn't see it.
* **The hidden E₈.** In T⁶/ℤ₃ the second E₈ has untwisted matter 3(1,14) + 3(1,64) (Pass 11714). A W(3,3)-type hidden
  sector would carry the Siegel modulus as a hidden Higgs: its vacuum selection, cusp displacement δ and CP phase would
  then be communicated to the visible sector only through moduli-dependent couplings, the theta-function Yukawas of
  11869–11876.
* **The twisted sectors.**

The next computation is the hidden-sector version.

## Scope

* Untwisted sector only.
* σ′ is one representative of the flagship's relative position, chosen to match multiplicities (3,2,1,1,1,1).
* Flat points are generic; special flat points with larger stabilisers are not excluded, but none was found in three
  random flows per plane.
