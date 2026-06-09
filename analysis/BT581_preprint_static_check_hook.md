# BT581 - Preprint Static Check Hook

Added a repository hook script:

```bash
bash tools/check_w33_preprint_static.sh
```

The hook changes to the repository root and runs:

```bash
python tools/build_w33_preprint.py
```

That executes the BT578 static build harness, including the BT574 LaTeX sanity verifier when present.

This gives future paper edits a one-command preflight check before attempting a full TeX/PDF build.

A CI workflow can later call this same script directly.
