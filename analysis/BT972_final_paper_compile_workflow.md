# BT972 — Final paper compile workflow

BT972 adds a GitHub Actions workflow for final paper compilation.

## Workflow

```text
.github/workflows/build-final-papers.yml
```

## Entrypoint

```text
tools/bt960_execute_final_selector_stack.py
```

## Papers

```text
w33_paper.tex
photonic_holonet.tex
```

## Artifacts

```text
w33_paper.pdf
photonic_holonet.pdf
logs
selector stack manifest
SHA256SUMS.txt
```

## Boundary

The workflow is committed. This connector pass did not fetch a completed run artifact.
