from scripts.w33_for_everyone_consistency_bridge import build_bridge


def test_paper_consistency_core_counts_and_identities():
    payload = build_bridge()
    s = payload["summary"]

    assert (s["q"], s["v"], s["k"], s["lam"], s["mu"], s["edges"]) == (3, 40, 12, 2, 4, 240)
    assert s["primitive_count"] == 34
    assert s["manuscript_anchor_count"] == 10
    assert s["all_identities_hold"] is True


def test_paper_consistency_alpha_delta_is_exact_registry_value():
    payload = build_bridge()
    s = payload["summary"]
    ids = payload["identities"]

    assert (s["alpha_delta_num"], s["alpha_delta_den"]) == (24, 5431679)
    assert ids["alpha_delta_matches_registry"] is True
    assert ids["alpha_variants_unresolved_but_close"] is True


def test_paper_consistency_qec_ouroboros_runtime_ledger():
    payload = build_bridge()
    qec = payload["qec_ouroboros"]
    ids = payload["identities"]

    assert qec["base_code"] == {"n": 240, "k": 81, "d_z": 4}
    assert qec["vertex_x_rank"] + qec["triangle_z_rank"] + qec["logical_qudits"] == 240
    assert qec["nilpotent_exact_sequence"] == [81, 162, 81]
    assert qec["directed_carrier"] == 480
    assert qec["accepted_bonds"] + qec["heralded_return_syndrome_slots"] == 480
    assert qec["local_turn_split"] == {"accepted_signed_clifford": 6, "return_a2_weyl": 6}
    assert qec["klm_primitive_slots"] == 960
    assert ids["qec_carrier_partition_identity"] is True
    assert ids["global_turn_carrier_identity"] is True


def test_paper_consistency_reads_manuscript_and_promoted_bridges():
    payload = build_bridge()

    assert all(payload["manuscript"]["anchors"].values())
    assert all(payload["promoted_bridge_anchors"]["anchors"].values())
    assert payload["manuscript"]["path"] == "W33_FOR_EVERYONE.tex"
    assert payload["part"] == "DCCCLXXII"
