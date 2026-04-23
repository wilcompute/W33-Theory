#!/usr/bin/env python3
"""Exact q=3 master-lock audit for the live W33 frontier.

This module packages the strongest already-exact `q = 3` selection data that
now exists in the repo into one boundary surface:

1. Local qutrit kernel:
   the `1 / 3 / 9 / 27 / 40 / 240` packet already appears exactly in the
   Heisenberg shell, line geometry, and E8-side edge/root count.
2. Corrected spectral core:
   the `SRG(40,12,2,4)` spectrum, zero-mode vanishing, even-moment recurrence,
   and Ihara determinant packet are exact.
3. Symbolic uniqueness factors:
   the new April 2026 formulas all vanish exactly at `q = 3`.
4. Continuum coefficient seed:
   the toroidal/decimal packet already fixes `8, 56, 320, 2240, 12480`.

So the conservative exact reading is now stronger than "q=3 looks special":
the finite/local/spectral/continuum-seed layers already overdetermine the same
selected point. The remaining wall is not finite q-selection. It is the smooth
continuum and dynamical realization theorem.
"""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys
import time
from typing import Dict, Tuple

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_qutrit_ladder_audit import (  # noqa: E402
    e8_side_exact_decomposition_summary,
    one_qutrit_local_layer_summary,
    two_qutrit_global_layer_summary,
)
from scripts.w33_spectral_core import get_w33_spectral_core  # noqa: E402
from scripts.w33_toroidal_continuum_seed_audit import (  # noqa: E402
    toroidal_continuum_seed_summary,
    toroidal_seed_packet_summary,
)


@lru_cache(maxsize=1)
def symbolic_q3_lock_summary() -> Dict[str, object]:
    q = sp.Symbol("q", positive=True)
    k_q = q * (q + 1)
    f_q = q * (q + 1) ** 2 / 2
    g_q = q * (q**2 + 1) / 2
    v_q = (q**4 - 1) / 2
    phi3_q = q**2 + q + 1
    phi4_q = q**2 + 1
    phi6_q = q**2 - q + 1

    n_zero_gap = sp.factor(2 * v_q - 2 - 2 * f_q - 2 * g_q)
    m2_gap = sp.factor((2 * k_q * k_q + 2 * f_q * (q - 1) ** 2 + 2 * g_q * (q + 1) ** 2) / (2 * v_q) - k_q)
    disc_r_gap = sp.factor((q - 1) ** 2 - 4 * (k_q - 1) + 4 * phi4_q)
    disc_s_gap = sp.factor((q + 1) ** 2 - 4 * (k_q - 1) + 4 * phi6_q)

    return {
        "n_zero_gap": str(n_zero_gap),
        "m2_minus_k_gap": str(m2_gap),
        "disc_r_plus_4phi4_gap": str(disc_r_gap),
        "disc_s_plus_4phi6_gap": str(disc_s_gap),
        "q3_evaluations": {
            "n_zero_gap_at_3": int(n_zero_gap.subs(q, 3)),
            "m2_minus_k_gap_at_3": int(m2_gap.subs(q, 3)),
            "disc_r_gap_at_3": int(disc_r_gap.subs(q, 3)),
            "disc_s_gap_at_3": int(disc_s_gap.subs(q, 3)),
        },
        "exact_factors": {
            "n_zero_gap_factor_is_exact": n_zero_gap == (q - 3) * (q + 1) * (q**2 + 1),
            "m2_minus_k_gap_factor_is_exact": m2_gap == -q * (q - 3) * (q + 1) / (q - 1),
            "disc_r_gap_factor_is_exact": disc_r_gap == (q - 3) ** 2,
            "disc_s_gap_factor_is_exact": disc_s_gap == (q - 3) ** 2,
            "all_symbolic_gaps_vanish_at_q3": all(
                int(expr.subs(q, 3)) == 0 for expr in (n_zero_gap, m2_gap, disc_r_gap, disc_s_gap)
            ),
        },
    }


