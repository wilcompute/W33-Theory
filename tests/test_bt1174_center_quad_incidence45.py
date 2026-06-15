def test_bt1174_comparison():
    point_edges = 270
    comp_edges = 720
    assert point_edges + comp_edges == 45 * 44 // 2
    assert 12 + 32 == 44
    assert (45, 12, 3, 3) == (45, 12, 3, 3)
