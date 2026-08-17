from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ANALYSIS = ROOT / "analysis"

SOURCE_NAMES = [
    "w33_pass5699_tower_artin_L_factorization.py",
    "w33_pass5700_girth_cycle_group_order_identity.py",
    "w33_pass5701_exact_psd_ramanujan_certificates.py",
    "w33_pass5702_kestent_mckay_equidistribution.py",
    "w33_pass5703_w39_independence_replication.py",
]
CERT_NAMES = [
    "PART_W33_PASS5699_TOWER_ARTIN_L_FACTORIZATION.json",
    "PART_W33_PASS5700_GIRTH_CYCLE_GROUP_ORDER_IDENTITY.json",
    "PART_W33_PASS5701_EXACT_PSD_RAMANUJAN_CERTIFICATES.json",
    "PART_W33_PASS5702_KESTEN_MCKAY_EQUIDISTRIBUTION.json",
    "PART_W33_PASS5703_W39_INDEPENDENCE_REPLICATION.json",
]


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def test_5699_is_separate_finite_artin_tower() -> None:
    cert = load(CERT_NAMES[0])
    assert cert["pass"] == 5699
    assert cert["status"] == "SEPARATE_DETERMINISTIC_FACTOR_PAIR_TOWER_ARTIN_FACTORIZATION_THROUGH_640"
    assert "not the frozen Pass5683/5693 tower" in cert["tower_provenance"]
    assert "no isomorphism" in cert["tower_provenance"]
    assert cert["spectrum_split_exact_by_2lift_block_conjugation"] is True
    assert cert["numeric_spectrum_split_error_below_1e_10_each_level"] == [True, True, True]
    assert cert["base_closed_form_verified"] is True
    assert [row["vertices"] for row in cert["unsigned_poles"]] == [80, 160, 320, 640]
    assert all(row["off_circle"] == 0 for row in cert["signed_L_function_poles"])
    assert "not Pass5696" in cert["non_identification"]
    assert "partition function" in cert["physics_boundary"]


def test_5700_orbits_are_root_grades_not_chirality() -> None:
    cert = load(CERT_NAMES[1])
    assert cert["master_identity"] == (
        "Tr(A_levi^8) = 193280 = 80*2092 + 25920 = n*M8_tree + |PSp(4,3)|"
    )
    assert cert["tower_excess"] == [25920, 25600, 25216, 24928]
    assert cert["tower_girth"] == [8, 8, 8, 8]
    cycles = cert["cycle_space"]
    assert cycles["unrooted_8cycles"] == 1620
    assert cycles["ordered_cycle_encodings"] == 25920
    assert cycles["root_grade_orbits"] == {
        "line_rooted": 12960,
        "point_rooted": 12960,
        "stabilizer_order_each": 2,
    }
    assert cycles["separator"] == (
        "initial vertex belongs to the point grade or the line grade; this is not chirality"
    )
    assert "No W(E6) point-line merger" in cycles["duality_firewall"]


def test_5701_exact_positive_definiteness_has_bounded_scope() -> None:
    cert = load(CERT_NAMES[2])
    assert cert["status"] == (
        "EXACT_POSITIVITY_FOR_THREE_SEPARATE_FACTOR_PAIR_LIFTS_THROUGH_640_VERTICES"
    )
    rows = cert["certificates"]
    assert [row["signed_parent_n"] for row in rows] == [80, 160, 320]
    assert all(row["B_eq_12I_minus_As2_positive_definite"] for row in rows)
    assert [row["n_pivots"] for row in rows] == [80, 160, 320]
    assert "no 640-parent signing" in cert["scope"]


def test_5702_is_sampled_cdf_diagnostic_not_ks_or_goe() -> None:
    cert = load(CERT_NAMES[3])
    contract = cert["sampling_contract"]
    assert contract == {
        "is_exact_KS_statistic": False,
        "lambda_grid_points": 241,
        "quadrature": "double-precision trapezoidal",
        "quadrature_panels_per_cdf_value": 4000,
        "rigorous_quadrature_error_bound": None,
    }
    assert [row["sampled_cdf_discrepancy"] for row in cert["sampled_cdf_discrepancies"]] == [
        0.02102,
        0.01079,
        0.0054,
    ]
    for row in cert["moment_matching"]:
        assert [row[f"diff{degree}_exact"] for degree in (2, 4, 6)] == ["0", "0", "0"]
    assert "no rate or all-level limit" in cert["finite_observation"]
    assert "no GOE" in cert["physics_boundary"]


def test_5703_is_explicit_pass5226_5227_rediscovery() -> None:
    cert = load(CERT_NAMES[4])
    assert cert["graph"]["srg"] == [820, 90, 8, 10]
    assert cert["prior_owner"] == {
        "certified_lower_witness": 50,
        "file": "data/PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json",
        "hoffman_upper_bound": 82,
        "randomized_greedy_baseline": 46,
    }
    assert cert["repo_bounds"] == {
        "exact_alpha_settled": False,
        "lower_witness": 50,
        "upper_hoffman": 82,
    }
    assert "no new independence-number result" in cert["verdict"]


def test_q5_file_is_an_executable_tombstone() -> None:
    source = (ANALYSIS / "PASS5703_Q5_TRANSITIVE_IDENTIFICATION.g").read_text(encoding="utf-8")
    assert "OBSOLETE" in source
    assert "Pass5667-5674" in source
    assert "TransitiveIdentification(" not in source
    gap = shutil.which("gap")
    if gap:
        proc = subprocess.run(
            [gap, "-q", str(ANALYSIS / "PASS5703_Q5_TRANSITIVE_IDENTIFICATION.g")],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        assert "OBSOLETE" in proc.stdout


def test_publication_sources_quarantine_withdrawn_claims() -> None:
    paths = [
        ANALYSIS / "PASS5699_5703_tower_zeta_frontier_report.md",
        ANALYSIS / "PASS5699_5703_tower_zeta_insert.tex",
        ANALYSIS / "PASS5699_5703_index_insert.html",
        ANALYSIS / "PASS5699_5703_external_prior_art_and_corrections.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    forbidden = [
        "orientation-twisted sector partition functions",
        "symplectic chirality invariant",
        "Eigenphase spacings sit near GOE",
        "51 <= alpha <= 80",
        "51\\le\\alpha",
        "merge into a regular action",
    ]
    assert not any(token in text for token in forbidden)
    assert "point-rooted" in text and "line-rooted" in text
    assert "5226" in text and "5227" in text
    assert "Pass5706" in text and "does not continue Pass5699" in text


def test_full_replay_is_byte_identical(tmp_path: Path) -> None:
    analysis = tmp_path / "analysis"
    data = tmp_path / "data"
    analysis.mkdir()
    data.mkdir()
    for name in SOURCE_NAMES:
        shutil.copy2(ANALYSIS / name, analysis / name)
    shutil.copy2(ANALYSIS / "w33_pass5699_5703_runner.py", analysis / "w33_pass5699_5703_runner.py")
    shutil.copy2(
        DATA / "PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json",
        data / "PART_W33_PASS5226_5227_ODD_Q_OVOID_DEFICIENCY.json",
    )
    proc = subprocess.run(
        [sys.executable, str(analysis / "w33_pass5699_5703_runner.py")],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert "PASS5699_5703_CORRECTED_REPLAY_OK" in proc.stdout
    for name in CERT_NAMES:
        assert (data / name).read_bytes() == (DATA / name).read_bytes()
