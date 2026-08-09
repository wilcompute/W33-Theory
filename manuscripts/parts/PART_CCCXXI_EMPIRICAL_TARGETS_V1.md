# Part CCCXXI — Empirical Targets v1

**Date:** 2026-05-05  
**Status:** versioned empirical target file with exact predictions and unresolved external-data slots

---

## 1. Purpose

CCCXX defined the observable dictionary and scale-map rules.

CCCXXI creates the first versioned empirical target file:

\[
\texttt{empirical\_targets\_v1.json}.
\]

The key rule is strict:

\[
\text{do not insert unverified measured constants.}
\]

Exact W33 finite-emulator predictions can be evaluated immediately.  Physical Standard Model / CODATA / PDG comparisons require a versioned external source before residuals are claimed.

---

## 2. Data policy

The data policy is:

1. exact finite W33 targets are marked `READY_EXACT`,
2. physical targets requiring measured constants are marked `DATA_REQUIRED`,
3. laboratory probability targets are marked `EXPERIMENT_REQUIRED`,
4. dimensionful targets are marked `ANCHORS_REQUIRED`,
5. residuals are computed only after measured value, uncertainty, scheme, scale, and source are supplied.

This prevents accidental numerology.

---

## 3. Exact ready targets

The ready exact targets are:

\[
\frac{q^4-1}{q-1}=40
\]

projective observables,

\[
E=240
\]

cluster edges,

\[
K+1=13
\]

full stabilizer weight,

\[
pE=120
\]

critical edge half,

\[
pK=6
\]

critical mean degree,

\[
Kp(1-p)=3
\]

critical degree variance,

\[
1+pK=7
\]

critical stabilizer weight,

\[
E/p=480
\]

expected full-cluster fusion trials,

and Clifford resource quotients

\[
[432,216,108,54].
\]

The ready walk targets are:

\[
\text{Markov contraction}=\frac13,
\]

\[
P_{nonreverse}=\frac{11}{12},
\]

\[
P_{reverse}=\frac1{12}.
\]

---

## 4. External data required targets

The first two physical comparison targets are intentionally unresolved:

\[
\sin^2\theta_W=\frac38
\]

requires a unification scale, gauge normalization convention, RG equations, and measured electroweak value with uncertainty.

\[
Q_{Koide}=\frac23
\]

requires a lepton mass scheme, scale, and measured masses with uncertainties.

Until those are supplied, there is no residual and no claim of empirical agreement.

---

## 5. Experiment required targets

The first two laboratory probability targets are:

\[
p_{fusion}=\frac12,
\]

and

\[
p_{KLM}=\frac14.
\]

These require specified experimental implementations before comparison.

---

## 6. Dimensionful anchor requirement

Dimensionful predictions are not evaluated in v1.

They require:

1. action anchor,
2. causal-speed anchor,
3. one energy/mass/length anchor.

Only after those are fixed can absolute physical quantities be compared without refitting.

---

## 7. Residual convention

The residual convention is:

\[
\text{residual}=\text{measured value}-\text{theory value}.
\]

The z-score convention is:

\[
z=\frac{\text{residual}}{\sigma_{measurement}}.
\]

Theory uncertainty should be added later when the RG/continuum map is specified.

---

## 8. Status summary

The target status summary is:

\[
12\text{ READY\_EXACT},
\]

\[
2\text{ DATA\_REQUIRED},
\]

\[
2\text{ EXPERIMENT\_REQUIRED},
\]

\[
1\text{ ANCHORS\_REQUIRED}.
\]

---

## 9. Theorem statement

**Empirical Targets v1 is the first versioned comparison layer for the W33 program.**

It separates exact finite targets from physical targets requiring external data, locks the residual convention, and prevents unverified constants from being treated as evidence.

---

## 10. Honest boundary

This file does not claim agreement with current PDG/CODATA values.

It prepares the exact target schema.

Measured values must be added from a cited, versioned source before physical residuals are interpreted.

---

## 11. Regression status

The CCCXXI test file verifies:

1. W33 and finite targets,
2. dimensionless and resource targets,
3. target schema and statuses,
4. threshold relations,
5. audit-level consistency.

---

## 12. Next target

The next part should create:

\[
\texttt{empirical\_data\_template\_v1.json}
\]

with fields for measured value, uncertainty, scheme, scale, source, date, and residual computation.

Once real data is inserted from a current source, the repo can produce a genuine empirical residual table.
