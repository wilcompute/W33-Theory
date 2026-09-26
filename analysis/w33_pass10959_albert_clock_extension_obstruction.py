#!/usr/bin/env python3
"""Pass 10959: 16D Albert clock extension no-go and minimal 32D completion."""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as p51
import w33_pass10955_d4_halfspin_clock_bridge as p55

OUT = ROOT / "data/w33_pass10959_albert_clock_extension_obstruction.json"
JOUT = ROOT / "data/w33_pass10959_doubled_albert_gl23_intertwiner.json"


def smat(rows):
    return sp.Matrix([[sp.sympify(x) for x in row] for row in rows])


def strings(m):
    return [[str(sp.simplify(m[i, j])) for j in range(m.cols)]
            for i in range(m.rows)]


def sha_matrix(m):
    payload = json.dumps(strings(m), sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def block_embed(v, which):
    z = sp.zeros(16, 1)
    return sp.Matrix.vstack(v, z) if which == 0 else sp.Matrix.vstack(z, v)


def main():
    p58i = json.loads(
        (ROOT / "data/w33_pass10958_mu4_intertwiner_matrix.json")
        .read_text(encoding="utf-8"))
    w = smat(p58i["full_change_of_basis_W"])
    assert w.shape == (16, 16) and w.det() != 0

    mats = json.loads(
        (ROOT / "data/w33_pass10956_albert_spin8_exact_matrices.json")
        .read_text(encoding="utf-8"))
    u = smat(mats["halfturn_U_equals_R_over_2"])
    i16 = sp.eye(16)
    assert u * u == -i16

    zeta = (1 + sp.I) / sp.sqrt(2)
    assert sp.simplify(zeta ** 8 - 1) == 0
    g15 = sp.simplify((1 / zeta) * u)
    g37 = sp.simplify(zeta * u)

    for gg in (g15, g37):
        assert sp.simplify(gg ** 4 + i16) == sp.zeros(16)
        assert sp.simplify(gg ** 8 - i16) == sp.zeros(16)

    a2 = sp.diag(sp.I, -sp.I)
    a8 = sp.diag(*([a2] * 8))
    assert u * w == w * a8

    phase_lifts = {}
    for r in (1, 3, 5, 7):
        vals = sorted({(r + 2) % 8, (r + 6) % 8})
        phase_lifts[r] = vals
    assert set(tuple(v) for v in phase_lifts.values()) == {(1, 5), (3, 7)}

    # Frozen GAP restriction table; companion .g script recomputes it.
    irreps = [
        {"index": 1, "degree": 1, "center": 1, "exponents": [0]},
        {"index": 2, "degree": 1, "center": 1, "exponents": [4]},
        {"index": 3, "degree": 2, "center": 1, "exponents": [0, 4]},
        {"index": 4, "degree": 2, "center": -1, "exponents": [1, 3]},
        {"index": 5, "degree": 2, "center": -1, "exponents": [5, 7]},
        {"index": 6, "degree": 3, "center": 1, "exponents": [0, 2, 6]},
        {"index": 7, "degree": 3, "center": 1, "exponents": [4, 2, 6]},
        {"index": 8, "degree": 4, "center": -1, "exponents": [1, 3, 5, 7]},
    ]

    assert sum(x["degree"] ** 2 for x in irreps) == 48
    odd = [x for x in irreps if x["center"] == -1]
    assert [(x["degree"], x["exponents"]) for x in odd] == [
        (2, [1, 3]), (2, [5, 7]), (4, [1, 3, 5, 7])
    ]

    combos16 = []
    for a, b, c in itertools.product(range(9), repeat=3):
        if 2*a + 2*b + 4*c != 16:
            continue
        m = {1: a+c, 3: a+c, 5: b+c, 7: b+c}
        combos16.append({"a": a, "b": b, "c": c, "multiplicities": m})
    assert len(combos16) == 25

    target15 = {1: 8, 3: 0, 5: 8, 7: 0}
    target37 = {1: 0, 3: 8, 5: 0, 7: 8}
    assert not any(x["multiplicities"] == target15 for x in combos16)
    assert not any(x["multiplicities"] == target37 for x in combos16)
    assert all(
        x["multiplicities"][1] == x["multiplicities"][3]
        and x["multiplicities"][5] == x["multiplicities"][7]
        for x in combos16
    )


    def minimal_completion(target):
        hits = []
        for a, b, c in itertools.product(range(33), repeat=3):
            degree = 2*a + 2*b + 4*c
            if degree < 16 or degree > 64:
                continue
            m = {1: a+c, 3: a+c, 5: b+c, 7: b+c}
            if all(m[k] >= target[k] for k in target):
                hits.append((degree, a, b, c, m))
        d = min(x[0] for x in hits)
        return d, [x for x in hits if x[0] == d]

    d15, hits15 = minimal_completion(target15)
    d37, hits37 = minimal_completion(target37)
    assert d15 == d37 == 32
    assert any((a, b, c) == (0, 0, 8)
               for _, a, b, c, _ in hits15)
    assert any((a, b, c) == (0, 0, 8)
               for _, a, b, c, _ in hits37)

    gf3_clock = ((0, 1), (1, 1))
    rg = sp.Matrix(p55.signed_matrix(gf3_clock).tolist())
    assert rg ** 4 == -sp.eye(4)
    assert rg ** 8 == sp.eye(4)
    lam = sp.symbols("lambda")
    assert sp.expand(rg.charpoly(lam).as_expr() - (lam ** 4 + 1)) == 0


    exp_order = [1, 3, 5, 7]
    vcols = []
    for k in exp_order:
        ev = sp.simplify(zeta ** k)
        ns = (rg - ev * sp.eye(4)).nullspace()
        assert len(ns) == 1
        vcols.append(ns[0])
    t4 = sp.Matrix.hstack(*vcols)
    assert t4.det() != 0
    t32 = sp.diag(*([t4] * 8))

    scols = []
    for j in range(8):
        vp = w[:, 2*j]
        vm = w[:, 2*j + 1]
        scols.extend([
            block_embed(vp, 0),
            block_embed(vp, 1),
            block_embed(vm, 0),
            block_embed(vm, 1),
        ])
    s32 = sp.Matrix.hstack(*scols)
    assert s32.det() != 0

    ga = sp.diag(g15, g37)
    r32g = sp.diag(*([rg] * 8))
    jmat = sp.simplify(s32 * t32.inv())
    assert jmat.det() != 0
    assert sp.simplify(ga * jmat - jmat * r32g) == sp.zeros(32)


    z = ((2, 0), (0, 2))
    rz = sp.Matrix(p55.signed_matrix(z).tolist())
    assert rz == -sp.eye(4)
    r32z = sp.diag(*([rz] * 8))
    assert r32z == -sp.eye(32)

    p55c = json.loads(
        (ROOT / "data/w33_pass10955_d4_halfspin_clock_bridge.json")
        .read_text(encoding="utf-8"))
    emb = p55c["signed_permutation_embedding"]
    assert emb["faithful"] is True
    assert emb["all_48_squared_products_checked"] is True

    jout = {
        "schema": "w33.pass10959.doubled-albert-gl23-intertwiner.v1",
        "field": "Q(zeta8)=Q(i,sqrt(2))",
        "formula": "J = S32 T32^-1",
        "intertwiner_J": strings(jmat),
        "sha256": sha_matrix(jmat),
        "source_clock": "diag(zeta8^-1 U, zeta8 U)",
        "target_clock": "8 copies of the Pass10955 signed 4D clock matrix",
        "relation": "G_A J = J R32(g)",
    }
    JOUT.write_text(json.dumps(jout, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


    out = {
        "schema": "w33.pass10959.albert-clock-extension-obstruction.v1",
        "status": "PASS_16D_NOGO_AND_MINIMAL_32D_GL23_COMPLETION",
        "gap_character_restriction": {
            "group": "GL(2,3)",
            "order": 48,
            "clock_order": 8,
            "irrep_degrees": [x["degree"] for x in irreps],
            "center_minus_irreps": odd,
            "companion_gap_script":
                "analysis/w33_pass10959_gl23_character_restriction.g",
            "central_minus_restriction_law":
                "m1=m3 and m5=m7 for every representation with center acting as -I",
        },
        "albert_16_phase_lifts": {
            "U_spectrum": {"+i": 8, "-i": 8},
            "allowed_mu8_phase_exponents": [1, 3, 5, 7],
            "distinct_C8_spectra": {
                "zeta8^-1_times_U": target15,
                "zeta8_times_U": target37,
            },
            "fourth_power": "-I16",
            "eighth_power": "+I16",
        },
        "dimension16_no_go": {
            "central_minus_degree16_combinations": len(combos16),
            "all_exhausted": True,
            "target_15_extension_exists": False,
            "target_37_extension_exists": False,
            "obstruction":
                "Albert phase lifts violate m1=m3 and m5=m7, forced by every central-odd GL(2,3) character",
            "scope":
                "no complex-linear 16D GL(2,3) representation can both send central -I to -I16 and restrict g to any mu8 phase lift of the exact Albert halfturn U",
        },
        "minimal_completion": {
            "dimension": 32,
            "extra_dimension": 16,
            "complement_of_15": target37,
            "complement_of_37": target15,
            "doubled_clock": "diag(zeta8^-1 U, zeta8 U)",
            "combined_C8_multiplicities": {1: 8, 3: 8, 5: 8, 7: 8},
            "realization":
                "8 copies of the Pass10955 faithful 4D signed D4 representation",
            "faithful": True,
        },
        "explicit_32D_extension": {
            "field": "Q(zeta8)=Q(i,sqrt(2))",
            "intertwiner_rank": jmat.rank(),
            "intertwiner_sha256": sha_matrix(jmat),
            "clock_intertwining_exact": True,
            "center_maps_to": "-I32",
            "transport_formula":
                "rho_A(h)=J [R_4(h) direct-sum ... direct-sum R_4(h)] J^-1",
            "homomorphism_reason":
                "transport of the Pass10955 faithful GL(2,3) representation",
        },

        "parent_welds": {
            "pass10958":
                "one Albert 16 is eight copies of the missing diag(i,-i) C4 module",
            "new_result":
                "one 16D phase lift cannot extend, but the two conjugate mu8 phase lifts together form the minimal full GL(2,3) carrier",
            "doubling_reading":
                "the crossed odd-character pairing forces a second 16D Albert copy at the level of complex finite representation theory",
        },
        "theorem": (
            "The exact Albert halfturn U has two distinct mu8 phase-lift spectra "
            "compatible with the clock relation g^4=-I: eight copies of characters "
            "{1,5} or eight copies of {3,7}. GAP restriction of every irreducible "
            "character of GL(2,3) to the frozen C8 shows that all representations "
            "with central -I acting as -1 satisfy m1=m3 and m5=m7. Exhausting all "
            "25 central-odd degree-16 combinations therefore proves that neither "
            "Albert spectrum extends to GL(2,3) in 16 dimensions. The minimal "
            "completion has dimension 32: adjoining the conjugate Albert phase lift "
            "gives multiplicities 8 on each odd C8 character. This is exactly eight "
            "copies of the faithful 4D signed D4 representation, and an explicit "
            "Q(zeta8) intertwiner transports that full GL(2,3) action onto the "
            "doubled Albert carrier."
        ),

        "boundary": (
            "This is a complex finite-representation theorem. The transported 32D "
            "GL(2,3) action is not proved to lie inside Spin(9), preserve the Albert "
            "Jordan product, represent physical time, or describe a physical Dirac "
            "doubling. The 16D no-go applies only under the stated central-sign and "
            "clock-spectrum constraints."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "degree16_combinations": len(combos16),
        "minimal_dimension": 32,
        "J_rank": jmat.rank(),
        "J_sha256": sha_matrix(jmat),
    }, indent=2))


if __name__ == "__main__":
    main()
