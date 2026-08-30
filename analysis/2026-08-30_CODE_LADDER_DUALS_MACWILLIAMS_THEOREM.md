# Adjacency-sentinel code ladder under duality

Let `C_S` be the sentinel `[40,15,8]_2` code and `C_A` the W33 adjacency-row code. The previous line-parity theorem gives `C_S < C_A` with quotient `C2`. The exact continuation audit closes the full primal and dual weight theory.

Primal parameters and enumerators:

- `C_S = [40,15,8]_2` with weights `0,8,12,16,20,24,28,32,40` and multiplicities `1,45,720,6930,17376,6930,720,45,1`.
- `C_A = [40,16,8]_2`, self-orthogonal, with multiplicities `1,45,1120,15570,32064,15570,1120,45,1` at the same weights.
- The unique nonzero coset `C_A \ C_S` has enumerator `400 z^12 + 8640 z^16 + 14688 z^20 + 8640 z^24 + 400 z^28`. Thus the extension adds no new minimum words: both primal codes have exactly the same 45 weight-eight sentinel minima.

MacWilliams duality gives:

- `C_A^perp = [40,24,6]_2`;
- `C_S^perp = [40,25,4]_2`;
- `C_S^perp/C_A^perp ~= C2`.

The dual extension is geometric, not merely enumerative. The 40 W33 line indicators have rank 25 and are exactly the 40 weight-four words of `C_S^perp`, so `C_S^perp` is precisely the binary W33 line code. Differences of line indicators have rank 24 and span `C_A^perp`. Its 240 minimum weight-six words are exactly the symmetric differences of intersecting W33 line pairs.

Thus duality turns the primal universal line-parity character into the literal line-code extension

`line-difference code [40,24,6] < line code [40,25,4]`.

Reproducibility:
- `analysis/w33_20260830_code_ladder_duals_macwilliams.py`
- `data/PART_W33_20260830_CODE_LADDER_DUALS_MACWILLIAMS.json`
- exact-continuation run `33337524115` passed.

Boundary: these are exact binary-code and finite-geometry identities; distance alone is not a hardware error-rate claim.
