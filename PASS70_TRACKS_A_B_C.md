# Pass 70 Tracks A-C

This packet materializes three legacy Pass 70 tracks as repository files. Its
claims are scoped to what the scripts actually construct.

## Files

- `w33_pass70_trackA_ramanujan.py` computes the explicit Ramanujan-bound excess
  for the stated eigenvalue `(1+sqrt(97))/2`.
- `w33_pass70_trackB_qec.py` records a 360-dimensional spectral multiplicity
  ledger. It does **not** construct a stabilizer code.
- `w33_pass70_trackC_partition.py` computes the stated critical inverse
  temperature and holographic-threshold quantities.

## Track B correction

The ledger identity is

```text
360 = 1 + 40 + 9 + 15 + 15 + 15 + 15 + 250.
```

That identity does not provide parity-check matrices, prove a CSS commutation
relation, identify a logical space, or compute distance. The former
`[[360,9,9]]` line is therefore withdrawn. The tracked JSON also once contained
`[[360,9,1]]`, while the script's literal ceiling ratio is
`ceil(360/250)=2`; none of `9`, `1`, or `2` is a certified code distance here.
Passes 343 and 345 preserve the exact obstruction and correction ledger.

## Outputs

Running the scripts writes:

- `w33_pass70_trackA_ramanujan.json`
- `w33_pass70_trackB_qec.json`
- `w33_pass70_trackC_partition.json`

The prior Pass 69 file already present in the repository is
`w33_pass69_track1_ihara_zeta.py`.
