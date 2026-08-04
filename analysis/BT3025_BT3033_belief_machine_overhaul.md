# Passes 3025–3033 — from a fixed decoder to a belief machine

## Evidence ladder

- **Exact finite mathematics:** the 1,436-to-457 causal-state quotient; the cyclic edit obstruction; the finite pilot-order synchronization scores; the D4 Fourier decomposition; the deterministic Blackwell ordering; the verified 28-row D4 upper bound.
- **Exact decision theory for an explicit synthetic channel:** collision-conditioned noisy Bayes policies and measurement-alphabet risks.
- **Source-complete hardware:** adaptive posterior/stopping core and protocol testbench.
- **Pending exact computation:** the SAT/DRUP decision of 27 versus 28.
- **Not measured:** optical D4 confusion matrices, edit rates, FPGA placement/timing, reset energy and laboratory posterior stopping.

## System-level result

The controller should no longer be described as a fixed syndrome decoder. It is a **belief machine**:

1. maintain calibrated likelihoods rather than prematurely hard-decoding a D4 symbol;
2. retain only the future-action causal state once the raw history is no longer operationally relevant;
3. choose both the triangle and the physical syndrome alphabet;
4. use the three already-required pilot identities as an insertion/deletion indexing alphabet;
5. predict conjugation-invariant D4 drift in five Fourier channels;
6. stop when posterior error is cheaper than another physical intervention.

The exact noiseless tree on `master` remains the zero-noise limit. This packet adds the missing inference, synchronization and hardware layers without retyping modeled quantities as laboratory results.

---

## Pass 3025 — noisy nonabelian escalation

The exact 23-row base leaves 1,436 collision classes, each of size two or three, carrying total sparse-prior mass

\[
P(\text{collision})=0.00423797155225715.
\]

For escalation, the observation alphabet is the eight D4 symbols plus erasure. The explicit synthetic channel separates:

- erasure;
- a partial left-rotation fault;
- conjugation drift;
- a uniform dark component.

For each collision class, exact finite-horizon dynamic programming compares immediate MAP stopping with every distinct remaining triangle-likelihood pattern. Probe cost is `0.001` times unit decision error and the horizon is two.

| profile | erasure | partial | drift | dark | conditional residual error | conditional extra probes | unconditional residual error |
|---|---:|---:|---:|---:|---:|---:|---:|
| mild | .02 | .01 | .005 | .001 | 0.000640402 | 0.414147 | 2.7140e-6 |
| moderate | .05 | .02 | .01 | .002 | 0.000757499 | 0.414541 | 3.2103e-6 |
| severe | .10 | .05 | .02 | .005 | 0.001316780 | 0.009295 | 5.5805e-6 |

The severe profile often stops immediately because the probe cost exceeds the information value of a very noisy symbol. That is not decoder failure; it is the stated loss function doing exactly what it should.

**Boundary.** The base collision class is assumed exact. A fully noisy 23-row belief filter is implemented as source architecture but is not part of these frozen numbers.

---

## Pass 3026 — the real fixed-schedule question is 27 versus 28

PR #231 already contains a verified 28-triangle schedule separating all 48,826 no/one/two-edge nonidentity-D4 hypotheses. Therefore “28 versus 29” is stale. The exact bound is

\[
23\le m_{\rm fixed}^\star\le28.
\]

For the central element `r^2`, every triangle reports the parity of faulty boundary edges. Two supports of weight at most two collide exactly when their symmetric difference is a nonzero edge set of weight at most four in the kernel. Hence a 27-row schedule requires a selected triangle-boundary matrix with binary minimum distance at least five.

This yields exactly

\[
\sum_{k=1}^{4}\binom{45}{k}=164220
\]

positive separation clauses over 120 triangle variables, plus an at-most-27 cardinality constraint. By S10 transitivity a selected triangle can be relabelled to `(0,1,2)`, giving a valid symmetry breaker.

The branch contains:

- a CNF generator;
- an exact 28-row full-D4 verifier;
- a proof-producing SAT route;
- an independent proof-check gate;
- fail-closed status language.

**Current status:** source complete, decision pending. UNSAT plus an independently checked proof establishes optimum 28. SAT supplies only a central candidate until the full D4 verifier accepts it.

---

## Pass 3027 — edit synchronization with no new optical mode

The substitution-optimal omitted-slot word remains

```text
102332001123
```

with cyclic Hamming distance nine.

But a cyclic phase word cannot by itself correct one insertion/deletion: adjacent rotations are always related by deleting the first symbol and inserting it at the end, so their Levenshtein distance is at most two. The exact minimum here is two.

The escape uses information already present physically. Three distinct curvature pilots occupy the non-omitted slots, and their order supplies one of `3! = 6` symbols without adding a channel.

The pilot-order sequence

```text
124523021541
```

has finite adjacent-interval insertion/deletion score `1/2`. Combined with the omitted-slot sequence, the pair alphabet has score

\[
\boxed{3/5},
\]

corresponding to finite synchronization parameter `epsilon = 2/5` under the stated convention.

This converts the same three pilots into both curvature telemetry and stream indexing. It is a finite length-12 construction, not an asymptotic synchronization-string theorem.

---

## Pass 3028 — adaptive controller hardware

A synthesizable protocol core now stores three signed log-posterior scores for a collision class, consumes calibrated log-likelihood increments, compares the top-two gap against a programmable stopping threshold and requests at most two escalation tests.

