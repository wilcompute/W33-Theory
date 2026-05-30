# Spread-Sector Chart Transition Affinity

Date: 2026-05-30

This continues the spread-sector affine-coordinate theorem.

Previously we proved that for fixed anchor `p`, anchor line `L`, and allowed direction `d`, the nine spreads in the `L`-sector receive explicit coordinates in

```text
F3^2 = AG(3,3)/<d>.
```

But different choices of direction `d` give different coordinate charts on the same nine spreads.

This theorem tests whether those charts are compatible as affine-plane charts.

## Main result

For a fixed anchor-line sector, every allowed direction gives one `F3^2` coordinate chart on the same nine spreads.

The verifier checks all chart transitions:

```text
chart_d1 -> chart_d2
```

for every ordered pair of distinct directions in every sector.

There are:

```text
4 sectors * 9 directions * 8 target directions = 288
```

ordered chart transitions.

Every one of them is affine-linear over `F3`:

```text
x -> A x + t
```

with

```text
A in GL(2,3), t in F3^2.
```

So the nine spread labels in a sector are not just a 9-element set. They form a genuine affine plane over `F3`, up to affine gauge.

## Meaning

The sector label set is canonically an affine plane object:

```text
sector labels ~= AG(2,3)
```

but no single direction is privileged. Each allowed direction gives one coordinate chart, and all charts are related by elements of

```text
AGL(2,3).
```

The affine gauge group has order

```text
|AGL(2,3)| = 9 * |GL(2,3)| = 9 * 48 = 432.
```

## Bridge to PG(5,3) projection fiber

The projection theorem gave:

```text
PG(5,3) -> PG(3,3)=W33
```

with a 9-point affine fiber over every W33 anchor.

The symplectic projection theorem showed each fiber is an `F3^2` affine plane with four directions.

This theorem shows each spread sector also carries an `F3^2` affine-plane structure, and its coordinate changes are affine-linear.

Therefore the bridge is now stronger:

```text
PG(5,3) projection fiber: affine plane over F3
spread sector labels: affine plane over F3
chart transitions: AGL(2,3)
```

So the identity

```text
36 = 4 * 9
```

means:

```text
four memory-line sectors, each carrying one affine AG(2,3) spread-label plane.
```

## Compressed theorem

```text
Fix anchor p and anchor-line sector L. For each allowed affine direction d in p^perp\L, quotienting AG(3,3) by <d> gives an F3^2 coordinate chart on the nine spreads containing L. For every ordered pair of directions d1,d2, the induced transition chart_d1 -> chart_d2 is affine-linear over F3. Hence each sector is intrinsically an affine AG(2,3) label plane, matching the 9-point projection fiber in PG(5,3)->W33.
```

## Honest boundary

This proves affine compatibility of all spread-sector charts. The remaining hard test is to construct a canonical functor from the PG(5,3) projection fiber to the spread-sector affine plane, including the action of the four kernel directions / line-at-infinity points.
