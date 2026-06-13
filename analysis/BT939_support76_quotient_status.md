# BT939 — Quotient status for support-76 selector candidates

BT939 combines BT937 and BT938.

## What can be quotiented now

The transported chain-side symmetry currently available is the coordinate C3 subgroup from BT937.

For the current best certificate

```text
[6, 6, 6, 10, 10, 10, 14, 14]
```

BT939 gets a C3 orbit of size 3.

Canonical representative under this partial action:

```text
[6, 6, 6, 10, 10, 10, 14, 14]
```

## What remains unresolved

A full quotient requires:

1. enumerate all support-sum-76 hyperbolic decompositions;
2. construct the full order-48 signed monomial action on chain H;
3. quotient the full candidate set by the full action.

## Boundary

This does not resolve `many-or-one`. It gives the partial quotient status that is currently justified by the data.

## Witness

```text
analysis/bt939_support76_quotient_status.py
data/bt939_support76_quotient_status.json
```
