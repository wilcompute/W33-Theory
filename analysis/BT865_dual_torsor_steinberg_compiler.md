# BT865 - The Dual-Torsor Steinberg Compiler

**Status: PROVEN** by `analysis/bt865_dual_torsor_steinberg_compiler.py`,
with evidence in `data/bt865_dual_torsor_steinberg_compiler.json`.

BT858 found two different order-27 geometries around a chosen self-context:

- the 27 non-collinear **points** are a torsor for the extraspecial
  Heisenberg group `H27 = 3^(1+2)`;
- the 27 disjoint **lines** of the Bell shell are a torsor for the flat
  translation group `F3^3`.

BT861 then proved that the native `[[240,81,4,3]]_3` logical space is the
Steinberg module, and BT863 proved that its character vanishes on every
nonidentity element of these 3-groups. BT865 joins those facts at module
level and at chain level.

## The dual regular-restriction theorem

For either canonical order-27 subgroup `O3`,

```text
St restricted to O3 = 3 Reg(O3)                  over C,
H1(F3) restricted to O3 = F3[O3] + F3[O3] + F3[O3].
```

The complex statement follows from the exact restricted character
`{81: 1, 0: 26}`. The native-field statement was not assumed: the verifier
constructs three cycle seeds for each torsor, translates each seed by all
27 group elements, and checks that the three orbit spans contribute
`27+27+27=81` independent homology classes modulo the 120-dimensional
boundary space.

Thus the protected memory is simultaneously:

- three complete copies of the **flat 3-trit program-address space**; and
- three complete copies of the **noncommutative Heisenberg state space**.

They are two exact coordinate systems on the same logical register. This is
the algebraic state/program compiler promised by the architecture: program
contexts translate through `F3^3`, while quantum state phases translate
through `H27`.

## The Heisenberg center selects triality

BT863 showed that every order-3 element produces a complex eigensplit
`27+27+27`, but left open which triality is structurally distinguished.
The point-shell torsor supplies the answer: `H27` has a unique center

```text
Z(H27) = C3.
```

For a generator `z` of that center, the three complex central-character
blocks have dimensions `27,27,27`:

| central character | content inside `3 Reg(H27)` | dimension |
| --- | --- | ---: |
| `1` | nine linear characters, each with multiplicity 3 | 27 |
| `omega` | the 3-dimensional Schrodinger irrep with multiplicity 9 | 27 |
| `omega^2` | its conjugate, with multiplicity 9 | 27 |

This does more than count generations. It interprets one generation as the
center-trivial sector and the other two as the conjugate noncommutative
qutrit-phase sectors. The selection is canonical after choosing the point
shell because the center is characteristic in `H27`; no individual
direction is characteristic in the elementary group `F3^3`.

## The native-field generation flag

Over the code field `F3`, the polynomial `x^3-1` becomes `(x-1)^3`, so the
three complex phases do **not** remain three eigenspaces. They coalesce into
a length-three unipotent memory stack. For `N=z-I` acting on `H1(F3)`, BT865
computes exactly

```text
rank(N), rank(N^2), rank(N^3) = 54, 27, 0.
```

Therefore

```text
0 < ker(N) < ker(N^2) < H1(F3)
    27         54          81
```

has three successive 27-dimensional quotients. Equivalently, the center
acts through 27 Jordan blocks of size 3. The same generation structure has
two mathematically correct forms:

- over `C`: three phase sectors `1, omega, omega^2`;
- over `F3`: three successive layers of a nilpotent filtration.

All 13 projective `C3` directions in each order-27 torsor have this
`54,27,0` Jordan profile. The Heisenberg center is special not because its
local rank data differ, but because it is the unique direction preserved by
every automorphism of the curved state torsor.

## Architecture reading

```text
Bell-shell program coordinates       point-shell state coordinates
F3^3                                 H27 = 3^(1+2)
  |                                    |
  |  three regular copies             |  three regular copies
  +---------------- H1(F3) ------------+
                    81 logical qutrits
                         |
                Z(H27) = C3 triality
                         |
              27 < 54 < 81 memory flag
```

The compiler is not a numerical analogy. It is an explicit pair of free
module structures on the same homology group. A packet can be addressed in
the commuting Bell-shell coordinates, represented in the noncommuting
Heisenberg coordinates, and stored in the Steinberg-protected code without
changing its 81-dimensional carrier.

## Boundary

`H27` and `F3^3` are not isomorphic. BT865 does not claim a canonical
intertwiner between their regular bases. The verifier proves that both are
free rank-3 coordinatizations of `H1(F3)` and exhibits deterministic bases;
the basis-to-basis matrix still depends on the chosen point, line, shell
origins, and cycle seeds. Determining whether the global W33 incidence
geometry removes those choices is the next compiler problem.
