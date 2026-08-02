#!/usr/bin/env python3
"""Fail-closed verifier for Passes 2011--2015.

This verifies canonical JSON digests, frozen theorem values, the literal D8
parallel-class witness, and aggregate consistency.  The expensive subgroup and
group-action enumerations are frozen upstream; this script does not pretend to
rerun them.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = {
    2011: ROOT / "data/w33_pass2011_decorated_four_line_spread_pair_classes.json",
    2012: ROOT / "data/w33_pass2012_enumerated_subgroup_orbit_parallel_classes.json",
    2013: ROOT / "data/w33_pass2013_rank_three_spread_association_scheme.json",
    2014: ROOT / "data/w33_pass2014_one_line_spread_pair_rook_double.json",
    2015: ROOT / "data/w33_pass2015_degree_safety_quadratic_physics_engineering.json",
}
EXPECTED = {
    2011: "f9255c1d19e4d2a2a230daee4a126d2ceab1d1193bd589c9797a770abab07a19",
    2012: "0196b13daa36e4e177748ec93e15d0b86968f67c47258581da9de9a3358d3499",
    2013: "ce30e474a97ce9a602dd52f3ce62d8ad207cabaa7f77cfd747ab953b96d31fa7",
    2014: "449951039cb1a41a2f98b9bc810cb26990755bfba01538e9def48c88c10a53b8",
    2015: "d0af2532a61bd32cfa3e2df41549dde98a2d4cd4f8992972a48cb72e4cefa3f5",
}
AGG = "338fc1cfd0d6e8baa9fa6739565581cca3eb92395f4c1b4a6964afbbcc57fed6"
WITNESS_SHA = "9070764d14ea9bd25134a5b606a3743f7883c51e91730396dea9eebab6236028"


def digest(obj: dict) -> str:
    x = dict(obj)
    x.pop("sha256_without_hash_field", None)
    raw = json.dumps(x, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def main() -> dict:
    data = {p: json.loads(path.read_text()) for p, path in FILES.items()}
    for p, obj in data.items():
        assert obj["sha256_without_hash_field"] == EXPECTED[p] == digest(obj), p
        assert all(obj["checks"].values()), p

    d11, d12, d13, d14, d15 = (data[p] for p in range(2011, 2016))
    assert d11["fiber_identities"] == {
        "270_times_1": 270,
        "270_times_2": 540,
        "270_times_6": 1620,
    }
    assert d11["classes"]["540_linewise_quarter_turn"]["objects_per_pair"] == 2
    assert d11["classes"]["1620_common_line_cycle"]["objects_per_pair"] == 6

    assert d12["subgroup_enumeration"]["all_subgroups"] == 1026
    assert d12["subgroup_enumeration"]["H_conjugacy_classes"] == 234
    assert d12["exact_cover_results"]["H_conjugacy_classes_with_orbit_parallel_class"] == 33
    assert d12["exact_cover_results"]["largest_successful_subgroup_order"] == 8
    assert d12["best_witness"]["witness_sha256"] == WITNESS_SHA

    witness = json.loads(
        (ROOT / "data/w33_pass2012_d8_orbit_parallel_class_witness.json").read_text()
    )
    assert witness["sha256_without_hash_field"] == WITNESS_SHA == digest(witness)
    assert witness["frame_count"] == 60 and witness["edge_count"] == 240
    assert witness["edge_multiplicity_profile"] == {"1": 240}
    assert sum(witness["selected_orbit_sizes"]) == 60
    assert len(witness["selected_frame_indices"]) == 60
    assert len(set(witness["selected_frame_indices"])) == 60

    assert d13["relations"]["intersection_4"]["srg_parameters"] == [36, 15, 6, 6]
    assert d13["relations"]["intersection_4"]["adjacency_square"] == "A^2 = 9 I + 6 J"
    assert d13["objects"]["four_line_pairs"] + d13["objects"]["one_line_pairs"] == 630

    assert d14["octet_test"]["equivariant_map_to_octets"] is False
    assert d14["octet_test"]["pair_stabilizer_octet_orbits"] == [6, 9, 12, 18]
    assert d14["replacement_geometry"]["automorphism_group_order"] == 144
    assert d14["replacement_geometry"]["isomorphic_to"] == (
        "bipartite double cover of the 3x3 rook graph"
    )

    assert d15["degree_safety"]["new_unsafe_degrees"]["240"]["subgroups_conjugate"] is False
    assert d15["degree_safety"]["new_unsafe_degrees"]["540"]["pairwise_conjugate"] == [False, False, False]
    assert d15["quadratic_phase_channels"]["Sym2_90"]["multiplicities"]["81"] == 5
    assert d15["quadratic_phase_channels"]["Lambda2_90"]["multiplicities"]["15"] == 0
    assert len(d15["computer_engineering_proposals"]) == 5

    n_checks = sum(len(obj["checks"]) for obj in data.values())
    assert n_checks == 53
    aggregate = json.loads((ROOT / "data/w33_pass2011_2015_five_frontiers.json").read_text())
    assert aggregate["sha256_without_hash_field"] == AGG == digest(aggregate)
    assert aggregate["certificates"] == {str(k): v for k, v in EXPECTED.items()}
    assert aggregate["n_checks"] == aggregate["n_verified"] == n_checks

    out = {
        "status": aggregate["status"],
        "n_checks": n_checks,
        "n_verified": n_checks,
        "certificates": EXPECTED,
        "witness_sha256": WITNESS_SHA,
        "aggregate_sha256": AGG,
    }
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
