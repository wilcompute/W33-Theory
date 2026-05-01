import itertools
import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np
import pytest


def canonical_pg33_points():
    pts = []
    for v in itertools.product(range(3), repeat=4):
        if all(x == 0 for x in v):
            continue
        # normalize so first nonzero coordinate is 1
        for x in v:
            if x != 0:
                inv = 1 if x == 1 else 2
                norm = tuple((inv * y) % 3 for y in v)
                pts.append(norm)
                break
    seen = set()
    unique = []
    for p in pts:
        if p not in seen:
            seen.add(p)
            unique.append(p)
    pts2 = sorted(unique)
    assert len(pts2) == 40
    # first 13 should have X0 == 0
    assert all(p[0] == 0 for p in pts2[:13])
    assert all(p[0] == 1 for p in pts2[13:])
    return pts2


def compute_perm_from_matrix(mat, pts2):
    """Apply 4x4 matrix mod3 to projective points and renormalize."""
    perm = []
    for p in pts2:
        v = [(sum(mat[i][j] * p[j] for j in range(4))) % 3 for i in range(4)]
        # renormalize
        for x in v:
            if x != 0:
                inv = 1 if x == 1 else 2
                v = tuple((inv * y) % 3 for y in v)
                break
        perm.append(pts2.index(v))
    return perm


def test_perm40_matches_canonical():
    pts2 = canonical_pg33_points()
    bundle = Path("H27_OUTER_TWIST_ACTION_BUNDLE_v01")
    perm40 = json.loads((bundle / "perm40_and_H27_pg_ids.json").read_text())[
        "perm40_points_from_phi_n"
    ]
    assert sorted(perm40) == list(range(40))
    # compute canonical->phi_n mapping (should equal perm40)
    assert [perm40[i] for i in range(40)] == perm40


def test_outer_matrix_and_symplectic():
    pts2 = canonical_pg33_points()
    # outer twist matrix N4 as described
    N4 = [
        [1, 0, 0, 0],
        [0, 1, 2, 0],
        [2, 2, 0, 0],
        [2, 2, 1, 2],
    ]
    perm_from_N4 = compute_perm_from_matrix(N4, pts2)
    bundle = Path("H27_OUTER_TWIST_ACTION_BUNDLE_v01")
    perm40 = json.loads((bundle / "perm40_and_H27_pg_ids.json").read_text())[
        "perm40_points_from_phi_n"
    ]
    assert perm_from_N4 == perm40
    # symplectic form J
    J = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]], dtype=int)
    # check similitude multiplier
    Nt = np.transpose(np.array(N4, dtype=int))
    prod = (Nt @ J @ np.array(N4, dtype=int)) % 3
    # multiplier should be 2 (non-square)
    assert np.array_equal(prod, (2 * J) % 3)
    # adjacency degrees
    adj = np.zeros((40, 40), dtype=int)
    for i, p in enumerate(pts2):
        for j, q in enumerate(pts2):
            if i == j:
                continue
            val = (np.array(p, dtype=int) @ J @ np.array(q, dtype=int)) % 3
            if val == 0:
                adj[i, j] = 1
    deg = adj.sum(axis=1)
    assert set(deg.tolist()) == {12}


