"""Pass 1140 regression for the shifted-adjacency publication repair.

{shifted-adjacency:corrected}
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


propagator = load_module(
    "pass1140_propagator",
    ROOT / "analysis" / "w33_propagator_spectral_action.py",
)
guard = load_module(
    "pass1140_guard",
    ROOT / "scripts" / "check_shifted_adjacency_descendants.py",
)
legacy_scanner = load_module(
    "pass1140_legacy_scanner",
    ROOT / "analysis" / "w33_false_cubic_quarantine_scanner.py",
)


def test_corrected_propagator_uses_exact_projectors_heat_and_zeta() -> None:
    moments = [
        propagator.trace_power(propagator.EIGENVALUES, n)
        for n in range(6)
    ]
    assert moments == [40, -40, 520, -520, 24040, 114200]

    tr_i, tr_d, tr_d2 = 40, moments[1], moments[2]
    ranks = [
        Fraction(tr_d2 + 4 * tr_d - 5 * tr_i, 160),
        Fraction(-(tr_d2 - 6 * tr_d - 55 * tr_i), 60),
        Fraction(tr_d2 - 12 * tr_d + 11 * tr_i, 96),
    ]
    assert ranks == [1, 24, 15]
    assert propagator.absolute_zeta(2) == (
        Fraction(1, 121) + 24 + Fraction(15, 25)
    )
    assert propagator.squared_zeta(1) == propagator.absolute_zeta(2)


def test_corrected_propagator_certificate_is_deterministic_and_passes() -> None:
    path = ROOT / "data" / "PROPAGATOR_2026_07_27_spectral_action.json"
    propagator.main()
    first = path.read_bytes()
    propagator.main()
    second = path.read_bytes()
    assert second == first
    cert = json.loads(second)
    assert cert["schema"] == "w33.pass1140.corrected_propagator.v1"
    assert cert["status"] == "PASS"
    assert cert["all_checks_pass"] is True
    assert cert["projector_rank_check"]["correct_1_24_15"] == [
        True,
        True,
        True,
    ]
    assert cert["signed_semigroup_trace"]["is_positive_heat"] is False
    assert cert["zeta_semantics"]["signed_requires_spectral_cut"] is True


def test_primary_publications_state_the_true_cubic_and_switch() -> None:
    for filename in ("w33_paper.tex", "W33_FOR_EVERYONE.tex"):
        text = (ROOT / filename).read_text(encoding="utf-8")
        assert (
            "(D-11I)(D-I)(D+5I)" in text
            or "(t-11)(t-1)(t+5)" in text
        )
        assert "13I+4\\overline A" in text
        assert "288D" in text
        assert not guard.scan_text(text)

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "there are 28 non-isomorphic graphs" in readme
    assert "parameters do not identify the graph" in readme


def test_legacy_manuscripts_have_visible_status_boundaries() -> None:
    w36 = (ROOT / "W36_PAPER.tex").read_text(encoding="utf-8")
    v2 = (ROOT / "w33_paper_v2.tex").read_text(encoding="utf-8")
    assert "Status: superseded historical synthesis" in w36
    assert "Audited finite conclusion" in w36
    assert "Superseded development draft" in v2
    assert "archived development draft" in v2
    assert guard.INLINE_RETRACTION in w36
    assert guard.INLINE_RETRACTION in v2


def test_negative_literal_detection_and_pruned_walk(tmp_path: Path) -> None:
    literal = "The historical spectrum {-7, -1, 5} is retracted."
    assert "old_spectrum" in guard.scan_text(literal)
    assert any(
        label == "old_eigenvalue_set"
        and re.search(pattern, literal, re.IGNORECASE)
        for pattern, label in legacy_scanner.FALSE_PATTERNS
    )

    (tmp_path / "analysis").mkdir()
    (tmp_path / "analysis" / "visible.tex").write_text("visible", encoding="utf-8")
    (tmp_path / "formal" / ".lake").mkdir(parents=True)
    (tmp_path / "formal" / ".lake" / "hidden.tex").write_text("hidden", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "object.txt").write_text("hidden", encoding="utf-8")
    found = {
        path.relative_to(tmp_path).as_posix()
        for path in guard.iter_files(tmp_path)
    }
    assert found == {"analysis/visible.tex"}


def test_full_audit_report_is_honest_and_closed() -> None:
    report = json.loads(
        (
            ROOT / "data" / "w33_shifted_adjacency_descendant_audit.json"
        ).read_text(encoding="utf-8")
    )
    assert report["status"] == "PASS"
    assert report["summary"]["unregistered_active_descendants"] == 0
    assert report["summary"]["matched_files"] == report["summary"]["registered_or_archival"]
    assert report["violations"] == []

    ledger = json.loads(
        (
            ROOT / "data" / "w33_shifted_adjacency_retraction_ledger.json"
        ).read_text(encoding="utf-8")
    )
    assert ledger["schema"] == "w33.shifted_adjacency.retraction_ledger.v4"
    assert ledger["primary_blob_manifest"].endswith(
        "PRIMARY_BLOB_MANIFEST.json"
    )
    assert all(
        "pending" not in status.lower()
        for status in ledger["known_descendants"].values()
    )
    assert ledger["pass1150_completion"]["pending_after"] == 0
    assert ledger["pass1150_completion"]["report"].endswith(
        "w33_pass1150_shifted_adjacency_completion.json"
    )
    assert "RETRACTION_STUB" in ledger["known_descendants"][
        "analysis/w33_BREAKTHROUGH_58_master_cubic_Z_anomaly.py"
    ].upper()
