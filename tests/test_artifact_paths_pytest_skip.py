from __future__ import annotations

import pytest

from exploration._artifact_paths import candidate_repo_roots, resolve_repo_data_path


def test_missing_heavy_artifact_skips_under_pytest(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("W33_DATA_ROOT", raising=False)
    candidate_repo_roots.cache_clear()
    try:
        with pytest.raises(pytest.skip.Exception):
            resolve_repo_data_path(tmp_path, "missing/heavy-artifact.json")
    finally:
        candidate_repo_roots.cache_clear()
