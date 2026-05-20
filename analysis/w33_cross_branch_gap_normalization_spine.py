"""Cross-branch gap normalization spine for the GitHub MCXXXIV-MCXL batch.

This script reconciles the executable Yang-Mills spectral floor, the
Navier-Stokes substrate decay gap, and the heat-kernel refinement constants.
The output is a finite substrate identity packet: it does not by itself claim
an external Clay proof.
"""

from __future__ import annotations

import ast
import json
import math
import operator
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analysis.w33_navier_stokes_substrate_flow import DELTA_YM as NS_DELTA  # noqa: E402
from analysis.w33_navier_stokes_substrate_flow import NU as NS_NU  # noqa: E402
from analysis.w33_ym_mass_gap_spectral_floor import (  # noqa: E402
    MASS_GAP_SQUARED,
    substrate_laplacian_spectrum,
)


def _exact(value: Fraction | int) -> dict[str, object]:
    fraction = Fraction(value)
    return {
        "fraction": str(fraction),
        "numerator": fraction.numerator,
        "denominator": fraction.denominator,
        "float": float(fraction),
    }


def _safe_eval(node: ast.AST, env: dict[str, Any]) -> Any:
    binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Pow: operator.pow,
    }
    unary_ops = {
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, str)):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
        return unary_ops[type(node.op)](_safe_eval(node.operand, env))
    if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
        return binary_ops[type(node.op)](_safe_eval(node.left, env), _safe_eval(node.right, env))
    raise ValueError(f"unsupported assignment expression: {ast.dump(node)}")


def _module_assignments(path: Path, names: set[str]) -> dict[str, Any]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    env: dict[str, Any] = {}
    for statement in tree.body:
        if not isinstance(statement, ast.Assign):
            continue
        if not all(isinstance(target, ast.Name) for target in statement.targets):
            continue
        try:
            value = _safe_eval(statement.value, env)
        except Exception:
            continue
        for target in statement.targets:
            assert isinstance(target, ast.Name)
            env[target.id] = value
    return {name: env[name] for name in names}


