from exploration.w33_toroidal_elkies_theta_heat_bridge import (
    build_summary,
    delta3_series,
    theta_a2_series,
    theta_e6_series,
    theta_k12_series,
)


def test_continuity_bridge_theorem() -> None:
    summary = build_summary()
    assert all(summary["continuity_bridge_theorem"].values())


def test_level3_theta_series_coefficients() -> None:
    assert theta_a2_series(7)[:8] == [1, 6, 0, 6, 6, 0, 0, 12]
    assert delta3_series(6)[:7] == [0, 1, -6, 9, 4, 6, -54]
    assert theta_k12_series(5)[:6] == [1, 0, 756, 4032, 20412, 60480]


def test_theta_e6_first_coefficients() -> None:
    assert theta_e6_series(5)[:6] == [1, 72, 270, 720, 936, 2160]
