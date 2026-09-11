from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_projective_horizon_lag_law import build_result  # noqa: E402


def test_minus_one_over_84_is_pair_correlation_not_markov_decay() -> None:
    data = build_result()
    assert data["status"] == "PASS"
    assert all(data["checks"].values())
    assert data["theorem"]["pairwise_correlation"] == "rho_n=-1/(4*|PG(n-1,4)|)"

    n3 = data["n3_projective_anticorrelation"]
    assert n3["projective_microstates"] == 85
    assert n3["boundary_sector_microstates"] == 21
    assert n3["pairwise_correlation"] == "-1/84"
    assert n3["autocorrelation_over_one_period"] == ["1", "-1/84", "-1/84", "-1/84", "1"]
    assert [x["lag"] for x in n3["all_nonzero_lags"]] == [1, 2, 3]
    assert n3["return_lag"] == 4
    assert n3["non_markov_witness"]["P_squared"] != n3["non_markov_witness"]["actual_lag2"]
