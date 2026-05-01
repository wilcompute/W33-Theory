from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    previous = sys.modules.get(name)
    had_previous = name in sys.modules
    try:
        sys.modules[name] = module
        spec.loader.exec_module(module)
    except BaseException:
        if had_previous:
            sys.modules[name] = previous
        else:
            sys.modules.pop(name, None)
        raise
    return module


MODULE = _load_module(
    Path(__file__).resolve().parents[1] / "exploration" / "w33_l4_quark_self_energy.py",
    "w33_l4_quark_self_energy",
)


def test_full27_cubic_screen_is_still_closed() -> None:
    candidate = MODULE.build_l4_quark_self_energy_candidate()
    assert candidate.full27_cubic_slice_screen_rank == 27
    assert candidate.full27_cubic_slice_screen_nullity == 0


def test_contracted_l4_family_counts_are_exact() -> None:
    candidate = MODULE.build_l4_quark_self_energy_candidate()
    assert candidate.total_contracted_operator_count == 54
    assert candidate.clean_operator_count == 42
    assert candidate.nonclean_operator_count == 12
    assert candidate.clean_family_counts == (
        ("antiquark_triplet", 18),
        ("lepton_down", 6),
        ("lepton_up", 6),
        ("quark_triplet", 6),
        ("singlet_higgs", 6),
    )
    assert candidate.nonclean_family_counts == (("quark_triplet", 12),)
    assert candidate.clean_triplet_operator_count == 24
    assert candidate.nonclean_triplet_operator_count == 12


def test_quark_only_clean_subspace_dimensions() -> None:
    candidate = MODULE.build_l4_quark_self_energy_candidate()
    assert candidate.quark_only_subspace_dimension == 4
    assert candidate.q_linked_subspace_dimension == 2
    assert candidate.ud_only_subspace_dimension == 2


def test_explicit_ud_only_counterterm_is_clean_and_localized() -> None:
    candidate = MODULE.build_l4_quark_self_energy_candidate()
    matrix = MODULE.explicit_ud_only_counterterm_27()
    assert MODULE.full_screen_residual_norm_27(matrix) == 0.0
    assert candidate.explicit_ud_only_counterterm_entries == (
        MODULE.CountertermEntry("u_c_2", "u_c_2", 2),
        MODULE.CountertermEntry("u_c_3", "u_c_3", -2),
        MODULE.CountertermEntry("d_c_2", "d_c_2", -2),
        MODULE.CountertermEntry("d_c_3", "d_c_3", 2),
    )
    assert int(np.count_nonzero(np.abs(matrix) > 1e-10)) == 4


def test_explicit_full_quark_counterterm_is_clean_and_localized() -> None:
    candidate = MODULE.build_l4_quark_self_energy_candidate()
    matrix = MODULE.explicit_full_quark_counterterm_27()
    assert MODULE.full_screen_residual_norm_27(matrix) == 0.0
    assert candidate.explicit_full_quark_counterterm_entries == (
        MODULE.CountertermEntry("Q_2_1", "Q_2_1", 2),
        MODULE.CountertermEntry("Q_2_2", "Q_2_2", 2),
        MODULE.CountertermEntry("Q_3_1", "Q_3_1", -2),
        MODULE.CountertermEntry("Q_3_2", "Q_3_2", -2),
        MODULE.CountertermEntry("u_c_2", "u_c_2", -2),
        MODULE.CountertermEntry("u_c_3", "u_c_3", 2),
        MODULE.CountertermEntry("d_c_2", "d_c_2", -2),
        MODULE.CountertermEntry("d_c_3", "d_c_3", 2),
    )
    assert int(np.count_nonzero(np.abs(matrix) > 1e-10)) == 8
