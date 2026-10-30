# Part MMCCCLXXII: Golden Failure Product Bijection

## Claim

The `108` unique golden-selector failures are a direct product:

```text
active K2,2 anchor edge x bridge-line affine cube
  = 4 * 27
  = 108.
```

After ordered orientations:

```text
2^q * 4 * 27 = 8 * 108 = 864.
```

## Forced Quadrangle Rule

Fix the draft selector's anchor line. Let `(a,b)` be one of the four active
anchor cross-pairs, and let `B` be any bridge line disjoint from the anchor
line.

For each anchor endpoint, the generalized-quadrangle axiom gives a unique
off-anchor endpoint line meeting `B`. Therefore `(a,b,B)` forces exactly one
quadrangle:

```text
{anchor line, endpoint_line(a,B), B, endpoint_line(b,B)}.
```

The verifier proves this forced line set and forced point set match every one
of the `108` unique failed quadrangles.

## Profiles

- Each active K2,2 edge sees all `27` bridge lines.
- Each bridge line occurs once for each of the `4` active K2,2 edges.
- For each active pair, the bridge-word projection onto that pair is balanced:
  all `9` coordinate pairs occur exactly `3` times.

## Reading

The previous `4` copies of `27` are not independent cubes. There is one shared
bridge-line affine cube `B27`; the four active K2,2 edges reuse it. The failure
carrier is therefore:

```text
K2,2 x B27.
```

## Boundary

This is a canonical bijection inside the draft golden-selector failure carrier.
It still does not identify these product coordinates with explicit
`O^-(6,2)/A5` cosets.

## Verification

Run:

```bash
python3 analysis/w33_golden_failure_product_bijection.py
```

Expected result: `12/12` checks verified.
