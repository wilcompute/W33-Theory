# Anchor-Stabilizer Spread Equivariance

Date: 2026-05-30

This addresses the honest boundary from the projection-spread functor theorem.

Previously we built a chart-dependent bijection

```text
PG(1,3) x AG(2,3) -> 36 symplectic spreads at an anchor.
```

That proved existence, but not naturality. The question was whether the symplectic stabilizer of the anchor acts compatibly with this product geometry.

## Method

The verifier:

1. Builds W(3,3) points, isotropic lines, and 36 symplectic spreads.
2. Generates the projective symplectic group `PSp(4,3)` from projective transvections.
3. Restricts to the stabilizer of one anchor.
4. Uses the already-constructed `F3^2` chart on each of the four anchor-line sectors.
5. Checks how every stabilizer element acts on those charts.

## Group orders

The generated projective symplectic group has order

```text
|PSp(4,3)| = 25920.
```

The stabilizer of one projective anchor has order

```text
25920 / 40 = 648.
```

The verifier checks both orders exactly.

## Sector structure

At the fixed anchor:

```text
4 anchor lines through the anchor
36 spreads through the anchor layer
4 sectors of 9 spreads
```

Each sector has an `F3^2` coordinate chart from the previous theorem.

## Equivariance test

For every anchor-stabilizer element and every source sector, the verifier computes:

```text
source sector -> target sector
```

and then checks the induced map on the nine labels:

```text
F3^2 -> F3^2
```

The condition is that this map must be affine-linear:

```text
x -> A x + t,
A in GL(2,3), t in F3^2.
```

There are

```text
648 stabilizer elements * 4 sectors = 2592
```

sector-chart actions.

The verifier checks:

```text
all 2592 actions are affine-linear over F3.
```

## Meaning

This upgrades the prior chart-dependent bijection.

The functor

```text
PG(1,3) x AG(2,3) -> 36 spreads at anchor
```

is not canonical pointwise without choosing charts, but it is natural up to affine gauge:

```text
AGL(2,3)
```

inside each sector.

So the correct statement is:

```text
The anchor stabilizer acts on the four memory-line sectors and acts by affine transformations on the nine AG(2,3) labels inside each sector.
```

## Architecture consequence

The identity

```text
36 = 4 * 9
```

is now stable under the local symmetry group.

It is not merely a chosen decomposition. It is equivariant up to the expected finite affine gauge:

```text
4 sectors = PG(1,3) / line-at-infinity directions
9 labels = AG(2,3) affine plane
chart changes = AGL(2,3)
```

## Compressed theorem

```text
The projective symplectic anchor stabilizer of W(3,3) has order 648. Its action on the 36 spreads preserves the 4*9 sector-label structure: it permutes the four anchor-line sectors and acts by affine-linear maps on the nine F3^2 labels inside each sector. Thus the product model PG(1,3) x AG(2,3) is equivariant up to AGL(2,3) gauge.
```

## Honest boundary

This proves equivariance of the local spread-label model. The next hard step is to connect this local stabilizer action to the global `Sp(4,3)` / `W(E6)` action on ordered spread-frame pairs, showing directly how

```text
51840 = 40 * 36^2
```

arises as anchor choice plus ordered local spread-frame transport.
