#!/usr/bin/env python3
"""Export the executable W33 periodic-table organization summary as an artifact."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


from scripts.w33_periodic_table_organization import (  # noqa: E402
    build_periodic_table_organization_summary,
)


OUTPUT_FILE = ROOT / "artifacts" / "w33_periodic_table_organization_summary.json"


def build_payload() -> dict[str, object]:
    summary = build_periodic_table_organization_summary()
    return {
        "kind": "w33_periodic_table_organization_summary",
        "layer_order": summary["layer_order"],
        "rows": summary["rows"],
        "periodic_table_theorem": summary["periodic_table_theorem"],
        "same_table_bridge_theorem": summary["same_table_bridge_theorem"],
        "bridge_verdict": summary["bridge_verdict"],
    }


def main() -> None:
    payload = build_payload()
    OUTPUT_FILE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()