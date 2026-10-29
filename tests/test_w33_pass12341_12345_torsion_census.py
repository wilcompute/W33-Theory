"""Independent root-of-unity and matrix checks for the finite-cover extension."""
from itertools import product
from pathlib import Path
import hashlib
import json
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass12341_12345_torsion_census as core
import w33_20261027_five_front_followthrough as prior
import w33_20261027_native_bloch_face_module as native


def independent_pair_census(roots, omega_square):
    """Use integer pairs in Z[i] or Z[omega], with no modular screening."""
    result = []
    for labels in product(range(len(roots)), repeat=4):
        a = np.array([roots[t][0]-1 for t in labels], dtype=np.int64)
        b = np.array([roots[t][1] for t in labels], dtype=np.int64)
        aa = int(a @ core.N @ a); ab = int(a @ core.N @ b); bb = int(b @ core.N @ b)
        if aa + omega_square[0]*bb == 0 and 2*ab + omega_square[1]*bb == 0:
            if any(labels):
                result.append(list(labels))
    return result


def test_exact_census_against_gaussian_and_eisenstein_arithmetic():
    fourth = [(1,0),(0,1),(-1,0),(0,-1)]
    sixth = [(1,0),(1,1),(0,1),(-1,0),(-1,-1),(0,-1)]
    assert core.census(4)["nonidentity_loop_labels"] == independent_pair_census(fourth, (-1,0))
    assert core.census(6)["nonidentity_loop_labels"] == independent_pair_census(sixth, (-1,-1))
    assert len(independent_pair_census(sixth, (-1,-1))) == 10


def test_screen_false_positive_is_removed_by_exact_reduction():
    row = core.census(31)
    assert row["modular_candidates"] > 1
    assert row["nonidentity_count"] == 0


def test_variational_bound_against_an_independent_spectral_solve():
    check = core.soft_mode_control()
    assert check["certified_n0"] == 12172
    assert check["certified_rayleigh_coefficient"] == 1652352
    _, voltage, edges, _, _, comm, _, _ = prior.inputs()
    f = json.loads((ROOT / "data/PART_20261023_NATIVE_ZERO_HOLONOMY_FACE_COMPLETION.json").read_text())
    short = [x["boundary"] for x in f["independent_face_basis"]]
    for item in (check["numeric_rayleigh_controls"][0], check["numeric_rayleigh_controls"][3]):
        n = item["n"]; m = (n+1)//3
        k = np.array([2*np.pi*m/n, 2*np.pi*m/n, 0, 0])
        A = np.vstack((native.curl(short, voltage, k), core.R @ native.curl(comm, voltage, k)))
        D = native.gradient(voltage, edges, k)
        rank, eigen = native.transverse(A, D)
        assert rank == 27
        assert -1e-12 < eigen[0] <= item["rayleigh_upper_bound"] + 1e-10
        assert item["n_squared_times_rayleigh"] < 51


def test_committed_data_matches_producer_and_census_range():
    data = json.loads((ROOT / "data/w33_pass12341_12345_torsion_census.json").read_text())
    assert data["source_sha256"] == hashlib.sha256(Path(core.__file__).read_bytes()).hexdigest()
    assert [r["n"] for r in data["census"]] == list(range(2,65))
    assert all(r["nonidentity_count"] == (10 if r["n"] % 3 == 0 else 0)
               for r in data["census"])
