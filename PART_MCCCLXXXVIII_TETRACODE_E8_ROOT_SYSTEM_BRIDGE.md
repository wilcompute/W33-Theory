# Part MCCCLXXXVIII: Tetracode E8 Root System Bridge

## Claim Boundary

MCCCLXXXVIII is an exact finite root-system theorem.  It starts from the
W33-derived tetracode of MCCCLXXXVII and applies the standard four-`A2`
Eisenstein/tetracode lift.  It proves that this lift is the `E8` root system.

This does not by itself assert a continuum physical gauge group.  It supplies
the exact finite `E8` root witness needed by the later identification bridge.

## Input

MCCCLXXXVII proved that the 27 nonneighbors of any W33 anchor point, read
through the four anchor lines, give the ternary tetracode:

```text
[4,2,3]_3
generators = (0,1,1,1), (1,0,1,2)
weight profile = {0:1, 3:8}
self-dual over F3 = true
```

MCCCLXXXVI supplied the companion rank-8 skeleton: four `A2` contrast planes.

## Construction

Work in four `A2` simple-root coordinate blocks.  The `A2` roots contribute

```text
4 * 6 = 24
```

roots.  For each nonzero tetracode word, lift every nonzero coordinate to one
of the three minimal representatives in its corresponding nonzero coset of
`A2^*/A2`.  Since each nonzero tetracode word has weight 3, each word has

```text
3^3 = 27
```

phase lifts.  The eight nonzero tetracode words therefore contribute

```text
8 * 27 = 216
```

glue roots.

The total is

```text
24 + 216 = 240.
```

## Result

The verifier constructs the 240 vectors exactly over rational numbers and
checks:

```text
unique roots = 240
rank = 8
norm profile = {2:240}
source profile = {A2:24, tetracode_glue:216}
```

Every root has the `E8` local inner-product profile:

```text
{-2:1, -1:56, 0:126, 1:56, 2:1}.
```

The ordered pair profile is:

```text
{-2:240, -1:13440, 0:30240, 1:13440, 2:240}.
```

## Simple Roots

A regular chamber extraction gives 8 simple roots.  Their Gram matrix has:

```text
determinant = 1
off-diagonal entries in {0,-1}
Dynkin edge count = 7
Dynkin degree profile = {1:3, 2:4, 3:1}
connected = true
```

That is the `E8` Dynkin tree profile.

## Reflection Closure

For every pair of roots `alpha, beta`, the root reflection

```text
beta -> beta - (beta, alpha) alpha
```

lands back in the 240-vector set.  The failure count is exactly zero.

## Reading

The previous theorem found the glue code.  This theorem confirms the whole
finite object:

```text
W33 affine tetracode
  + MCCCLXXXVI A2^4 rank-8 contrast skeleton
  -> exact E8 root system.
```

So the bridge has moved from a count match to a verified root system.

## Artifacts

- Analysis: `analysis/w33_tetracode_e8_root_system_bridge.py`
- Tests: `tests/test_w33_tetracode_e8_root_system_bridge.py`
- Result: `PART_MCCCLXXXVIII_TETRACODE_E8_ROOT_SYSTEM_BRIDGE_results.json`
