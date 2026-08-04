# Passes 3133–3142 — certifying adaptive inference closure

## Why this packet exists

The parallel Passes 3124–3132 search the hard underlying objects: the 27-row schedule,
rank-three M36 codes, the 6,480-flag representation, the coupled POMDP, the 2,796-tick
fabric, and the compute/routing ISA trade. This packet does not race those searches. It
builds the independent filters, certifiers, streaming decoders, hardware envelopes and
proof boundaries needed to decide whether their outputs are usable.

The controlling architecture is now:

```text
physical D4 symbols
  -> full 48,826-hypothesis posterior
  -> Fourier prediction lanes
  -> future-action causal state
  -> action-rate-distortion selector
  -> streaming phase tracker
  -> isolated virtual belief context
  -> explicit irreversible reset
```

## Evidence ladder

- **Exact finite:** D4 hypothesis/signature census; batch/streaming posterior identity;
  576-case single-edit tracking theorem; Pareto hull construction; contraction
  coefficients; virtual-context bit counts; collision break-even algebra.
- **Exact for explicit synthetic models:** posterior values, action-rate-distortion surface,
  and memory horizons.
- **Source-complete:** rank-three candidate certifier, fixed-point Fourier/causal RTL,
  isolated-context RTL, front-door integrator and evidence workflow.
- **Pending:** external rank-three candidates, RTL simulation/synthesis/placement, paper
  materialization and laboratory likelihoods.

---

## 3133 — the base panel must remain a belief, not a lookup

The exact 23-row panel on the full nonabelian fault universe reproduces:

```text
hypotheses                         48,826
signature classes                 46,284
immediately unique hypotheses     44,848
largest collision class                3
```

A log-domain filter now evaluates all 48,826 hypotheses under explicit positive
D4-plus-erasure channels. Batch normalization and row-by-row streaming normalization agree
to `3.4416913763379853e-15`.

The sparse prior is:

```text
P(no fault)       = 0.995
P(one-edge total) = 0.0045
P(two-edge total) = 0.0005
```

Under the **moderate** synthetic channel, even a transcript equal to a rare fault's
noiseless signature can remain dominated by no fault:

| modal transcript | truth posterior | MAP posterior | truth is MAP? |
|---|---:|---:|---:|
| no fault | 0.999990198 | 0.999990198 | yes |
| one edge carrying `r` | 0.069173283 | 0.928631086 | no |
| adjacent `r,s` pair | 0.107423432 | 0.795379866 | no |
| disjoint `r,s` pair | 0.768219361 | 0.768219361 | yes |

This is not a defect. It is the correct Bayesian consequence of a 99.5% no-fault prior
and a noisy detector. The architecture must therefore preserve a posterior over the full
universe through the base panel; hard assignment to a noiseless collision class is valid
only in the exact-symbol model.

**Boundary:** these are exact calculations for stated synthetic kernels. Laboratory
confusion matrices remain absent.

---

## 3134 — a rank-three candidate must pass an independent certifier

A six-qubit rank-three stabilizer group defines an eight-dimensional code. The certifier
accepts three signed binary symplectic generators and checks, independently:

1. binary rank exactly three;
2. pairwise commutation;
3. Hermitian idempotent projector of trace eight;
4. all nine single-error vectors annihilated;
5. nonzero clean success probability;
6. accepted clean output is not a stabilizer state, tested by the complete Pauli
   expectation criterion.

The committed negative control uses `Z0,Z1,Z2`. It has rank three, commutes, and produces a
trace-eight projector, but is rejected because:

```text
max single-error projection norm = 1/sqrt(3)
clean success probability         = 0
```

The tool is deliberately a **certifier, not a search**. Failure to receive an accepted
candidate is not a no-go theorem. Parallel Pass 3125 can feed candidates into this checker
without sharing its search implementation.

---

## 3135 — five spectral lanes fused to the causal controller

The conjugation-invariant D4 predictor has four one-dimensional Fourier gains and one
scalar two-dimensional block. The fixed-point Q1.15 datapath implements:

```text
43/50 -> 28180 / 32768
22/25 -> 28836 / 32768
 9/10 -> 29491 / 32768
89/100 -> 29164 / 32768  (twice)
```

Maximum coefficient error is below `1.47e-5`.

The same clock edge updates the generated nine-bit causal-state ID and four-bit action.
The module does **not** pretend Bayesian normalization is linear: likelihood
multiplication, normalization, and the generated 470-state transition ROM remain explicit
interfaces.

A second module stores multiple guest contexts. Only the selected context can change; the
shared Fourier datapath is read-only with respect to every guest. The testbench writes two
contexts in succession and proves the first remains unchanged.

**Boundary:** source RTL and protocol tests are committed. Tool-observed synthesis and
timing remain evidence-gated.

---

## 3136 — one edit is tracked within three received symbols

The transmitted per-tick index is the pair:

```text
(omitted slot, ordering of the three existing pilots)
```

so the alphabet has `4 x 6 = 24` symbols. Assuming phase was locked before the edit, every
single event was enumerated:

```text
12 positions x (23 substitutions + 24 insertions + 1 deletion) = 576 cases
```

Exact result:

| received symbols after the edit | cases |
|---:|---:|
| 2 | 565 |
| 3 | 11 |

The eleven three-symbol cases are exactly insertions equal to the expected symbol. Hence:

> **Every single insertion, deletion, or substitution relocks within three received
> symbols, with no extra optical mode.**

This is a tracking theorem with prior lock. It is not blind phase acquisition and not a
multiple-edit guarantee. Synchronization strings remain the relevant asymptotic prior-art
framework; this finite periodic tracker is project-specific.

---

## 3137 — the complete action-rate-distortion surface

