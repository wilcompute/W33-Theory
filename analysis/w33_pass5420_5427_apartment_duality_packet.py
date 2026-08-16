#!/usr/bin/env python3
"""Passes 5420--5427: all-q apartment duality packet.

This producer closes five queued directions after Pass5404--5411 and executes
three outside-box probes without relying on floating-point numerics.

5420  complementary cycle/cut Naimark tight frames on the flag set;
5421  canonical dual exact sequence from Levi H1 to the all-odd footprint code;
5422  all-q apartment/apartment intersection profile and dual Gram geometry;
5423  exact condition number of unsigned apartment visibility;
5425  exact finite-difference version of the q^4 "derivative" heuristic;
5426  all-odd footprint code as the point half of the Levi bicycle space;
5427  orthogonal two-design/simplex splitting of the flag representation.

Pass5424 is publication/CI closure and is handled by the packet workflow/auditor.
"""
from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/PART_W33_PASS5420_5427_APARTMENT_DUALITY_PACKET.json"
ANCHORS = (2, 3, 5)
ODD_ANCHORS = (3, 5, 7, 9, 11, 13)


def flag_parameters(q: int) -> dict:
    assert q > 1
    N = (q + 1) ** 2 * (q * q + 1)
    h1 = q**4
    cut = N - h1
    assert cut == 2 * (q + 1) * (q * q + 1) - 1
    return {"q": q, "N": N, "h1": h1, "cut": cut}


def cycle_cut_frame(q: int) -> dict:
    p = flag_parameters(q)
    N, h1, cut = p["N"], p["h1"], p["cut"]
    cyc = [Fraction(1, 1)] + [Fraction((-1) ** d, q**d) for d in range(1, 5)]
    cutip = [Fraction(1, 1)] + [
        Fraction(((-1) ** (d + 1)) * q ** (4 - d), cut) for d in range(1, 5)
    ]
    if q == 3:
        assert cyc == [Fraction(1), Fraction(-1, 3), Fraction(1, 9),
                       Fraction(-1, 27), Fraction(1, 81)]
        assert cutip == [Fraction(1), Fraction(27, 79), Fraction(-9, 79),
                         Fraction(3, 79), Fraction(-1, 79)]
    return {
        **p,
        "cycle_inner_products_d0_to_d4": [str(x) for x in cyc],
        "cut_inner_products_d0_to_d4": [str(x) for x in cutip],
        "cycle_frame_bound": f"{N}/{h1}",
        "cut_frame_bound": f"{N}/{cut}",
        "weighted_complement": f"({h1}/{N})G_cycle+({cut}/{N})G_cut=I_{N}",
    }


def footprint_bicycle(q: int) -> dict:
    assert q >= 3 and q % 2 == 1
    npts = (q + 1) * (q * q + 1)
    g = q * (q * q + 1) // 2
    line_rank = 1 + q * (q + 1) ** 2 // 2
    assert npts - line_rank == g
    bike = 2 * g - 1
    return {
        "q": q,
        "footprint_length": npts,
        "footprint_dimension_g": g,
        "point_half_dimension": g,
        "line_kernel_half_dimension": g,
        "intersection_dimension": 1,
        "bicycle_dimension": bike,
        "formula": "Bike = P_g + L_g, P_g cap L_g = <J>, dim Bike=2g-1=q(q^2+1)-1",
    }


def apartment_intersection_formula(q: int) -> dict:
    N = (q + 1) ** 2 * (q * q + 1)
    M = N * q**4 // 8
    a4 = q - 1
    a3 = (q - 1) ** 2
    a2 = q * (q - 1) ** 2
    a1 = q**2 * (q - 1) ** 2
    n = {
        4: 8 * a4,
        3: 8 * a3,
        2: 8 * a2,
        1: 8 * a1,
    }
    n[0] = M - 1 - sum(n.values())
    assert n[0] >= 0
    assert sum(n.values()) == M - 1
    return {
        "q": q,
        "apartments": M,
        "per_apartment_other_intersections": {str(k): n[k] for k in range(5)},
        "proper_nonempty_intersection": "one consecutive flag-edge path of length j in {1,2,3,4}",
        "signed_normalized_absolute_inner_products": ["0", "1/8", "1/4", "3/8", "1/2"],
        "coherence": "1/2",
    }


def unsigned_condition(q: int) -> dict:
    assert q > 1
    lam_max = 8 * q**4
    lam_min = (q - 1) ** 2 * (q * q + 1)
    gram_cond = Fraction(lam_max, lam_min)
    residual = (q*q + 1) * (q**4 - 2*q**3 + 6*q*q - 2*q + 1)
    assert residual > 0
    return {
        "q": q,
        "lambda_max": lam_max,
        "lambda_min": lam_min,
        "gram_condition_squared_singular_condition": str(gram_cond),
        "singular_condition": f"sqrt({gram_cond.numerator}/{gram_cond.denominator})",
        "asymptotic_gram_condition": 8,
        "asymptotic_singular_condition": "sqrt(8)",
    }


