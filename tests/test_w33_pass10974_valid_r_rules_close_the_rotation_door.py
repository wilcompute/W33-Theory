"""Regression for Pass 10974 (numbers established by independent scratch runs before the producer)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
C = json.loads((ROOT / "data" / "w33_pass10974_valid_r_rules_close_the_rotation_door.json").read_text())


def test_established_rules_close_z6ii():
    A = C["A"]["summary"]
    assert A["models"] == 128 and A["parity_exists"] == 1 and A["open"] == 0 and A["closed"] == 1
    z = C["A"]["models"]["Z6-II|Z6II_23__SM_20260917_2913"]
    assert z["fi_cancelling_rays"] == 304 and z["realizable_rays"] == 0


def test_gamma_corrected_g2_plane_keeps_it_closed():
    assert C["B"]["parity_exists"] and C["B"]["realizable_rays"] == 0
    assert C["B"]["verdict"].startswith("closed")


def test_families():
    assert C["C"]["Z2xZ6-I"]["models"] == 29 and C["C"]["Z2xZ6-I"]["open_torus_sg"] == 0
    assert C["C"]["Z2xZ6-I"].get("open_with_uncorrected_R", 0) == 0
    z = C["C"]["Z6xZ6"]
    assert z["models"] == 10 and z["open_torus_sg"] == 0
    assert z["open_with_uncorrected_R"] == 2 and z["of_which_MSSM_viable_none"] == 2
    assert C["C"]["scans"]["z2xz6ii"]["sms"] == 0
    assert C["C"]["Z3xZ6"]["models"] == 5 and C["C"]["Z3xZ6"]["parity_torus_sg"] == 0


def test_z12_reclassified():
    assert C["D"] == {"dead_robust": 5, "undetermined": 9}
