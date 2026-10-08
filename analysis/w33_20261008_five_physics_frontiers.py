#!/usr/bin/env python3
"""Five independent, reproducible frontier tests; physical boundaries are explicit.

These are *necessary checks / constructive models*, not a TOE or a continuum limit.
Prior ownership: 2026-09-24 dual-27 firewall, 2026-10-08 electrical-transport
certificate; Pass10952/11038 CPTP; Pass11675 lattice Gauss; Pass11697/11698
chirality vacuum; Pass11742-11757 string and kinetic interfaces.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
from w33_20261008_dual_27_electrical_transport import build_graphs, normalize, pairing

OUT = ROOT / "data" / "w33_20261008_five_physics_frontiers.json"


def projective_points_and_lines():
    pts = sorted({normalize(v) for v in itertools.product(range(3), repeat=4) if any(v)})
    lines = set()
    for x, y in itertools.combinations(pts, 2):
        if pairing(x, y):
            continue
        support = tuple(sorted({
            normalize(tuple((a*xi+b*yi) % 3 for xi, yi in zip(x, y)))
            for a, b in itertools.product(range(3), repeat=2) if a or b
        }))
        assert len(support) == 4
        lines.add(support)
    assert len(pts) == len(lines) == 40
    return pts, sorted(lines)


def cp_walk_frontier():
    """One exact CPTP *entanglement-breaking* realization, not a claimed native photon dynamics."""
    result = {}
    for name, a in build_graphs().items():
        assert a.shape == (27, 27) and np.all(a.sum(axis=0) == 8)
        # K_{j,i}=|j><i|/sqrt(8) for all oriented adjacent pairs.
        # Sum K^dagger K = diag(outdegree_i/8) = I.
        kraus_count = int(a.sum())
        assert kraus_count == 216
        kdagk_diag = [Q(int(x), 8) for x in a.sum(axis=1)]
        assert set(kdagk_diag) == {Q(1)}
        # The 216 orthogonal vectorized matrix units give positive Choi
        # eigenvalues 1/8, plus 513 exact zero eigenvalues.
        # An incoherent measure-and-prepare channel is entanglement-breaking.
        two_steps_num = a @ a
        assert np.array_equal(two_steps_num, two_steps_num.T)
        assert np.all(two_steps_num.sum(axis=1) == 64)
        offzero = int(sum(two_steps_num[i, j] == 0
                          for i in range(27) for j in range(27) if i != j))
        hist = Counter(int(two_steps_num[i, j])
                       for i in range(27) for j in range(27) if i != j)
        result[name] = {
            "kraus_count": kraus_count,
            "choi_positive_eigenvalue": "1/8",
            "choi_positive_multiplicity": 216,
            "choi_zero_multiplicity": 513,
            "trace_preserving": True,
            "entanglement_breaking": True,
            "two_step_ordered_offdiagonal_zero_count": offzero,
            "two_step_numerator_histogram": dict(sorted(hist.items())),
            "probability_unit": "1/64",
        }
    assert result["point_far_H27"]["two_step_ordered_offdiagonal_zero_count"] == 54
    assert result["line_transverse_null"]["two_step_ordered_offdiagonal_zero_count"] == 0
    return result


def constraint_frontier():
    """Exact local-edge-current nonclosure test; not a proof about all ADM discretizations."""
    pts, lines = projective_points_and_lines()
    idx = {p: i for i, p in enumerate(pts)}
    nb = {i: [] for i in range(80)}
    for k, line in enumerate(lines):
        j = 40 + k
        for p in line:
            i = idx[p]
            nb[i].append(j)
            nb[j].append(i)
    assert len(nb) == 80 and all(len(x) == 4 for x in nb.values())
    assert sum(map(len, nb.values())) // 2 == 160
    wedges = []
    for j, neighbors in nb.items():
        for i, k in itertools.combinations(neighbors, 2):
            assert k not in nb[i]  # Levi is bipartite (girth 8).
            wedges.append((i, j, k))
    assert len(wedges) == 480
    q0, q1, q2, p0, p1, p2 = sp.symbols("q0 q1 q2 p0 p1 p2")
    j01 = (p0+p1)*(q0-q1)
    j12 = (p1+p2)*(q1-q2)
    qvars, pvars = (q0,q1,q2), (p0,p1,p2)
    bracket = sp.expand(sum(sp.diff(j01,q)*sp.diff(j12,p) -
                            sp.diff(j01,p)*sp.diff(j12,q)
                            for q,p in zip(qvars,pvars)))
    # A nonedge i--k cannot appear in any nearest-neighbor current.
    assert sp.expand(bracket).coeff(p0).coeff(q2) == 1
    assert sp.expand(bracket).coeff(p2).coeff(q0) == -1
    return {
        "levi_vertices": 80, "levi_edges": 160,
        "induced_length_two_wedges": len(wedges),
        "first_witness_vertices": list(wedges[0]),
        "local_edge_current_bracket": str(bracket),
        "nonedge_p0_q2_coefficient": 1,
        "nonedge_p2_q0_coefficient": -1,
        "naive_nearest_edge_current_algebra_closes": False,
    }


FIELDS = {
    # All fermions are LEFT-handed Weyl superfields; hypercharges are conventional.
    "Q":  {"Y":Q(1,6), "BL":Q(1,3), "weight":6},
    "Uc": {"Y":Q(-2,3),"BL":Q(-1,3),"weight":3},
    "Dc": {"Y":Q(1,3), "BL":Q(-1,3),"weight":3},
    "L":  {"Y":Q(-1,2),"BL":Q(-1),  "weight":2},
    "Ec": {"Y":Q(1),   "BL":Q(1),   "weight":1},
    "Nc": {"Y":Q(0),   "BL":Q(1),   "weight":1},
    "Hu": {"Y":Q(1,2), "BL":Q(0),   "weight":2},
    "Hd": {"Y":Q(-1,2),"BL":Q(0),   "weight":2},
}


def anomaly_sum(charge: str, power: int, names):
    return sum((FIELDS[n]["weight"] * FIELDS[n][charge]**power
                for n in names), Q(0))


def chirality_frontier():
    """Reproduce the discrete pair obstruction; check full-family anomaly sums."""
    pts, lines = projective_points_and_lines()
    assert len(pts) == len(lines) == 40
    classes = {}
    for a, b in itertools.product(range(3), repeat=2):
        if not a and not b:
            continue
        kernel = tuple(sorted({
            (x,y) if next(t for t in (x,y) if t) == 1 else ((2*x)%3,(2*y)%3)
            for x,y in itertools.product(range(3), repeat=2)
            if (x or y) and (a*x+b*y) % 3 == 0
        }))
        assert len(kernel) == 1
        classes[(a,b)] = kernel[0]
    c = Counter(classes.values())
    assert len(c) == 4 and set(c.values()) == {2}
    # Exactly 4 kernel directions x 2 conjugate characters on every one
    # of 40 isotropic lines -> 320 vacua, paired under sign reversal.
    pairs = len(lines)*len(c)
    assert pairs == 160
    matter = ["Q","Uc","Dc","L","Ec","Nc"]
    conditions = {
        "SU3_squared_Y": 2*FIELDS["Q"]["Y"]+FIELDS["Uc"]["Y"]+FIELDS["Dc"]["Y"],
        "SU2_squared_Y": 3*FIELDS["Q"]["Y"]+FIELDS["L"]["Y"],
        "gravitational_Y": anomaly_sum("Y",1,matter),
        "cubic_Y": anomaly_sum("Y",3,matter),
        "gravitational_BL_with_Nc": anomaly_sum("BL",1,matter),
        "cubic_BL_with_Nc": anomaly_sum("BL",3,matter),
        "gravitational_BL_without_Nc": anomaly_sum("BL",1,matter[:-1]),
        "cubic_BL_without_Nc": anomaly_sum("BL",3,matter[:-1]),
    }
    assert all(v == 0 for k,v in conditions.items() if not k.endswith("without_Nc"))
    assert conditions["gravitational_BL_without_Nc"] == -1
    assert conditions["cubic_BL_without_Nc"] == -1
    return {
        "isotropic_lines": 40,
        "nontrivial_line_characters_each": 8,
        "quartic_chiral_vacua": 320,
        "conjugate_sign_pairs": pairs,
        "unique_handedness_from_even_potential": False,
        "anomaly_checks": {k:str(v) for k,v in conditions.items()},
        "scope": "Standard Model plus one right-handed neutrino per family; no vacuum dynamics derived",
    }


def operator_charges(ops):
    y = sum((FIELDS[n]["Y"] for n in ops), Q(0))
    bl = sum((FIELDS[n]["BL"] for n in ops), Q(0))
    threebl = 3*bl
    assert threebl.denominator == 1
    return {"Y":str(y),"BL":str(bl),
            "matter_parity":1 if int(threebl)%2 == 0 else -1,
            "hypercharge_neutral":y==0, "BL_neutral":bl==0}


def vacuum_frontier():
    """Necessary abelian selection rules, NEVER a full heterotic worldsheet test."""
    operators = {
        "UcDcDc": ["Uc","Dc","Dc"],
        "QLDc": ["Q","L","Dc"],
        "LLEc": ["L","L","Ec"],
        "NcUcDcDc": ["Nc","Uc","Dc","Dc"],
        "NcQLDc": ["Nc","Q","L","Dc"],
        "NcLLEc": ["Nc","L","L","Ec"],
        "QQQL": ["Q","Q","Q","L"],
        "UcUcDcEc": ["Uc","Uc","Dc","Ec"],
    }
    out = {k:operator_charges(v) for k,v in operators.items()}
    for key in ["UcDcDc","QLDc","LLEc"]:
        assert out[key]["hypercharge_neutral"] and out[key]["matter_parity"] == -1
        c = "Nc"+key
        assert out[c]["BL_neutral"] and out[c]["matter_parity"] == 1
    for key in ["QQQL","UcUcDcEc"]:
        assert out[key]["BL_neutral"] and out[key]["matter_parity"] == 1
    return {"operator_checks":out,
            "consequence":"Nc VEV can regenerate three RPV operators; matter parity does not exclude QQQL/UcUcDcEc",
            "boundary":"SU(3)xSU(2) contractions require suitable family indices; string selection rules, FI D flatness and actual vacuum spectra NOT checked"}


def normalization_frontier():
    """A no-go for scale extraction from the unweighted graph spectrum alone."""
    eigenvalues = {0:1,6:12,9:8,12:6}
    # omega^2(lambda)=(a+b*lambda)/Z for supplied coefficients.
    a,b,z = Q(3),Q(2),Q(5)
    mass2 = {str(k): str((a+b*k)/z) for k in eigenvalues}
    assert {str(k):str((7*a+7*b*k)/(7*z)) for k in eigenvalues} == mass2
    mass2_scaled = {str(k):str((7*a+7*b*k)/z) for k in eigenvalues}
    assert mass2_scaled != mass2
    assert ((a+b*12)/z - a/z) / ((a+b*6)/z - a/z) == 2
    return {
        "laplacian_spectrum_multiplicity":{str(k):v for k,v in eigenvalues.items()},
        "supplied_coefficients":{"a":str(a),"b":str(b),"Z":str(z)},
        "conditional_mode_omega_squared":mass2,
        "rescaling_degeneracy_example":"(a,b,Z)->(7a,7b,7Z) leaves every omega^2 unchanged",
        "variable_physical_spectrum_example":"(a,b,Z)->(7a,7b,Z) multiplies every omega^2 by seven",
        "mass2_scaled_by_seven":mass2_scaled,
        "conditional_excitation_gap_ratio":"2",
        "graph_side_identifiable_from_mode_spectrum":False,
        "physical_absolute_scale_derived":False,
    }


def build():
    out = {
        "status":"Exact finite checks/necessary conditions; NO physical TOE completion",
        "prior":{"point_line":"w33_20260924_history_pointline_cospectral_firewall.py",
                 "transport":"w33_20261008_dual_27_electrical_transport.py",
                 "CP":"w33_pass10952_clock_complete_positivity_firewall.py / w33_pass11038_spread_instrument_cp_firewall.py",
                 "gravity":"w33_pass11672_11679_native_dynamics_index.py / w33_pass11639 metric-cycle obstruction",
                 "chirality":"w33_pass11697_11698_chirality_vacuum.py",
                 "vacuum":"PASS11750_11757_INTEGRAL_GEOMETRY_AND_FLUX_DYNAMICS.md",
                 "normalization":"PASS11734_11741_GAUGING_AND_CHIRAL_QUOTIENT.md"},
        "quantum_channel":cp_walk_frontier(),
        "gravity_constraint":constraint_frontier(),
        "chirality":chirality_frontier(),
        "heterotic_operator_filter":vacuum_frontier(),
        "normalization":normalization_frontier(),
    }
    return out


def main():
    out = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print("FIVE_FRONTIERS_PASS")
    for key in ("quantum_channel","gravity_constraint","chirality",
                "heterotic_operator_filter","normalization"):
        print(key, json.dumps(out[key],sort_keys=True))
    return out


if __name__ == "__main__":
    main()
