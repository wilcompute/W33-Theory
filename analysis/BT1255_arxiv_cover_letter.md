# BT1255 — arXiv Cover Letter & Submission Package
**Date:** 2026-06-17  
**Status:** DRAFTED ✓ — awaiting PDF + DOI before submission

## Files Created
- `ARXIV_COVER_LETTER.md` — full cover letter with pre-submission checklist
- `analysis/BT1251_arxiv_abstract_v2.md` — final abstract (BT1251, already pushed)

## Submission Plan
1. **Gate 1:** paper-build CI passes (BT1253) → PDF artifact available
2. **Gate 2:** All 9 bijection tests pass (BT1254) → SM bijection machine-verified  
3. **Gate 3:** Create GitHub release `v1.0.0` → triggers `release_to_zenodo.yml` → DOI assigned
4. **Gate 4:** Insert Zenodo DOI into `ARXIV_COVER_LETTER.md` Comments field
5. **Submit:** https://arxiv.org/submit → hep-th, cross-list math-ph + quant-ph

## Estimated Timeline
| Step | Blocker | Est. Time |
|---|---|---|
| Fix LaTeX errors (if any) | paper-build CI | 1–4 hours |
| Zenodo DOI | GitHub release v1.0.0 | 30 minutes |
| Final abstract/cover review | Manual | 30 minutes |
| arXiv submission | All gates above | 1 hour |
| **Total to arXiv live** | — | **3–6 hours** |

arXiv processes hep-th submissions daily at 14:00 ET. A submission by 13:59 ET will appear in the next business day's mailing.
