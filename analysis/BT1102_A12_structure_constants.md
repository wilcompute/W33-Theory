# BT1102 — Structure constants for normalized A12

BT1102 records the trace-normalized commutator table for

```text
A12_R = u(1) direct_sum su(2) direct_sum su(3).
```

## Normalization

BT1098 uses compact anti-Hermitian generators with trace pairing

```text
<X,Y> = -Re Tr(XY).
```

For the weak sector,

```text
W_a = i sigma_a / sqrt(2),  a=1,2,3.
```

For the color sector,

```text
C_a = i lambda_a / sqrt(2),  a=1,...,8.
```

where `sigma_a` are Pauli matrices and `lambda_a` are Gell-Mann matrices.

## U1 sector

The U1 generator commutes with everything:

```text
[Y, anything] = 0.
```

## su(2) structure constants

With the above anti-Hermitian normalization,

```text
[W_a, W_b] = -sqrt(2) epsilon_abc W_c.
```

Equivalently, the only positive-orientation constant is

```text
f^W_123 = -sqrt(2),
```

with total antisymmetry.

## su(3) structure constants

Let `f_abc` be the standard Gell-Mann constants defined by

```text
[lambda_a, lambda_b] = 2 i f_abc lambda_c.
```

Then the normalized anti-Hermitian basis satisfies

```text
[C_a, C_b] = -sqrt(2) f_abc C_c.
```

The independent sorted triples are

```text
f_123 = 1,
f_147 = 1/2,
f_156 = -1/2,
f_246 = 1/2,
f_257 = 1/2,
f_345 = 1/2,
f_367 = -1/2,
f_458 = sqrt(3)/2,
f_678 = sqrt(3)/2.
```

Therefore the normalized constants are the above values multiplied by `-sqrt(2)`.

## Cross-sector constants

All cross-sector commutators vanish:

```text
[u(1), su(2)] = 0,
[u(1), su(3)] = 0,
[su(2), su(3)] = 0.
```

## Boundary

BT1102 fixes the algebraic commutator table for the normalized compact packet.  Physical gauge couplings can still rescale the three direct-summand brackets independently.
