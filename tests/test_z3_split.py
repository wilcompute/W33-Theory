import glob
import json
import os
import sys
from pathlib import Path

import numpy as np
import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from w33_full_decomposition import build_psp43_group, compute_full_hodge_eigenbasis
from w33_homology import build_clique_complex, build_w33


def test_z3_candidate_exists_and_splits():
    files = sorted(
        glob.glob("checks/PART_CVII_z3_candidates_*.json"), key=os.path.getmtime
    )
    if not files:
        pytest.skip("optional z3 candidates file is absent from checks/")
    j = files[-1]
    data = json.load(open(j, "r", encoding="utf-8"))
    assert data.get("checked", 0) > 0
    cand = data["candidates"][0]

    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    hodge = compute_full_hodge_eigenbasis(n, adj, edges, simplices)
    V_harm = hodge["harmonic"]

    group = build_psp43_group(vertices, edges)
    vperm = tuple(cand["vertex_perm"])
    assert vperm in group
    ep, es = group[vperm]
    ep = np.asarray(ep, dtype=int)
    es = np.asarray(es, dtype=float)

    # compute restricted action
    temp = V_harm * es[:, None]
    Y = np.zeros_like(V_harm, dtype=float)
    Y[ep, :] = temp
    R = V_harm.T.conj() @ Y

    # R^3 approx identity
    err = np.linalg.norm(R @ R @ R - np.eye(R.shape[0]))
    assert err < 1e-8, f"R^3 - I too large: {err}"

    w = np.linalg.eigvals(R)
    roots = [1.0 + 0j, complex(-0.5, np.sqrt(3) / 2), complex(-0.5, -np.sqrt(3) / 2)]
    counts = [int(((np.abs(w - r)) < 1e-6).sum()) for r in roots]
    assert counts == [27, 27, 27], f"Got eigen-counts {counts}"
