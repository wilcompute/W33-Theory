# BT859 - The Bell-Compass Parabolic Router

**Status: PROVEN** by GAP in
`analysis/bt859_bell_compass_parabolic_router.py`, with generated evidence in
`data/bt859_bell_compass_parabolic_router.json`.

## The question

Two independently derived quantities equal `1296`:

- the full Bell-line stabilizer has order `1296`;
- the compass incidence graph has `216 x 6 = 1296` cross-class pairs
  `(pentad A5, spread A5)` meeting in `D10`.

The equality is not an identification.  The center of `Sp(4,3)` is invisible
on projective compass objects, so the Bell stabilizer acts through a group of
order `648`.  BT859 computes the actual action and finds a stronger routing
structure.

## The Bell/Siegel router

Fix one isotropic Bell line.  Its projective stabilizer
`3^3:S4` has four orbits on the `1296` compass incidences:

| orbit | Bell line in the pentad core | Bell line in the spread core | local stabilizer |
| ---: | --- | --- | ---: |
| `648` | dark `20`-orbit | outside the schedule (`30`) | `1` |
| `324` | common schedule `10`-orbit | schedule `10`-orbit | `2` |
| `162` | first absolute `5`-pentad | outside the schedule (`30`) | `4` |
| `162` | second absolute `5`-pentad | outside the schedule (`30`) | `4` |

After normalization this is

```text
648/1296 + 324/1296 + 162/1296 + 162/1296
  = 1/2 + 1/4 + 1/8 + 1/8 = 1.
```

It is therefore a complete binary prefix decoder:

```text
0    -> dark mirror bus
10   -> common schedule
110  -> left pentad cache
111  -> right pentad cache
```

This is object-level, not number matching: the four words are decoded by the
fixed Bell line's orbit inside the pentad compass.

## Outer symmetry and chirality

The outer involution extending `PSp(4,3)` to the full order-`51840` symmetry
fuses exactly the two chiral cache orbits.  The full Bell stabilizer therefore
has orbit sizes

```text
648 mirror + 324 schedule + 324 cache.
```

The coarse decoder is `{0,10,11}`.  Restricting to the orientation-preserving
projective subgroup resolves `11` into `{110,111}`.  Route chirality is a
refinement bit: visible to `PSp(4,3)`, gauged by the outer symmetry.

## The dual point router

The point parabolic `3^(1+2):SL(2,3)` behaves differently.  On the same
`1296` compass incidences it has two **regular** orbits of size `648`.  The
outer extension preserves both sheets rather than fusing them.  Thus:

- line/Bell localization produces a variable-length route word;
- point localization produces a persistent one-bit address sheet;
- the two nodes of the `C2` building implement different halves of the
  network protocol.

This supplies the missing architecture-level meaning of the two parabolic
vacua: the point side chooses an address sheet; the Bell-line side decodes a
route class.  The equality `1296=1296` was the shadow of this dual protocol,
not a regular-action isomorphism.
