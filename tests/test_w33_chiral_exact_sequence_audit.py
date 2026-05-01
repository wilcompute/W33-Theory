from pathlib import Path

from scripts.w33_chiral_exact_sequence_audit import build_chiral_exact_sequence_summary


PART_LXXXIV_NOTE = Path("PART_LXXXIV_CHIRAL_EXACT_SEQUENCE.md")


def test_chiral_exact_sequence_records_chirality_dictionary() -> None:
    summary = build_chiral_exact_sequence_summary()

    assert summary["status"] == "ok"
    assert summary["carrier_dictionary"] == {
        "positive_chirality": "P_+ = L_15 + L_24 + S_20",
        "negative_chirality": "P_- = S_15 + Q_24 + Q_20",
        "harmonic_sector": "H = 1_L + 1_S + 1_Q",
        "positive_dimension": "15 + 24 + 20 = 59",
        "negative_dimension": "15 + 24 + 20 = 59",
        "harmonic_dimension": "1 + 1 + 1 = 3",
        "exact_dimension_identity": "2(15 + 24 + 20) = 118",
        "total_dimension_identity": "121 = 59_+ + 59_- + 3_harm",
        "representation_triangle_identity": "121 = 3 + 2(15 + 20 + 24)",
    }
    assert summary["derived_invariants"] == {
        "rank_Q": 59,
        "nullity_Q": 62,
        "positive_chirality_dimension": 59,
        "negative_chirality_dimension": 59,
        "harmonic_dimension": 3,
        "exact_dimension": 118,
        "total_dimension": 121,
    }


def test_chiral_exact_sequence_records_supercharge_relations_and_block_support() -> None:
    summary = build_chiral_exact_sequence_summary()

    assert summary["supercharge_relations"] == {
        "supercharge": "Q = (D + J) / 2",
        "adjoint_supercharge": "Q* = (D - J) / 2 = Q^T",
        "positive_chiral_projector": "P_+ = (P_0 + Gamma) / 2",
        "negative_chiral_projector": "P_- = (P_0 - Gamma) / 2",
        "positive_projector_identity": "Q Q* = P_+",
        "negative_projector_identity": "Q* Q = P_-",
    }
    assert summary["block_support"] == {
        "nonzero_forward_blocks": [
            {
                "block": "Q_{S15->L15}",
                "source": "S_15",
                "target": "L_15",
                "dimension": 15,
                "certificate": "adjoint of B_c^T / sqrt(18) : L_15 -> S_15",
            },
            {
                "block": "Q_{Q24->L24}",
                "source": "Q_24",
                "target": "L_24",
                "dimension": 24,
                "certificate": "adjoint of U_c^T / sqrt(18) : L_24 -> Q_24",
            },
            {
                "block": "Q_{Q20->S20}",
                "source": "Q_20",
                "target": "S_20",
                "dimension": 20,
                "certificate": "shared target-side Naimark shadow 1 + 20 on the spread and quotient channels",
            },
        ],
        "block_sum": "Q = Q_{S15->L15} oplus Q_{Q24->L24} oplus Q_{Q20->S20}",
        "harmonic_modes": ["1_L", "1_S", "1_Q"],
        "cohomology_statement": "the only cohomology is the three module means",
    }


def test_chiral_exact_sequence_theorem_and_checks_all_hold() -> None:
    summary = build_chiral_exact_sequence_summary()

    assert summary["theorem"] == {
        "the_121_carrier_splits_as_59_positive_plus_59_negative_plus_3_harmonic": True,
        "the_only_nonzero_forward_blocks_are_s15_to_l15_q24_to_l24_and_q20_to_s20": True,
        "the_exact_part_is_the_direct_sum_of_three_two_term_complexes_of_dimensions_15_24_and_20": True,
        "the_only_cohomology_is_the_three_module_means": True,
    }
    assert all(summary["checks"].values())
    assert "three exact two-term complexes" in summary["interpretation"]
    assert "121 = 59_+ + 59_- + 3_harm" in summary["interpretation"]
    assert "118 = 2(15 + 24 + 20)" in summary["interpretation"]


def test_part_lxxxiv_note_mentions_the_executable_surface() -> None:
    note_text = PART_LXXXIV_NOTE.read_text(encoding="utf-8")

    assert "QQ^*=P_+" in note_text
    assert "Q^*Q=P_-" in note_text
    assert "121=59_+ + 59_- + 3_{\\mathrm{harm}}" in note_text
    assert "S_{15}\\to L_{15}" in note_text
    assert "Q_{24}\\to L_{24}" in note_text
    assert "Q_{20}\\to S_{20}" in note_text
    assert "scripts/w33_chiral_exact_sequence_audit.py" in note_text
    assert "tests/test_w33_chiral_exact_sequence_audit.py" in note_text