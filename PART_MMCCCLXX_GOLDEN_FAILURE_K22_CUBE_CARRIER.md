# Part MMCCCLXX: Golden Failure K2,2 x F3^3 Carrier

## Claim

The `108` unique golden-selector failures decompose structurally as

```text
K2,2 x F3^3 = 4 * 27 = 108 = mu*q^3.
```

After the eight ordered orientations, this becomes

```text
2^q * K2,2 * F3^3 = 8 * 108 = 864.
```

## Carrier Structure

In the draft selector gauge, every unique failed quadrangle contains one anchor
line. The four points on that line split into two inactive matched pairs:

```text
inactive: (0,1), (2,3)
active:   (0,2), (0,3), (1,2), (1,3)
```

Thus the failures occur on the `K2,2` cross-pairs between the two halves of the
anchor line. Each active pair carries exactly `27 = 3^3` failures.

For each active pair:

- there are `3` off-anchor lines through the first endpoint;
- there are `3` off-anchor lines through the second endpoint;
- every endpoint-line pair contributes exactly `3` bridge choices.

That gives the exact local cube:

```text
3 endpoint lines x 3 endpoint lines x 3 bridges = 27 failures.
```

## Global Profiles

- The anchor line occurs in all `108` unique failures.
- The `12` endpoint lines each occur `18` times.
- The `27` bridge lines each occur `4` times.
- The `4` anchor points each occur `54` times.
- The `36` non-anchor points each occur `6 = 3!` times.

## Boundary

This explains the internal carrier of the golden-selector obstruction. It does
not yet identify these four ternary cubes with explicit `O^-(6,2)/A5` cosets.
That coset bijection remains the next selector target.

## Verification

Run:

```bash
python3 analysis/w33_golden_failure_k22_cube_carrier.py
```

Expected result: `12/12` checks verified.
