def test_bt1200_projection_codec_counts():
    assert 45 * 48 == 2160
    assert (45 * 16) * 3 == 2160
    assert (45 * 6) * 8 == 2160
    assert (45 * 2) * 24 == 2160
    assert 54 * 40 == 2160
