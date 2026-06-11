# BT772 — Chirality is the Axis Type; the Plücker Mirror Flips Chirality

Resolves the BT759 transport question (T6) — at a different level than
conjectured, with a sharper outcome.

## Setup

BT750: duo partners (k, r^6 k) share their canonical reflection t but
present distinct apartments.  Both apartments are t-invariant, and an
involution fixing an octagon setwise acts through an axis: through 2
antipodal points (P-axis), 2 antipodal lines (L-axis), or freely.

## Measured (12 duo pairs of the test rectangle; exhaustive by D12)

```text
chirality 1 (Type-A): BOTH duo octagons P-axis, DIFFERENT axis points  (x6)
chirality 0 (Type-B): BOTH duo octagons L-axis, DIFFERENT axis lines   (x6)
```

## Theorem 1: chirality = axis type

A presentation pair is Type-A iff its canonical reflection acts on its
apartment with an axis through 2 POINTS; Type-B iff through 2 LINES.
This is the first intrinsic geometric characterization of the BT745/BT746
chirality — no mask convention, no edge ordering: just where the
reflection axis meets the apartment.

## Theorem 2: the duality mirrors chirality, not the duo bit

The W(3,3) <-> Q(4,3) duality is the point/line side-swap at the
incidence-graph level.  Side-swap exchanges P-axis and L-axis, hence
exchanges Type-A and Type-B.  Consequences:

- BT746's absolute chirality is exactly the q-odd NON-self-duality of
  W(3): the only operation that could flip chirality is the duality that
  Aut(W(3,3)) does not contain.
- The BT755/BT759 "Pluecker mirror" exists, but it is the CHIRALITY
  mirror.  The duo-bit transport conjecture (r^6 = dual orientation) is
  refuted.

## Theorem 3: the duo bit is the axis-vertex selection

Duo partners share (rectangle, reflection, axis type) and differ in WHICH
antipodal pair of t's fixed vertices forms their apartment axis.  The duo
bit is an internal choice within the fixed geometry of t (8 points + 6
lines, BT747): same mirror, different anchor pair.

## Updated dictionary

```text
hinge datum (BT705)  =  dihedral phase (6)  x  duo (2)        [BT749]
chirality            =  P-axis vs L-axis of canonical reflection [BT772]
duality / Pluecker   =  chirality mirror                        [BT772]
duo bit              =  axis-anchor selection inside Fix(t)     [BT772]
```

## Boundary

Open: enumerate the t-invariant apartments through a fixed rectangle
(expected: 2 per axis-type per reflection — verify the count 2+2 against
the 24 = (6+6) x 2 lift structure); transport the axis-anchor datum into
the BT760-771 Q(4,3) harness (it should now resolve the 48 partner
directions: the partner direction is the OTHER anchor pair, same type);
and re-express the BT718 sheet's non-uniformity (BT748) in axis-anchor
coordinates.
