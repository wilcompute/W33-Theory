# Passes 3356–3363 — Wrapper-aware theorem reachability closure

## Exact finding

The merged Passes 3320–3331 packet supplied a theorem insert, an index insert, and a publication integrator, but the three canonical TeX front doors are lightweight wrappers:

- `w33_paper.tex` delegates to `w33_paper_body.tex`;
- `photonic_holonet.tex` delegates to `photonic_holonet_body.tex`;
- `holonet_machine_blueprint.tex` delegates to `holonet_machine_blueprint_body.tex`.

The previous integrator searched each wrapper for `\\end{document}`. None of the wrappers contains that token, so the integration path terminated before materializing the theorem into any manuscript. Code search also found the public HTML identifier only in the insert and integrator, not in `docs/index.html`.

This is a source-reachability defect, not a defect in the Passes 3320–3331 mathematics.

## Repair

`tools/integrate_bt3320_bt3331.py` now recognizes two exact front-door architectures.

1. **Wrapper mode.** It inserts

   ```tex
   \\input{analysis/BT3330_global_cover_quantum_hypercube_insert}%
   ```

   into the wrapper's table-of-contents hook, immediately before the delegated body input.

2. **Monolithic mode.** It retains the former inline insertion before `\\end{document}`.

The public HTML path inserts before the final `</main>` and falls back to `</body>`. All paths are idempotent and expose machine-readable modes in a JSON report.

## Regression theorem

The focused regression proves:

- wrapper insertion occurs exactly once;
- monolithic insertion occurs exactly once;
- HTML insertion occurs exactly once;
- a second application is byte-identical;
- after materialization, all three live TeX front doors reference the packet exactly once.

The dedicated workflow applies the integrator twice, runs the focused regression, compiles all three canonical manuscripts with Tectonic, checks the public HTML identifier, uploads evidence, and commits the materialized four-front-door delta back to `master` once.

## Evidence boundary

This packet proves source-level reachability and idempotent publication wiring. A queued workflow is not described as a successful PDF build until its logs and artifacts are observed. No chromatic decision, hardware result, laboratory observation, quantum speedup, or physical interpretation is created by this repair.
