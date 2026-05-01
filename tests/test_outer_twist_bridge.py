import json
from pathlib import Path

import numpy as np
import pytest

BUNDLE = Path("CE2_OUTER_TWIST_TO_WEIL_BRIDGE_BUNDLE_v01")
pytestmark = pytest.mark.skipif(
    not BUNDLE.exists(),
    reason="optional outer-twist Weil bridge bundle missing",
)


def mat_mod3(M):
    return np.array(M, dtype=int) % 3


def det2(A):
    return int((A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]) % 3)


def test_outer_twist_spinor_det():
    data = json.load(open(BUNDLE / "outer_twist_on_sl2_layer.json"))
    A = np.array(data["induced_GL2_on_U_over_Z"], dtype=int) % 3
    assert det2(A) == 2, "determinant should be 2 (nonsquare) under outer twist"


def test_mu_recovery_gauge():
    mu = json.load(open(BUNDLE / "mu_recovery.json"))
    # verify that after applying the recorded gauge correction the formulas match
    corr = mu["gauge_to_canonical"]
    assert corr["scale_center_s"] == 2
    assert corr["linear_cochain_l(a,b)=u*a+v*b"]["u"] == 2
    assert corr["linear_cochain_l(a,b)=u*a+v*b"]["v"] == 0
    # canonical expressions given in result string
    assert "mu_S(a,b)=2ab" in corr["result"]
    assert "mu_T(a,b)=2a^2" in corr["result"]


def test_heisenberg_commutator():
    Udat = json.load(open(BUNDLE / "heisenberg_U_generators.json"))
    x = mat_mod3(Udat["x"])
    y = mat_mod3(Udat["y"])
    z = mat_mod3(Udat["z_center"])

    # compute commutator [x,y]
    def mat_mul(A, B):
        return (A @ B) % 3

    def mat_inv(M):
        return np.linalg.inv(M) % 3

    comm = mat_mul(mat_mul(x, y), mat_mul(mat_inv(x), mat_inv(y)))
    # commutator should equal z or z^2
    comm_bytes = comm.reshape(-1).tolist()
    z_bytes = z.reshape(-1).tolist()
    z2_bytes = mat_mul(z, z).reshape(-1).tolist()
    assert comm_bytes == z_bytes or comm_bytes == z2_bytes


def test_verify_bridge_script_runs(capsys):
    import subprocess
    import sys

    # run the verifier as a subprocess to avoid polluting namespace
    res = subprocess.run(
        [sys.executable, "verify_bridge.py"], cwd=BUNDLE, capture_output=True, text=True
    )
    assert res.returncode == 0
    assert "outer twist induces det=-1" in res.stdout
