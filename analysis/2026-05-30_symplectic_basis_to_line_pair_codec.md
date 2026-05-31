# Symplectic Basis to Line-Pair Codec

Date: 2026-05-30

This continues the symplectic-basis regular-lift theorem.

The previous correction identified the true regular object:

```text
ordered symplectic bases of F3^4
```

with count

```text
51840 = |Sp(4,3)| = 40 * 36^2.
```

Now we ask what projective incidence data a symplectic basis determines.

## Map

Given a symplectic basis

```text
(a,b,c,d)
```

with

```text
<a,c> = 1
<b,d> = 1
```

and all other basis pairings zero, define

```text
anchor = [a]
L_in  = P(span(a,b))
L_out = P(span(c,d)).
```

Both `L_in` and `L_out` are totally isotropic projective lines.

The anchor lies on `L_in`, and `L_out` is disjoint from `L_in`.

So we have a map

```text
(a,b,c,d) -> ([a], L_in, L_out).
```

## Verified fiber count

The verifier counts all ordered symplectic bases and maps them to the incidence data above.

It checks:

```text
40 anchors
40 isotropic lines
4 isotropic lines through each anchor
27 isotropic lines disjoint from any fixed isotropic line
```

So the image has size

```text
40 * 4 * 27 = 4320.
```

The full basis count is

```text
51840.
```

The fiber size is uniform:

```text
51840 / 4320 = 12.
```

The verifier checks exactly:

```text
every ([a], L_in, L_out) has 12 symplectic bases above it.
```

Therefore:

```text
51840 = 40 * 4 * 27 * 12.
```

## Meaning of the 12

This is a major clarification.

The missing refinement between projective incidence transport and the full regular symplectic-basis torsor is exactly:

```text
12 states.
```

That is the same recurring 12-codec that appeared in:

```text
genus denominator 12
local flag codec 12
Csaszar/Szilassi 84=7*12
Tetrahedron 24=2*12
chain shell 480=40*12
```

Here it appears as:

```text
basis/orientation codec above an anchored disjoint line pair.
```

## Corrected transport hierarchy

The hierarchy is now:

```text
ordered symplectic basis:
    fully regular Sp(4,3) object, size 51840

anchored disjoint line pair:
    projective incidence transport shadow, size 4320

12-codec fiber:
    missing basis/orientation information over each projective line-pair
```

So the correct regular lift is:

```text
projective anchored line-pair transport + 12-state local codec.
```

## Relation to spread transport

The arbitrary ordered spread-pair model has the same total count per anchor,

```text
36^2,
```

but it splits into multiple projective orbit types.

This theorem shows a cleaner projective shadow of the symplectic-basis torsor:

```text
anchor + input isotropic line + disjoint output isotropic line + 12-codec.
```

The `4` in the factorization is the choice of input line through the anchor.

The `27` is the choice of disjoint output line.

The `12` is the local basis/orientation codec.

Thus:

```text
4 * 27 * 12 = 1296 = 36^2
```

above each anchor.

## Compressed theorem

```text
Every ordered symplectic basis (a,b,c,d) determines an anchor [a], an input isotropic line P(span(a,b)) through the anchor, and a disjoint output isotropic line P(span(c,d)). This map has uniform fiber size 12. Hence |Sp(4,3)|=51840 factors as 40 anchors * 4 input lines * 27 disjoint output lines * 12 local codec states. The recurring 12 is exactly the missing basis/orientation refinement over projective line-pair transport.
```

## Honest boundary

This proves the line-pair codec factorization. The next hard step is to identify the 12 fiber states explicitly with tetrahedral flags, oriented bases of `L_in`/`L_out`, or the earlier flag-codec construction.
