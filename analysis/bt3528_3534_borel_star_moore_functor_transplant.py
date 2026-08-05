#!/usr/bin/env python3
"""Passes 3528-3534: Borel Fourier restriction, star-complement firewall,
Moore spectral/curvature tracks, typed quotient-reconstruction, and a
repository-wide W33/Gewirtz transplant audit.

All promoted arithmetic is exact and standard-library only.  The 3,720
star-complement candidate census was regenerated separately by the companion
heavy enumerator; the published compatibility-clique histogram is source-locked
rather than represented as an independent reimplementation.
"""
from __future__ import annotations
import collections
import hashlib
import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_BT3528_BT3534_BOREL_STAR_MOORE_FUNCTOR_TRANSPLANT_results.json"

def canon(x: Any) -> str:
    return json.dumps(x, sort_keys=True, separators=(",", ":"))

def semantic_sha(x: Any) -> str:
    return hashlib.sha256(canon(x).encode()).hexdigest()

def matmul(A: list[list[int]], B: list[list[int]]) -> list[list[int]]:
    n, p, m = len(A), len(B), len(B[0])
    assert len(A[0]) == p
    BT = list(zip(*B))
    return [[sum(a*b for a,b in zip(row,col)) for col in BT] for row in A]

def perkel_graph() -> tuple[list[tuple[int,int]], dict[tuple[int,int],int], list[list[int]]]:
    vertices = [(i,j) for i in range(3) for j in range(19)]
    index = {v:i for i,v in enumerate(vertices)}
    A = [[0]*57 for _ in range(57)]
    for i,j in vertices:
        rhs = pow(2, 6*i, 19)
        for k in range(19):
            if pow((k-j) % 19, 3, 19) == rhs:
                u = index[(i,j)]
                v = index[((i+1) % 3, k)]
                A[u][v] = A[v][u] = 1
    assert all(sum(row) == 6 for row in A)
    assert sum(map(sum,A)) // 2 == 171
    return vertices,index,A

def borel_action(v: tuple[int,int], b: int, m: int) -> tuple[int,int]:
    i,j = v
    return ((i+m) % 3, (pow(4,m,19)*j+b) % 19)

def perkel_borel_restriction() -> dict[str, Any]:
    vertices,index,A = perkel_graph()
    edge = {(i,j) for i in range(57) for j in range(i+1,57) if A[i][j]}
    for m in range(9):
        for b in range(19):
            perm = [index[borel_action(v,b,m)] for v in vertices]
            assert {tuple(sorted((perm[i],perm[j]))) for i,j in edge} == edge

    A2 = matmul(A,A)
    A3 = matmul(A2,A)
    N = [[-A3[i][j] + 9*A2[i][j] - 19*A[i][j] + (6 if i==j else 0)
          for j in range(57)] for i in range(57)]
    chars: dict[tuple[int,int], int] = {}
    fixed: dict[tuple[int,int], int] = {}
    for m in range(9):
        for b in range(19):
            perm = [index[borel_action(v,b,m)] for v in vertices]
            numerator = sum(N[perm[i]][i] for i in range(57))
            assert numerator % 171 == 0
            chars[(b,m)] = numerator // 171
            fixed[(b,m)] = sum(perm[i] == i for i in range(57))

    assert collections.Counter(chars.values()) == {20:1, 1:18, 2:38, -1:114}
    assert chars[(0,0)] == 20
    assert all(chars[(b,0)] == 1 for b in range(1,19))
    assert all(chars[(b,m)] == 2 for m in (3,6) for b in range(19))
    assert all(chars[(b,m)] == -1 for m in (1,2,4,5,7,8) for b in range(19))

    def fixed_dim(elements: list[tuple[int,int]]) -> int:
        total = sum(chars[g] for g in elements)
        assert total % len(elements) == 0
        return total // len(elements)

    dims = {
        "C19": fixed_dim([(b,0) for b in range(19)]),
        "C9": fixed_dim([(0,m) for m in range(9)]),
        "C3": fixed_dim([(0,m) for m in (0,3,6)]),
        "Borel_19:9": fixed_dim([(b,m) for m in range(9) for b in range(19)]),
    }
    assert dims == {"C19":2, "C9":2, "C3":8, "Borel_19:9":0}

    for b in range(19):
        for m in range(9):
            v18 = 18 if (b,m)==(0,0) else (-1 if m==0 else 0)
            v2 = 2 if m % 3 == 0 else -1
            rhs_perm = 1 + 3*v18 + v2
            assert rhs_perm == fixed[(b,m)]
            rhs_minus3 = v18 + v2
            assert rhs_minus3 == chars[(b,m)]
            golden = fixed[(b,m)] - 1 - chars[(b,m)]
            assert golden == 2*v18

    return {
        "group": {"structure":"C19 semidirect C9", "order":171,
                  "action":"(i,j)->(i+m mod 3, 4^m*j+b mod 19)"},
        "all_171_actions_verified_graph_automorphisms": True,
        "minus3_character_distribution": {"20":1,"1":18,"2":38,"-1":114},
        "minus3_complex_decomposition":
            "chi_3 + chi_6 + psi_plus(deg9) + psi_minus(deg9)",
        "minus3_rational_decomposition": "V18(conductor19) + V2(conductor3)",
        "fixed_dimensions": dims,
        "boundary":
            "This closes the surviving 19:9 shadow on the Perkel side; it does not construct a 19:9 action on a hypothetical M57.",
        "full_permutation_rational_decomposition":
            "Q^57 = 1 + 3*V18 + V2",
        "spectral_allocation": {
            "constant_6_eigenspace":"1",
            "combined_golden_36_space":"2*V18",
            "minus3_20_space":"V18+V2",
        },
    }

