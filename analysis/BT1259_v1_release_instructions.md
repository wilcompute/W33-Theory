# BT1259 — GitHub Release v1.0.0 — Instructions
**Date:** 2026-06-17  
**Status:** READY TO EXECUTE

## Pre-Release Gate Checklist
- [x] BT1247-BT1259 pushed to master
- [x] `.zenodo.json` deployed
- [x] `paper/sections/` stubs in place for clean LaTeX build
- [x] `tests/test_bijection_solver_v3.py` pytest suite (9 tests)
- [x] `ARXIV_COVER_LETTER.md` drafted
- [ ] **paper-build CI passes** (trigger: this commit pushes to `paper/**`)
- [ ] **bijection-tests CI passes** (already passing — pure Python, no deps)

## Release Command (run locally or via GitHub UI)
```bash
# Option A: GitHub CLI
gh release create v1.0.0 \
  --title "W33-Theory v1.0.0 — arXiv Submission Release" \
  --notes "First official release of W33-Theory. Accompanies arXiv submission hep-th/2026.XXXXX. Contains 1,259 breakthrough logs, Python solvers, SageMath scripts, Lean 4 proofs, and the full preprint PDF."

# Option B: GitHub UI
# 1. Go to https://github.com/wilcompute/W33-Theory/releases/new
# 2. Tag: v1.0.0 (create new tag on master)
# 3. Title: W33-Theory v1.0.0 — arXiv Submission Release
# 4. Body: paste BT1259 summary
# 5. Attach: paper/w33_preprint.pdf (download from CI artifact)
# 6. Click: Publish release
```

## What Happens on Release
1. `release_to_zenodo.yml` fires → Zenodo archives the repo → DOI assigned
2. `zenodo_sync.yml` fires → metadata synced
3. DOI appears at https://zenodo.org/doi/10.5281/zenodo.XXXXXXX within ~5 minutes
4. Insert DOI into `ARXIV_COVER_LETTER.md` and submit to arXiv

## Timeline
- Gate: paper-build CI ≈ 8-12 minutes to complete
- Release creation: 2 minutes
- Zenodo DOI assignment: ~5 minutes after release
- arXiv submission: 30 minutes to fill form
- **arXiv public:** next 14:00 ET announcement cycle
