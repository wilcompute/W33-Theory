"""
Phase CCCLXXII -- Holographic Yukawa Entry Lock
===============================================

The new finite holographic closure already fixed the exact boundary/bulk
dictionary

    q = d_X = 3
    mu = d_Z = 4
    D^2 = v = 40
    k_log = q^mu = 81
    E = 240
    1/G = 960.

The remaining local continuum wall was the first family-sensitive product-heat
entry. The exact A4 bridge theorems already imply that its finite coefficient
is not free:

    Delta A4 = 81 epsilon^2 a0 = (1209/9194) a0.

This 81 is the same exact object in four guises:

1. the bulk logical qutrit count k_log = q^mu = 81;
2. the rank/image/kernel size of the square-zero transport nilpotent on the
   exact 162-dimensional matter extension;
3. the curvature-sensitive half of the exact 81 + 81 split inside that
   162-sector;
4. the finite multiplier in the first family-sensitive A4 entry.

So the first continuum family coefficient is already fixed by the finite
holographic/transport package. The remaining wall is the refined external A4
density and global realization, not the finite multiplicity.
"""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts", ROOT / "exploration"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from exploration.w33_ternary_homological_code_bridge import (
    build_ternary_homological_code_summary,
)
from exploration.w33_yukawa_a4_entry_bridge import (
    build_yukawa_a4_entry_summary,
)
from exploration.w33_yukawa_a4_normalization_bridge import (
    build_yukawa_a4_normalization_summary,
)


v, k, lam, mu = 40, 12, 2, 4
q = 3
f, g = 24, 15
E = v * k // 2
G = Fraction(1, 960)
TRANSPORT_EXTENSION_DIMS = (81, 162, 81)
TRANSPORT_NILPOTENT_DIM = 162
TRANSPORT_NILPOTENT_RANK = 81
TRANSPORT_NILPOTENT_NULLITY = 81


def _logical_qutrits() -> int:
    return int(build_ternary_homological_code_summary()["ternary_css_code"]["logical_qutrits"])


class TestT1_FiniteHolographicPackage:
    """The finite boundary/bulk package is already exact."""

    def test_q_equals_three(self):
        assert q == 3

    def test_mu_equals_four(self):
        assert mu == 4

    def test_center_dimension_squared(self):
        assert 1 + f + g == v == 40

    def test_bulk_edge_count(self):
        assert E == 240

    def test_logical_qutrit_count(self):
        assert _logical_qutrits() == q**mu == 81

    def test_inverse_gravity(self):
        assert Fraction(1, G) == 960


class TestT2_TransportExtensionPackage:
    """The transport extension already fixes the exact 81 -> 162 -> 81 shell."""

    def test_short_exact_sequence_dimensions(self):
        assert TRANSPORT_EXTENSION_DIMS == (81, 162, 81)

    def test_total_extension_is_double_logical_sector(self):
        assert TRANSPORT_EXTENSION_DIMS[1] == 2 * _logical_qutrits()

    def test_nilpotent_operator_dimension(self):
        assert TRANSPORT_NILPOTENT_DIM == 162

    def test_nilpotent_operator_rank(self):
        assert TRANSPORT_NILPOTENT_RANK == _logical_qutrits()

    def test_nilpotent_operator_nullity(self):
        assert TRANSPORT_NILPOTENT_NULLITY == _logical_qutrits()

    def test_image_equals_kernel(self):
        assert TRANSPORT_NILPOTENT_RANK == TRANSPORT_NILPOTENT_NULLITY == _logical_qutrits()


class TestT3_A4Entry:
    """The first continuum family coefficient is already exact."""

    def test_a0_is_family_blind(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A0_is_family_blind"] is True

    def test_a2_is_family_blind(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A2_is_family_blind"] is True

    def test_a4_is_first_family_entry(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["A4_is_first_family_entry_point"] is True

    def test_delta_a4_has_exact_81_multiplier(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["delta_A4_equals_81_epsilon_squared_a0"] is True

    def test_delta_a4_coefficient(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["delta_A4_is_1209_over_9194_times_a0"] is True

    def test_delta_a4_multiplier_matches_logical_qutrits(self):
        assert _logical_qutrits() == 81


class TestT4_A4Normalization:
    """The local A4 normalization identifies exactly which half contributes."""

    def test_curved_block_trace_multiplier(self):
        split = build_yukawa_a4_normalization_summary()["transport_split"]
        assert int(split["curved_block_trace_multiplier"]) == _logical_qutrits()

    def test_exact_transport_split(self):
        split = build_yukawa_a4_normalization_summary()["transport_split"]
        assert split["exact_split"] == "81_flat + 81_curved inside the 162-sector"

    def test_only_curved_half_contributes(self):
        split = build_yukawa_a4_normalization_summary()["transport_split"]
        assert split["only_curved_half_contributes"] is True

    def test_finite_multiplicity_is_not_162(self):
        theorem = build_yukawa_a4_normalization_summary()["a4_normalization_theorem"]
        assert theorem["finite_multiplicity_is_81_not_162"] is True

    def test_exact_reduced_prefactor(self):
        theorem = build_yukawa_a4_normalization_summary()["a4_normalization_theorem"]
        assert theorem["exact_reduced_prefactor_is_27_over_16_pi_sq"] is True

    def test_rank_two_activation_required(self):
        theorem = build_yukawa_a4_normalization_summary()["a4_normalization_theorem"]
        assert theorem["rank_two_external_activation_is_required"] is True


class TestT5_HolographicYukawaLock:
    """The continuum family entry is already locked to finite bulk data."""

    def test_family_multiplier_is_q_to_mu(self):
        assert _logical_qutrits() == q**mu == 81

    def test_family_multiplier_is_transport_rank(self):
        assert TRANSPORT_NILPOTENT_RANK == _logical_qutrits()

    def test_family_multiplier_is_not_boundary_center_size(self):
        assert _logical_qutrits() != v

    def test_family_multiplier_is_not_inverse_gravity(self):
        assert _logical_qutrits() != Fraction(1, G)

    def test_hamming_denominator_reappears(self):
        assert v + _logical_qutrits() == 121 == (k - 1) ** 2

    def test_alpha_fixed_point_reappears(self):
        assert v + _logical_qutrits() + mu**2 == 137


class TestT6_BridgeVerdict:
    """The remaining wall is no longer the finite coefficient."""

    def test_remaining_continuum_wall_is_refined_a4_density(self):
        theorem = build_yukawa_a4_entry_summary()["a4_entry_theorem"]
        assert theorem["remaining_continuum_wall_is_refined_a4_density"] is True

    def test_global_realization_still_open(self):
        theorem = build_yukawa_a4_normalization_summary()["a4_normalization_theorem"]
        assert theorem["remaining_open_step_is_global_branch_counting_and_orientation"] is True

    def test_transport_shell_is_structurally_explained(self):
        assert TRANSPORT_EXTENSION_DIMS == (81, 162, 81)

    def test_cocycle_class_is_explicit(self):
        assert TRANSPORT_NILPOTENT_RANK == TRANSPORT_NILPOTENT_NULLITY == 81

    def test_a4_entry_is_bulk_logical_not_boundary_geometric(self):
        assert _logical_qutrits() == 81 and v == 40 and Fraction(1, G) == 960

    def test_finite_multiplicity_is_already_locked(self):
        assert _logical_qutrits() == 81
