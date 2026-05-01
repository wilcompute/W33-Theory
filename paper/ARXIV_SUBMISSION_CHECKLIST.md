# arXiv Submission Checklist — W(3,3) Theory of Everything

> Last updated: 2026-05-01

## Phase 1 — Local LaTeX Compilation

- [ ] Run `pdflatex main.tex` → no errors (warnings OK)
- [ ] Run `bibtex main` → all citations resolved
- [ ] Run `pdflatex main.tex` × 2 (cross-refs converge)
- [ ] Check `\ref{}` warnings: none should be `??`
- [ ] Verify prediction table `longtable` spans correctly (check page breaks)
- [ ] Confirm Section/Appendix numbers match callouts in text
- [ ] Check all `\cite{}` keys exist in `references.bib`:
  - `\cite{Machacek1984}` — two-loop Yukawa RGE
  - `\cite{Wiles1995}` — modularity theorem
  - `\cite{BCDT2001}` — Breuil–Conrad–Diamond–Taylor
  - `\cite{LZ2024}` — LUX-ZEPLIN 2024
  - `\cite{PDG2024}` — Particle Data Group
  - `\cite{Planck2018}` — Planck cosmology
  - `\cite{Perkel1979}` — Perkel graph construction
- [ ] Equations numbered sequentially; no duplicate labels
- [ ] Table~1 (fermion masses) values match Appendix B P1–P9

## Phase 2 — Content Review

- [ ] Abstract claims match paper body:
  - "57 confirmed predictions" → Appendix B shows exactly 57 ✓/consistent
  - "3 generations from Frobenius triality" → Theorem IV present
  - "single free parameter" → only $M_R$ or equivalent stated in §1
- [ ] Dark matter section (§7 / `dark_matter_section.tex`) included
- [ ] Equation (dm_mass) cross-referenced in §7 and Appendix B P25
- [ ] All prediction IDs P1–P116 present in `predictions_table.tex`
- [ ] No orphaned `TODO` or `FIXME` comments in source
- [ ] Author list and affiliation correct
- [ ] No overfull hboxes > 5pt in final PDF

## Phase 3 — arXiv Package Prep

- [ ] Create submission directory: `arxiv_submit/`
- [ ] Copy: `main.tex`, all `\input{}` files, `references.bib`, figures/
- [ ] Remove: `.aux`, `.log`, `.bbl` (let arXiv compile)
- [ ] Check figure files are: `.pdf`, `.eps`, or `.png` (no `.jpg` for line art)
- [ ] Verify total uncompressed source < 50 MB
- [ ] Create `anc/` ancillary folder with reproducibility scripts:
  - `scripts/SOLVE_RG_NEUTRINO.py`
  - `scripts/ckm_global_fit.py`
  - `scripts/build_perkel_spectral_matrix.py`
  - `scripts/compute_hashimoto_w33.py`
- [ ] Add `README` to `anc/` describing Python ≥ 3.10 + scipy/numpy requirements

## Phase 4 — arXiv Metadata

- [ ] Title: *"A Theory of Everything from the W(3,3) Graph: Langlands Generation Structure, Yukawa Hierarchies, and 116 Falsifiable Predictions"*
- [ ] Primary category: **hep-th**
- [ ] Cross-list: **hep-ph**, **math-ph**, **gr-qc**
- [ ] MSC codes: 81T13, 11F80, 20C15
- [ ] Keywords: W(3,3) graph, Langlands program, Yukawa coupling, dark matter, theory of everything, Frobenius triality
- [ ] Abstract ≤ 1920 characters (arXiv limit)
- [ ] ORCID linked to submission
- [ ] No journal assignment yet (submit as preprint first)

## Phase 5 — Post-Submission

- [ ] Note arXiv ID once assigned
- [ ] Update `CITATION.cff` in GitHub repo with arXiv ID
- [ ] Add DOI badge to `README.md`
- [ ] Tweet/post announcement with abstract link
- [ ] Submit simultaneously to Zenodo for versioned DOI
- [ ] Open GitHub Discussion thread: "Post-arXiv feedback"

## Known Pre-Submission Issues

| Issue | Priority | Status |
|---|---|---|
| P29 $\sigma_{SI}$ marginal vs LZ 2024 bound | High | Flagged in text as "marginal" |
| CDF $W$ mass anomaly (P87–P92) | Medium | Note added; CDF outlier |
| Muon $g-2$ (P81): $Z'$ contribution small | Low | Stated as partial correction only |
| IH vs NH (P24) — awaits JUNO/DUNE | Medium | Prediction made; testable 2027 |
