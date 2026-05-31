# C3 Overlap as the Qutrit Triangle Codec

Date: 2026-05-30

This continues the `S4` torsor bridge theorem.

Previous result:

```text
A4-type 12 = tetrahedral chirality / oriented flags
Borel-type 12 = signed anchored line bases
```

They meet through

```text
S4 = PGL(2,3),
S4 = A4 H,
H = S3 point stabilizer,
A4 ∩ H = C3.
```

This theorem identifies the geometric meaning of the overlap

```text
C3 = A4 ∩ H.
```

## Projective C3

On the projective line

```text
PG(1,3)
```

fix the anchor point.

The point stabilizer is

```text
H = S3,
```

acting on the three non-anchor projective points.

The subgroup

```text
A4 ∩ H = C3
```

is the alternating subgroup of this `S3`.

The verifier checks:

```text
|C3| = 3
C3 has element orders 1,3,3
C3 acts transitively on the three non-anchor points
```

So the overlap is exactly:

```text
the cyclic qutrit triangle of non-anchor choices on the input line.
```

## Borel lift

The line-basis codec lives in the Borel subgroup

```text
B < GL(2,3)
```

of order 12.

The preimage of the projective `C3` inside `B` has order 6.

The verifier checks its element-order distribution is

```text
1, 2, 3, 3, 6, 6.
```

So the lift is cyclic:

```text
C6.
```

The unipotent part

```text
[[1,t],[0,1]],  t in F3
```

is a `C3`.

It fixes the signed anchor vector and cycles the three projective non-anchor choices.

## Action on signed b choices

The six signed choices for `b` are:

```text
3 projective non-anchor choices * 2 signs = 6.
```

The verifier checks:

```text
unipotent C3 gives two 3-cycles on signed b choices
```

one for each sign.

Adding the central sign

```text
-I
```

gives the full lifted `C6`, which acts transitively on all six signed `b` choices.

So:

```text
C3 projective triangle + central sign = C6 signed-b cycle.
```

## Meaning for the 12-codec

The full 12-codec was

```text
12 = 2 anchor signs * 6 signed b choices.
```

Now the six signed `b` choices are identified as a single lifted `C6` orbit:

```text
6 = C6 signed non-anchor cycle.
```

The projective shadow is:

```text
3 = C3 qutrit triangle.
```

Therefore:

```text
12 = 2 anchor signs * (C3 triangle with central sign lift).
```

## Bridge to tetrahedral chirality

The same `C3` is also the overlap

```text
A4 ∩ S3.
```

So the tetrahedral chiral codec and line-basis codec meet exactly on the local qutrit triangle rotation.

This gives the geometric meaning of the 3-fold overlap in

```text
S4 = A4 S3.
```

## Compressed theorem

```text
The overlap C3=A4∩S3 inside S4=PGL(2,3) is the cyclic rotation of the three non-anchor points of PG(1,3). In the Borel line-codec lift, its preimage is C6: the unipotent C3 gives two sign-separated 3-cycles on the six signed b choices, and adjoining central -I makes one transitive 6-cycle. Thus the common C3 between tetrahedral chirality and anchored line-basis data is precisely the qutrit triangle inside the 12-codec.
```

## Honest boundary

This proves the geometric meaning of the `C3` overlap. The next hard step is to connect this local qutrit triangle to the Fano-line triple law `{a,b}->a+b` and check whether the cyclic orientation agrees with the wedge/dot codec orientation.
