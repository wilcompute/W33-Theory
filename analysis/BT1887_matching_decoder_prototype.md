# BT1887 — Matching Decoder Prototype

BT1887 turns the BT1884 detector-time graph into a first finite matching-decoder prototype.

## Scope

The prototype handles:

```text
one persistent data event + one transient measurement event
```

over a three-round detector window.

## Graph counts

```text
detector nodes = 168
time links = 112
single-error links = 528
```

## Weights

```text
time link = 1.0
data link = 2.0
relation-shadow flag = 100.0
```

## Rules

```text
persistent pair -> choose BT1878 data correction
isolated same-check adjacent pair -> choose time-link explanation
data plus measurement -> choose one data link plus one time link if supports are disjoint
relation shadow -> flag/postselect instead of correcting
```

## Verdict

This is the first matching-style decoder layer on top of the repeated-syndrome graph.  It separates one persistent data event from one transient measurement event while preserving the distance-3 boundary.

Boundary: prototype rule table only; not an optimized MWPM implementation or calibrated detector likelihood model.
