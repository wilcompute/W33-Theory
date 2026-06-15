def test_bt1153_clifford_completion():
    grade_counts = [1, 4, 6, 4, 1]
    assert sum(grade_counts) == 16
    assert sum(grade_counts[1:]) == 15
    assert grade_counts[0] == 1
    assert grade_counts[4] == 1
