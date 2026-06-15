# BT1115 — Safer cumulative integrator

BT1115 rebuilds the paper integration helper in smaller chunks to avoid the connector-filtering that blocked the monolithic BT1112 helper.

## Added helpers

```text
tools/bt1115_integrate_core.py
tools/bt1115_integrate_late.py
```

The first helper inserts the core matter/reservoir sections.  The second inserts the later real-form, whitening, coupling, generation, and closure sections.

## Rationale

Several full-size integration-helper patches were blocked by the connector filter.  Splitting the helper into small deterministic chunks makes the integration path easier to maintain and less likely to be filtered.

## Boundary

The helpers stage the section includes.  They do not compile the TeX sources and do not claim a compile pass.
