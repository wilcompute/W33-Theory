# Ordered Spread-Transport Orbits

Date: 2026-05-30

This tests the global transport claim suggested by the exact identity

```text
51840 = 40 * 36^2 = |Sp(4,3)|.
```

The tempting stronger claim would be:

```text
ordered triples (anchor, source spread, target spread)
```

form a single regular transport torsor.

The verifier checks the projective version under

```text
PSp(4,3).
```

## Setup

The object set is

```text
(anchor, source spread, target spread)
```

with size

```text
40 * 36 * 36 = 51840.
```

The projective symplectic group has order

```text
|PSp(4,3)| = 25920.
```

The full linear symplectic group is the double cover:

```text
|Sp(4,3)| = 2 * 25920 = 51840.
```

So the count matches the full linear symplectic order exactly.

## Projective orbit test

The verifier generates `PSp(4,3)` from projective transvections and acts on all ordered triples.

Result:

```text
The ordered triples do not form one projective regular orbit.
```

Instead, they split into multiple projective transport orbit types.

The orbit invariants include:

```text
whether source and target spreads lie in the same anchor-line sector
how many isotropic lines the two spreads share
```

So projective spread transport has genuine incidence types; it is not just a free homogeneous torsor at the projective level.

## Meaning

The identity

```text
40 * 36^2 = |Sp(4,3)|
```

is still real and important, but it should be read carefully:

```text
40*36^2 is a linear symplectic / Weyl lift count.
```

It is not, by itself, proof that projective triples

```text
(anchor, spread_in, spread_out)
```

are a single regular `PSp(4,3)` orbit.

The missing ingredient is the central sign/orientation lift from projective to linear symplectic geometry.

## Corrected statement

```text
PSp(4,3) acts on ordered anchor/spread/spread triples with several orbit types.
Sp(4,3) has the same order as the total number of triples, so a regular transport interpretation must include additional linear sign/orientation data not visible in the projective incidence geometry alone.
```

## Why this matters

This is a good correction. It prevents us from overclaiming the meaning of

```text
51840 = 40 * 36^2.
```

The equality remains one of the strongest count identities:

```text
anchor * ordered spread-frame pair = full linear symplectic order.
```

But the projective action has multiple transport types. Therefore the next hard test is not merely group order; it is to construct the missing orientation/sign refinement and see whether the seven projective orbit types collapse into a regular linear transport object.

## Compressed theorem

```text
The set of ordered triples (anchor, source spread, target spread) has 51840 elements, equal to |Sp(4,3)|. Under PSp(4,3), however, these triples split into multiple incidence orbit types rather than one regular projective orbit. Thus 40*36^2 is best read as a full linear symplectic/Weyl lift count; a regular transport model requires extra sign/orientation data beyond projective W(3,3) incidence.
```

## Honest boundary

This proves the projective orbit correction. The next hard step is to identify the missing sign/orientation datum explicitly, probably from oriented isotropic lines, ordered bases of spread lines, or the central `±I` lift in `Sp(4,3)`.
