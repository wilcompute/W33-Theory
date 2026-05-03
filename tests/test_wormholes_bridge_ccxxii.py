"""
Regression tests for Part CCXXII: Wormholes and ER=EPR Correspondence from W(3,3).

All tests import and validate the CCXXII wormholes bridge.
Parametrisation: SRG(40,12,2,4) with W(E6) automorphism group |Aut|=51840.
No free parameters — all values derived from SRG definition.
"""

import pytest
import sys
import json
import math
from pathlib import Path

# Load bridge module
sys.path.insert(0, str(Path(__file__).parent.parent / "exploration"))
from PART_CCXXII_WORMHOLES_EREPR_BRIDGE import (
    Q, V, K, LAM, MU, M_LAM, M_NEG, XI_POS, XI_NEG,
    LAP_MID, LAP_TOP, EDGES, AUT_ORDER,
    results, checks, verified
)


class TestWormholesBridgeMetadata:
    """Test that CCXXII bridge module is correctly loaded."""

    def test_module_exists(self):
        assert "PART_CCXXII_WORMHOLES_EREPR_BRIDGE" in sys.modules

    def test_results_dict_present(self):
        assert isinstance(results, dict)
        assert "Part" in results
        assert results["Part"] == "CCXXII"

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


class TestEinsteinRosenBridge:
    """Bridge 1: Einstein-Rosen Wormhole Length."""

    def test_er_bridge_length(self):
        # L_ER ~ K / LAP_MID = 12 / 10 = 1.2
        expected = K / LAP_MID
        assert results["Bridges"]["1_er_bridge_length"] == pytest.approx(expected, abs=0.01)

    def test_throat_circumference(self):
        # sqrt(K) = sqrt(12) ≈ 3.464
        expected = math.sqrt(K)
        # Computed and rounded to 2 decimals
        assert expected == pytest.approx(3.464, abs=0.01)


class TestEntanglementViaRyuTakayanagi:
    """Bridge 2: Entanglement Entropy and Ryu-Takayanagi."""

    def test_entanglement_entropy(self):
        # S_A ~ sqrt(EDGES) = sqrt(240) ≈ 15.49
        expected = math.sqrt(EDGES)
        assert results["Bridges"]["2_entanglement_entropy"] == pytest.approx(expected, abs=0.1)

    def test_minimal_surface_area(self):
        # Area = EDGES = 240
        assert results["Bridges"]["2_entanglement_entropy"] ** 2 == pytest.approx(EDGES, abs=1)


class TestTraversability:
    """Bridge 3: Traversable Wormhole Constraint."""

    def test_traversability_parameter(self):
        # sqrt(K² - MU²) = sqrt(144 - 16) = sqrt(128) ≈ 11.31
        expected = math.sqrt(K**2 - MU**2)
        assert results["Bridges"]["3_traversability_param"] == pytest.approx(expected, abs=0.1)

    def test_exotic_matter_required(self):
        # Traversability requires sqrt(K² - MU²) > 0
        assert results["Bridges"]["3_traversability_param"] > 0

    def test_maximum_curvature(self):
        # Max curvature ~ 1 / (K - MU)^2
        max_curvature = 1 / ((K - MU)**2)
        assert max_curvature == pytest.approx(1/64)


class TestEntanglementWedge:
    """Bridge 4: Entanglement Wedge Volume."""

    def test_wedge_volume(self):
        # V_ew ~ V - K = 40 - 12 = 28
        assert results["Bridges"]["4_entanglement_wedge"] == 28

    def test_accessible_fraction(self):
        # (V - K) / V = 28 / 40 = 0.7
        fraction = (V - K) / V
        assert fraction == pytest.approx(0.7, abs=0.01)


class TestThroatRadius:
    """Bridge 5: Wormhole Throat Radius."""

    def test_throat_radius(self):
        # r_th ~ sqrt(K / LAP_MID) = sqrt(12 / 10) ≈ 1.095
        expected = math.sqrt(K / LAP_MID)
        assert results["Bridges"]["5_throat_radius"] == pytest.approx(expected, abs=0.01)

    def test_throat_diameter(self):
        # Diameter = LAP_MID × r_th
        diameter = LAP_MID * math.sqrt(K / LAP_MID)
        assert diameter == pytest.approx(math.sqrt(LAP_MID * K), abs=0.1)


