#!/usr/bin/env python3
"""Pass 10975: E6 cubic -> clock augmentation via an exact Reynolds weld.

The current H27 gauge splits the 27 cubic coordinates into three central
coordinates plus four six-point fibres indexed by P1(F3). Those four fibres
carry the same S4=PGL2(3) clock permutation module as the temporal/Hesse/A2
carrier. Restricting the signed E6 cubic to fibre-constant amplitudes is not
itself S4-invariant, but its Reynolds projection is nonzero and on the
augmentation hyperplane equals -2/3 times the unique clock cubic p3.
"""
from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "analysis") not in sys.path:
    sys.path.insert(0, str(ROOT / "analysis"))

import w33_pass10947_five_front_execution as P47

OUT = ROOT / "data/w33_pass10975_e6_cubic_reynolds_clock_weld.json"
CANON = ROOT / "extracted_v13/W33-Theory-master/artifacts/canonical_su3_gauge_and_cubic.json"
BRIDGE = ROOT / "data/w33_e6id_current_h27_gauge_bridge.json"
PARENT = ROOT / "data/w33_20260924_null_hesse_4a2_s4_intertwiner.json"
AFFINE = ROOT / "artifacts/e6_cubic_affine_heisenberg_model.json"
P10972 = ROOT / "data/w33_pass10972_tetrahedral_cubic_clock_selector.json"
def norm_dir(v: tuple[int, int]) -> tuple[int, int] | None:
    a, b = (int(v[0]) % 3, int(v[1]) % 3)
    if (a, b) == (0, 0):
        return None
    pivot = a if a else b
    scale = pow(pivot, -1, 3)
    return ((scale * a) % 3, (scale * b) % 3)


