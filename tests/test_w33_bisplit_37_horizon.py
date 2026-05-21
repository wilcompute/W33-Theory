from __future__ import annotations

from analysis.w33_bisplit_37_horizon import bisplit_37_horizon_packet


PACKET = bisplit_37_horizon_packet()


def test_mclxxix_37_is_first_open_bisplit_prime() -> None:
    classification = PACKET["bisplit_classification"]

    assert classification["prime"] == 37
    assert classification["mod_4"] == 1
    assert classification["mod_3"] == 1
    assert classification["mod_12"] == 1
    assert classification["gaussian_split"] is True
    assert classification["eisenstein_split"] is True
    assert classification["first_prime_after_31"] == [37]
    assert classification["closed_bisplit_primes_through_31"] == [13]
    assert classification["first_open_bisplit_after_31"] == [37]


def test_mclxxix_w33_witnesses_for_37() -> None:
    witnesses = PACKET["w33_witnesses"]

    assert witnesses["q"] == 3
    assert witnesses["v"] == 40
    assert witnesses["k"] == 12
    assert witnesses["mu"] == 4
    assert witnesses["phi3_q"] == 13
    assert witnesses["phi6_q"] == 7
    assert witnesses["v_minus_q"] == 37
    assert witnesses["q_factorial_squared_plus_one"] == 37


def test_mclxxix_gaussian_and_eisenstein_norm_witnesses() -> None:
    gaussian = PACKET["gaussian_matter_witness"]
    eisenstein = PACKET["eisenstein_mixed_witness"]

    assert gaussian["element"] == "6+i"
    assert gaussian["real_part"] == 6
    assert gaussian["imag_part"] == 1
    assert gaussian["norm"] == 37
    assert gaussian["sqrt_minus_one_roots_mod_37"] == [6, 31]

    assert eisenstein["element"] == "7+3omega"
    assert eisenstein["a"] == 7
    assert eisenstein["b"] == 3
    assert eisenstein["norm"] == 37
    assert eisenstein["phi3_roots_mod_37"] == [10, 26]
    assert eisenstein["phi6_roots_mod_37"] == [11, 27]


def test_mclxxix_superbeat_residue_lands_on_mu_channel() -> None:
    residue = PACKET["superbeat_residue"]

    assert residue["Q_mod_37"] == 4
    assert residue["mu"] == 4
    assert residue["q_plus_1"] == 4
    assert residue["square_roots_mod_37"] == [2, 35]


def test_mclxxix_minimal_bisplit_closure() -> None:
    closure = PACKET["minimal_closure"]

    assert closure["R"] == 801439718559480
    assert closure["identity"] == "801439718559480 = 37*Q = 108*37#"
    assert closure["R_over_A_star"] == 2226221440443
    assert closure["R_over_cloud"] == 9894317513080


def test_mclxxix_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 17
    assert all(PACKET["checks"].values())
