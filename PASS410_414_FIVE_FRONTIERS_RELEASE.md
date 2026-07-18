# Passes 410–414 — Prime-Power Smith Closure, Qutrit Magic Injection, Radius-Three Sandpile Decoding, Symmetry Twirling, and Independent Laboratory Custody

**Status: executable mathematical and engineering certificates pass locally. No physical experiment is claimed.**

## Pass 410 — the first non-prime Smith form

Let `Gamma_q` be the `q^3`-vertex Heisenberg bulk graph on `(x,y,z) in F_q^3`, with

```text
(x,y,z) ~ (x',y',z') iff (x,y)!=(x',y') and z'-z = yx'-xy'.
```

The reduced Laplacian for `q=9` has size `728 x 728`. Instead of applying a coefficient-exploding integer Smith algorithm, the witness performs exact unit-pivot elimination over `Z/(3^K)`, deletes every unit row/column pair, divides the remaining 3-divisible block by 3, and repeats. These are Smith-equivalent operations over `Z_3`, so the pivot count at page `k` is the number of elementary divisors with exact 3-adic valuation `k`.

The exact sequence, including unit invariant factors, is

```text
valuation:  0    1    2    3   4  5   6
count:     100  128  292   92  37  0  79
```

Therefore

\[
K(\Gamma_9)_{(3)}\cong
(\mathbb Z/3)^{128}\oplus
(\mathbb Z/9)^{292}\oplus
(\mathbb Z/27)^{92}\oplus
(\mathbb Z/81)^{37}\oplus
(\mathbb Z/729)^{79}.
\]

There are no `3^5` factors. Combining this with the semisimple and 2-adic sectors gives

\[
\boxed{
K(\Gamma_9)\cong
(\mathbb Z/8)^{72}\oplus(\mathbb Z/16)^{288}
\oplus(\mathbb Z/3)^{128}\oplus(\mathbb Z/9)^{292}
\oplus(\mathbb Z/27)^{92}\oplus(\mathbb Z/81)^{37}
\oplus(\mathbb Z/729)^{79}\oplus(\mathbb Z/5)^{288}
}.
\]

Its order is

\[
2^{1368}3^{1610}5^{288},
\]

which exactly equals the matrix-tree formula. The same algorithm rederives the frozen `q=3` and `q=5` characteristic-primary forms.

**Boundary:** Pass 410 gives an exact prime-power algorithm and the complete first extension-field case `q=9`. It does not claim a closed elementary-divisor multiplicity formula for all extension degrees `f`.

## Pass 411 — a non-Clifford qutrit resource

Define

\[
T=\operatorname{diag}(1,\zeta_9,\zeta_9^{-1}),\qquad \zeta_9=e^{2\pi i/9}.
\]

The witness enumerates the existing 216 projective qutrit Cliffords and proves:

- `T` is not Clifford;
- `T^9=I` projectively, while `T^3` is nontrivial;
- `T X T^\dagger` and `T Z T^\dagger` are Clifford, so `T` lies in the third Clifford-hierarchy level;
- the magic state `|M_T>=T F|0>` has maximum stabilizer fidelity approximately `0.7123860142`, hence is non-stabilizer.

The Choi resource

\[
(I\otimes T)|\Phi_3\rangle
\]

implements deterministic gate teleportation. Every one of the nine generalized Bell outcomes has probability `1/9` and an exact feed-forward correction in the existing `X,Z,F,P` alphabet. The longest correction word has length three.

For a five-qutrit distance-three postselection gadget with independent input error `e`, detecting every weight-one and weight-two fault gives the conservative conditional logical-error bound

\[
\epsilon_{\rm out}\le
\frac{10e^3(1-e)^2+5e^4(1-e)+e^5}{(1-e)^5}.
\]

This bound contracts below the input error for `e < 0.2086219937`; at one percent it is approximately `1.036e-5`. If each input leaks with probability `l` and leakage flags have efficiency `eta`, a conservative undetected-round bound is

\[
1-[1-l(1-eta)]^5.
\]

**Boundary:** the distance-three expression is a rigorous combinatorial upper bound, not a claim that a particular five-qutrit distillation code has exactly that nonlinear map.

## Pass 412 — the exact multi-slip frontier

A pulse relocation contributes the degree-zero divisor `e_target-e_source`. For multiple relocations, the sandpile syndrome depends only on the sum of these divisors.

The first essential distinction is:

\[
\text{sandpile memory records net imbalance, not hidden edge pairing.}
\]

Two path decompositions with the same target and source multiplicities have identical syndromes. Integer directed cycle flows are therefore invisible to the divisor map. Edge or time-bin telemetry is required to reconstruct pairing.

