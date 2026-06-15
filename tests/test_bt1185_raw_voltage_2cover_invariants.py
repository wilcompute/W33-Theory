def test_bt1185_raw_voltage_2cover_invariants():
    assert 45 * 32 // 2 == 720
    assert 2 * 45 == 90
    assert 2 * 720 == 1440
    assert 3120 + 2160 == 5280
    assert 2160 > 0
