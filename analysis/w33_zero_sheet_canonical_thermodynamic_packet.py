"""Canonical zero-sheet interior/wall thermodynamic packet.

This script promotes the zero-sheet cycle data 4,4,6 into the canonical completed-spectral
interior packet at λ = 4 and the finite wall packet at λ = 6.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from w33.cyclotomic import (  # noqa: E402
    completed_defect_spectral_real_packet,
    completed_defect_spectral_uniform_wall_packet,
)

FUNCTOR_PATH = ROOT / "analysis" / "w33_hamming_horizon_functor_search.py"


def load_hamming_functor_payload() -> dict[str, object]:
    spec = importlib.util.spec_from_file_location("w33_hamming_horizon_functor_search", FUNCTOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {FUNCTOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.build_payload()


def main() -> None:
    functor_payload = load_hamming_functor_payload()
    cycle_lengths = functor_payload["zero_sheet_subgraph"]["simple_cycle_lengths"]
    prime_limits = [10**3, 10**4, 10**5]
    s = 1.0

    interior_rows = [completed_defect_spectral_real_packet(prime_limit, s, deformation=4.0) for prime_limit in prime_limits]
    wall_rows = [completed_defect_spectral_uniform_wall_packet(prime_limit, s) for prime_limit in prime_limits]

    payload = {
        "theorem": "Zero-sheet canonical thermodynamic packet",
        "cycle_lengths": cycle_lengths,
        "interior_scale": 4.0,
        "wall_scale": 6.0,
        "prime_limits": prime_limits,
        "s": s,
        "interior_rows": interior_rows,
        "wall_rows": wall_rows,
        "all_identities_hold": (
            cycle_lengths == [4, 4, 6]
            and all(wall["order_parameter"] > interior["order_parameter"] for interior, wall in zip(interior_rows, wall_rows, strict=True))
            and all(wall["hessian"] > interior["hessian"] for interior, wall in zip(interior_rows, wall_rows, strict=True))
            and all(wall["stiffness"] < interior["stiffness"] for interior, wall in zip(interior_rows, wall_rows, strict=True))
        ),
    }

    data_path = ROOT / "data" / "w33_zero_sheet_canonical_thermodynamic_packet.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "cycle_lengths": cycle_lengths,
        "interior_row": interior_rows[-1],
        "wall_row": wall_rows[-1],
        "all_identities_hold": payload["all_identities_hold"],
    }
    result_path = ROOT / "PART_MCXVI_zero_sheet_canonical_thermodynamic_packet_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXVI Zero-Sheet Canonical Thermodynamic Packet ===")
    print(
        f"cycle_lengths={cycle_lengths}, interior_order={interior_rows[-1]['order_parameter']}, "
        f"wall_order={wall_rows[-1]['order_parameter']}, wall_stiffness={wall_rows[-1]['stiffness']}"
    )


if __name__ == "__main__":
    main()