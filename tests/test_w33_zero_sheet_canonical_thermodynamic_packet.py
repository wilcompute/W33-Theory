from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "analysis" / "w33_zero_sheet_canonical_thermodynamic_packet.py"


def load_module():
    spec = importlib.util.spec_from_file_location("w33_zero_sheet_canonical_thermodynamic_packet", MODULE_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_zero_sheet_canonical_thermodynamic_packet_payload() -> None:
    module = load_module()
    module.main()

    functor_payload = module.load_hamming_functor_payload()
    assert functor_payload["zero_sheet_subgraph"]["simple_cycle_lengths"] == [4, 4, 6]

    cycle_lengths = functor_payload["zero_sheet_subgraph"]["simple_cycle_lengths"]
    assert cycle_lengths == [4, 4, 6]

    interior_rows = [module.completed_defect_spectral_real_packet(prime_limit, 1.0, deformation=4.0) for prime_limit in [10**3, 10**4, 10**5]]
    wall_rows = [module.completed_defect_spectral_uniform_wall_packet(prime_limit, 1.0) for prime_limit in [10**3, 10**4, 10**5]]

    assert all(wall["order_parameter"] > interior["order_parameter"] for interior, wall in zip(interior_rows, wall_rows, strict=True))
    assert all(wall["hessian"] > interior["hessian"] for interior, wall in zip(interior_rows, wall_rows, strict=True))
    assert all(wall["stiffness"] < interior["stiffness"] for interior, wall in zip(interior_rows, wall_rows, strict=True))