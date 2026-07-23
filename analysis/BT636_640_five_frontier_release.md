# Passes 636–640 — mod-4 lifting, conductor relations, endpoint parity, covariance confidence sequences, and closed-loop falsification

## Pass 636 — Complete mod-4 commutant and first Bockstein obstruction

An explicit integral basis for

\[
H_2(\operatorname{Cl}(J(8,3));\mathbb Z)\cong\mathbb Z^{125}
\]

is reconstructed from the elementary-collapse certificate. The seven adjacent transpositions act by exact integral matrices satisfying the Coxeter relations. If \(S\) denotes the sum of all 28 transpositions, then

\[
S^2=4S,\qquad \operatorname{tr}S=140,\qquad \operatorname{tr}S^2=560.
\]

The multiplicity-free rational decomposition and the primitive off-diagonal entries of \(S\) give

\[
\boxed{\operatorname{End}_{\mathbb Z[S_8]}(H_2)=\mathbb Z[I,S].}
\]

Modulo two the commutant enlarges to the three-dimensional local algebra from Pass 631. The exotic rank-34 radical direction has nonzero Bockstein obstruction, detected separately by all seven adjacent transpositions. Hence the reduction image of the mod-4 commutant is exactly \(\langle I,\bar S\rangle_{\mathbb F_2}\). Every liftable reduction has \(2^3\) homogeneous lifts, so the complete mod-4 ring has 32 elements and presentation

\[
\boxed{(\mathbb Z/4)[\epsilon,\eta]/(\epsilon^2,\epsilon\eta,\eta\epsilon,\eta^2,2\eta),}
\]

where \(\epsilon=S\bmod4\) and \(\eta=2E\) for an exotic mod-two endomorphism \(E\). This closes the first mod-4 lifting problem; higher 2-adic Ext remains open.

## Pass 637 — Local-field conductor graph

The 17 arithmetic fields and five torsion primes define 85 localization nodes. Joining nodes that share a field or a prime gives the rook graph

\[
R(17,5)=K_{17}\square K_5,
\]

with adjacency spectrum

\[
20^1,\quad15^4,\quad3^{16},\quad(-2)^{64}
\]

and Laplacian spectrum

\[
0^1,\quad5^4,\quad17^{16},\quad22^{64}.
\]

These coarse eigenspace multiplicities do not recover the modular simple dimensions \(6,8,14,40\).

Enriching every localization by field, prime, ramification kind, index defect, ramification flag, all \(e\), all \(f\), and every \((e,f)\) pair with multiplicity produces an integral incidence matrix of size \(85\times187\), exact rank 78, and nullity 7. A primitive kernel basis consists entirely of alternating boundaries of \(2\times2\) field-prime rectangles supported on quartic fields 2, 3, 4, and 6. The seven relation-intersection graph has 17 edges, degree sequence \(4,4,6,6,4,4,6\), and characteristic polynomial

\[
(x-5)(x-1)(x+1)^4(x+2).
\]

Two exact count bridges are recorded but not promoted to canonical identifications:

\[
7=v_7(\det\Delta),\qquad 78=2(24+15),
\]

the latter being the total nontrivial Ihara pole order.

## Pass 638 — Minimal endpoint-parity optical fibre

The minimal Wilson fibre \(\mathbf1\oplus\chi_{xy}\) has an optimal two-rail realization: both endpoint generators act by the same rail swap \(X\), and one balanced coupler diagonalizes the representation into trivial and \(\chi_{xy}\) outputs. This uses two modes, one coupler, and depth one, all minimal.

A faithful endpoint-resolved realization uses four modes indexed by \(\mathbb F_2^2\). The network \(H_2\otimes H_2\) realizes all four characters of \(C_2\times C_2\) using four balanced couplers and depth two, again optimal. Every single phase inversion sends guard power \(1/2\); every single rail loss sends guard power \(1/8\).

The existing order-eight Walsh guard modes already restrict to the required fibre. Choosing endpoint translations \(x=010\) and \(y=101\), output mode 6 (Walsh character 110) is \(\chi_{xy}\), while output mode 7 (character 101) is trivial. No extra spatial couplers or Walsh depth are required.

There is an exact same-shot no-go: a scalar mode cannot simultaneously be dark as a leakage sentinel and populated as a logical fibre. Reusing the guard pair while preserving sentinel semantics therefore requires time-bin, polarization, or another orthogonal multiplexing label.

## Pass 639 — Matrix covariance confidence sequence

For adapted optical residuals \(z_t\) satisfying \(\|z_t\|_2\le1\), set \(Y_t=z_tz_t^{\mathsf T}\). Matrix-Bernstein confidence sequences are stitched over all times and dyadic windows

\[
8,16,32,64,128,256,512,1024
\]

using

\[
\alpha_{t,w}=\frac{6\alpha}{\pi^2t^2|\mathcal W|},\qquad \alpha=0.002.
\]

With \(L=\log(2d/\alpha_{t,w})\), the spectral radius is

\[
r_{t,w}=\frac{2L/3+\sqrt{(2L/3)^2+2wL}}{2w}.
\]

If \(\|\Sigma_t-\Sigma_{t-1}\|_{\mathrm{op}}\le\delta\), adding \(\delta(w-1)/2\) converts the average-covariance enclosure into a current-covariance enclosure. All windows are simultaneous, so adaptive window selection is valid.

In the deterministic nonstationary replay, off-diagonal leakage is first excluded from zero at shot 1618 using the 512-shot window. The upper-model whitener

\[
W=(\widehat\Sigma+\rho I)^{-1/2}
\]

satisfies \(W\Sigma_tW^{\mathsf T}\preceq I\) on the confidence event and preserves minimum robust squared selector separation

\[
\boxed{2.2719710121733003}.
\]

The theorem is distribution-free for bounded adapted residuals; unbounded detector outputs require clipping or a sub-exponential matrix process.

## Pass 640 — Closed-loop anytime falsification controller

The controller has states NOMINAL, AUDIT, RECALIBRATE, and SAFE_HALT. The global error ledger is

\[
0.002\;\text{(covariance CS)}+0.007\;\text{(adaptive e-process mixture)}+0.001\;\text{(recalibration confidence)}=0.01.
\]

Operational CUSUMs alter acquisition but never reject. Rejection evidence is carried only by a weighted mixture of predictably selected e-process epochs; epoch \(k\) has weight \(2^{-(k+1)}\), with unused tail mass held at the constant e-value one.

The nominal schedule uses thirteen \(\operatorname{Tr}(U)\) shots per \(\operatorname{Tr}(U^2)\) shot. AUDIT activates the held-out \(\operatorname{Tr}(U^3)\) channel. RECALIBRATE cycles through the two guard modes, endpoint parity, and phase reference.

In the recoverable replay, a guard warning occurs at shot 401, 64 held-out \(\operatorname{Tr}(U^3)\) samples are collected, recalibration begins at 529, nuisance intervals and endpoint parity are updated at 785, and the controller returns to NOMINAL. In the structural-departure replay, the held-out audit warns at 405 and the global mixture safely halts at shot 413 with e-value above \(1/0.007\).

## Verification boundaries

All five scripts emit deterministic JSON certificates, support `--check`, compile, and are exercised by the focused regression. The release has 82 internal assertions. Open boundaries are stated explicitly: higher 2-adic Ext beyond mod four; functorial conductor maps into Smith or Ihara modules; physical multiplexing hardware characterization; unbounded-output matrix processes; and empirical hardware performance beyond deterministic controller replay.
