# BT1110 — Candidate generation weights from W33 generation ledgers

BT1110 tests what the known generation ledgers can and cannot determine about the BT1108 weights

```text
w0,w1,w2 > 0.
```

## Constraint from the 27+27+27 split

The W33 generation carrier is already split as

```text
27 direct_sum 27 direct_sum 27.
```

This split alone is generation-symmetric.  Therefore it selects the baseline

```text
w = (1,1,1)
```

and the symmetric projector

```text
M_w = (1/3) 11^T.
```

No mass hierarchy follows from the bare `27+27+27` decomposition.

## Constraint from D9 shell-cycle bookkeeping

Each generation contributes one `D9` cycle-sum bookkeeping block.  The count is again symmetric:

```text
D9_0 + D9_1 + D9_2.
```

The `D9` blocks are killed by the reservoir readout, so their dimension count alone cannot determine `w_g`.  They can only supply future perturbation data if an additional cycle-energy or orbit-depth functional is defined.

## Koide-phase candidate family

The one existing generation-breaking pattern in the archive is the Koide-style phase family.  A W33-compatible traceless first-order perturbation is

```text
w_g = 1 + epsilon cos(theta + 2*pi*g/3),  g=0,1,2.
```

The cosine triple satisfies

```text
sum_g cos(theta + 2*pi*g/3) = 0,
```

so it matches the BT1108 traceless first-order condition.

Thus the best current candidate is the two-parameter family

```text
w(theta,epsilon) = (1 + epsilon cos(theta),
                    1 + epsilon cos(theta+2*pi/3),
                    1 + epsilon cos(theta+4*pi/3)).
```

The symmetric point is recovered at `epsilon=0`.

## Positivity

The weights are positive whenever

```text
1 + epsilon cos(theta + 2*pi*g/3) > 0
```

for all `g`.  A sufficient uniform condition is

```text
|epsilon| < 1.
```

## Conclusion

Current W33 data determines the symmetric baseline and admits a natural Koide-phase traceless perturbation family.  It does not yet determine a unique numerical triple `(w0,w1,w2)` without an additional mass, Yukawa, orbit-depth, or cycle-energy functional.
