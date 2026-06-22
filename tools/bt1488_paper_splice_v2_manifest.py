#!/usr/bin/env python3
"""BT1488: paper splice v2 manifest for the ABI/E6/D4 frontier."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "bt1488_paper_splice_v2_manifest.json"
MD = ROOT / "analysis" / "BT1488_paper_splice_v2_manifest.md"
INSERT = ROOT / "analysis" / "BT1486_BT1488_holonet_insert.tex"


def load_json(relpath: str) -> dict:
    return json.loads((ROOT / relpath).read_text(encoding="utf-8"))


def exists(relpath: str) -> bool:
    return (ROOT / relpath).exists()


def main() -> None:
    bt1479 = load_json("data/bt1479_splice_cascade_manifest.json")
    bt1484 = load_json("data/bt1484_e6_dag_claim_table_v2.json")
    bt1486 = load_json("data/bt1486_retwined_css_from_abi_v2.json")
    bt1487 = load_json("data/bt1487_v4_triangle_stabilizer_classifier.json")

    cascade = [
        {
            "order": 1,
            "name": "claim_firewalled_section",
            "target": "photonic_holonet.tex",
            "insert": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "dependency": "BT1457",
            "status": "section root remains preferred firewall",
        },
        {
            "order": 2,
            "name": "claim_dependency_table_v2",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1484_e6_dag_claim_table_v2.tex",
            "replaces": "analysis/BT1472_dag_claim_table.tex",
            "dependency": "BT1484",
            "status": "preferred; BT1472 retained only as superseded v1 provenance",
        },
        {
            "order": 3,
            "name": "css_join_proof_table",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1474_css_join_proof_table.tex",
            "dependency": "BT1474",
            "status": "preferred exact finite CSS join table",
        },
        {
            "order": 4,
            "name": "tensor_product_grid_reading",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1480_tensor_product_grid_reading.tex",
            "dependency": "BT1480",
            "status": "preferred exact finite C3 x V4 grid reading",
        },
        {
            "order": 5,
            "name": "closure_abi_v2_packet",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "analysis/BT1480_BT1482_holonet_insert.tex",
            "dependency": "BT1482",
            "status": "preferred runtime ABI packet",
        },
        {
            "order": 6,
            "name": "retwined_css_abi_v2_join",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "data/bt1486_retwined_css_from_abi_v2.json",
            "dependency": "BT1486",
            "status": "new exact row-level verification",
        },
        {
            "order": 7,
            "name": "v4_triangle_stabilizer_classifier",
            "target": "analysis/BT1457_claim_firewalled_holonet_section.tex",
            "insert": "data/bt1487_v4_triangle_stabilizer_classifier.json",
            "dependency": "BT1487",
            "status": "new Fano-aware branch stabilizer classifier",
        },
        {
            "order": 8,
            "name": "rendered_equation_fill",
            "target": "data/bt1473_scirp_prefilled_transcription_packet.csv and paper section",
            "insert": "transcribed formulas for equations 49,50,64,65,66",
            "dependency": "rendered equation images acquired",
            "status": "blocked pending rendered formula transcription; no external code repository is assumed",
        },
    ]

    preferred_exact_packet = [
        "BT1474_css_join_proof_table",
        "BT1480_tensor_product_grid_reading",
        "BT1482_closure_abi_v2",
        "BT1484_e6_dag_claim_table_v2",
        "BT1486_retwined_css_from_abi_v2",
        "BT1487_v4_triangle_stabilizer_classifier",
    ]

    insert = r"""\subsection{BT1486--BT1488 ABI v2 retwined CSS and splice manifest}
\label{sec:bt1486-bt1488-abi-v2-css-splice}

BT1486 reruns the CSS join from the ABI v2 consumer output.  The result is not
just the old 72-row count: every row satisfies the retwined \(X\)- and
\(Z\)-syndrome checks, while the \(C_3\) channel profile remains
\(P_0=P_1=P_2=24\) rows and the \(V_4\) triangle profile remains
\(T_0=T_1=T_2=T_3=18\) rows.

