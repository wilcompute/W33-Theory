"""Tests for Pillar 110 (Part CCX): CE2 Table-Free Seed Transport Law."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCX_CE2_SEED_TRANSPORT import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Seed-transport for C0
# ---------------------------------------------------------------------------

class TestT1SeedTransportC0:
    """T1: C0[t][d](s,w) = C0[t][d0](pullback) + DeltaC0_B(w) for all inputs."""

    def test_c0_all_pass(self, summary):
        """All C0 transport checks pass."""
        assert summary["T1_c0_all_pass"] is True

    def test_c0_passes_count(self, summary):
        """All 126 C0 checks pass (7 dirs x 2 t-values x 9 sw-pairs)."""
        assert summary["T1_c0_passes"] == 126

    def test_total_checks(self, summary):
        """Total checks = 126 (7 non-seed dirs x 2 types x 9 sw inputs)."""
        assert summary["T1_checks_total"] == 126

    def test_7_times_2_times_9(self, summary):
        """126 = 7 directions x 2 t-values x 9 (s,w) pairs."""
        assert summary["T1_checks_total"] == 7 * 2 * 9


# ---------------------------------------------------------------------------
# T2: Seed-transport for E
# ---------------------------------------------------------------------------

class TestT2SeedTransportE:
    """T2: E[t][d](s,w) = E[t][d0](pullback) + DeltaE_{B,t}(s,w) for all inputs."""

    def test_e_all_pass(self, summary):
        """All E transport checks pass."""
        assert summary["T2_e_all_pass"] is True

    def test_e_passes_count(self, summary):
        """All 126 E checks pass."""
        assert summary["T2_e_passes"] == 126

    def test_no_failures(self, summary):
        """Zero failures in transport law verification."""
        assert summary["T2_num_failures"] == 0

    def test_combined_pass(self, summary):
        """Both C0 and E transport laws verified simultaneously."""
        assert summary["T2_all_pass"] is True


# ---------------------------------------------------------------------------
# T3: DeltaC0 structure
# ---------------------------------------------------------------------------

class TestT3DeltaC0Structure:
    """T3: DeltaC0_B(w) is w-only (rows for s^1 and s^2 vanish) polynomial over F3."""

    def test_dc0_w_only(self, summary):
        """DeltaC0 depends only on w (s-rows are all zero)."""
        assert summary["T3_dc0_w_only"] is True

    def test_7_dc0_polys(self, summary):
        """Exactly 7 DeltaC0 polynomials (one per non-seed direction)."""
        assert summary["T3_num_dc0_polys"] == 7

    def test_one_trivial_dc0(self, summary):
        """Exactly 1 DeltaC0 is identically zero."""
        assert summary["T3_trivial_dc0_count"] == 1


# ---------------------------------------------------------------------------
# T4: DeltaE structure
# ---------------------------------------------------------------------------

class TestT4DeltaEStructure:
    """T4: DeltaE_{B,t}(s,w) depends on both B and t; t=1 vs t=2 differ for all B."""

    def test_all_t_differ(self, summary):
        """For every B, DeltaE with t=1 differs from t=2."""
        assert summary["T4_all_t_differ"] is True

    def test_de_t_dependent_count(self, summary):
        """All 7 B-values have t-dependent DeltaE."""
        assert summary["T4_de_t_dependent_count"] == 7

    def test_14_de_polys(self, summary):
        """14 DeltaE polynomials: 7 B-values x 2 t-values."""
        assert summary["T4_num_de_polys"] == 14


# ---------------------------------------------------------------------------
# T5: SL(2,3) equivariance
# ---------------------------------------------------------------------------

class TestT5SL2F3Equivariance:
    """T5: Coverage complete — all 7 non-seed directions have a unique canonical B."""

    def test_coverage_complete(self, summary):
        """All 7 non-seed directions are covered."""
        assert summary["T5_coverage_complete"] is True

    def test_7_directions_covered(self, summary):
        """Exactly 7 non-seed directions covered."""
        assert summary["T5_directions_covered"] == 7

    def test_7_delta_c0_entries(self, summary):
        """7 DeltaC0 polynomials (one per direction)."""
        assert summary["T5_delta_c0_entries"] == 7

    def test_7_delta_e_entries(self, summary):
        """7 B-keyed DeltaE polynomial dicts."""
        assert summary["T5_delta_e_entries"] == 7

    def test_sl2f3_order_24(self, summary):
        """SL(2,3) has order 24."""
        assert summary["T5_sl2f3_order"] == 24


# ---------------------------------------------------------------------------
# T6: Table completeness from seed
# ---------------------------------------------------------------------------

class TestT6TableCompleteness:
    """T6: 21 Delta polynomials (7 C0 + 14 E) completely determine all 16 tables."""

    def test_total_tables(self, summary):
        """16 total tables: 2 t-values x 8 directions."""
        assert summary["T6_total_tables"] == 16

    def test_2_seed_tables(self, summary):
        """2 seed tables: C0[t][d0] and E[t][d0] for t=1,2."""
        assert summary["T6_seed_tables"] == 2

    def test_21_delta_polys(self, summary):
        """21 Delta polynomials: 7 DeltaC0 + 14 DeltaE."""
        assert summary["T6_total_delta_polys"] == 21

    def test_completeness(self, summary):
        """Completeness flag is True (21 = 7 + 7*2)."""
        assert summary["T6_completeness"] is True

    def test_21_equals_7_plus_14(self, summary):
        """21 = 7 DeltaC0 + 14 DeltaE."""
        assert summary["T6_total_delta_polys"] == 7 + 14

    def test_16_equals_2_times_8(self, summary):
        """16 = 2 t-values x 8 directions."""
        assert summary["T6_total_tables"] == 2 * 8


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_ce2_seed_transport.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads(
            (ROOT / "data" / "w33_ce2_seed_transport.json").read_text(encoding="utf-8")
        )
        required = [
            "T1_checks_total", "T1_c0_passes", "T1_c0_all_pass",
            "T2_e_passes", "T2_e_all_pass", "T2_num_failures",
            "T3_dc0_w_only", "T3_trivial_dc0_count",
            "T4_all_t_differ", "T4_de_t_dependent_count",
            "T5_coverage_complete", "T5_sl2f3_order",
            "T6_total_tables", "T6_total_delta_polys", "T6_completeness",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
