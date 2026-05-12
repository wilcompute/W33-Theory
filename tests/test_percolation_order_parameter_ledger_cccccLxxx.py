def rank_positive(eigs, eps=1e-12):
    return sum(1 for x in eigs if x > eps)


def traces(eigs):
    t1 = sum(eigs)
    t2 = sum(x * x for x in eigs)
    deff = 0 if t2 == 0 else (t1 * t1) / t2
    return t1, t2, deff


def split_count(eigs, eps=1e-9):
    vals = sorted(x for x in eigs if x > eps)
    if not vals:
        return 0
    groups = 1
    last = vals[0]
    for x in vals[1:]:
        if abs(x - last) > eps:
            groups += 1
            last = x
    return groups


def test_zero_visibility():
    eigs = [0] * 81
    assert rank_positive(eigs) == 0
    assert traces(eigs) == (0, 0, 0)
    assert split_count(eigs) == 0


def test_isotropic_full_visibility():
    eigs = [2] * 81
    t1, t2, deff = traces(eigs)
    assert rank_positive(eigs) == 81
    assert t1 == 162
    assert t2 == 324
    assert deff == 81
    assert split_count(eigs) == 1


def test_split_visibility():
    eigs = [3] * 40 + [1] * 41
    t1, t2, deff = traces(eigs)
    assert rank_positive(eigs) == 81
    assert t1 == 161
    assert t2 == 401
    assert deff < 81
    assert split_count(eigs) == 2


def test_rank_defective_visibility():
    eigs = [1] * 27 + [0] * 54
    assert rank_positive(eigs) == 27
    assert split_count(eigs) == 1


def test_threshold_names():
    thresholds = ["p_geom", "p_H1", "p_full", "p_split"]
    assert thresholds == ["p_geom", "p_H1", "p_full", "p_split"]
