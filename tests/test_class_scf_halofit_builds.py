"""Regression guard for the CLASS halofit scalar-field bug (Pass 12632; lesgourg/class_public#682).

Every patched build (~/cosmo/class_{fading,klt,klt2,massive}_hf) must give LCDM-as-scalar-field the same halofit boost
P_nl/P_lin as plain Lambda (to 1e-5; measured 2e-6, the Omega_scf shooting precision), and the unpatched build must still
differ (so the test would notice if the control itself broke).  Needs WSL with the builds, so it runs only with
RUN_CLASS_TESTS=1; CI skips it.  The committed certificates are checked by tests/test_w33_pass12632.py.
usage: RUN_CLASS_TESTS=1 py -3 -m pytest -q tests/test_class_scf_halofit_builds.py"""
import json
import os
import subprocess

import pytest

pytestmark = pytest.mark.skipif(os.environ.get("RUN_CLASS_TESTS") != "1", reason="needs WSL CLASS builds; set RUN_CLASS_TESTS=1")

SCRIPT = r"""
import json, os, sys
import numpy as np
os.chdir("/mnt/c/tmp/toe_wt/analysis/toe_uv"); sys.path.insert(0, ".")
import class_cmb as C
H = os.path.expanduser("~/cosmo")
L = json.load(open("class_fit_dovekie.json"))["LCDM"]["p"]
extra = "z_pk=0.01,1.0\nz_max_pk=3.1\nP_k_max_1/Mpc=30"
def boost(p, kind, b):
    kp = {}
    C.run_class(dict(p, mnu=0.06), kind, extra=extra, keep=kp, binp=b)
    r = []
    for i in (1, 2):
        nl = np.loadtxt(f"{kp['tag']}/o_z{i}_pk_nl.dat"); li = np.loadtxt(f"{kp['tag']}/o_z{i}_pk.dat")
        r += [float(np.interp(k, nl[:, 0], nl[:, 1]) / np.interp(k, li[:, 0], li[:, 1])) for k in (0.1, 1.0, 3.0)]
    os.system(f"rm -rf {kp['tag']}")
    return r
ref = boost(dict(L), "lambda", H + "/class_fading/class")
out = {}
for b in ("class_fading", "class_fading_hf", "class_massive_hf"):
    s = boost(dict(L, c=0.0, cp=0.0), "fading", f"{H}/{b}/class")
    out[b] = max(abs(x / y - 1) for x, y in zip(s, ref))
print("RESULT " + json.dumps(out))
"""


def test_patched_builds_match_lambda():
    r = subprocess.run(["wsl", "-e", "bash", "-lc", "OMP_NUM_THREADS=4 python3 -"], input=SCRIPT, capture_output=True, text=True, timeout=1800)
    line = next(x for x in r.stdout.splitlines() if x.startswith("RESULT "))
    dev = json.loads(line[7:])
    assert dev["class_fading"] > 0.25, dev  # the bug is still visible in the unpatched build (control)
    assert dev["class_fading_hf"] < 1e-5, dev
    assert dev["class_massive_hf"] < 1e-5, dev
