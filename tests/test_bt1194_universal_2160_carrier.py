def test_bt1194_universal_2160_carrier():
    vals = [2160, 720*3, 270*8, 45*48, 90*24]
    assert all(v == 2160 for v in vals)