The testbench covers:

1. a decisive first observation;
2. an erasure-like equal-likelihood observation followed by escalation;
3. the two-probe horizon guard.

The likelihood ROM and 1,436-class causal-state table remain generated data rather than hard-coded physics. RTL simulation, synthesis and placement are merge-gated and not presumed successful.

---

## Pass 3029 — exact predictive causal states

Two post-base classes are equivalent when the canonical controller requests the same triangle and every possible D4 observation leads to equivalent future states. This is exact future-action equivalence, not generic state compression.

The result is

\[
1436\longrightarrow457
\]

initial causal states. Including every recursive test node and the single STOP state gives 470 states total:

```text
1230 initial classes stop after one escalation test
 206 initial classes require a possible second test
```

Under the frozen sparse prior:

| representation | fixed bits | conditional entropy |
|---|---:|---:|
| raw collision class | 11 | 8.280979504 |
| future-action causal state | 9 | 7.202688649 |

Thus the exact predictive reduction is

\[
1.078290855\text{ bits}.
\]

For prior drift, the explicit extension retains the posterior probability of a hidden calm/burst regime together with the finite causal state. No laboratory drift law is inferred.

---

## Pass 3030 — BONKERS: a five-channel nonabelian Fourier belief engine

A conjugation-invariant D4 error kernel is a class function. D4 has four one-dimensional irreducible representations and one two-dimensional irreducible representation. Schur's lemma therefore reduces the two-dimensional Fourier block to a scalar.

For the exact rational demonstration kernel with conjugacy-class masses

\[
(90,1,2,3,4)/100,
\]

the four one-dimensional gains are

\[
1,\quad 43/50,\quad22/25,\quad9/10,
\]

and the two-dimensional block gain is

\[
89/100.
\]

In the regular representation the latter appears with multiplicity four. Eight physical symbol probabilities therefore propagate through five spectral channels for the convolution/prediction step.

**Boundary.** Bayesian evidence multiplication and normalization remain nonlinear and occur in the symbol domain. General non-class noise requires a full 2-by-2 block.

---

## Pass 3031 — BONKERS: the measurement-basis portfolio

The controller may choose not only the triangle but the physical syndrome alphabet:

1. full D4 plus erasure;
2. five conjugacy classes plus erasure;
3. the V4 abelianization plus erasure;
4. reflection parity plus erasure.

Every coarse detector is a deterministic post-processing of full D4, so full D4 Blackwell-dominates it. But physical cost can reverse the preferred action.

For the moderate synthetic channel, conditional on a base collision:

| alphabet | outcomes incl. erasure | best one-probe Bayes error | risk reduction |
|---|---:|---:|---:|
| full D4 | 9 | 0.001222911 | 0.004959477 |
| conjugacy class | 6 | 0.001239361 | 0.004943027 |
| V4 | 5 | 0.002411084 | 0.003771304 |
| reflection parity | 3 | 0.004097881 | 0.002084507 |

The conjugacy sensor retains

\[
99.6683\% 
\]

of the full detector's risk reduction. The full detector is worth its extra cost only when its per-decision premium is below `1.64507e-5` times unit decision-error loss in this model.

The physical action is therefore a pair:

\[
(\text{triangle},\text{syndrome alphabet}).
\]

---

## Passes 3032–3033 — paper and evidence overhaul

All four front doors are reorganized around one decision stack:

```text
GEOMETRY
  exact D4 route hypotheses and triangle observations

LIKELIHOODS
  calibrated full/coarse group-valued sensor models

BELIEF
  posterior over a size-2 or size-3 collision class

CAUSAL STATE
  quotient histories by identical future action distributions

ACTION
  STOP, or choose (triangle, sensor alphabet)

CLOCK / STREAM
  omitted slot protects substitution phase
  pilot ordering supplies insertion/deletion indexing

IRREVERSIBLE BOUNDARY
  retain action and residual risk, then uncompute the transcript
```

The overhaul corrects three stale readings:

- the fixed upper bound is 28 on PR #231, not 29;
- a cyclic omitted-slot block is substitution-strong but edit-ambiguous;
- predictive entropy is model-specific logical information, not measured heat.

## Primary-literature boundaries

- Active sequential hypothesis testing and belief-dependent action selection: Naghshvar and Javidi, *Active Sequential Hypothesis Testing*, arXiv:1203.4626.
- Noisy correlated-test active learning: Chen, Hassani and Karbasi, *Near-Optimal Bayesian Active Learning with Correlated and Noisy Tests*, arXiv:1606.09341.
- Synchronization strings and insertion/deletion indexing: Haeupler and Shahrasbi, *Synchronization Strings: Codes for Insertions and Deletions Approaching the Singleton Bound*, STOC 2017 / arXiv:1704.00807.
- Predictive information and thermodynamic inefficiency: Still, Sivak, Bell and Crooks, *Thermodynamics of Prediction*, Physical Review Letters 109, 120604 (2012).
- Harmonic filtering on groups: Chirikjian and Kyatkin, harmonic exponential filtering on motion groups; the D4 specialization and exact five-lane hardware interpretation here are project-specific.

## Selected architecture

The strongest supported controller is a mixed-radix, likelihood-preserving, future-action machine. It does not always use the richest detector, perform the maximum test panel, or remember the complete past. It measures only until the calibrated posterior identifies the next useful action at acceptable residual risk.
