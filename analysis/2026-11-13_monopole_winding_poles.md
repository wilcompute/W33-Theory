# Complex-energy poles of the W33 radial winding sectors

Continuing the outgoing grand-spin-zero matching problem produces a pair of near-threshold poles in each of the quark and lepton-doublet sectors of the real W33 core. The calculation uses the piecewise constant radial generator and the constant vacuum exterior of the real-energy scan. [Real-energy scan](2026-11-13_monopole_winding_threshold.md)

Use time dependence exp(−iEt). The analytically continued right frame consists of the massive decaying branches with rate sqrt(m²−E²), chosen positive at E = 0, and the outward-flux light modes. The left frame uses the regular origin subspace. The square matching determinant vanishes when the two frames intersect. With the fixed basis at the endpoints, the determinant is analytic within the first massive thresholds before normalization. Each positive-diagonal QR step divides its analytic frame by a matrix with positive real determinant. Thus the normalized matching determinant retains the phase winding of the analytic determinant. [Evans function continuation](https://www.aimsciences.org/article/doi/10.3934/dcds.2004.10.857)

For the real core the mass blocks are real. In the left/right doubled basis let C be +1 on the left and −1 on the right. C commutes with the radial flux and preserves the origin condition. The generator satisfies C conjugate(G(E)) C = G(−conjugate(E)). The map sends the continued decaying and outgoing boundary subspaces to the corresponding subspaces at the reflected energy. Each reported positive-real zero has a negative-real partner with the same imaginary part.

| Sector | Positive-real pole on 80 cells | Positive-real pole on 144 cells |
| --- | --- | --- |
| Q/U^c | 0.000781785 − 0.000250302 i | 0.000782931 − 0.000250854 i |
| L | 0.001703943 − 0.000566917 i | 0.001707430 − 0.000568170 i |

The smallest singular values at the computed roots are below 3×10⁻¹⁶ in the numerical frames. Moving the outer cut from 5 to the mesh node near 3 shifts the 80-cell roots by less than 2×10⁻⁶. Local circles of radius 10⁻⁴ around the positive-real roots have sampled phase winding +1. The broad circle centered at −0.0025 i with radius 0.003 has sampled winding +2 in both enhanced sectors and zero in the charged-lepton singlet control. The largest sampled phase step on these contours is below 1.40 radians. The contour checks are numerical and leave a continuous nonvanishing bound between samples open.

These poles are for the frozen real monopole with the vacuum exterior attached at finite radius. The scattering residues, infinite-tail corrections, and dynamics of the quantum rotor remain to be computed.

Run `python analysis/toe_20261113_monopole_winding_poles.py` for the [80-cell roots and contours](../data/toe_20261113_monopole_winding_poles.json). Use `--roots-only --count 72 --output data/toe_20261113_monopole_winding_poles_refinement.json` for the [144-cell root control](../data/toe_20261113_monopole_winding_poles_refinement.json).
