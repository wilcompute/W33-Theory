# Polarity, Chirality, and Orientation Duality

Date: 2026-05-31

This addresses the chirality boundary from the Fano-polarity toroidal flag labeling.

Previous theorem:

```text
Fano chart state (L,p,d)
```

is equivalently

```text
(L, M, orientation of M\L),
```

where `L` and `M` are distinct Fano lines.

This labels Szilassi face flags directly and Csaszar vertex flags after Fano polarity.

The remaining question was:

```text
Does polarity preserve or reverse chirality?
```

## Important boundary

In the abstract Fano plane over `F2`, there is no ordinary determinant sign or Euclidean handedness.

So the honest finite chirality datum is the two-state local orientation

```text
p -> q
```

versus

```text
q -> p
```

on the two affine points of

```text
M\L.
```

This is a side/orientation codec, not a Euclidean chirality sign.

## Polarity action

A Szilassi-style flag is

```text
(line axis L, adjacent line M, orientation p->q).
```

Fano polarity maps it to the Csaszar-style flag

```text
(polar point of L, polar point of M, same orientation p->q).
```

So polarity:

```text
swaps line/face axes with point/vertex axes,
```

but preserves the local orientation label

```text
p -> q.
```

## Verified result

The verifier checks:

```text
84 Szilassi-style flags
84 Csaszar-style flags
42 ordered axis pairs on each side
2 orientations per ordered axis pair
42 orientation-reversal pairs on each side
```

It also checks:

```text
polarity is involutive
```

and, crucially,

```text
polarity commutes with local orientation reversal.
```

That is:

```text
polar(reverse(flag)) = reverse(polar(flag)).
```

So polarity does not flip the local two-state orientation by itself. It preserves the local side/orientation label and reverses the incidence type.

## Correct statement

The correct finite-incidence statement is:

```text
Fano polarity preserves local orientation labels and swaps axis type line<->point.
```

or:

```text
polarity preserves the side/orientation codec while performing face-vertex duality.
```

It is not meaningful, at this abstract F2-incidence level, to claim that polarity preserves or reverses Euclidean chirality.

For that, we would need an embedding orientation for a specific Csaszar or Szilassi realization.

## Relation to toroidal duality

This cleanly matches the toroidal duality:

```text
Szilassi:
    face/line axes

Csaszar:
    vertex/point axes
```

Fano polarity implements the dual swap.

The local two-state side/orientation survives the swap.

## Compressed theorem

```text
In the Fano incidence labeling of the 84 flags, a local orientation is the ordered pair p->q on M\L. Fano polarity maps Szilassi-style line/face flags (L,M,p->q) to Csaszar-style point/vertex flags (polar(L),polar(M),p->q). It is involutive and commutes with orientation reversal p->q <-> q->p. Thus polarity preserves the finite two-state orientation codec while reversing incidence type line<->point. Any stronger Euclidean chirality claim requires an added embedding orientation.
```

## Honest boundary

This proves the abstract incidence orientation behavior. The next hard step is to add a concrete oriented realization of Csaszar/Szilassi and test whether the geometric embedding orientation agrees with, or reverses, the Fano side/orientation label.
