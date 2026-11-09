# A calibrated measurement and finite-shot corollary of exact two-qutrit UMUBs

**Date:** 2026-11-09. Inputs: exact k=5 and k=8 SOS certificate, analysis/w33_exact_mub_sym2_blocks_20261109.py, now on master. Reproducer: analysis/w33_20261109_umub_operational_margin.py. Result JSON: data/w33_20261109_umub_operational_margin.json. **Not experimental data.**

## Exact uniform-bias witness

For a pure two-qutrit state v, k Pauli MUB contexts produce m=9k outcome probabilities p_j. The existing exact theorem supplies

\[
\sum_{j=1}^{9k}(p_j-1/9)^2 \ge \delta_k,\quad
\delta_5=1/9,\quad\delta_8=4/9.
\]

By comparison of L2 and Linfinity norms, **at least one labelled outcome** must obey

\[
|p_j-1/9|\ge\sqrt{\delta_k/(9k)}.
\]

The exact worst-case thresholds are \(1/(9\sqrt5)\approx0.0496904\) for k=5 and \(1/(9\sqrt2)\approx0.0785674\) for k=8. This follows from the previously certified quartic and is not a new quantum prediction.

## Calibrated imperfect measurement effects

Suppose each physical POVM effect E_j has an independently certified operator-norm discrepancy of at most epsilon from the intended rank-one projector P_j. For any pure v, \(|\langle v|(E_j-P_j)|v\rangle|\le\epsilon\). Consequently, for measured probabilities q_j,

\[
\max_j|q_j-1/9|\ge
\left[\sqrt{\delta_k/(9k)}-\epsilon\right]_+.
\]

The bound is strictly positive for k=5 when epsilon is below \(1/(9\sqrt5)\), and k=8 when epsilon is below \(1/(9\sqrt2)\). This is a **calibration tolerance**, not a stochastic device-independent guarantee or an error-correction threshold.

## Finite-shot observable

Sample each of the k contexts independently N times, with nine outcomes per context. Each outcome count is a Bernoulli sum of N i.i.d. indicators; the within-context counts need not be independent. Hoeffding and a union bound guarantee, with probability at least \(1-\alpha\), that

\[
\max_j|\widehat q_j-1/9|\ge
\left[
\sqrt{\delta_k/(9k)}-\epsilon-
\sqrt{\log(18k/\alpha)/(2N)}
\right]_+.
\]

For a conservative illustration take epsilon=0.01, N=20,000 shots per basis and alpha=0.01. The guaranteed observed deviation is about **0.02460** for k=5 and **0.05310** for k=8, across 100,000 and 160,000 total shots respectively. Actual measurement design, tomography errors, drift, SPAM, detector loss, setting bias and non-i.i.d. effects are not modeled.

**Essential mixed-state no-go:** the completely mixed density operator I/9 produces exactly uniform outcomes in every ideal orthonormal basis. The pure-state witness therefore cannot certify arbitrary mixed states. Nor does it prove quantum advantage, an operational optical gate, the origin of a Hamiltonian, or the theory of everything.

The novelty here is only the practical formal corollary and reproducible conditional number sheet, not the underlying Hoeffding inequality or Pass 12639 strong-unextendibility theorem.
