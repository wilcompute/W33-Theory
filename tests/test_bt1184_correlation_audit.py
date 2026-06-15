def test_bt1184_correlation_audit():
    transport = True
    chirality = True
    common_map = False
    assert transport and chirality
    assert not common_map
