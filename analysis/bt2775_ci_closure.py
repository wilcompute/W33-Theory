#!/usr/bin/env python3
"""Pass 2775: reproducibility and implementation-evidence closure packet."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def sha(name: str) -> str:
    return hashlib.sha256((DATA / name).read_bytes()).hexdigest()


def main() -> None:
    expected = {
        "PART_BT2767_M36_PREPARATION_ROM.json": "4f637e7c174cd6f8597511911bb2ecdd6ee58fe8bfd862c3d62b18bf30138322",
        "PART_BT2769_CX_CENTRALIZER_COMPILER_summary.json": "171f786436da34dc52c876032ee4ab80905e4808658a244de6ee43f172b067b7",
    }
    observed = {name: sha(name) for name in expected}
    checks = {name: observed[name] == digest for name, digest in expected.items()}
    assert all(checks.values()), {k: observed[k] for k, v in checks.items() if not v}
    out = {
        "schema": "w33.pass2775.ci_placed_netlist_closure.v1",
        "status": "LOCAL_DRIFT_CLOSED_REMOTE_IMPLEMENTATION_PENDING",
        "prior_failure": {
            "workflow_run": 30804032606,
            "failed_step": "Fail on certificate drift",
            "root_causes": [
                "M36 serialized floating-point overlap values were not canonical across NumPy/LAPACK versions",
                "the compiler summary was committed in hand-compacted JSON rather than generator formatting",
            ],
            "mathematical_generators_completed_before_failure": True,
            "rtl_and_pnr_steps_were_skipped": True,
        },
        "repairs": [
            "serialize exact M36 overlap labels plus rounded canonical values",
            "commit generator-formatted compiler summary",
            "split exact-certificate and RTL/P&R jobs so implementation evidence is not masked by certificate drift",
            "run exhaustive Icarus simulation, Yosys synthesis, nextpnr-ice40 placement, and icetime timing",
        ],
        "canonical_hashes": observed,
        "checks": checks,
        "implementation_boundary": "Placed utilization, timing, and power-proxy evidence becomes promoted only after the new GitHub Actions artifact is observed and parsed.",
    }
    path = DATA / "PART_BT2775_CI_PLACED_NETLIST_CLOSURE.json"
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
