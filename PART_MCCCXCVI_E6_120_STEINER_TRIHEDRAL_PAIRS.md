# Part MCCCXCVI: E6 120 Steiner Trihedral Pairs

## Claim Boundary

MCCCXCVI is a finite cubic-surface incidence theorem on the W33-derived `E6`
matter charts.  It reconstructs the 120 Steiner trihedral-pair layer from the
finite double-six and tritangent data.

It does not assert a continuum surface equation.

## Input

Earlier parts reconstructed the finite cubic-surface stack:

```text
MCCCXCI: 45 zero-sum tritangent triples
MCCCXCII: 36 double-sixes
MCCCXCV: 51840 scheme automorphism order
```

## Construction

A finite Steiner trihedral-pair witness is defined as a triple of double-sixes
with:

```text
pairwise double-six overlaps = (6,6,6)
triple intersection = empty
union size = 18
complement size = 9
```

The complementary 9 weights must contain exactly six zero-sum tritangent
triples.  Those six tritangents must split uniquely into two trihedra, each
made from three disjoint tritangent triples covering the same 9 weights.

## Result

For every one of the eight W33-derived `E6` matter charts, the verifier finds:

```text
Steiner trihedral-pair witnesses = 120
```

and checks:

```text
each witness uses 3 double-sixes;
each complement has 9 weights;
each complement contains exactly 6 tritangents;
each complement has exactly 1 pair of complementary trihedra;
each overlap-6 double-six pair lies in exactly 1 witness.
```

The incidence profiles are exact:

```text
each weight lies in 40 trihedral pairs;
each tritangent lies in 16 trihedral pairs;
each double-six lies in 10 trihedral pairs.
```

## Reading

The `E6` matter chart now reconstructs the classical cubic-surface count:

```text
120 Steiner trihedral pairs.
```

The important W33 signal is the participation number:

```text
each of the 27 matter weights lies in 40 trihedral pairs.
```

So the W33 vertex count `40` appears here not as the number of trihedral pairs,
but as the exact incidence multiplicity through each `E6` matter weight.

## Artifacts

- Analysis: `analysis/w33_e6_120_steiner_trihedral_pairs.py`
- Tests: `tests/test_w33_e6_120_steiner_trihedral_pairs.py`
- Result: `PART_MCCCXCVI_E6_120_STEINER_TRIHEDRAL_PAIRS_results.json`