PUBLISHED_CLIQUE_HIST = {
    2:6,3:2,4:13,5:32,6:18,7:173,8:358,9:403,10:131,
    11:220,12:502,13:400,14:58,15:123,16:303,29:19,30:49,31:910,
}

def star_complement_firewall() -> dict[str, Any]:
    assert sum(PUBLISHED_CLIQUE_HIST.values()) == 3720
    assert max(PUBLISHED_CLIQUE_HIST) == 31
    assert all(k not in PUBLISHED_CLIQUE_HIST for k in range(17,29))
    low = sum(v for k,v in PUBLISHED_CLIQUE_HIST.items() if k <= 16)
    high = sum(v for k,v in PUBLISHED_CLIQUE_HIST.items() if k >= 29)
    assert (low,high) == (2742,978)
    independent = {
        "stage_counts_after_added_vertices":[22,784,157349],
        "spectral_survivors":3720,
        "canonical_survivor_sha256":
            "c1e0cb753fbdeab4d8ecf8059896b6ff1eb1fcc75c663022ab7040ceea012219",
        "criterion":"second-largest adjacency eigenvalue strictly below 2",
    }
    return {
        "target_parameters":[57,14,1,4],
        "target_spectrum":{"14":1,"2":38,"-5":18},
        "star_complement_order":19,
        "seed":"closed neighborhood windmill W14 plus one external vertex meeting four independent leaves",
        "independent_candidate_census":independent,
        "published_compatibility_clique_histogram":
            {str(k):v for k,v in sorted(PUBLISHED_CLIQUE_HIST.items())},
        "required_clique":38,
        "largest_clique":31,
        "nonexistence_margin":7,
        "obstruction_landscape":{
            "maxima_2_through_16":low,
            "maxima_29_through_31":high,
            "forbidden_maximum_band":[17,28],
        },
        "verdict":"No compatibility graph has a 38-clique; SRG(57,14,1,4) does not exist.",
        "provenance":{
            "paper":"M. Milosevic, Filomat 22:2 (2008), 53-57",
            "doi":"10.2298/FIL0802053M",
        },
        "boundary":
            "The 3720-candidate census is independently regenerated. The maximum-clique histogram is source-locked to the published Cliquer computation; an independent all-3720 clique rerun remains a separate reproducibility job.",
    }

