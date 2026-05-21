from __future__ import annotations

from analysis.w33_superbeat_prime_horizon import superbeat_prime_horizon_packet


PACKET = superbeat_prime_horizon_packet()


def test_mclxxviii_closed_prime_sieve_identity() -> None:
    sieve = PACKET["closed_prime_sieve"]

    assert sieve["trigger_primes"] == [7, 11, 13, 17, 19, 23, 29, 31]
    assert sieve["closed_prime_product"] == 6685349671
    assert sieve["primorial_31"] == 200560490130
    assert sieve["substrate_lift"] == 108
    assert sieve["identity"] == "21660532934040 = 108 * 31# = (q^2*k) * 31#"


def test_mclxxviii_scaled_duality_survives_through_31() -> None:
    sieve = PACKET["closed_prime_sieve"]

    assert sieve["Q_over_base_beat"] == 6685349671
    assert sieve["Q_over_A_star"] == 60168147039
    assert sieve["Q_over_cloud"] == 267413986840


def test_mclxxviii_next_horizon_is_37() -> None:
    horizon = PACKET["next_horizon"]

    assert horizon["prime"] == 37
    assert horizon["origin"] == {
        "v_minus_q": 37,
        "gaussian_matter_pole": "|6+i|^2 = 37",
        "first_prime_after_31": 37,
    }
    assert horizon["Q_mod_37"] == 4


def test_mclxxviii_37_closure_values() -> None:
    horizon = PACKET["next_horizon"]

    assert horizon["R"] == 801439718559480
    assert horizon["identity"] == "801439718559480 = lcm(Q,37) = 37*Q = 108*37#"
    assert horizon["R_over_A_star"] == 2226221440443
    assert horizon["R_over_cloud"] == 9894317513080


def test_mclxxviii_all_checks_pass() -> None:
    assert PACKET["n_verified"] == 12
    assert all(PACKET["checks"].values())
