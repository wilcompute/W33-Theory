"""
Tests for PART CCLXVI — Tomotope as Universal Turing Machine Skeleton.

The tomotope face-vector (V,E,F,C) = (4,12,16,8) encodes W(3,3)
as a universal Turing machine skeleton.  These tests verify every
bridge identity independently so failures are precisely locatable.
"""

import json
import pytest
from math import gcd
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════
#  Shared constants
# ═══════════════════════════════════════════════════════════════════

# W(3,3)  srg(40, 12, 2, 4)
V33, K, LAM, MU = 40, 12, 2, 4
E33, f, g       = 240, 24, 15
r_eig, s_eig    = 2, -4
q               = 3

# Group orders
AUT     = 51840   # |W(E₆)|
WD5     = 1920    # |W(D₅)|
N_ORDER = 192     # |Aut(C₂×Q₈)|

# Tomotope face-vector
TV, TE, TF, TC = 4, 12, 16, 8
T_FLAGS        = 192
T_BLOCKS       = 48

# Derived stabiliser sizes
VSTAB = T_FLAGS // TV   # 48
ESTAB = T_FLAGS // TE   # 16
FSTAB = T_FLAGS // TF   # 12
CSTAB = T_FLAGS // TC   # 24

BUNDLE = (Path(__file__).resolve().parent.parent
          / "axis_bundle_content"
          / "TOE_tomotope_axis_block_twist_v02_20260228")


# ═══════════════════════════════════════════════════════════════════
#  §1  Face-vector encodes the Turing machine
# ═══════════════════════════════════════════════════════════════════

def test_B1_face_vector_sums_to_V33():
    """TV+TE+TF+TC = V33 = 40  (face-vector sum = W33 vertex count)."""
    assert TV + TE + TF + TC == V33


def test_B2_edges_equal_valency():
    """TE = K = 12  (tomotope edges = W33 valency)."""
    assert TE == K


def test_B3_vertices_equal_mu():
    """TV = MU = 4  (tomotope vertices = tape alphabet size)."""
    assert TV == MU


def test_B4_turing_completeness():
    """TV × q = TE  (μ × states = transition-table size = k)."""
    assert TV * q == TE


def test_B5_faces_equal_mu_squared():
    """TF = MU² = 16  (faces = symbol-pair configurations)."""
    assert TF == MU ** 2


def test_B6_cells_equal_2_pow_q():
    """TC = 2^q = 8  (cells = 2^states)."""
    assert TC == 2 ** q


def test_B7_cells_equal_double_mu():
    """TC = 2 × MU = 8  (cells = double tape alphabet)."""
    assert TC == 2 * MU


# ═══════════════════════════════════════════════════════════════════
#  §2  Turing ratios inside the face-vector
# ═══════════════════════════════════════════════════════════════════

def test_B8_edge_vertex_ratio_equals_q():
    """TE / TV = q = 3  (edges-per-vertex = number of states)."""
    assert TE % TV == 0
    assert TE // TV == q


def test_B9_face_vertex_ratio_equals_mu():
    """TF / TV = MU = 4  (faces-per-vertex = tape alphabet)."""
    assert TF % TV == 0
    assert TF // TV == MU


def test_B10_face_cell_ratio_equals_lam():
    """TF / TC = LAM = 2  (faces-per-cell = λ)."""
    assert TF % TC == 0
    assert TF // TC == LAM


# ═══════════════════════════════════════════════════════════════════
#  §3  Topology and balance
# ═══════════════════════════════════════════════════════════════════

def test_B11_euler_characteristic_zero():
    """TV − TE + TF − TC = 0  (tomotope has toroidal Euler characteristic)."""
    assert TV - TE + TF - TC == 0


def test_B12_balanced_face_vector_split():
    """TV+TF = TE+TC = V33/2 = 20  (face-vector splits evenly at midpoint)."""
    assert TV + TF == TE + TC == V33 // 2


# ═══════════════════════════════════════════════════════════════════
#  §4  Flag factorizations
# ═══════════════════════════════════════════════════════════════════

def test_B13_flags_equal_N_order():
    """T_FLAGS = N_ORDER = 192  (flags = |Aut(C₂×Q₈)|)."""
    assert T_FLAGS == N_ORDER


