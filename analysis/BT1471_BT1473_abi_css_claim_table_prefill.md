# BT1471--BT1473: ABI-to-CSS join, DAG claim table, and SCIRP-prefilled transcription

## BT1471 — ABI-to-CSS executable join

The closure ABI now feeds directly into the retwined CSS matrices.  The ABI
loop generates 72 qutrit-value rows:

\[
24\text{ active}+48\text{ guard}=72.
\]

Those rows are checked against the retwined CSS matrices from BT1425.  The ranks
remain

\[
\operatorname{rank}(H_X)=39,\qquad \operatorname{rank}(H_Z)=120,\qquad k=81.
\]

All ABI-generated rows satisfy both X and Z syndrome checks under the retwined
frame.

## BT1472 — DAG-to-paper claim table

The BT1469 dependency DAG is rendered as a TeX table with columns:

\[
\text{Claim},\quad\text{Tier},\quad\text{Dependencies},\quad\text{Allowed paper language}.
\]

Exact coordinate/count/group/decoder/ABI claims receive exact language.
Numerical bridges receive resonance language.  Formula-level claims remain
blocked pending transcription, and external real-world interpretation remains
not imported.

## BT1473 — SCIRP-prefilled transcription packet

The transcription packet now includes visible prose anchors from the SCIRP HTML:

- equations (49)--(50): golden-mean and series approximations to the anomalous gyromagnetic factor;
- equation (64): icosahedron/quartic/circumsphere relation;
- equation (65): power of the 12-sling / 13-half-turn ratio;
- equation (66): modified Schwinger alpha/pi relation.

The formula fields remain blank and blocked until rendered equations are
transcribed.

## Current architecture

\[
\boxed{
\text{ABI rows}\to\text{retwined CSS checks}
\quad+\quad
\text{DAG claim table}
\quad+\quad
\text{SCIRP-prefilled formula worksheet}
}
\]
