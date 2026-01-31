Thanks for checking out this repository!

Quick start
---------
- Create a virtual environment and activate it: `python -m venv .venv` then `source .venv/bin/activate` (or Windows PowerShell: `.venv\Scripts\Activate.ps1`).
- Install dependencies: `pip install -r requirements.txt` (or `pip install -e .`).
- Run the test suite: `python -m pytest -q`.

Pre-commit and CI
----------------
- This repo uses pre-commit for formatting and linting. Install hooks with `pip install pre-commit && pre-commit install`.
- CI is set up with GitHub Actions in `.github/workflows/ci.yml` to run the test suite on push and PR.

Developer tools
----------------
- `scripts/find_top_level_calls.py` detects modules that execute work at import time (e.g., `plt.show()` or top-level function calls). Use it locally to find and fix modules that should be safe to import.

Guidelines
----------
- Avoid heavy computations or blocking calls at import time.
- Put runtime logic in `main()` and protect with `if __name__ == '__main__':`.
- Use `json.dump(..., indent=2, default=str)` for robust serialization of non-native JSON types.

Sage & heavy-test policy
------------------------
- Sage-dependent verification runs are **optional** in CI; they are executed under the official Sage container to provide reproducible results.
- By default, the Sage pytest job runs on PRs *only when the PR touches Sage-relevant files* (scripts/**, tools/**, src/**, `**/*.sage`, `README.md`, `FINAL_TOE_PROOF.md`). Use the manual workflow dispatch if you want a full Sage run regardless of touched files.
- To request a Sage run explicitly for a PR, add the `run-sage` label to the PR; the label triggers a dedicated Sage test job that runs even if the PR doesn't touch Sage files. This job uploads a `skipped-optional-tests` artifact showing which tests were skipped due to missing optional dependencies.
- Locally, you can force optional tests to run by setting `RUN_OPTIONAL_TESTS=ALL` in your environment before running `pytest` (or set it to a comma-separated list like `sage,strawberryfields`).

If you'd like, I can open a branch and a draft PR with these changes, add CI badges to the README, and run the top-level scanner and fix remaining modules automatically. Let me know which you'd like next.