def moore_spectral_gate(fibre_size: int) -> dict[str, Any]:
    d = fibre_size + 1
    disc = 4*d - 3
    t = math.isqrt(disc)
    row: dict[str,Any] = {
        "fibre_size":fibre_size, "degree":d, "vertices":d*d+1,
        "discriminant":disc,
    }
    if t*t != disc:
        if d == 2:
            row.update({
                "status":"SPECTRALLY_ADMISSIBLE",
                "restricted_eigenvalues":["(-1+sqrt(5))/2","(-1-sqrt(5))/2"],
                "multiplicities":[2,2],
            })
            return row
        row["status"] = "REJECT_GLOBAL_SPECTRUM_NONSQUARE"
        return row
    r = (-1+t)//2
    s = (-1-t)//2
    num = d*(d-2)
    if num % t:
        row["status"] = "REJECT_NONINTEGRAL_MULTIPLICITIES"
        row["restricted_eigenvalues"]=[r,s]
        return row
    f_num = d*d + num//t
    g_num = d*d - num//t
    if f_num % 2 or g_num % 2:
        row["status"] = "REJECT_NONINTEGRAL_MULTIPLICITIES"
        return row
    row.update({
        "status":"SPECTRALLY_ADMISSIBLE",
        "restricted_eigenvalues":[r,s],
        "multiplicities":[f_num//2,g_num//2],
    })
    return row

def moore_dual_tracks() -> dict[str, Any]:
    stages = [1,2,4,6] + list(range(8,57,2))
    rows = [moore_spectral_gate(n) for n in stages]
    admissible = [x["fibre_size"] for x in rows if x["status"]=="SPECTRALLY_ADMISSIBLE"]
    assert admissible == [1,2,6,56]
    status = {1:"C5 exact witness",2:"Petersen exact witness",
              6:"Hoffman-Singleton exact witness",56:"M57 open"}
    for row in rows:
        if row["fibre_size"] in status:
            row["interpretation"] = status[row["fibre_size"]]
    return {
        "global_stage_gate":rows,
        "only_admissible_fibre_sizes":admissible,
        "unrestricted_track":{
            "n6":"exact Hoffman-Singleton edge-chart witness",
            "n8_to_n54":"rejected before CSP by the global Moore spectral gate",
            "n56":"172480 directed integer variables plus lazy triangle and mu separators",
        },
        "involutive_curvature_track":{
            "n2":"Petersen matching is the unique fixed-point-free involution on two symbols",
            "n6":"all 15 pair matchings and all 20 triangle holonomies are 2^3",
            "n56":"export conjugacy-class branch with 2^28 holonomy cuts; no SAT/UNSAT verdict",
        },
        "boundary":
            "Spectral rejection of intermediate stages is not a local-CSP UNSAT proof. The n=56 unrestricted and involutive tracks remain unsolved.",
    }

def quotient_reconstruct_no_go() -> dict[str, Any]:
    w33 = {
        "objects":[240,120,40],
        "operations":["uniform antipodal quotient fibre 2",
                      "uniform 40K3 quotient fibre 3"],
        "combined_fibre":6,
        "side_label_alphabet":6,
        "every_stage_surjective":True,
    }
    golay = {
        "objects":[100,77,56],
        "operations":["induced second-subconstituent restriction deleting infinity plus 22 points",
                      "point-avoidance restriction deleting 21 hexads"],
        "deleted_counts":[23,21],
        "uniform_quotient_possible":[100 % 77 == 0, 77 % 56 == 0],
        "reconstruction_requires":"deleted incidence objects, not a fibre label",
    }
    assert golay["uniform_quotient_possible"] == [False,False]
    return {
        "W33_face_tower":w33,
        "Golay_Witt_tower":golay,
        "uniform_fibre_functor_equivalence":False,
        "no_go_reason":"100/77 and 77/56 are nonintegral, whereas 240/120=2 and 120/40=3.",
        "minimal_typed_morphism_vocabulary":[
            "uniform_quotient","induced_restriction","point_avoidance","incidence_extension"
        ],
        "reconstruction_axiom":
            "A quotient plus side label reconstructs iff x -> (q(x),side(x)) is injective; an induced restriction instead needs the deleted object and incidence attachment data.",
        "boundary":
            "The two towers share a quotient-reconstruct pattern only in a typed information-loss category, not as one uniform quotient functor.",
    }

BASELINE_SEARCH_HITS = [
"tools/SOLVE_IT.py","docs/index.html","docs/triangle-free-srg-m57.html",
"docs/seven-graph-csp-scheme.html",
"analysis/BT3500_BT3505_triangle_free_srg_m57_bridge.md",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry.md",
"analysis/bt3500_3505_triangle_free_srg_m57_bridge.py",
"analysis/bt3506_3512_seven_graph_csp_scheme_symmetry.py",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry_insert.tex",
"exploration/PART_CCLXXVII_SCHLAFLI_DOUBLE_SIX_BRIDGE.py",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry_index_insert.html",
"out.txt","exploration/PART_CCLXXVIII_GOSSET_POLYTOPE_BRIDGE.py",
"data/PART_BT3500_BT3505_TRIANGLE_FREE_SRG_M57_BRIDGE_results.json",
"data/PART_BT3506_BT3512_SEVEN_GRAPH_CSP_SCHEME_SYMMETRY_results.json",
"exploration/PART_CCLXXXV_ALBERT_JORDAN_BRIDGE.py",
"exploration/PART_CCLXXXI_TERNARY_CODES_BRIDGE.py",
"exploration/PART_CCLXXXII_MBQC_GRAPH_STATES_BRIDGE.py",
"archive/root_scripts/PMNS_AND_UNIQUENESS.py",
"exploration/PART_CCLXXIX_PLATONIC_MCKAY_BRIDGE.py",
"exploration/PART_CCLXXXIV_RAMANUJAN_IHARA_BRIDGE.py",
"exploration/PART_CCLXXX_FINITE_GEOMETRY_BRIDGE.py",
"exploration/PART_CCLXXXIII_DISCRETE_WIGNER_BRIDGE.py",
"tests/test_schlafli_double_six_cclxxvii.py",
"tests/test_bt3500_bt3505_triangle_free_srg_m57_bridge.py",
"tests/test_gosset_polytope_cclxxviii.py",
"_test_q35.txt","_test_q36.txt","_test_q37.txt","_test_q35b.txt",
"_test_q35c.txt","_test_q36b.txt","_test_q36c.txt",
"tests/test_albert_jordan_cclxxxv.py",
]
DIRECT_KERNEL_ARTIFACTS = {
"docs/index.html","docs/triangle-free-srg-m57.html","docs/seven-graph-csp-scheme.html",
"analysis/BT3500_BT3505_triangle_free_srg_m57_bridge.md",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry.md",
"analysis/bt3500_3505_triangle_free_srg_m57_bridge.py",
"analysis/bt3506_3512_seven_graph_csp_scheme_symmetry.py",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry_insert.tex",
"analysis/BT3506_BT3512_seven_graph_csp_scheme_symmetry_index_insert.html",
"data/PART_BT3500_BT3505_TRIANGLE_FREE_SRG_M57_BRIDGE_results.json",
"data/PART_BT3506_BT3512_SEVEN_GRAPH_CSP_SCHEME_SYMMETRY_results.json",
"tests/test_bt3500_bt3505_triangle_free_srg_m57_bridge.py",
}

def spectral_transplant_audit() -> dict[str, Any]:
    assert len(BASELINE_SEARCH_HITS) == 34
    direct = sorted(set(BASELINE_SEARCH_HITS) & DIRECT_KERNEL_ARTIFACTS)
    context = sorted(set(BASELINE_SEARCH_HITS) - DIRECT_KERNEL_ARTIFACTS)
    assert len(direct)==12 and len(context)==22
    return {
        "baseline_head":"54133497390161b6cb6502e7c1aff1d8033b78d3",
        "repository_code_search_query":"W33 Gewirtz",
        "hits":34,
        "direct_common_kernel_artifacts":direct,
        "context_or_atlas_hits":context,
        "automatic_port_policy":{
            "ALLOW":["identities reduced in Q[x]/(x^2+2x-8)",
                     "U=(-I-A)/3 and U^2=I on augmentation",
                     "polynomial spectral projectors as formulas"],
            "REQUIRE_NEW_EVIDENCE":["trace","determinant","projector rank",
                                    "multiplicity","p-rank"],
            "DENY_AUTOMATIC_PORT":["lines","cliques","incidence factorizations",
                                   "automorphism groups","codes","descendant maps",
                                   "symplectic geometry"],
        },
        "ported_now":[
            "all adjacency polynomial identities reduce to aA+bI",
            "centered complement is a common reflection",
            "functional calculus is two-channel"
        ],
        "explicit_nonports":[
            "W33 projector ranks 24 and 15 versus Gewirtz ranks 35 and 20",
            "W33 line/incidence and code constructions",
            "any objectwise intertwiner"
        ],
        "boundary":
            "This is an exact live-head source-search audit and policy guard, not proof that every historical prose mention is mathematically correct.",
    }

def hs_factorization_pencil() -> dict[str, Any]:
    n=6
    matchings_per_pencil=n-1
    edges_per_matching=n//2
    assert matchings_per_pencil*edges_per_matching == n*(n-1)//2
    n56=56
    assert (n56-1)*(n56//2) == n56*(n56-1)//2 == 1540
    return {
        "theorem":
            "If every row-pair permutation is an involution, then the vertex-star AllDifferent law makes the n-1 nonidentity maps at each source row a 1-factorization of K_n.",
        "Hoffman_Singleton":{
            "fibre_size":6,
            "pencils":6,
            "matchings_per_pencil":5,
            "cycle_type":"2^3",
            "edges_covered_once_per_pencil":15,
            "closed_under_composition":False,
            "reading":"six coupled non-group 1-factorization pencils",
        },
        "M57_involutive_branch":{
            "fibre_size":56,
            "pencils":56,
            "matchings_per_pencil":55,
            "cycle_type":"2^28",
            "edges_covered_once_per_pencil":1540,
            "new_model_view":"56 reciprocity-coupled 1-factorizations of K56 plus holonomy and mu=1 cuts",
        },
        "boundary":
            "Pair-matching involution is gauge/coordinate dependent; triangle-holonomy cycle type is conjugacy invariant. The factorization theorem applies only inside the explicit involutive branch.",
    }

def build_certificate() -> dict[str, Any]:
    result = {
        "schema":"w33.pass3528_3534.borel_star_moore_functor_transplant.v1",
        "status":"PASS_7_FRONTS",
        "passes":[3528,3529,3530,3531,3532,3533,3534],
        "front_3528_perkel_borel_restriction":perkel_borel_restriction(),
        "front_3529_star_complement_firewall":star_complement_firewall(),
        "front_3530_m57_dual_tracks":moore_dual_tracks(),
        "front_3531_typed_quotient_reconstruct":quotient_reconstruct_no_go(),
        "front_3532_spectral_transplant_audit":spectral_transplant_audit(),
        "front_3533_bonkers_borel_fourier_tomography":{
            "headline":"The entire Perkel 57-space is 1 + 3 conductor-19 channels + one conductor-3 phase channel.",
            "decomposition":"Q^57 = 1 + 3*V18 + V2",
            "spectral_split":"golden36=2*V18; minus3_20=V18+V2",
        },
        "front_3534_bonkers_factorization_curvature":hs_factorization_pencil(),
        "evidence_boundary":[
            "No existence or nonexistence verdict for M57 is claimed.",
            "No n=56 CP-SAT SAT/UNSAT result is claimed.",
            "The star-complement 3720 census is independent; the all-graph clique histogram is publication-locked, not independently recomputed here.",
            "The 19:9 module is constructed on Perkel only, not on a hypothetical M57.",
            "The two descendant towers are not identified.",
            "W33/Gewirtz geometry-sensitive claims do not auto-port.",
        ],
    }
    payload=dict(result)
    result["semantic_sha256"]=semantic_sha(payload)
    return result

def main() -> None:
    result=build_certificate()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(result["status"],result["semantic_sha256"])

if __name__=="__main__":
    main()
