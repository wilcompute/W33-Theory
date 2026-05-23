# Part MCCVIII: r=3 Face-Code Rate Law

## Claim Boundary

MCCVIII is a finite rate theorem for the face-code packet induced by the
established K12 orientable horizon surface. It does not claim a completed
minimum-distance proof.

## Statement

From MCXCII:

```text
F = 44,
genus = 6.
```

Define face-code packet:

```text
[n_face, k_face, *]_3 = [50, 44, *]_3,
n_face = F + genus = 50,
k_face = F = 44.
```

So the rate is:

```text
R_face = 44/50 = 22/25.
```

Universal 56-form identity (k=12):

```text
56 = C(k,2)-k+2,
R_face = (56-k)/(56-k/2) = (56-12)/(56-6) = 44/50 = 22/25.
```

## Open Boundary (explicit)

The rate is fixed exactly; explicit constructive proof of minimum distance
`d=3` for `[50,44,d]_3` remains open.

## Artifacts

- Analysis: `analysis/w33_r3_face_code_rate.py`
- Tests: `tests/test_w33_r3_face_code_rate.py`
- Result: `PART_MCCVIII_R3_FACE_CODE_RATE_results.json`
