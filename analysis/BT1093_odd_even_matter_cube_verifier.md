# BT1093 — Odd/even matter cube verifier

BT1093 exports the explicit antipodal decomposition of the ternary matter cube used in BT1089.

## Ambient cube

```text
C[F3^3]
```

has dimension 27.  The antipodal involution is

```text
x -> -x.
```

It fixes only the origin and partitions the remaining 26 vectors into thirteen antipodal pairs.

## Explicit decomposition

The odd subspace is

```text
B13 = span{ e_x - e_-x }
```

with one basis vector for each projective direction in `PG(2,3)`.  Hence

```text
dim B13 = 13.
```

The even subspace is

```text
R14 = span{ e_0 } direct_sum span{ e_x + e_-x }
```

so

```text
dim R14 = 1 + 13 = 14.
```

Therefore

```text
C[F3^3] = B13 direct_sum R14,
13 + 14 = 27.
```

## Witnesses

```text
analysis/bt1093_odd_even_matter_cube_verifier.py
data/bt1093_odd_even_matter_cube_verifier.json
```

The JSON lists all thirteen antipodal pairs using canonical projective representatives whose first nonzero coordinate is `1`.
