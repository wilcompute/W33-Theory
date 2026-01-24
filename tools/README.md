# W33 tooling

## Verify the rigorous kernel (Sections 3–7)

Runs consistency checks directly against the artifact bundles (`*.zip`) in the repo root:

```bash
python3 tools/verify_w33_kernel.py
```

This verifies (among other things):
- `W33` is `SRG(40,12,2,4)` with spectrum `12^1, 2^24, (-4)^15`
- `A^2 ≡ 0 (mod 2)` and `rank_GF2(A)=16`
- the GF(2) kernel code has dimension 24 and the 240 weight‑6 generators span it
- `H=ker(A)/im(A)` has dimension 8 with a quadratic form splitting nonzero vectors into orbits `135/120`
- the 120‑root graph is `SRG(120,56,28,24)`
- gauge‑fixing removes all 16‑weight defects and yields 40 disjoint “flat triples”
- the quotient graph is `overline(W33)` and identity‑holonomy triangles match the 90 non‑isotropic PG(3,3) lines

## Audit the “prediction” numerology in `W33_FORMAL_THEORY.pdf`

Compares the formulas to the experimental values **as quoted in the PDF**:

```bash
python3 tools/audit_formal_theory_predictions.py
```

Notes:
- Many of these quantities are scheme/scale dependent (e.g., `α`, `sin²θW`), so this is a bookkeeping check, not a physics validation.

## Holonomy vs. symplectic phase (Section 10)

Builds `W33_holonomy_phase_decomposition_bundle.zip` from the existing bundles:

```bash
python3 tools/build_holonomy_phase_decomposition_bundle.py
```

## Holonomy as an S3 gauge field (recommended)

Builds `W33_holonomy_s3_gauge_bundle.zip`, showing:
- edge-parity `Z2` cocycle `s` is exact (`s=dt`)
- transported Bianchi identity `d_s F ≡ 0`
- gauge-fixed `F^(t)` is an ordinary cocycle and admits an edge potential `A` with `dA=F^(t)`

```bash
python3 tools/build_holonomy_s3_gauge_bundle.py
```

## Naive dF → H^3 → 90-line weights (sanity check)

Builds `W33_charge_to_line_weights_bundle.zip`, projecting the naive untwisted tetrahedra flux
`J := dF` into:
- `H^3` coordinates (dim 89 over `Z3`)
- the 88D core / 90-line-weight model

Because `J=dF` is a coboundary of a global triangle cochain, its `H^3` class is necessarily zero;
the bundle makes that explicit and includes an example nonzero `H^3` basis element for comparison.

```bash
python3 tools/build_charge_to_line_weights_bundle.py
```

## 90-line association scheme: spectral decomposition

Builds `W33_nonisotropic_line_scheme_spectral_bundle.zip`, computing the primitive idempotents / eigenmatrices
for the Aut(W33)-invariant 5D commutant algebra acting on the 90 non-isotropic lines:

```bash
python3 tools/build_noniso_line_scheme_spectral_bundle.py
```

Optional: if you have two 90-entry CSV vectors (indexed by `line_id`) you want to compare (e.g. `z` and `m`),
you can pass them to fit an invariant operator `D = Σ a_i B_i` in the scheme algebra:

```bash
python3 tools/build_noniso_line_scheme_spectral_bundle.py --z-csv path/to/z.csv --m-csv path/to/m.csv
```

## Bulk → vacuum mode-response table (tetrahedra orbits)

Builds `W33_mode_response_table_bulk_to_vacuum_bundle.zip`, decomposing the 9450 quotient tetrahedra
into Aut(W33)-orbits and reporting how the signed flux `J := dF` injects into the 5 vacuum modes via:
- `m_line`: flat-face (line-face) boundary moment
- `z_line`: curved-face edge-shadow (edge → nonisotropic line)

```bash
python3 tools/build_mode_response_table_bulk_to_vacuum_bundle.py
```

## Transfer operators `M` and `Z` (explicit COO)

Builds `W33_transfer_operators_J_to_lines_and_mode_injection_bundle.zip`, constructing the explicit sparse
transfer operators from tetra flux `J := dF` (9450 tetrahedra) to the two 90-line observables:
- `M J` = boundary moment (`m_line`)
- `Z J` = bulk shadow (`z_line`)

```bash
python3 tools/build_transfer_operators_J_to_lines_and_mode_injection_bundle.py
```

## Charge decomposition + line moments

Builds `W33_charge_decomposition_and_line_moments_bundle.zip`, summarizing support of `J := dF` on tetrahedra,
its split by (bulk/boundary/vacuum) flat-face-count orbit type, plus pointwise incidence and boundary line moments.

```bash
python3 tools/build_charge_decomposition_and_line_moments_bundle.py
```

## Curved-triangle operator chain (`C_lineface`, `K0/K1`, `R`)

Builds three bundles used by the complete draft’s field-equation layer:
- `W33_current_operator_C_lineface_bundle.zip`
- `W33_bulk_operator_K0K1_curved_triangle_current_bundle.zip`
- `W33_curved_triangle_to_noniso_line_operator_R_bundle.zip`

```bash
python3 tools/build_operator_chain_Clineface_K0K1_R_bundles.py
```