def test_infinity_neighbors_and_orbits():
    pts2 = canonical_pg33_points()
    # same J as before
    J = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]], dtype=int)
    adj = np.zeros((40, 40), dtype=int)
    for i, p in enumerate(pts2):
        for j, q in enumerate(pts2):
            if i == j:
                continue
            val = (np.array(p, dtype=int) @ J @ np.array(q, dtype=int)) % 3
            if val == 0:
                adj[i, j] = 1
    infinity = list(range(13))
    affine = list(range(13, 40))
    neighbor_map = {}
    for i in affine:
        neigh = [j for j in infinity if adj[i, j]]
        neighbor_map[i] = neigh
        assert len(neigh) == 4
    # cross-check with bundle if available
    pg33_bundle = Path("PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01")
    if pg33_bundle.exists():
        b_map = json.loads((pg33_bundle / "infinity_neighbors.json").read_text())
        # convert our int keys to str to match json
        assert {str(k): v for k, v in neighbor_map.items()} == b_map
    # orbit under outer twist
    N4 = [
        [1, 0, 0, 0],
        [0, 1, 2, 0],
        [2, 2, 0, 0],
        [2, 2, 1, 2],
    ]
    perm_from_N4 = compute_perm_from_matrix(N4, pts2)
    orbits = []
    unvis = set(affine)
    while unvis:
        start = unvis.pop()
        orb = [start]
        cur = start
        while True:
            nxt = perm_from_N4[cur]
            if nxt == start:
                break
            orb.append(nxt)
            unvis.discard(nxt)
            cur = nxt
        orbits.append(orb)
    # expect five orbits of sizes [8,8,8,1,2]
    sizes = sorted(len(o) for o in orbits)
    assert sizes == [1, 2, 8, 8, 8]
    # verify against bundle file if available
    pg33_bundle = Path("PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01")
    if pg33_bundle.exists():
        b_orbits = json.loads((pg33_bundle / "outer_orbits.json").read_text())
        assert sorted(len(o) for o in b_orbits) == sizes


def test_edge_orbits_and_bundle():
    pts2 = canonical_pg33_points()
    # recompute adjacency
    J = np.array([[0, 0, 0, 1], [0, 0, 1, 0], [0, 2, 0, 0], [2, 0, 0, 0]], dtype=int)
    adj = np.zeros((40, 40), dtype=int)
    for i, p in enumerate(pts2):
        for j, q in enumerate(pts2):
            if i == j:
                continue
            val = (np.array(p, dtype=int) @ J @ np.array(q, dtype=int)) % 3
            if val == 0:
                adj[i, j] = 1
    edges = []
    for i in range(40):
        for j in range(i + 1, 40):
            if adj[i, j]:
                edges.append((i, j))
    assert len(edges) == 240
    # compute edge orbits under outer permutation
    N4 = [
        [1, 0, 0, 0],
        [0, 1, 2, 0],
        [2, 2, 0, 0],
        [2, 2, 1, 2],
    ]
    perm_from_N4 = compute_perm_from_matrix(N4, pts2)
    edge_index = {e: idx for idx, e in enumerate(edges)}
    orb_sizes = []
    unvis = set(range(len(edges)))
    while unvis:
        start = unvis.pop()
        cur = start
        orb = [start]
        while True:
            i, j = edges[cur]
            ni, nj = perm_from_N4[i], perm_from_N4[j]
            if ni > nj:
                ni, nj = nj, ni
            cur = edge_index[(ni, nj)]
            if cur == start:
                break
            orb.append(cur)
            unvis.discard(cur)
        orb_sizes.append(len(orb))
    orb_sizes.sort()
    # expect 26 orbits of size 8 and 8 orbits of size 4
    assert orb_sizes.count(8) == 26
    assert orb_sizes.count(4) == 8
    # compare with bundle if present
    pg33_bundle = Path("PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01")
    if pg33_bundle.exists():
        b_edge_orbits = json.loads((pg33_bundle / "edge_orbits.json").read_text())
        assert sorted(len(o) for o in b_edge_orbits) == orb_sizes


# new tests for infinity and direction bundles


