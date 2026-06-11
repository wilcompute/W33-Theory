#!/usr/bin/env python3
"""BT766 — root-torsor/Q43 transport table seed generator.

BT763 defined the schema needed to promote the BT750 central half-turn r^6
into a Q(4,3) / Pluecker oriented-apartment mirror.  BT766 creates the
source-side deterministic scaffold for that future table.

It does *not* fill the Q(4,3) target apartment frames.  Those are deliberately
left unresolved until BT767's stable apartment IDs and the actual root-torsor
transport are wired in.

Default output is a compact manifest plus a small sample.  Use --emit-full to
write the full 51,840-row unresolved scaffold.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "data" / "bt766_transport_seed_scaffold_summary.json"
SAMPLE = ROOT / "data" / "bt766_transport_seed_scaffold_sample.json"
FULL = ROOT / "data" / "bt760_root_torsor_to_q43_transport.seed.json"

ROOT_TRIPLES = 540
CHIRALITIES = 2
INNER_ORDER = 48
PHASES = 6
DUOS = 2
BRANCHES = INNER_ORDER // (PHASES * DUOS)  # 4 unresolved branch/lift copies
TOTAL_ROWS = ROOT_TRIPLES * CHIRALITIES * INNER_ORDER


def row_id(tau: int, eps: int, inner: int) -> str:
    return f"tau_{tau:03d}_{eps}_{inner:02d}"


def decompose_inner(inner: int) -> dict:
    branch = inner // (PHASES * DUOS)
    residue = inner % (PHASES * DUOS)
    duo = residue // PHASES
    phase = residue % PHASES
    return {"branch": branch, "phase": phase, "duo": duo}


def compose_inner(branch: int, phase: int, duo: int) -> int:
    return branch * PHASES * DUOS + duo * PHASES + phase


def partner_inner(inner: int) -> int:
    d = decompose_inner(inner)
    return compose_inner(d["branch"], d["phase"], 1 - d["duo"])


def build_row(tau: int, eps: int, inner: int) -> dict:
    d = decompose_inner(inner)
    pin = partner_inner(inner)
    return {
        "row_id": row_id(tau, eps, inner),
        "root_triple_id": tau,
        "chirality": eps,
        "inner_coordinate": inner,
        "phase": d["phase"],
        "duo": d["duo"],
        "branch": d["branch"],
        "r6_partner_row_id": row_id(tau, eps, pin),
        "r6_action": {
            "fixed_tau": True,
            "fixed_chirality": True,
            "fixed_phase": True,
            "fixed_branch": True,
            "duo_flipped": True,
            "partner_inner_coordinate": pin,
        },
        "q43_target": {
            "status": "unresolved_pending_BT767_and_transport",
            "q43_apartment_id": None,
            "q43_oriented_frame": None,
            "q43_mirror_frame": None,
        },
    }


def iter_rows():
    for tau in range(ROOT_TRIPLES):
        for eps in range(CHIRALITIES):
            for inner in range(INNER_ORDER):
                yield build_row(tau, eps, inner)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--emit-full", action="store_true", help="write full unresolved scaffold")
    ap.add_argument("--sample-size", type=int, default=24)
    args = ap.parse_args()

    sample = []
    involution_ok = True
    phase_fixed_ok = True
    duo_flipped_ok = True
    for i, r in enumerate(iter_rows()):
        if len(sample) < args.sample_size:
            sample.append(r)
        partner = build_row(r["root_triple_id"], r["chirality"], r["r6_action"]["partner_inner_coordinate"])
        involution_ok &= partner["r6_partner_row_id"] == r["row_id"]
        phase_fixed_ok &= partner["phase"] == r["phase"]
        duo_flipped_ok &= partner["duo"] == 1 - r["duo"]

    summary = {
        "theorem": "BT766 transport table seed generator",
        "status": "source_side_seed_only",
        "root_triples": ROOT_TRIPLES,
        "chiralities": CHIRALITIES,
        "inner_centralizer_order": INNER_ORDER,
        "branches_per_phase_duo_coordinate": BRANCHES,
        "phases": PHASES,
        "duos": DUOS,
        "total_rows": TOTAL_ROWS,
        "r6_source_action": "tau, chirality, branch, and phase fixed; duo flipped",
        "checks": {
            "row_count_expected_51840": TOTAL_ROWS == 51840,
            "r6_partner_involution": involution_ok,
            "r6_fixed_phase": phase_fixed_ok,
            "r6_flips_duo": duo_flipped_ok,
        },
        "outputs": {
            "sample": str(SAMPLE.relative_to(ROOT)),
            "full_seed_when_requested": str(FULL.relative_to(ROOT)),
        },
        "boundary": "This is the BT748/BT750 source scaffold only. Q(4,3) target apartment IDs and mirror frames remain unresolved; therefore this is not a BT763 verified transport table."
    }

    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    SAMPLE.write_text(json.dumps({"rows": sample, "summary": summary}, indent=2, sort_keys=True) + "\n")
    if args.emit_full:
        payload = {
            "bt766_seed_version": "1.0",
            "status": "unresolved_source_scaffold",
            "summary": summary,
            "rows": list(iter_rows()),
        }
        FULL.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
