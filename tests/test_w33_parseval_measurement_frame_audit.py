from scripts.w33_parseval_measurement_frame_audit import build_parseval_measurement_frame_summary


def test_parseval_measurement_frame_records_the_spread_and_anti_line_carriers() -> None:
    summary = build_parseval_measurement_frame_summary()

    assert summary["status"] == "ok"
    assert summary["carrier_dictionary"] == {
        "line_side": "40 = 1 + 15 + 24",
        "projective_line_split": {"total": 130, "true_lines": 40, "anti_lines": 90},
        "spread_probe": {
            "shape": [40, 36],
            "incidence_count": 360,
            "density": "1/4",
            "row_degree_distribution": {9: 40},
            "column_degree_distribution": {10: 36},
        },
        "anti_line_probe": {
            "shape": [40, 90],
            "incidence_count": 1440,
            "density": "2/5",
            "row_degree_distribution": {36: 40},
            "column_degree_distribution": {16: 90},
        },
    }


def test_parseval_measurement_frame_records_the_exact_identities_and_spectra() -> None:
    summary = build_parseval_measurement_frame_summary()

    assert summary["exact_identities"] == {
        "centered_spread_probe": "B_c = B - J/4",
        "centered_anti_line_probe": "R_c = R - 2J/5",
        "parseval_identity": "B_c B_c^T / 18 + R_c R_c^T / 36 = I - J/40",
        "full_identity_resolution": "J/40 + B_c B_c^T / 18 + R_c R_c^T / 36 = I",
        "signed_spread_probe": "B_4 = 4B - J",
        "signed_anti_line_probe": "R_5 = 5R - 2J",
        "signed_orthogonality": "B_4^T R_5 = 0",
        "integer_parseval_identity": "25 B_4 B_4^T + 8 R_5 R_5^T = 7200 I - 180 J",
    }
    assert summary["spectral_data"] == {
        "line_disjoint_spectrum": {-3: 24, 3: 15, 27: 1},
        "centered_spread_probe_spectrum": {0: 25, 18: 15},
        "centered_anti_line_probe_spectrum": {0: 16, 36: 24},
        "signed_spread_probe_spectrum": {0: 25, 288: 15},
        "signed_anti_line_probe_spectrum": {0: 16, 900: 24},
    }


def test_parseval_measurement_frame_theorem_and_checks_all_hold() -> None:
    summary = build_parseval_measurement_frame_summary()

    assert summary["theorem"] == {
        "the_36_spreads_and_90_anti_lines_form_an_exact_parseval_measurement_frame_on_the_40_line_module": True,
        "the_centered_spread_probe_carries_exactly_the_line_side_15_sector": True,
        "the_centered_anti_line_probe_carries_exactly_the_line_side_24_sector": True,
        "the_mean_channel_completes_the_exact_split_1_plus_15_plus_24": True,
    }
    assert all(summary["checks"].values())