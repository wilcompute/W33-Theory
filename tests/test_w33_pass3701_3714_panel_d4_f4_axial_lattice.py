from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "PART_3701_3714_D4_F4_TRIALITY_AXIAL_LATTICE_results.json"
SCRIPT = ROOT / "analysis" / "w33_pass3701_3714_panel_d4_f4_axial_lattice.py"
EXPECTED = "17e8e1caaa48587b8feb5678963358b1a18961efd933858f677ca42e5713c644"


def frozen() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_frozen_certificate_boundary_and_hash() -> None:
    data = frozen()
    assert data["status"] == "PASS_EXACT_SEVEN_FRONT_SOURCE"
    assert data["semantic_sha256"] == EXPECTED
    assert all(data["checks"].values())
    assert data["monster_four_parabolic_front"]["status"] == "MMgroup_WORDS_PENDING"
    assert data["II24_24_polarization"]["explicit_Leech_basis_frozen_here"] is False
    assert data["octad_axial_envelope"]["solutions"] == []


def test_exact_structural_counts() -> None:
    data = frozen()
    tower = data["d4_f4_triality"]
    assert (tower["frames"], tower["octads"], tower["frames_per_octad"]) == (135, 45, 3)
    assert (tower["frame_stabilizer_order"], tower["triality_normalizer_order"], tower["full_outer_stabilizer_order"]) == (192, 576, 1152)
    assert data["axis45_geometry"]["disjointness_srg"] == [45, 12, 3, 3]
    assert data["three_qubit_lagrangian_code"]["dual_weight_enumerator"] == {"0":1,"16":63,"20":63,"36":1}
    assert data["binary_panel_resolution"]["minimum_total_noncommuting_edges"] == 16


def test_recompute_matches_frozen() -> None:
    spec = importlib.util.spec_from_file_location("pass3701_3714", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    generated = module.build()
    assert generated == frozen()
