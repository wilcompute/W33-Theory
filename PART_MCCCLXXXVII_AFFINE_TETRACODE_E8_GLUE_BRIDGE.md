# Part MCCCLXXXVII: Affine Tetracode E8 Glue Bridge

## Claim Boundary

MCCCLXXXVII is a finite incidence theorem inside W33.  It identifies the
standard tetracode glue pattern required by the known `A2^4 + tetracode`
construction of the `E8` lattice.  It does not by itself choose a continuum
metric scale.

## Input

MCCCLXXXVI found the rank-8 contrast skeleton:

```text
adjacent E6 triplet sums -> line-wise ternary contrasts -> A2^4 rank 8.
```

The missing question was whether W33 also supplies the glue code that turns
`A2^4` into `E8`.

## Construction

Fix a W33 point `p`.  There are four lines through `p`.  If `x` is a
nonneighbor of `p`, then the generalized-quadrangle axiom gives exactly one
common neighbor of `p` and `x` on each of those four lines.

Label the three non-`p` points on each anchor line by `0,1,2`.  The nonneighbor
`x` therefore determines a length-4 ternary word.

## Result

The 27 nonneighbors of `p` collapse to 9 unique words, each with multiplicity 3.
Those 9 words form the ternary tetracode:

```text
generators = (1,0,1,2), (0,1,1,1)
rank       = 2
length     = 4
size       = 9
minimum weight = 3
weight profile = {0:1, 3:8}
self-dual over F3 = true
```

This holds for all 40 choices of anchor point.

## E8 Reading

The standard tetracode construction of `E8` starts from four `A2` coordinate
planes and glues them by the ternary tetracode.  W33 now supplies both pieces:

```text
MCCCLXXXVI: A2^4 rank-8 contrast skeleton
MCCCLXXXVII: tetracode glue from the affine nonneighbor cloud
```

The root count closes exactly:

```text
240 = 4*6 + 8*27.
```

Here `4*6 = 24` is the `A2^4` root subsystem, and `8*27 = 216` is the eight
nonzero tetracode words lifted by the 27 ternary phase choices.

## Verification

The verifier checks:

```text
all 40 anchors have rank-2 code profile;
all 40 anchors have 9 unique codewords;
all codewords appear with multiplicity 3;
all 40 anchor codes are self-dual [4,2,3]_3 tetracodes;
the E8 root count is 240 = 4*6 + 8*27.
```

## Artifacts

- Analysis: `analysis/w33_affine_tetracode_e8_glue_bridge.py`
- Tests: `tests/test_w33_affine_tetracode_e8_glue_bridge.py`
- Result: `PART_MCCCLXXXVII_AFFINE_TETRACODE_E8_GLUE_BRIDGE_results.json`