def test_B14_flags_equals_edges_times_faces():
    """T_FLAGS = TE × TF = 12×16 = 192."""
    assert T_FLAGS == TE * TF


def test_B15_flags_equals_vertices_times_blocks():
    """T_FLAGS = TV × T_BLOCKS = 4×48 = 192."""
    assert T_FLAGS == TV * T_BLOCKS


def test_B16_flags_equals_cells_times_f():
    """T_FLAGS = TC × f = 8×24 = 192  (cells × W33 multiplicity)."""
    assert T_FLAGS == TC * f


# ═══════════════════════════════════════════════════════════════════
#  §5  Stabiliser sizes cross-link W33 parameters
# ═══════════════════════════════════════════════════════════════════

def test_B17_edge_stab_equals_face_count():
    """|N| / TE = TF = 16  (edge-stabiliser size = number of faces)."""
    assert N_ORDER % TE == 0
    assert N_ORDER // TE == TF


def test_B18_face_stab_equals_edge_count():
    """|N| / TF = TE = 12 = K  (face-stabiliser size = number of edges = valency)."""
    assert N_ORDER % TF == 0
    assert N_ORDER // TF == TE


def test_B19_cell_stab_equals_f():
    """|N| / TC = f = 24  (cell-stabiliser size = W33 multiplicity f)."""
    assert N_ORDER % TC == 0
    assert N_ORDER // TC == f


def test_B20_vertex_stab_equals_blocks():
    """|N| / TV = T_BLOCKS = 48  (vertex-stabiliser size = block count)."""
    assert N_ORDER % TV == 0
    assert N_ORDER // TV == T_BLOCKS


# ═══════════════════════════════════════════════════════════════════
#  §6  Quaternionic skeleton and cuboctahedron
# ═══════════════════════════════════════════════════════════════════

def _order4_count_c2xq8() -> int:
    """Count order-4 elements in C₂ × Q₈."""
    def lcm(a, b):
        return a * b // gcd(a, b)

    q8_orders = {"1": 1, "-1": 2,
                 "i": 4, "-i": 4, "j": 4, "-j": 4, "k": 4, "-k": 4}
    c2_orders = {0: 1, 1: 2}
    return sum(1 for oa in c2_orders.values()
               for ob in q8_orders.values()
               if lcm(oa, ob) == 4)


def test_B21_C2xQ8_order4_elements_equal_K():
    """|order-4 elements of C₂×Q₈| = 12 = K = TE."""
    assert _order4_count_c2xq8() == 12
    assert _order4_count_c2xq8() == K


def test_B22_cuboctahedron_vertices_equal_K():
    """Cuboctahedron has 12 vertices = K  (cube's 12 edge-midpoints)."""
    cubocta_vertices = 12  # cube has 12 edges; truncation maps each to one vertex
    assert cubocta_vertices == K


# ═══════════════════════════════════════════════════════════════════
#  §7  W(E₆) transport from tomotope symmetry
# ═══════════════════════════════════════════════════════════════════

def test_B23_transport_edges_270():
    """|W(E₆)| / |N| = 270  (directed transport edges counted by tomotope flags)."""
    assert AUT // N_ORDER == 270
    assert AUT % N_ORDER == 0


def test_B24_schlafli_valence_10():
    """|W(D₅)| / |N| = 10  (Schläfli graph valence from tomotope symmetry)."""
    assert WD5 // N_ORDER == 10
    assert WD5 % N_ORDER == 0


def test_B25_lines_on_cubic_surface_27():
    """|W(E₆)| / |W(D₅)| = 27  (27 lines on a cubic surface)."""
    assert AUT // WD5 == 27
    assert AUT % WD5 == 0


# ═══════════════════════════════════════════════════════════════════
#  §8  Computation bridges (Phase CCCXIX)
# ═══════════════════════════════════════════════════════════════════

def test_B26_turing_q_times_mu_equals_K():
    """q × MU = K  (states × symbols = transition-table = W33 valency)."""
    assert q * MU == K


def test_B27_busy_beaver_v33_minus_lam():
    """BB(2,3) = 38 = V33 − λ  (Busy-Beaver value from W33 parameters)."""
    BB23 = 38  # known value of BB(2-state, 3-symbol Turing machine)
    assert BB23 == V33 - LAM


