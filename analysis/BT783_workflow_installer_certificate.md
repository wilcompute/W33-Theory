# BT783 Workflow Installer Certificate

Installer added: `tools/install_bt777_workflow.py`.

Run from a local checkout:

`python tools/install_bt777_workflow.py`

It creates the BT777 workflow file at `.github/workflows/bt766_bt777_suite.yml`.

The workflow uses Python 3.11, installs numpy and networkx, and runs the BT777
suite runner.

Boundary: the workflow file itself was not committed directly because connector
writes to the workflow path were blocked. The installer provides a local one-step
fallback.
