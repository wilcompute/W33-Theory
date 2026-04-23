# Repository Structure

This repo is large. The active theorem/program surfaces are concentrated in a
few directories; a large amount of historical computation and bundled output is
preserved alongside them.

## Start Here

- [README.md](../README.md): top-level project summary and reading route
- [docs/index.html](./index.html): live public paper / promoted theorem surface
- [docs/qutrit_foundation.html](./qutrit_foundation.html): exact qutrit/Heisenberg/local-E6 theorem boundary
- [docs/repo_frontier_audit.html](./repo_frontier_audit.html): repo-wide evidence map, folder audit, and literature-boundary corrections
- [docs/march_2026_frontier_note.md](./march_2026_frontier_note.md): current frontier and open wall

## Active Research Surfaces

- `exploration/`: exact theorem builders and bridge summaries
- `tests/`: targeted theorem regressions and search checks
- `tools/qiskit/`: local Qiskit workflow and discrete search/oracle tooling
- `tools/qiskit/bridge_oracle_ledger.json`: promoted local Qiskit bridge-oracle stack and operating points
- `tools/qiskit/ORACLE_LEDGER.md`: GitHub-readable summary of the promoted local Qiskit bridge-oracle stack
- `tools/`: helper programs that are still part of the active research stack

## Heavy but Important Context

- `docs/`: public-facing notes, HTML surfaces, and supporting writeups
- `artifacts/`: small committed fixtures needed by live scripts/tests
- `data/atlas/`: vendored offline data kept in-repo for verification

## Historical / Archive Weight

- `legacy/root_solvers/`: preserved root-era standalone solver scripts moved off the GitHub landing surface
- `legacy/one_off_root/`: preserved root-level scratch drivers and helpers moved off the GitHub landing surface
- `archive/`: preserved historical notes, bundles, and migrated material
- `archive/snapshots/`: archived pilot-output directories moved off the repo root
- `archive/extracted/`: archived extracted snapshot directories moved off the repo root
- `archive/misc/`: archived notes, logs, and assistant-era drop files moved off the repo root
- `bundles/`: large generated or staged computation output
- `V*_output*/`: phase or pilot output drops
- `extracted_v*/`: preserved extracted snapshots

## Bootstrap and Doctor

- `./scripts/bootstrap_repo_env.sh`: reproducible local setup for the repo
- `python3 tools/repo_doctor.py`: health check for dependencies, artifacts, and worktree hygiene
- `python3 tools/repo_cleanup_audit.py`: non-destructive audit of root clutter and dirty entries
- `python3 tools/browser_docs_audit.py`: automated desktop/mobile browser audit for the public docs surfaces
- `make full-audit`: run doctor, cleanup audit, and browser audit together

If heavyweight theorem artifacts live in another checkout or worktree, set:

```bash
export W33_DATA_ROOT=/path/to/repo-with-artifacts
```

## Local Hygiene Policy

- Root-level deliverable zips and extracted bundle drops are treated as local
  drop artifacts, not primary repo structure.
- Root-level one-off uppercase / `SOLVE_*` scripts are preserved legacy research
  context, not the recommended entrypoint for new readers.
- Generated helper output under `tools/artifacts/` is local scratch unless
  deliberately promoted elsewhere.
- If you need an inventory of current worktree clutter, run:

```bash
python3 tools/repo_cleanup_audit.py
```

The cleanup goal is not to hide active source work. It is to keep the live
entrypoints readable while preserving historical material and local research
drops without letting them overwhelm the repo root.
