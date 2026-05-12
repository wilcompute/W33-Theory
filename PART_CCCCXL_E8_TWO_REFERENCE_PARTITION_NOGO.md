# PART CCCCXL — E8 Two-Reference Non-Uniqueness Witness

This part extends the dictionary-boundary program.

## Setup

Given E8 roots (doubled coordinates), choose one or two reference roots $a,b$.
Classify every root $r$ by tuple class:

$$
(r\cdot a,\ r\cdot b).
$$

Then ask whether tuple classes can be grouped into three blocks of sizes

$$
24,\ 108,\ 108.
$$

## Result (exhaustive)

Exhaustive search over all unordered pairs $(a,b)$ including $a=b$:

$$
\binom{240}{2}+240 = 28920
$$

finds **many** valid partitions:

$$
15120\ \text{feasible pairs out of}\ 28920.
$$

The tuple-class signature landscape has exactly three signatures, with exactly
one signature family feasible for the $24/108/108$ split.

## Meaning

- Count bridge remains exact: $240$ edges (W33) and $240$ roots (E8).
- But two-reference tuple-class grouping is **non-unique**: it allows too many
  realizations and therefore does not canonically select the bridge.

So the future constructive dictionary must use richer data than two-reference
tuple classes (e.g., higher-order packet/transport structure).

## Honesty boundary

This is a non-uniqueness (degeneracy) witness for the two-reference ansatz.
It does not yet provide the unique higher-order constructive dictionary.