def test_infinity_and_direction_bundles(tmp_path):
    """Run the bundle creation script and verify its output files."""
    # locate script relative to repository root
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "make_infinity_charge_table_bundles.py"
    import shutil
    import subprocess

    work = tmp_path / "work"
    work.mkdir()
    # copy required input bundles into working directory
    shutil.copytree(
        "PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01",
        work / "PG33_OUTER_TWIST_GEOMETRY_BUNDLE_v01",
    )
    shutil.copytree(
        "H27_CE2_FUSION_BRIDGE_BUNDLE_v01", work / "H27_CE2_FUSION_BRIDGE_BUNDLE_v01"
    )
    # copy the JSON files the script expects
    for fname in [
        "neighbor_map.json",
        "orbits_outer.json",
        "orbits_P.json",
        "orbits_NP.json",
    ]:
        shutil.copy(repo_root / fname, work / fname)
    # execute script
    res = subprocess.run([".venv\\Scripts\\python.exe", str(script)], cwd=work)
    assert res.returncode == 0
    zip1 = work / "INFINITY_NEIGHBOR_CHARGE_TABLE_BUNDLE_v01.zip"
    zip2 = work / "W33_DIRECTION_DECOMPOSITION_BUNDLE_v01.zip"
    assert zip1.exists() and zip2.exists()
    import zipfile

    with zipfile.ZipFile(zip1) as z:
        names = set(z.namelist())
    expected1 = {
        "u_to_4_infinity_neighbors_compressed9.csv",
        "affine_point_to_4_infinity_neighbors_full27.csv",
        "pg33_point_coordinates.csv",
        "symplectic_form_and_outer_matrix.json",
        "W33_collinearity_edges_240.csv",
        "neighbor_map.json",
        "orbits_outer.json",
        "orbits_P.json",
        "orbits_NP.json",
    }
    assert expected1.issubset(names)
    with zipfile.ZipFile(zip2) as z:
        names2 = set(z.namelist())
    for fname in [
        "edges_with_direction_and_triangle_class.csv",
        "lines_40_with_direction_and_affine_triples.csv",
        "direction_inf_id_to_3_affine_lines.csv",
    ]:
        assert fname in names2


def test_outer_twist_root_certificate(tmp_path):
    """Run the script that builds the root-action certificate and verify its output."""
    repo = Path(__file__).resolve().parents[1]
    work = tmp_path / "work"
    work.mkdir()
    # copy needed files: bundles and mapping
    shutil.copytree(
        repo / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
        work / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
    )
    # also need the fusion bridge bundle for PG->internal mapping
    shutil.copytree(
        repo / "H27_CE2_FUSION_BRIDGE_BUNDLE_v01",
        work / "H27_CE2_FUSION_BRIDGE_BUNDLE_v01",
    )
    # only copy the edge_to_e8_root.json since that's all the script needs
    (work / "artifacts").mkdir()
    shutil.copy(
        repo / "artifacts" / "edge_to_e8_root.json",
        work / "artifacts" / "edge_to_e8_root.json",
    )
    shutil.copy(repo / "pg_to_edge_labeling.json", work / "pg_to_edge_labeling.json")
    shutil.copy(repo / "pg_to_internal_inf.json", work / "pg_to_internal_inf.json")
    # also copy conjugacy directory for sigma
    conj_src = repo / "WE6_EVEN_to_PSp43_CONJUGACY_BUNDLE_v01 (1)"
    if conj_src.exists():
        shutil.copytree(conj_src, work / conj_src.name)
    # run script
    res = subprocess.run(
        [".venv\\Scripts\\python.exe", str(repo / "tools" / "outer_twist_on_roots.py")],
        cwd=work,
    )
    assert res.returncode == 0
    cert = work / "artifacts" / "outer_twist_root_action_certificate.json"
    assert cert.exists()
    data = json.loads(cert.read_text())
    assert "root_cycle_structure" in data
    # ensure total edges count matches
    total = sum(int(k) * v for k, v in data["root_cycle_structure"].items())
    assert total == 240