For `Gamma_3`, the edge connectivity is eight. If an integer firing vector is nonconstant, its maximum-level set has boundary at least eight, so every nonzero principal divisor has positive degree at least eight. A single fired vertex attains eight. Hence the minimum principal transport weight is exactly eight.

Two net errors of weight at most three differ by weight at most six, so they cannot differ by a nonzero principal divisor. Therefore:

\[
\boxed{\text{every net pulse imbalance of weight }\le3\text{ has a unique sandpile class}.}
\]

The exact counts are:

| net transport weight | classes |
|---:|---:|
| 1 | 702 |
| 2 | 123,552 |
| 3 | 9,746,802 |

Including zero, there are `9,871,057` uniquely represented net classes through weight three.

The radius is sharp. Splitting the eight neighbors of one vertex into two sets of four produces distinct weight-four divisors `d1,d2` with

\[
d_1-d_2=L e_v,
\]

so they have the same syndrome. Pass 412 also supplies an erasure-aided decoder that enumerates degree-zero divisors on a detector-supplied support of at most six modes and verifies unique recovery through weight three.

## Pass 413 — symmetry-twirled calibration

The full spatial group

\[
\operatorname{Aut}(\Gamma_3)=H_3\rtimes GL(2,3)
\]

has order `1296`. The witness explicitly generates all 1,296 permutations and verifies that every one preserves adjacency.

The action has four pair orbitals, exactly the four distance classes. Therefore the group average of an arbitrary `27 x 27` mode covariance lies in the four-dimensional Bose–Mesner algebra. Equivalently it decomposes into adjacency eigenspaces

| eigenvalue | rank |
|---:|---:|
| 8 | 1 |
| 2 | 12 |
| -1 | 8 |
| -4 | 6 |

The witness constructs the exact spectral projectors, proves that they are orthogonal idempotents summing to the identity, and directly averages a deterministic covariance over all 1,296 permutations.

On the qutrit channel side, both `SL(2,3)` and `GL(2,3)` act transitively on the eight nonidentity Pauli labels. A Pauli-diagonal channel therefore reduces to one nonidentity error parameter after twirling. The combined diagonal calibration report contracts 216 raw mode/Pauli axes to four spatial spectral powers, one common Pauli rate, and a separately measured leakage rate.

A deterministic 64-epoch randomized-compiling schedule records each spatial automorphism, its exact inverse, and a qutrit Clifford word.

**Boundary:** the group average is exact. Experimental gate dependence, non-Markovian drift, and sampling error remain measured assumptions, consistent with finite-group and character randomized-benchmarking theory.

## Pass 414 — independent laboratory replication custody

The external handoff packet defines five signing roles:

1. protocol owner;
2. acquisition laboratory;
3. blind-key custodian;
4. blinded analyst;
5. independent auditor.

Eight artifacts form a signed chain:

1. frozen protocol;
2. accepted BOM;
3. calibration certificate;
4. blinded raw counts;
5. blinded analysis;
6. blind key;
7. unblinded result;
8. independent audit.

Each artifact receives an Ed25519 signature over a canonical envelope containing the artifact SHA-256 digest, artifact type, signer role, and timestamp. The contract enforces protocol/BOM/calibration freeze before acquisition, analysis after acquisition, key release after blinded-analysis freeze, and audit after unblinding. The raw-count signer, key custodian, analyst, and auditor satisfy explicit separation constraints.

The release contains:

- a JSON Schema;
- an empty production manifest;
- a human runbook and acceptance checklist;
- a deterministic signed nonclaim fixture that validates all signatures and ordering rules.

The deterministic private keys are test-only and invalid for production.

## Validation

The release gate regenerates every artifact, requires zero drift, runs every witness in check mode, validates both Pass-414 manifests against the JSON Schema, executes cross-pass tests, and verifies the live claims ledger.

No laboratory counts were acquired. `physical_experiment_completed=false` and `claim_eligible=false` remain mandatory for every fixture.

## Primary research anchors

- Anwar, Campbell, and Browne, *Qutrit Magic State Distillation*, arXiv:1202.2326.
- Prakash, Jain, Kapur, and Seth, *Normal form for single-qutrit Clifford+T operators and synthesis of single-qutrit gates*, arXiv:1803.03228.
- França and Hashagen, *Approximate Randomized Benchmarking for Finite Groups*, arXiv:1803.03621.
- Claes, Rieffel, and Wang, *Character randomized benchmarking for non-multiplicity-free groups*, arXiv:2011.00007.
