# Part MCCCXCVII: E6 240 Steiner Trihedra / E8 Count

## Claim Boundary

MCCCXCVII is a finite `E6` cubic-surface incidence theorem on the W33-derived
matter charts.

It proves a count resonance:

```text
120 Steiner trihedral pairs -> 240 individual Steiner trihedra
240 = E8 root count = W33 oriented-corner count
```

It does not identify these finite trihedra with continuum `E8` roots.

## Input

MCCCXCVI reconstructed the 120 finite Steiner trihedral pairs in each `E6`
matter chart.  Each pair is made of two complementary trihedra.  Each trihedron
is three disjoint zero-sum tritangent triples covering the same 9 matter
weights as its partner.

## Construction

For every MCCCXCVI witness:

```text
contained tritangents = 6
unique partition = two trihedra
trihedron = 3 disjoint tritangents
trihedron cover = 9 weights
```

The verifier forgets the pair container, deduplicates the individual trihedra,
and then rebuilds the partner relation from the shared 9-weight cover.

## Result

For every one of the eight W33-derived `E6` matter charts, the verifier finds:

```text
individual Steiner trihedra = 240
partner pairs by common 9-weight cover = 120
```

The incidence profiles are exact:

```text
each trihedron uses 3 tritangents;
each trihedron covers 9 weights;
each trihedron has exactly 1 partner;
partners share 0 tritangents;
each tritangent lies in 16 trihedra;
each weight lies in 80 trihedra.
```

The pairwise trihedron overlap spectra are also exact:

```text
tritangent-overlap profile:
  0 shared tritangents: 23280 pairs
  1 shared tritangent:   5400 pairs

weight-intersection profile:
  0 shared weights:    480 pairs
  2 shared weights:  12960 pairs
  3 shared weights:   8640 pairs
  5 shared weights:   6480 pairs
  9 shared weights:    120 pairs
```

## Reading

The previous layer proved the `120` pair count.  This layer proves that the
underlying object carrier has `240` individual trihedra, exactly matching the
`E8` root count and the W33 oriented-corner count.

The important point is not merely numerology.  The `240` objects come with a
fully checked incidence structure:

```text
240 trihedra x 9 weights = 2160 = 27 weights x 80 trihedra;
240 trihedra x 3 tritangents = 720 = 45 tritangents x 16 trihedra.
```

So the finite cubic-surface stack now contains a verified 240-shell:

```text
27 matter weights
45 zero-sum tritangents
36 double-sixes
120 Steiner trihedral pairs
240 individual Steiner trihedra
```

That gives the W33/E6 side an internal 240-object carrier before any continuum
`E8` interpretation is made.

## Artifacts

- Analysis: `analysis/w33_e6_240_steiner_trihedra_e8_count.py`
- Tests: `tests/test_w33_e6_240_steiner_trihedra_e8_count.py`
- Result: `PART_MCCCXCVII_E6_240_STEINER_TRIHEDRA_E8_COUNT_results.json`
