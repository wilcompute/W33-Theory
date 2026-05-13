from scripts.tomotope_six_kernel_generator_alignment import build_alignment


def test_alignment_summary_counts():
    payload = build_alignment()
    summary = payload["summary"]

    assert summary["generator_count"] == 4
    assert summary["edge_count"] == 12
    assert summary["perfect_match_involution_count"] == 10395
    assert summary["commuting_involution_count"] >= 1
    assert summary["slot_count"] == 6
    assert summary["all_generators_preserve_slots"] is True


def test_canonical_involution_is_fixed_point_free_involution():
    payload = build_alignment()
    tau = payload["canonical_commuting_involution"]
    n = len(tau)

    assert n == 12
    assert all(0 <= x < n for x in tau)
    assert all(tau[tau[i]] == i for i in range(n))
    assert all(tau[i] != i for i in range(n))


def test_slot_pairs_partition_edges_exactly_once():
    payload = build_alignment()
    slot_pairs = payload["slot_pairs"]

    assert len(slot_pairs) == 6
    all_edges = []
    for pair in slot_pairs.values():
        assert len(pair) == 2
        all_edges.extend(pair)

    assert len(all_edges) == 12
    assert len(set(all_edges)) == 12
    assert set(all_edges) == {f"e{i}" for i in range(12)}


def test_each_generator_induces_permutation_of_six_slots():
    payload = build_alignment()
    actions = payload["induced_slot_actions"]
    slots = {f"k{i}" for i in range(1, 7)}

    assert set(actions.keys()) == {"p0", "p1", "p2", "p3"}
    for image in actions.values():
        assert len(image) == 6
        assert set(image) == slots
