from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_cubic_sym_numba_equivalence():
    # skip test if numba is not installed (numba is optional / accelerates kernel)
    pytest.importorskip("numba")

    repo_root = Path(__file__).resolve().parents[1]
    tool = _load_module(
        repo_root / "tools" / "toe_e8_z3graded_bracket_jacobi.py",
        "toe_e8_z3graded_bracket_jacobi",
    )

    basis_path = repo_root / "artifacts" / "e6_27rep_basis_export" / "E6_basis_78.npy"
    if not basis_path.exists():
        pytest.skip(
            "Missing E6 basis export; run build_e6_27rep_minuscule.py --export-basis78"
        )
    e6_basis = np.load(basis_path).astype(np.complex128)

    triads = tool._load_signed_cubic_triads()
    proj = tool.E6Projector(e6_basis)

    # baseline (numpy) and numba-enabled brackets
    br = tool.E8Z3Bracket(e6_projector=proj, cubic_triads=triads, use_numba=False)
    br_numba = tool.E8Z3Bracket(e6_projector=proj, cubic_triads=triads, use_numba=True)

    rng = np.random.default_rng(42)
    for _ in range(5):
        # complex test vectors
        u = (rng.standard_normal(27) + 1j * rng.standard_normal(27)).astype(
            np.complex128
        )
        v = (rng.standard_normal(27) + 1j * rng.standard_normal(27)).astype(
            np.complex128
        )
        out0 = br.cubic_sym(u, v, scale=0.75)
        out1 = br_numba.cubic_sym(u, v, scale=0.75)
        np.testing.assert_allclose(out0, out1, rtol=1e-12, atol=1e-12)
