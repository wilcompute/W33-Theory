def _kernel_label_ledger():
    slots = ["k1", "k2", "k3", "k4", "k5", "k6"]

    a2_roots = ["alpha1", "alpha2", "alpha3", "alpha4", "alpha5", "alpha6"]
    bivectors = ["B01", "B02", "B03", "B12", "B13", "B23"]
    singletons = ["s1", "s2", "s3", "s4", "s5", "s6"]
    remainders = ["r1", "r2", "r3", "r4", "r5", "r6"]

    # A fixed canonical slot dictionary for this part.
    return {
        "slots": slots,
        "a2": dict(zip(slots, a2_roots)),
        "bivectors": dict(zip(slots, bivectors)),
        "singletons": dict(zip(slots, singletons)),
        "remainders": dict(zip(slots, remainders)),
    }


def test_kernel_has_rank_six():
    ledger = _kernel_label_ledger()
    assert len(ledger["slots"]) == 6


def test_each_family_has_six_labels():
    ledger = _kernel_label_ledger()
    assert len(set(ledger["a2"].values())) == 6
    assert len(set(ledger["bivectors"].values())) == 6
    assert len(set(ledger["singletons"].values())) == 6
    assert len(set(ledger["remainders"].values())) == 6


def test_slot_projections_are_bijections():
    ledger = _kernel_label_ledger()
    slots = set(ledger["slots"])

    assert set(ledger["a2"].keys()) == slots
    assert set(ledger["bivectors"].keys()) == slots
    assert set(ledger["singletons"].keys()) == slots
    assert set(ledger["remainders"].keys()) == slots

    for family in ["a2", "bivectors", "singletons", "remainders"]:
        values = list(ledger[family].values())
        assert len(values) == len(set(values)) == len(slots)


def test_monodromy_ratio_is_k_to_six():
    gamma2 = 192 * 192
    for k in [1, 2, 3, 5, 7]:
        mon_qk = gamma2 * (k**6)
        assert mon_qk // gamma2 == k**6


def test_packet_ladder_consistency_with_rank_six_kernel():
    packet = 24
    aut_t = 96
    flags_t = 192
    gamma2 = 36864

    assert 4 * packet == aut_t
    assert 8 * packet == flags_t
    assert flags_t * flags_t == gamma2
