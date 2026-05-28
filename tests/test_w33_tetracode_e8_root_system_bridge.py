from __future__ import annotations

from analysis.w33_tetracode_e8_root_system_bridge import tetracode_e8_root_system_packet


PACKET = tetracode_e8_root_system_packet()


def test_mccclxxxviii_w33_tetracode_input() -> None:
    code = PACKET["w33_tetracode"]

    assert code["equals_standard_tetracode"] is True
    assert len(code["words"]) == 9
    assert code["standard_generators"] == [[0, 1, 1, 1], [1, 0, 1, 2]]


def test_mccclxxxviii_root_system_profile() -> None:
    root_system = PACKET["root_system"]

    assert root_system["count"] == 240
    assert root_system["rank"] == 8
    assert root_system["source_profile"] == {"A2": 24, "tetracode_glue": 216}
    assert root_system["norm_profile"] == {"2": 240}
    assert root_system["reflection_closure_failures"] == 0


def test_mccclxxxviii_e8_inner_product_profiles() -> None:
    root_system = PACKET["root_system"]

    assert root_system["representative_local_inner_product_profile"] == {
        "-1": 56,
        "-2": 1,
        "0": 126,
        "1": 56,
        "2": 1,
    }
    assert root_system["unique_local_profile_count"] == 1
    assert root_system["ordered_pair_inner_product_profile"] == {
        "-1": 13440,
        "-2": 240,
        "0": 30240,
        "1": 13440,
        "2": 240,
    }


def test_mccclxxxviii_simple_root_system() -> None:
    simple = PACKET["simple_root_system"]

    assert simple["simple_root_count"] == 8
    assert simple["gram_determinant"] == "1"
    assert simple["dynkin_edge_count"] == 7
    assert simple["dynkin_connected"] is True
    assert simple["dynkin_degree_profile"] == {"1": 3, "2": 4, "3": 1}


def test_mccclxxxviii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 14
    assert all(PACKET["checks"].values())
    assert "exact finite E8 root-system witness" in PACKET["reading"]
