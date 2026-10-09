"""Independent five-state collective Hermite orbit/energy regression."""
from pathlib import Path
import importlib.util
import math
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ritz',ROOT/'analysis/w33_20261008_5state_ritz.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def test_five_state_symmetry_and_upper_bound():
    geo=m.geometry()
    assert m.orbit_guard(geo)==8
    tr=m.prior.exact_trial()
    low=m.build_matrix(geo,tr,7)
    high=m.build_matrix(geo,tr,8)
    import numpy as np
    assert np.max(np.abs(low-high))<1e-9
    val=float(np.linalg.eigvalsh(low)[0])
    assert math.isclose(val,127.61937784333911,abs_tol=1e-8)
    assert val<127.61950907272602
