# Passes 671–675 — Actual H1 rigidity, compiled gauge transport, noisy optics, per-shot dropout, and controller atlas

## Pass 671 — The actual 81-dimensional lattice is PSp(4,3)-rigid

The proposed “81-dimensional integral S8 lattice” conflated two different complexes. The S8 complex used in Pass 636 has integral H2 rank 125. The 81-dimensional object is the torsion-free integral H1 lattice of the W33 triangle complex, with natural symmetry PSp(4,3).

A unit-pivot integral reduction gives

\[
\operatorname{rank} Z_1=201,\qquad \operatorname{rank} B_1=120,
\qquad H_1\cong\mathbf Z^{81}.
\]

Six explicit symplectic transvections generate the projective group of order 25,920 and induce integral unimodular 81 by 81 matrices. Their simultaneous mod-two centralizer has dimension one. Since reduction can only enlarge a characteristic-zero centralizer,

\[
\operatorname{End}_{\mathbf Q[PSp(4,3)]}(H_1\otimes\mathbf Q)=\mathbf Q,
\qquad
\operatorname{End}_{\mathbf Z[PSp(4,3)]}(H_1)=\mathbf Z.
\]

The actual H1 representation is therefore Schur-rigid: the non-scalar two-character directions of Pass 656 do not lift to it.

## Pass 672 — Three-bit conductor gauge compiler

The 40,320 ordered Singer frames are represented losslessly as

\[
5,040\text{ canonical unmarked cycles}\times 8\text{ directed-edge gauge states}.
\]

The gauge state is exactly the regular D8 marker of Pass 657. Every compiled state reconstructs its unique S8 transporter and the complete sparse 280 by 7 conductor matrix. Exhaustive verification checks all 40,320 states under each of the seven adjacent transpositions.

Storing one canonical sparse matrix per unmarked frame plus the fixed eight-state gauge program gives a compression factor of

\[
7.998186\ldots,
\]

without falsely claiming descent after the gauge register is discarded.

## Pass 673 — Noisy flat-probe hardware falsifier

The 286-setting tomography protocol was tested under a joint model containing unequal detector efficiencies, insertion loss, Gaussian phase diffusion, multiphoton background, incoherent crosstalk, dead time, and count saturation.

The robust minimax allocation is proportional to inverse pair Fisher weight and exactly equalizes the predicted worst information. In 3,000 deterministic Monte Carlo replays, the optimized allocation improves the worst channel RMSE over uniform allocation and keeps the worst pair’s 95th-percentile absolute phase error at

\[
0.0242616\text{ rad}<0.03\text{ rad}.
\]

No nominal setting saturates. A combined hardware-stress scan passes through multiplier 5.0 and fails at the next tested level, giving an explicit falsification envelope.

## Pass 674 — Per-shot drifting-propensity martingale

Every science shot is preceded by 32 independent pilot gates. A 1,024-shot sliding state estimate supplies predictable simultaneous confidence intervals for all first- and pair-inclusion propensities under a declared bounded-drift law.

A finite-horizon mixture of restarted Hoeffding e-processes detects the covariance change at shot 27,619, a delay of 5,619 shots. Across the replay:

- every post-burn-in true pair propensity lies inside its interval;
- dynamic covariance error is 1.1559% of the frozen-propensity error;
- dynamic error is 12.14% of the previous block update;
- the robust upper model gives whitened maximum eigenvalue 0.41443 and positive selector separation.

## Pass 675 — Exact seven-dimensional controller atlas

The controller is exhaustively classified on the integer box spanning two tagged action costs, science quota, both tagged science yields, outcome-envelope branch overhead, and calibration penalty.

The exact atlas contains

\[
7,776\text{ parameter cells},\qquad 22\text{ optimal-root phases},
\]

with 1,308 cells where the tagged-trace pair is uniquely optimal. No pair cell survives when the two science yields sum below the quota.

Calibration uncertainty is the most sensitive direction, producing 3,498 adjacent-cell phase transitions. At the nominal point, the exact one-axis stability ranges are

\[
c_1=0\ldots11,\quad c_2=0\ldots7,\quad Q=7\ldots10,
\]

trace-one yield at least 6, trace-two yield at least 4, outcome overhead 0 through 3, and calibration penalty exactly zero.

## Verification boundaries

All five scripts generate deterministic JSON ledgers, support `--check`, and are covered by the focused regression.

- Pass 671 proves commutant rigidity, not full group-cohomological Ext vanishing.
- Pass 672 preserves the gauge register; unmarked descent remains impossible.
- Pass 673 uses calibrated visibility/rate envelopes rather than waveform-level detector dynamics.
- Pass 674 assumes independent pilot packets and the declared per-shot drift bound.
- Pass 675 is exact on its integer box and affine robust-cost model, not a continuous seven-dimensional polyhedral decomposition.
