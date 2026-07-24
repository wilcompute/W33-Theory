# Passes 656–660 — Ext quiver, torsor cocycle, Fisher-optimal optics, drifting propensities, and continuous control

## Pass 656 — Two-character Ext/Kuranishi theorem

For the completed commutant order

\[
R=\mathbf Z_2[S]/(S(S-4)),
\]

let \(M_0\) and \(M_4\) be the two rank-one character lattices. Their periodic matrix-factorization resolutions give

\[
\operatorname{Ext}^1(M_0,M_4)=\operatorname{Ext}^1(M_4,M_0)=\mathbf Z/4,
\]

with vanishing self-\(\operatorname{Ext}^1\), while

\[
\operatorname{Ext}^2(M_0,M_0)=\operatorname{Ext}^2(M_4,M_4)=\mathbf Z/4
\]

and the cross-\(\operatorname{Ext}^2\) groups vanish. For \(M=M_0\oplus M_4\), the quadratic Yoneda obstruction is

\[
(x,y)\longmapsto(xy,xy)\pmod4.
\]

Exactly eight of the sixteen first-order pairs satisfy \(xy=0\pmod4\).

## Pass 657 — The genuine \(D_8\) cocycle and minimal marking

The rank defect \(\delta(g)=\dim(V+gV)-7\) is not additive and is therefore not itself a group cocycle. The true descent datum is the nonabelian Čech cocycle of the regular frame torsor,

\[
t_{ij}=g_i^{-1}g_j,
\qquad t_{ij}t_{jk}=t_{ik}.
\]

Because the relation-space stabilizer in \(D_8\) is trivial, descent requires a torsor section. A directed boundary edge has trivial stabilizer and an orbit of size eight. Thus one vertex plus one adjacent direction is the minimal marking: three bits are necessary and sufficient.

## Pass 658 — Fisher-optimal flat-output phase tomography

The arbitrary-phase row representatives recovered by the 256 intensity probes synthesize

\[
x_{\rm flat}=U_{\rm rep}^{\dagger}\frac{(1,\ldots,1)^T}{4}.
\]

If \(U=D U_{\rm rep}\), then

\[
Ux_{\rm flat}=D\frac{(1,\ldots,1)^T}{4},
\]

so every output amplitude is exactly \(1/4\), independently of the unknown output phases. All 15 reference pairs have unit ideal visibility. The existing 30 two-quadrature phase settings remain sufficient, keeping the complete protocol at

\[
256+30=286
\]

configurations. Uniform phase-shot allocation is minimax and the 15-edge star is A-optimal among minimal trees. At visibility floor \(0.99\), the worst Cramér–Rao coefficient improves by more than 56% relative to the previous generic probe.

## Pass 659 — Unknown and drifting pair propensities

Each science block is preceded by an independent calibration stream that estimates all first- and pair-inclusion propensities. Simultaneous Hoeffding intervals are frozen before the block, making the weights predictable. Calibration uncertainty and a multiplicative MNAR envelope \(e^{\gamma}\) propagate into an explicit matrix penalty.

In the deterministic drift replay, all true propensities remain inside the simultaneous intervals, dynamic weighting reduces covariance error to about 12% of the frozen-propensity error, the covariance change is detected in the first changed block, and the final PSD upper model yields a valid whitener.

## Pass 660 — Exact continuous minimax polyhedral complex

Let \(c_1\) and \(c_2\) be the two tagged-trace costs. The unique unordered two-action controller is optimal precisely on

\[
\boxed{c_1<12,\quad c_2<15,\quad(c_1<5\ \text{or}\ c_2<8)}
\]

for nonnegative costs. This is an L-shaped open polyhedral complex, not one convex box. Its two cells are

\[
0\le c_1<5,\ 0\le c_2<15
\]

and

\[
5\le c_1<12,\ 0\le c_2<8.
\]

The minimax value inside is \(c_1+c_2\). Omission policies certify the walls \(c_1=12\) and \(c_2=15\); a guard-first tree of value at most \(\max(c_2+5,c_1+8,4)\) certifies the northeast exclusion. At the nominal point \((5,7)\), the exact robustness radius is one block.

## Verification and boundaries

All five scripts generate deterministic JSON ledgers, support `--check`, compile, and are exercised by the focused regression.

- Pass 656 closes the full two-character block, not every higher-rank integral \(\mathbf Z_2[S_8]\)-lattice.
- Pass 657 distinguishes the genuine torsor cocycle from the nonadditive rank defect.
- Pass 658 assumes independent detected photons and a calibrated visibility floor.
- Pass 659 is block-predictable and requires the declared calibration/MNAR envelope.
- Pass 660 varies only the two tagged-action costs while fixing the remaining finite game model.
