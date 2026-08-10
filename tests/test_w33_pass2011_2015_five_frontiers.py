from analysis.w33_pass2011_2015_verify_frozen import main


def test_frozen_packet():
    out = main()
    assert out["n_checks"] == out["n_verified"] == 53


def test_exact_boundaries_and_engineering_separation():
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    d12 = json.loads(
        (root / "data/w33_pass2012_enumerated_subgroup_orbit_parallel_classes.json").read_text(encoding="utf-8")
    )
    d13 = json.loads(
        (root / "data/w33_pass2013_rank_three_spread_association_scheme.json").read_text(encoding="utf-8")
    )
    d14 = json.loads(
        (root / "data/w33_pass2014_one_line_spread_pair_rook_double.json").read_text(encoding="utf-8")
    )
    d15 = json.loads(
        (root / "data/w33_pass2015_degree_safety_quadratic_physics_engineering.json").read_text(encoding="utf-8")
    )

    assert d12["boundary"].startswith("The enumeration is complete for subgroups")
    assert d12["exact_cover_results"]["no_success_at_order_at_least_12"] is True
    assert d13["boundary"].startswith("This is a q=3 theorem")
    assert d14["status"] == "PASS_WITH_OCTET_FIBRATION_REFUTED"
    assert d15["boundary"].endswith("All hardware items are proposals.")
    assert "electric charge" in d15["physics"]["withdrawn"]
