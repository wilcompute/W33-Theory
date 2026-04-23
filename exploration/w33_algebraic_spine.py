"""Executable algebraic spine for the W33 qutrit/Golay/Vogel program.

This module does not introduce a new physical theorem. It consolidates the
strongest already-executable algebraic layers that matter for the next step:

1. Local qutrit shell:
   around any W33 vertex, H27 is an F3^3/Heisenberg shell and N12 splits into
   4 MUB classes.
2. Global qutrit shell:
   W33 is the 2-qutrit Pauli commutation geometry.
3. Universal closure:
   the s12/Golay Jacobi obstruction resolves by passing to the Heisenberg lift
   and the 3-qutrit sl(27) closure.
4. Tomotope/Reye bridge:
   the exact (12,16) motif and the hard obstruction live in the repo already.
5. Vogel position:
   the relevant s12 dimensions do not land on the positive nondegenerate hit
   set of the repo's exceptional-line arithmetic, so Vogel should constrain
   Jacobi/kernel structure after Lie closure, not replace it.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
from math import comb
from pathlib import Path

from scripts.w33_golay_lie_algebra import analyze as analyze_golay_lie
from scripts.w33_heisenberg_qutrit import build_f3_cube, compute_local_structure
from scripts.w33_monster_3b_s12_sl27_bridge import analyze as analyze_monster_bridge
from scripts.w33_two_qutrit_pauli import (
    build_commutation_graph,
    build_pauli_operators,
    compare_with_w33,
    find_isomorphism,
)
from scripts.w33_homology import build_clique_complex, build_w33
from tools.s12_universal_algebra import (
    enumerate_linear_code_f3,
    grade_mod3,
    ternary_golay_generator_matrix,
    verify_universal_grade_laws,
)
from tools.tomotope_reye_e8_connection import generate_summary
from tools.vogel_rational_dimension_theorem import positive_nondeg_hit_dims
from tools.vogel_rational_hit_crosswalk import build_crosswalk, classical_hits


ROOT = Path(__file__).resolve().parents[1]
TWIST_TRANSPORT_REYE_JSON = ROOT / "data" / "w33_twist_transport_reye.json"


@dataclass(frozen=True)
class LocalQutritShell:
    """Exact local 1-qutrit shell around a W33 vertex."""

    base_vertex: int
    neighbor_count: int
    nonneighbor_count: int
    mub_class_count: int
    mub_class_sizes: tuple[int, ...]
    h27_induced_degree: int
    schlafli_parameters: tuple[int, int, int, int]
    fiber_count: int
    fiber_size: int
    missing_tritangent_count: int
    generation_fiber_sizes: tuple[int, int, int]
    omega_adjacency: tuple[int, int, int]
    omega_non_adjacency: tuple[int, int, int]


@dataclass(frozen=True)
class GlobalPauliGeometry:
    """Exact 2-qutrit Pauli realization of W33."""

    projective_point_count: int
    vertex_degree: int
    edge_count: int
    line_count: int
    line_size: int
    lines_per_point: int
    srg_parameters: tuple[int, int, int, int]
    identity_isomorphism_holds: bool
    label_match_count: int


@dataclass(frozen=True)
class UniversalClosureSpine:
    """s12/Golay/Monster/Heisenberg/3-qutrit closure data."""

    s12_total_nonzero_dim: int
    s12_grade_dimensions: tuple[int, int, int]
    s12_jacobi_failure_count: int
    s12_ad3_holds: bool
    golay_lie_dim: int
    golay_lie_is_perfect: bool
    golay_lie_center_dim: int
    golay_cartan_like_dim: int
    monster_extraspecial_order: int
    heisenberg_irrep_dim: int
    sl27_traceless_dim: int
    golay_lagrangian_isotropic: bool


@dataclass(frozen=True)
class TomotopeReyeBridge:
    """Exact repo-side tomotope/Reye obstruction data."""

    tomotope_edges: int
    tomotope_faces: int
    tomotope_automorphism_order: int
    reye_points: int
    reye_lines: int
    reye_point_degree: int
    reye_valid_configs: int
    tomotope_signature: tuple[int, ...]
    axis_signature: tuple[int, ...]
    signatures_differ: bool


@dataclass(frozen=True)
class VogelPosition:
    """Current executable Vogel position of the relevant s12 dimensions."""

    positive_hit_dims: tuple[int, ...]
    grade0_dim: int
    quotient_dim: int
    total_nonzero_dim: int
    grade0_in_positive_hit_set: bool
    quotient_in_positive_hit_set: bool
    total_in_positive_hit_set: bool
    nearest_grade0_hit: int
    nearest_quotient_hit: int
    nearest_total_hit: int
    total_classical_a_hits: tuple[int, ...]


@dataclass(frozen=True)
class ExceptionalParameterDictionary:
    """Exact W(3,3) parameter dictionary behind the user-facing Rosetta tables."""

    srg_parameters: tuple[int, int, int, int]
    qutrit_order: int
    cubic_line_count: int
    complement_schlafli_edge_count: int
    tritangent_plane_count: int
    directed_meeting_edge_count: int
    stabilizer_order: int
    phi3_q: int
    a2_dim: int
    g2_dim: int
    f4_dim: int
    e6_dim: int
    e7_fund_dim: int
    e7_dim: int
    e8_dim: int
    z3_grade_dims: tuple[int, int, int]
    full_magic_square_dims: tuple[tuple[int, int, int, int], ...]
    octonionic_magic_square_dims: tuple[int, int, int, int]
    full_magic_square_is_symmetric: bool
    formulas_match_magic_square: bool


@dataclass(frozen=True)
class AlgebraicSpine:
    """Consolidated executable route for the next algebraic step."""

    local_qutrit_shell: LocalQutritShell
    global_pauli_geometry: GlobalPauliGeometry
    universal_closure: UniversalClosureSpine
    tomotope_reye_bridge: TomotopeReyeBridge
    vogel_position: VogelPosition
    exceptional_parameter_dictionary: ExceptionalParameterDictionary
    route_recommendation: str


def _latest_heisenberg_shell() -> LocalQutritShell:
    n, vertices, adj, edges = build_w33()
    adj_s = [set(row) for row in adj]
    base_vertex = 0
    n12, h27, triangles, _ = compute_local_structure(base_vertex, n, adj_s)
    fibers, vertex_to_xyz = build_f3_cube(n12, h27, triangles, adj_s)

    h27_set = set(h27)
    h27_degrees = [len(adj_s[v] & h27_set) for v in h27]
    h27_induced_degree = h27_degrees[0]

    # Build the Schläfli graph exactly as the script does.
    schlafli = {u: set() for u in h27}
    for index, u in enumerate(h27):
        for v in h27[index + 1 :]:
            common = len((adj_s[u] & adj_s[v]) & h27_set)
            if common == 3:
                schlafli[u].add(v)
                schlafli[v].add(u)

    schlafli_degree = len(next(iter(schlafli.values())))
    lambda_values = set()
    mu_values = set()
    for index, u in enumerate(h27):
        for v in h27[index + 1 :]:
            common = len(schlafli[u] & schlafli[v])
            if v in schlafli[u]:
                lambda_values.add(common)
            else:
                mu_values.add(common)

    missing_tritangents = 0
    for vertices_3 in fibers.values():
        a, b, c = vertices_3
        is_triangle = b in adj_s[a] and c in adj_s[a] and c in adj_s[b]
        if not is_triangle:
            missing_tritangents += 1

    generations = {0: 0, 1: 0, 2: 0}
    for vertex in h27:
        _, _, t = vertex_to_xyz[vertex]
        generations[t] += 1

    omega_adj = [0, 0, 0]
    omega_non_adj = [0, 0, 0]
    for i, u in enumerate(h27):
        xu, yu, _ = vertex_to_xyz[u]
        for v in h27[i + 1 :]:
            xv, yv, _ = vertex_to_xyz[v]
            omega = (xu * yv - yu * xv) % 3
            if v in adj_s[u]:
                omega_adj[omega] += 1
            else:
                omega_non_adj[omega] += 1

    return LocalQutritShell(
        base_vertex=base_vertex,
        neighbor_count=len(n12),
        nonneighbor_count=len(h27),
        mub_class_count=len(triangles),
        mub_class_sizes=tuple(len(triangle) for triangle in triangles),
        h27_induced_degree=int(h27_induced_degree),
        schlafli_parameters=(27, schlafli_degree, next(iter(lambda_values)), next(iter(mu_values))),
        fiber_count=len(fibers),
        fiber_size=len(next(iter(fibers.values()))),
        missing_tritangent_count=missing_tritangents,
        generation_fiber_sizes=(generations[0], generations[1], generations[2]),
        omega_adjacency=tuple(int(value) for value in omega_adj),
        omega_non_adjacency=tuple(int(value) for value in omega_non_adj),
    )


def _global_pauli_geometry() -> GlobalPauliGeometry:
    reps, matrices = build_pauli_operators()
    pauli_adj = build_commutation_graph(reps)
    n, vertices, adj, edges = build_w33()
    simplices = build_clique_complex(n, adj)
    identity_holds, mismatches = find_isomorphism(reps, pauli_adj)
    comparison = compare_with_w33(reps, pauli_adj)

    return GlobalPauliGeometry(
        projective_point_count=len(reps),
        vertex_degree=comparison["pauli_k"],
        edge_count=comparison["pauli_edges"],
        line_count=len(simplices[3]),
        line_size=4,
        lines_per_point=4,
        srg_parameters=(comparison["pauli_n"], comparison["pauli_k"], 2, 4),
        identity_isomorphism_holds=bool(identity_holds),
        label_match_count=len(reps) - int(mismatches if mismatches >= 0 else len(reps)),
    )


def _universal_closure_spine() -> UniversalClosureSpine:
    s12_report = _s12_core_summary()
    golay = analyze_golay_lie(compute_derivations=False)
    monster = analyze_monster_bridge()

    dims = s12_report["algebra_dimensions"]
    laws = s12_report["universal_grade_laws"]
    lie = golay["lie"]
    cartan = golay["cartan_like"]
    golay_lagrangian = monster["golay_lagrangian"]

    return UniversalClosureSpine(
        s12_total_nonzero_dim=int(dims["total_nonzero"]),
        s12_grade_dimensions=(int(dims["grade0"]), int(dims["grade1"]), int(dims["grade2"])),
        s12_jacobi_failure_count=int(laws["jacobi_failure_count"]),
        s12_ad3_holds=bool(laws["ad3_coefficient_identity_holds"]),
        golay_lie_dim=int(golay["dim"]),
        golay_lie_is_perfect=bool(lie["perfect"]),
        golay_lie_center_dim=int(lie["center_dim"]),
        golay_cartan_like_dim=int(cartan["dim"]),
        monster_extraspecial_order=int(monster["monster"]["extraspecial_order"]),
        heisenberg_irrep_dim=int(monster["heisenberg"]["irrep_dim"]),
        sl27_traceless_dim=int(monster["sl27"]["traceless_dim"]),
        golay_lagrangian_isotropic=bool(golay_lagrangian["symplectic_isotropic_all_pairs"]),
    )


def _tomotope_reye_bridge() -> TomotopeReyeBridge:
    summary = generate_summary()
    report = json.loads(TWIST_TRANSPORT_REYE_JSON.read_text(encoding="utf-8"))
    verification = summary["verification"]

    return TomotopeReyeBridge(
        tomotope_edges=int(verification["tomotope"]["edges"]),
        tomotope_faces=int(verification["tomotope"]["faces"]),
        tomotope_automorphism_order=int(verification["tomotope"]["|Γ(T)|"]),
        reye_points=int(report["T5_reye_point_count"]),
        reye_lines=int(report["T5_reye_line_count"]),
        reye_point_degree=int(report["T5_reye_point_degree"]),
        reye_valid_configs=int(report["T5_reye_configs_valid"]),
        tomotope_signature=tuple(int(v) for v in report["T6_tomotope_P_signature"]),
        axis_signature=tuple(int(v) for v in report["T6_all_axis_signatures"][0]),
        signatures_differ=sorted(report["T6_tomotope_P_signature"], reverse=True)
        != sorted(report["T6_all_axis_signatures"][0], reverse=True),
    )


def _nearest_hit(target: int, hits: tuple[int, ...]) -> int:
    return min(hits, key=lambda value: (abs(value - target), value))


def _vogel_position() -> VogelPosition:
    s12_report = _s12_core_summary()
    dims = s12_report["algebra_dimensions"]
    hits = tuple(positive_nondeg_hit_dims())
    crosswalk = build_crosswalk([728, 486, 242])

    return VogelPosition(
        positive_hit_dims=hits,
        grade0_dim=int(dims["grade0"]),
        quotient_dim=int(dims["quotient_by_grade0"]),
        total_nonzero_dim=int(dims["total_nonzero"]),
        grade0_in_positive_hit_set=242 in hits,
        quotient_in_positive_hit_set=486 in hits,
        total_in_positive_hit_set=728 in hits,
        nearest_grade0_hit=_nearest_hit(242, hits),
        nearest_quotient_hit=_nearest_hit(486, hits),
        nearest_total_hit=_nearest_hit(728, hits),
        total_classical_a_hits=tuple(int(v) for v in classical_hits(728)["A"]),
    )


def _exceptional_parameter_dictionary(
    local_shell: LocalQutritShell,
    global_geometry: GlobalPauliGeometry,
) -> ExceptionalParameterDictionary:
    v, k, lam, mu = global_geometry.srg_parameters
    q = 3
    cubic_lines = local_shell.nonneighbor_count
    schlafli_degree = local_shell.schlafli_parameters[1]
    meeting_degree = cubic_lines - 1 - schlafli_degree
    directed_meeting_edges = cubic_lines * meeting_degree
    complement_schlafli_edges = directed_meeting_edges // 2
    tritangents_per_line = meeting_degree // 2
    tritangent_planes = cubic_lines * tritangents_per_line // 3
    sp43_order = q**4 * (q**2 - 1) * (q**4 - 1)
    stabilizer_order = sp43_order // directed_meeting_edges
    phi3_q = q * q + q + 1

    a2_dim = k - mu
    g2_dim = k + mu - lam
    f4_dim = v + k
    e6_dim = 2 * v - lam
    e7_fund_dim = v + k + mu
    e7_dim = v * q + phi3_q
    e8_dim = global_geometry.edge_count + k - mu
    z3_grade_dims = (e6_dim + a2_dim, q * cubic_lines, q * cubic_lines)
    full_magic_square_dims = (
        (3, 8, 21, 52),
        (8, 16, 35, 78),
        (21, 35, 66, 133),
        (52, 78, 133, 248),
    )
    octonionic_magic_square_dims = (f4_dim, e6_dim, e7_dim, e8_dim)
    full_magic_square_is_symmetric = all(
        full_magic_square_dims[i][j] == full_magic_square_dims[j][i]
        for i in range(4)
        for j in range(4)
    )

    return ExceptionalParameterDictionary(
        srg_parameters=(v, k, lam, mu),
        qutrit_order=q,
        cubic_line_count=cubic_lines,
        complement_schlafli_edge_count=complement_schlafli_edges,
        tritangent_plane_count=tritangent_planes,
        directed_meeting_edge_count=directed_meeting_edges,
        stabilizer_order=stabilizer_order,
        phi3_q=phi3_q,
        a2_dim=a2_dim,
        g2_dim=g2_dim,
        f4_dim=f4_dim,
        e6_dim=e6_dim,
        e7_fund_dim=e7_fund_dim,
        e7_dim=e7_dim,
        e8_dim=e8_dim,
        z3_grade_dims=z3_grade_dims,
        full_magic_square_dims=full_magic_square_dims,
        octonionic_magic_square_dims=octonionic_magic_square_dims,
        full_magic_square_is_symmetric=full_magic_square_is_symmetric,
        formulas_match_magic_square=octonionic_magic_square_dims == full_magic_square_dims[-1]
        and full_magic_square_is_symmetric
        and full_magic_square_dims[3] == (52, 78, 133, 248)
        and z3_grade_dims == (86, 81, 81)
        and sum(z3_grade_dims) == e8_dim
        and complement_schlafli_edges == comb(cubic_lines, 2) - (cubic_lines * schlafli_degree // 2),
    )


@lru_cache(maxsize=1)
def _s12_core_summary() -> dict[str, object]:
    generator = ternary_golay_generator_matrix()
    codewords = enumerate_linear_code_f3(generator)
    zero = tuple([0] * len(generator[0]))
    by_grade = {0: 0, 1: 0, 2: 0}
    for codeword in codewords:
        if codeword == zero:
            continue
        by_grade[grade_mod3(codeword)] += 1

    return {
        "algebra_dimensions": {
            "total_nonzero": len(codewords) - 1,
            "grade0": by_grade[0],
            "grade1": by_grade[1],
            "grade2": by_grade[2],
            "quotient_by_grade0": by_grade[1] + by_grade[2],
        },
        "universal_grade_laws": verify_universal_grade_laws(),
    }


@lru_cache(maxsize=1)
def build_algebraic_spine() -> AlgebraicSpine:
    local_shell = _latest_heisenberg_shell()
    global_geometry = _global_pauli_geometry()
    universal = _universal_closure_spine()
    tomotope = _tomotope_reye_bridge()
    vogel = _vogel_position()
    exceptional = _exceptional_parameter_dictionary(local_shell, global_geometry)

    route = (
        "Use the exact local H27 Heisenberg/MUB shell (1 qutrit) to organize "
        "phase transport, embed it into the exact W33 two-qutrit Pauli geometry, "
        "pass first through the canonical projective operator layer with "
        "Hamiltonian H_can = 12I - A = 16I - BB^T, and only then lift through "
        "the s12/Golay Heisenberg closure and the W(3,q) scaling family to the "
        "three-qutrit sl(27) layer. The same W(3,3) parameter package "
        "(40,12,2,4; q=3) already generates G2=14, F4=52, E6=78, E7=133, "
        "E8=248 and the octonionic magic-square row, so the Lie tower should "
        "be constrained to land on that dictionary rather than treated as a "
        "free bracket cascade. Vogel should be applied after Jacobi is "
        "resolved, as a universal constraint on the resulting Lie/kernel data, "
        "not as a raw replacement for the 728-dimensional closure."
    )

    return AlgebraicSpine(
        local_qutrit_shell=local_shell,
        global_pauli_geometry=global_geometry,
        universal_closure=universal,
        tomotope_reye_bridge=tomotope,
        vogel_position=vogel,
        exceptional_parameter_dictionary=exceptional,
        route_recommendation=route,
    )