BT1487 classifies the branch symmetries behind those four triangles.  The full
triangle-partition stabilizer is \(S_4\) of order \(24\), giving the Fano point
reading \(7\cdot24=168\).  The physically used square subgroup is \(D_4\) of
order \(8\), giving the Fano flag reading \(21\cdot8=168\).  Thus the active
detector-bin count is Fano-native, not merely an optical count.

BT1488 updates the splice cascade: the E6 claim table v2 from BT1484 supersedes
the BT1472 table as the preferred paper table, and the preferred exact finite
insert packet is now BT1474, BT1480, BT1482, BT1484, BT1486, and BT1487.  The
Golden Quartic/Moebius-ball equation fill remains blocked pending rendered
formula transcription; no public source-code repository is assumed.
"""
    INSERT.write_text(insert, encoding="utf-8")

    md = [
        "# BT1488 Paper Splice v2 Manifest",
        "",
        "BT1488 supersedes the BT1479 manifest without deleting v1 provenance.",
        "",
        "| order | name | insert | dependency | status |",
        "|---:|---|---|---|---|",
    ]
    for row in cascade:
        md.append(
            f"| {row['order']} | {row['name']} | {row['insert']} | "
            f"{row['dependency']} | {row['status']} |"
        )
    md.extend(
        [
            "",
            "Preferred exact finite insert packet:",
            "",
            *[f"- {item}" for item in preferred_exact_packet],
            "",
            "BT1472 remains provenance only; BT1484 is the preferred claim table.",
        ]
    )
    MD.write_text("\n".join(md) + "\n", encoding="utf-8")

    checks = {
        "bt1479_v1_manifest_loaded": bt1479["verified"] is True,
        "bt1484_table_v2_loaded": bt1484["verified"] is True,
        "bt1486_css_join_loaded": bt1486["verified"] is True,
        "bt1487_classifier_loaded": bt1487["verified"] is True,
        "cascade_orders_are_1_to_8": [row["order"] for row in cascade]
        == list(range(1, 9)),
        "bt1484_replaces_bt1472": cascade[1]["insert"]
        == "analysis/BT1484_e6_dag_claim_table_v2.tex"
        and cascade[1]["replaces"] == "analysis/BT1472_dag_claim_table.tex",
        "preferred_packet_contains_bt1474_bt1480_bt1482": all(
            item in preferred_exact_packet
            for item in [
                "BT1474_css_join_proof_table",
                "BT1480_tensor_product_grid_reading",
                "BT1482_closure_abi_v2",
            ]
        ),
        "preferred_packet_contains_new_bt1486_bt1487": all(
            item in preferred_exact_packet
            for item in [
                "BT1486_retwined_css_from_abi_v2",
                "BT1487_v4_triangle_stabilizer_classifier",
            ]
        ),
        "blocked_formula_fill_remains_last": cascade[-1]["name"]
        == "rendered_equation_fill"
        and "blocked" in cascade[-1]["status"],
        "all_declared_insert_files_exist_or_are_data_contracts": all(
            exists(row["insert"]) or row["insert"].startswith("transcribed formulas")
            for row in cascade
        ),
        "markdown_written": MD.exists()
        and "BT1484 is the preferred claim table" in MD.read_text(encoding="utf-8"),
        "holonet_insert_written": INSERT.exists()
        and "BT1486 reruns the CSS join" in INSERT.read_text(encoding="utf-8"),
    }
    result = {
        "bt": 1488,
        "title": "Paper splice v2 manifest",
        "verified": all(checks.values()),
        "supersedes": "data/bt1479_splice_cascade_manifest.json",
        "cascade": cascade,
        "preferred_exact_finite_insert_packet": preferred_exact_packet,
        "markdown": "analysis/BT1488_paper_splice_v2_manifest.md",
        "holonet_insert": "analysis/BT1486_BT1488_holonet_insert.tex",
        "interpretation": (
            "BT1488 makes BT1484 the preferred E6-aware claim table and promotes "
            "BT1474/BT1480/BT1482 plus BT1486/BT1487 as the exact finite paper "
            "splice packet.  Formula-level Otto claims remain blocked."
        ),
        "checks": checks,
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {"bt": 1488, "verified": result["verified"], "steps": len(cascade)},
            indent=2,
        )
    )
    if not result["verified"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
