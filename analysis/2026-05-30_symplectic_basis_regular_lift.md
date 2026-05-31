# Symplectic-Basis Regular Lift

Date: 2026-05-30

This resolves the correction from the ordered spread-transport orbit test.

We tested the tempting claim that arbitrary ordered triples

```text
(anchor, source spread, target spread)
```

form a single regular transport object. Projectively, they do not. They split into several orbit types under `PSp(4,3)`.

The correct regular object of size

```text
51840 = 40 * 36^2
```

is instead:

```text
ordered symplectic bases of F3^4.
```

## Symplectic basis definition

An ordered basis

```text
(a,b,c,d)
```

of `F3^4` is symplectic if, with the standard alternating form,

```text
<a,c> = 1
<b,d> = 1
```

and all other pairings among basis vectors vanish.

These bases are exactly the images of the standard basis under `Sp(4,3)`. Therefore `Sp(4,3)` acts simply transitively on them.

## Count

The verifier counts the bases by construction:

```text
choose a nonzero vector:                          80 choices
choose c with <a,c>=1:                            27 choices
choose b in span(a,c)^perp, b != 0:                8 choices
choose d in span(a,c)^perp with <b,d>=1:           3 choices
```

Thus:

```text
80 * 27 * 8 * 3 = 51840.
```

So:

```text
number of ordered symplectic bases = |Sp(4,3)| = 51840.
```

## Fiber over projective anchor

Projectivize the first vector `a`.

There are:

```text
40
```

projective anchors, since each projective point has two nonzero representatives `a` and `-a`.

For each projective anchor, the number of symplectic bases above it is:

```text
2 * 27 * 8 * 3 = 1296.
```

But:

```text
1296 = 36^2.
```

Therefore:

```text
51840 = 40 * 1296 = 40 * 36^2.
```

This is the precise regular meaning of the spread-square factorization.

## Correction to arbitrary spread transport

The previous ordered-spread transport test showed:

```text
(anchor, spread_in, spread_out)
```

has the right total count:

```text
40 * 36^2 = 51840.
```

But under projective symplectic action, those triples split into multiple incidence orbit types.

So arbitrary ordered spread pairs are count-compatible with the symplectic basis torsor, but they are not themselves the clean regular object.

The clean regular object is:

```text
ordered symplectic basis.
```

## Interpretation

The corrected dictionary is:

```text
40:
    projective choice of first symplectic vector / W33 anchor

36^2:
    number of symplectic completions over that projective anchor

51840:
    ordered symplectic bases = Sp(4,3)
```

The spread-frame pair language remains useful, but it needs an orientation/basis refinement to become regular.

## Compressed theorem

```text
The equality 51840=40*36^2 is not best interpreted as arbitrary projective ordered spread transport. The canonical regular object is the set of ordered symplectic bases (a,b,c,d) of F3^4. There are 80*27*8*3=51840 such bases, and over each projective anchor [a] there are 2*27*8*3=1296=36^2 completions. Thus Sp(4,3) acts simply transitively on the regular lift, while the projective spread-pair model is a quotient shadow with several orbit types.
```

## Honest boundary

This proves the regular linear object. The next hard step is to map a symplectic basis completion over an anchor to a refined pair of local spread frames, determining exactly what orientation/basis data must be added to a spread pair to recover the symplectic-basis torsor.
