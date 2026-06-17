# BT1251 -- Ordered/Oriented Gate Invariance

## Purpose

BT1251 answers the ordered-gate refinement question for the BT1233 symmetric Cayley tomography fingerprint.

## Result

For a four-generator set there are

\[
4!\,2^4=384
\]

ordered/oriented label variants.

However, BT1233 uses the symmetric alphabet

\[
\{g_1,g_1^{-1},\ldots,g_4,g_4^{-1}\}.
\]

Therefore:

1. permuting the four labels leaves the same alphabet;
2. replacing any \(g_i\) by \(g_i^{-1}=g_i^2\) also leaves the same alphabet.

So all 384 label/orientation variants have the same unlabelled Cayley sphere and ball-growth fingerprint.

## Consequence

The BT1233 fingerprint is intentionally an unlabelled symmetric recovery invariant.  To distinguish ordered pulse labels or generator orientation, a future harness must add labelled-word observables, directed-channel observables, or calibrated physical pulse data.

## Files

- Code: `analysis/bt1251_ordered_oriented_gate_invariance.py`
- Result: `data/bt1251_ordered_oriented_gate_invariance_summary.json`