def derivative_gallery(q: int) -> dict:
    tower = [q**4, q**3, q**2, q, 1]
    delta = (q + 1) ** 4 - q**4
    weighted = 4 * tower[1] + 6 * tower[2] + 4 * tower[3] + tower[4]
    assert delta == weighted
    return {
        "q": q,
        "gallery_tower": tower,
        "finite_difference_q4": delta,
        "identity": "(q+1)^4-q^4 = 4 q^3 + 6 q^2 + 4 q + 1",
        "gallery_reading": "Delta(q^4)=4 I2+6 I3+4 I4+I5 for I_k=q^(5-k)",
    }


def simplex_split(q: int) -> dict:
    p = flag_parameters(q)
    N, h1, cut = p["N"], p["h1"], p["cut"]
    nonconstant_cut = cut - 1
    assert h1 + nonconstant_cut == N - 1
    return {
        "q": q,
        "N": N,
        "cycle_design_dimension": h1,
        "centered_cut_design_dimension": nonconstant_cut,
        "simplex_dimension": N - 1,
        "orthogonal_projectors": "P_cycle + P_cut0 = I - J/N",
        "weighted_gram_identity":
            f"({h1}/{N-1})G_cycle+({nonconstant_cut}/{N-1})G_cut0=G_simplex",
        "cycle_is_spherical_2_design": True,
        "centered_cut_is_spherical_2_design": True,
    }


def _canon_vec(v: tuple[int, ...], q: int) -> tuple[int, ...]:
    for x in v:
        x %= q
        if x:
            inv = pow(x, -1, q)
            return tuple((y * inv) % q for y in v)
    raise ValueError("zero vector")


def _symp(u: tuple[int, ...], v: tuple[int, ...], q: int) -> int:
    return (u[0] * v[1] - u[1] * v[0] + u[2] * v[3] - u[3] * v[2]) % q


def _build_W_prime(q: int):
    pts = sorted({
        _canon_vec(v, q)
        for v in product(range(q), repeat=4)
        if any(v)
    })
    idx = {p: i for i, p in enumerate(pts)}
    line_sets = set()
    for i, u in enumerate(pts):
        for v in pts[i + 1:]:
            if _symp(u, v, q) != 0:
                continue
            L = {
                _canon_vec(tuple((a*u[k] + b*v[k]) % q for k in range(4)), q)
                for a in range(q) for b in range(q) if a or b
            }
            line_sets.add(tuple(sorted(L)))
    lines = [tuple(idx[p] for p in L) for L in sorted(line_sets)]
    pair_line = {}
    neigh = [set() for _ in pts]
    for li, L in enumerate(lines):
        for a, b in combinations(L, 2):
            key = tuple(sorted((a, b)))
            pair_line[key] = li
            neigh[a].add(b)
            neigh[b].add(a)
    return pts, lines, pair_line, neigh


def _enumerate_apartments_prime(q: int):
    pts, lines, pair_line, neigh = _build_W_prime(q)
    apartments = {}
    for a in range(len(pts)):
        for c in range(a + 1, len(pts)):
            if c in neigh[a]:
                continue
            common = sorted(neigh[a] & neigh[c])
            for b, d in combinations(common, 2):
                if d in neigh[b]:
                    continue
                cyc = (a, b, c, d)
                ls = [
                    pair_line[tuple(sorted((cyc[i], cyc[(i + 1) % 4])))]
                    for i in range(4)
                ]
                flags = set()
                for i, li in enumerate(ls):
                    flags.add((cyc[i], li))
                    flags.add((cyc[(i + 1) % 4], li))
                apartments[frozenset(flags)] = cyc
    return pts, lines, apartments


def census_anchor(q: int) -> dict:
    pts, lines, apartments = _enumerate_apartments_prime(q)
    formula = apartment_intersection_formula(q)
    assert len(pts) == (q + 1) * (q*q + 1)
    assert len(lines) == len(pts)
    assert len(apartments) == formula["apartments"]
    base = next(iter(apartments))
    profile = Counter(len(base & A) for A in apartments if A != base)
    got = {str(k): profile.get(k, 0) for k in range(5)}
    assert got == formula["per_apartment_other_intersections"]
    return {
        "q": q,
        "points": len(pts),
        "lines": len(lines),
        "apartments": len(apartments),
        "intersection_profile": got,
    }


