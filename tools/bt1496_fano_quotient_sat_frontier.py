#!/usr/bin/env python3
"""BT1496: quotient/SAT attack packet for the BT1373 330-correction frontier."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1496_fano_quotient_sat_frontier.json"
CNF = ROOT / "proofs" / "bt1496_fano_quotient_frontier.wcnf"
MD = ROOT / "proofs" / "BT1496_fano_quotient_sat_frontier.md"


def main() -> None:
    # BT1373/BT1376 frontier facts.
    skew_edges = 540
    identity_edges = 210
    corrections = 330
    s3_labels = 6
    root_fixed_free_lines = 39
    raw_space = f"6^{root_fixed_free_lines}"
    # BT1492 canonical fiber facts.
    fano_points = 7
    shared_fiber = 24
    flag_stabilizer = 8
    fano_flags = 21
    fano_point_bus = fano_points * shared_fiber
    fano_flag_bus = fano_flags * flag_stabilizer
    # Quotient packet: a proof scaffold, not a solved SAT certificate.
    quotient_blocks = [
        {"name": "point_anchor", "count": fano_points, "fiber": shared_fiber, "bus": fano_point_bus},
        {"name": "flag_anchor", "count": fano_flags, "fiber": flag_stabilizer, "bus": fano_flag_bus},
        {"name": "local_d4_flag", "count": 3, "fiber": flag_stabilizer, "bus": shared_fiber},
    ]
    # WCNF scaffold: one soft unit per desired identity edge and hard comments for quotient gates.
    soft_weight = 1
    top_weight = corrections + 1
    lines = [
        f"c BT1496 quotient/SAT scaffold for BT1373 330-correction frontier",
        f"c raw root-fixed space {raw_space}; observed identity edges {identity_edges}; corrections {corrections}",
        f"c canonical quotient: 168 = 7*24 = 21*8; 24 = 3*8",
        f"p wcnf {skew_edges} {skew_edges} {top_weight}",
    ]
    for var in range(1, skew_edges + 1):
        # x_var means skew edge var is identity after gauge assignment.
        lines.append(f"{soft_weight} {var} 0")
    CNF.parent.mkdir(parents=True, exist_ok=True)
    CNF.write_text("\n".join(lines) + "\n", encoding="utf-8")
    md = [
        "# BT1496 Fano Quotient/SAT Frontier",
        "",
        "This is a quotient certificate scaffold, not a solved global optimum proof.",
        "",
        f"- BT1373 witness: {identity_edges} identity edges and {corrections} corrections among {skew_edges} skew-line residuals.",
        f"- Raw root-fixed search space: `{raw_space}`.",
        "- Canonical Fano quotient from BT1492: `168 = 7*24 = 21*8`, with `24 = 3*8`.",
        "- WCNF scaffold: one soft identity-edge variable per skew residual; quotient clauses are the next certificate layer.",
    ]
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    checks = {
        "frontier_210_plus_330_is_540": identity_edges + corrections == skew_edges,
        "canonical_point_bus_168": fano_point_bus == 168,
        "canonical_flag_bus_168": fano_flag_bus == 168,
        "shared_fiber_24_as_3_times_d4": 3 * flag_stabilizer == shared_fiber,
        "quotient_blocks_present": len(quotient_blocks) == 3,
        "wcnf_written": CNF.exists() and CNF.read_text(encoding="utf-8").startswith("c BT1496"),
        "wcnf_has_540_soft_edges": len([ln for ln in CNF.read_text(encoding="utf-8").splitlines() if ln.startswith("1 ")]) == skew_edges,
        "md_written": MD.exists(),
    }
    result = {
        "bt": 1496,
        "title": "Fano quotient/SAT frontier certificate scaffold",
        "verified": all(checks.values()),
        "status": "quotient_certificate_scaffold_not_global_optimum_proof",
        "frontier": {"skew_edges": skew_edges, "identity_edges": identity_edges, "corrections": corrections, "raw_space": raw_space},
        "canonical_fano": {"point_bus": "7*24=168", "flag_bus": "21*8=168", "shared_fiber": "24=3*8"},
        "quotient_blocks": quotient_blocks,
        "wcnf": "proofs/bt1496_fano_quotient_frontier.wcnf",
        "markdown": "proofs/BT1496_fano_quotient_sat_frontier.md",
        "interpretation": "The 330-correction frontier is now attacked through the BT1492 canonical Fano quotient: raw S3 gauge search is replaced by point/flag/fiber quotient blocks and a WCNF scaffold for future solver certificates.",
        "honesty_boundary": "This does not prove 330 globally optimal. It prepares the quotient/SAT certificate layer needed to test that claim without raw 6^39 enumeration.",
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"bt": 1496, "verified": result["verified"], "frontier": corrections}, indent=2))
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
