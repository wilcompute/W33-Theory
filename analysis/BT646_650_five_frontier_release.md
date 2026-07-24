# Passes 646–650 — derived 2-adic deformation, conductor descent, dual-label optics, partial-channel covariance, and joint control

## Pass 646 — Continuous commutant deformation and the phantom correction

The continuous endomorphism deformation order of the fixed integral Johnson-clique homology lattice is

\[
\boxed{R=\mathbb Z_2[S]/(S^2-4S).}
\]

Its residual dual-number tangent space has dimension one over \(\mathbb F_2\). The two characteristic-zero characters \(S=0\) and \(S=4\) coincide modulo two. The nonzero scalar tangent represented by \(S=2\pmod4\) has no lift modulo eight, giving an explicit first obstruction.

The finite extra classes from Pass 641 form the zero-transition inverse system \(P_n\cong\mathbb Z/2\). For this system the standard \(\varprojlim^1\) operator \(1-T\) is the identity. Consequently

\[
\boxed{\varprojlim P_n=0,\qquad \varprojlim{}^1P_n=0.}
\]

Thus the exotic finite-level class is not a hidden derived-limit deformation. It is a genuine finite-level phantom.

## Pass 647 — Gauge removal by an ordered-frame torsor

There are exactly \(40320\) ordered four-tuples of triples in \(J(8,3)\) having the required \(C_4\) overlap pattern. The \(S_8\) action is simply transitive: every ordered frame has a unique transporter from the Pass-642 base frame, and the ordered-frame stabilizer is trivial.

Forgetting the arithmetic ordering leaves \(5040\) unmarked cycle frames, each with stabilizer \(D_8\) of order eight. Every nonidentity \(D_8\) re-marking enlarges the seven-dimensional arithmetic relation span to dimension 8, 9, or 10. Therefore the conductor map does not descend—even projectively—to an unmarked frame.

Naive \(S_8\) averaging also fails: it annihilates the map because each fibre-coordinate coefficient sum is zero and \(S_8\) is transitive on triples. The canonical object is the \(S_8\)-equivariant family over the simply transitive ordered-frame torsor.

## Pass 648 — Component-level dual-label optical prototype

The polarization/time-bin compiler is promoted to a full 16-mode transfer model,

\[
8\text{ spatial modes}\times2\text{ orthogonal labels}.
\]

The logical label carries \(\mathbf1\oplus\chi_{xy}\) in spatial outputs 7 and 6, while the orthogonal label carries the dark sentinel. The spatial network remains the existing depth-three Walsh interferometer:

\[
\boxed{12\text{ couplers},\quad\text{depth }3,\quad0\text{ added spatial couplers}.}
\]

A complete coherent tomography frame uses \(16+120+120=256\) settings: basis states, real pair superpositions, and quadrature pair superpositions. Its Hermitian design matrix has exact rank 256.

Under total optical insertion loss \(1.2\,\mathrm{dB}\), detector efficiency \(0.8\), and dark probability \(10^{-6}\) per gate, exact Poisson tail searches give 122 input photons for a one-rail phase inversion and 487 for complete rail loss, with false alarm at most \(10^{-6}\) and miss probability at most \(10^{-3}\). The full calibration frame uses 124,672 input photons at the rail-loss design level.

## Pass 649 — Partial-channel matrix e-process

Complete-case deletion is no longer necessary. For predictable independent channel indicators \(O_i\) with probabilities \(p_i\), define

\[
w_i=\frac{O_i z_i}{p_i}
\]

and

\[
\boxed{Y=ww^T-\operatorname{diag}\!\left(\frac{O_i z_i^2(1-p_i)}{p_i^2}\right).}
\]

Conditionally on the clipped innovation \(z\), \(\mathbb E[Y\mid z]=zz^T\). A stitched self-adjoint matrix Bernstein e-process supplies simultaneous dyadic-window covariance enclosures, and PSD projection plus the confidence radius gives an upper model suitable for whitening.

In the deterministic 120,000-shot replay, only 71.9% of shots are complete. The covariance change begins at shot 20,000 and is first detected at shot 23,328. The final upper whitener satisfies \(\lambda_{\max}(W\Sigma W^T)=0.989142568<1\), while minimum robust selector separation remains positive.

## Pass 650 — Joint science-and-diagnosis minimax controller

Every continue branch must accumulate ten science units. Ordinary \(\operatorname{Tr}(U)\) and \(\operatorname{Tr}(U^2)\) blocks remain diagnostically ambiguous under the old envelopes. Two co-designed actions add simultaneous telemetry:

1. guard-tagged \(\operatorname{Tr}(U)\), cost 5 and science gain 6;
2. covariance-tagged \(\operatorname{Tr}(U^2)\), cost 7 and science gain 4.

Exact backward dynamic programming chooses precisely those two actions. The policy guarantees the right decision for all twelve preregistered adversarial scenarios, completes the science quota on all seven recoverable branches, and halts all five structural branches.

The worst-case cost is \(12\), versus \(20\) for minimax diagnosis followed by separate science acquisition. This saves eight blocks, a 40% reduction. Uniform-scenario mean cost falls from 14.25 to 10.25.

## Verification and boundaries

The release contains 79 internal assertions. All five scripts generate deterministic JSON ledgers, support `--check`, compile, and are invoked by the focused regression.

- Pass 646 treats deformations represented inside the fixed continuous commutant order, not all module deformations between arbitrary lattices.
- Pass 647 proves ordered-frame torsor descent and the obstruction to stronger unmarked descent.
- Pass 648 is an engineering design calculation with explicit assumed component specifications, not measured prototype data.
- Pass 649 requires valid conditional dropout, tail, variance, and afterpulse-calibration envelopes.
- Pass 650 is minimax-optimal only for the declared scenario envelopes, science weights, and action costs.
