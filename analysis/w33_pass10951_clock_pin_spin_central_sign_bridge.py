#!/usr/bin/env python3
"""Pass 10951: clock Pin/Spin central-sign bridge.

Separate det:GL(2,3)->C2 (the finite Pin-component/Hesse spinor-norm bit)
from the central element z=-I (the spin sign).  The Pass-10948 order-eight
clock lift is determinant-odd but has fourth power z.  We construct the
determinant-one subgroup explicitly as the binary tetrahedral group 2T in
unit quaternions and weld z to Pass 10950's 2pi Spin(9) matter-parity sign.
"""
from __future__ import annotations

import itertools
import json
import sys
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10946_clock_code_cone_objectwise as p46
import w33_pass10948_clock_tetracode_negacyclic_hyperbolic_bridge as p48

OUT = ROOT / "data/w33_pass10951_clock_pin_spin_central_sign_bridge.json"
I = ((1, 0), (0, 1))
Z = ((2, 0), (0, 2))
def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) % 3
                       for j in range(2)) for i in range(2))

def inv(a):
    d = p46.det2(a)
    di = pow(d, -1, 3)
    return ((di * a[1][1] % 3, -di * a[0][1] % 3),
            (-di * a[1][0] % 3, di * a[0][0] % 3))

def mpow(a, n):
    r = I
    for _ in range(n):
        r = mm(r, a)
    return r

def order(a):
    r = I
    for n in range(1, 49):
        r = mm(r, a)
        if r == I:
            return n
    raise AssertionError(a)

def neg(a):
    return tuple(tuple((-x) % 3 for x in row) for row in a)

def conj(a, b):
    return mm(mm(a, b), inv(a))
