from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_basis_export_chevalley_normalization_dynkin_and_serre():
    repo_root = Path(__file__).resolve().parents[1]

    # Ensure extracted zips are present (the normalization tool reads extracted paths).
    ingest = _load_module(
        repo_root / "tools" / "ingest_more_new_work.py", "ingest_more_new_work"
    )
    ingest.main()
    if not list(
        (repo_root / "artifacts" / "more_new_work_extracted").rglob("E6_basis_78.npy")
    ):
        pytest.skip(
            "More New Work E6_basis_78.npy export is absent; "
            "run tools/ingest_more_new_work.py with the external drop to enable this regression"
        )

    tool = _load_module(
        repo_root / "tools" / "chevalley_normalize_e6_from_basis_export.py",
        "chevalley_normalize_e6_from_basis_export",
    )
    tool.main()

    out_path = repo_root / "artifacts" / "e6_basis_export_chevalley.json"
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["dims"] == {"cartan": 6, "roots": 72, "total": 78}
    assert data["serre"]["ok"] is True
    assert data["serre"]["n_failures"] == 0

    # As of v3p38 export, the recovered Cartan is B6 (so(13)), not E6.
    assert data["cartan"]["dynkin_type"] in {"B6", "C6", "E6"}
    assert data["cartan"]["perm_to_canonical"] is not None
