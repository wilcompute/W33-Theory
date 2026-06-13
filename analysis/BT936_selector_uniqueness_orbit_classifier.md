# BT936 — Selector uniqueness/orbit classifier

BT936 classifies the selector theorem candidate from BT933 using the new BT934 and BT935 data.

## Classification

| layer | status |
|---|---|
| support | best certificate is support sum 76, spread 8, profile `[6,6,6,10,10,10,14,14]`; global minimality not yet proved |
| metric | dual compatibility known: BT929 and BT930 lift into both vertex and tetracode E8 witnesses |
| symmetry | vertex symmetry is useless; tetracode signed monomial symmetry has order 48 but its chain action is not yet constructed |

## Orbit conclusion

```text
many-or-one unresolved
```

The current data do not justify a one-orbit uniqueness claim. The selector is metric-compatible and has a best support certificate, but uniqueness waits on exhaustive support classification plus a chain action of the tetracode signed monomial group.

## Next exact test

Enumerate all support-sum-76 hyperbolic decompositions and quotient them by the tetracode monomial group once its chain action is built.

## Witness

```text
analysis/bt936_selector_uniqueness_orbit_classifier.py
data/bt936_selector_uniqueness_orbit_classifier.json
```