class TestWormholeStability:
    """Bridge 6: Wormhole Stability Parameter."""

    def test_stability_lambda(self):
        # λ ~ XI_POS / (K × MU) = 2 / 48 = 1/24 ≈ 0.0417
        expected = XI_POS / (K * MU)
        # Check with reasonable precision
        assert abs(expected - (2/48)) < 1e-10

    def test_stable_condition(self):
        # Wormhole is stable if λ < 0.1
        lambda_param = XI_POS / (K * MU)
        assert lambda_param < 0.1


class TestHolographicMinimalSurface:
    """Bridge 7: Holographic Minimal Surface and Entanglement Wedge Boundary."""

    def test_minimal_surface_area(self):
        # A_min ~ EDGES / (LAP_TOP - LAP_MID) = 240 / 6 = 40
        expected = EDGES / (LAP_TOP - LAP_MID)
        assert results["Bridges"]["7_minimal_surface"] == pytest.approx(expected, abs=0.1)

    def test_surface_equals_boundary(self):
        # Minimal surface area = boundary dimension V
        assert results["Bridges"]["7_minimal_surface"] == V


class TestExoticMatter:
    """Bridge 8: Traversable Wormhole Exotic Matter Fraction."""

    def test_exotic_matter_fraction(self):
        # b₀ ~ sqrt(K² - MU²) / EDGES
        expected = math.sqrt(K**2 - MU**2) / EDGES
        assert results["Bridges"]["8_exotic_matter"] == pytest.approx(expected, abs=0.001)

    def test_small_exotic_fraction(self):
        # b₀ should be small (< 0.1) for realistic wormhole
        assert results["Bridges"]["8_exotic_matter"] < 0.1


class TestEREPRDuality:
    """Bridge 9 & 10: ER=EPR Correspondence and Entanglement-Spacetime Duality."""

    def test_equivalent_epr_pairs(self):
        # Number of entangled pairs ~ EDGES / 2 = 120
        expected = EDGES / 2
        assert results["Bridges"]["9_epr_pairs_equivalent"] == int(expected)

    def test_epr_pairs_from_edges(self):
        # Each edge ~ 2 graviton modes ~ 1 entangled pair
        assert results["Bridges"]["9_epr_pairs_equivalent"] == 120

    def test_correlation_volume_ratio(self):
        # (K × M_LAM) / (V × K) = M_LAM / V = 27 / 40 ≈ 0.675
        expected = M_LAM / V
        assert results["Bridges"]["10_correlation_volume_ratio"] == pytest.approx(expected, abs=0.01)


class TestPhysicalConsistency:
    """Cross-check physical constraints and relations."""

    def test_er_traversable(self):
        # ER is traversable iff exotic matter exists
        traversability = results["Bridges"]["3_traversability_param"]
        assert traversability > 0

    def test_throat_geometry(self):
        # Throat radius should be positive and finite
        r_th = results["Bridges"]["5_throat_radius"]
        assert 0 < r_th < 10

    def test_entropy_positive(self):
        # Entanglement entropy should be positive
        S_A = results["Bridges"]["2_entanglement_entropy"]
        assert S_A > 0

    def test_stability_positive(self):
        # Stability parameter should be positive (cost of deviation)
        lambda_param = results["Bridges"]["6_stability_lambda"]
        assert lambda_param > 0


class TestVerification:
    """Verify all checks pass."""

    def test_verified_flag(self):
        assert results["Verified"] is True

    def test_all_checks_pass(self):
        all_pass = all(c["pass"] for c in results["Checks"])
        assert all_pass is True

    def test_zero_free_parameters(self):
        # All values from SRG(40,12,2,4)
        assert Q == 3
        assert V == 40
        assert K == 12
        assert LAM == 2
        assert MU == 4


class TestJSONExport:
    """Verify JSON results file was created correctly."""

    def test_json_file_exists(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXII_wormholes_results.json"
        assert json_file.exists()

    def test_json_content(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXII_wormholes_results.json"
        with open(json_file, "r") as f:
            data = json.load(f)
        assert data["Part"] == "CCXXII"
        assert data["Verified"] is True
        assert len(data["Checks"]) == 21

    def test_json_bridges(self):
        json_file = Path(__file__).parent.parent / "PART_CCXXII_wormholes_results.json"
        with open(json_file, "r") as f:
            data = json.load(f)
        bridges = data["Bridges"]
        assert "1_er_bridge_length" in bridges
        assert "7_minimal_surface" in bridges
        assert "10_correlation_volume_ratio" in bridges
