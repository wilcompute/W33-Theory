#!/usr/bin/env python3
"""Pass 4881 withdrawal tombstone for the unbuilt wreath quotient."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHORITATIVE = ROOT / "data" / "PART_W33_PASS4948_MODULAR_BOSE_MESNER_CORRECTION.json"
OUTPUT = ROOT / "data" / "PART_W33_PASS4881_AGL13_WREATH_EXTENSION_CHECK.json"


def main() -> int:
    audit = json.loads(AUTHORITATIVE.read_text())
    values = audit["corrected_finite_values"]
    assert audit["status"] == "PASS"
    assert values["order1440_groups"] == ["S6xC2", "Aut(S6)"]
    assert values["S3_wreath_S6_order"] == 33_592_320
    assert values["local_port_compiler_order"] == 6_912

    out = {
        "pass": 4881,
        "schema": "w33.pass4881.withdrawal_tombstone.v1",
        "status": "WITHDRAWN_BY_PASS4948",
        "surviving_values": {
            "local_port_compiler_order": 6_912,
            "S3_wreath_S6_order": 33_592_320,
            "order_1440_groups_in_Pass4873": ["S6xC2", "Aut(S6)"],
        },
        "withdrawn_statements": [
            "Pass4873 compares S6xC2 with the Schur cover 2.S6.",
            "The AGL(1,3) wreath compiler selects or surjects onto S6xC2.",
            "Split local factors alone exclude a non-split central quotient.",
        ],
        "reason": (
            "Pass4873's second group is Aut(S6), and no quotient homomorphism from "
            "the compiler was constructed. Group orders alone do not build one."
        ),
        "authoritative_certificate": AUTHORITATIVE.name,
        "boundary": (
            "The two exact compiler orders survive; no order-1440 quotient selection theorem does."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Pass 4881 withdrawal tombstone: status=WITHDRAWN_BY_PASS4948")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
