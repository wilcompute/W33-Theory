#!/usr/bin/env python3
"""Execute the locally checked E6 normal-form and synthetic frontiers."""
from w33_e6_normal_form_local import run
if __name__ == '__main__':
    result = run()
    assert result['e6']['exact_rank'] == 78
    print(result)