The selector now ranges jointly over:

- syndrome alphabet: stop, reflection parity, V4, conjugacy class, or full D4;
- zero through six chirality copies;
- raw, causal-state, or immediate-action retention;
- expected W33 route cost of 1.275 symplectic shears.

An explicit normalized synthetic cost model generates 105 policies. Eleven lie on the
lower convex envelope:

| cost | distortion | detector | chirality copies | retained state |
|---:|---:|---|---:|---|
| 0.000103 | 0.031209 | stop | 0 | action |
| 0.040103 | 0.010796 | stop | 1 | action |
| 0.080103 | 0.007638 | stop | 2 | action |
| 0.120103 | 0.006676 | stop | 3 | action |
| 0.395603 | 0.002905 | V4 | 3 | action |
| 0.435603 | 0.002592 | V4 | 4 | action |
| 0.635603 | 0.001420 | conjugacy | 4 | action |
| 0.675603 | 0.001317 | conjugacy | 5 | action |
| 0.689905 | 0.001291 | conjugacy | 5 | causal |
| 0.729905 | 0.001257 | conjugacy | 6 | causal |
| 1.079905 | 0.001240 | full D4 | 6 | causal |

The crucial architectural reading is that optimal resolution increases in stages. Full D4
is used only at the extreme low-distortion end; most of the frontier uses either no route
measurement, V4, or conjugacy-class sensing.

**Boundary:** this is a dimensionless design surface with all weights frozen in the
certificate, not a physical-energy or laboratory-risk prediction.

---

## 3138 — BONKERS: the belief simplex has a certified forgetting geometry

For each strictly positive D4 prediction kernel, the Dobrushin coefficient gives a total-
variation contraction and the Hilbert projective diameter gives Birkhoff's coefficient.
Bayesian multiplication by a positive diagonal likelihood is Hilbert-isometric, so the
uniform worst-case forgetting rate is controlled by prediction.

| profile | Dobrushin | Birkhoff | steps to TV <= 1% | steps to TV <= 1e-6 |
|---|---:|---:|---:|---:|
| mild | 0.998989899 | 0.999744703 | 4,557 | 13,671 |
| moderate | 0.996907216 | 0.999204455 | 1,487 | 4,461 |
| severe | 0.988888889 | 0.996923077 | 413 | 1,237 |

The counterintuitive direction is correct: a more strongly mixing noise kernel forgets its
initial condition faster. The bounds are deliberately conservative and uniform over all
priors and observation sequences.

This converts “retain history until it seems irrelevant” into a certifiable memory horizon
for every calibrated positive kernel.

---

## 3139 — BONKERS: recursive virtual belief machines

The raw post-base controller needs 1,436 class labels, or 11 fixed bits per guest. The
future-action controller needs 470 states, or 9 fixed bits.

| guests | raw independent bits | causal independent bits | saved |
|---:|---:|---:|---:|
| 1 | 11 | 9 | 2 |
| 2 | 22 | 18 | 4 |
| 4 | 44 | 36 | 8 |
| 8 | 88 | 72 | 16 |
| 16 | 176 | 144 | 32 |

For a fixed child policy, a parent needs only the nine-bit causal state: action and
advantage are recovered from the policy table. Distinct guest updates commute exactly
because they act on different Cartesian-product coordinates.

The proposed recursive machine therefore shares the five-lane predictor while retaining
private causal contexts. This is stronger than permission-based isolation: a guest update
has no write path to another context.

---

## 3140 — compute-versus-inference break-even law

The current computing ISA has 45 generator collisions among 324 outgoing labeled edges.
The minimum-collision computing set has 18. Therefore:

```text
current collision exposure per dispatch = 45/324 = 5/36
minimum computing exposure              = 18/324 = 1/18
reduction                                = 27/324 = 1/12
```

At the measured mean native program length `14.175585`, the lower-collision ISA avoids:

```text
14.175585 / 12 = 1.18129875
```

collision exposures per program. At equal instruction and collision-resolution cost, it
may therefore spend **1.1813 additional mean instructions** and still break even. The
allowed extra path length scales linearly with the collision/instruction cost ratio:

| cost ratio | affordable extra mean instructions |
|---:|---:|
| 0.25 | 0.2953 |
| 0.5 | 0.5906 |
| 1 | 1.1813 |
| 2 | 2.3626 |
| 4 | 4.7252 |

This does not duplicate Pass 3129's ISA search. It is the decision boundary that tells the
search when a longer, less-colliding ISA is actually superior.

---

## 3141–3142 — paper and evidence overhaul

All canonical front doors are reorganized around **certifiable predictive execution**:

```text
geometry -> symbol likelihood -> full posterior -> spectral prediction
         -> causal state -> costed action -> stream tracker -> reset
```

The overhaul makes four corrections explicit:

1. the noisy base panel is not a hard collision-class lookup;
2. an eight-dimensional candidate is not a protocol until an independent certifier checks
   its accepted output is magic;
3. finite edit tracking requires prior lock;
4. contraction horizons and rate-distortion values are model-derived, not measured heat or
   optical performance.

## Primary-literature boundaries

- Naghshvar and Javidi, *Active Sequential Hypothesis Testing*, arXiv:1203.4626.
- Nitinawarat and Veeravalli, *Controlled Sensing for Sequential Multihypothesis Testing
  with Controlled Markovian Observations and Non-Uniform Control Cost*, arXiv:1310.1844.
- Haeupler, Shahrasbi and Vitercik, *Synchronization Strings: Channel Simulations and
  Interactive Coding for Insertions and Deletions*, arXiv:1707.04233.
- Hilbert/Birkhoff contraction of positive filtering kernels is established mathematics;
  the exact D4 coefficients and memory horizons are project-specific.
