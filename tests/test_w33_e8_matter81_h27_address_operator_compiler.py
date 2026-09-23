from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "analysis/w33_e8_matter81_h27_address_operator_compiler.py"
DATA = ROOT / "data/w33_e8_matter81_h27_address_operator_compiler.json"


def load_script():
    spec = importlib.util.spec_from_file_location("matter81_h27_compiler_test", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_checked_certificate_is_exact_recomputation():
    module = load_script()
    recomputed = module.main(write=False)
    checked = json.loads(DATA.read_text())
    assert recomputed == checked


def test_address_execution_and_qpsi_firewalls_remain_visible():
    checked = json.loads(DATA.read_text())
    assert checked["status"] == (
        "PASS_INCREMENTAL_H27_CLIFFORD_UNIQUENESS_AND_QPSI_COMMUTANT_AUDIT"
    )
    ownership = checked["ownership_and_increment"]
    assert ownership["shared_observables_exactly_replayed"] is True
    assert len(ownership["new_checks"]) == 3
    address = checked["address_space"]
    operator = checked["operator_space"]

    assert address["base_collinearity_srg"] == [27, 10, 1, 5]
    assert address["base_cosets"] == 45
    assert address["lifted_direction_count"] == 10
    assert address["lifted_cosets"] == 270
    assert address["lifted_lines_per_root"] == 10
    assert address["equals_E8_270_cubic_triples"] is True
    assert len(address["root_addresses"]) == 81
    assert address["anchored_incidence_isomorphism_count"] == 1920

    normalizer = address["physical_Clifford648_address_normalizer"]
    assert normalizer["order"] == 648
    assert normalizer["complement_suborbit_sizes"] == [1, 1, 1, 8, 8, 8]
    assert sum(
        record["is_GQ24_SRG"]
        for record in normalizer["three_eight_orbit_census"]
    ) == 1
    assert normalizer["all_648_preserve_45_address_lines"] is True
    assert normalizer["address_line_orbit_sizes"] == [9, 36]
    assert normalizer["phase_labels_held_fixed_instruction_orbit_sizes"] == [
        27,
        27,
        216,
    ]
    assert normalizer["instruction_stabilizer_orders"] == [24, 24, 3]

    assert operator["matter_factorization"] == (
        "C^81 ~= C^9_multiplicity tensor C^3_internal tensor C^3_external"
    )
    assert operator["operator_algebra_dimension"] == 81
    assert operator["commutant_dimension"] == 81
    qpsi = operator["Qpsi_clock_vs_execution_commutant"]
    assert qpsi["commuting_powers_mod12"] == [0, 4, 8]
    assert qpsi["matter_parity_D12_power6_commutes"] is False
    assert qpsi["Kummer_mod4_D12_power3_commutes"] is False

    witness = checked["nonidentification_witness"]
    assert witness["regular_address_H27_center_orbit_size"] == 3
    assert witness["trinification_operator_H27_center_basis_fixed_points"] == 27
    assert witness["equivariant_basis_bijection_exists"] is False

    obstruction = checked["equivariant_compiler_obstruction"]
    assert obstruction["H27_maximum_rank"] == 9
    assert obstruction["H27_target_dimension"] == 27
    assert obstruction["invertible_H27_equivariant_intertwiner_exists"] is False
    assert obstruction["K81_maximum_rank"] == 27
    assert obstruction["K81_target_dimension"] == 81
    assert obstruction["invertible_K81_equivariant_compiler_exists"] is False
    assert "symmetry-changing" in obstruction["surviving_frontier"]

    checks = checked["checks"]
    assert checks["H27_equivariant_coordinate_intertwiner_exists"] is False
    assert checks["full_K_equivariant_compiler_exists"] is False
    assert checks["symmetry_changing_coordinate_dictionary_left_open"] is True
