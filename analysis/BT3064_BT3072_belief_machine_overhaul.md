# Passes 3064–3072 — the Holonet becomes a belief machine

## Parallel-work reconciliation

This packet was initially numbered 3025–3033, but `master` independently reserved 3025–3031 for a predictive photonic overhaul. The work was re-homed before publication. It composes with, rather than duplicates, two live parallel results:

- Passes 3020–3024 prove the 18 rank-two witness pairs are not stabilizer codes, quantify the two machine diameters, and derive the 45.98% routed-read information efficiency and logarithmic network energy law.
- The parallel 3025–3031 reservation targets rank-three M36 codes, the 6,480-flag representation, optical A4 readout and a unified posterior controller. The present packet supplies the noisy D4 inference, edit-indexing, causal-state and detector-alphabet layers that such a controller needs.

## Evidence ladder

- **Exact finite:** 1,436→457 future-action quotient; edit obstruction and finite scores; D4 Fourier decomposition; Blackwell order; verified 28-row upper bound.
- **Exact for explicit synthetic models:** noisy Bayes policy values and detector-alphabet Bayes risks.
- **Source-complete:** adaptive RTL, SAT/DRUP route, four-front-door integrator.
- **Pending:** proof-checked 27-row SAT decision, RTL simulation/synthesis/placement, three PDF builds and laboratory likelihoods.

## 3064 — noisy nonabelian escalation

The exact common 23-row panel leaves 1,436 collision classes of size at most three, carrying sparse-prior mass 0.00423797155225715. For escalation, observations are the eight D4 symbols plus erasure. The synthetic channel explicitly separates erasure, partial left rotation, conjugation drift and uniform dark outcomes.

At probe cost 0.001 times unit decision loss and horizon two:

| profile | conditional residual error | conditional extra probes | unconditional residual error |
|---|---:|---:|---:|
| mild | 0.000640402 | 0.414147 | 2.7140e-6 |
| moderate | 0.000757499 | 0.414541 | 3.2103e-6 |
| severe | 0.001316780 | 0.009295 | 5.5805e-6 |

The severe model often stops: the physical symbol is too noisy to justify its cost. The calculation assumes the base collision class is exact; a fully noisy base filter remains open.

## 3065 — 27 versus 28, fail closed

PR #231 already supplies a verified 28-triangle schedule, so the stale “28 versus 29” formulation is corrected to

\[
23\le m_{\rm fixed}^{\star}\le28.
\]

On the central element r², two weight-at-most-two supports collide exactly when their symmetric difference is a nonzero edge set of weight at most four in the selected triangle-boundary kernel. A 27-row schedule therefore requires binary minimum distance at least five.

The exact decision instance has

\[
\sum_{k=1}^{4}\binom{45}{k}=164220
\]

separation clauses over 120 triangle variables, an at-most-27 constraint and a valid S10 symmetry breaker. UNSAT plus independent DRUP checking proves optimum 28; SAT is only a central candidate until all 48,826 group-valued hypotheses pass. Source is complete; the decision is not yet claimed.

## 3066 — edit synchronization with the same three pilots

The omitted-slot word `102332001123` retains cyclic Hamming distance nine, but adjacent cyclic phases are always related by one deletion and one insertion. Its minimum cyclic Levenshtein distance is two, so an isolated cyclic block cannot uniquely correct one insertion/deletion.

The three distinct pilots already occupying the non-omitted slots have six possible orders. The order word

```text
124523021541
```

has finite adjacent-interval insertion/deletion score 1/2. Paired with the omitted slot, the score is 3/5, with zero additional optical modes. Omission protects substitutions; pilot ordering supplies stream indexing.

## 3067 — hardware posterior core

The committed synthesizable core stores three signed log-posterior scores, adds calibrated likelihood increments, compares the top-two gap with a programmable threshold and requests at most two escalation tests. The testbench covers decisive stopping, erasure-like escalation and the horizon guard. The 1,436-class ROM remains generated data, not invented physics.

## 3068 — predictive causal states

Two post-base histories are equivalent when they request the same next triangle and every possible D4 observation enters equivalent future states. Exact Moore-machine minimization gives

\[
1436\to457
\]

initial causal states and 470 total recursive states including STOP. Of the raw classes, 1,230 need at most one escalation test and 206 may need two.

| representation | fixed bits | conditional entropy |
|---|---:|---:|
| raw collision class | 11 | 8.280979504 |
| future-action state | 9 | 7.202688649 |

The exact reduction is 1.078290855 bits under the frozen sparse prior. For drifting priors, the explicit extension retains posterior burst probability plus the finite causal state; no measured drift law is inferred.

## 3069 — BONKERS: five spectral belief lanes

A conjugation-invariant D4 error kernel is a class function. D4 has four one-dimensional irreducible representations and one two-dimensional irrep; Schur’s lemma makes the latter block scalar. For class masses `(90,1,2,3,4)/100`, the nontrivial gains are

\[
43/50,\quad22/25,\quad9/10,\quad89/100,
\]

with 89/100 repeated four times in the regular representation. Thus eight symbol probabilities propagate through five Fourier channels for convolution/prediction. Bayesian evidence multiplication and normalization remain nonlinear and explicit.

## 3070 — BONKERS: choose the sensor alphabet

The controller chooses both the triangle and the syndrome alphabet:

| alphabet | outcomes incl. erasure | one-probe error | risk reduction |
|---|---:|---:|---:|
| full D4 | 9 | 0.001222911 | 0.004959477 |
| conjugacy class | 6 | 0.001239361 | 0.004943027 |
| V4 abelianization | 5 | 0.002411084 | 0.003771304 |
| reflection parity | 3 | 0.004097881 | 0.002084507 |

Full D4 Blackwell-dominates every deterministic coarse detector, but the conjugacy detector retains 99.6683% of its risk reduction. In the moderate model, full D4 is worth its premium only below 1.64507e-5 units of decision loss per collision decision.

## 3071–3072 — overhaul and evidence

The four canonical front doors are reorganized around:

```text
geometry → likelihood → belief → causal state → action → stream index → reset
```

Three stale claims are corrected: the fixed upper bound is 28, not 29; cyclic substitution strength is not insertion/deletion correction; logical predictive entropy is not measured heat. The paper also cross-links the parallel 45.98% information-efficiency law and the rank-three M36 mechanism without absorbing them into this packet’s claims.

## Primary-literature boundaries

- Naghshvar and Javidi, *Active Sequential Hypothesis Testing*, arXiv:1203.4626.
- Chen, Hassani and Karbasi, *Near-Optimal Bayesian Active Learning with Correlated and Noisy Tests*, arXiv:1606.09341.
- Haeupler and Shahrasbi, *Synchronization Strings*, STOC 2017 / arXiv:1704.00807.
- Still, Sivak, Bell and Crooks, *Thermodynamics of Prediction*, PRL 109, 120604 (2012).
- Harmonic filtering on groups is established; the exact five-lane D4 specialization and hardware interpretation are project-specific.
