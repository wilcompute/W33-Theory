"""Exact slot-to-triality dictionary for the paper CKM packet.

This bridge turns the tetra-axis map into an explicit basis dictionary on the
four live CKM slots

    Q_1_1, Q_2_1, Q_2_2, Q_3_2.

The exact point is not just that the paper packet lands in the U/M/O triality
carrier. Each canonical slot coefficient has a rigid role there:

    Q_1_1                  seeds only the fixed line,
    Q_2_2                  shifts only the real U/M plane,
    ± i Q_2_1             creates equal-opposite phase drift on U/M plus O,
    - i Q_3_2             creates the same U/M drift with opposite sign and
                          the opposite bare O orientation.

This makes three structural claims exact:

1. The real up/down asymmetry (3/37 versus 1/14) lives entirely in the
   fixed-line/middle-anchor plane and never touches the outer shell.
2. The down-only 1/27 injector is not a generic complex correction: it
   reinforces the outer shell while partially cancelling the Cabibbo phase
   drift on the fixed/middle lock.
3. The paper average isolates the pure generation scale on the outer shell.
"""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DEFAULT_OUTPUT_PATH = DATA_DIR / "w33_slot_triality_dictionary_bridge_summary.json"


ComplexQ = tuple[Fraction, Fraction]


def _c(real: Fraction | int = 0, imag: Fraction | int = 0) -> ComplexQ:
    return (Fraction(real), Fraction(imag))


def _cadd(a: ComplexQ, b: ComplexQ) -> ComplexQ:
    return (a[0] + b[0], a[1] + b[1])


def _cmul_real(a: ComplexQ, scalar: Fraction | int) -> ComplexQ:
    scalar_fraction = Fraction(scalar)
    return (a[0] * scalar_fraction, a[1] * scalar_fraction)


def _cneg(a: ComplexQ) -> ComplexQ:
    return (-a[0], -a[1])


def _serialize_complex(value: ComplexQ) -> dict[str, str]:
    return {"real": str(value[0]), "imag": str(value[1])}


def _serialize_packet(packet: dict[str, ComplexQ]) -> dict[str, dict[str, str]]:
    return {name: _serialize_complex(value) for name, value in packet.items()}


def _slot_triality_dictionary() -> dict[str, dict[str, Fraction]]:
    return {
        "Q_1_1": {
            "fixed_line": Fraction(1, 2),
            "middle_anchor": Fraction(0, 1),
            "outer_shell": Fraction(0, 1),
        },
        "Q_2_1": {
            "fixed_line": Fraction(-1, 6),
            "middle_anchor": Fraction(1, 6),
            "outer_shell": Fraction(1, 2),
        },
        "Q_2_2": {
            "fixed_line": Fraction(-1, 6),
            "middle_anchor": Fraction(-1, 3),
            "outer_shell": Fraction(0, 1),
        },
        "Q_3_2": {
            "fixed_line": Fraction(-1, 6),
            "middle_anchor": Fraction(1, 6),
            "outer_shell": Fraction(-1, 2),
        },
    }


def _apply_slot(
    packet: dict[str, ComplexQ],
    slot_name: str,
    coefficient: ComplexQ,
    slot_dictionary: dict[str, dict[str, Fraction]],
) -> None:
    for component, basis_weight in slot_dictionary[slot_name].items():
        packet[component] = _cadd(packet[component], _cmul_real(coefficient, basis_weight))


def _zero_packet() -> dict[str, ComplexQ]:
    return {
        "fixed_line": _c(),
        "middle_anchor": _c(),
        "outer_shell": _c(),
    }


def _canonical_scalars() -> dict[str, Fraction]:
    return {
        "q": Fraction(3, 1),
        "v": Fraction(40, 1),
        "phi6": Fraction(7, 1),
        "q_cubed": Fraction(27, 1),
        "v_minus_q": Fraction(37, 1),
        "dim_g2": Fraction(14, 1),
        "a12": Fraction(9, 40),
        "u22": Fraction(3, 37),
        "d22": Fraction(1, 14),
        "d32": Fraction(1, 27),
    }


