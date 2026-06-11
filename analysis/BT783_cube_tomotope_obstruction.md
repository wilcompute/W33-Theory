# BT783 — Cube/Tomotope Bridge Obstruction

BT782 proposed the cleanest possible bridge:

```text
1 -> C2_chiral -> Gamma(T)' -> Aut+(Q3) -> 1
```

BT783 executes that test.  The answer is **no**, and the no is highly
structured.

## Exact failure

The tomotope derived half is

```text
Gamma(T)' = C2^4 : C3
|Gamma(T)'| = 48
```

but it has:

```text
center order = 1
abelianization order = 3
normal C2 subgroup = none
index-2 subgroup = none
order-24 quotient = none
```

So it cannot be a central or even normal `C2` extension of
`Aut+(Q3) = C2^3:C3`.

## The real obstruction

The cube orientation half is:

```text
Aut+(Q3) = C2^3 : C3
|Aut+(Q3)| = 24
```

Its binary core decomposes under the C3 rotation as:

```text
C2^3 = 1 + 2
```

Equivalently, the C3 fixes one non-identity diagonal bit and permutes the
remaining six nonzero bits in two 3-cycles.

The tomotope derived half has binary core:

```text
C2^4
```

and its C3 action is fixed-point-free on nonzero binary bits:

```text
C2^4 = 2 + 2
```

The nonzero orbit profile is five 3-cycles.

Therefore the bridge is not:

```text
add one central chirality bit
```

It is:

```text
kill the cube fixed diagonal bit and insert a second irreducible F4 phase plane
```

## Bridge law

```text
cube:      C2^3 = 1 + 2
tomotope: C2^4 = 2 + 2
```

This is the real exchange rate behind the order-48 coincidence.

The cube chart layer contains a fixed global diagonal bit: the all-ones
translation of the hypercube.  The tomotope cannot tolerate such a fixed bit:
its non-orientable two-flag-orbit structure forces C3 to act without fixed
binary directions.

## CE2 / L∞ reading

This matches the GraphTheory phase-lift motif: the problem is not a missing
lookup-table bit.  It is a cocycle-level obstruction.  The fixed cube diagonal
must be replaced by a second irreducible 2-dimensional phase plane over F2,
which is the finite-field shadow of a Weyl/Heisenberg phase lift.

## Consequence

BT782's exact sequence is false, but a stronger program emerges:

```text
Aut+(Q3)=C2^(1+2):C3
        -- remove fixed diagonal --> C2^2:C3
        -- add second phase plane --> C2^(2+2):C3 = Gamma(T)'
```

This should now be tested against the rank-32 BT780 suborbit atlas.  The
prediction is that one BT780 orbit family detects the fixed diagonal bit, and a
paired family detects the inserted tomotope phase plane.
