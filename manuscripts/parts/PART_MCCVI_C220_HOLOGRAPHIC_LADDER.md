# Part MCCVI: C220 Holographic Ladder Law

## Claim Boundary

MCCVI is a finite combinatorial packet extracted from established counts. It is
not a full continuum holographic derivation.

## Statement

The rank-3 channel of `k=12` is

```text
C(12,3) = 220.
```

With `q=3`, `d_Z=4`:

```text
220/81 = C(12,3)/3^4.
```

This equals the enhancement factor already established in MCCV:

```text
R_boundary / R_bulk = 220/81.
```

Also:

```text
dim(Sym^2(C^11)) = C(12,2) = 66 (not 220).
```

So the correct `220` source is the `r=3` combinatorial channel, not the Sym²
channel.

## Ladder (k=12)

```text
C(12,1)=12,
C(12,2)=66,
C(12,3)=220,
C(12,4)=495,
C(12,5)=792,
C(12,6)=924.
```

## Artifacts

- Analysis: `analysis/w33_c220_holographic_ladder.py`
- Tests: `tests/test_w33_c220_holographic_ladder.py`
- Result: `PART_MCCVI_C220_HOLOGRAPHIC_LADDER_results.json`
