# Passes 6545–6552 — CE2 carrier/provenance correction

## Status

**PASS as a provenance/type correction; global CE2 formula closure remains OPEN pending independent replay.**

The verifier is `analysis/w33_pass6545_6552_ce2_carrier_provenance_correction.py`. It is intentionally narrower than the later synthetic anchor-orbit scripts: it certifies the actual object present in the repository and records what is still missing.

## Pass 6545 — the authentic CE2 local object is present

The live repository contains

`committed_artifacts/ce2_sparse_local_solutions.json`

with
\[
\boxed{5832}
\]
sparse local solution rows. Its compact metadata points back to `artifacts/ce2_rational_local_solutions.json`, and the key format is a triple of labels
\[
(i,f),\qquad 0\le i<27,\quad 0\le f<3.
\]
Thus the authentic local data lives on a
\[
\boxed{27\times3}
\]
carrier/fiber set.

The current `scripts/ce2_global_cocycle.py` documents the same decomposition:
\[
\boxed{5832=5184+648},
\]
with the dominant one-term \(1/54\) family and the two-term \(1/108\) fiber/rank-drop family.

## Pass 6546 — the carrier is the \(E_6\) minuscule 27, not the 40 W33 points

The actual graded bracket code realizes
\[
(\mathfrak e_6\oplus\mathfrak{sl}_3)
\oplus(27\otimes3)
\oplus(27^*\otimes3^*).
\]
The CE2 local labels therefore index the \(27\)-dimensional \(E_6\) carrier together with an \(\mathfrak{sl}_3\) fiber. The committed affine-Heisenberg model supplies a bijection
\[
\boxed{\{0,\ldots,26\}\cong\mathbb F_3^3}.
\]
This is categorically different from the \(40\)-point projective action of \(W(3,3)\).

Accordingly a later instruction of the form “take CE2 anchor 22 and enumerate its 40-point W33 orbit” is ill-typed unless an explicit equivariant map between the 27-carrier and the 40-point W33 set is constructed first.

## Pass 6547 — anchor 22 has a natural 27-point Schläfli label

The already-committed `balanced_orbit_schlafli_isomorphism.json` is a verified 27-point identification with the classical Schläfli 27-line carrier. Under that map,
\[
\boxed{22\longleftrightarrow L_{45}},
\]
with phase \(0\) and root type `half`.

This does **not** by itself prove that every CE2 basis convention is equivariant with every Schläfli convention. It does, however, identify the correct size and the natural representation-theoretic candidate carrier: 27, not 40.

## Pass 6548 — the synthetic 40-point closure is explicitly retracted

The current corrected `scripts/w33_ce2_anchor22_closure.py` says exactly what its predecessor did wrong: it generated synthetic weights from a hard-coded rule on labels \(1,\ldots,39\) without constructing a W33 automorphism action or evaluating the CE2 tensor on that orbit.

The corrected file retains only three imported witnesses and reports
\[
\boxed{\texttt{OPEN\_BEYOND\_THREE\_IMPORTED\_WITNESSES}}.
\]
That retraction is correct. The stronger correction here is that the requested 40-point orbit is not merely unavailable; it uses the wrong native carrier.

## Pass 6549 — authentic source rows exist, but the named producer does not

The compact 5832-row artifact names

`artifacts/ce2_rational_local_solutions.json`

as its source. That source is absent from the current checkout. More importantly, the historical metadata names

`tools/solve_sparse_ce2_all_triples.py`

as the producer, but the current tree does not contain that file and the GitHub path-history endpoint returns no commits for that exact path.

Therefore the compact artifact is real evidence, but its named from-scratch producer is not currently recoverable under that path. A release that claims pristine reproducibility must repair this provenance hole by restoring the producer/dependencies or by replacing it with an independent replay verifier.

## Pass 6550 — the global predictor is a compression, not yet an independent certificate

`scripts/ce2_global_cocycle.py` contains substantial affine-Heisenberg and metaplectic structure and documents the \(5184+648\) law. However its current implementation also loads the committed local table as authoritative data for known rows and derives some tables/sign information from that source.

That is useful compression and a plausible theorem candidate, but a verifier that consumes the same 5832-row table it is supposed to explain is not an independent proof of the global formula.

The theorem-tier target is therefore:
\[
\boxed{\text{generate/predict all 5832 rows without reading their U/V answers, then compare exactly}.}
\]

## Pass 6551 — corrected CE2 evidence hierarchy

The current safe hierarchy is:
\[
\boxed{\text{genuine graded }E_8\text{ bracket machinery}}
\]
\[
\Downarrow
\]
\[
\boxed{5832\text{ committed authentic local CE2 rows on }27\times3}
\]
\[
\Downarrow
\]
\[
\boxed{\text{affine-Heisenberg global compression/predictor}}
\]
with the final arrow “independent all-row theorem” still requiring a no-answer-table replay.

The unrelated 40-point W33 anchor-orbit scaffold is removed from this chain unless a new explicit equivariant transport is supplied.

## Pass 6552 — manuscript boundary

The three canonical papers should distinguish sharply between:

- **certified local CE2 data:** present, 5832 rows, native 27×3 carrier;
- **structured global formula:** implemented and strongly supported, but not independently replay-certified in the present checkout;
- **40-point anchor closure:** invalid as a native CE2 orbit construction without an explicit 27↔40 intertwiner;
- **K3:** still separate and still requires the real curvature/cochain object before any deformation scan is theorem-tier.

This correction strengthens the project: it identifies the authentic object and removes a false transport assumption rather than weakening the CE2 program.
