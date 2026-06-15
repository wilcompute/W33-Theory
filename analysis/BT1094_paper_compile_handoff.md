# BT1094 — Paper compile handoff

BT1094 adds the first one-command paper integration/build handoff.

## Build script

```text
tools/bt1094_build_papers.py
```

The script:

1. runs the cumulative integration helper,
2. compiles `paper/w33_preprint.tex` from the `paper/` directory,
3. compiles `photonic_holonet.tex` from the repository root,
4. uses `latexmk` when available, otherwise falls back to two `pdflatex` passes.

## Cumulative integration helper

```text
tools/bt1094_integrate_all_latest_sections.py
```

It inserts the BT1083--BT1093 sections into both papers idempotently.

## GitHub Actions workflow

```text
.github/workflows/bt1094-tex-check.yml
```

The workflow runs on manual dispatch and pull requests touching the paper or integration files.  It installs TeX Live packages and runs:

```text
python3 tools/bt1094_build_papers.py
```

## Boundary

The workflow/build handoff is committed.  It has not been executed inside this chat because the execution container cannot clone GitHub or install TeX packages from the internet.  The next verification step is to run the workflow or run the script in a local clone.