def cross_branch_gap_normalization_packet() -> dict[str, object]:
    """Return the exact normalization spine connecting the new GitHub branches."""
    heat_names = {
        "q",
        "k",
        "lam",
        "mu",
        "f",
        "g",
        "E",
        "Theta",
        "c_EH",
        "a0",
        "a2",
        "a4",
        "lambda_2",
        "C4",
        "C2",
        "C0",
    }
    heat = _module_assignments(ROOT / "analysis" / "w33_heat_kernel_convergence.py", heat_names)

    local_factor_p2 = Fraction(3, 4)
    ym_p2_floor = substrate_laplacian_spectrum(0, 1, 2)
    exact_global_floor = min(
        substrate_laplacian_spectrum(winding, charge, prime)
        for prime in [2, 3, 5, 7, 11, 23]
        for charge in [1, 2, 3]
        for winding in [0, 1, 2]
    )
    declared_floor = MASS_GAP_SQUARED * local_factor_p2
    ns_delta = Fraction(NS_DELTA)
    ns_decay_rate = Fraction(2, 1) * Fraction(str(NS_NU)) * ns_delta
    vortex_barrier = ns_delta / 2

    q = int(heat["q"])
    mu = int(heat["mu"])
    theta = Fraction(int(heat["Theta"]))
    lambda_2 = Fraction(int(heat["lambda_2"]))
    integer_gap = Fraction(mu + math.factorial(q), 2)
    kolmogorov_magnitude = integer_gap / q
    heat_decay_product = lambda_2 * ns_decay_rate
    heat_floor_amplitudes = {
        "C4_times_floor": Fraction(int(heat["C4"])) * ym_p2_floor,
        "C2_times_floor": Fraction(int(heat["C2"])) * ym_p2_floor,
        "C0_times_floor": Fraction(int(heat["C0"])) * ym_p2_floor,
    }
    eh_ratios = {
        "a0_over_a2": Fraction(int(heat["a0"]), int(heat["a2"])),
        "a4_over_a0": Fraction(int(heat["a4"]), int(heat["a0"])),
        "c_EH_over_theta": Fraction(int(heat["c_EH"]), int(heat["Theta"])),
    }

    return {
        "source_commit_after_fetch": "3c619a82",
        "ym_floor": {
            "mass_gap_squared": _exact(MASS_GAP_SQUARED),
            "p2_local_factor": _exact(local_factor_p2),
            "p2_floor": _exact(ym_p2_floor),
            "global_floor_scan": _exact(exact_global_floor),
            "declared_floor": _exact(declared_floor),
            "formula_aligned": ym_p2_floor == exact_global_floor == declared_floor == Fraction(1, 12),
        },
        "navier_stokes": {
            "delta": _exact(ns_delta),
            "enstrophy_decay_rate_2nu_delta": _exact(ns_decay_rate),
            "vortex_barrier_delta_over_2": _exact(vortex_barrier),
            "delta_matches_ym_floor": ns_delta == ym_p2_floor,
        },
        "heat_kernel": {
            "lambda_2": _exact(lambda_2),
            "theta": _exact(theta),
            "lambda_2_equals_theta": lambda_2 == theta,
            "residual_amplitudes": {name: _exact(Fraction(value)) for name, value in heat_floor_amplitudes.items()},
            "residual_floor_amplitudes_integral": all(value.denominator == 1 for value in heat_floor_amplitudes.values()),
        },
        "cross_branch_spine": {
            "integer_gap": _exact(integer_gap),
            "integer_gap_over_q": _exact(kolmogorov_magnitude),
            "lambda_2_times_ns_decay_rate": _exact(heat_decay_product),
            "lambda2_decay_equals_kolmogorov": heat_decay_product == kolmogorov_magnitude == Fraction(5, 3),
            "ns_delta_half_is_vortex_barrier": vortex_barrier == Fraction(1, 24),
            "ym_floor_to_decay_rate_ratio": _exact(ns_decay_rate / ym_p2_floor),
        },
        "einstein_hilbert_ratios": {name: _exact(value) for name, value in eh_ratios.items()},
        "normalization_spine_detected": (
            ym_p2_floor == ns_delta == Fraction(1, 12)
            and ns_decay_rate == Fraction(1, 6)
            and heat_decay_product == Fraction(5, 3)
            and all(value.denominator == 1 for value in heat_floor_amplitudes.values())
        ),
        "claim_boundary": (
            "finite W33 substrate normalization across the GitHub MCXXXIV-MCXL scripts; "
            "not an external continuum Clay proof by itself"
        ),
    }


def main() -> None:
    packet = cross_branch_gap_normalization_packet()
    payload = {
        "theorem": "Cross-branch gap normalization spine",
        "packet": packet,
    }
    data_path = ROOT / "data" / "w33_cross_branch_gap_normalization_spine.json"
    data_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    result = {
        "theorem": payload["theorem"],
        "source_commit_after_fetch": packet["source_commit_after_fetch"],
        "ym_floor": packet["ym_floor"]["p2_floor"],
        "ns_delta": packet["navier_stokes"]["delta"],
        "ns_decay_rate": packet["navier_stokes"]["enstrophy_decay_rate_2nu_delta"],
        "heat_lambda_2": packet["heat_kernel"]["lambda_2"],
        "lambda_2_times_ns_decay_rate": packet["cross_branch_spine"]["lambda_2_times_ns_decay_rate"],
        "integer_gap_over_q": packet["cross_branch_spine"]["integer_gap_over_q"],
        "normalization_spine_detected": packet["normalization_spine_detected"],
        "claim_boundary": packet["claim_boundary"],
    }
    result_path = ROOT / "PART_MCXLI_cross_branch_gap_normalization_spine_results.json"
    result_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print("=== MCXLI Cross-Branch Gap Normalization Spine ===")
    print(
        f"ym_floor={packet['ym_floor']['p2_floor']['fraction']}, "
        f"ns_decay={packet['navier_stokes']['enstrophy_decay_rate_2nu_delta']['fraction']}, "
        f"lambda2*decay={packet['cross_branch_spine']['lambda_2_times_ns_decay_rate']['fraction']}, "
        f"integer_gap/q={packet['cross_branch_spine']['integer_gap_over_q']['fraction']}"
    )


if __name__ == "__main__":
    main()
