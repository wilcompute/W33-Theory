# BT974 — Direct final paper build path

BT974 adds a direct build script that includes the BT973 rail generation/phase theorem before compiling both papers.

## Script

```text
tools/bt974_direct_final_paper_build.sh
```

## Targets

```text
w33_paper.tex
photonic_holonet.tex
```

## Outputs

```text
build_artifacts/w33_paper.pdf
build_artifacts/photonic_holonet.pdf
build_artifacts/SHA256SUMS.txt
```

## Boundary

Workflow YAML updates were blocked by the connector filter, so the direct shell build path was committed instead. The connector did not run a full checkout compile or fetch artifacts.
