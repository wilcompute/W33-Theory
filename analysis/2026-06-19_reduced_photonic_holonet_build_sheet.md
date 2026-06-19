# BT1339 — Lab Build Sheet for the Reduced Photonic Holonet

**Date:** 2026-06-19

## Scope

This document packages BT1337 and BT1338 into one laboratory-ready reduced demonstrator:

1. **BT1337:** self-entangled Bell qutrit using one photon
2. **BT1338:** 3-qutrit route-controlled extension

## Experimental milestones

### Milestone 1 — Bell qutrit
Prepare
\[
|\Omega\rangle = \frac{1}{\sqrt{3}}(|00\rangle+|11\rangle+|22\rangle)
\]
and verify:
- $V(I)=1$
- $V(F_3)=1/3$
- $V(X)=0$
- $V(Z)=0$

### Milestone 2 — Route control
Add route qutrit $R$ and implement
\[
U_{R\to F}=|0\rangle\langle0|\otimes I + |1\rangle\langle1|\otimes Z + |2\rangle\langle2|\otimes X
\]

### Milestone 3 — Coherent routing
Inject
\[
|r\rangle = (|0\rangle+|1\rangle+|2\rangle)/\sqrt{3}
\]
and show the route register remains coherent after controlled routing.

## Required hardware

- Heralded single-photon source (SPDC)
- Polarizing beam splitter
- Two 3-port fiber tritters
- Fiber delay ladders for ternary time bins
- Electro-optic modulator (>1 GHz)
- Phase plate / qutrit phase element
- Shift-arm routing element
- Phase-stable interferometric recombination
- Single-photon detectors
- Time-tagging electronics

## Minimal falsification tests

A single failed exact witness kills the corresponding claim:

- If $V(F_3) \neq 1/3$, the tritter is not the qutrit Fourier gate.
- If $V(X)$ or $V(Z)$ is nonzero, the route/gate arms are not clean Clifford actions.
- If coherent superposition in $R$ is lost, route ≠ gate ≠ transport experimentally.
- If the BC-loop gap census fails, the quasicrystal clock claim fails.

## Architecture claim tested

This reduced demonstrator does **not** yet realize the full W(3,3) atlas, but it does test the core architectural identity:

> one photonic transport process can simultaneously carry state, gate action, and route selection.

That is the minimal experimental core of the Photonic Holonet.
