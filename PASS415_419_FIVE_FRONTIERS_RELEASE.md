# Passes 415–419 — Frobenius Smith Packets, Protocol-Specific Qutrit Distillation, Optimal Cycle Telemetry, Twirl-Breaking Spectroscopy, and Adversarial Replication

**Status: 85 executable checks pass. No physical experiment is claimed.**

## Pass 415 — Frobenius packets and the prime-power Smith normalization theorem

Let `q=p^f` and let `Gamma_q` be the `q^3`-vertex Heisenberg bulk graph. Nonzero additive central characters fall into cyclotomic packets indexed by

\[
\mathbb F_q^\times/\mathbb F_p^\times,
\]

which is cyclic of order

\[
N=\frac{q-1}{p-1}.
\]

Arithmetic Frobenius acts by

\[
\sigma([a])=[a^p].
\]

Consequently,

\[
|\operatorname{Fix}(\sigma^d)|=\gcd(N,p^d-1),
\]

and the number of exact length-`d` Frobenius orbits is

\[
O_d=\frac1d\sum_{e\mid d}\mu(d/e)\gcd(N,p^e-1).
\]

Choosing an `F_p` basis of `F_q` identifies its additive Fourier matrix with `F_p^{\otimes f}`. The two-coordinate symplectic block is therefore `F_p^{\otimes 2f}`. Over

\[
R=\mathbb Z_p[\zeta_p],\qquad \pi=\zeta_p-1,
\]

its exact normalized `pi`-Smith polynomial is

\[
\boxed{(1+x+\cdots+x^{p-1})^{2f}}.
\]

There are `(q-1)/(p-1)` such projective packets. Converting `R/(pi^s)` to a `Z_p` module and adding the trivial-central sector gives total `p`-adic order

\[
f(q^3+q^2-4).
\]

The matrix-tree theorem gives the integral critical-group order

\[
f(q^3+q^2-5).
\]

Therefore the conductor normalization has exact index

\[
\boxed{p^f=q}.
\]

The theorem freezes the full normalization, Frobenius orbit structure, and conductor index for every odd prime power. It does **not** claim a closed all-`f` formula for the redistribution among individual `p^k` factors after conductor gluing.

Concrete orbit censuses include:

- `q=9`: two fixed packets and one two-cycle;
- `q=25`: two fixed packets and two two-cycles;
- `q=27`: one fixed packet and four three-cycles.

For `q=9`, comparison with the exact Pass-410 Smith form shows that the conductor removes 75 generators, promotes the `q^2-2=79` trivial-sector classes from `3^4` to `3^6`, creates no `3^5` layer, and has index `3^2=9`.

## Pass 416 — the five-qutrit perfect code does not directly distill the new T orbit

The Pass-411 resource is

\[
|M_T\rangle=T F|0\rangle,
\qquad
T=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1}).
\]

Pass 416 constructs the complete `[[5,1,3]]_3` code projector and logical decoder, then searches all 72 distinct Clifford images of `|M_T>` as inputs and all 72 images as output corrections.

Every noiseless orbit input has the same acceptance probability,

\[
P_{\rm acc}=0.039780521262\ldots,
\]

and the same best return fidelity,

\[
F_{\rm return}=0.918222659014\ldots.
\]

Thus even a pure input exits the code projection outside the T Clifford orbit:

\[
\boxed{\text{the five-qutrit perfect-code map is not a direct T-state distiller}.}
\]

For depolarizing inputs

\[
\rho_e=(1-e)|M_T\rangle\!\langle M_T|+eI/3,
\]

both the success probability and corrected target-overlap numerator are frozen as degree-five polynomials. Across the complete `e in [0,1)` numerical certificate grid, the output T-orbit fidelity is strictly below the input fidelity.

This is a protocol-specific no-go. It does not exclude conversion through the known five-qutrit attractors, parity checking, equatorialization, another code, or a non-code-specific protocol. The implementation independently verifies that the qutrit Strange state is a pure fixed point with acceptance probability `1/36`.

