# BT949 — Holonet-to-w33 cross-reference

BT949 adds a paper-routing bridge from the main narrative paper to the heavy-math manuscript.

## Correct split

```text
photonic_holonet.tex = current main narrative / architecture paper
w33_paper.tex       = heavy-math manuscript target
```

## Integrator

```text
tools/integrate_bt949_holonet_w33_crossref.py
```

It idempotently inserts a short paragraph after the Holonet abstract saying that the heavy E8/SNF/symplectic-selector derivations live in `w33_paper.tex`.

## Boundary

The connector pass committed the integrator and routing manifest. It did not directly overwrite `photonic_holonet.tex`; run the integrator in a full checkout to patch the source.