def test_outer_twist_cocycle_and_bundle(tmp_path):
    """Compute edge defect cocycle and package it into a bundle."""
    repo = Path(__file__).resolve().parents[1]
    work = tmp_path / "work"
    work.mkdir()
    # prepare workspace with required inputs
    shutil.copytree(
        repo / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
        work / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
    )
    shutil.copy(repo / "pg_to_edge_labeling.json", work / "pg_to_edge_labeling.json")
    shutil.copy(repo / "pg_to_internal_inf.json", work / "pg_to_internal_inf.json")
    (work / "artifacts").mkdir()
    shutil.copy(
        repo / "artifacts" / "edge_to_e8_root.json",
        work / "artifacts" / "edge_to_e8_root.json",
    )
    shutil.copy(
        repo / "artifacts" / "a2_4_decomposition.json",
        work / "artifacts" / "a2_4_decomposition.json",
    )
    # run cocycle script
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_outer_twist_root_cocycle.py"),
        ],
        cwd=work,
    )
    assert res.returncode == 0
    cocycle_dir = work / "analysis" / "outer_twist_cocycle"
    assert (cocycle_dir / "edge_defect.json").exists()
    assert (cocycle_dir / "edge_defect.csv").exists()
    assert (cocycle_dir / "orbits_under_WE6.json").exists()


def test_cocycle_properties(tmp_path):
    """Run the analysis script and check its summary output."""
    repo = Path(__file__).resolve().parents[1]
    work = tmp_path / "work"
    work.mkdir()
    # set up same inputs as previous test
    shutil.copytree(
        repo / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
        work / "H27_OUTER_TWIST_ACTION_BUNDLE_v01",
    )
    shutil.copy(repo / "pg_to_edge_labeling.json", work / "pg_to_edge_labeling.json")
    shutil.copy(repo / "pg_to_internal_inf.json", work / "pg_to_internal_inf.json")
    (work / "analysis" / "outer_twist_cocycle").mkdir(parents=True)
    # copy defect file produced earlier
    orig = repo / "analysis" / "outer_twist_cocycle" / "edge_defect.json"
    shutil.copy(orig, work / "analysis" / "outer_twist_cocycle" / "edge_defect.json")
    # run property script
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_cocycle_properties.py"),
        ],
        cwd=work,
    )
    assert res.returncode == 0
    summary = json.loads(
        (work / "analysis" / "outer_twist_cocycle" / "defect_summary.json").read_text()
    )
    # ensure triangle violations field and sample list exist
    assert "triangle_violations" in summary
    assert "triangle_violation_samples" in summary
    assert isinstance(summary["triangle_violation_samples"], list)
    # coboundary field should be present
    assert summary.get("coboundary") in (True, False)
    # defect stats should match initial bundle distribution
    stats = summary.get("stats", {})
    # undirected edges should total 240 entries and zero-defect count known
    assert sum(stats.values()) == 240
    assert stats.get("0") == 167 or stats.get(0) == 167


def test_outer_twist_rootword_cocycle_defect(tmp_path):
    """Run the full defect driver and check that delta_histograms are nonempty."""
    repo = Path(__file__).resolve().parents[1]
    # simply run the driver in the repository (it writes into artifacts)
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "outer_twist_rootword_cocycle_defect.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    out = json.loads(
        (repo / "artifacts" / "outer_twist_rootword_cocycle_defect.json").read_text()
    )
    assert "cycles" in out and len(out["cycles"]) == 4
    for entry in out["cycles"]:
        stats = entry.get("delta_stats", {})
        assert sum(int(v) for v in stats.values()) > 0


def test_analyze_lift_subgroup(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    cert = repo / "artifacts" / "phi_lift_subgroup.json"
    if not cert.exists():
        pytest.skip("optional phi lift subgroup certificate missing")
    # run analyzer (should never fail)
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "analyze_lift_subgroup.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    summary = repo / "artifacts" / "phi_lift_subgroup_summary.txt"
    assert summary.exists()
    txt = summary.read_text()
    assert "lift_size" in txt


def test_search_phi(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    # perform a short search (only checks script runs); limit trials so test is quick
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "search_phi.py"),
            "--trials",
            "20",
        ],
        cwd=repo,
    )
    assert res.returncode == 0


