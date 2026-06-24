# BT1664 — Component-Level Optical Budget

## Purpose

BT1663 used abstract contrast parameters. BT1664 replaces those knobs with named
hardware components:

- switch survival;
- delay survival;
- phase-shifter survival;
- analyzer survival;
- detector efficiency;
- dark-count probability per time bin.

The numerical values are explicit placeholders, not measured hardware values.

## Default component values

\[
\eta_{\rm switch}=0.995,
\qquad
\eta_{\rm delay}=0.998,
\qquad
\eta_{\rm phase}=0.999.
\]

Thus one graph-walk pass has survival

\[
\eta_{\rm walk}=0.99201699.
\]

Analyzer and detector defaults are

\[
\eta_{\rm analyzer}=0.98,
\qquad
\eta_{\rm detector}=0.85.
\]

The time-bin envelope is

\[
N=2048.
\]

## Resonance port

For

\[
P_{\rm res}=P_{c,6}\otimes P_{m,24},
\]

the compiler gives:

\[
\text{term count}=6,
\qquad
\|c\|_1=31/432,
\qquad
\text{max walk depth}=5.
\]

The placeholder budget gives

\[
\eta_{\rm weighted}=0.815807499276,
\qquad
S=36.666463881272.
\]

## Companion port

For

\[
P_{\rm comp}=P_{c,0}\otimes P_{m,30},
\]

the compiler gives:

\[
\text{term count}=8,
\qquad
\|c\|_1=35/108,
\qquad
\text{max walk depth}=5.
\]

The placeholder budget gives

\[
\eta_{\rm weighted}=0.821383867965,
\qquad
S=36.791565396791.
\]

## Boundary

The pass rule is

\[
S\ge5.
\]

Both ports pass under the placeholder defaults. This is not an experimental claim:
the next step is to replace the defaults with actual component measurements from
the optical design.

## Files

- `analysis/bt1664_component_optical_budget.py`
- `data/PART_BT1664_COMPONENT_OPTICAL_BUDGET_results.json`
