"""Tests for Pillar 103 (Part CCIII): S3 Sheet Transport Law on K-Schreier Graph.

Verifies all six theorems establishing the exact C3 transport law:
  T1: L-label distribution on 54 K-pockets
  T2: Exact transport law L[v] = (s_g[g] + L[u] + e) mod 3 for all 270 edges
  T3: Only g3 has non-trivial shift s_g[g3]=2; all others 0
  T4: 6 sheets of 9 pockets; no sheet is L-homogeneous
  T5: 9/27 qids same L both twin bits; 18/27 differ
  T6: Cocycle exponent recovered exactly from L-labels
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCIII_S3_SHEET_TRANSPORT import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: L-label distribution
# ---------------------------------------------------------------------------

class TestT1LDistribution:
    """T1: L-label distribution on 54 K-pockets."""

    def test_num_pockets(self, summary):
        """Exactly 54 pockets."""
        assert summary["T1_num_pockets"] == 54

    def test_L_distribution_values(self, summary):
        """L-distribution is {0:17, 1:11, 2:26}."""
        assert summary["T1_L_distribution"] == {0: 17, 1: 11, 2: 26}

    def test_L_distribution_sums_to_54(self, summary):
        """L-distribution sums to 54."""
        assert sum(summary["T1_L_distribution"].values()) == 54

    def test_all_three_labels_present(self, summary):
        """All three C3 labels appear."""
        assert set(summary["T1_L_distribution"].keys()) == {0, 1, 2}


# ---------------------------------------------------------------------------
# T2: Exact transport law
# ---------------------------------------------------------------------------

class TestT2TransportLaw:
    """T2: Exact transport law L[v] = (s_g[g] + L[u] + e) mod 3."""

    def test_all_270_edges_ok(self, summary):
        """All 270 edges satisfy the transport law."""
        assert summary["T2_edge_check_ok"] == 270

    def test_zero_failures(self, summary):
        """No edges fail the transport law."""
        assert summary["T2_edge_check_fail"] == 0

    def test_transport_law_exact_flag(self, summary):
        """Transport law exact flag is True."""
        assert summary["T2_transport_law_exact"] is True


# ---------------------------------------------------------------------------
# T3: Generator shift table
# ---------------------------------------------------------------------------

class TestT3GeneratorShifts:
    """T3: Generator shift table -- only g3 is non-trivial."""

    def test_g3_shift_is_2(self, summary):
        """g3 has shift 2 (= c^2 in Z3)."""
        assert summary["T3_generator_shifts"]["g3"] == 2

    def test_g2_shift_is_0(self, summary):
        """g2 has trivial shift."""
        assert summary["T3_generator_shifts"]["g2"] == 0

    def test_g5_shift_is_0(self, summary):
        """g5 has trivial shift."""
        assert summary["T3_generator_shifts"]["g5"] == 0

    def test_g8_shift_is_0(self, summary):
        """g8 has trivial shift."""
        assert summary["T3_generator_shifts"]["g8"] == 0

    def test_g9_shift_is_0(self, summary):
        """g9 has trivial shift."""
        assert summary["T3_generator_shifts"]["g9"] == 0

    def test_exactly_one_nonzero_generator(self, summary):
        """Exactly one generator has non-trivial shift."""
        assert summary["T3_nonzero_generators"] == ["g3"]

    def test_five_generators_total(self, summary):
        """Exactly 5 generators in shift table."""
        assert len(summary["T3_generator_shifts"]) == 5


# ---------------------------------------------------------------------------
# T4: Sheet structure
# ---------------------------------------------------------------------------

class TestT4SheetStructure:
    """T4: 6 sheets of 9 pockets each; no sheet is L-homogeneous."""

    def test_six_sheets(self, summary):
        """Exactly 6 sheets."""
        assert summary["T4_num_sheets"] == 6

    def test_nine_pockets_per_sheet(self, summary):
        """Each sheet has 9 pockets."""
        assert summary["T4_pockets_per_sheet"] == 9

    def test_total_pockets(self, summary):
        """6 sheets x 9 pockets = 54 total."""
        assert summary["T4_num_sheets"] * summary["T4_pockets_per_sheet"] == 54

    def test_all_sheets_have_distribution(self, summary):
        """All 6 sheets have an L-distribution entry."""
        dists = summary["T4_sheet_L_distributions"]
        assert len(dists) == 6

    def test_each_sheet_sums_to_9(self, summary):
        """Each sheet's L-distribution sums to 9."""
        for sh, dist in summary["T4_sheet_L_distributions"].items():
            assert sum(dist.values()) == 9, f"Sheet {sh} sum != 9"

    def test_no_sheet_is_homogeneous(self, summary):
        """No sheet has all 9 pockets with the same L-label."""
        for sh, dist in summary["T4_sheet_L_distributions"].items():
            assert len(dist) > 1, f"Sheet {sh} is homogeneous"

    def test_sheet_0_identity_dominated(self, summary):
        """Sheet 0 is identity-dominated (6 out of 9 are L=0)."""
        dist = summary["T4_sheet_L_distributions"]["0"]
        assert dist.get(0, 0) == 6

    def test_sheet_1_identity_dominated(self, summary):
        """Sheet 1 is identity-dominated (6 out of 9 are L=0)."""
        dist = summary["T4_sheet_L_distributions"]["1"]
        assert dist.get(0, 0) == 6

    def test_sheet_3_c2_dominated(self, summary):
        """Sheet 3 is c2-dominated (7 out of 9 are L=2)."""
        dist = summary["T4_sheet_L_distributions"]["3"]
        assert dist.get(2, 0) == 7


