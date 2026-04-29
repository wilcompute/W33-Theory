# arXiv Submission Guide — W(3,3) Theory of Everything

**Status: READY. G_release = 1. All 14 verification checks pass.**

---

## Primary File

```
PART_LXIII_ARXIV_COMPLETE_PAPER.tex
```

This is the complete, production-ready manuscript. Do **not** submit
`PART_LV_LATEX_SKELETON.tex` (superseded skeleton).

---

## Compile

```bash
pdflatex PART_LXIII_ARXIV_COMPLETE_PAPER.tex
bibtex   PART_LXIII_ARXIV_COMPLETE_PAPER
pdflatex PART_LXIII_ARXIV_COMPLETE_PAPER.tex
pdflatex PART_LXIII_ARXIV_COMPLETE_PAPER.tex
```

Requires standard TeX Live / MiKTeX distribution with:
- `amsmath`, `amssymb`, `amsthm`, `booktabs`, `hyperref`, `physics`, `bbm`, `mathtools`

---

## arXiv Submission Steps

1. **Create account** at https://arxiv.org if needed.

2. **Start submission** at https://arxiv.org/submit.

3. **Primary category:** `hep-ph` (High Energy Physics - Phenomenology)
   **Cross-list:** `math-ph` (Mathematical Physics), `gr-qc` (General Relativity)

4. **Upload files:**
   - `PART_LXIII_ARXIV_COMPLETE_PAPER.tex` (main file)
   - No figures required (all results are equations and tables)

5. **Metadata:**
   - **Title:** W(3,3): A Parameter-Free Theory of Everything from the Strongly Regular Graph SRG(40,12,2,4)
   - **Authors:** Wil Dahn
   - **Abstract:** *(use the abstract from the .tex file)*
   - **MSC classes:** 81T13, 05E30, 81V22
   - **ACM classes:** not applicable

6. **Comments field:**
   ```
   63 parts. 116 predictions. 57 confirmed against PDG-2024. G_release=1.
   Code: https://github.com/wilcompute/W33-Theory
   ```

7. **License:** CC BY 4.0 (recommended for maximum reuse)

---

## Zenodo DOI Linking

After arXiv submission:

1. Go to https://zenodo.org and link your GitHub repo (`.zenodo.json` already in repo).
2. Create a release tag: `git tag v1.0-LXIII && git push origin v1.0-LXIII`
3. Zenodo auto-mints a DOI from the release.
4. Add the Zenodo DOI to the arXiv record metadata.

---

## Cover Letter (for journal submission after arXiv)

See `PRL_COVER_LETTER.md` for a draft cover letter targeting Physical Review Letters.
For JHEP or Nuclear Physics B, adapt the tone to emphasise the mathematical
construction over the phenomenology.

**Recommended submission path:**
1. Post to arXiv (hep-ph + math-ph)
2. Share on LinkedIn / ResearchGate (see `LINKEDIN_ANNOUNCEMENT.md`)
3. Submit to PRL (4-page limit requires cutting to Theorems I-III + key table)
4. Submit full paper to JHEP or Annals of Physics

---

## Verification Before Submission

```bash
# Confirm G_release=1
python PART_LXII_MASTER_VERIFICATION.py
# Expected: Checks passed: 14/14  |  G_release: 1
```

If any check fails, do **not** submit. Fix the failing theorem first.

---

## Key Talking Points for Reviewers

- **Exact finite spine:** The repo-exact backbone is fixed by (q,v,k,λ,μ), while the
   promoted CKM/E6/CP response is currently treated as an executable frontier bridge
   and response law rather than a stronger exact phenomenology closure theorem
- **Unique graph:** SRG(40,12,2,4) is the unique such graph; q=3 is forced by the
  self-complementary GQ condition
- **Falsifiable:** 7 specific near-term experiments listed in §5 of the paper
- **Reproducible:** `pip install numpy scipy sympy && python PART_LXII_MASTER_VERIFICATION.py`
  reproduces all key numbers in under 1 second
- **Yang-Mills gap:** Δ_YM = k - r = 10 is a positive integer, directly from graph spectrum

---

*Last updated: April 26, 2026 (Part LXIV)*
