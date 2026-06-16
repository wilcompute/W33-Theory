def test_bt1197_projection_codec():
    rows = []
    for t in range(45):
        for h in range(48):
            rows.append((t, h, 16*t + h % 16, h // 16, 6*t + h // 8, h % 8, 2*t + h // 24, h % 24))
    assert len(rows) == 2160
    assert len({(r[2], r[3]) for r in rows}) == 2160
    assert len({(r[4], r[5]) for r in rows}) == 2160
    assert len({(r[6], r[7]) for r in rows}) == 2160
