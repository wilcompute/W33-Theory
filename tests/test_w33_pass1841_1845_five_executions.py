from analysis.w33_pass1841_1845_five_executions import verify


def test_pass1841_1845_frozen_certificate():
    result = verify(run_worker=False)
    assert result['status'] == 'PASS', result
    assert result['passed'] == result['total']
