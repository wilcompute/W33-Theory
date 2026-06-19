# BT1344 -- Q4 Quotient Canonicalization Audit

## Purpose

BT1344 canonicalizes the BT1341 [[32,4,4]] gauge quotient under the full automorphism group of the 4-cube.

## Automorphism group

The Q4 cube automorphism group has order:

```text
2^4 * 4! = 384
```

The script applies all 384 signed coordinate permutations to the quotient subspace.

## Result

The BT1341 quotient has:

```text
orbit size = 384
stabilizer size = 1
```

So the quotient is valid but generic under the full Q4 cube symmetry.

Canonical orbit representative, recorded as the full 16-element quotient span
rather than a noncanonical choice of four basis rows:

```text
0x0
0x23
0x1ec9
0x1eea
0x2c96
0x2cb5
0x325f
0x327c
0x4984
0x49a7
0x574d
0x576e
0x6512
0x6531
0x7bdb
0x7bf8
```

## Interpretation

BT1341 solves the code-parameter problem. BT1344 shows that this solution is not yet the most geometrically natural or symmetric solution. The next refinement is to search for a quotient that is invariant under a meaningful Q4/W33/heptad subgroup.

## Files

```text
tools/bt1344_canonicalize_q4_quotient.py
data/bt1344_q4_quotient_canonicalization.json
```