## Pass 417 — optimal divisor-cycle hybrid telemetry

Pass 412 proved that the sandpile class uniquely recovers the net divisor through transport weight three, but it cannot see directed cycle flows or hidden source-target pairing.

For 27 modes there are 702 directed non-loop slip types. Conditioned on a recovered net divisor, Pass 417 ranks all slip multisets of size at most three in a canonical lexicographic fibre.

The worst unordered fibre is the zero divisor:

- one empty history;
- 351 reciprocal two-cycles;
- 5,850 directed three-cycles.

Hence

\[
1+351+5850=6202,
\]

so

\[
\boxed{13\text{ bits are necessary and sufficient}}
\]

to recover the complete unordered slip multiset through weight three.

If temporal order must also be preserved, the zero fibre contains

\[
1+702+35100=35803
\]

ordered histories, requiring and attaining

\[
\boxed{16\text{ bits}.}
\]

When cancellations and cycles are excluded and only three-source/three-target pairing remains, the maximum ambiguity is `3!=6`, so three bits suffice.

## Pass 418 — the complete symmetry-breaking calibration space

The real symmetric `27 x 27` calibration space has dimension

\[
\frac{27\cdot28}{2}=378.
\]

The four distance orbits contain

\[
27,\ 108,\ 216,\ 27
\]

orthonormal coordinates corresponding to mode gains, native couplers, distance-two crosstalk, and phase-fibre pairs.

Each orbit splits into one mean plus a centered regular-simplex defect space. Therefore

\[
\boxed{378=4+(26+107+215+26)=4+374.}
\]

The four means are the exact automorphism-twirled invariants. The other 374 coordinates are a complete localized symmetry-breaking atlas.

For an orbit of size `m`, centered single-defect atoms satisfy

\[
\langle r_i,r_j\rangle=\delta_{ij}-\frac1m.
\]

The largest matched-filter coefficient therefore identifies a unique defect exactly, and its amplitude is recovered by multiplying by `m/(m-1)`. Deterministic injections in all four families are recovered exactly.

If fewer than half of an orbit's coordinates are corrupted, median centering removes an unknown common-mode baseline and recovers every noiseless sparse defect. A separate temporal witness distinguishes white sampling noise from a localized `AR(1)` drift after twirl subtraction.

## Pass 419 — adversarial custody and the hardened v2 replication chain

The Pass-414 v1 fixture signs each artifact independently. Those signatures do not bind the study ID, device ID, manifest nonce, sequence, or predecessor. A valid artifact can therefore be replayed into another manifest unless an auditor adds external context checks.

Pass 419 introduces a v2 signature envelope binding:

- study ID and device ID;
- a 128-bit manifest nonce;
- artifact type and sequence;
- signer role and registered public key;
- payload SHA-256;
- predecessor signed-envelope SHA-256;
- signing timestamp.

The independent verifier additionally enforces five distinct role keys, protocol/BOM/calibration cross-hashes, raw-byte hashing, raw-row counts, blind raw and analysis payloads, key-release ordering, audit ordering, and nonclaim flags.

Twelve attacks are constructed and rejected:

1. timestamp substitution;
2. authorized key leakage;
3. cross-study calibration replay;
4. cross-device replay;
5. role-key collision;
6. authorized calibration substitution;
7. unsigned selective row deletion;
8. re-signed row deletion;
9. artifact reordering;
10. early key release;
11. manifest-nonce substitution;
12. nonclaim flag forgery.

Several attacks are freshly signed with valid fixture keys, proving that the verifier is checking policy and chain integrity rather than merely detecting stale signatures.

## Validation and claim boundary

The release gate regenerates every artifact, requires zero drift, runs all five witnesses in check mode, validates the v2 manifest against JSON Schema, executes cross-pass regressions, and audits the repository claims ledger.

All raw counts, keys, signatures, defects, and attacks are deterministic software fixtures.

```text
physical_experiment_completed = false
claim_eligible = false
```
