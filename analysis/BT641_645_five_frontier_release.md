# Passes 641–645 — higher 2-adic commutants, conductor torsion, multiplexed guards, unbounded covariance, and minimax control

## Pass 641 — The complete higher 2-adic commutant tower

The Pass-636 mod-four calculation extends to every level. For \(n\ge2\),

\[
R_n=\operatorname{End}_{(\mathbb Z/2^n)[S_8]}(H_2/2^nH_2)
\]

has presentation

\[
\boxed{
R_n=(\mathbb Z/2^n)[S,\eta_n]/
(S^2-4S,S\eta_n,\eta_nS,\eta_n^2,2\eta_n).
}
\]

Its additive group is

\[
(\mathbb Z/2^n)^2\oplus\mathbb Z/2,
\qquad |R_n|=2^{2n+1}.
\]

Consequently

\[
|R_3|=128,
\qquad |R_4|=512.
\]

The order-two class \(\eta_n=2^{n-1}E\) is a finite-level phantom: every proper reduction sends it to zero. Hence it contributes no compatible inverse-limit element, and

\[
\boxed{
\operatorname{End}_{\mathbb Z_2[S_8]}(H_2\widehat\otimes\mathbb Z_2)
=\mathbb Z_2[S]/(S^2-4S).
}
\]

Thus the continuous commutant is free of rank two over \(\mathbb Z_2\), even though every finite level contains one extra order-two endomorphism.

## Pass 642 — An explicit conductor-to-seven-primary torsion isomorphism

The seven arithmetic rectangle relations from Pass 637 are embedded into the 280 Singer-Laplacian coordinates by a displayed frame:

- fields \(2,3,4,6\) map to the base triples
  \((2,5,7),(0,4,5),(1,3,7),(3,4,6)\);
- primes \(2,3,5,7,13\) map to augmentation coordinates \(2,3,4,0,1\).

The four base triples form a \(C_4\) overlap frame: adjacent members intersect in one point and opposite members are disjoint. Each rectangle maps to a four-sparse vector with coefficients \(+1,-1,-1,+1\).

For the Singer augmentation Laplacian \(\Delta\),

\[
\operatorname{rank}_{\mathbb F_7}\Delta=273,
\qquad
\dim\operatorname{coker}(\Delta\bmod7)=7.
\]

Adjoining the seven rectangle representatives raises the rank from \(273\) to \(280\). In left-kernel coordinates, their quotient matrix has determinant

\[
\boxed{6\pmod7},
\]

while the first \(7\)-Bockstein matrix has determinant

\[
\boxed{2\pmod7}.
\]

Both matrices are invertible. Since the complete Smith profile is

\[
\operatorname{coker}(\Delta)_{(7)}\cong(\mathbb Z/7)^7,
\]

the seven framed conductor rectangles are explicit order-seven generators of the entire integral seven-primary cokernel.

This closes the numerical \(7=7\) bridge from Pass 637 as a framed isomorphism. A gauge-free canonical map is not claimed.

## Pass 643 — Multiplexed logical fibre and dark sentinel

The existing depth-three, eight-mode Walsh network can perform both jobs simultaneously when the logical fibre and sentinel occupy orthogonal polarization or time-bin labels.

- The logical label populates detector slots 6 and 7, carrying \(\chi_{xy}\) and the trivial character.
- The sentinel label is injected as a back-propagated Walsh probe that is ideally dark in those same spatial slots.
- A polarization combiner/demultiplexer, or an input switch plus calibrated delay and time-resolved gate, separates the labels.

No new spatial coupler and no additional Walsh depth are required.

The complete enumerated single-fault transfer table gives:

\[
P_{\rm guard}(\text{one phase inversion})=\frac18,
\qquad
P_{\rm guard}(\text{one rail loss})=\frac1{32}.
\]

Both exceed the preregistered threshold \(1/64\). For one-rail phase drift \(\phi\),

\[
\boxed{P_{\rm guard}(\phi)=\frac18\sin^2(\phi/2).}
\]

The same threshold requires polarization mixing below approximately \(7.18^\circ\), or time-bin switch extinction above approximately \(18.06\,\mathrm{dB}\). Twelve individual \(0.05\)-radian coupler-imbalance cases were also enumerated; their leakage remains below the gross-fault threshold and is delegated to covariance monitoring.

## Pass 644 — Unbounded-output matrix e-process

Let the measured detector vector obey a calibrated afterpulse model

\[
x_t=u_t+a x_{t-1},
\]

where the innovations have a predictable conditional sub-exponential radial tail and complete-case observation probability \(q_t\ge q_{\min}\). Recover the innovation, clip predictably,

\[
z_t=\widehat u_t\min\!\left(1,\frac{\tau}{\|\widehat u_t\|}\right),
\]

and form the inverse-propensity PSD outer product

\[
Y_t=\frac{O_t}{q_t}z_tz_t^{\mathsf T}.
\]

The clipping bias is bounded explicitly by

\[
2e^{-\tau/K}(\tau^2+2K\tau+2K^2).
\]

A stitched trace-exponential matrix Bernstein e-process over dyadic windows yields simultaneous covariance enclosures with missingness inflation, clipping bias, and afterpulse-calibration sensitivity. The deterministic unbounded-Laplace replay uses 12,000 shots, 7.375% missing complete cases, and a 0.508% clipping rate. It detects the introduced off-diagonal covariance at shot

\[
\boxed{9692}
\]

using the 8192-shot window. The resulting upper-model whitener satisfies

\[
\lambda_{\max}(W\Sigma W^{\mathsf T})=0.737348694681<1
\]

and preserves minimum squared selector separation

\[
\boxed{0.099704450345}.
\]

## Pass 645 — Exact minimax fault-isolation policy

Twelve preregistered hidden scenarios—seven recoverable or nominal and five structural—define a finite zero-sum diagnostic game. Nature may choose any observation allowed by each scenario’s preregistered envelope. The controller chooses among guard, phase-reference, endpoint-parity, multiplex-sentinel, covariance e-process, held-out \(\operatorname{Tr}(U^3)\), recalibration challenge, and the ordinary science traces.

Backward dynamic programming over uncertainty sets yields an exact minimax policy. Its first action is endpoint parity. Only endpoint parity and held-out \(\operatorname{Tr}(U^3)\) are needed on the optimal tree.

The policy guarantees the correct terminal decision for all twelve adversarial scenarios and achieves

\[
\boxed{\text{worst-case cost }11}
\]

versus

\[
12
\]

for the handcrafted guard-audit-recalibration order. Mean adversarial cost falls from \(11\) to \(9\). The ordinary \(\operatorname{Tr}(U)\) and \(\operatorname{Tr}(U^2)\) science action is formally dominated during fault diagnosis and never appears in the optimal tree.

## Verification and boundaries

The release contains 65 internal assertions. All five scripts generate deterministic JSON ledgers, support `--check`, compile, and are invoked by the focused regression.

The exact boundaries are:

- the higher commutant calculation does not classify all unrelated \(\mathbb Z_2[S_8]\)-lattices;
- the conductor map is framed, not gauge-free;
- the hardware compiler is a transfer-matrix and fault-model result, not a physical measurement;
- the unbounded covariance theorem requires valid tail, missingness, and covariance envelopes;
- minimax optimality applies to the preregistered finite game and must be recomputed when hardware likelihood envelopes change.
