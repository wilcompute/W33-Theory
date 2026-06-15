def test_bt1156_grade_decomposition():
    grades = [4, 6, 4, 1]
    assert sum(grades) == 15
    assert grades[-1] == 1
