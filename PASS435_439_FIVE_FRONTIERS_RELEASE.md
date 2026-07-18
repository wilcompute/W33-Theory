# Passes 435–439 — Five-frontier closure

This release executes all five follow-ups from Pass 434 and preserves explicit boundaries between known literature, new integral proofs, deterministic certificates, and synthetic hardware models.

## Pass 435 — Integral Heisenberg Smith pairing

For every odd prime power \(q=p^f\), the complete prime-to-characteristic critical group of the native Heisenberg bulk graph is proved.

For odd \(\ell
eq p\),

\[
K_{(\ell)}\cong
(\mathbb Z/\ell^{
u_\ell(q-1)})^{q(q^2-1)/2}
\oplus
(\mathbb Z/\ell^{
u_\ell(q+1)})^{q(q-1)^2/2}.
\]

At \(\ell=2\), the two rational Fourier sectors glue integrally:

\[
K_{(2)}\cong
(\mathbb Z/2^{
u_2(q-1)})^{q(q-1)}
\oplus
(\mathbb Z/2^{
u_2(q^2-1)})^{q(q-1)^2/2}.
\]

The proof uses central Fourier decomposition, a transpose fixed-space lemma in characteristic two, primitive rank factorization, and the paired block

\[
egin{pmatrix}q(q+1)&1\\0&q(q-1)\end{pmatrix}\sim
\operatorname{diag}(1,q^2(q^2-1)).
\]

## Pass 436 — Literature and attribution gate

The exact PDS family, its genuine nonabelianness, the Heisenberg construction for all odd prime powers, and the \((27,10,1,5)\) example are explicitly present in Polhill–Davis–Smith–Swartz, with the Heisenberg construction traced to Kantor. The repository paper now rejects novelty for those facts.

The surviving project boundary is the elation-cover recovery, section classification, integral Smith theorem, field/ring conductor atlas, and hardware falsifier.

## Pass 437 — Complete Smith weld

Pass 425's characteristic-primary layers and Pass 435's prime-to-characteristic theorem are welded into full invariant factors. Exact complete groups are released for \(q=3,5,9,25,27\). The \(q=3\) result reconstructs independently:

\[
(\mathbb Z/3)^4\oplus(\mathbb Z/6)^4\oplus\mathbb Z/18\oplus\mathbb Z/54\oplus(\mathbb Z/216)^6.
\]

## Pass 438 — Field/ring conductor atlas

For \(GF(p^2)\), every nontrivial central character is primitive and the graph has four eigenvalues. For \(\mathbb Z/p^2\mathbb Z\), conductor-\(p\) and primitive characters produce six eigenvalues and three 2-primary torsion periods. Exact atlas entries are released for \(p=3,5,7\), including matrix-free certificates at orders \(25^3\) and \(49^3\).

## Pass 439 — Torsion-sensitive photonic falsifier

A 16-step Ramsey/echo protocol distinguishes the \(GF(9)\) periods \(8,16\) from the \(\mathbb Z/9\mathbb Z\) periods \(2,8,16\). The residue-ring model has an exact Nyquist amplitude \(2/47\), absent from the field model. A deterministic \(72\)-scenario, \(16{,}384\)-shot synthetic census obtains \(72/72\) correct classifications.

No physical experiment is claimed.

## Artifacts

- `analysis/w33_pass435_integral_heisenberg_smith_pairing.py`
- `analysis/PASS435_INTEGRAL_HEISENBERG_SMITH_PAIRING.md`
- `data/w33_pass435_integral_heisenberg_smith_pairing.json`
- `analysis/PASS436_POLHILL_FULL_TABLE_AUDIT.md`
- `data/w33_pass436_polhill_full_table_audit.json`
- corrected `papers/heisenberg_pds_note.tex`
- `analysis/w33_pass437_full_smith_weld.py`
- `analysis/PASS437_FULL_SMITH_WELD.md`
- `data/w33_pass437_full_smith_weld.json`
- `analysis/w33_pass438_field_ring_discrimination_atlas.py`
- `analysis/PASS438_FIELD_RING_DISCRIMINATION_ATLAS.md`
- `data/w33_pass438_field_ring_discrimination_atlas.json`
- `analysis/w33_pass439_torsion_sensitive_photonic_fault_channel.py`
- `analysis/PASS439_TORSION_SENSITIVE_PHOTONIC_FAULT_CHANNEL.md`
- `data/w33_pass439_torsion_sensitive_photonic_fault_channel.json`
- `tests/test_pass435_439_five_frontiers.py`
- `.github/workflows/pass435-439-five-frontiers.yml`

## Validation contract

```bash
python analysis/w33_pass435_integral_heisenberg_smith_pairing.py --check
python analysis/w33_pass437_full_smith_weld.py --check
python analysis/w33_pass438_field_ring_discrimination_atlas.py --check
python analysis/w33_pass439_torsion_sensitive_photonic_fault_channel.py --check
python -m pytest -q tests/test_pass435_439_five_frontiers.py
```

The permanent workflow also compiles the corrected Heisenberg PDS note.
