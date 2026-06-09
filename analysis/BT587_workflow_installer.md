# BT587 - Workflow Installer

Added:

```bash
python tools/install_preprint_workflow.py
```

Purpose: copy the CI-ready template from

```text
analysis/BT584_preprint_static_check_workflow_template.yml
```

to

```text
.github/workflows/w33-preprint-static-check.yml
```

inside a local checkout.

This bypasses connector restrictions on writing directly to `.github/workflows` while preserving the workflow activation path.

After installation, the workflow calls:

```bash
bash tools/check_w33_preprint_static.sh
```

which delegates to the BT578 build harness and BT574 static verifier.
