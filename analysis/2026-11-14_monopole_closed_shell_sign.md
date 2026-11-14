# Massive-channel sign test for the W33 monopole shell

The projected monopole calculation keeps the light channels outside radius 36. The [earlier closed-channel comparison](2026-11-13_monopole_closed_feedback.md) restored the massive channels through radius 72 and found a small net effect. A small net effect can arise from cancellation between different processes. The new comparison keeps all 98 radial Weyl components, changes the exterior shell blocks independently and propagates the regular core subspace to the fixed shell interface. The total energy is 0.002.

Let P project to the eight vacuum open channels and Q to the massive channels. Decompose the shell generator into its P and Q diagonal blocks and off-diagonal mixing. In the same core and with the same boundary frames, compute conversion with the mixing multiplied by +1, -1 and 0. Denote the probabilities by p+, p- and p0. Also compute p_ref with zero mixing and the vacuum massive block. The exact algebraic decomposition is

    p+ - p_ref = (p0 - p_ref) + (p+ - p-)/2 + ((p+ + p-)/2 - p0).

The three terms isolate the closed diagonal change at zero mixing, the sign-odd change, and the sign-even change at fixed diagonal blocks. The same decomposition applies to the complex reflection matrix before taking norms. All four branches obey the same flux-conservation equation. [Feshbach projection onto open and closed channels](https://doi.org/10.1016/0003-4916%2858%2990007-1)

There is a direct test for core dependence of the odd effect. Conjugation by P-Q flips the sign of mixing in the shell and preserves both vacuum boundary spaces and the light incident and outgoing frames. Moving the conjugation through the shell gives the positive-mixing problem with its inner regular subspace conjugated by P-Q. If the inner regular subspace were invariant, the reflection would be exactly even in the shell mixing. A nonzero odd part witnesses sensitivity to the core's open-closed coupling. The even part includes all even powers of the shell mixing and can include return through the core. This finite sign comparison does not assign either part to a single perturbation order.

The backward QR matching only reconstructs the light quotient from its triangular factors. The calculation independently checks the complete reflection matrix at the shortest shell against the existing full native matcher. It also compares the vacuum-closed branch against the projected eight-channel propagation on every shell. These controls use the same piecewise-constant Hamiltonian. Mesh refinement tests sampling sensitivity. The result is a finite-shell diagnostic for the fitted Robin background and its supplied quadratic scattering model.

Replay with py -3 analysis/toe_20261114_monopole_closed_shell_sign.py. Use --cells 64 and an alternate --output path for the finer replay.

## Results

| Outer radius | Full minus projected | Closed diagonal | Sign odd | Sign even |
| --- | ---: | ---: | ---: | ---: |
| 72 | 2.140e-7 | 3.668e-11 | 4.458e-9 | 2.095e-7 |
| 144 | 2.206e-7 | 3.647e-11 | 4.415e-9 | 2.162e-7 |
| 288 | 2.209e-7 | 3.651e-11 | 4.426e-9 | 2.165e-7 |

At radius 288, about 98% of the correction is even in the coupling. All three contributions have the same sign. Doubling the shell resolution changes the net correction there by about 1.0e-10. The 32-cell run replayed on TheHeavyCrown. Both resolutions passed the native full-matcher and projected-matcher comparisons. Infinite-radius full scattering and sensitivity across resonance energies require separate checks.
