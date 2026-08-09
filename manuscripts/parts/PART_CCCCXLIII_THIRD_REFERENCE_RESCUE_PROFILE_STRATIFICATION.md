# PART CCCCXLIII — Third-Reference Rescue-Profile Stratification (Deterministic Sample)

This part extends CCCCXLII by sampling all three two-reference signature strata
in a deterministic, reproducible way.

## Protocol

For each two-reference signature family:

1. enumerate unordered pairs $(a,b)$ in canonical order,
2. take first 12 pairs,
3. for each pair count feasible third references $c$ (out of 240)
   for the $24/108/108$ partition.

## Result (sampled)

All three strata are internally constant on this deterministic sample:

- signature family size 360: rescue count $126$,
- signature family size 13440: rescue count $234$,
- signature family size 15120: rescue count $240$.

So the sampled rescue profile is strictly ordered:

$$
126 < 234 < 240.
$$

## Consequence

Third-reference rescue power appears strongly signature-conditioned.

## Honesty boundary

This is a deterministic sampled stratification witness, not a full all-pairs
third-reference stratification theorem.
