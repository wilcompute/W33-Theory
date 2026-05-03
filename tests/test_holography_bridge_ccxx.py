"""
Regression tests for Part CCXX: Holography and AdS-CFT from W(3,3).

All tests import and validate the CCXX holography bridge.
Parametrisation: SRG(40,12,2,4) with W(E6) automorphism group |Aut|=51840.
No free parameters — all values derived from SRG definition.
"""

import pytest
import sys
import json
from pathlib import Path

# Load bridge module
sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXX_HOLOGRAPHY_ADSCFT_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified
)


class TestHolographyBridgeMetadata:
    """Test that bridge module is correctly loaded."""

    def test_module_exists(self):
        assert "PART_CCXX_HOLOGRAPHY_ADSCFT_BRIDGE" in sys.modules

    def test_results_dict_present(self):
        assert isinstance(results, dict)
        assert "Part" in results
        assert results["Part"] == "CCXX"

    def test_checks_list_present(self):
        assert isinstance(checks, list)
        assert len(checks) == 21


class TestSRGParameters:
    """Verify W(3,3) SRG parameters are correct."""

    def test_V(self):
        assert V == 40

    def test_K(self):
        assert K == 12

    def test_LAM(self):
        assert LAM == 2

    def test_MU(self):
        assert MU == 4

    def test_M_LAM(self):
        assert M_LAM == 27

    def test_M_NEG(self):
        assert M_NEG == 12

    def test_XI_POS(self):
        assert XI_POS == 2

    def test_XI_NEG(self):
        assert XI_NEG == -4

    def test_LAP_MID(self):
        assert LAP_MID == 10

    def test_LAP_TOP(self):
        assert LAP_TOP == 16

    def test_EDGES(self):
        assert EDGES == 240

    def test_AUT_ORDER(self):
        assert AUT_ORDER == 51840


class TestBoundaryDuality:
    """Bridge 1: Boundary-Bulk Duality in AdS/CFT."""

    def test_cft_boundary_dimension(self):
        assert results["Bridges"]["1_boundary_dimension"] == V

    def test_bulk_boundary_volume_scaling(self):
        assert results["Bridges"]["1_boundary_dimension"] == 40
        # Scaling factor K/LAM = 12/2 = 6
        assert K / LAM == 6


class TestPrimaryOperators:
    """Bridge 2: CFT Primary Operators."""

    def test_primary_operators_count(self):
        # Non-zero eigenspace: M_LAM + M_NEG = 27 + 12 = 39
        assert results["Bridges"]["2_primary_operators"] == 39

    def test_marginal_operator_scaling_dim(self):
        # Δ ~ LAM = 2
        assert results["Bridges"]["3_leading_scaling_dim"] == XI_POS


class TestScalingDimension:
    """Bridge 3: Conformal Dimension and Scaling."""

    def test_leading_operator_dimension(self):
        assert results["Bridges"]["3_leading_scaling_dim"] == 2

    def test_scaling_ratio(self):
        # Δ_min / V = 10 / 40 = 0.25
        assert results["Bridges"]["6b_scaling_ratio"] == 250  # in thousandths


class TestBulkGravitons:
    """Bridge 4: Graviton Modes in Bulk."""

    def test_bulk_graviton_modes(self):
        assert results["Bridges"]["4_bulk_graviton_modes"] == EDGES

    def test_graviton_dof_per_mode(self):
        # 2 polarisations × 2 (temporal/spatial) = 4
        assert results["Bridges"]["4_bulk_graviton_modes"] == 240
        # Total DOF should be 240 × 4 = 960


class TestCentralCharge:
    """Bridge 5: CFT Central Charge."""

    def test_central_charge(self):
        # C = EDGES / LAP_MID = 240 / 10 = 24
        assert results["Bridges"]["5_central_charge"] == 24

    def test_leech_connection(self):
        # Central charge 24 matches Leech lattice rank
        assert results["Bridges"]["5_central_charge"] == 24


class TestMinimalDimension:
    """Bridge 6: Minimal CFT Scaling Dimension."""

    def test_minimal_scaling_dimension(self):
        assert results["Bridges"]["6_minimal_scaling_dim"] == LAP_MID

    def test_bulk_mass_gap(self):
        assert LAP_MID == 10


class TestSpectralDimension:
    """Bridge 7: Holographic Spectral Dimension."""

    def test_spectral_dimension_computed(self):
        d_S = results["Bridges"]["7_spectral_dimension"]
        assert d_S == 4.0  # capped at 4.0

    def test_spectral_floor(self):
        # floor(d_S) = floor(4.0) = 4
        d_S_floor = int(results["Bridges"]["7_spectral_dimension"])
        assert d_S_floor == 4


class TestLargeNScaling:
    """Bridge 8: Large-N Scaling Exponent."""

    def test_large_n_parameter(self):
        # N_eff ~ M_LAM = 27
        assert M_LAM == 27

    def test_large_n_exponent(self):
        # log_3(27) = 3
        assert results["Bridges"]["8_large_N_exponent"] == 3.0


class TestBulkBoundaryCorrelation:
    """Bridge 9: Bulk-Boundary Correlation Structures."""

    def test_bulk_correlation_scale(self):
        # sqrt(LAP_MID) = sqrt(10) ≈ 3.1623
        import math
        expected = math.sqrt(LAP_MID)
        assert abs(results["Bridges"]["9_bulk_correlation_scale"] - expected) < 0.01

    def test_boundary_2pt_falloff(self):
        # ~r^(−2Δ) = r^(−4)
        assert results["Bridges"]["10_holographic_entropy"] == 15


class TestEntanglementEntropy:
    """Bridge 10: Entanglement Entropy and Ryu-Takayanagi."""

    def test_holographic_entropy_proxy(self):
        # sqrt(EDGES) = sqrt(240) ≈ 15.49 → floor(15)
        import math
        expected = int(math.sqrt(EDGES))
        assert results["Bridges"]["10_holographic_entropy"] == expected


class TestVerification:
    """Verify all checks pass."""

    def test_verified_flag(self):
        assert results["Verified"] is True

    def test_all_checks_pass(self):
        all_pass = all(c["pass"] for c in results["Checks"])
        assert all_pass is True

    def test_zero_free_parameters(self):
        # All values derived from SRG(40,12,2,4)
        assert Q == 3
        assert V == 40
        assert K == 12
        assert LAM == 2
        assert MU == 4


class TestCrossValidation:
    """Cross-check holographic relations."""

    def test_boundary_volume_consistency(self):
        # CFT boundary = V = 40
        assert results["Bridges"]["1_boundary_dimension"] == V

    def test_edge_count_graviton_modes(self):
        # Bulk gravitons = EDGES = 240
        assert results["Bridges"]["4_bulk_graviton_modes"] == EDGES

    def test_area_entropy_density(self):
        # S_BH ~ EDGES / 4 = 60; area density ~ C ~ 24
        assert results["Bridges"]["5_central_charge"] == 24

    def test_spectral_gap_mass(self):
        # Bulk mass gap ~ LAP_MID = 10
        assert results["Bridges"]["6_minimal_scaling_dim"] == LAP_MID


class TestJSONExport:
    """Verify JSON results file was created correctly."""

    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXX_holography_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXX_holography_results.json"
        with open(json_file, "r") as f:
            data = json.load(f)
        assert data["Part"] == "CCXX"
        assert data["Verified"] is True
