"""Regression guard for the finite logic-switch reading of oscillator artifacts."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


ROOT = Path(__file__).resolve().parents[1]


def _load_module(relpath: str, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, ROOT / relpath)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_bt828_control_bank_is_binary_q3_not_ternary_parity_arithmetic() -> None:
    compiler = _load_module("analysis/bt828_holonet_packet_compiler.py", "bt828")

    assert compiler.bits3(0) == (0, 0, 0)
    assert compiler.bits3(7) == (1, 1, 1)
    assert compiler.bits3(8) == compiler.bits3(0)
    assert compiler.bits3(39) == (1, 1, 1)

    row = compiler.compile_digit(0, 7, 0)
    assert row["xor_axes"] == [0, 1, 2]
    assert row["xor_hops"] == 3
    assert row["apartment_hops"] == 1
    assert row["reversible_moves"] == 4


def test_instruction_word_and_state_machine_keep_switch_layers_typed() -> None:
    isa = _load_module("analysis/bt1300_oscillator_instruction_isa.py", "bt1300")
    state_machine = _load_module(
        "analysis/bt1698_holonet_packet_state_machine.py", "bt1698"
    )

    assert [isa.micro_op_for_tick(tick) for tick in range(8)] == [
        "q3_xor_axis_0",
        "q3_xor_axis_1",
        "q3_xor_axis_2",
        "apartment_hop_0",
        "apartment_hop_1",
        "apartment_hop_2",
        "apartment_hop_3",
        "apartment_hop_4",
    ]
    assert state_machine.BODY_OPS == ["LOAD_FLAG", "FLIP_Q6_AXIS", "LATCH_VERTEX"]
    assert state_machine.EPILOGUE_OPS == [
        "ERASE",
        "ROUTE",
        "PHASE",
        "X-CORR",
        "Z-CORR",
        "T-BIT",
        "RESTORE",
        "NEXT",
    ]


def test_public_surfaces_keep_the_switch_boundary_explicit() -> None:
    docs = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    photonic = (ROOT / "photonic_holonet.tex").read_text(encoding="utf-8")
    isa_note = (ROOT / "analysis" / "BT1300_oscillator_instruction_isa.md").read_text(
        encoding="utf-8"
    )
    two_switch = (ROOT / "analysis" / "w33_two_switch_generation.py").read_text(
        encoding="utf-8"
    )
    word_metric = (ROOT / "analysis" / "w33_hardware_compilation.py").read_text(
        encoding="utf-8"
    )
    clock = (ROOT / "analysis" / "w33_machine_clock_is_mass.py").read_text(
        encoding="utf-8"
    )
    clock_payload = json.loads(
        (ROOT / "data" / "w33_machine_clock_is_mass.json").read_text(
            encoding="utf-8"
        )
    )
    toy_pump = (ROOT / "analysis" / "w33_topological_pump_test.py").read_text(
        encoding="utf-8"
    )
    spin_one_pump = (ROOT / "analysis" / "w33_qutrit_topological_pump.py").read_text(
        encoding="utf-8"
    )
    heawood_homology = (
        ROOT / "analysis" / "bt1654_heawood_clock_homology.py"
    ).read_text(encoding="utf-8")

    assert "binary Q<sub>3</sub>-coordinate XOR" in docs
    assert "analogue harmonic oscillator without additional physical modelling" in docs
    assert "three-cube address-toggle bank" in photonic
    assert "established identification of the" in photonic
    assert "all $13$ generating pairs" in photonic
    assert "finite logic-clock interpretation" in isa_note
    assert "hardware_boundary" in two_switch
    assert "No physical-switch, braid, carrier" in two_switch
    assert "hardware_boundary" in word_metric
    assert "optical-switch-depth prediction" in word_metric
    assert "legacy filename retained" in clock
    assert "spectral branch switch" in clock
    assert "m_top_from_clock" not in clock
    assert "order_matches_Sp43" in clock
    assert "Pass 379" in clock
    assert "Pass 380" in clock
    assert "m_top_from_clock" not in clock_payload
    assert "v_EW" not in clock_payload
    assert clock_payload["schema"] == "w33.heawood_logic_switch_clock.v2"
    assert "header_geometry_boundary" in clock_payload["typed_control_pipeline"]
    assert "scheduler_binding_boundary" in clock_payload["typed_control_pipeline"]
    assert "outside the logic-switch ABI" in toy_pump
    assert "gapless at\n``m=0``" in toy_pump
    assert "model calculation only" in spin_one_pump
    assert "band_chern_m0" not in spin_one_pump
    assert "spectral_branch_switch" in heawood_homology
    assert "energy_minus" not in heawood_homology
    assert "energy_plus" not in heawood_homology