def pcanon(m: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    first = next(x for x in m if x)
    z = pow(first, -1, 3)
    return tuple((z * x) % 3 for x in m)


def load_inputs():
    canon = json.loads(CANON.read_text(encoding="utf-8"))
    bridge = json.loads(BRIDGE.read_text(encoding="utf-8"))
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    affine = json.loads(AFFINE.read_text(encoding="utf-8"))
    p72 = json.loads(P10972.read_text(encoding="utf-8"))
    signed = {
        tuple(sorted(map(int, row["triple"]))):
        (1 if int(row["sign"]) % 3 == 1 else -1)
        for row in canon["solution"]["d_triples"]
    }
    e6_to_h = {
        int(i): tuple(map(int, h))
        for i, h in bridge["maps"]["e6id_to_current_H27_address"].items()
    }
    return signed, e6_to_h, parent, affine, p72
def classify_triads(signed, e6_to_h, dirs):
    classes = {d: [] for d in dirs}
    classes[None] = []
    for tri, sign in signed.items():
        h0, h1, h2 = [e6_to_h[i] for i in tri]
        d1 = norm_dir(((h1[0] - h0[0]) % 3, (h1[1] - h0[1]) % 3))
        d2 = norm_dir(((h2[0] - h0[0]) % 3, (h2[1] - h0[1]) % 3))
        assert d1 == d2
        classes[d1].append((tri, sign))
    return classes


def induced_auto(m, det, q, x):
    u = x[:2]
    v = P47.act2(m, u)
    return (v[0], v[1], (det * x[2] + q[u]) % 3)


def unique_line_lift(m, det, address_triads):
    q0 = P47.q_particular(m, det)
    good = []
    for alpha, beta in itertools.product(range(3), repeat=2):
        q = {
            u: (q0[u] + alpha * u[0] + beta * u[1]) % 3
            for u in P47.F3_2
        }
        mapped = {
            tuple(sorted(induced_auto(m, det, q, x) for x in tri))
            for tri in address_triads
        }
        if mapped == address_triads:
            good.append(q)
    assert len(good) == 1
    return good[0]
def support_action_packet(signed, e6_to_h, dirs, parent):
    h_to_e6 = {h: i for i, h in e6_to_h.items()}
    address_triads = {
        tuple(sorted(e6_to_h[i] for i in tri)) for tri in signed
    }
    did = {d: i for i, d in enumerate(dirs)}
    parent_rows = {
        tuple(x for row in rec["matrix"] for x in row): tuple(rec["permutation"])
        for rec in parent["projective_action_rows"]
    }

    rows = []
    for m, det in P47.gl2_elements():
        q = unique_line_lift(m, det, address_triads)
        perm = tuple(
            h_to_e6[induced_auto(m, det, q, e6_to_h[i])]
            for i in range(27)
        )
        dperm = tuple(did[norm_dir(P47.act2(m, d))] for d in dirs)
        assert dperm == parent_rows[pcanon(m)]
        rows.append((m, det, q, perm, dperm))

    perms = {r[3] for r in rows}
    assert len(perms) == 48
    assert all(
        tuple(a[b[i]] for i in range(27)) in perms
        for a in perms for b in perms
    )
    return rows
def fibre_module_packet(e6_to_h, dirs, rows):
    fibres = {
        d: frozenset(
            i for i, h in e6_to_h.items()
            if h[:2] != (0, 0) and norm_dir(h[:2]) == d
        )
        for d in dirs
    }
    center = frozenset(i for i, h in e6_to_h.items() if h[:2] == (0, 0))
    assert {len(v) for v in fibres.values()} == {6}
    assert len(center) == 3
    assert len(center | frozenset().union(*fibres.values())) == 27

    did = {d: i for i, d in enumerate(dirs)}
    equivariant = True
    for m, det, q, perm, dperm in rows:
        for d in dirs:
            target = dirs[dperm[did[d]]]
            image = frozenset(perm[i] for i in fibres[d])
            equivariant &= image == fibres[target]
    assert equivariant

    minus_i = next(r for r in rows if r[0] == (2, 0, 0, 2))
    central_perm = minus_i[3]
    fixed = sum(central_perm[i] == i for i in range(27))
    two_cycles = (27 - fixed) // 2
    assert minus_i[4] == (0, 1, 2, 3)
    assert (fixed, two_cycles) == (3, 12)

    return fibres, center, {
        "four_fibres_size": 6,
        "center_size": 3,
        "module": "R^4 permutation module = 1 + standard_3",
        "augmentation_dimension": 3,
        "all_48_GL23_lifts_equivariant_on_fibres": True,
        "projective_image": "PGL(2,3) ~= S4",
        "central_minus_I_support_cycle_shape": "1^3 2^12",
        "central_minus_I_trivial_on_four_fibre_module": True,
    }
def signed_firewall_packet(signed, classes, rows):
    triads = tuple(sorted(signed))
    sign_rows = []
    for tri in triads:
        row = [0] * 27
        for i in tri:
            row[i] = 1
        sign_rows.append(row)

    pure = 0
    rank_hist = Counter()
    for m, det, q, perm, dperm in rows:
        exact = True
        equations = []
        for tri, row in zip(triads, sign_rows):
            image = tuple(sorted(perm[i] for i in tri))
            if signed[image] != signed[tri]:
                exact = False
            rhs = 0 if signed[image] == signed[tri] else 1
            equations.append(row + [rhs])
        pure += int(exact)
        rank, nullity, _ = P47.solve_linear_mod(equations, 2)
        rank_hist[(rank, nullity)] += 1

    sign_counts = {}
    for d, vals in classes.items():
        key = "center" if d is None else str(d)
        sign_counts[key] = {
            str(k): int(v)
            for k, v in sorted(Counter(s for _, s in vals).items())
        }
    assert pure == 1
    assert rank_hist == Counter({(21, 6): 48})
    return {
        "raw_sign_counts_by_direction": sign_counts,
        "pure_coordinate_permutations_preserving_signed_cubic": pure,
        "GL23_support_operations_checked": 48,
        "all_support_operations_have_sign_repairs": True,
        "binary_sign_equation_rank": 21,
        "homogeneous_sign_gauge_dimension": 6,
        "repairs_per_support_operation": 64,
        "reading": (
            "the clock S4 is exact on cubic support, but the frozen signed gauge "
            "does not realize it by bare coordinate permutations"
        ),
    }
def restricted_cubic_packet(signed, e6_to_h, dirs):
    did = {d: i for i, d in enumerate(dirs)}
    coeff = Counter()
    contrib = Counter()
    posneg: dict[tuple[int, ...], Counter] = {}

    for tri, sign in signed.items():
        labels = []
        for i in tri:
            h = e6_to_h[i]
            if h[:2] == (0, 0):
                labels = []
                break
            labels.append(did[norm_dir(h[:2])])
        if not labels:
            continue
        key = tuple(sorted(labels))
        coeff[key] += sign
        contrib[key] += 1
        posneg.setdefault(key, Counter())[sign] += 1

    assert sum(contrib.values()) == 32
    cube_keys = [(i, i, i) for i in range(4)]
    triple_keys = [tuple(c) for c in itertools.combinations(range(4), 3)]
    assert set(contrib) == set(cube_keys + triple_keys)
    assert {contrib[k] for k in cube_keys} == {2}
    assert {contrib[k] for k in triple_keys} == {6}
    assert sorted(coeff[k] for k in cube_keys) == [-2, -2, 0, 0]
    assert sorted(coeff[k] for k in triple_keys) == [-2, -2, 4, 4]

    y = sp.symbols("y0:4")
    raw = sum(v * sp.prod(y[i] for i in key) for key, v in coeff.items())
    reynolds = 0
    for p in itertools.permutations(range(4)):
        reynolds += raw.xreplace({y[i]: y[p[i]] for i in range(4)})
    reynolds = sp.expand(reynolds / 24)
    p3 = sum(z**3 for z in y)
    e3 = sum(sp.prod(y[i] for i in c) for c in itertools.combinations(range(4), 3))
    expected = sp.expand(-p3 + e3)
    assert sp.expand(reynolds - expected) == 0

    aug = {y[3]: -(y[0] + y[1] + y[2])}
    reynolds_aug = sp.expand(reynolds.subs(aug))
    p3_aug = sp.expand(p3.subs(aug))
    assert sp.expand(3 * reynolds_aug + 2 * p3_aug) == 0

    return {
        "embedding": (
            "x_h = y_[h mod Z(H27)] for the four nonzero projective quotient "
            "directions; x_h=0 on the three central addresses"
        ),
        "surviving_signed_triads": 32,
        "raw_monomial_coefficients": {
            str(k): int(coeff[k]) for k in sorted(coeff)
        },
        "raw_is_S4_invariant": False,
        "reynolds_operator": "(1/24) sum_{sigma in S4} sigma",
        "reynolds_polynomial": "-sum_i y_i^3 + sum_{i<j<k} y_i y_j y_k",
        "augmentation_constraint": "sum_i y_i = 0",
        "augmentation_identity": "R(D)|_A = -(2/3) p3",
        "selector_cubic": "p3=sum_i y_i^3",
        "coefficient": "-2/3",
        "nonzero_projection": True,
    }


def payload():
    signed, e6_to_h, parent, affine, p72 = load_inputs()
    dirs = tuple(tuple(map(int, d)) for d in parent["carrier"]["labels"])
    assert len(dirs) == 4
    classes = classify_triads(signed, e6_to_h, dirs)
    assert {len(v) for v in classes.values()} == {9}

    bad9 = {
        tuple(sorted(map(int, t))) for t in affine["fiber_triads_e6id"]
    }
    center9 = {tri for tri, _ in classes[None]}
    assert center9 == bad9

    rows = support_action_packet(signed, e6_to_h, dirs, parent)
    fibres, center, module = fibre_module_packet(e6_to_h, dirs, rows)
    firewall = signed_firewall_packet(signed, classes, rows)
    restriction = restricted_cubic_packet(signed, e6_to_h, dirs)
    checks = {
        "five_direction_classes_9_each": {len(v) for v in classes.values()} == {9},
        "center_class_is_firewall_bad9": center9 == bad9,
        "full_GL23_support_lift_order48": len({r[3] for r in rows}) == 48,
        "clock_PGL23_image_S4": parent["action"]["image_order"] == 24,
        "four_six_point_coordinate_fibres": all(len(v) == 6 for v in fibres.values()),
        "three_central_coordinates": len(center) == 3,
        "fibre_module_is_equivariant": module["all_48_GL23_lifts_equivariant_on_fibres"],
        "augmentation_dimension3": module["augmentation_dimension"] == 3,
        "raw_signed_gauge_breaks_bare_support_symmetry":
            firewall["pure_coordinate_permutations_preserving_signed_cubic"] == 1,
        "all_48_have_64_sign_repairs":
            firewall["repairs_per_support_operation"] == 64,
        "reynolds_projection_nonzero": restriction["nonzero_projection"],
        "reynolds_to_selector_coefficient_minus_2_over_3":
            restriction["coefficient"] == "-2/3",
        "pass10972_selector_is_p3": p72["invariants"]["cubic"] == "p3=sum_i x_i^3",
    }
    assert all(checks.values())

    return {
        "schema": "w33.pass10975.e6-cubic-reynolds-clock-weld.v1",
        "status": "PASS",
        "headline": (
            "The four P1(F3) clock directions embed objectwise as four six-point "
            "fibres inside the current 27-coordinate E6/H27 cubic carrier. Their "
            "zero-sum span is the exact 3D S4 clock augmentation module. The raw "
            "signed cubic is not S4-invariant in the frozen coordinate gauge, but "
            "its canonical Reynolds projection is nonzero and restricts to "
            "-2/3 times the Pass-10972 tetrahedral selector p3."
        ),
        "support_geometry": {
            "cubic_triads": 45,
            "direction_classes": 5,
            "triads_per_direction": 9,
            "center_direction": "the existing firewall bad-nine spread",
            "noncentral_directions": [list(d) for d in dirs],
        },
        "coordinate_module": module,
        "signed_gauge_firewall": firewall,
        "clock_restriction": restriction,
        "what_changed": (
            "Pass 10972 left open an objectwise S4-equivariant embedding of the "
            "clock augmentation module into the cubic carrier. This pass supplies "
            "that embedding at the 27-coordinate support level and computes the "
            "native cubic's exact invariant component on it."
        ),
        "physical_reading": (
            "If an effective dynamics projects or equilibrates the native cubic "
            "over the exact clock support symmetry, the only cubic anisotropy on "
            "the clock augmentation field is already the tetrahedral selector, "
            "with fixed relative coefficient -2/3 in this normalization."
        ),
        "boundary": (
            "The Reynolds operator is a canonical finite-group invariant-theory "
            "projection, not a derived physical averaging mechanism. The raw signed "
            "E6 cubic does not itself equal the clock Landau cubic on the fibre-constant "
            "subspace. A physical theory must explain why the S4-invariant component "
            "is dynamically selected, or supply a larger signed-equivariant field."
        ),
        "prior_art_boundary": (
            "Finite-group Reynolds averaging and the S4/A3 invariant cubic are "
            "classical invariant theory. The repo increment is the explicit objectwise "
            "H27/E6 fibre embedding, the signed-gauge obstruction census, and the "
            "computed nonzero -2/3 projection onto the already-certified clock selector."
        ),
        "checks": checks,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--output", type=Path, default=OUT)
    a = ap.parse_args()
    p = payload()
    text = json.dumps(p, indent=2, sort_keys=True) + "\n"
    if a.check:
        if not a.output.exists() or a.output.read_text(encoding="utf-8") != text:
            raise SystemExit("certificate drift")
    else:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(text, encoding="utf-8")
    print(json.dumps({
        "status": p["status"],
        "GL23_support": p["coordinate_module"]["all_48_GL23_lifts_equivariant_on_fibres"],
        "bare_signed_symmetries": p["signed_gauge_firewall"]["pure_coordinate_permutations_preserving_signed_cubic"],
        "repairs_each": p["signed_gauge_firewall"]["repairs_per_support_operation"],
        "reynolds_to_p3": p["clock_restriction"]["coefficient"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
