# Part CCCXX — Observable Dictionary / Scale Map v1

**Date:** 2026-05-05  
**Status:** first concrete empirical scale-map candidate with locked observable dictionary and no-refit rules

---

## 1. Purpose

CCCXIX defined the empirical closure protocol.

CCCXX instantiates the first concrete observable dictionary.

This is not a completed data fit.  It is the locked comparison machinery required before physical claims can become empirical claims.

The guiding rule is:

\[
\text{finite invariant}
\to
\text{observable dictionary}
\to
\text{fixed scale/RG map}
\to
\text{residuals}
\to
\text{falsification}.
\]

---

## 2. Three scale-map levels

### M0 — No-scale finite predictions

These require no physical unit conversion.

They are tested in finite emulators such as qutrit Pauli systems, photonic graph states, and W33 cluster-state implementations.

### M1 — Dimensionless physical predictions

These compare W33 ratios to measured dimensionless observables.

They require a specified physical scale, scheme, and RG/continuum prescription.

### M2 — Dimensionful predictions

These require anchors for action, causal speed, and one energy/mass/length scale.

Until those are fixed, absolute masses, lengths, times, and gravitational/cosmological constants are not locked predictions.

---

## 3. M0 finite-emulator dictionary

The directly testable finite predictions are:

\[
\frac{q^4-1}{q-1}=40
\]

projective two-qutrit observables.

\[
E=240
\]

W33 graph-state edges.

\[
K+1=13=\Phi_3
\]

full cluster stabilizer weight.

At critical fusion

\[
p=\frac{\lambda}{\mu}=\frac12,
\]

we get

\[
pE=120,
\]

\[
pK=6=2q,
\]

\[
Kp(1-p)=3=q,
\]

\[
1+pK=7=\Phi_6,
\]

and

\[
E/p=480.
\]

These are not interpretive guesses.  They are finite emulator predictions.

---

## 4. M1 dimensionless target dictionary

The initial dimensionless target list is:

\[
\sin^2\theta_W=\frac38
\]

as a unification-boundary candidate,

\[
Q_{Koide}=\frac23
\]

as a charged-lepton mass-ratio candidate,

\[
p_{fusion}=\frac12,
\]

\[
p_{KLM}=\frac14,
\]

\[
\text{Markov contraction}=\frac1q=\frac13,
\]

\[
P_{nonreverse}=\frac{K-1}{K}=\frac{11}{12},
\]

and

\[
P_{reverse}=\frac1K=\frac1{12}.
\]

The physical targets require explicit scale/scheme choices before residuals are meaningful.

---

## 5. M2 dimensionful requirements

Dimensionful predictions require at least three anchors:

1. action-unit anchor, usually \(\hbar\),
2. causal-speed anchor, usually \(c\),
3. one energy/mass/length anchor to fix the remaining unit scale.

Once these are fixed, every additional dimensionful observable becomes a prediction, not another fit.

---

## 6. No-refit rules

The scale-map rules are:

1. after anchors and RG/continuum rules are fixed, no observable-specific refitting is allowed,
2. dimensionless ratios must be tested before dimensionful absolute quantities,
3. every fitted anchor consumes one degree of freedom and must be listed separately from predictions,
4. the RG or continuum rule must be specified before comparing with data,
5. each empirical claim must include measurement uncertainty and theory uncertainty.

These rules prevent the theory from becoming numerology.

---

## 7. Theorem statement

**Scale Map v1 turns the W33 finite theorem into an empirical framework by separating no-scale finite predictions, dimensionless physical predictions, and dimensionful predictions.**

It locks an observable dictionary and no-refit rules.

After anchors, schemes, and RG/continuum flow are fixed, all residuals must be evaluated without moving the map.

---

## 8. Honest boundary

This is a candidate empirical dictionary, not a completed data fit.

It defines what must be compared and how it can fail.

Measured constants should be supplied by a separate versioned data file before numerical residuals are claimed.

---

## 9. Regression status

The CCCXX test file verifies:

1. W33 atoms and finite targets,
2. M0 finite emulator predictions,
3. M1 dimensionless targets,
4. resource/Clifford and dimensionful requirements,
5. dictionary and rule shape,
6. threshold relations,
7. audit-level consistency.

---

## 10. Next target

The next empirical move is a versioned data-target file:

\[
\texttt{empirical\_targets\_v1.json}
\]

with measured values, schemes, uncertainties, W33 predictions, residuals, and pass/fail rules.

Only then should the physical comparison layer claim numerical agreement or disagreement.
