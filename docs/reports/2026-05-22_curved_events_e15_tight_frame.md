# 2026-05-22 - Curved Events as an E15 Tight Frame with Tomotope Redundancy

## Breakthrough

The previous result showed the trace identity

```text
trace(192 E15) = 15 * 192 = 2880
```

matching the number of one-centered curved events.

This pass proves a stronger statement: the 2880 curved events form a unit tight frame after projection onto the rank-15 curvature-active sector.

## Setup

Let M_curved be the 40 x 2880 point-event incidence matrix of one-centered curved events.

Let E15 be the rank-15 W33 projector

```text
E15 = (8I + J - 4A) / 24.
```

The curved Gram matrix is

```text
M_curved M_curved^T = 272I + 16J + 20A.
```

## Tight-frame theorem

The script verifies the exact identity

```text
E15 M_curved M_curved^T E15 = 192 E15.
```

So the E15-projected curved events form a tight frame in the 15-dimensional curvature-active space with frame bound 192.

## Unit norm theorem

For every curved event vector b, the projected E15 norm is exactly one:

```text
b^T E15 b = 1.
```

So the 2880 curved events become 2880 unit vectors in the E15 sector.

The redundancy is therefore

```text
2880 / 15 = 192.
```

## Meaning

The tomotope 192 is no longer only a count or trace coefficient.  It is the exact tight-frame redundancy of the one-centered curved events inside the rank-15 curvature-active sector.

```text
curved events -> E15 projection -> 2880 unit vectors -> tight frame bound 192
```

This is stronger than saying the events can be counted as 15 packets of 192.  The whole set is canonically a 192-redundant frame over the 15-dimensional mode.

## Boundary

This still does not choose a canonical partition of the 2880 events into 15 disjoint 192-event packets.  It gives a canonical frame decomposition, which is probably the more natural linear-algebraic version of the tomotope packet relation.

## New code

- `analysis/w33_curved_events_e15_tight_frame.py`

When run, it writes:

- `data/w33_curved_events_e15_tight_frame.json`
