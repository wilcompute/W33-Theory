# W33-Theory audit: May 16, 2026

## Summary

This audit was produced after reviewing the May 16, 2026 commit stream and the public-facing theory files `w33_paper.tex`, `single_photon_universal_computation.tex`, and `docs/index.html` through the GitHub connector and raw repository views. The key result is not a new speculative layer; it is a reproducibility hardening pass.

The core W(3,3) graph survives independent reconstruction cleanly:

- 40 projective points in `PG(3,3)`
- 240 symplectic-orthogonality edges
- regular degree 12
- strongly regular parameters `(40,12,2,4)`
- adjacency spectrum `{12^1, 2^24, (-4)^15}`

That confirms the finite-geometry seed. The next credibility step is enforcing consistency across all formula claims derived from the seed.

## Main finding

The project is strong where it is graph-theoretic and finite-geometric, but the public artifacts currently show formula drift in at least two visible places:

1. fine-structure constant expressions, and
2. Weinberg-angle normalizations.

For a zero-free-parameter theorem, this must be surfaced in CI rather than left in prose.

## Files added in this pass

- `scripts/reproduce_w33_core.py`
- `tests/test_reproduce_w33_core.py`
- `docs/consistency_notes.md`
- `reports/2026-05-16_repo_audit.md`

## What the script checks

`reproduce_w33_core.py` reconstructs W(3,3) from the alternating symplectic form on `F_3^4`, computes the graph invariants, exports a spectrum CSV, exports a one-loop Standard Model running benchmark CSV, and reports the fine-structure formula delta.

The one-loop running benchmark is not asserted as the theory's final coupling story. It is included as a sanity baseline: every exact coupling formula should be interpreted relative to a regime, normalization, and running convention.

## Next theorem-engineering targets

1. Move all public numerical formulas into one canonical machine-readable source.
2. Add tests that fail if `docs/index.html`, TeX manuscripts, and scripts disagree on exact formulas without regime labels.
3. Isolate the quark/Yukawa obstruction into a small failing test rather than broad prose.
4. Convert the finite-to-continuum bridge into a named checklist of theorem obligations.
5. State the single-photon/qutrit universality result as an exact gate-generation theorem with non-Clifford resource assumptions explicit.
