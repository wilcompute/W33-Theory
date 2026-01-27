PR: Fix tests and CI — generate summary artifacts and test fixes

Summary
-------
This PR makes the local test workflow deterministic and reproducible by generating the repository's summary artifacts before running tests and by fixing a number of issues uncovered during local test runs.

Key changes
-----------
- Fixes
  - `conftest.py`: use regex `.search` to avoid TypeError during test collection
  - `THEORY_PART_CXLIV_CRYPTO.py`: fix correlation calculation (conjugate Bob's state) and guard large prints with `if __name__ == '__main__'`
  - `THEORY_PART_CLII_STATE_PARTICIPATION.py`: guard large prints and ensure triangles computed at import-time for tests
  - `tests/test_mub_triangle.py`: precompute `all_triangles` at module scope
  - `scripts/collect_results.py`: omit null timestamps and only include `part`/`part_number` where valid (normalize Roman numerals when possible)
- Additions
  - `pytest.ini`: restrict discovery to `tests/`, filter deprecation warnings, exclude large folders
  - `Makefile`: `generate-summary` and `test` targets
  - `scripts/generate_summary.sh` and `scripts/generate_summary.ps1` for local artifact generation
  - `.github/workflows/pytest.yml`: run local artifact generators before pytest
- Dependencies
  - install `pandas` in dev env to allow some proof scripts to execute during tests

Validation
----------
- Generated `SUMMARY_RESULTS.json` (71 PART_*.json collected) and `NUMERIC_COMPARISONS.json` (1 entry)
- Ran `pytest tests/`: all tests now pass locally after fixes

Notes
-----
- The repo in this workspace was initialized and committed locally on branch `fix/tests-and-ci/generate-summary`.
- No remote push was performed. A patch `fix-tests-and-ci.patch` was produced.

Checklist
--------
- [ ] Confirm PR description and title
- [ ] Push branch to remote and open PR
- [ ] Add CI run (optional: include Sage verification job separately)

If you'd like, I can push the branch to remote and open a PR — provide the remote URL or let me know and I'll prepare the exact git commands for you to run locally.