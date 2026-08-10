"""Tests for Pillar 104 (Part CCIV): 27x10 Heisenberg-Orient Quotient."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from THEORY_PART_CCIV_27x10_QUOTIENT import analyze


@pytest.fixture(scope="module")
def summary():
    return analyze()


# ---------------------------------------------------------------------------
# T1: Bijectivity
# ---------------------------------------------------------------------------

class TestT1Bijectivity:
    """T1: (qid, orient_index) bijects with the 270 directed edges."""

    def test_total_edges(self, summary):
        """270 directed K-Schreier edges."""
        assert summary["T1_total_edges"] == 270

    def test_unique_pairs(self, summary):
        """270 unique (qid, orient_index) pairs."""
        assert summary["T1_unique_qid_orient_pairs"] == 270

    def test_bijective(self, summary):
        """Map is a bijection onto Z_27 x Z_10."""
        assert summary["T1_bijective"] is True

    def test_270_equals_27_times_10(self, summary):
        """270 = 27 qids x 10 orient slots."""
        assert summary["T1_total_edges"] == 27 * 10


# ---------------------------------------------------------------------------
# T2: Orient split
# ---------------------------------------------------------------------------

class TestT2OrientSplit:
    """T2: Orient indices 0-4 = twin_bit=0; 5-9 = twin_bit=1."""

    def test_orient_split_consistent(self, summary):
        """Each orient index consistently maps to one twin_bit and one gen."""
        assert summary["T2_orient_split_consistent"] is True

    def test_tb0_orient_indices(self, summary):
        """Twin_bit=0 uses orient indices 0-4."""
        assert summary["T2_tb0_orient_indices"] == [0, 1, 2, 3, 4]

    def test_tb1_orient_indices(self, summary):
        """Twin_bit=1 uses orient indices 5-9."""
        assert summary["T2_tb1_orient_indices"] == [5, 6, 7, 8, 9]

    def test_gen_order_tb0(self, summary):
        """Generator order for twin_bit=0: g2,g3,g5,g8,g9."""
        assert summary["T2_gen_order_tb0"] == ["g2", "g3", "g5", "g8", "g9"]

    def test_gen_order_tb1(self, summary):
        """Generator order for twin_bit=1: g2,g3,g5,g8,g9."""
        assert summary["T2_gen_order_tb1"] == ["g2", "g3", "g5", "g8", "g9"]

    def test_270_equals_27_times_5_times_2(self, summary):
        """270 = 27 qids x 5 generators x 2 twin_bits."""
        assert summary["T1_total_edges"] == 27 * 5 * 2


# ---------------------------------------------------------------------------
# T3: Fixed trio
# ---------------------------------------------------------------------------

class TestT3FixedTrio:
    """T3: Exactly 3 qids (13, 14, 26) are fixed by both g8 and g9."""

    def test_fixed_trio_members(self, summary):
        """Fixed trio is {13, 14, 26}."""
        assert summary["T3_fixed_trio"] == [13, 14, 26]

    def test_fixed_trio_correct(self, summary):
        """Fixed trio matches expected set."""
        assert summary["T3_fixed_trio_correct"] is True

    def test_self_loop_count(self, summary):
        """Exactly 12 self-loop edges: 3 qids x 2 gens x 2 twin_bits."""
        assert summary["T3_self_loop_count"] == 12

    def test_self_loop_gen_dist(self, summary):
        """Self-loops come only from g8 and g9, 6 each."""
        assert summary["T3_self_loop_gen_dist"] == {"g8": 6, "g9": 6}

    def test_no_g2_g3_g5_self_loops(self, summary):
        """Generators g2, g3, g5 produce no self-loops."""
        dist = summary["T3_self_loop_gen_dist"]
        assert "g2" not in dist
        assert "g3" not in dist
        assert "g5" not in dist

    def test_three_fixed_qids(self, summary):
        """Exactly 3 fixed qids."""
        assert len(summary["T3_fixed_trio"]) == 3


# ---------------------------------------------------------------------------
# T4: Cocycle asymmetry
# ---------------------------------------------------------------------------

class TestT4CocycleAsymmetry:
    """T4: g8 and g9 from twin_bit=0 have all-trivial cocycle."""

    def test_g8_tb0_all_trivial(self, summary):
        """g8 from twin_bit=0: 0 non-trivial cocycle edges."""
        assert summary["T4_g8_tb0_all_trivial"] is True

    def test_g9_tb0_all_trivial(self, summary):
        """g9 from twin_bit=0: 0 non-trivial cocycle edges."""
        assert summary["T4_g9_tb0_all_trivial"] is True

    def test_g8_tb1_has_nontrivial(self, summary):
        """g8 from twin_bit=1: 6 non-trivial cocycle edges."""
        assert summary["T4_g8_tb1_nontrivial"] == 6

    def test_g9_tb1_has_nontrivial(self, summary):
        """g9 from twin_bit=1: 6 non-trivial cocycle edges."""
        assert summary["T4_g9_tb1_nontrivial"] == 6

    def test_g3_tb0_nontrivial(self, summary):
        """g3 from twin_bit=0: 9 non-trivial edges."""
        assert summary["T4_gen_twin_nontrivial"]["g3_tb0"] == 9

    def test_g3_tb1_most_nontrivial(self, summary):
        """g3 from twin_bit=1 has most non-trivial edges (15)."""
        assert summary["T4_gen_twin_nontrivial"]["g3_tb1"] == 15

    def test_g2_symmetric(self, summary):
        """g2 has 6 non-trivial edges on both twin_bits."""
        nt = summary["T4_gen_twin_nontrivial"]
        assert nt["g2_tb0"] == 6
        assert nt["g2_tb1"] == 6

    def test_total_nontrivial_is_69(self, summary):
        """Total non-trivial cocycle edges = 69 (matches Pillar 83/103)."""
        total = sum(summary["T4_gen_twin_nontrivial"].values())
        assert total == 69

    def test_twin_bit_symmetry_breaking_for_diagonal_gens(self, summary):
        """g8 and g9 break twin_bit symmetry: 0 nontrivial for tb0, 6 for tb1."""
        nt = summary["T4_gen_twin_nontrivial"]
        assert nt["g8_tb0"] == 0 and nt["g8_tb1"] > 0
        assert nt["g9_tb0"] == 0 and nt["g9_tb1"] > 0


# ---------------------------------------------------------------------------
# T5: Sheet equidistribution
# ---------------------------------------------------------------------------

class TestT5SheetEquidistribution:
    """T5: All 6 sheets receive exactly 45 = 270/6 directed edges."""

    def test_six_sheets_present(self, summary):
        """Exactly 6 sheets."""
        assert len(summary["T5_sheet_dist"]) == 6

    def test_each_sheet_has_45(self, summary):
        """Each sheet has exactly 45 edges."""
        for sh, cnt in summary["T5_sheet_dist"].items():
            assert cnt == 45, f"Sheet {sh} has {cnt} edges, not 45"

    def test_edges_per_sheet(self, summary):
        """Expected edges per sheet is 45."""
        assert summary["T5_edges_per_sheet"] == 45

    def test_equidistributed(self, summary):
        """Sheet equidistribution flag is True."""
        assert summary["T5_equidistributed"] is True

    def test_total_edges_from_sheets(self, summary):
        """Sum over sheets = 270."""
        assert sum(summary["T5_sheet_dist"].values()) == 270

    def test_45_is_270_div_6(self, summary):
        """45 = 270/6 (edges / sheets)."""
        assert summary["T5_edges_per_sheet"] == summary["T1_total_edges"] // 6


# ---------------------------------------------------------------------------
# T6: L-label split
# ---------------------------------------------------------------------------

class TestT6LLabelSplit:
    """T6: L-label distribution splits between the two twin_bits."""

    def test_L_dist_tb0(self, summary):
        """Twin_bit=0 L-distribution: {0:13, 1:4, 2:10}."""
        assert summary["T6_L_dist_tb0"] == {0: 13, 1: 4, 2: 10}

    def test_L_dist_tb1(self, summary):
        """Twin_bit=1 L-distribution: {0:4, 1:7, 2:16}."""
        assert summary["T6_L_dist_tb1"] == {0: 4, 1: 7, 2: 16}

    def test_L_dist_tb0_sums_to_27(self, summary):
        """Twin_bit=0 L-distribution covers 27 pockets."""
        assert sum(summary["T6_L_dist_tb0"].values()) == 27

    def test_L_dist_tb1_sums_to_27(self, summary):
        """Twin_bit=1 L-distribution covers 27 pockets."""
        assert sum(summary["T6_L_dist_tb1"].values()) == 27

    def test_L_merged_recovers_pillar103(self, summary):
        """Merged L-distribution recovers Pillar 103 T1: {0:17, 1:11, 2:26}."""
        assert summary["T6_L_merged"] == {0: 17, 1: 11, 2: 26}

    def test_sum_recovers_pillar103_flag(self, summary):
        """T6 recovery flag is True."""
        assert summary["T6_sum_recovers_pillar103"] is True

    def test_tb1_c2_dominated(self, summary):
        """Twin_bit=1 pockets are c2-dominated (L=2 is most common)."""
        dist = summary["T6_L_dist_tb1"]
        assert dist[2] > dist[0] and dist[2] > dist[1]

    def test_tb0_identity_dominated(self, summary):
        """Twin_bit=0 pockets are identity-dominated (L=0 is most common)."""
        dist = summary["T6_L_dist_tb0"]
        assert dist[0] > dist[1] and dist[0] > dist[2]


# ---------------------------------------------------------------------------
# Output file
# ---------------------------------------------------------------------------

class TestOutputFile:
    def test_json_exists(self):
        assert (ROOT / "data" / "w33_27x10_quotient.json").exists()

    def test_json_has_required_keys(self):
        data = json.loads((ROOT / "data" / "w33_27x10_quotient.json").read_text(encoding="utf-8"))
        required = [
            "T1_total_edges", "T1_unique_qid_orient_pairs", "T1_bijective",
            "T2_orient_split_consistent", "T2_tb0_orient_indices", "T2_tb1_orient_indices",
            "T3_fixed_trio", "T3_fixed_trio_correct", "T3_self_loop_count",
            "T4_g8_tb0_all_trivial", "T4_g9_tb0_all_trivial",
            "T4_gen_twin_nontrivial",
            "T5_sheet_dist", "T5_equidistributed",
            "T6_L_dist_tb0", "T6_L_dist_tb1", "T6_L_merged", "T6_sum_recovers_pillar103",
        ]
        for key in required:
            assert key in data, f"Missing key: {key}"
