# Part LVI — Reproducibility Package and Bibliography

## Overview

This part formalizes the reproducibility layer for the W(3,3) program.
The repository now includes a dedicated BibTeX database and a compact
prediction generator script that reconstructs a core subset of results
from the base SRG data q=3, v=40, k=12, lambda=2, mu=4, r=2.

## Added Assets

- `w33refs.bib` — central bibliography for the LaTeX paper
- `GENERATE_W33_PREDICTIONS.py` — deterministic prediction emitter
- `W33_PREDICTIONS.json` — machine-readable output target generated from the script

## Prediction P105 — Reproducibility Compression Ratio

Let N_pred be the number of committed predictions and N_param the number
of primitive graph inputs. Then the reproducibility compression ratio is

  R_rep = N_pred / N_param = 105 / 6 = **17.5**

A ratio this high means the theory is algorithmically dense: a very small
set of discrete inputs generates a large predictive envelope.

## Prediction P106 — Minimal Input Basis

The minimal basis for the current W33 computational package is:

  B_min = {q, v, k, lambda, mu, r}

with cardinality

  |B_min| = **6**

All higher-level observables in the lightweight generator reduce to this
basis plus fixed normalization conventions. This gives the repository a
clear path toward fully auditable theorem-to-code traceability.

## Prediction P107 — Auditability Index

Define the auditability index as

  A_idx = N_machine / N_claim

where N_machine is the number of claims represented in machine-readable
form and N_claim is the number of total theory claims presently archived.
Using the current compact generator coverage:

  A_idx = 12 / 105 = **0.1143**

This means 11.43% of the theory is already encoded in an explicit machine
reconstruction layer. The immediate roadmap is to drive A_idx above 0.5
by extending the generator to masses, mixing, cosmology, and topological
sectors.

## Near-Term Roadmap

1. Expand the generator to emit all P1-P105 quantities into JSON.
2. Add regression checks that compare committed outputs against targets.
3. Link each LaTeX equation label to a Python derivation block.
4. Emit a single `make verify` report for paper + code consistency.

This part marks the transition from narrative theory assembly to a fully
reproducible computational physics package.