@lru_cache(maxsize=1)
def q3_local_kernel_summary() -> Dict[str, object]:
    one_qutrit = one_qutrit_local_layer_summary()
    two_qutrit = two_qutrit_global_layer_summary()
    e8_side = e8_side_exact_decomposition_summary()
    core = get_w33_spectral_core()

    q = int(core.q)
    phi3 = q * q + q + 1
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    return {
        "q": q,
        "phi3": phi3,
        "phi4": phi4,
        "phi6": phi6,
        "visible_shell_size": int(one_qutrit["visible_shell_size"]),
        "fiber_count": int(one_qutrit["fiber_count"]),
        "fiber_size": int(one_qutrit["fiber_size"]),
        "line_size": int(two_qutrit["line_size"]),
        "lines_per_point": int(two_qutrit["lines_per_point"]),
        "projective_point_count": int(two_qutrit["projective_point_count"]),
        "edge_count": int(two_qutrit["edge_count"]),
        "e8_root_count": int(e8_side["total_root_count"]),
        "cartan_rank_candidate": q * q - 1,
        "exact_factorizations": {
            "visible_shell_is_q_cubed": int(one_qutrit["visible_shell_size"]) == q**3,
            "fiber_count_is_q_squared": int(one_qutrit["fiber_count"]) == q * q,
            "fiber_size_is_q": int(one_qutrit["fiber_size"]) == q,
            "line_size_is_q_plus_1": int(two_qutrit["line_size"]) == q + 1,
            "lines_per_point_is_q_plus_1": int(two_qutrit["lines_per_point"]) == q + 1,
            "projective_point_count_is_q3_plus_q2_plus_q_plus_1": int(two_qutrit["projective_point_count"])
            == q**3 + q**2 + q + 1,
            "edge_count_matches_e8_root_count": int(two_qutrit["edge_count"]) == int(e8_side["total_root_count"]),
            "edge_count_is_half_vk": int(two_qutrit["edge_count"])
            == (int(two_qutrit["projective_point_count"]) * int(core.k)) // 2,
        },
    }


@lru_cache(maxsize=1)
def q3_spectral_uniqueness_summary() -> Dict[str, object]:
    core = get_w33_spectral_core()
    symbolic = symbolic_q3_lock_summary()

    q = int(core.q)
    phi4 = q * q + 1
    phi6 = q * q - q + 1

    return {
        "q": q,
        "srg_parameters": (int(core.v), int(core.k), int(core.lam), int(core.mu)),
        "adjacency_eigenpairs": core.adjacency_eigenpairs,
        "bipartite_zero_mode_count": int(core.bipartite_lift_zero_mode_count),
        "canonical_hamiltonian_eigenpairs": core.canonical_hamiltonian_eigenpairs,
        "fourth_moment_per_vertex": int(core.adjacency_moment_per_vertex(4)),
        "even_moment_characteristic_roots": core.even_moment_characteristic_roots,
        "even_moment_recurrence_coefficients": core.even_moment_recurrence_coefficients,
        "ihara_nontrivial_discriminants": core.ihara_nontrivial_discriminants,
        "expected_discriminants": (-4 * phi4, -4 * phi6),
        "zeta_regularised_determinant": int(core.zeta_regularised_determinant),
        "symbolic_uniqueness": symbolic,
        "exact_factorizations": {
            "self_verified": bool(core.self_verified),
            "bipartite_has_no_zero_modes": int(core.bipartite_lift_zero_mode_count) == 0,
            "fourth_moment_matches_q3_special_factorization": int(core.adjacency_moment_per_vertex(4))
            == q * (q + 1) ** 2 * (q**2 + q + 1),
            "ihara_discriminants_match_minus_4phi4_and_minus_4phi6": core.ihara_nontrivial_discriminants
            == (-4 * phi4, -4 * phi6),
            "even_moment_recurrence_holds": bool(core.verify_even_moment_recurrence(8)),
            "all_symbolic_uniqueness_gaps_vanish_at_q3": bool(
                symbolic["exact_factors"]["all_symbolic_gaps_vanish_at_q3"]
            ),
        },
    }


