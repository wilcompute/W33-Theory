from scripts.tomotope_toroidal_operator_confluence_bridge import build_bridge


def test_operator_confluence_shell_values():
    payload = build_bridge()
    s = payload["summary"]

    assert (s["base_shell"], s["oriented_shell"], s["quotient_shell"], s["weighted_shell"]) == (
        21,
        42,
        84,
        168,
    )


def test_operator_route_equalities():
    payload = build_bridge()
    routes = payload["routes"]

    assert routes["to_84"]["direct"] == 84
    assert routes["to_84"]["via_weight_then_quotient"] == 84
    assert routes["to_168"]["direct_weight"] == 168
    assert routes["to_168"]["via_double_double"] == 168


def test_all_operator_confluence_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True
