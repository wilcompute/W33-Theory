"""Fail-closed regressions for the corrected Pass-4878--4882 legacy entry points."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]

LEGACY_REPLAYS = (
    (
        ROOT / "analysis" / "w33_pass4878_bose_mesner_f3_collapse.py",
        ROOT / "data" / "PART_W33_PASS4878_BOSE_MESNER_F3_COLLAPSE.json",
        "Pass 4878 correction tombstone: status=CORRECTED_BY_PASS4948",
    ),
    (
        ROOT / "analysis" / "w33_pass4879_dual_code_covering_radius.py",
        ROOT / "data" / "PART_W33_PASS4879_DUAL_CODE_COVERING_RADIUS.json",
        "Pass 4879 correction tombstone: rho(K^perp) in [6,36]",
    ),
    (
        ROOT / "analysis" / "w33_pass4880_symplectic_chart_bound.py",
        ROOT / "data" / "PART_W33_PASS4880_SYMPLECTIC_CHART_CANONICAL_BASIS.json",
        "Pass 4880 withdrawal tombstone: status=WITHDRAWN_BY_PASS4948",
    ),
    (
        ROOT / "analysis" / "w33_pass4881_agl13_wreath_extension_check.py",
        ROOT / "data" / "PART_W33_PASS4881_AGL13_WREATH_EXTENSION_CHECK.json",
        "Pass 4881 withdrawal tombstone: status=WITHDRAWN_BY_PASS4948",
    ),
    (
        ROOT / "analysis" / "w33_pass4882_pancharatnam_steiner_f3_cocycle.py",
        ROOT / "data" / "PART_W33_PASS4882_PANCHARATNAM_STEINER_COCYCLE.json",
        '"status": "WITHDRAWN_SUPERSEDED_BY_PASS4963"',
    ),
)

FALSE_PASS4801_ARTIFACTS = (
    ROOT / "PASS4801_4812_SRG_CONSTELLATION_BREAKTHROUGH.md",
    ROOT / "PASS4801_gap_verification.g",
    ROOT / "analysis" / "PASS4801_4812_srg_constellation_insert.tex",
)

REDUNDANT_PASS4946_ARTIFACTS = (
    ROOT / "analysis" / "w33_pass4946_row_point_dual.g",
    ROOT / "data" / "PART_W33_PASS4946_ROW_POINT_DUAL_GAP.json",
)


def test_legacy_entry_points_replay_to_identical_tombstones() -> None:
    frozen = {certificate: certificate.read_bytes() for _, certificate, _ in LEGACY_REPLAYS}

    for producer, certificate, marker in LEGACY_REPLAYS:
        completed = subprocess.run(
            [sys.executable, str(producer)],
            cwd=ROOT,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        assert completed.returncode == 0, completed.stdout
        assert marker in completed.stdout
        assert certificate.read_bytes() == frozen[certificate]


def test_corrected_payloads_freeze_exact_scope() -> None:
    p4878 = json.loads(LEGACY_REPLAYS[0][1].read_text())
    assert p4878["status"] == "CORRECTED_BY_PASS4948"
    replacement = p4878["authoritative_replacement"]
    assert replacement["algebra_dimension"] == 3
    assert replacement["semisimple_quotient_dimension"] == 2
    assert replacement["augmentation_layers"] == [10, 19, 10]
    assert replacement["scheme_idempotent_ranks"] == [0, 1, 39, 40]

    p4879 = json.loads(LEGACY_REPLAYS[1][1].read_text())
    assert p4879["status"] == "CORRECTED_BY_PASS4948"
    assert p4879["rho_interval"] == [6, 36]
    assert "not determined" in p4879["boundary"]

    p4880 = json.loads(LEGACY_REPLAYS[2][1].read_text())
    assert p4880["status"] == "WITHDRAWN_BY_PASS4948"
    assert "rank-24 and rank-15" in p4880["withdrawn_statement"]
    assert "No F2-to-F3 splitting" in p4880["boundary"]

    p4881 = json.loads(LEGACY_REPLAYS[3][1].read_text())
    assert p4881["status"] == "WITHDRAWN_BY_PASS4948"
    assert p4881["surviving_values"] == {
        "S3_wreath_S6_order": 33_592_320,
        "local_port_compiler_order": 6_912,
        "order_1440_groups_in_Pass4873": ["S6xC2", "Aut(S6)"],
    }
    assert "no order-1440 quotient" in p4881["boundary"]

    p4882 = json.loads(LEGACY_REPLAYS[4][1].read_text())
    assert p4882["status"] == "WITHDRAWN_SUPERSEDED_BY_PASS4963"
    assert "withdrawn, not merely left open" in p4882["boundary"]


def test_retired_artifacts_are_absent_and_docs_are_fail_closed() -> None:
    assert all(not path.exists() for path in FALSE_PASS4801_ARTIFACTS)
    assert all(not path.exists() for path in REDUNDANT_PASS4946_ARTIFACTS)

    report = (ROOT / "analysis" / "PASS4939_CHAMBER_STEINER_INTERTWINER.md").read_text()
    assert "rank-24 chamber line lane" in report
    assert "rank-24 chamber point lane" not in report

    docs = "\n".join(
        path.read_text()
        for path in (
            ROOT / "docs" / "PASS4878_4882_PERPLEXITY_FRONTIER.md",
            ROOT / "docs" / "pass4878-4882-bose-mesner-dual-compiler-pancharatnam.html",
        )
    )
    assert "corrected historical ledger" in docs.lower()
    assert "6 ≤ ρ" in docs or "6\\leq\\rho" in docs
    assert "merging the Bose-Mesner algebra to rank 2" not in docs
    assert "W33 fiber quotient ≅ Witting" not in docs
    assert "rho ∈ [10, 36]" not in docs