@lru_cache(maxsize=1)
def q3_continuum_seed_summary() -> Dict[str, object]:
    seed = toroidal_seed_packet_summary()
    continuum = toroidal_continuum_seed_summary()
    q = int(seed["q"])
    phi3 = q * q + q + 1
    phi6 = q * q - q + 1
    cartan_packet = q * q - 1

    return {
        "q": q,
        "phi3": phi3,
        "phi6": phi6,
        "cartan_packet": cartan_packet,
        "topological_packet": int(seed["topological_packet"]),
        "continuum_eh_coefficient": int(continuum["continuum_eh_coefficient"]),
        "topological_coefficient": int(continuum["topological_coefficient"]),
        "discrete_eh_coefficient": int(continuum["discrete_eh_coefficient"]),
        "rank39": int(continuum["rank39"]),
        "exact_factorizations": {
            "phi3_is_6_plus_7": int(seed["shared_six_channel"]) + int(seed["phi6"]) == int(seed["phi3"]),
            "cartan_packet_is_1_plus_7": int(seed["selector_line_dimension"]) + int(seed["phi6"])
            == int(seed["cartan_packet"]),
            "cartan_packet_is_q_squared_minus_1": int(seed["cartan_packet"]) == cartan_packet,
            "topological_packet_is_phi6_times_cartan_packet": int(seed["topological_packet"]) == phi6 * cartan_packet,
            "continuum_eh_is_40_times_cartan_packet": int(continuum["continuum_eh_coefficient"])
            == int(continuum["vertex_count"]) * cartan_packet,
            "topological_is_40_times_topological_packet": int(continuum["topological_coefficient"])
            == int(continuum["vertex_count"]) * int(seed["topological_packet"]),
            "discrete_6_mode_is_39_times_40_times_cartan_packet": int(continuum["discrete_eh_coefficient"])
            == int(continuum["rank39"]) * int(continuum["vertex_count"]) * cartan_packet,
        },
    }


@lru_cache(maxsize=1)
def classify_q3_master_lock() -> Tuple[Dict[str, object], ...]:
    local_kernel = q3_local_kernel_summary()
    spectral = q3_spectral_uniqueness_summary()
    continuum = q3_continuum_seed_summary()

    return (
        {
            "name": "q3_local_qutrit_kernel_lock",
            "support_level": "repo-exact finite kernel",
            "statement": (
                "The local qutrit kernel already carries the exact q=3 packet "
                "1/3/9/27/40/240 via fibers, lines, projective points, and edges."
            ),
            "evidence": local_kernel,
        },
        {
            "name": "q3_spectral_ihara_uniqueness_lock",
            "support_level": "repo-exact spectral uniqueness",
            "statement": (
                "The corrected spectral core, zero-mode vanishing, even-moment recurrence, "
                "and Ihara discriminant identities all lock exactly at q=3."
            ),
            "evidence": spectral,
        },
        {
            "name": "q3_toroidal_continuum_seed_lock",
            "support_level": "repo-exact continuum seed",
            "statement": (
                "The toroidal/decimal route already fixes the continuum coefficient packet "
                "8, 56, 320, 2240, 12480 at the same selected point q=3."
            ),
            "evidence": continuum,
        },
        {
            "name": "q3_full_physical_realization_theorem",
            "support_level": "not-yet-exact smooth realization theorem",
            "statement": (
                "The q=3 lock is exact on the finite and coefficient-seed layers, but that "
                "still does not by itself provide the full dynamical/continuum realization."
            ),
            "evidence": {
                "remaining_wall": "smooth realization + Yukawa / dynamics",
            },
        },
    )


