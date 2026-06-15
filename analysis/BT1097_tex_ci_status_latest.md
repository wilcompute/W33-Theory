# BT1097 — Latest TeX CI status

BT1097 also updates the existing paper build script so it uses the newest cumulative integrator.

## Updated build path

```text
tools/bt1094_build_papers.py
```

now calls

```text
tools/bt1097_integrate_all_latest_sections.py
```

before compiling both TeX sources.

## Workflow trigger

The workflow file now includes `push`, `pull_request`, and manual dispatch triggers for paper/helper/workflow changes.

## Inspection result

For commit

```text
ae841fe903b6ccb80bfb5e12ae355424cb406b04
```

the combined status query returned no status contexts and the connector-visible workflow-run query returned no workflow runs.

## Boundary

The CI path is now wired to the latest integrator, but no compile result is visible through the connector at inspection time.  Compile success remains unclaimed until a workflow run or local TeX build is observed.