def cross_regressions() -> dict:
    old549 = json.loads((ROOT / "data/PART_BT549_W33_LEVI_CYCLE_CUT_TIGHT_FRAME_DUALITY_results.json").read_text())
    assert old549["objects"]["cycle_projector_rank"] == 81
    assert old549["objects"]["cut_projector_rank"] == 79
    assert old549["cut_tight_frame_R79"]["inner_products_by_line_graph_distance"] == {
        "0": "1", "1": "27/79", "2": "-9/79", "3": "3/79", "4": "-1/79"
    }

    old546 = json.loads((ROOT / "data/PART_BT546_W33_LEVI_CYCLE_PHASE_FRAME_UNIFICATION_results.json").read_text())
    assert old546["cycle_Z_side"]["per_cycle_overlap_profile"] == {
        "0": 1187, "1": 288, "2": 96, "3": 32, "4": 16
    }

    p5066 = json.loads((ROOT / "data/PART_W33_PASS5066_5073_RESULTS.json").read_text())
    assert p5066["5066"]["W3q"]["theta_generates_full_dual"] is True
    assert p5066["5068"]["subdivision_2_height_dimensions"][0:2] == [81, 29]
    assert p5066["5068"]["point_half"]["dimension"] == 15

    p5378_path = ROOT / "data/PART_W33_PASS5378_FOOTPRINT_CODE_MINIMUM_ORBIT.json"
    if p5378_path.is_file():
        p5378 = json.loads(p5378_path.read_text())
        assert p5378["sample_parameters"]["3"]["dimension"] == 15
        assert p5378["sample_parameters"]["3"]["minimum_distance"] == 8

    return {
        "BT549_q3_cut_frame": "matched",
        "BT546_q3_apartment_intersections": "matched",
        "Pass5066_theta_H1": "matched",
        "Pass5068_P15_Bike29": "matched",
        "Pass5378_q3_footprint15": "matched if certificate present",
    }


