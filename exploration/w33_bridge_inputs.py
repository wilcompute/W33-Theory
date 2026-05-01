"""Resolve generated bridge summaries from tracked files or live builders."""

from __future__ import annotations

import json
from importlib import import_module
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

_BUILDERS: dict[str, tuple[str, str]] = {
    "w33_bott_triality_asymmetry_bridge_summary.json": (
        "exploration.w33_bott_triality_asymmetry_bridge",
        "build_summary",
    ),
    "w33_complete_packet_bridge_summary.json": (
        "exploration.w33_complete_packet_bridge",
        "build_summary",
    ),
    "w33_dominant_32_dirac_refinement_bridge_summary.json": (
        "exploration.w33_dominant_32_dirac_refinement_bridge",
        "build_summary",
    ),
    "w33_down_asymmetry_projector_bridge_summary.json": (
        "exploration.w33_down_asymmetry_projector_bridge",
        "build_summary",
    ),
    "w33_l6_v4_closure_selection_bridge_summary.json": (
        "exploration.w33_l6_v4_closure_selection_bridge",
        "build_l6_v4_closure_selection_bridge_summary",
    ),
    "w33_l6_v4_projector_bridge_summary.json": (
        "exploration.w33_l6_v4_projector_bridge",
        "build_l6_v4_projector_bridge_summary",
    ),
    "w33_gamma16_chirality_bridge_summary.json": (
        "exploration.w33_gamma16_chirality_bridge",
        "build_summary",
    ),
    "w33_higgs_ew_octet_bridge_summary.json": (
        "exploration.w33_higgs_ew_octet_bridge",
        "build_summary",
    ),
    "w33_heawood_tetra_radical_bridge_summary.json": (
        "exploration.w33_heawood_tetra_radical_bridge",
        "build_heawood_tetra_radical_summary",
    ),
    "w33_mod12_packet_selector_bridge_summary.json": (
        "exploration.w33_mod12_packet_selector_bridge",
        "build_summary",
    ),
    "w33_mod12_selector_closure_bridge_summary.json": (
        "exploration.w33_mod12_selector_closure_bridge",
        "build_mod12_selector_closure_summary",
    ),
    "w33_affine_nonaffine_common_grammar_bridge_summary.json": (
        "exploration.w33_affine_nonaffine_common_grammar_bridge",
        "build_summary",
    ),
    "w33_quantum_split_operator_bridge_summary.json": (
        "exploration.w33_quantum_split_operator_bridge",
        "build_summary",
    ),
    "w33_spread_overlap_algebra_bridge_summary.json": (
        "exploration.w33_spread_overlap_algebra_bridge",
        "build_summary",
    ),
    "w33_subdominant_octet_bridge_summary.json": (
        "exploration.w33_subdominant_octet_bridge",
        "build_summary",
    ),
    "w33_ternary_heptad_triality_bridge_summary.json": (
        "exploration.w33_ternary_heptad_triality_bridge",
        "build_summary",
    ),
    "w33_toroidal_heptad_projector_bridge_summary.json": (
        "exploration.w33_toroidal_heptad_projector_bridge",
        "build_summary",
    ),
    "w33_toroidal_genus_fourier_bridge_summary.json": (
        "exploration.w33_toroidal_genus_fourier_bridge",
        "build_summary",
    ),
    "w33_affine_e8_sixth_mode_bridge_summary.json": (
        "exploration.w33_affine_e8_sixth_mode_bridge",
        "build_summary",
    ),
    "w33_theta_e8_lattice_summary.json": (
        "exploration.w33_theta_e8_lattice",
        "derive_all",
    ),
    "w33_lfunction_delta_summary.json": (
        "exploration.w33_lfunction_delta",
        "derive_all",
    ),
}


def load_bridge_json(filename: str, data_dir: Path = DATA_DIR) -> dict[str, Any]:
    path = data_dir / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    try:
        module_name, builder_name = _BUILDERS[filename]
    except KeyError as exc:
        raise FileNotFoundError(path) from exc

    module = import_module(module_name)
    builder = getattr(module, builder_name)
    return builder()