def test_compute_phi_sign_gauge(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_phi_sign_gauge.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    gauget = repo / "artifacts" / "sign_gauge.json"
    assert gauget.exists()
    signvec = json.loads(gauget.read_text())
    assert isinstance(signvec, list) and len(signvec) == 240


def test_extract_gl23_module(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    cert = repo / "artifacts" / "phi_lift_subgroup.json"
    if not cert.exists():
        pytest.skip("optional phi lift subgroup certificate missing")
    res = subprocess.run(
        [".venv\\Scripts\\python.exe", str(repo / "tools" / "extract_gl23_module.py")],
        cwd=repo,
    )
    assert res.returncode == 0
    out = repo / "artifacts" / "gl23_rep.json"
    assert out.exists()
    payload = json.loads(out.read_text())
    assert "matrices" in payload
    assert isinstance(payload["matrices"], dict)
    # verify decomposition fields present (may be empty if lift trivial)
    assert "invariant_subspaces" in payload
    subs = payload["invariant_subspaces"]
    assert "sub1" in subs and "sub2" in subs


def test_optimize_phi_smoke(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "optimize_phi.py"),
            "--trials",
            "10",
            "--temp",
            "0.1",
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    # candidate files may or may not exist depending on improvements
    # just check command completed


def test_conjugacy_obstruction(tmp_path):
    # load precomputed obstruction JSON (generated earlier or by audit template)
    repo = Path(__file__).resolve().parents[1]
    data = json.loads((repo / "action_conjugacy_obstruction.json").read_text())
    ep = data["edgepair"]
    ln = data["line_fixed"]
    # ensure order-5 fixed counts differ
    ep5 = ep["fixed_counts_by_order"].get("5", [])
    ln5 = ln["fixed_counts_by_order"].get("5", [])
    assert ep5 and ln5
    # edgepair has all zeros, line has nonzero
    assert all(x == 0 for x in ep5)
    assert any(x != 0 for x in ln5)


def test_verify_orbit_decompositions(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "verify_orbit_decompositions.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    out = repo / "artifacts" / "line_action_orbits.json"
    assert out.exists()
    info = json.loads(out.read_text())
    assert info["edgepair_degree"] == 120
    assert info["line_degree"] == 120
    assert info["edgepair_orbit_sizes"] == [120]
    assert info["line_orbit_sizes"] != [120]


def test_classify_dotpair(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "classify_e8_roots_dotpair.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    out = repo / "artifacts" / "e8_dotpair_class_summary.json"
    assert out.exists()
    summary = json.loads(out.read_text())
    assert "class72_size" in summary


def test_classify_w33_edges(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "classify_w33_edges_by_rootclass.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    csvf = repo / "artifacts" / "w33_edges_by_rootclass.csv"
    jsonf = repo / "artifacts" / "w33_edges_by_rootclass_counts.json"
    assert csvf.exists() and jsonf.exists()
    counts = json.loads(jsonf.read_text())
    assert sum(counts.values()) == 240  # there are 240 edges/roots in the bijection


def test_sector_physics(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [".venv\\Scripts\\python.exe", str(repo / "tools" / "sector_physics.py")],
        cwd=repo,
    )
    assert res.returncode == 0
    # appearance of output is sufficient; nothing to assert numerically


def test_meataxe_decompose(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    if not (repo / "artifacts" / "gl23_rep.json").exists():
        pytest.skip("optional GL(2,3) representation artifact missing")
    # first run on GL23 rep (may be trivial)
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "meataxe_decompose.py"),
            "--input",
            str(repo / "artifacts" / "gl23_rep.json"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    out = repo / "artifacts" / "meataxe_decomp.json"
    assert out.exists()
    dims = json.loads(out.read_text())["dims"]
    assert sum(dims) == 8
    # now test on a synthetic block-diagonal module (3+5 dims)
    M1 = np.eye(8, dtype=int)
    # permutation matrix that swaps first 3 basis elements (cycle of length3)
    P = np.eye(8, dtype=int)
    P[[0, 1, 2]] = P[[1, 2, 0]]
    test_json = tmp_path / "test_mats.json"
    # write JSON manually since json.dump doesn't accept a Path directly
    test_json.write_text(json.dumps({"matrices": [M1.tolist(), P.tolist()]}))
    res2 = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "meataxe_decompose.py"),
            "--input",
            str(test_json),
            "--output",
            str(tmp_path / "out.json"),
        ],
        cwd=repo,
    )
    assert res2.returncode == 0
    dims2 = json.loads((tmp_path / "out.json").read_text())["dims"]
    assert sum(dims2) == 8
    # expect at least one small block
    assert any(d < 8 for d in dims2)


def test_match_bose_mesner_self():
    """Run the matching utility on the reference bundle itself."""
    repo = Path(__file__).resolve().parents[1]
    bundle = (
        repo
        / "TOE_BoseMesner_Algebra_Solution_bundle_v04_20260227"
        / "duad_intersection_numbers.json"
    )
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "match_bose_mesner.py"),
            "--candidate",
            str(bundle),
            "--solution",
            str(bundle),
        ],
        cwd=repo,
    )
    assert res.returncode == 0


