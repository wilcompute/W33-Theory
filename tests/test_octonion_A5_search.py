import importlib.util
import json
import os
from pathlib import Path

import pytest

# load the script from the bundle directory (moved during repo reorg)
_bundle_dir = (
    Path("archive/dirs/TOE_line_polarization_A5_v01_20260227_bundle")
    / "TOE_line_polarization_A5_v01_20260227"
)
_bundle_path = _bundle_dir / "recompute_line_polarization_A5.py"
if not _bundle_path.exists():
    pytest.skip("Bundle directory not available (archived)", allow_module_level=True)
spec = importlib.util.spec_from_file_location("recompute_line", _bundle_path)
mod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(mod)
except ModuleNotFoundError as _e:
    pytest.skip(f"Bundle dependency unavailable ({_e})", allow_module_level=True)


def test_find_a5_candidate_small_sample():
    if os.environ.get("RUN_OCTONION_A5_SEARCH") != "1":
        pytest.skip("full octonion A5 subgroup search is opt-in")
    candidates = mod.search_octonion_A5(max_g=200, max_h=200, random_seed=42)
    assert candidates, "expected at least one A5 candidate in small sample"
    cand = candidates[0]
    assert cand["H_size"] == 60
    # verify fingerprint
    assert sorted(cand["orbit"]) == [20] * 6 + [60] * 6


def test_cached_a5_certificate():
    cert = json.loads((_bundle_dir / "stabilizer_A5_generators.json").read_text())
    assert cert["size"] == 60
    assert len(cert["generators"]) == 2
    assert all(len(generator) == 40 for generator in cert["generators"])
    assert "A5" in cert["note"]
