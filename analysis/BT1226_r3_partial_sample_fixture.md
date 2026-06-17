# BT1226 -- R3 Partial Sample Fixture

## Purpose

BT1223 created the sample-status validator. BT1226 creates the first fixture for the middle lane:

```text
partial
```

This is stronger than the BT1220 mock sequence but still not a final evidence candidate.

## Fixture

The fixture is

```text
k3_partial_refinement_n32_v1
```

with

\[
h=0.03125,
\qquad
\text{shape quality}=0.99375.
\]

It includes:

- K3 topology \(\chi=24,\sigma=-16,b_2=22,(b_2^+,b_2^-)=(3,19)\),
- nonempty operator sample of size 8,
- non-null \(A_4\),
- non-null refinement scale \(h\),
- partial claim status.

## Status

The expected validator level is

```text
partial
```

and candidate promotion is still disallowed.

## Why this matters

The R3 evidence pipeline now has all three lanes represented:

\[
\text{blocked mock sequence}
\to
\text{partial computed fixture}
\to
\text{future candidate evidence}.
\]

## Files

- Code: `analysis/bt1226_r3_partial_sample_fixture.py`
- Result: `data/bt1226_r3_partial_sample_fixture_summary.json`

## Boundary

BT1226 is not physical R3 evidence. It tests the validator's middle lane and records exactly what remains missing: independent metric/operator certification.
