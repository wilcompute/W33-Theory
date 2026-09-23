# Affine-holonomy virtual-machine code architecture

The ramified Cartan-cubic code is more than a list of parameters.  Its exact
generator can be placed in the form

```text
G45 = [2 A | I12 tensor (1,1,1)],
```

where `A` is the 12-line by 9-point incidence matrix of `AG(2,3)`.  This gives
a literal finite-machine encoder:

- 12 logical trits, one for each affine line / ramified Fourier fiber;
- 36 payload trits, three identical copies of each logical trit;
- 9 holonomy-check trits, one for each affine point;
- encoding `c -> (2cA, c tensor (1,1,1))`.

Every codeword obeys

```text
wt(cG45) = 3 wt(c) + wt(cA).
```

The full code is `[45,12,6]_3`, so it corrects two arbitrary trit errors and
detects five in the algebraic Hamming model.  Retaining one coordinate from
each private triple gives the systematic core

```text
G21 = [2 A | I12],   [21,12,4]_3,
```

which corrects one and detects three.  Exhaustive `3^12` enumeration freezes
both complete weight enumerators.

The dual is `[45,33,2]_3`.  Its 72 weight-two words are exactly the two
nonzero scalar multiples of each pair-difference inside the twelve private
triples.  These local equality checks span dimension 24.  The remaining nine
dual dimensions are the global affine point-holonomy checks.  Thus the
parity-check architecture splits exactly as

```text
33 = 24 local repetition checks + 9 global affine checks.
```

The code's Euclidean hull has dimension nine because the generator Gram has
rank three.

The minimum shell determines the complete permutation symmetry.  A fiber
coordinate occurs in four of the twelve minimum supports, while a private
coordinate occurs in one, so every code automorphism preserves the `9+36`
split.  The induced incidence on the nine coordinates is all of `AG(2,3)`.
Exhausting all `9!` point permutations leaves exactly 432, equal to
`AGL(2,3)`.  Each private triple may then be permuted independently.  Hence

```text
Aut_perm(C) = S3^12 : AGL(2,3),
|Aut_perm(C)| = 6^12 * 432 = 940,369,969,152.
```

This is a classical ternary encoder/checker derived from the finite compiler.
The Hamming guarantees are not a hardware threshold or stochastic noise
model, and the construction is not by itself a quantum code.

Evidence:

- `analysis/w33_affine_holonomy_vm_code_architecture.py`
- `data/w33_affine_holonomy_vm_code_architecture.json`
- `tests/test_w33_affine_holonomy_vm_code_architecture.py`