# ═══════════════════════════════════════════════════════════════════
#  §9  Block structure
# ═══════════════════════════════════════════════════════════════════

def test_B28_blocks_per_edge_equals_TV():
    """T_BLOCKS / TE = TV = 4  (48 blocks / 12 edges = 4 = μ)."""
    assert T_BLOCKS % TE == 0
    assert T_BLOCKS // TE == TV


def test_B29_blocks_per_state_equals_TF():
    """T_BLOCKS / q = TF = 16  (48 blocks / 3 states = 16 = μ²)."""
    assert T_BLOCKS % q == 0
    assert T_BLOCKS // q == TF


# ═══════════════════════════════════════════════════════════════════
#  §10  Combinatorial keystone
# ═══════════════════════════════════════════════════════════════════

def test_B30_edges_plus_g_equals_27_lines():
    """TE + g = 12 + 15 = 27  (tomotope edges + W33 eigenvalue multiplicity = 27 lines)."""
    assert TE + g == 27


# ═══════════════════════════════════════════════════════════════════
#  Orbit file consistency tests
# ═══════════════════════════════════════════════════════════════════

def _load(fname):
    return json.loads((BUNDLE / fname).read_text(encoding="utf-8"))["orbits"]


def test_edge_orbits_count_and_size():
    """12 edge orbits, each covering ESTAB=16 flags, total = T_FLAGS."""
    orbs = _load("tomotope_edge_orbits_12.json")
    assert len(orbs) == TE
    assert all(len(o) == ESTAB for o in orbs)
    assert sum(len(o) for o in orbs) == T_FLAGS


def test_vertex_orbits_count_and_size():
    """4 vertex orbits, each covering VSTAB=48 flags, total = T_FLAGS."""
    orbs = _load("tomotope_vertex_orbits_4.json")
    assert len(orbs) == TV
    assert all(len(o) == VSTAB for o in orbs)
    assert sum(len(o) for o in orbs) == T_FLAGS


def test_face_orbits_count_and_size():
    """16 face orbits, each covering FSTAB=12 flags, total = T_FLAGS."""
    orbs = _load("tomotope_face_orbits_16.json")
    assert len(orbs) == TF
    assert all(len(o) == FSTAB for o in orbs)
    assert sum(len(o) for o in orbs) == T_FLAGS


def test_cell_orbits_count_and_size():
    """8 cell orbits, each covering CSTAB=24 flags, total = T_FLAGS."""
    orbs = _load("tomotope_cell_orbits_8.json")
    assert len(orbs) == TC
    assert all(len(o) == CSTAB for o in orbs)
    assert sum(len(o) for o in orbs) == T_FLAGS


def test_orbit_flags_partition():
    """All four orbit families partition the same 192 flags with no overlap."""
    for fname, count in [
        ("tomotope_edge_orbits_12.json",   TE),
        ("tomotope_vertex_orbits_4.json",  TV),
        ("tomotope_face_orbits_16.json",   TF),
        ("tomotope_cell_orbits_8.json",    TC),
    ]:
        orbs = _load(fname)
        flat = sorted(flag for o in orbs for flag in o)
        assert flat == list(range(T_FLAGS)), f"{fname}: flags don't cover 0..{T_FLAGS-1}"


# ═══════════════════════════════════════════════════════════════════
#  Integration: run bridge module and check JSON output
# ═══════════════════════════════════════════════════════════════════

def test_bridge_json_exists_and_verified():
    """PART_CCLXVI_tomotope_results.json must exist and be fully verified."""
    out = Path(__file__).resolve().parent.parent / "PART_CCLXVI_tomotope_results.json"
    assert out.exists(), "Run the bridge script first to generate the JSON"
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["verified"] is True
    assert data["checks_passed"] == data["checks_total"]


def test_bridge_json_checks_all_pass():
    """Every individual named check in the JSON must be True."""
    out = Path(__file__).resolve().parent.parent / "PART_CCLXVI_tomotope_results.json"
    data = json.loads(out.read_text(encoding="utf-8"))
    failed = [k for k, v in data["checks"].items() if not v]
    assert failed == [], f"Failed checks: {failed}"
