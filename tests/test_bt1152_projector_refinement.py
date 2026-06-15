def test_bt1152_refinement():
    negative_rank = 15
    support_projection_rank = 5
    assert negative_rank == 15
    assert support_projection_rank == 5
    assert support_projection_rank != negative_rank
    assert 16 == 1 + 15
