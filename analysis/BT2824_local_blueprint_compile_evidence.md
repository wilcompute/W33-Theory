# Pass 2824 — local Holonet blueprint compile evidence

This note records an independent local reconstruction and compile of the Passes 2820–2824 migration while the GitHub-hosted Actions queue was stalled.

## Procedure

1. Reconstructed the current `master` version of `holonet_machine_blueprint.tex` from bounded GitHub line ranges.
2. Applied the same deterministic replacements implemented by `analysis/bt2820_2824_blueprint_truth_gate.py`.
3. Added `analysis/BT2820_BT2824_blueprint_evidence_insert.tex`.
4. Compiled twice with `pdfLaTeX` to stabilize references.
5. Rejected any log containing `Overfull`, `Undefined control sequence`, `LaTeX Error`, `Emergency stop`, or `Fatal error`.

## Result

- Pages: **23**
- Overfull boxes: **0**
- Undefined references after the second pass: **0**
- Migrated TeX SHA-256: `04d2ac130376911120d4496afe23b32f29794bf2ad39263227b95996c9cede4c`
- PDF SHA-256: `cba3e73bde8b7344a8383e98217325234aa607905f6d74f565aeb9706c5b0c3b`
- Log SHA-256: `881d57aab2646a342bbf0bbbebe0b0cac02361eb1cc1574762be22e6e77df145`

The only layout defect found on the first pass was a `2.1224 pt` overfull box caused by the unbreakable evidence-state label `Placed/timed`. The source insert now uses the shorter label `Routed`; the two-pass rebuild is clean.

## Evidence boundary

This is corroborating local compile evidence, not the remote release gate. PR #210 still requires its dedicated GitHub runner to apply the migration, compile with Tectonic 0.16.9, commit the generated TeX/PDF/certificates, and then complete a second drift-free run before merge.
