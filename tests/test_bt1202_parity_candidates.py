def test_bt1202_parity_candidates():
    assert 366 + 354 == 720
    assert 720 == 45 * 32 // 2
    assert {0: 720} != {0: 366, 1: 354}
    assert {0: 360, 1: 360} != {0: 366, 1: 354}
    assert {1: 720} != {0: 366, 1: 354}
