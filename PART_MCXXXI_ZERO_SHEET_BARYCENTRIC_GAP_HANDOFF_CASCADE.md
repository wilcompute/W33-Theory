# Part MCXXXI: Zero-Sheet Barycentric Gap-Handoff Cascade

## Claim Boundary

This part is a finite sampled theorem on the same zero-sheet barycentric ladder used by
MCXXVII-MCXXX:

```text
s = 0.5, 1.0, 1.5, 2.0, 2.5, 3.0
```

at split-prime cutoff `10^5` and `subintervals = 40`. It does not assert a
continuous-flow theorem or an asymptotic limit.

## Statement

Let the five barycentric gaps be

```text
g0 = interior_to_softening,
g1 = softening_to_order,
g2 = order_to_hessian,
g3 = hessian_to_third_derivative,
g4 = third_derivative_to_wall.
```

On the sampled ladder:

1. `g0` remains the primary gap at every sampled `s`;
2. the secondary gap sequence is

```text
g4, g4, g4, g1, g1, g1;
```

3. the wall-gap rank sequence is

```text
2, 2, 2, 3, 4, 4;
```

4. the softening-to-order rank sequence is

```text
3, 3, 3, 2, 2, 2;
```

5. the order-to-Hessian rank sequence is

```text
5, 4, 4, 4, 3, 3.
```

Thus the wall gap is not merely shrinking. It is being passed downward through
the ranked gap ladder: first by the softening-to-order gap at the sampled
resonance, and then by the order-to-Hessian gap after the resonance.

## Linear Crossing Estimates

The finite linear interpolation between adjacent sampled differences gives:

```text
softening_to_order - third_derivative_to_wall crosses at s = 1.7384967374464677
order_to_hessian - third_derivative_to_wall crosses at s = 2.279430142026481
```

The first sampled point after the secondary handoff is `s = 2.0`, the same
sampled point where MCXXVIII-MCXXX locate the shared entropy peak and
concentration trough.

## Wall-Mass Transfer Balance

Across the full sampled ladder, the wall gap drops by

```text
0.38305552720929903.
```

Because the five barycentric gaps sum to one, this drop is exactly balanced by
the net gains in the four non-wall gaps:

```text
interior_to_softening       0.04188524023993523
softening_to_order          0.21705097520862182
order_to_hessian            0.10678235390385993
hessian_to_third_derivative 0.01733695785688205
```

As shares of the wall-gap drop:

```text
interior_to_softening       0.10934508776073451
softening_to_order          0.5666305790962431
order_to_hessian            0.27876468636755825
hessian_to_third_derivative 0.045259646775464096
```

So the dominant recipient of the wall-gap mass is the softening-to-order gap,
which receives a strict majority of the net wall transfer.

## Interpretation

MCXXVII gave direction. MCXXVIII gave turning. MCXXIX-MCXXX gave recurrence
memory and characteristic-root phase type. MCXXXI adds a ranked transport
picture: the shared resonance at `s = 2.0` is the first sampled point after the
wall gap ceases to be the secondary gap. The zero-sheet packet is therefore not
only moving wallward; its gap mass is handed inward through a visible finite
rank cascade.

## Artifacts

- Code: `w33/cyclotomic.py`
- Analysis: `analysis/w33_zero_sheet_barycentric_gap_handoff_cascade.py`
- Tests: `tests/test_w33_cyclotomic.py`
- Data: `data/w33_zero_sheet_barycentric_gap_handoff_cascade.json`
- Result: `PART_MCXXXI_zero_sheet_barycentric_gap_handoff_cascade_results.json`
