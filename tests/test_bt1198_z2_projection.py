def test_bt1198_z2_projection():
    z2_by_c3 = {0: {0}, 1: {0, 1}, 2: {1}}
    assert z2_by_c3[1] == {0, 1}
    assert not all(len(v) == 1 for v in z2_by_c3.values())
    assert 720 * 3 == 2160