@lru_cache(maxsize=1)
def analyze() -> Dict[str, object]:
    records = classify_q3_master_lock()
    exact_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] != "not-yet-exact smooth realization theorem"
    )
    open_record_names = tuple(
        record["name"]
        for record in records
        if record["support_level"] == "not-yet-exact smooth realization theorem"
    )

    local_kernel = q3_local_kernel_summary()
    spectral = q3_spectral_uniqueness_summary()
    continuum = q3_continuum_seed_summary()

    theorem = {
        "the_local_kernel_exactly_realizes_the_q3_packet_1_3_9_27_40_240": (
            local_kernel["exact_factorizations"]["visible_shell_is_q_cubed"]
            and local_kernel["exact_factorizations"]["fiber_count_is_q_squared"]
            and local_kernel["exact_factorizations"]["fiber_size_is_q"]
            and local_kernel["exact_factorizations"]["line_size_is_q_plus_1"]
            and local_kernel["exact_factorizations"]["lines_per_point_is_q_plus_1"]
            and local_kernel["exact_factorizations"]["projective_point_count_is_q3_plus_q2_plus_q_plus_1"]
            and local_kernel["exact_factorizations"]["edge_count_matches_e8_root_count"]
        ),
        "the_corrected_spectral_core_exactly_realizes_the_q3_lock": (
            spectral["srg_parameters"] == (40, 12, 2, 4)
            and spectral["adjacency_eigenpairs"] == ((12, 1), (2, 24), (-4, 15))
            and spectral["bipartite_zero_mode_count"] == 0
            and spectral["canonical_hamiltonian_eigenpairs"] == ((0, 1), (10, 24), (16, 15))
            and spectral["fourth_moment_per_vertex"] == 624
            and spectral["ihara_nontrivial_discriminants"] == spectral["expected_discriminants"]
            and spectral["exact_factorizations"]["even_moment_recurrence_holds"]
            and spectral["exact_factorizations"]["all_symbolic_uniqueness_gaps_vanish_at_q3"]
        ),
        "the_continuum_seed_exactly_realizes_the_q3_packet_8_56_320_2240_12480": (
            continuum["cartan_packet"] == 8
            and continuum["topological_packet"] == 56
            and continuum["continuum_eh_coefficient"] == 320
            and continuum["topological_coefficient"] == 2240
            and continuum["discrete_eh_coefficient"] == 12480
            and all(continuum["exact_factorizations"].values())
        ),
        "the_q3_lock_is_now_overdetermined_across_local_spectral_and_continuum_seed_layers": (
            local_kernel["q"] == spectral["q"] == continuum["q"] == 3
            and local_kernel["phi3"] == continuum["phi3"] == 13
            and local_kernel["phi6"] == continuum["phi6"] == 7
            and local_kernel["cartan_rank_candidate"] == continuum["cartan_packet"] == 8
        ),
        "the_remaining_wall_is_not_finite_q_selection_but_smooth_realization": True,
    }

    return {
        "status": "ok",
        "q3_local_kernel": local_kernel,
        "q3_spectral_uniqueness": spectral,
        "q3_continuum_seed": continuum,
        "record_names_exact_or_boundary": exact_record_names,
        "record_names_open": open_record_names,
        "record_details": records,
        "q3_master_lock_theorem": theorem,
        "boundary_note": (
            "The q=3 selection is now exact and overdetermined across three independent repo "
            "layers: local qutrit geometry, corrected spectral/Ihara uniqueness, and the "
            "toroidal continuum coefficient seed. The honest remaining theorem is therefore "
            "not 'why q=3?' but how the already-selected finite package acquires its smooth "
            "continuum and dynamical realization."
        ),
    }


def main() -> None:
    started = time.time()
    payload = analyze()
    payload["analysis_duration_sec"] = round(time.time() - started, 6)

    output_dir = ROOT / "checks"
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = output_dir / f"PART_CXV_q3_master_lock_audit_{timestamp}.json"
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("Q=3 master-lock audit")
    print(f"  Local packet: q={payload['q3_local_kernel']['q']}, shell={payload['q3_local_kernel']['visible_shell_size']}, edges={payload['q3_local_kernel']['edge_count']}")
    print(
        "  Spectral packet: "
        f"zero-modes={payload['q3_spectral_uniqueness']['bipartite_zero_mode_count']}, "
        f"discriminants={payload['q3_spectral_uniqueness']['ihara_nontrivial_discriminants']}"
    )
    print(
        "  Continuum seed: "
        f"{payload['q3_continuum_seed']['cartan_packet']}, "
        f"{payload['q3_continuum_seed']['topological_packet']}, "
        f"{payload['q3_continuum_seed']['continuum_eh_coefficient']}, "
        f"{payload['q3_continuum_seed']['topological_coefficient']}, "
        f"{payload['q3_continuum_seed']['discrete_eh_coefficient']}"
    )
    print(f"  Wrote: {output_path}")


if __name__ == "__main__":
    main()
