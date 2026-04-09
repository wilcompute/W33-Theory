"""Canonical-selection derivation of the paper CKM asymmetry.

The previous bridges established that the paper packet uses the exact canonical
fractions

    q^2/v,  q/(v-q),  1/(2 Phi_6),  1/q^3.

This module asks the sharper question:

    if we restrict the live two-sheet bridge to those canonical operator-side
    values, does the observed paper asymmetry get selected uniquely?

The answer is yes.  With the Cabibbo leg fixed to ``q^2/v = 9/40`` and quarter-
turn phases on the active complex legs, the unique best canonical assignment is

    Yu = Y11 - i*(q^2/v) Y21 + (q/(v-q)) Y22,
    Yd = Y11 + i*(q^2/v) Y21 + (1/(2 Phi_6)) Y22 - i*(1/q^3) Y32.

So the remaining asymmetry is not a free fit:

    - up real dressing  -> cyclic shell q/(v-q),
    - down real dressing -> inverse G2 scale 1/(2 Phi_6),
    - down complex injector -> universal-mixing scale 1/q^3.

Pushed through the exact U/M/O formulas, the down packet is the conjugate
Cabibbo branch plus one pure ``1/q^3`` outer-shell injector.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_paper_asymmetry_selection_bridge_summary.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from exploration.w33_paper_ckm_asymmetric_bridge import (
    PAPER_TARGETS,
    PDG_2025_TARGETS,
    _build_slot_yukawas,
    _evaluate_packet,
    _squared_error,
)


Q = Fraction(3, 1)
V = Fraction(40, 1)
PHI6 = Fraction(7, 1)

A12 = Q**2 / V
CYCLIC_DRESSING = Q / (V - Q)
G2_DRESSING = Fraction(1, 1) / (2 * PHI6)
GENERATION_INJECTOR = Fraction(1, 1) / (Q**3)


def _to_float(value: Fraction) -> float:
    return float(value)


def _record(slot_yukawas: dict[str, Any], *, u22: Fraction, d22: Fraction, d32: Fraction) -> dict[str, Any]:
    rec = _evaluate_packet(
        slot_yukawas,
        a12=_to_float(A12),
        u22=_to_float(u22),
        u32=0.0,
        d22=_to_float(d22),
        d32=_to_float(d32),
        phase12_over_pi=1.5,
        phase_u32_over_pi=1.5,
        phase_d32_over_pi=1.5,
    )
    rec["canonical_parameters"] = {
        "a12": str(A12),
        "u22": str(u22),
        "u32": "0",
        "d22": str(d22),
        "d32": str(d32),
    }
    rec["paper_squared_error"] = _squared_error(rec, PAPER_TARGETS)
    rec["pdg_squared_error"] = _squared_error(rec, PDG_2025_TARGETS)
    return rec


def _umo_coefficients_for_packet(u22: Fraction, d22: Fraction, d32: Fraction) -> dict[str, dict[str, str]]:
    # exact coefficients in the U/M/O triality basis
    return {
        "up": {
            "fixed": str((Fraction(3, 1) - u22) / 6 + 1j * A12 / 6),
            "middle": str((-2 * u22) / 6 - 1j * A12 / 6),
            "outer": str(-1j * A12 / 2),
        },
        "down": {
            "fixed": str((Fraction(3, 1) - d22) / 6 - 1j * (A12 - d32) / 6),
            "middle": str((-2 * d22) / 6 + 1j * (A12 - d32) / 6),
            "outer": str(1j * (A12 + d32) / 2),
        },
    }


def build_summary() -> dict[str, Any]:
    slot_yukawas = _build_slot_yukawas()
    candidate_real = [CYCLIC_DRESSING, G2_DRESSING]
    candidate_injector = [Fraction(0, 1), GENERATION_INJECTOR]

    records = []
    for u22, d22, d32 in itertools.product(candidate_real, candidate_real, candidate_injector):
        rec = _record(slot_yukawas, u22=u22, d22=d22, d32=d32)
        rec["umo_dictionary"] = _umo_coefficients_for_packet(u22, d22, d32)
        records.append(rec)

    by_paper = sorted(records, key=lambda item: item["paper_squared_error"])
    by_pdg = sorted(records, key=lambda item: item["pdg_squared_error"])
    best_paper = by_paper[0]
    second_paper = by_paper[1]
    best_pdg = by_pdg[0]

    return {
        "canonical_pool": {
            "cabibbo_leg_fixed": str(A12),
            "real_dressing_candidates": [str(CYCLIC_DRESSING), str(G2_DRESSING)],
            "complex_injector_candidates": ["0", str(GENERATION_INJECTOR)],
        },
        "best_to_paper_targets": best_paper,
        "second_best_to_paper_targets": second_paper,
        "best_to_pdg_2025_targets": best_pdg,
        "paper_asymmetry_selection_theorem": {
            "the_unique_best_canonical_assignment_to_paper_targets_is_the_repo_paper_packet": (
                best_paper["canonical_parameters"]
                == {
                    "a12": "9/40",
                    "u22": "3/37",
                    "u32": "0",
                    "d22": "1/14",
                    "d32": "1/27",
                }
            ),
            "the_same_assignment_is_also_best_against_pdg_2025_within_this_canonical_pool": (
                best_pdg["canonical_parameters"]
                == {
                    "a12": "9/40",
                    "u22": "3/37",
                    "u32": "0",
                    "d22": "1/14",
                    "d32": "1/27",
                }
            ),
            "up_sector_prefers_cyclic_shell_over_inverse_g2_dressing": (
                best_paper["canonical_parameters"]["u22"] == "3/37"
            ),
            "down_sector_prefers_inverse_g2_over_cyclic_shell_and_requires_generation_injector": (
                best_paper["canonical_parameters"]["d22"] == "1/14"
                and best_paper["canonical_parameters"]["d32"] == "1/27"
            ),
            "the_down_sector_asymmetry_is_the_conjugate_cabibbo_branch_plus_one_pure_generation_injector": (
                best_paper["umo_dictionary"]["down"]["outer"] == str(1j * (A12 + GENERATION_INJECTOR) / 2)
            ),
        },
        "interpretation": (
            "Within the live two-sheet bridge, the paper asymmetry is selected by a "
            "small canonical pool rather than by unconstrained fitting. The up real "
            "dressing chooses the cyclic shell q/(v-q), the down real dressing "
            "chooses the inverse G2 scale 1/(2Phi_6), and the down complex injector "
            "chooses the universal-mixing scale 1/q^3."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["paper_asymmetry_selection_theorem"], indent=2))


if __name__ == "__main__":
    main()
