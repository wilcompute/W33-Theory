from scripts.tomotope_toroidal_universal_functorial_bridge import build_bridge


def test_functorial_objects_and_morphisms():
    payload = build_bridge()
    s = payload["summary"]

    assert s["objects"] == [21, 42, 84, 168]
    assert s["morphisms"] == ["D", "Q", "W"]


def test_stability_weights():
    payload = build_bridge()
    s = payload["summary"]
    weights = s["stability_weights"]

    assert weights["D"] > 0.95
    assert weights["Q"] > 0.95
    assert weights["W"] > 0.95


def test_all_functorial_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True