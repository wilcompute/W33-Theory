# Passes 7033–7040 — CE2 normal form is compressed, not yet blind

## Executive result

The requested no-answer-table replay does **not** currently close.

This is not because the CE2 structure is empty.  The repo has a substantial Heisenberg/metaplectic compression of the simple-family repair law.  The problem is stronger and more specific: the current source still uses the target answers inside the path advertised as a normal-form derivation, and several of its closed-form correction coefficients are explicitly documented as fits to the full 864-entry sign dataset.

The correct present status is therefore

\[
\boxed{\text{STRUCTURAL COMPRESSION VERIFIED; INDEPENDENT BLIND DERIVATION OPEN}.}
\]

## Pass7033 — runtime blindness and provenance blindness are different

A strict replay needs two independent conditions.

**Runtime blind:** while predictions are being produced, no target answer table or answer-derived lookup is read.

**Provenance blind:** none of the coefficients/rules used by the predictor were themselves fitted or selected using the target answers.

A predictor can satisfy the first while failing the second.  That distinction matters here.

## Pass7034 — the current “normal-form” table builder reads the answer map

In `scripts/ce2_global_cocycle.py`, `_derive_tables_via_normal_form()` says in its docstring that it is a table-free algebraic construction, but the implementation then explicitly iterates over

```python
_simple_family_sign_map().items()
```

to build the constant-line tables.

Its own explanatory text states that it “uses the *actual* sign map” for the final fitting.

Therefore the current implementation is not runtime blind.

## Pass7035 — even the “naive” domain enumeration reads target keys

`_derive_naive_tables()` avoids using the target *values* for its reconstructed sign, but it still loops over

```python
_simple_family_sign_map().keys()
```

so the domain being replayed is supplied by the answer artifact rather than independently enumerated from the Heisenberg/E6 conditions.

This is weaker leakage than reading values, but a strict blind replay must remove it too.

## Pass7036 — the delta law is fitted provenance

The strongest obstruction is recorded directly in the source comments.  The delta polynomials are described as having been obtained by solving over the full 864-entry dataset, and the coefficient table is described as “computed once by fitting the actual deltas for all 864 CE2 entries.”

Consequently the current delta law is a compact closed form for the observed data, but it is not yet an independent consequence of the metaplectic/Heisenberg action.

That is a valuable distinction: compression is real mathematics, but compression is not the same certificate as derivation.

## Pass7037 — what does survive independently

Several components are genuinely structural:

- the 27-point affine-Heisenberg coordinate system;
- symplectic directions in `F_3^2`;
- the metaplectic cochain machinery;
- the side/support rule for the dominant simple family;
- the seed-frame transport construction;
- the explicit fiber-family geometry and its separate closed rules.

These explain a large amount of the 5832-row table and strongly constrain the final law.  The audit does **not** demote those results.

## Pass7038 — what an actual blind certificate must do

A conclusive replay should proceed in this order:

1. derive the seed polynomial coefficients directly from the E6/Heisenberg bracket or CE differential;
2. derive the delta correction from the group/cochain law, not a fit;
3. enumerate the full simple-family domain from the structural conditions, without reading answer keys;
4. generate every predicted sparse row and freeze a hash;
5. only after the hash is frozen, open `committed_artifacts/ce2_sparse_local_solutions.json` and compare all rows.

That procedure would separate theorem construction from theorem checking.

## Pass7039 — the 5832-row artifact remains evidence

Nothing in this audit says the committed sparse local solutions are synthetic.  The earlier provenance packet already separated the genuine native `27 x 3` CE2 carrier from the later synthetic 40-label orbit wrappers.

The current conclusion is narrower:

\[
\boxed{\text{the native table is real evidence, but the global closed form is not yet independently derived from it}.}
\]

## Pass7040 — boundary

This packet refutes only the phrase “no-answer-table derivation” for the current implementation.  It does not refute the existing predictor's agreement with its source data, the Heisenberg support laws, or the possibility that the fitted delta polynomial admits a short algebraic proof.

The next meaningful CE2 breakthrough is therefore not another fit.  It is a derivation of the correction law from the actual bracket/cochain structure.