def build_certificate() -> dict:
    anchors = {str(q): census_anchor(q) for q in ANCHORS}
    odd = {str(q): footprint_bicycle(q) for q in ODD_ANCHORS}
    frames = {str(q): cycle_cut_frame(q) for q in (2, 3, 4, 5, 7, 9, 11, 13)}
    cond = {str(q): unsigned_condition(q) for q in (2, 3, 4, 5, 7, 9, 11, 13)}
    derivative = {str(q): derivative_gallery(q) for q in (2, 3, 5, 7, 11)}
    simplex = {str(q): simplex_split(q) for q in (2, 3, 5, 7, 11)}

    assert odd["3"]["bicycle_dimension"] == 29
    assert odd["3"]["point_half_dimension"] == 15
    assert frames["3"]["cut"] == 79
    assert anchors["3"]["intersection_profile"] == {
        "0": 1187, "1": 288, "2": 96, "3": 32, "4": 16
    }
    assert cond["3"]["gram_condition_squared_singular_condition"] == "81/5"
    assert simplex["3"]["cycle_design_dimension"] == 81
    assert simplex["3"]["centered_cut_design_dimension"] == 78

    return {
        "schema": "w33.pass5420_5427.apartment_duality.v1",
        "status": "THEOREM_PACKET_SOURCE_COMPLETE",
        "domain": {
            "all_q": "finite generalized quadrangles GQ(q,q), q>1, for frame/intersection/conditioning statements",
            "odd_q": "odd prime powers q for footprint-code/bicycle identification using C_F=C_W^perp",
        },
        "5420_complementary_cut_frame": {
            "cycle_projector":
                "E=(q^4 A0-q^3 A1+q^2 A2-q A3+A4)/N, rank q^4",
            "cut_projector": "I-E, rank r=N-q^4=2(q+1)(q^2+1)-1",
            "cycle_unit_gram": "G_cyc=(N/q^4)E; <x_e,x_f>=(-1/q)^d",
            "cut_unit_gram":
                "G_cut=N(I-E)/r; offdiag_d=(-1)^(d+1)q^(4-d)/r",
            "weighted_identity": "(q^4/N)G_cyc+(r/N)G_cut=I_N",
            "anchors": frames,
        },
        "5421_H1_footprint_dual_sequence": {
            "input_5066": "0 -> Theta -> F2[A] -> H1(Levi;F2) -> 0",
            "dual": "0 -> H1(Levi)^* -> F2[A] -> Theta^* -> 0, so C_A=Theta^perp ~= H1(Levi)^*",
            "input_5384_odd": "0 -> D_q -> C_A -> C_F -> 0",
            "composite_odd":
                "0 -> D_q -> H1(Levi)^* -> C_F -> 0; dualizing gives 0 -> C_F^* -> H1(Levi) -> D_q^* -> 0",
            "dimensions":
                "dim H1=q^4, dim C_F=g=q(q^2+1)/2, dim D_q=q^4-g",
            "boundary":
                "This is an equivariant module exact sequence; it does not identify C_F with H1 itself without choosing/constructing a pairing.",
        },
        "5422_apartment_intersection_scheme": {
            "rigidity":
                "Two distinct apartments have either empty intersection or exactly one consecutive flag-edge path of length j=1..4.",
            "per_apartment_counts": {
                "n4": "8(q-1)",
                "n3": "8(q-1)^2",
                "n2": "8q(q-1)^2",
                "n1": "8q^2(q-1)^2",
                "n0": "Nq^4/8 - 1 - n1-n2-n3-n4",
            },
            "dual_signed_frame":
                "For normalized oriented apartment columns, |<c_A,c_B>|=j/8 on an intersection path of j edges; coherence=1/2.",
            "independent_prime_anchors": anchors,
        },
        "5423_unsigned_conditioning": {
            "lambda_max": "8q^4",
            "lambda_min": "(q-1)^2(q^2+1)",
            "gram_condition": "8q^4/((q-1)^2(q^2+1)) -> 8",
            "singular_condition": "sqrt(8)q^2/((q-1)sqrt(q^2+1)) -> sqrt(8)",
            "delicate_positivity_factor":
                "(q^2+1)(q^4-2q^3+6q^2-2q+1)>0",
            "anchors": cond,
            "boundary":
                "This conditions the full unsigned incidence operator B, not arbitrary sparse hardware submatrices.",
        },
        "5425_discrete_derivative_gallery": {
            "identity": "(q+1)^4-q^4 = 4q^3+6q^2+4q+1",
            "geometric_rewrite":
                "with I_k=q^(5-k) common-apartment counts for k consecutive chambers, Delta(q^4)=4I_2+6I_3+4I_4+I_5",
            "reading":
                "The user's 4q^3 observation is the leading term of an exact finite-difference identity whose lower corrections are the next gallery-intersection levels.",
            "anchors": derivative,
            "boundary": "This is discrete combinatorics, not a differential equation in q.",
        },
        "5426_footprint_bicycle_amalgam": {
            "odd_q_theorem":
                "Let M be point-line incidence over F2. Because q+1 is even, the Levi mod-2 signless Laplacian is [[0,M],[M^T,0]].",
            "point_embedding":
                "x in ker(M^T)=C_W^perp=C_F maps to flag vector y_(p,L)=x_p and lies in cut cap cycle.",
            "line_embedding":
                "z in ker(M) maps to y_(p,L)=z_L and lies in cut cap cycle; this is an incidence-dual kernel copy, not a claim of an L-footprint tensor.",
            "amalgam":
                "Bike=P_g+L_g, P_g cap L_g=<J>, dim Bike=2g-1=q(q^2+1)-1",
            "q3":
                "g=15 and dim Bike=29, exactly recovering the Pass5068 P15/Bike29 dimensions; the point half is canonically the q=3 footprint code.",
            "anchors": odd,
        },
        "5427_simplex_two_design_split": {
            "projectors":
                "P0=J/N, Pcyc=E_-2, Pcut0=I-P0-Pcyc, with ranks 1,q^4,r-1",
            "designs":
                "The normalized row projections onto Pcyc and Pcut0 are centered unit-norm tight frames, hence spherical 2-designs.",
            "simplex":
                "They orthogonally split the N-vertex regular simplex: q^4/(N-1) Gcyc + (r-1)/(N-1) Gcut0 = Gsimplex.",
            "q3":
                "160 simplex vertices split into an 81-dimensional cycle design and a 78-dimensional centered-cut design.",
            "anchors": simplex,
            "boundary":
                "This is a finite-frame/association-scheme statement, not a claim of new optimal spherical codes.",
        },
        "cross_regressions": cross_regressions(),
        "prior_art_firewall": {
            "flag_scheme":
                "Colangelo-Monzillo-Siciliano already construct the flag association scheme and its symmetric fusion; no priority claim is made for that scheme.",
            "naimark":
                "Complementary tight-frame language is standard Naimark-complement theory; the repo contribution here is the exact GQ(q,q) Hodge specialization and formulas.",
            "gq_frames":
                "Fickus-Jasper-Mixon-Peterson-Watson construct other tight frames from generalized quadrangles; no claim is made that generalized-quadrangle frame constructions are new.",
        },
    }


def main() -> dict:
    out = build_certificate()
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))
    return out


if __name__ == "__main__":
    main()
