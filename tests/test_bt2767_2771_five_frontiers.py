from __future__ import annotations

import gzip
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def load(name: str):
    p = ROOT / "data" / name
    if p.suffix == ".gz":
        with gzip.open(p, "rt") as f:
            return json.load(f)
    return json.loads(p.read_text(encoding="utf-8"))


def test_m36_rom_exact_and_typed():
    from bt2767_m36_factory import controls_to_ray, expected_ray
    rom = load("PART_BT2767_M36_PREPARATION_ROM.json")
    assert len(rom["rows"]) == 36
    assert rom["grade_census"] == {"deep": 8, "mid": 24, "shallow": 4}
    assert rom["resource_type"] == "M36_Q4_RAW"
    for row in rom["rows"]:
        assert abs(abs(np.vdot(controls_to_ray(row), expected_ray(row))) ** 2 - 1) < 1e-10


def test_metaplectic_sensor_complete():
    s = load("PART_BT2768_SP43_METAPLECTIC_LIFT_SENSOR_summary.json")
    assert s["group_order"] == 51840
    assert s["conjugacy_classes"] == 34
    assert s["geometric_signatures"] == 15
    assert s["geometry_plus_theta1_signatures"] == 30
    assert s["theta1_theta2_signatures"] == 33
    assert s["complete_joint_signatures"] == 34


def test_centralizer_compiler_metrics():
    s = load("PART_BT2769_CX_CENTRALIZER_COMPILER_summary.json")
    assert s["centralizer_order"] == 108
    assert s["right_cosets"] == 480
    assert s["coset_representative_length"]["max"] == 6
    assert s["unweighted_generator_savings"]["positive"] == 50577
    assert abs(s["entangler_count_savings"]["mean"] - 19 / 30) < 1e-12
    assert s["canonical_coset_entangler_counts"] == {"0": 32, "1": 416, "2": 32}


def test_remote_sum_all_branches():
    from bt2771_remote_sum_link import ideal_sum, remote_branch
    rng = np.random.default_rng(77)
    psi = rng.normal(size=(3, 3)) + 1j * rng.normal(size=(3, 3))
    psi /= np.linalg.norm(psi)
    target = ideal_sum(psi)
    for m in range(3):
        for n in range(3):
            branch = remote_branch(psi, m, n)
            assert np.allclose(branch, target / 3)
            assert abs(np.linalg.norm(branch) ** 2 - 1 / 9) < 1e-12


def test_release_firewalls():
    release = load("PART_BT2767_BT2771_FIVE_FRONTIERS_results.json")
    assert release["check_count"] == 18
    assert all(release["checks"].values())
    assert "no M36 distillation" in release["boundaries"]["m36"]
    assert "await remote toolchain" in release["boundaries"]["fpga"]