def build_summary() -> dict[str, Any]:
    slot_dictionary = _slot_triality_dictionary()
    counts = _canonical_scalars()

    q11 = _c(1, 0)
    q21_up = _c(0, -counts["a12"])
    q21_down = _c(0, counts["a12"])
    q22_up = _c(counts["u22"], 0)
    q22_down = _c(counts["d22"], 0)
    q32_down = _c(0, -counts["d32"])

    q11_packet = _zero_packet()
    _apply_slot(q11_packet, "Q_1_1", q11, slot_dictionary)

    q21_up_packet = _zero_packet()
    _apply_slot(q21_up_packet, "Q_2_1", q21_up, slot_dictionary)

    q21_down_packet = _zero_packet()
    _apply_slot(q21_down_packet, "Q_2_1", q21_down, slot_dictionary)

    q22_up_packet = _zero_packet()
    _apply_slot(q22_up_packet, "Q_2_2", q22_up, slot_dictionary)

    q22_down_packet = _zero_packet()
    _apply_slot(q22_down_packet, "Q_2_2", q22_down, slot_dictionary)

    q32_down_packet = _zero_packet()
    _apply_slot(q32_down_packet, "Q_3_2", q32_down, slot_dictionary)

    paper_up = _zero_packet()
    for slot_name, coefficient in (
        ("Q_1_1", q11),
        ("Q_2_1", q21_up),
        ("Q_2_2", q22_up),
    ):
        _apply_slot(paper_up, slot_name, coefficient, slot_dictionary)

    paper_down = _zero_packet()
    for slot_name, coefficient in (
        ("Q_1_1", q11),
        ("Q_2_1", q21_down),
        ("Q_2_2", q22_down),
        ("Q_3_2", q32_down),
    ):
        _apply_slot(paper_down, slot_name, coefficient, slot_dictionary)

    paper_average = {
        name: _cmul_real(_cadd(paper_up[name], paper_down[name]), Fraction(1, 2))
        for name in paper_up
    }
    real_asymmetry = {
        name: _cadd(q22_down_packet[name], _cneg(q22_up_packet[name]))
        for name in q22_up_packet
    }
    phase_rebalance = {
        name: _cadd(q21_down_packet[name], q32_down_packet[name])
        for name in q21_down_packet
    }

    return {
        "canonical_counts": {name: str(value) for name, value in counts.items()},
        "slot_triality_dictionary": {
            slot_name: {component: str(weight) for component, weight in components.items()}
            for slot_name, components in slot_dictionary.items()
        },
        "canonical_slot_contributions": {
            "Q_1_1": _serialize_packet(q11_packet),
            "-i*(q^2/v) Q_2_1": _serialize_packet(q21_up_packet),
            "+i*(q^2/v) Q_2_1": _serialize_packet(q21_down_packet),
            "(q/(v-q)) Q_2_2": _serialize_packet(q22_up_packet),
            "(1/(2Phi6)) Q_2_2": _serialize_packet(q22_down_packet),
            "-i*(1/q^3) Q_3_2": _serialize_packet(q32_down_packet),
        },
        "paper_packets": {
            "up": _serialize_packet(paper_up),
            "down": _serialize_packet(paper_down),
            "average": _serialize_packet(paper_average),
        },
        "derived_packets": {
            "real_asymmetry_(down_real_minus_up_real)": _serialize_packet(real_asymmetry),
            "down_phase_rebalance_(+i*q2_over_v*Q21_-_i_over_q3*Q32)": _serialize_packet(phase_rebalance),
        },
        "slot_triality_dictionary_theorem": {
            "q11_seeds_only_the_fixed_line": (
                q11_packet["middle_anchor"] == _c()
                and q11_packet["outer_shell"] == _c()
            ),
            "q22_real_dressings_never_touch_the_outer_shell": (
                q22_up_packet["outer_shell"] == _c()
                and q22_down_packet["outer_shell"] == _c()
                and real_asymmetry["outer_shell"] == _c()
            ),
            "the_real_up_down_asymmetry_lives_entirely_in_the_fixed_middle_plane": (
                real_asymmetry["outer_shell"] == _c()
            ),
            "the_down_only_generation_injector_reinforces_the_outer_shell_while_partially_cancelling_the_q21_phase_drift": (
                phase_rebalance["outer_shell"][1] > q21_down_packet["outer_shell"][1]
                and abs(phase_rebalance["fixed_line"][1]) < abs(q21_down_packet["fixed_line"][1])
                and abs(phase_rebalance["middle_anchor"][1]) < abs(q21_down_packet["middle_anchor"][1])
            ),
            "the_paper_average_outer_shell_is_exactly_i_over_4q_cubed": (
                paper_average["outer_shell"] == _c(0, Fraction(1, 108))
            ),
            "the_exact_paper_up_and_down_triality_packets_are_recovered_from_the_slot_dictionary": (
                paper_up["fixed_line"] == _c(Fraction(18, 37), Fraction(3, 80))
                and paper_up["middle_anchor"] == _c(Fraction(-1, 37), Fraction(-3, 80))
                and paper_up["outer_shell"] == _c(0, Fraction(-9, 80))
                and paper_down["fixed_line"] == _c(Fraction(41, 84), Fraction(-203, 6480))
                and paper_down["middle_anchor"] == _c(Fraction(-1, 42), Fraction(203, 6480))
                and paper_down["outer_shell"] == _c(0, Fraction(283, 2160))
            ),
        },
        "interpretation": (
            "The slot dictionary makes the paper packet structural instead of fitted. "
            "Q_2_2 controls only the real fixed-line/middle-anchor plane, so the "
            "3/37 versus 1/14 asymmetry never touches the outer shell. The down-only "
            "Q_3_2 injector is not a generic extra phase: it adds outer-shell weight "
            "while reducing the Cabibbo-induced phase drift on the fixed/middle lock. "
            "So the paper packet separates cleanly into a real family-anchor "
            "reweighting plus a pure generation-shell rebalance."
        ),
    }


def main() -> None:
    summary = build_summary()
    DEFAULT_OUTPUT_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary["slot_triality_dictionary_theorem"], indent=2))


if __name__ == "__main__":
    main()
