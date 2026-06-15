def test_bt1180_transport_cover_counts():
    base_v = 45
    base_k = 32
    base_e = base_v * base_k // 2
    assert base_e == 720
    assert 2 * base_v == 90
    assert 2 * base_e == 1440
