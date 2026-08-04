from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "analysis" / "bt3262_3265_signature_s3_affine_lift.py"
SPEC = spec_from_file_location("bt3262_3265", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_signature_s3_affine_lift_theorem():
    result = MODULE.build_results()
    assert result["local_alphabet_size"] == 16
    assert result["global_signature_count"] == 720
    assert result["character"]["fixed_point_character"] == [16, 2, 1]
    assert result["character"]["irreducible_multiplicities"] == {
        "trivial": 4,
        "sign": 2,
        "standard": 5,
    }
    assert result["character"]["commutant_dimension"] == 45
    assert result["coherent_configuration"]["orbital_count"] == 45
    assert result["four_bit_affine_obstruction"]["s3_subgroup_count"] == 2800
    assert result["four_bit_affine_obstruction"]["affine_four_bit_realization"] is False
    assert result["five_bit_lift"]["minimal_affine_binary_dimension"] == 5
    assert result["five_bit_lift"]["equivariant"] is True
