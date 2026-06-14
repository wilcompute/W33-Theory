#!/usr/bin/env python3
"""BT1003 — CI status probe manifest for the R3 edgewise workflow.

The connector status probe for the latest checked commit returned no legacy
combined statuses and no workflow runs surfaced through the commit workflow-runs
endpoint.  This file records that boundary and keeps the next check reproducible:
use the Actions tab or `gh run list --workflow r3-edgewise-fat-tower.yml` from a
checkout/token with Actions read access.
"""
from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    out = {
        "theorem": "BT1003 CI status probe for R3 edgewise workflow",
        "workflow": ".github/workflows/r3-edgewise-fat-tower.yml",
        "checked_commit": "12cadf5d49b6bc66bc167e65c57ee42bc5804891",
        "connector_combined_statuses": [],
        "connector_commit_workflow_runs": [],
        "reading": "The GitHub connector did not surface a workflow run or legacy status for the checked commit. The workflow file is committed; next verification should use GitHub Actions UI or gh run list with Actions read access.",
        "next_command": "gh run list --workflow r3-edgewise-fat-tower.yml --branch master --limit 5"
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/bt1003_ci_status_probe.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