# ---------------------------------------------------------------------------
# T5: Twin-pair L analysis
# ---------------------------------------------------------------------------

class TestT5TwinPairs:
    """T5: L-label analysis across 27 Heisenberg qid twin-pairs."""

    def test_9_same_L_qids(self, summary):
        """9 qids have the same L-label on both twin_bit=0 and twin_bit=1."""
        assert summary["T5_qid_same_L"] == 9

    def test_18_diff_L_qids(self, summary):
        """18 qids have differing L-labels across twin bits."""
        assert summary["T5_qid_diff_L"] == 18

    def test_total_qids_is_27(self, summary):
        """Total qids = 9 same + 18 diff = 27."""
        assert summary["T5_qid_same_L"] + summary["T5_qid_diff_L"] == 27

    def test_most_common_transition_id_to_c2(self, summary):
        """Most common inter-bit transition is (0->2): 8 qids."""
        dist = summary["T5_L_pair_distribution"]
        count_0_2 = dist.get("(0, 2)", 0)
        assert count_0_2 == 8

    def test_same_L_c2_c2_count(self, summary):
        """8 qids have (L=2, L=2) -- largest same-label group."""
        dist = summary["T5_L_pair_distribution"]
        assert dist.get("(2, 2)", 0) == 8

    def test_L_pair_distribution_sums_to_27(self, summary):
        """L-pair distribution sums to 27 qids."""
        assert sum(summary["T5_L_pair_distribution"].values()) == 27


# ---------------------------------------------------------------------------
# T6: Cocycle recovery
# ---------------------------------------------------------------------------

class TestT6CocycleRecovery:
    """T6: Cocycle exponent recovered exactly from L-labels."""

    def test_cocycle_recovery_exact(self, summary):
        """Cocycle recovery is exact for all 270 edges."""
        assert summary["T6_cocycle_recovered_exact"] is True

    def test_cocycle_distribution(self, summary):
        """Cocycle distribution matches Pillar 83: {0:201, 1:33, 2:36}."""
        assert summary["T6_cocycle_dist"] == {0: 201, 1: 33, 2: 36}

    def test_69_nontrivial_edges(self, summary):
        """69 non-trivial cocycle edges (33+36)."""
        assert summary["T6_nontrivial_edges"] == 69

    def test_total_edges_is_270(self, summary):
        """Total edges = 201 trivial + 69 non-trivial = 270."""
        cocycle_dist = summary["T6_cocycle_dist"]
        assert sum(cocycle_dist.values()) == 270

    def test_majority_trivial_cocycle(self, summary):
        """201/270 edges have trivial cocycle (> non-trivial 69)."""
        cocycle_dist = summary["T6_cocycle_dist"]
        assert cocycle_dist[0] == 201
        assert cocycle_dist[0] > sum(v for k, v in cocycle_dist.items() if k > 0)


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    """Test that the JSON output file is generated and well-formed."""

    def test_json_output_exists(self):
        """data/w33_s3_sheet_transport.json is generated."""
        assert (ROOT / "data" / "w33_s3_sheet_transport.json").exists()

    def test_json_output_valid(self):
        """JSON output contains all expected keys."""
        data = json.loads((ROOT / "data" / "w33_s3_sheet_transport.json").read_text(encoding="utf-8"))
        required_keys = [
            "T1_L_distribution", "T1_num_pockets",
            "T2_edge_check_ok", "T2_edge_check_fail", "T2_transport_law_exact",
            "T3_generator_shifts", "T3_nonzero_generators",
            "T4_num_sheets", "T4_pockets_per_sheet", "T4_sheet_L_distributions",
            "T5_qid_same_L", "T5_qid_diff_L", "T5_L_pair_distribution",
            "T6_cocycle_recovered_exact", "T6_cocycle_dist", "T6_nontrivial_edges",
        ]
        for key in required_keys:
            assert key in data, f"Missing key: {key}"
