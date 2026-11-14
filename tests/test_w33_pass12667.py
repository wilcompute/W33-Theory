"""Pass 12667: attractor flows stay physical, end at a pseudo-pure state, majorised by the start."""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda f: json.load(open(os.path.join(ROOT, "data", f)))


def test_paths_physical_and_endpoint_pseudo_pure():
    d = load("w33_attractor_path_physicality.json")
    assert d["all_paths_physical"] and d["all_endpoints_pseudo_pure"] and len(d["rows"]) == 8
    for r in d["rows"]:
        assert r["min_at_t"] == 0.0 and r["V_monotone_decreasing"] and r["purity_monotone"] and r["purity_end"] <= r["purity_start"] + 1e-12
        assert abs(r["endpoint_min_eig"] - r["predicted_endpoint_min_eig"]) < 1e-6


def test_majorisation_census():
    d = load("w33_attractor_majorisation.json")
    assert d["failures"] == 0 and d["points_with_N_positive"] > 150000 and d["worst_margin"] > -1e-12


def test_majorisation_spot_checks_independent():
    rng = np.random.default_rng(99)
    for _ in range(5000):
        p = np.sort(rng.dirichlet(np.ones(4) * 0.7) / 2)[::-1]
        N = sum((8 * x - 1) ** 3 for x in p) / 24
        if N <= 0:
            continue
        c = N ** (1 / 3)
        a = np.repeat(p, 2)
        b = np.array([c / 2 + (1 - c) / 8] * 2 + [(1 - c) / 8] * 6)
        assert np.all(np.cumsum(a) >= np.cumsum(b) - 1e-12)
        assert np.min(np.linalg.eigvalsh(np.diag(b))) >= -1e-15
