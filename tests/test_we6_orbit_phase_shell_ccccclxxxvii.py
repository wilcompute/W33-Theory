def test_we6_orbit_sizes_sum_to_e8_root_carrier():
    orbit_sizes = [72] + [27] * 6 + [1] * 6
    assert sum(orbit_sizes) == 240


def test_phase_shell_is_non_e6_complement():
    e6_root_orbit = 72
    matter_orbits = 6 * 27
    singleton_axes = 6
    phase_shell = matter_orbits + singleton_axes
    assert phase_shell == 168
    assert e6_root_orbit + phase_shell == 240


def test_matter_orbits_are_two_81_packages():
    six_27_orbits = 6 * 27
    assert six_27_orbits == 162
    assert six_27_orbits == 81 + 81


def test_local_12_clock_refinement():
    assert 240 == 20 * 12
    assert 72 == 6 * 12
    assert 168 == 14 * 12
    assert 20 == 6 + 14


def test_we6_orbit_count_pattern():
    orbit_size_counts = {72: 1, 27: 6, 1: 6}
    assert orbit_size_counts[72] == 1
    assert orbit_size_counts[27] == 6
    assert orbit_size_counts[1] == 6
    assert sum(size * count for size, count in orbit_size_counts.items()) == 240
