# arXiv Submission Checklist — Photonic Holonet Paper

**Paper:** `photonic_holonet.tex`  
**Target:** arXiv `quant-ph` (primary) + `hep-th` (cross-list)  
**Status:** Ready for submission  
**PDF:** Compiled June 2026 · SHA `68e906086abbfe2b81637055f3a53eec38078fc9`

---

## Pre-submission Checklist

- [ ] PDF compiles cleanly via CI (`holonet-build.yml` green)
- [ ] Abstract ≤ 1920 characters (arXiv hard limit)
- [ ] All `\cite{}` keys have matching `\bibitem` entries
- [ ] TikZ figures compile (packages: `tikz`, `positioning`, `arrows.meta`, `calc`)
- [ ] MSC 2020 codes declared in source:
  - `81P68` — Quantum computation
  - `20G40` — Linear algebraic groups over finite fields
  - `51E12` — Generalized quadrangles / polar spaces
  - `81V22` — Unified quantum theories
- [ ] arXiv categories:
  - Primary: `quant-ph`
  - Cross-list: `hep-th`, `math.GR`
- [ ] Author ORCID linked on arXiv submission form
- [ ] No hardcoded absolute file paths in source
- [ ] Journal-ref field: leave blank (not yet submitted to journal)
- [ ] Report-no field: `W33-BT739-889` (internal identifier)

---

## Theorem Ledger (BT739–BT889)

| Range | Topic | Count | Verified |
|-------|-------|-------|----------|
| BT739–BT760 | W(3,3) substrate & SRG(40,12,2,4) | 22 | ✓ |
| BT761–BT790 | Photon self-entanglement & Bell compass | 30 | ✓ |
| BT791–BT820 | [[240,81,4,3]]₃ CSS code & Steinberg module | 30 | ✓ |
| BT821–BT850 | D₁₂ mirror bus & holonet routing | 30 | ✓ |
| BT851–BT870 | Universality: Clifford group + magic states | 20 | ✓ |
| BT871–BT886 | SM spine: gauge group, generations, color | 16 | ✓ |
| BT887–BT889 | Architecture completeness (R1–R3 resolved) | 3 | ✓ |
| **Total** | | **151** | **✓** |

---

## Physics–Architecture Dictionary (key entries)

| SM Physics | Architecture |
|---|---|
| Gauge group U(1)×SU(2)×SU(3) | Centraliser C(R) in PSp(4,3) |
| 3 generations | Centre Z₃ of C(R) |
| Color triplets | Matter-shell Heisenberg group 3^{1+2} |
| Charge conjugation | Unique order-2 element of N(C(R))∖C(R) |
| Vacuum split 1+12+27 | Bell-line shell decomposition |
| Yang–Mills mass gap | Spectral gap of SRG(40,12,2,4) Laplacian |

---

## Submission Steps

1. Run `make holonet-release` locally; confirm zero LaTeX errors
2. Verify `holonet-build.yml` CI is green on master
3. Go to https://arxiv.org/submit
4. Upload: `photonic_holonet.tex` + all `.tikz` / figure files
5. Set primary category `quant-ph`, cross-list `hep-th` and `math.GR`
6. Paste abstract from paper (verify ≤ 1920 chars)
7. Add MSC codes in the Comments field: `MSC: 81P68, 20G40, 51E12, 81V22`
8. Submit → record arXiv ID below

**arXiv ID:** _(to be filled after submission)_

---

## Post-submission

- [ ] Record arXiv ID in `.zenodo.json` → `related_identifiers`
- [ ] Trigger Zenodo DOI registration (`.zenodo.json` already present in repo root)
- [ ] Create INSPIRE-HEP record (auto-imports from arXiv within 24h)
- [ ] Update `ABSTRACT_CCCCCXXII.md` with arXiv link
- [ ] Post announcement to `quant-ph` mailing list
- [ ] Cross-post to `hep-th` digest

---

## Related Papers in This Repo

| File | Role |
|------|------|
| `photonic_holonet.tex` | **This paper** — standalone submission |
| `paper/` | Master TOE preprint (cites this paper) |
| `w33_holographic_tower_final.tex` | CSS code paper (companion) |
| `w33_preprint.tex` | Physics TOE preprint |
