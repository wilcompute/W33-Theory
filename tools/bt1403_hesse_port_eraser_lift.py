#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1403_hesse_port_eraser_lift.json"
PREVIEW_PDF = ROOT / "photonic_holonet_BT1403_preview.pdf"


def load_json(path: str) -> dict[str, Any]:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    ap.add_argument("--preview-pdf", type=Path, default=PREVIEW_PDF)
    ns = ap.parse_args()

    eraser = load_json("data/bt1396_qutrit_quantum_erasure_readout.json")
    hesse = load_json("data/bt1385_hesse_sic_t_port_abi.json")
    queue = load_json("data/bt1391_hesse_sic_t_queue_model.json")
    bt1402 = load_json("data/bt1402_photonic_manuscript_runtime_frontier.json")

    holonet = " ".join(read("photonic_holonet.tex").split())
    single_photon = " ".join(read("single_photon_universal_computation.tex").split())
    docs = " ".join(read("docs/index.html").split())

    branches = eraser["readout"]["branches"]
    branch_count = len(branches)
    sic_outcomes = hesse["resource_token"]["sic_outcomes"]
    hesse_grid = [
        {
            "h": 3 * route_trit + phase_trit,
            "route_trit": route_trit,
            "phase_trit": phase_trit,
            "branch": branches[route_trit],
            "pauli_correction": f"X^{route_trit} Z^{phase_trit}",
        }
        for route_trit in range(3)
        for phase_trit in range(3)
    ]
    preview_exists = ns.preview_pdf.exists()
    preview_size = ns.preview_pdf.stat().st_size if preview_exists else 0

    checks = {
        "eraser_verified": eraser["verified"] is True,
        "hesse_port_verified": hesse["verified"] is True,
        "bt1402_frontier_verified": bt1402["verified"] is True,
        "eraser_has_three_bell_branches": branch_count == 3,
        "hesse_is_three_by_three_lift": sic_outcomes
        == branch_count * branch_count
        == len(hesse_grid),
        "grid_covers_all_hesse_outcomes": [row["h"] for row in hesse_grid]
        == list(range(9)),
        "grid_covers_two_trit_corrections": sorted(
            (row["route_trit"], row["phase_trit"]) for row in hesse_grid
        )
        == [(a, b) for a in range(3) for b in range(3)],
        "eraser_restores_route_before_port": abs(
            eraser["readout"]["eraser_success_probability"] - (1.0 / 3.0)
        )
        < 1e-12
        and eraser["readout"]["conditional_route_l1_coherence"] == 2.0,
        "packet_boundary_returns_to_clifford_abi": "Clifford correction"
        in hesse["measurement_signature"]["feed_forward"]
        and hesse["timing_contract"]["word_ticks"] == 8,
        "queue_window_is_runtime_window": queue["window"]["ticks"] == 51840
        and queue["window"]["microframes"] == 720,
        "manuscripts_expose_eraser_lift": "BT1403 eraser-lift port" in holonet
        and "Hesse port is not a second computer" in holonet
        and "BT1403 eraser-lift port" in single_photon,
        "docs_expose_eraser_lift": "BT1403: Hesse port as eraser lift" in docs,
        "preview_pdf_built_under_distinct_name": preview_exists
        and ns.preview_pdf.name != "photonic_holonet.pdf"
        and preview_size > 100_000,
    }

    result = {
        "bt": 1403,
        "title": "Hesse-SIC/T port as a quantum-eraser lift",
        "verified": all(checks.values()),
        "checks": checks,
        "eraser_lift": {
            "route_eraser_branches": branches,
            "branch_count": branch_count,
            "hesse_sic_outcomes": sic_outcomes,
            "factorization": "9 = 3 route branches * 3 phase labels",
            "grid": hesse_grid,
            "side_record": "h = 3*route_trit + phase_trit, plus one T-frame parity bit",
        },
        "physical_reading": (
            "The quantum eraser first removes which-route information over the "
            "three Bell branches. The Hesse-SIC/T port is the same measurement "
            "boundary lifted by one phase trit, giving a 3x3 outcome alphabet "
            "whose outcome feeds the next 8-tick Clifford packet word."
        ),
        "preview_pdf": {
            "path": str(ns.preview_pdf.relative_to(ROOT)),
            "bytes": preview_size,
        },
        "boundary": (
            "BT1403 proves an ABI/alphabet lift, not physical Hesse-SIC optics, "
            "a magic-state yield, or a detector-level noise threshold."
        ),
    }

    ns.out.parent.mkdir(parents=True, exist_ok=True)
    ns.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "bt": result["bt"],
                "verified": result["verified"],
                "sic_outcomes": sic_outcomes,
                "preview_pdf_built": preview_exists,
            },
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