def parity(perm):
    inversions = sum(perm[i] > perm[j] for i in range(4)
                     for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1

def cycles(perm):
    seen = set()
    out = []
    for i in range(4):
        if i in seen:
            continue
        c = []
        j = i
        while j not in seen:
            seen.add(j)
            c.append(j)
            j = perm[j]
        if len(c) > 1:
            out.append(tuple(c))
    return tuple(out)

def qmul(q, r):
    a,b,c,d=q
    e,f,g,h=r
    return (a*e-b*f-c*g-d*h,
            a*f+b*e+c*h-d*g,
            a*g-b*h+c*e+d*f,
            a*h+b*g-c*f+d*e)

def qconj(q):
    return (q[0], -q[1], -q[2], -q[3])
QONE = (F(1), F(0), F(0), F(0))
QI = (F(0), F(1), F(0), F(0))
QJ = (F(0), F(0), F(1), F(0))
QK = qmul(QI, QJ)
QMINUS = (F(-1), F(0), F(0), F(0))
QW = (F(-1,2), F(-1,2), F(-1,2), F(-1,2))

def qorder(q):
    r = QONE
    for n in range(1, 25):
        r = qmul(r, q)
        if r == QONE:
            return n
    raise AssertionError(q)

def clock_action_in_frozen_gauge(word, signs):
    dword = tuple(signs[j] * word[j] % 3 for j in range(4))
    shifted = p48.negashift(dword)
    return tuple(signs[j] * shifted[j] % 3 for j in range(4))

def minpoly(a):
    tr = (a[0][0] + a[1][1]) % 3
    det = p46.det2(a)
    if (tr, det) == (1, 2):
        return "x^2-x-1"
    if (tr, det) == (2, 2):
        return "x^2+x-1"
    return f"x^2-{tr}x+{det} (mod 3)"
def main():
    gl = []
    for e in itertools.product(range(3), repeat=4):
        g = ((e[0], e[1]), (e[2], e[3]))
        if p46.det2(g):
            gl.append(g)
    sl = [g for g in gl if p46.det2(g) == 1]
    odd = [g for g in gl if p46.det2(g) == 2]
    assert len(gl) == 48 and len(sl) == len(odd) == 24
    repo_code = frozenset(p46.span(p46.STANDARD_TETRACODE_GENERATORS))

    gauges = {
        "plus": (1, 2, 1, 1),
        "minus": (1, 1, 1, 2),
    }
    lifts = {}
    for name, D in gauges.items():
        hits = []
        for g in gl:
            action = p46.monomial_pullback(g)
            if all(p46.apply_monomial(w, *action) ==
                   clock_action_in_frozen_gauge(w, D) for w in repo_code):
                hits.append(g)
        assert len(hits) == 1
        g = hits[0]
        perm, scales = p46.monomial_pullback(g)
        lifts[name] = dict(matrix=g, trace=(g[0][0]+g[1][1]) % 3,
                           det=p46.det2(g), order=order(g),
                           minimal_polynomial=minpoly(g),
                           projective_permutation=perm,
                           projective_cycles=cycles(perm),
                           monomial_scales=scales)
    gp = lifts["plus"]["matrix"]
    gm = lifts["minus"]["matrix"]
    assert gp == neg(gm)
    assert lifts["plus"]["minimal_polynomial"] == "x^2+x-1"
    assert lifts["minus"]["minimal_polynomial"] == "x^2-x-1"
    assert lifts["plus"]["projective_permutation"] == lifts["minus"]["projective_permutation"]
    assert len(lifts["plus"]["projective_cycles"][0]) == 4
    for g in (gp, gm):
        assert order(g) == 8
        assert p46.det2(g) == 2
        assert mpow(g, 4) == Z
        assert mpow(g, 8) == I
    projective = {}
    for g in gl:
        perm = p46.monomial_pullback(g)[0]
        projective.setdefault(perm, []).append(g)
        det_sign = 1 if p46.det2(g) == 1 else -1
        assert det_sign == parity(perm)
    assert len(projective) == 24
    assert set(len(v) for v in projective.values()) == {2}
    for pair in projective.values():
        assert set(pair) == {pair[0], neg(pair[0])}

    projective_types = Counter(
        (parity(p), tuple(sorted(map(len, cycles(p)))))
        for p in projective
    )
    expected_types = Counter({
        (1, ()): 1,
        (1, (2, 2)): 3,
        (1, (3,)): 8,
        (-1, (2,)): 6,
        (-1, (4,)): 6,
    })
    assert projective_types == expected_types
    total_orders = Counter((p46.det2(g), order(g)) for g in gl)
    expected_orders = Counter({
        (1,1):1, (1,2):1, (1,3):8, (1,4):6, (1,6):8,
        (2,2):12, (2,8):12,
    })
    assert total_orders == expected_orders

    q8 = [g for g in sl if order(g) in (1,2,4)]
    assert len(q8) == 8
    assert all(mm(a,b) in q8 for a in q8 for b in q8)
    assert [g for g in sl if order(g) == 2] == [Z]

    b = mpow(gm, 2)
    assert order(b) == 4
    assert mpow(b, 2) == Z
    found = None
    for a in q8:
        if order(a) != 4 or a in (b, neg(b)):
            continue
        k = mm(a, b)
        if order(k) != 4:
            continue
        for c in sl:
            if order(c) != 3:
                continue
            if conj(c,a)==b and conj(c,b)==k and conj(c,k)==a:
                found = (a,b,k,c)
                break
        if found:
            break
    assert found is not None
    a,b,k,c = found
    assert mm(a,b) == k
    assert mm(a,b) == neg(mm(b,a))
    assert qorder(QW) == 3
    assert qmul(qmul(QW,QI),qconj(QW)) == QJ
    assert qmul(qmul(QW,QJ),qconj(QW)) == QK
    assert qmul(qmul(QW,QK),qconj(QW)) == QI

    gens = ((a,QI), (b,QJ), (c,QW))
    phi = {I: QONE}
    queue = deque([I])
    while queue:
        x = queue.popleft()
        qx = phi[x]
        for mg,qg in gens:
            y = mm(x,mg)
            qy = qmul(qx,qg)
            if y in phi:
                assert phi[y] == qy
            else:
                phi[y] = qy
                queue.append(y)
    assert set(phi) == set(sl)
    assert len(set(phi.values())) == 24
    assert phi[Z] == QMINUS
    assert phi[b] == QJ
    for x in sl:
        for y in sl:
            assert phi[mm(x,y)] == qmul(phi[x],phi[y])
    old_spin = json.loads(
        (ROOT / "data/w33_hesse_nullcone_spinor_norm.json").read_text()
    )
    assert old_spin["checks"]["Omega_equals_SL2_projective_image_order12"] is True

    albert = json.loads(
        (ROOT / "data/w33_pass10950_clock_albert_lorentz_spinor.json").read_text()
    )
    matter = albert["matter_parity"]
    assert all(matter["peirce_symmetry_U_(2c-e)"].values())
    assert matter["two_pi_rotation_equals_U_s_max_error"] < 1e-8
    assert "2 pi rotation of Spin(9)" in matter["reading"]

    # The determinant C2 and the central spin C2 are not the same character.
    assert p46.det2(Z) == 1
    zperm,zscales = p46.monomial_pullback(Z)
    assert zperm == tuple(range(4))
    assert zscales == (2,2,2,2)
    assert mpow(gm,4) == Z

    def matlist(g):
        return [list(row) for row in g]

    def lift_record(row):
        return {
            "matrix": matlist(row["matrix"]),
            "trace_mod3": row["trace"],
            "det_mod3": row["det"],
            "order": row["order"],
            "minimal_polynomial": row["minimal_polynomial"],
            "projective_permutation": list(row["projective_permutation"]),
            "projective_cycles": [list(x) for x in row["projective_cycles"]],
            "monomial_scales": list(row["monomial_scales"]),
        }
    out = {
        "schema": "w33.pass10951.clock-pin-spin-central-sign-bridge.v1",
        "status": "PASS_CLOCK_PIN_SPIN_CENTRAL_SIGN_BRIDGE",
        "groups": {
            "GL2_3_order": len(gl),
            "SL2_3_order": len(sl),
            "center": "-I2",
            "center_order": 2,
            "projective_image_order": len(projective),
            "projective_image": "PGL(2,3) ~= S4",
            "spin_subgroup": "SL(2,3) ~= binary tetrahedral 2T",
            "spin_subgroup_order_spectrum": dict(
                sorted(Counter(order(g) for g in sl).items())
            ),
            "det_minus_coset_order_spectrum": dict(
                sorted(Counter(order(g) for g in odd).items())
            ),
            "schur_cover_type": "2^+ S4 = GL(2,3)",
        },
        "two_C2s": {
            "pin_component_character": {
                "map": "det: GL(2,3) -> F3^x = {+1,-1}",
                "kernel": "SL(2,3)",
                "projective_reading": "even/odd permutation of four clock rays",
                "repo_weld": "finite Hesse orthogonal spinor norm",
            },
            "central_spin_sign": {
                "element": "-I2",
                "determinant": 1,
                "projective_action": "identity",
                "clock_code_action": "global sign -1",
                "quaternion_image": "-1 in 2T subset Spin(3)",
                "spin_reading": "2pi rotation",
            },
            "independent_not_conflated": True,
        },
        "negacyclic_clock_lifts": {
            "plus": lift_record(lifts["plus"]),
            "minus": lift_record(lifts["minus"]),
        },
        "clock_power_ladder": {
            "g": matlist(gm),
            "g_minimal_polynomial": minpoly(gm),
            "g_order": 8,
            "g_is_pin_odd": True,
            "g_squared": matlist(b),
            "g_squared_quaternion_image": "j",
            "g_squared_reading": "order-4 Spin(3) lift of a pi rotation",
            "g_fourth": "-I2",
            "g_fourth_quaternion_image": "-1",
            "g_fourth_reading": "central 2pi spin rotation",
            "g_eighth": "+I2",
            "projective_period": 4,
            "spin_lift_period": 8,
        },
        "binary_tetrahedral_certificate": {
            "Q8_size": len(q8),
            "Q8_generator_a": matlist(a),
            "Q8_generator_b_clock_square": matlist(b),
            "C3_generator": matlist(c),
            "C3_cycles_quaternion_axes": True,
            "quaternion_group_size": len(set(phi.values())),
            "full_24_squared_homomorphism_check": True,
            "center_maps_to_quaternion_minus_one": phi[Z] == QMINUS,
        },
        "projective_cycle_census": {
            str((sgn, cy)): n
            for (sgn, cy), n in sorted(projective_types.items(), key=str)
        },
        "lift_order_census": {
            f"det{det}_order{ordr}": n
            for (det, ordr), n in sorted(total_orders.items())
        },
        "matter_parity_weld": {
            "pass10950_status": albert["status"],
            "pass10950_spin9_2pi_equals_peirce_symmetry": True,
            "pass10950_numerical_error":
                matter["two_pi_rotation_equals_U_s_max_error"],
            "central_chain":
                "-I2 in SL(2,3)=2T subset Spin(3) -> -1 in Spin(9)",
            "central_character_match":
                "clock -I2 is the finite spin sign; in Pass10950 the "
                "Spin(9) central 2pi sign is matter parity on the Peirce 16",
            "not_claimed":
                "No action of the full determinant-minus-one clock lift "
                "on the Albert 16 is constructed here.",
        },
        "theorem": (
            "The Pass10948 negacyclic shift is the unique GL(2,3) lift, "
            "in each of two oriented gauges, of one projective 4-cycle. "
            "The lifts are central negatives with minimal polynomials "
            "x^2+x-1 and x^2-x-1, order 8, determinant -1, common square "
            "in the quaternion Q8 inside SL(2,3), and fourth power -I. "
            "The determinant-one subgroup is explicitly isomorphic to the "
            "24 Hurwitz units 2T in Spin(3), sending -I to quaternion -1. "
            "Thus determinant gives the Pin-component/Hesse spinor-norm bit, "
            "while central -I gives the 2pi spin sign. Pass10950 realizes "
            "the latter as matter parity on the clock Albert 16."
        ),
        "boundary": (
            "Finite group and central-character theorem only. GL(2,3) is "
            "the plus Schur cover 2^+S4, not the binary octahedral 2^-S4. "
            "The shared central -1 does not construct physical time evolution, "
            "the action of every clock tick on matter, a continuum Pin bundle, "
            "or a chirality-selection mechanism."
        ),
    }
    OUT.write_text(
        json.dumps(out, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": out["status"],
        "clock_lift": matlist(gm),
        "g2": matlist(b),
        "g4": "-I2",
        "projective_cycle": [
            list(x) for x in lifts["minus"]["projective_cycles"]
        ],
        "SL23_to_2T": len(phi),
    }, indent=2))

if __name__ == "__main__":
    main()
