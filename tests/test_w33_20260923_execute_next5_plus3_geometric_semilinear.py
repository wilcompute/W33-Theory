from __future__ import annotations

import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/"analysis/w33_20260923_execute_next5_plus3_geometric_semilinear.py"
FROZEN=ROOT/"data/w33_20260923_execute_next5_plus3_geometric_semilinear_frozen.json"


def load_module():
    spec=importlib.util.spec_from_file_location("w33_next5_plus3_geometric_semilinear",SCRIPT)
    assert spec and spec.loader
    m=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=m
    spec.loader.exec_module(m)
    return m


def test_weighted_hodge_and_allq_similitude_exact():
    m=load_module()
    a1=m.weighted_spectrum()
    a2=m.full_similitude_theorem()

    assert a1["laplacian_spectra"]["L1"] == {
        "0":81,"3":24,"24/5":15,"96/5":120
    }
    assert a1["laplacian_spectra"]["L2"] == {"96/5":120,"216/5":40}
    assert a1["maxwell_C1_decomposition"]["harmonic_topological_modes"] == 81
    assert a1["maxwell_C1_decomposition"]["coexact_Maxwell_eigenvalue"] == "96/5"

    assert a2["restricted_Hq_character"] == {
        "identity":"q(q-1)",
        "nontrivial_center_z":"-q",
        "noncentral_Heisenberg_element":"0",
        "derivation":"sum all q-1 nontrivial central-character Schrodinger characters once",
    }
    assert a2["cases"]["3"]["minimal_full_carrier_dimension"] == 6
    assert a2["cases"]["9"]["minimal_full_carrier_dimension"] == 72
    assert all(row["full_similitude_commutant_dimension"] == 1 for row in a2["cases"].values())


def test_antilinear_classification_and_FI_minimum():
    m=load_module()
    a3=m.antilinear_classification()
    a4=m.pulse_minimization()

    assert len(a3["canonical_six"]) == 6
    squares=[r["square"] for r in a3["canonical_six"]]
    assert squares[:3] == ["1","1","1"]
    assert set(squares[3:]) == {"1","C^1","C^2"}
    assert [r["order"] for r in a3["canonical_six"][3:]] == [2,6,6]
    assert a3["forbidden_Kramers"].startswith("No member")

    assert a4["unoptimized_identity_test_word"]["F3_or_inverse_traversals"] == 8
    assert a4["exact_gate_synthesis_optimum"]["F3_or_inverse_traversals"] == 0
    assert a4["exact_gate_synthesis_optimum"]["relative_phase_operations"] == 1


def test_frozen_sequential_and_outside_box_boundaries():
    frozen=json.loads(FROZEN.read_text())
    seq=frozen["attack5_sequential_q5_q7_q9"]
    assert seq["q9_geometry"]["identity"].endswith("P^1(F3)")
    sim=seq["simulation"]
    assert sim["q9_adaptive_information_gain"]["mean"] < sim["q9_cyclic"]["mean"]
    assert sim["q9_adaptive_information_gain"]["mean"] < sim["q7"]["mean"]

    extra=frozen["outside_box"]
    assert extra["geometric_n_squared_ladder"]["identity"] == "{24/5,96/5,216/5}=(24/5)*{1^2,2^2,3^2}"
    assert extra["E8_minimal_q3_completion"]["identity"] == "162=81+81=27*6=27*[3*(3-1)]"
    assert extra["Z3_generalized_antilinear_clock"]["orders"] == [6,6]
