# Passes 3003–3011 — symmetry-reduced M36, 28-check D4 localization, typed golden control, and two outside-box closures

## Evidence ladder

- **Exact finite mathematics:** Passes 3003, 3004, 3006, 3008, and 3009.
- **Exact source model and synthesizable RTL:** Pass 3005. Local Python exhausts the finite model; Icarus/Yosys evidence remains a workflow gate.
- **Exact Bayesian stopping for a stated component channel:** Pass 3007. The frozen counts are synthetic and are not device measurements.
- **Still pending:** the complete 213,648,435-subspace M36 sweep, a proof that 28 is the minimum two-edge schedule, observed RTL synthesis/timing, and physical receiver calibration.

## Pass 3003 — the M36 pilot collapses to one symmetry mechanism

The projective two-qubit Clifford group has order 11,520. The deep M36 ray has orbit 640 and stabilizer 18. Therefore the natural three-copy symmetry is

\[
\operatorname{Stab}(m)^3\rtimes S_3,
\qquad |G_m|=18^3\cdot6=34,992.
\]

The six non-CSS, success-\(1/27\), stabilizer-output projectors found by the 649,940-subspace general-isotropic pilot are all in one orbit of size 729. Their orbit stabilizer has order 48. They are one false-lead mechanism, not six independent protocols.

Copy permutations also reduce the 495 RREF pivot patterns to 98 exact types: 31 orbits of size three and 67 of size six. The full 213,648,435-subspace sweep remains pending; every future hit can now be canonicalized by the 34,992-element symmetry before physical analysis.

## Pass 3004 — 28 triangles replace 29

A new 28-triangle schedule separates the complete set of 48,826 hypotheses consisting of no fault, one nonidentity \(D_4\) edge fault, or two nonidentity \(D_4\) edge faults. The full group-valued syndrome is injective. Its central \(r^2\) restriction separately proves that all edge supports of weight at most two are distinct.

The prior 29-triangle construction is therefore not optimal. A deterministic search found no 27-triangle witness, but this is not an impossibility proof; the exact minimum remains in \([23,28]\).

## Pass 3005 — typed \(A_4\) shell and protected \(D_4\) core

The four binary syndrome labels form \(V_4\). The Fibonacci quotient modulo two,

\[
F(x,y)=(y,x+y),\qquad F^3=I,
\]

acts cyclically on the three nonzero labels, giving

\[
V_4\rtimes\langle F\rangle\cong A_4.
\]

The RTL stores the affine shell element \((v,k)\), but the \(D_4\) route registers are in a separate write block. Shell opcodes have no syntactic write path into the core; core opcodes require an explicit authorization bit. This implements the previously proved order-three lift obstruction as a hardware type boundary.

A finite machine cannot generate an irrational Sturmian word forever. The hardware therefore uses the honest Christoffel approximant \(89/233\): exactly 89 expensive events per 233 ticks, no adjacent expensive events, and prefix discrepancy below one.

## Pass 3006 — the 540 correspondence is objectwise real but dynamically false

Every unordered skew pair of isotropic lines lies in exactly three symplectic spreads and has exactly four isotropic transversal lines. Hence every one of the 540 skew pairs carries the natural 12-set

\[
\{(\text{containing spread},\text{isotropic transversal})\},
\]

and the total flag count is

\[
540\cdot3\cdot4=6,480.
\]

\(PSp(4,3)\) is transitive on these 6,480 flags. A skew-pair stabilizer has order 48 and induces an order-24 local action whose projections are full \(S_3\) on the three spreads and full \(S_4\) on the four transversals.

The stronger clock identification fails. \(PGSp(4,3)\) has two order-12 conjugacy classes, each of size 4,320. Their flag cycle profiles are

\[
6^{48}12^{516},\qquad 6^4 12^{538}.
\]

No projective automorphism acts as \(12^{540}\). Thus the 12-object geometric bundle is exact, but the semiregular 540-cycle clock is genuinely affine/controller-added.

## Pass 3007 — component-resolved sequential chirality stopping

The receiver accepts one coherent count record: launched photons, survived photons, OAM-correct survivors, slot-correct OAM events, dark trials, and dark clicks. It converts these to a three-outcome channel—detector 0, detector 1, or erasure/multiclick—and performs Bayesian updating after each prior-conditioned single-copy Helstrom measurement.

At each posterior it compares immediate decision error with copy cost plus expected continuation risk. For the repository's synthetic component stack and horizon 12:

| copy cost | modeled success | expected copies |
|---:|---:|---:|
| 0 | 0.997182 | 11.569 |
| \(10^{-4}\) | 0.997139 | 9.301 |
| \(10^{-3}\) | 0.996589 | 7.710 |
| \(5\times10^{-3}\) | 0.988309 | 4.911 |
| \(10^{-2}\) | 0.987369 | 4.781 |

Adaptive individual measurements attaining the collective bound for ideal binary pure states are prior art (Acín et al., arXiv:quant-ph/0410097). The new repository contribution is the component-channel stopping compiler and its explicit claim boundary.

## Pass 3008 — outside-box tetrahedral syndrome measurement

The four \(V_4\) labels are assigned to tetrahedral Bloch vectors. Their orientation-preserving symmetry group is exactly \(A_4\), so the same group controls both the classical shell and a covariant four-outcome qubit measurement.

For visibility \(\eta\),

\[
E_i=\frac14(I+n_i\cdot\sigma),\qquad
\rho_j=\frac12(I+\eta n_j\cdot\sigma),
\]

and

\[
p(i\mid j)=\frac14(1+\eta n_i\cdot n_j).
\]

At perfect visibility the single-copy success is \(1/2\), rising to approximately 0.8510 after 12 independent copies with maximum-likelihood decoding. This is a compact syndrome-shell readout proposal, not a compression of the nonabelian core. Qubit tetrahedral SIC measurements are established prior art; see Renes et al., arXiv:quant-ph/0310075.

## Pass 3009 — outside-box reversible cut-and-project calendar

Cross the 233-slot Christoffel scheduler with the 12-phase curvature clock. Since \(\gcd(233,12)=1\), the superperiod is

\[
233\cdot12=2,796.
\]

It contains 1,068 expensive events and gives each clock phase exactly 89. Global inter-event gaps are only two or three ticks; each fixed phase sees gaps 24, 36, or 60. Reversing the 233-slot word gives the same cyclic word shifted by 89 positions, so time reversal requires only an origin relabeling.

Christoffel-word reversal lying in the same conjugacy class is classical; the new result is the exact D12 phase-balanced calibration calendar.

## System decision

```text
D4 ROUTE CORE
  protected nonabelian holonomy
  28-triangle two-fault diagnostic

A4 SYNDROME SHELL
  four parity labels plus order-three Fibonacci action
  optional tetrahedral covariant readout

TIME / CALIBRATION
  D12 logical phase clock
  89/233 Christoffel event calendar

RESOURCE RECEIVER
  component-resolved posterior
  adaptive measurement and optimal stopping

M36 SEARCH
  34,992-element canonicalizer
  98 copy-permutation pivot types
  full exhaustive sweep still separately gated
```
