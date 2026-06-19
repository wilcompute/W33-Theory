# BT1336 -- Erasure Distance Benchmark

## Purpose

BT1336 adds the first explicit erasure benchmark curve for the [[32,4,4]] block after the BT1334 capacity gate.

## Model

Independent erasures on n=32. Distance d=4 guarantees correction of all erasure sets of size <= 3. The benchmark reports:

```text
Pr[E >= d]
Pr[E <= d-1]
Q(p) = max(0, 1-2p)
```

for representative loss rates below 50 percent.

## Boundary

This is not a full ML or Gottesman-Knill decoder threshold. It is a distance-only guaranteed-correction benchmark plus capacity overlay.

A full threshold curve requires the explicit W33 stabilizer/check matrix so the decoder can determine which erasure sets of size >= 4 remain correctable.

## Files

```text
tools/bt1336_erasure_distance_benchmark.py
data/bt1336_erasure_distance_benchmark.json
```
