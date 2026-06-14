# BT959 — Transported S4 orbit/stabilizer of the final selector

BT959 uses the recovered BT956 chain-to-tetracode matrix and transports the tetracode block-permutation quotient S4 back to the BT925 chain mask gauge.

## Final selector

```text
[[3,68], [4,42], [38,65], [90,144]]
```

## Result

```text
group_order = 24
orbit_size = 24
stabilizer_size = 1
stabilizer = identity only
```

The S4 orbit intersects the exact support-60 minimizer set in exactly one point: the selected minimizer itself.

## Reading

Under the strongest explicit transported quotient currently available, the final selector is S4-rigid inside the six support-60 minimizers. Its S4 orbit has size 24, but only the original selected minimizer remains support-minimal.

## Boundary

This is the transported block-permutation quotient. It does not yet include a fully transported local A2/Weyl glue stabilizer action.

## Witness

```text
analysis/bt959_selected_minimizer_stabilizer_orbit.py
data/bt959_selected_minimizer_stabilizer_orbit.json
```
