"""Part MCLXIV: Temporal Morita holographic lock for W(3,3).

This packet fuses four already verified finite layers:

* MCLXI  — Lovasz-Hoffman extremal shell      (10, 4)
* MCLXII — Yang-Mills gap-shell envelope      (S_holo=20, mult_gap=24)
* MCLXIII— Temporal self-entangled qutrit     (Bell line + 9 histories)
* CXXVI  — Spread-line Morita bridge          (rank 16, kernels 20 and 24)

The new point is that these are not merely compatible. They lock exactly:

* the temporal Bell line lies in exactly 9 complete spreads = q^2 histories,
* each such spread has 10 contexts of size 4 = theta(G) and theta(Gbar),
* the spread-side kernel dimension is exactly S_holo = 20,
* the line-side killed block is exactly mult(nu_gap) = S_holo / nu_gap = 24,
* the preserved Morita spine has dimension 16 = k - s.

So the temporal carrier, the extremal graph shell, and the YM holographic shell
sit on one exact finite dictionary.
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for candidate in (ROOT, ROOT / "scripts"):
    candidate_str = str(candidate)
    if candidate_str not in sys.path:
        sys.path.insert(0, candidate_str)

from analysis.w33_lovasz_hoffman import (  # noqa: E402
    clique_number,
    fractional_chromatic,
    hoffman_bound,
    lovasz_theta,
    lovasz_theta_complement,
)
from analysis.w33_temporal_self_entangled_qutrit import (  # noqa: E402
    temporal_self_entangled_qutrit_packet,
)
from analysis.w33_ym_deformation_envelope import (  # noqa: E402
    ym_deformation_envelope_packet,
)
from scripts.w33_projective_affine_shell_audit import (  # noqa: E402
    isotropic_lines,
    projective_lines,
    projective_points,
)
from scripts.w33_spread_line_morita_bridge_audit import (  # noqa: E402
    spread_line_morita_bridge_summary,
)
from scripts.w33_symplectic_spread_frame_audit import symplectic_spreads  # noqa: E402


V = 40
K = 12
S = -4
Q = 3


def _bell_line_index_and_spread_count() -> tuple[tuple[int, ...], int]:
    temporal = temporal_self_entangled_qutrit_packet()
    bell_line_points = [tuple(point) for point in temporal["bell_stabilizer_line"]["line_points"]]

    points = projective_points()
    point_index = {tuple(point): index for index, point in enumerate(points)}
    bell_line = tuple(sorted(point_index[point] for point in bell_line_points))

    lines = isotropic_lines(points, projective_lines(points))
    try:
        bell_line_index = lines.index(bell_line)
    except ValueError as exc:  # pragma: no cover - impossible if MCLXIII is valid
        raise AssertionError("temporal Bell line is not a symplectic isotropic line") from exc

    spreads = symplectic_spreads(lines, n_points=len(points))
    spread_count = sum(1 for spread in spreads if bell_line_index in spread)
    return bell_line, spread_count


def temporal_morita_holographic_lock_packet() -> dict[str, object]:
    temporal = temporal_self_entangled_qutrit_packet()
    ym = ym_deformation_envelope_packet()
    morita = spread_line_morita_bridge_summary()

    alpha = hoffman_bound()
    theta_g = lovasz_theta()
    theta_gbar, _, _, _ = lovasz_theta_complement()
    omega = clique_number()
    chi_f = fractional_chromatic()

    bell_line, spreads_through_bell_line = _bell_line_index_and_spread_count()

    spread_size = int(temporal["spread_packet"]["spread_size"])
    context_size = int(temporal["spread_packet"]["context_size"])
    temporal_history_square = int(temporal["temporal_qutrit"]["past_future_basis_pairs"])

    spread_kernel_dim = int(morita["spread_side"]["right_kernel_dimension"])
    line_cokernel_dim = int(morita["line_side"]["left_cokernel_dimension"])
    common_spine_dim = int(morita["morita_bridge"]["common_spine_total_dimension"])

    s_holo = Fraction(ym["gap_shell_lock"]["S_holo"]["numerator"], ym["gap_shell_lock"]["S_holo"]["denominator"])
    nu_gap = Fraction(ym["gap_shell_lock"]["nu_gap"]["numerator"], ym["gap_shell_lock"]["nu_gap"]["denominator"])
    gap_shell_ratio = Fraction(
        ym["gap_shell_lock"]["S_holo_over_nu_gap"]["numerator"],
        ym["gap_shell_lock"]["S_holo_over_nu_gap"]["denominator"],
    )
    gap_multiplicity = int(ym["gap_shell_lock"]["gap_multiplicity"])

    common_spine_formula = K - S
    obstruction_gap = line_cokernel_dim - spread_kernel_dim

    checks = {
        "bell_line_lies_in_q_squared_spreads": spreads_through_bell_line == Q**2 == temporal_history_square,
        "spread_size_equals_theta_and_alpha": spread_size == int(alpha) == int(theta_g) == 10,
        "context_size_equals_theta_bar_omega_chi_f": context_size == int(theta_gbar) == int(omega) == int(chi_f) == 4,
        "spread_kernel_equals_S_holo": spread_kernel_dim == s_holo == 20,
        "line_cokernel_equals_gap_multiplicity": line_cokernel_dim == gap_multiplicity == 24,
        "line_cokernel_equals_S_holo_over_nu_gap": line_cokernel_dim == gap_shell_ratio == 24,
        "common_spine_equals_k_minus_s": common_spine_dim == common_spine_formula == 16,
        "obstruction_gap_equals_context_size": obstruction_gap == context_size == 4,
        "incidence_counts_match_temporal_frame_shell": spreads_through_bell_line * spread_size * context_size == 360,
    }

    packet = {
        "part": "MCLXIV",
        "theorem": "Temporal Morita holographic lock",
        "temporal_shell": {
            "q": Q,
            "bell_line": bell_line,
            "temporal_history_square": temporal_history_square,
            "spreads_through_bell_line": spreads_through_bell_line,
            "spread_size": spread_size,
            "context_size": context_size,
            "identity": "9 Bell-line spreads × 10 contexts × 4 rays = 360 line-spread incidences",
        },
        "extremal_shell": {
            "alpha": str(alpha),
            "theta_G": str(theta_g),
            "theta_Gbar": str(theta_gbar),
            "omega": str(omega),
            "chi_f": str(chi_f),
        },
        "morita_shell": {
            "spread_kernel_dimension": spread_kernel_dim,
            "line_cokernel_dimension": line_cokernel_dim,
            "common_spine_dimension": common_spine_dim,
            "common_spine_formula": "k - s",
            "common_spine_value": common_spine_formula,
            "obstruction_gap": obstruction_gap,
        },
        "holographic_shell": {
            "S_holo": str(s_holo),
            "nu_gap": str(nu_gap),
            "S_holo_over_nu_gap": str(gap_shell_ratio),
            "gap_multiplicity": gap_multiplicity,
        },
        "claim_boundary": (
            "finite exact bridge tying temporal Bell-line spreads, Lovasz-Hoffman extremality, "
            "the spread-line Morita operator, and the normalized-Laplacian holographic shell"
        ),
        "checks": checks,
        "n_verified": sum(1 for value in checks.values() if value),
    }
    return packet


def main() -> None:
    packet = temporal_morita_holographic_lock_packet()
    output_path = ROOT / "PART_MCLXIV_TEMPORAL_MORITA_HOLOGRAPHIC_LOCK_results.json"
    with open(output_path, "w", encoding="utf-8") as handle:
        json.dump(packet, handle, indent=2)

    print("=== Part MCLXIV: Temporal Morita Holographic Lock ===")
    print(
        "bell_spreads={bell}, spread_size={spread}, context_size={context}, "
        "spread_kernel={kernel}, line_cokernel={cokernel}, common_spine={spine}".format(
            bell=packet["temporal_shell"]["spreads_through_bell_line"],
            spread=packet["temporal_shell"]["spread_size"],
            context=packet["temporal_shell"]["context_size"],
            kernel=packet["morita_shell"]["spread_kernel_dimension"],
            cokernel=packet["morita_shell"]["line_cokernel_dimension"],
            spine=packet["morita_shell"]["common_spine_dimension"],
        )
    )
    print(f"verified: {packet['n_verified']} / {len(packet['checks'])}")


if __name__ == "__main__":
    main()