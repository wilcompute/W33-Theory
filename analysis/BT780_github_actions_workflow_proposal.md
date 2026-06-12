# BT780 — GitHub Actions Workflow Proposal

The connector blocked direct creation of `.github/workflows/...`, so this file
contains the workflow body to install manually or copy into a workflow file.

Suggested path:

`.github/workflows/bt766_bt777_suite.yml`

```yaml
name: BT766 BT777 Suite

on:
  push:
    branches:
      - master
  pull_request:
    branches:
      - master
  workflow_dispatch:

jobs:
  suite:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          python -m pip install numpy networkx
      - name: Run theorem suite
        run: python analysis/bt777_run_bt766_bt776_suite.py
```

Boundary: the active workflow file was not created because the connector blocked
writes to the workflow path. The import-based BT777 runner itself is already in
the repository.
