def test_bt1165_counts():
    cols = [16, 24, 16, 4]
    image = [4, 6, 4, 1]
    rel = [12, 18, 12, 3]
    assert sum(cols) == 60
    assert sum(image) == 15
    assert sum(rel) == 45
    assert rel == [3*x for x in image]
