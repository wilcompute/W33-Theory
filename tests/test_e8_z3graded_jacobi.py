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


def test_e8_z3graded_bracket_satisfies_jacobi():
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

    # Empirically locked by the Jacobi tuning in the tool:
    #   scale_sl3 = +1/6,  scale_g2g2 = -1/6, with scale_e6=1, scale_g1g1=1.
    br = tool.E8Z3Bracket(
        e6_projector=proj,
        cubic_triads=triads,
        scale_g1g1=1.0,
        scale_g2g2=-1.0 / 6.0,
        scale_e6=1.0,
        scale_sl3=1.0 / 6.0,
    )

    rng = np.random.default_rng(0)

    def rand_g1():
        return tool._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=2,
            scale2=0,
            include_g0=False,
            include_g2=False,
        )

    def rand_g2():
        return tool._random_element(
            rng,
            e6_basis,
            scale0=0,
            scale1=0,
            scale2=2,
            include_g0=False,
            include_g1=False,
        )

    def rand_g0():
        return tool._random_element(
            rng,
            e6_basis,
            scale0=2,
            scale1=0,
            scale2=0,
            include_g0=True,
            include_g1=False,
            include_g2=False,
        )

    def rand_all():
        return tool._random_element(
            rng,
            e6_basis,
            scale0=2,
            scale1=2,
            scale2=2,
            include_g0=True,
            include_g1=True,
            include_g2=True,
        )

    cases = [
        ("g0_g0_g0", (rand_g0, rand_g0, rand_g0)),
        ("g1_g1_g1", (rand_g1, rand_g1, rand_g1)),
        ("g2_g2_g2", (rand_g2, rand_g2, rand_g2)),
        ("g1_g1_g2", (rand_g1, rand_g1, rand_g2)),
        ("g1_g2_g2", (rand_g1, rand_g2, rand_g2)),
        ("mixed_all", (rand_all, rand_all, rand_all)),
    ]

    for _, (fx, fy, fz) in cases:
        for _trial in range(30):
            x, y, z = fx(), fy(), fz()
            j = tool._jacobi(br, x, y, z)
            assert tool._elt_norm(j) < 1e-9
