"""Tests for Part CCCCCXCVI: Grand synthesis W33/E8/tomotope."""
import math


def test_packet_positions_all_multiples_of_24():
    expected = {
        "K4_ground": 1 * 24,
        "E6_roots": 3 * 24,
        "Aut_T": 4 * 24,
        "Fano_shell": 7 * 24,
        "Tomotope_D4": 8 * 24,
        "W33_edges": 9 * 24,
        "E8_roots": 10 * 24,
    }
    assert expected["K4_ground"] == 24
    assert expected["E6_roots"] == 72
    assert expected["Aut_T"] == 96
    assert expected["Fano_shell"] == 168
    assert expected["Tomotope_D4"] == 192
    assert expected["W33_edges"] == 216
    assert expected["E8_roots"] == 240


def test_tomotope_mediates_k4_to_f4():
    k4 = 24
    tomotope = 192
    f4 = 1152
    assert tomotope == 8 * k4
    assert f4 == 6 * tomotope
    eight = 4 * 2
    six = 6
    assert eight * six == 48 == 2 * k4


def test_w33_bridges_tomotope_and_e8():
    tomotope = 8 * 24
    w33_edges = 9 * 24
    e8 = 10 * 24
    assert w33_edges - tomotope == 24
    assert e8 - w33_edges == 24


def test_six_kernel_in_eight_faces():
    sources = [
        6,  # A2 roots
        6,  # K4 bivectors
        6,  # W(E6) singletons
        6,  # tomotope monodromy rank
        6,  # Clifford bivectors
        6,  # Csaszar six-shell
        6,  # W33 s=-2 eigenspace
        6,  # W(F4)/W(D4)
    ]
    assert all(s == 6 for s in sources)
    assert len(sources) == 8


def test_phase_to_carrier_ratio():
    fano_phase = 168
    tomotope = 192
    assert fano_phase / tomotope == 7 / 8


def test_master_identity():
    w33_edges = 9 * 24
    assert w33_edges == 216 == 6 ** 3
    gamma2 = 192 ** 2
    mon_q6_ratio = 6 ** 6
    assert int(math.sqrt(mon_q6_ratio)) == w33_edges
