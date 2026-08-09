# Part MCCCLXXXVI: E6 Triality Contrast Rank-8 Bridge

## Claim Boundary

MCCCLXXXVI is a finite spectral quotient theorem inside the W33 corner
scheme.  It identifies a canonical rank-8 quotient of the adjacent E6 packet.
It does not yet claim a continuum E8 lattice embedding.

## Input Frontier

MCCXLV proved the flag-anchored split

```text
240 = 6 A2 singletons + 24 adjacent/E6 triplets + 27 + 27 matter triplets.
```

It also proved that the naive A2-triplet-sum quotient does **not** collapse the
golden 24D frame to rank 8.  That left the triality quotient open.

## New Result

Fix a W33 point `p`.  The adjacent E6 packet has the internal shape

```text
4 lines through p
× 3 other points on each line
× 2 local triplet types (through / away)
× 3 corners per triplet
= 72 adjacent corners.
```

After summing each local A2 triplet in the golden 24D eigenspace, the raw
adjacent packet has rank

```text
rank(raw 24 triplet sums) = 12.
```

Now take the two independent ternary point contrasts on each of the four lines.
Using the through-plus-away vector at each adjacent point gives exactly

```text
4 lines × 2 contrasts = 8 vectors,
rank = 8.
```

The Gram spectrum is clean:

```text
G_sum spectrum = {3/2 with multiplicity 4, 9/2 with multiplicity 4}.
```

The complementary through-minus-away quotient is also rank 8:

```text
G_diff spectrum = {3/10 with multiplicity 4, 9/10 with multiplicity 4},
G_sum = 5 G_diff.
```

The through-only and away-only contrast quotients carry the golden split:

```text
G_away = phi^4 G_through.
```

## Reading

The missing rank-8 bridge is not the naive collapse of all A2 triplets.  It is
the ternary **line-contrast quotient** of the adjacent E6 packet:

```text
adjacent E6 triplets -> line-wise ternary contrasts -> rank 8.
```

This is the first exact rank-8 projection found inside the MCCXLV matter-chart
frontier.  It says the rank reduction lives in the adjacent E6 contrast layer,
not in the 81-sector matter coordinate charts themselves.

## Verification

The verifier checks all 40 W33 anchor points:

```text
raw adjacent E6 triplet-sum rank profile = {12: 40}
through contrast rank profile            = {8: 40}
away contrast rank profile               = {8: 40}
pair-sum contrast rank profile           = {8: 40}
pair-diff contrast rank profile          = {8: 40}
```

## Artifacts

- Analysis: `analysis/w33_e6_triality_contrast_rank8_bridge.py`
- Tests: `tests/test_w33_e6_triality_contrast_rank8_bridge.py`
- Result: `PART_MCCCLXXXVI_E6_TRIALITY_CONTRAST_RANK8_BRIDGE_results.json`
