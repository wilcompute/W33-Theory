from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bt3226", ROOT / "analysis/bt3226_3234_port_spiral_closure.py"
)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


@pytest.fixture(scope="module")
def generated():
    return MOD.certificate()


def test_exact_eight_front_certificate(generated):
    data = generated
    assert data["live_chromatic_boundary"] == "10 <= chi(H) <= 11"
    assert data["pass3226_port_sat"]["shards"] == 100
    assert set(data["pass3227_port_terwilliger"]["cell_port_terwilliger_dimension_mod_primes"].values()) == {26}
    near = data["pass3228_near_cover"]
    assert near["commuting_switch_loci"] == 5
    assert near["exact_cover_switch_family_size"] == 243
    assert near["maximum_compatible_replacements"] == {"1":0,"2":0,"3":0,"4":4,"5":4,"6":4}
    assert {x["final_size"] for x in data["pass3229_kempe_vizing"]["deterministic_descent_records"]} == {41}
    assert data["pass3230_oa_voltage"]["local_OA_isotopy_types"] == {"V4":45}
    assert data["pass3230_oa_voltage"]["transport_obstruction"]["matching_triples_per_holonomy"] == 36
    assert data["pass3231_z9_lift"]["frozen_11_color_positive_control"]["valid"]
    assert not data["pass3231_z9_lift"]["single_collision_negative_control"]["valid"]
    assert data["pass3232_physical_port_compiler"]["inverse_from_any_two_ports"]
    assert all(data["pass3233_3234_unit_spiral_phigital"]["checks"].values())


def test_frozen_result_matches_generator(generated):
    frozen = json.loads((ROOT / "data/PART_BT3226_BT3234_PORT_SPIRAL_results.json").read_text())
    assert frozen["sha256_without_hash_field"] == generated["sha256_without_hash_field"]


def test_rom_is_exact_geometry_output(tmp_path):
    out = tmp_path / "rom.mem"
    sha = MOD.emit_rom(out)
    frozen = ROOT / "data/bt3232_port_rom.mem"
    assert out.read_bytes() == frozen.read_bytes()
    assert len(out.read_text().splitlines()) == 720
    assert len(sha) == 64
