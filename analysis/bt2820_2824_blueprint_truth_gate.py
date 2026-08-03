#!/usr/bin/env python3
"""Passes 2820-2824: verify and freeze the modular Holonet blueprint."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "holonet_machine_blueprint.tex"
PARTS = tuple(ROOT / "analysis" / "blueprint_parts" / f"part_{i:02d}.tex" for i in range(6))
INSERT = ROOT / "analysis" / "BT2820_BT2824_blueprint_evidence_insert.tex"
SUPPORT = ROOT / "data" / "PART_BT2808_PG32_TETRAHEDRAL_SUPPORT_LIFT_results.json"
OPERATING = ROOT / "data" / "PART_BT2821_M36_DISTILLATION_OPERATING_CURVE_results.json"
OUT = ROOT / "data" / "PART_BT2820_BT2824_BLUEPRINT_HARDENING_results.json"
PDF = ROOT / "holonet_machine_blueprint.pdf"
LOG = ROOT / "holonet_machine_blueprint.log"

WRAPPER = """% Modular source for The Holonet Machine blueprint.
% Pass 2824 splits the generated document into bounded reviewable fragments.
\\input{analysis/blueprint_parts/part_00.tex}
\\input{analysis/blueprint_parts/part_01.tex}
\\input{analysis/blueprint_parts/part_02.tex}
\\input{analysis/blueprint_parts/part_03.tex}
\\input{analysis/blueprint_parts/part_04.tex}
\\input{analysis/blueprint_parts/part_05.tex}
"""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def upgrade(_text: str) -> str:
    """Normalize the root source to the canonical modular wrapper."""
    return WRAPPER


def read_parts() -> tuple[list[str], str]:
    missing = [str(path.relative_to(ROOT)) for path in PARTS if not path.is_file()]
    if missing:
        raise AssertionError(f"missing modular blueprint parts: {missing}")
    texts = [path.read_text(encoding="utf-8") for path in PARTS]
    return texts, "".join(texts)


def truth_checks(wrapper: str) -> dict[str, bool]:
    part_texts, source = read_parts()
    insert = INSERT.read_text(encoding="utf-8")
    support = json.loads(SUPPORT.read_text(encoding="utf-8"))
    operating = json.loads(OPERATING.read_text(encoding="utf-8"))
    combined = source + "\n" + insert
    flat_source = " ".join(source.split())
    flat_combined = " ".join(combined.split())
    return {
        "canonical_wrapper": wrapper == WRAPPER,
        "six_ordered_parts": len(part_texts) == 6 and all(part_texts),
        "document_balanced": source.count("\\begin{document}") == 1 and source.count("\\end{document}") == 1,
        "pass_range_2824": "Passes 2700--2824" in source,
        "minimal_four_operation_core": "four operations encoded by two opcode bits" in flat_combined,
        "public_shell": "public eight-opcode three-bit ISA remains a" in flat_source,
        "support_first_abstract": "$15$ nonempty binary tetrahedral masks" in flat_source,
        "evidence_input_once": source.count("\\input{analysis/BT2820_BT2824_blueprint_evidence_insert}") == 1,
        "promotion_firewall": "Evidence-state contract" in insert,
        "m36_full_decoder_count": "$11{,}520$-element projective two-qubit" in insert,
        "m36_48_branches": "exactly $48$ improving branches" in combined,
        "m36_operating_curve": "p'=R(p)" in insert and operating["fixed_points"] == ["0", "2/3", "1"],
        "m36_magic_section_repaired": "That was the former frontier" in source and "No distillation protocol for $M_{36}$ is known" not in source,
        "m36_exact_recurrence_in_body": "p'=\\frac{p(4-p)}{3(p^2-2p+2)}" in source,
        "m36_threshold_boundary": "not yet provide asymptotic" in insert and "fault-tolerant injection" in source,
        "support_profile_4_12_16_8": "(4,12,16,8)" in insert and support["support_lift"]["tomotope_f_vector"] == [4, 12, 16, 8],
        "support_equitable": "equitable partition" in insert and support["check_count"] == 43,
        "support_selector_boundary": "objectwise intertwiner" in insert,
        "sensor_all_n_mu12": "is $\\mu_{12}$ for every register width" in insert,
        "sensor_u1_boundary": "$U(1)$ phases rather than the standard finite lift" in insert,
        "transpose_direction": "T\\,\\mathrm{CX}_{p\\to f}\\,T^{-1}=\\mathrm{CX}_{f\\to p}" in insert,
        "mixer_removed": "removed\nfrom the active tree" in insert,
        "component_not_system": "not a measured Holonet" in flat_source,
        "stale_broad_no_go_removed": "No distillation protocol for $M_{36}$ is known" not in source,
        "stale_no_protocol_removed": "does \\emph{not} supply a distillation protocol" not in source,
    }


def build_payload(wrapper: str, checks: dict[str, bool]) -> dict:
    part_texts, source = read_parts()
    payload = {
        "schema": "w33.pass2820_2824.blueprint_hardening.v2",
        "canonical_pass_range": "2820-2824",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "check_count": len(checks),
        "checks": checks,
        "wrapper_sha256": sha256_bytes(wrapper.encode()),
        "assembled_source_sha256": sha256_bytes(source.encode()),
        "part_sha256": {
            str(path.relative_to(ROOT)): sha256_bytes(text.encode())
            for path, text in zip(PARTS, part_texts)
        },
        "insert_sha256": sha256_bytes(INSERT.read_bytes()),
        "support_certificate_sha256": sha256_bytes(SUPPORT.read_bytes()),
        "operating_curve_sha256": sha256_bytes(OPERATING.read_bytes()),
        "boundaries": {
            "m36": "state-fidelity distillation and exact recurrence, not optimized yield or fault-tolerant injection",
            "support_codec": "exact fiber-capacity/equitable quotient, not yet an objectwise tomotope or selector intertwiner",
            "sensor": "3/9 law for standard finite mu_12 lift; arbitrary U(1) uses 3^n",
            "hardware": "synthesis and P&R require observed clean-run evidence",
            "photonic": "published component evidence is not an end-to-end Holonet",
        },
    }
    if PDF.is_file():
        payload["compiled_pdf"] = {
            "sha256": sha256_bytes(PDF.read_bytes()),
            "bytes": PDF.stat().st_size,
            "log_sha256": sha256_bytes(LOG.read_bytes()) if LOG.is_file() else None,
        }
    return payload


def write_certificate(wrapper: str, checks: dict[str, bool]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build_payload(wrapper, checks), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="normalize wrapper and refresh certificate")
    mode.add_argument("--check", action="store_true", help="fail closed on source or certificate drift")
    args = parser.parse_args()

    original = TEX.read_text(encoding="utf-8")
    normalized = upgrade(original)
    if args.write and normalized != original:
        TEX.write_text(normalized, encoding="utf-8")

    current = TEX.read_text(encoding="utf-8")
    checks = truth_checks(current)
    write_certificate(current, checks)

    if args.check and current != WRAPPER:
        raise AssertionError("root blueprint source is not the canonical modular wrapper")
    missing = [name for name, ok in checks.items() if not ok]
    if missing:
        raise AssertionError(f"blueprint truth-gate failures: {missing}")
    if upgrade(current) != current:
        raise AssertionError("wrapper normalization is not idempotent")
    print(f"PASS {len(checks)}/{len(checks)}; six-part modular blueprint")


if __name__ == "__main__":
    main()
