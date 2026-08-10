# Passes 4727–4728 — integration, public surface, and evidence closure

This closes the reserved Pass 4721–4728 lane without adding another physical claim.

## Pass 4727 — manuscript and public integration

The verified Pass 4721–4726 results are integrated into all three canonical manuscript wrappers:

- `w33_paper.tex`
- `photonic_holonet.tex`
- `holonet_machine_blueprint.tex`

through:

- `analysis/PASS4721_4724_support12_involution_square_root_cover_insert.tex`
- `analysis/PASS4725_4726_involution_residue_dual_code_insert.tex`

The public theorem surfaces are:

- `analysis/PASS4721_4724_support12_involution_square_root_cover_index_insert.html`
- `analysis/PASS4725_4726_involution_residue_dual_code_index_insert.html`
- `docs/support12-involution-square-root-cover.html`

and both cards are registered in:

- `data/w33_public_frontier_extension_pass4461_4464.json`.

The repository's existing safe public-frontier materializer watches that extension file and `analysis/*_index_insert.html`, then idempotently updates only `docs/index.html`. A narrow companion materializer, `tools/integrate_pass4721_4724.py`, independently checks that both cards occur exactly once.

The coding-theory prior-art boundary is explicit:

- `analysis/PASS4725_4726_CODING_PRIOR_ART_BOUNDARY.md`.

The underlying `[40,10,12]` adjacency code and its weight enumerator are credited to Haemers–Peeters–van Rijckevorsel (1999); the project claims only the new involution/support-shell/dual-minimum identification and square-root cover.

## Pass 4728 — evidence and provenance closure

Executable verifiers:

- `analysis/w33_pass4721_4724_support12_involution_square_root_cover.py`
- `analysis/w33_pass4725_4726_involution_residue_dual_code.py`
- `analysis/w33_pass4726_regulus_residue_falsifier.py`

Frozen certificates:

- `data/PART_W33_PASS4721_4724_SUPPORT12_INVOLUTION_SQUARE_ROOT_COVER.json`
- `data/PART_W33_PASS4725_4726_INVOLUTION_RESIDUE_DUAL_CODE.json`
- `data/PART_W33_PASS4726_REGULUS_RESIDUE_FALSIFIER.json`

Focused regressions:

- `tests/test_w33_pass4721_4724_support12_involution_square_root_cover.py`
- `tests/test_w33_pass4725_4726_involution_residue_dual_code.py`
- `tests/test_w33_pass4726_regulus_residue_falsifier.py`

CI closure:

- `.github/workflows/w33_pass4721_4724_support12_involution_cover.yml`

recomputes all three certificates, runs the frozen tests before and after recomputation, checks the Pass 1830 erratum and coding prior-art boundary, materializes the public cards, and compiles the three canonical manuscripts with Tectonic.

Two provenance records prevent silent historical contamination:

- `analysis/PASS1830_ERRATUM_PASS4722_LINE_ACTION.md` withdraws the old 2,880 line-orbit conclusion caused by applying a point action to line indices;
- `analysis/PASS4721_4728_NAMESPACE_COLLISION_OWNERSHIP.md` records that this lane reserved 4721–4728 before a later Track-A collision, under the repository's first-reservation ownership convention.

## Exact theorem chain closed by this release

\[
1620\text{ support-12 thickenings}
\longrightarrow
540K_3
\longrightarrow
270\text{ four-line residues}
\longleftrightarrow
270\text{ inner involutions},
\]

with a PSp-equivariant lift

\[
540\text{ support triangles}
\longleftrightarrow
540\text{ four-fixing outer order-4 roots}
\xrightarrow{h\mapsto h^2}
270\text{ inner involutions},
\]

and the binary coding closure

\[
\operatorname{span}_{\mathbf F_2}(270\text{ residues})
=
\ker A_*
=
H_{10}^{\perp}
=[40,30,4],
\]

where the 270 residues are the complete weight-4 shell and hence the complete minimum parity-check shell reconstructing the known `[40,10,12]` adjacency code `H10`.

## Falsifier retained

A tempting shortcut was rejected rather than promoted. The 270 residues are **not** the BT794 four-transversal regulus sets. BT794 gives 540 distinct four-transversal sets, disjoint from the 270 residue family, with uniform cross-intersection profiles bounded by two. This keeps the older regulus/tomotope lane separate until an actual intertwiner is found.

## Closure boundary

This release closes an exact finite-geometry / permutation-group / binary-code lane. It does not turn any of these combinatorial identities into a claim about measured particle physics, quantum hardware performance, or a physical dynamical law.
