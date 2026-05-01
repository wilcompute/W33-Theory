from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _ensure_signed_we6_action(repo_root: Path) -> None:
    signed_action = repo_root / "artifacts" / "we6_signed_action_on_27.json"
    if signed_action.exists():
        return

    exporter = _load_module(
        repo_root / "tools" / "export_we6_signed_action_on_27.py",
        "export_we6_signed_action_on_27",
    )
    exporter.main()


def test_e6_27rep_minuscule_aligned_and_cubic_invariant():
    repo_root = Path(__file__).resolve().parents[1]
    _ensure_signed_we6_action(repo_root)

    tool = _load_module(
        repo_root / "tools" / "build_e6_27rep_minuscule.py", "build_e6_27rep_minuscule"
    )

    tool.main([])

    out_path = repo_root / "artifacts" / "e6_27rep_minuscule.json"
    data = json.loads(out_path.read_text(encoding="utf-8"))
    assert data["status"] == "ok"
    assert data["weights"]["count"] == 27
    assert data["serre"]["ok"] is True
    assert data["serre"]["n_failures"] == 0
    assert data["weyl"]["match_ok"] is True
    assert data["cubic"]["ok"] is True
    assert data["cubic"]["max_abs_coeff"] == 0.0
