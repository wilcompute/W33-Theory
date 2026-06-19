# BT1334 -- Gottesman-Knill Threshold Capacity Gate

## Purpose

BT1334 answers the BT1327 question in a capacity-aware way.

## Question

Can a Gottesman-Knill / stabilizer decoder push the W33 holonet photon-loss threshold above 50 percent?

## Result

Under the channel model used in BT1325 -- independent photon loss treated as quantum erasure -- the answer is no.

The relevant capacity form is:

```text
Q(p) = max(0, 1 - 2p)
```

So:

```text
Q(0.144) = 0.712
Q(0.50) = 0
Q(p>0.50) = 0
```

A Gottesman-Knill decoder can make stabilizer decoding efficient and may improve the practical threshold toward 50 percent from below, but it cannot violate the erasure-channel capacity wall.

## Correct target

Replace the speculative target:

```text
p_th > 50 percent
```

with the admissible target:

```text
certify the best W33 stabilizer decoder threshold below 50 percent and compare it against 14.4 percent ML-loss baseline.
```

## Files

```text
tools/bt1334_gk_threshold_capacity_gate.py
data/bt1334_gk_threshold_capacity_gate.json
```
