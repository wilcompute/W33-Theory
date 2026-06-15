# BT1100 — TeX CI status

BT1100 updates the paper build path and workflow to use the no-network sanity checker and the latest cumulative section integrator.

## Build path

```text
tools/bt1094_build_papers.py
```

now runs:

```text
python tools/bt1100_tex_path_sanity.py
python tools/bt1100_integrate_all_latest_sections.py
```

before compiling the W33 and holonet TeX sources.

## Workflow path

The workflow file is still

```text
.github/workflows/bt1094-tex-check.yml
```

but it is now titled `BT1100 TeX check` and watches the BT1100 sanity/integration helpers.

## Connector-visible status

For workflow update commit

```text
c8449f0ad3f0e1f12441e547d815824e9700cc40
```

the combined status query returned no status contexts and the workflow-run query returned no visible workflow runs.

## Boundary

The no-network sanity checker and CI path are committed.  No TeX compile pass is claimed until a visible workflow run or local build output is available.
