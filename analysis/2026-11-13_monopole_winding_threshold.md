# Near-threshold response of the W33 winding Weyl channels

The flux-normalized standing solutions on the real W33 core have a sharply energy-dependent quark response. This calculation scans the open light channels while staying below the first exterior massive threshold. It resolves the matching gap, the overlap with incident flux, and the distance to a solution with only decaying massive exterior modes. [Zero-energy profiles](2026-11-13_monopole_winding_radial.md)

Write F for the radial flux matrix and V for the potential. At energy E the radial generator is G(E) = −i F V + i E F. In the constant vacuum exterior, V anticommutes with F. If s is a unit eigenvector of G(0) of eigenvalue −m, its continuation into the decaying subspace below threshold is

    s(E) = s − i E F s / (m + sqrt(m² − E²)).

The light eigenvectors retain their unit flux. QR transport brings the regular origin frame and exterior frame to the same radius. The square matching matrix combines the regular frame with the outgoing and decaying frames. Projecting the incident forcing onto the left singular vectors gives the coefficient of each response direction after division by its singular value. Separately, the largest overlap between the regular frame and the decaying-only frame determines the smallest principal angle to a localized zero-flux solution. These are finite-cut diagnostics with a specified matching radius. A resonance pole requires continuation of the outgoing problem into complex energy. [Evans function and resonance continuation](https://www.aimsciences.org/article/doi/10.3934/dcds.2004.10.857)

At matching radius 0.14, the quark norm drops from 47.169 at zero to 22.964 at |E| = 0.002 and 7.772 at |E| = 0.005. The lepton-doublet norm grows from 40.991 at zero to 74.669 at |E| = 0.002, then falls to 25.089 at |E| = 0.005. These are sampled values, with no interpolation claim about the peak location. The singlet charged-lepton norm stays near 1.279 over the entire scan. At zero the decaying-only principal-angle sines are 0.01041, 0.001637, and 0.9016 for the quark, lepton-doublet, and singlet charged-lepton sectors, respectively. The first two sectors therefore approach a decaying-only match but retain a positive numerical gap. The three weakest directions account for norms 47.143 and 39.561 in the quark and lepton-doublet solutions at zero. For the quark sector the norm of the corresponding incident projections changes by only 0.21% between zero and 0.005, while the matching gap increases by more than sixfold. The amplification is tied to the small denominators.

At zero energy, moving the cut from 5 to about 2.05 changes the quark norm from 47.169 to 47.243 and the lepton-doublet norm from 40.991 to 41.029. This is a real-axis robustness check for the sampled finite-cut model.

The exterior is set to the constant vacuum at the selected cut. Moving that cut tests sensitivity to discarding the tabulated tail. The scan uses the phase-zero real core, with the regular subspace imposed at radius 10⁻⁶. It does not determine a physical rotor resonance or a compact winding rate.

Run `python analysis/toe_20261113_monopole_winding_threshold.py` to regenerate the [energy and cut scan](../data/toe_20261113_monopole_winding_threshold.json).
