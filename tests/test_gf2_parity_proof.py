import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts"


def ensure_file_generated(script, out_path):
    if not out_path.exists():
        subprocess.check_call([sys.executable, script])


def ensure_gf2_certificates():
    ensure_file_generated(
        str(ROOT / "tools" / "generate_gf2_certificate.py"),
        ART / "gf2_certificates.json",
    )


def ensure_minimal_hitting_sets():
    ensure_file_generated(
        str(ROOT / "tools" / "minimal_hitting_sets.py"),
        ART / "minimal_hitting_sets.json",
    )


def test_certificates_are_contradictions():
    # ensure generated certificates show A * v = 0 and RHS parity = 1
    ensure_gf2_certificates()
    certs = json.load(open(ART / "gf2_certificates.json", "r", encoding="utf-8"))
    assert certs, "No gf2 certificates found; run tools/generate_gf2_certificate.py"
    for entry in certs:
        assert entry["is_null"], f"Certificate left side not zero for {entry['file']}"
        assert entry["rhs_is_one"], f"Certificate RHS parity != 1 for {entry['file']}"


def test_minimal_hitting_sets_contains_020_23():
    ensure_minimal_hitting_sets()
    hs = json.load(open(ART / "minimal_hitting_sets.json", "r", encoding="utf-8"))
    hitting_sets = hs.get("hitting_sets", [])
    assert any([[0, 20, 23]] == hs_ for hs_ in hitting_sets) or any(
        [[0, 20, 23]] in [list(x) for x in hs_] for hs_ in hitting_sets
    ), "Expected hitting set [0,20,23] not found"


def test_all_odd_null_vectors_include_020_23():
    # Repeat the nullspace search up to weight 10 and ensure every odd-parity null vector includes triad (0,20,23)
    heis_path = ART / "e6_cubic_affine_heisenberg_model.json"
    sdata_path = ART / "e6_cubic_sign_gauge_solution.json"
    if not heis_path.exists() or not sdata_path.exists():
        import pytest

        pytest.skip(
            "Missing artifacts for null-space GF(2) check; skipping in this environment."
        )

    heis = json.load(open(heis_path, "r", encoding="utf-8"))
    triads = [
        tuple(sorted(tri)) for item in heis["affine_u_lines"] for tri in item["triads"]
    ]
    assert len(triads) == 36
    # build node incidence rows
    rows = []
    for node in range(27):
        mask = 0
        for i, tri in enumerate(triads):
            if node in tri:
                mask |= 1 << i
        rows.append(mask)
    # elimination to find nullspace basis
    m = 27
    n = 36
    rows_copy = rows.copy()
    pivots = {}
    row_idx = 0
    for col in range(n):
        pivot_row = None
        for r in range(row_idx, m):
            if (rows_copy[r] >> col) & 1:
                pivot_row = r
                break
        if pivot_row is None:
            continue
        rows_copy[row_idx], rows_copy[pivot_row] = (
            rows_copy[pivot_row],
            rows_copy[row_idx],
        )
        pivots[col] = row_idx
        for r in range(m):
            if r != row_idx and ((rows_copy[r] >> col) & 1):
                rows_copy[r] ^= rows_copy[row_idx]
        row_idx += 1
    free_vars = [i for i in range(n) if i not in pivots]
    pivot_rows = {c: rows_copy[r] for c, r in pivots.items()}
    basis = []
    for f in free_vars:
        x = 1 << f
        for c, rmask in pivot_rows.items():
            if (rmask >> f) & 1:
                x |= 1 << c
        basis.append(x)
    # load dmap
    sdata = json.load(
        open(ART / "e6_cubic_sign_gauge_solution.json", "r", encoding="utf-8")
    )
    dmap = {
        tuple(sorted(t["triple"])): 0 if t["sign"] == 1 else 1
        for t in sdata["solution"]["d_triples"]
    }
    # BFS enumeration of null vectors weight<=10
    from collections import deque

    queue = deque([(basis[i], [i]) for i in range(len(basis))])
    seen = set(basis)
    maxw = 10
    target_tri = (0, 20, 23)
    while queue:
        vec, idxs = queue.popleft()
        w = vec.bit_count()
        supp = [i for i in range(n) if (vec >> i) & 1]
        d_par = sum(dmap.get(triads[i], 0) for i in supp) % 2
        if w <= maxw and d_par == 1:
            # ensure target tri appears in support
            assert target_tri in [
                triads[i] for i in supp
            ], f"Odd null vector without {target_tri} found: support {supp}"
        if len(idxs) < len(basis):
            last = idxs[-1]
            for j in range(last + 1, len(basis)):
                newvec = vec ^ basis[j]
                if newvec not in seen:
                    seen.add(newvec)
                    queue.append((newvec, idxs + [j]))
