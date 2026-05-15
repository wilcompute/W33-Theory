from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.PART_CCCCCLXXXVII_we6_orbit_phase_shell import build


def test_we6_orbit_sizes_sum_to_e8_root_carrier():
    shell = build()
    assert sum(shell.orbit_sizes) == 240


def test_phase_shell_is_non_e6_complement():
    shell = build()
    assert shell.phase_shell == 168
    assert shell.e6_root_shell + shell.phase_shell == 240


def test_matter_orbits_are_two_81_packages():
    shell = build()
    assert shell.matter_81_plus_shell == 81
    assert shell.matter_81_minus_shell == 81
    assert shell.matter_81_plus_shell + shell.matter_81_minus_shell == 162
    assert shell.matter_orbit_pairing["81_plus"]["orbit_sizes"] == [27, 27, 27]
    assert shell.matter_orbit_pairing["81_minus"]["orbit_sizes"] == [27, 27, 27]


def test_signed_clifford_channels_are_extracted_from_singletons():
    shell = build()
    channels = shell.signed_clifford_channels
    assert len(channels) == 6
    assert all(channel["name"].startswith("chi_") for channel in channels)
    assert all(channel["sign"] in {"+", "-"} for channel in channels)
    assert all(channel["support"] for channel in channels)


def test_local_12_clock_refinement():
    shell = build()
    assert 240 == 20 * 12
    assert shell.e6_root_shell == 6 * 12
    assert shell.phase_shell == 14 * 12
    assert 20 == 6 + 14


def test_we6_orbit_count_pattern():
    shell = build()
    orbit_size_counts = shell.orbit_size_counts
    assert orbit_size_counts["72"] == 1
    assert orbit_size_counts["27"] == 6
    assert orbit_size_counts["1"] == 6
    assert sum(int(size) * count for size, count in orbit_size_counts.items()) == 240


def test_all_checks_hold():
    shell = build()
    assert all(shell.checks.values())