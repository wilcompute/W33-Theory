# A sixth W33 front: an exactly soluble quantum prepare-and-measure channel

**Date:** 2026-11-02. **Status:** exact abstract finite-dimensional quantum instrument analysis, not a hardware implementation.  
**Producer:** `analysis/w33_20261102_frame_prepare_measure_channel.py`.  
**Certificate:** `data/w33_20261102_frame_prepare_measure_channel.json`.

The prior round established the 216-unit-vector rank-one POVM in a 24-dimensional eigenspace of the W33 route frame. Prepare one of its 216 pure states `|u_s><u_s|`, then measure using effects `E_t=(1/9)|u_t><u_t|`. The outcome probability is

\[
P(t\mid s)=\operatorname{tr}(E_t |u_s\rangle\langle u_s|)
=\frac{(Z_t\cdot Z_s)^2}{14400}.
\]

The `216×216` transition matrix is **strictly positive, symmetric, and doubly stochastic**. Each row, for a fixed prepared state, has the exact probability distribution

| Number of output labels | Probability for each output |
|---:|---:|
| 1 (itself) | `1/9` |
| 20 | `4/225` |
| 95 | `1/225` |
| 100 | `1/900` |

The row sums exactly to one. In particular, even in a perfect implementation the outcome identifying the prepared state occurs with probability only `1/9`, so this is **not** deterministic single-shot discrimination of 216 distinct nonorthogonal states.

The prior CRT spectrum of the integer numerator immediately gives the **exact** stochastic spectrum:

\[
\operatorname{spec}(P)=
1^1,\quad (11/50)^{24},\quad(4/25)^{80},
\quad(4/75)^{81},\quad(1/25)^{15},\quad0^{15}.
\]

Therefore its spectral gap is `39/50` and there is a 15-dimensional blind sector. If this conditional channel is applied as a classical Markov kernel repeatedly, the worst-case total variation from the uniform stationary distribution obeys

\[
\|P^k(s,\cdot)-\pi\|_{TV}
\le \tfrac12\sqrt{215}\,(11/50)^k.
\]

**Five steps suffice for a conservative bound below 1%.** This is a bound on the classical Markov chain of repeated outcome-conditioning/prepare-measure, *not* a thermalization time, coherent quantum mixing rate, or evidence for a physical universal clock.

## Physical hardware and dimensional firewall

An abstract measurement on `C^24` is not directly a measurement on the paper's single-photon time-bin×frequency-bin register `C^9`. An isometric encoding into at least 24 orthogonal accessible modes is needed. Three qutrits have dimension 27, so a 24-dimensional logical subspace can fit inside them; to resolve 216 distinct computational-basis outcomes, at least five ternary digits (243 basis states) are needed. A `216×24` Naimark isometry exists exactly by the frame identity, and it can be completed to a unitary in a 243-dimensional Hilbert space after choosing 27 unused outcome modes; **no local or efficient photonic decomposition is established here**. The optical resource count and implementability must be compiled and independently measured.

The established metaplectic-anyon reference, Cui and Wang, *Universal quantum computation with metaplectic anyons* (J. Math. Phys. 56, 2015, doi:10.1063/1.4914941), requires measurements in addition to finite-image braiding for universality. The present finite-image channel alone does not imply universality.

The test `tests/test_w33_20261102_frame_prepare_measure_channel.py` regenerates all 216 labels and verifies the positivity, exact row populations, previously CRT-certified eigenvalues, spectral gap and five-step convergence bound.

**Novel emphasis relative to the existing repository:** this is the input-output channel induced *operationally* by the earlier minimum-route frame, not a new discovery of its 216 objects, 36 simplices, or Hesse/anyon symmetries.
