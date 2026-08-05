from analysis.bt3500_3505_triangle_free_srg_m57_bridge import build_certificate


def test_triangle_free_srg_m57_bridge_certificate():
    result = build_certificate()
    assert result["status"] == "PASS_6_FRONTS"
    assert result["semantic_sha256"] == "e308364dd480970803061b90ab27bf86afa2ae4946399b656292f02682c17fd9"

    ladder = result["mu4_r2_ladder"]
    assert [row["parameters"] for row in ladder] == [
        [77, 16, 0, 4],
        [57, 14, 1, 4],
        [40, 12, 2, 4],
        [26, 10, 3, 4],
        [15, 8, 4, 4],
    ]
    assert ladder[1]["status"] == "nonexistent_Wilbrink_Brouwer_1983"

    kernel = result["w33_gewirtz_kernel"]
    assert kernel["common_nonprincipal_minimal_polynomial"] == "x^2 + 2*x - 8"
    assert kernel["centered_complement_square"] == "9*I_on_augmentation"

    chart = result["missing_moore_edge_chart"]
    assert chart["edge_rooted_partition"] == [2, 56, 56, 3136]
    assert chart["residual_grid"] == [56, 56]
    assert chart["residual_degree"] == 55
    assert chart["edge_count"] == 92625

    firewall = result["fifty_seven_firewall"]
    assert firewall["psl2_19_order"] == 3420
    assert firewall["psl2_19_even"] is True

    audit = result["claim_audit"]
    assert audit["edge_count_is_not_automorphism_count"] is True
    assert audit["factorial_relabelling_is_not_fixed_graph_automorphism_group"] is True
