# Projection-Spread Functor Existence

Date: 2026-05-30

This packages the previous projection-fiber and spread-sector coordinate theorems into an explicit finite functor.

Previous results:

```text
PG(5,3) -> PG(3,3)=W33
```

has a 9-point affine `F3^2` fiber over each anchor plus a 4-point kernel

```text
PG(1,3).
```

Also, for a fixed W33 anchor, the 36 symplectic spreads split into:

```text
4 anchor-line sectors * 9 spreads per sector.
```

Each sector carries an affine `F3^2` coordinate plane, and all chart transitions are affine-linear.

## New construction

After choosing one affine chart in each sector, define a map

```text
PG(1,3)_kernel directions x F3^2_fiber labels -> symplectic spreads at anchor.
```

The four kernel directions are represented by the four points of

```text
PG(1,3):
(1,0), (0,1), (1,1), (1,2).
```

The verifier pairs those four directions with the four anchor-line sectors.

Then, inside each sector, the `F3^2` label selects one of the nine spreads using the affine coordinate chart from the spread-sector theorem.

## Verified result

The domain has

```text
4 * 9 = 36
```

objects.

The codomain has

```text
36
```

symplectic spreads.

The verifier checks:

```text
functor domain size = 36
functor image size = 36
all 36 spreads are hit exactly once
```

So, after finite chart choices, this gives an explicit bijective functor:

```text
PG(1,3) x AG(2,3) -> {36 spreads at anchor}.
```

## Line at infinity compatibility

The four `PG(1,3)` kernel directions are also the four parallel classes of the affine `AG(2,3)` fiber plane.

For each direction, the verifier checks the corresponding parallel class in `F3^2` has:

```text
3 parallel lines
3 points per line
covers all 9 points
pairwise disjoint lines
```

So the line-at-infinity structure matches:

```text
PG(1,3) = directions at infinity of AG(2,3).
```

## Meaning

This is the coordinate-level bridge we needed:

```text
PG(5,3) projection fiber:
    AG(2,3) points plus PG(1,3) directions

spread sector layer:
    four memory-line sectors, each with AG(2,3) spread labels
```

The finite functor identifies:

```text
kernel direction -> memory-line sector
fiber coordinate -> spread label inside that sector
```

Therefore:

```text
36 = 4 * 9
```

is not just a count. It is the product of:

```text
PG(1,3) line-at-infinity directions
```

and

```text
AG(2,3) affine fiber labels.
```

## Compressed theorem

```text
After choosing one affine chart per anchor-line sector, the 36 spreads at an anchor are bijective with PG(1,3) x AG(2,3). The four PG(1,3) directions select the four memory-line sectors; the AG(2,3) coordinate selects the spread inside that sector. The four kernel directions are also exactly the four parallel classes of the AG(2,3) fiber plane.
```

## Honest boundary

This proves existence after finite chart choices. It is not yet canonical without choices. The next hard test is to determine whether the symplectic group stabilizer of the anchor acts equivariantly on both sides, which would upgrade this from a chart-dependent bijection to a natural equivalence of finite geometries.
