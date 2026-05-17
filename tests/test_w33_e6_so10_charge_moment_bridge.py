from scripts.w33_e6_so10_charge_moment_bridge import build_bridge


def test_charge_moment_summary_values() -> None:
    payload = build_bridge()
    s = payload["summary"]

    assert s["generations"] == 3
    assert s["one_gen_m0"] == 27
    assert s["one_gen_m1"] == 0
    assert s["one_gen_m2"] == 72
    assert s["one_gen_m3"] == 0
    assert s["three_gen_m0"] == 81
    assert s["three_gen_m1"] == 0
    assert s["three_gen_m2"] == 216
    assert s["three_gen_m3"] == 0


def test_root_split_and_bridge_links() -> None:
    payload = build_bridge()
    rs = payload["root_split"]

    assert rs["identity"] == "240 = 72 + 6 + 81 + 81"
    assert rs["e6_roots"] + rs["a2_roots"] + rs["g1_roots"] + rs["g2_roots"] == rs["total"]


def test_all_identities_hold() -> None:
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