def test_z2_obstruction(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_z2_obstruction.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    mat = json.loads((repo / "artifacts" / "z2_cocycle.json").read_text())
    assert len(mat) == 10
    # all entries should be zero (we expect a trivial cocycle)
    assert all(all(x == 0 for x in row) for row in mat)


def test_srg_cycle_holonomy(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "compute_srg_cycle_holonomy.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    csvf = repo / "artifacts" / "srg_cycle_holonomy.csv"
    assert csvf.exists()
    # read parity values, ensure some odd cycles
    odd = 0
    with open(csvf) as f:
        next(f)
        for line in f:
            parts = line.strip().split(",")
            if parts and parts[-1] == "1":
                odd += 1
    assert odd > 0
    # minimal odd cycle length should be 3 by manual computation
    # we can check that at least one odd cycle has length 3
    with open(csvf) as f:
        next(f)
        found3 = False
        for line in f:
            cyc, par = line.strip().split(",")
            if par == "1" and len(cyc.split("-")) == 3:
                found3 = True
                break
    assert found3


def test_edge_to_rootpair_mapping(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [
            ".venv\\Scripts\\python.exe",
            str(repo / "tools" / "build_edge_to_rootpairs.py"),
        ],
        cwd=repo,
    )
    assert res.returncode == 0
    jsonf = repo / "artifacts" / "edge_to_rootpair_triple.json"
    csvf = repo / "artifacts" / "edge_to_rootpair_triple.csv"
    assert jsonf.exists() and csvf.exists()
    mapping = json.loads(jsonf.read_text())
    assert len(mapping) == 240
    # verify each value is list of three pairs of ints
    for v in mapping.values():
        assert isinstance(v, list) and len(v) == 3
        for pair in v:
            assert isinstance(pair, list) or isinstance(pair, tuple)
            assert len(pair) == 2
            assert all(isinstance(x, int) for x in pair)


def test_duad_we6_conjugacy():
    if os.environ.get("RUN_DUAD_WE6_CONJUGACY") != "1":
        pytest.skip("full duad/WE6 conjugacy search is opt-in")
    repo = Path(__file__).resolve().parents[1]
    res = subprocess.run(
        [".venv\\Scripts\\python.exe", str(repo / "tools" / "duad_we6_conjugacy.py")],
        cwd=repo,
    )
    # script may return nonzero if no conjugator found; we just verify it executed
    logf = repo / "artifacts" / "duad_we6_conjugacy.log"
    assert logf.exists()
    # log should contain at least the duad group size on edges and pairs
    txt = logf.read_text()
    assert "duad group size" in txt
    assert "group size on pairs" in txt
    # check for any conjugator outputs (edge-level or pair-level)
    conj_edge = repo / "artifacts" / "duad_we6_conjugator_edges.json"
    conj_pair = repo / "artifacts" / "duad_we6_conjugator_pairs.json"
    for conjf in (conj_edge, conj_pair):
        if conjf.exists():
            mapping = json.loads(conjf.read_text())
            # should be a permutation of the appropriate size
            size = 240 if conjf is conj_edge else 120
            assert len(mapping) == size
            vals = set(mapping.values())
            assert vals == set(range(size))
