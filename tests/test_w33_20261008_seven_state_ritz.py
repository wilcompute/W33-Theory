"""Extended W33 collective Hermite Ritz regression."""
import importlib.util
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v7',ROOT/'analysis/w33_20261008_7state_ritz.py')
mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def test_seven_state_ritz():
    a=mod.ritz(9)
    b=mod.ritz(10)
    assert np.max(np.abs(a-b))<1e-8
    v=float(np.linalg.eigvalsh(a)[0])
    v5=float(np.linalg.eigvalsh(a[:5,:5])[0])
    assert abs(v-127.61920315299878)<1e-8
    assert v < v5-0.00017
    assert np.max(np.abs(a-a.conj().T))<1e-8
