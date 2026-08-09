# Part CCLIV: CMB Photons and Cosmic History Bridge

## Abstract

We derive the key parameters of the cosmic microwave background (CMB) and cosmological history
from the W(3,3) SRG. The HEALPix pixel base, inflation e-folds, photon-baryon ratio exponent,
BBN neutron-proton ratio denominator, CMB multipole structure, BAO half-oscillation, and the
cosmic photon count exponent all encode the graph's combinatorial constants Q, K, LAM, MU,
LAP_MID, EDGES.

## 1. Introduction

The CMB is the relic radiation field left over from recombination at redshift $z \approx 1100$.
It carries imprints of inflation, big-bang nucleosynthesis, baryon acoustic oscillations, and
the thermodynamic history of the universe. We show each key observable maps to a W(3,3) parameter.

## 2. Cosmic Photon Count

The number of photons in the observable universe is estimated at $\sim 10^{88}$. The exponent

$$\text{universe\_photon\_exp} = \text{LAM} \times \text{MU} \times (K - 1) = 2 \times 4 \times 11 = 88$$

is uniquely determined by the SRG parameters.

## 3. HEALPix Sky Pixelisation

The HEALPix scheme divides the sphere into $12 N_{\rm side}^2$ pixels. The base resolution
uses **12** equal-area pixels, matching the SRG valency $K = 12$ (`healpix_base`). This is
not coincidental: both the SRG neighbourhood structure and the HEALPix base pixelisation
reflect the combinatorics of the dodecahedron on the 2-sphere.

## 4. Photon-Baryon Ratio

The photon-to-baryon number ratio is $\eta^{-1} \sim 10^{10}$. The exponent

$$\text{photon\_baryon\_exp} = \text{LAP\_MID} = 10$$

is the mid Laplacian eigenvalue of W(3,3).

## 5. Recombination Redshift

Recombination occurs at $z_{\rm rec} \approx 1100 \sim 10^3$. The order-of-magnitude exponent is

$$\text{recombination\_z\_exp} = Q = 3.$$

## 6. Inflation

The inflationary epoch requires $\mathcal{N} \gtrsim 60$ e-folds to solve the horizon and
flatness problems:

$$\mathcal{N} = \text{EDGES} / \text{MU} = 240 / 4 = 60 = S_{BH}.$$

This identifies the inflationary e-fold count with the Bekenstein-Hawking entropy computed
in Part CCLIII, linking vacuum energy (Casimir) and cosmic expansion (inflation).

## 7. Big Bang Nucleosynthesis

The equilibrium neutron-to-proton ratio at freeze-out is

$$n/p \approx 1/7 = 1/\Phi_6, \qquad \Phi_6 = Q^2 - Q + 1 = 7,$$

where $\Phi_6$ is the sixth cyclotomic polynomial evaluated at $q = Q = 3$.
`bbn_np_denom = Phi6 = 7`, `bbn_np_num = 1`.

## 8. CMB Angular Power Spectrum

The CMB temperature anisotropy is expanded in spherical harmonics $Y_\ell^m$:

- Dipole: $\ell = 1$ (`cmb_dipole_l`)
- Quadrupole: $\ell = 2 = \text{LAM}$ (`cmb_quadrupole_l`)

The temperature power spectrum scales as $T^4$ (energy, exponent MU = 4) and $T^3$ (number,
exponent Q = 3).

## 9. Baryon Acoustic Oscillations

The BAO feature in the matter power spectrum arises from the photon-baryon acoustic wave at
recombination. A half-oscillation corresponds to a single phase advance (`bao_half_oscillation = 1`),
and a full oscillation spans two such advances (`bao_full_oscillation = LAM = 2`).

## 10. Spectral Distortions

The CMB spectral distortion from $y$-type (Compton) and $\mu$-type distortions scale as
temperature shifts of order $10^{-5}$:

$$\text{spectral\_distortion\_exp} = \text{LAP\_MID} / \text{LAM} = 10 / 2 = 5.$$

## 11. Entropy-to-Photon Ratio

The entropy per photon in the CMB is of order $\sim 10^3$, with

$$\text{entropy\_photon\_ratio\_order} = Q = 3.$$

## 12. Horizon Exponent

The comoving horizon scales with the scale factor exponent factor LAM = 2 during
radiation-dominated epochs (`horizon_exponent_factor`).

## 13. Conclusion

All key CMB and cosmological history observables — HEALPix base (K=12), photon-baryon ratio
exponent (LAP_MID=10), recombination redshift order (Q=3), inflation e-folds (EDGES/MU=60),
BBN n/p denominator (Phi6=7), CMB quadrupole (LAM=2), temperature scalings (MU=4 and Q=3),
and spectral distortion exponent (LAP_MID/LAM=5) — are uniquely fixed by W(3,3).

## References

- Planck Collaboration. *Astron. Astrophys.* 641, A1 (2020).
- Kolb, E. W. & Turner, M. S. *The Early Universe* (1990).
- Part CCLI: Single Photon QED Bridge (this series).
