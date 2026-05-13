from scripts.tomotope_toroidal_quotient_category_bridge import build_bridge


def test_category_objects_and_morphisms():
    payload = build_bridge()
    s = payload["summary"]

    assert s["objects"] == [21, 42, 84, 168]
    assert s["morphisms"] == ["D", "Q", "W"]


def test_all_category_identities_hold():
    payload = build_bridge()
    assert all(payload["identities"].values())
    assert payload["summary"]["all_identities_hold"] is True