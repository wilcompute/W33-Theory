#!/usr/bin/env python3
"""Pass 10957: mu4 Schur-cover converter.

Extract the exact section cocycle of GL(2,3)->S4 from the frozen clock
representation. Toggling it by the cup-square of permutation parity converts
the plus-cover cocycle to the minus-cover cocycle. The difference becomes a
coboundary after coefficients are enlarged from mu2 to mu4, using the
explicit cochain b(sigma)=i^epsilon(sigma).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "analysis"))
import w33_pass10951_clock_pin_spin_central_sign_bridge as P51

P46 = P51.p46
OUT = ROOT / "data/w33_pass10957_mu4_schur_cover_converter.json"
I2 = P51.I


def mkey(g):
    return tuple(x for row in g for x in row)


def parity(p):
    return sum(p[i] > p[j] for i in range(4)
               for j in range(i + 1, 4)) % 2
def main():
    gl = []
    for e in itertools.product(range(3), repeat=4):
        g = ((e[0], e[1]), (e[2], e[3]))
        if P46.det2(g):
            gl.append(g)
    assert len(gl) == 48

    # Central quotient and a deterministic section S4 -> GL(2,3).
    projective = {}
    for g in gl:
        p = P46.monomial_pullback(g)[0]
        projective.setdefault(p, []).append(g)
    assert len(projective) == 24
    assert all(len(v) == 2 for v in projective.values())
    S4 = sorted(projective)
    rep = {p: min(projective[p], key=mkey) for p in S4}

    def pmul(p, q):
        x = P51.mm(rep[p], rep[q])
        return P46.monomial_pullback(x)[0]

    def cplus(p, q):
        pq = pmul(p, q)
        x = P51.mm(rep[p], rep[q])
        if x == rep[pq]:
            return 0
        if x == P51.neg(rep[pq]):
            return 1
        raise AssertionError((p, q))

    cp = {(p, q): cplus(p, q) for p in S4 for q in S4}
    cm = {
        (p, q): cp[p, q] ^ (parity(p) & parity(q))
        for p in S4 for q in S4
    }
    # Both are normalized Z2 cocycles on the actual quotient multiplication.
    idp = P46.monomial_pullback(I2)[0]
    assert all(cp[idp, p] == cp[p, idp] == 0 for p in S4)
    assert all(cm[idp, p] == cm[p, idp] == 0 for p in S4)
    cocycle_checks = 0
    for a, b, c in itertools.product(S4, repeat=3):
        assert (cp[a, b] ^ cp[pmul(a, b), c]) == (
            cp[b, c] ^ cp[a, pmul(b, c)])
        assert (cm[a, b] ^ cm[pmul(a, b), c]) == (
            cm[b, c] ^ cm[a, pmul(b, c)])
        cocycle_checks += 1
    assert cocycle_checks == 24 ** 3

    elements = [(p, a) for p in S4 for a in (0, 1)]
    identity = (idp, 0)

    def emul(x, y, C):
        p, a = x
        q, b = y
        return pmul(p, q), a ^ b ^ C[p, q]

    def eorder(x, C):
        y = identity
        for n in range(1, 97):
            y = emul(y, x, C)
            if y == identity:
                return n
        raise AssertionError(x)

    def center(C):
        return [x for x in elements
                if all(emul(x, y, C) == emul(y, x, C) for y in elements)]
    plus_orders = Counter(eorder(x, cp) for x in elements)
    minus_orders = Counter(eorder(x, cm) for x in elements)
    plus_center = center(cp)
    minus_center = center(cm)
    assert plus_orders == Counter({2: 13, 8: 12, 3: 8, 6: 8,
                                  4: 6, 1: 1})
    assert minus_orders == Counter({4: 18, 8: 12, 3: 8, 6: 8,
                                   1: 1, 2: 1})
    assert plus_center == [identity, (idp, 1)]
    assert minus_center == [identity, (idp, 1)]

    # The plus extension is objectwise the original GL(2,3).
    def to_gl(x):
        p, a = x
        return rep[p] if a == 0 else P51.neg(rep[p])

    assert len({mkey(to_gl(x)) for x in elements}) == 48
    gl_hom_checks = 0
    for x, y in itertools.product(elements, repeat=2):
        assert to_gl(emul(x, y, cp)) == P51.mm(to_gl(x), to_gl(y))
        gl_hom_checks += 1
    assert gl_hom_checks == 48 ** 2

    # The cocycle difference is epsilon cup epsilon.
    difference_checks = 0
    for p, q in itertools.product(S4, repeat=2):
        assert (cp[p, q] ^ cm[p, q]) == (parity(p) & parity(q))
        difference_checks += 1
    assert difference_checks == 24 ** 2
    # Extend coefficients to mu4.  Write i^k by exponent k mod 4.
    # b_+(p)=i^epsilon(p), b_-(p)=(-i)^epsilon(p).
    # Their coboundary has exponent 2*epsilon(p)epsilon(q), exactly the
    # embedded mu2 cocycle difference.
    mu4_checks = 0
    for p, q in itertools.product(S4, repeat=2):
        ep, eq, epq = parity(p), parity(q), parity(pmul(p, q))
        delta_plus = (ep + eq - epq) % 4
        delta_minus = (-ep - eq + epq) % 4
        expected = 2 * (ep & eq)
        assert delta_plus == expected
        assert delta_minus == expected
        assert ((2 * cp[p, q] + delta_plus) % 4) == (2 * cm[p, q])
        mu4_checks += 1
    assert mu4_checks == 24 ** 2

    # Clock projective C4: the missing Pass10954 k=2,6 C8 characters descend
    # to the two square roots +/-i of the S4 sign character on this subgroup.
    g = ((0, 1), (1, 1))
    pclock = P46.monomial_pullback(g)[0]
    clock_powers = [idp]
    for _ in range(3):
        clock_powers.append(pmul(clock_powers[-1], pclock))
    assert pmul(clock_powers[-1], pclock) == idp
    assert len(set(clock_powers)) == 4
    parity_word = [parity(p) for p in clock_powers]
    assert parity_word == [0, 1, 0, 1]
    chi_plus_exp = [n % 4 for n in range(4)]
    chi_minus_exp = [(-n) % 4 for n in range(4)]
    assert [k % 2 for k in chi_plus_exp] == parity_word
    assert [k % 2 for k in chi_minus_exp] == parity_word
    p54 = json.loads(
        (ROOT / "data/w33_pass10954_regular_c8_clock_completion.json")
        .read_text(encoding="utf-8"))
    assert p54["compressed_clock"]["missing_character_exponents"] == [2, 6]
    assert p54["compressed_clock"]["missing_phase_values"] == ["+i", "-i"]

    p56 = json.loads(
        (ROOT / "data/w33_pass10956_albert_spin8_halfspin_normalizer.json")
        .read_text(encoding="utf-8"))
    assert p56["spin9_normalizer_halfturn"]["two_pi_equals_minus_I16_error"] < 1e-8

    p363 = json.loads(
        (ROOT / "data/w33_pass363_real_clifford_character_diamond.json")
        .read_text(encoding="utf-8"))
    corr = p363["correction"]
    assert corr["GL(2,3)"] == "SmallGroup(48,29), 13 involutions"
    assert corr["binary_octahedral_2O"] == "SmallGroup(48,28), 1 involution"
    assert corr["isomorphic"] is False

    table_bits = "".join(
        str(cp[p, q]) for p in S4 for q in S4)
    plus_sha = hashlib.sha256(table_bits.encode()).hexdigest()
    table_bits_m = "".join(
        str(cm[p, q]) for p in S4 for q in S4)
    minus_sha = hashlib.sha256(table_bits_m.encode()).hexdigest()
    out = {
        "schema": "w33.pass10957.mu4-schur-cover-converter.v1",
        "status": "PASS_MU4_SCHUR_COVER_CONVERTER",
        "clock_plus_cover": {
            "quotient": "S4=PGL(2,3)",
            "extension": "GL(2,3)=2^+S4",
            "section": "lexicographically minimal matrix in each +/-I pair",
            "cocycle_table_sha256": plus_sha,
            "cocycle_identity_checks": cocycle_checks,
            "objectwise_GL2_3_homomorphism_checks": gl_hom_checks,
            "order_spectrum": {str(k): v for k, v in sorted(plus_orders.items())},
            "involution_count": plus_orders[2],
            "center_order": len(plus_center),
            "smallgroup_crosscheck": "[48,29]",
        },
        "twisted_minus_cover": {
            "cocycle_formula":
                "c_minus(s,t)=c_plus(s,t)+epsilon(s)epsilon(t) mod 2",
            "cocycle_table_sha256": minus_sha,
            "difference_checks": difference_checks,
            "order_spectrum": {str(k): v for k, v in sorted(minus_orders.items())},
            "involution_count": minus_orders[2],
            "center_order": len(minus_center),
            "identification":
                "2^-S4 / binary-octahedral cover by one-involution fingerprint",
            "smallgroup_repo_crosscheck": "[48,28]",
        },
        "mu4_converter": {
            "cochains": {
                "plus": "b_+(sigma)=i^epsilon(sigma)",
                "minus": "b_-(sigma)=(-i)^epsilon(sigma)",
            },
            "all_pair_checks": mu4_checks,
            "coboundary":
                "delta b = (-1)^(epsilon(sigma)epsilon(tau))",
            "cohomology_statement":
                "the two distinct mu2 extension cocycles become cohomologous after coefficient inclusion mu2 -> mu4 subset U(1)",
            "abstract_group_boundary":
                "the 48-element central extensions remain nonisomorphic as abstract mu2 groups",
        },
        "clock_C4_square_root": {
            "projective_clock_order": 4,
            "permutation_parity_word": parity_word,
            "chi_plus_mu4_exponents": chi_plus_exp,
            "chi_minus_mu4_exponents": chi_minus_exp,
            "chi_plus_values": ["1", "i", "-1", "-i"],
            "chi_minus_values": ["1", "-i", "-1", "i"],
            "square_equals_sign_character": True,
            "pass10954_missing_C8_characters": [2, 6],
            "pass10954_missing_phase_values": ["+i", "-i"],
            "exact_reading":
                "the two missing C8 characters descend to the two mu4 square roots of sign on the projective clock C4",
        },
        "albert_cover_bridge": {
            "pass10956":
                "the natural Spin(9) half-turn exchanging 8_s and 8_c squares to the central -1, i.e. minus-cover-style local lifting",
            "clock":
                "the finite clock starts from the plus cover GL(2,3)",
            "resolution":
                "their Schur cocycles differ by epsilon cup epsilon and are projectively converted by the mu4 determinant-phase cochain",
            "remaining_gap":
                "no matrix intertwiner identifies the Pass10954 missing spectral modes with the Albert half-turn; the result is at cocycle/projective-representation level",
        },
        "theorem": (
            "The section cocycle of the frozen clock extension GL(2,3)->S4 is "
            "computed on all 24^2 pairs and verified on all 24^3 cocycle triples. "
            "Adding the parity cup-square epsilon(sigma)epsilon(tau) produces a "
            "second central extension with one involution and the binary-octahedral "
            "2^-S4 order spectrum, whereas the original has the GL(2,3)=2^+S4 "
            "spectrum with 13 involutions. The difference is the coboundary of "
            "b(sigma)=i^epsilon(sigma) after enlarging coefficients from mu2 to "
            "mu4, so the two nonisomorphic double covers define equivalent complex "
            "projective cocycles with that determinant-phase gauge. On the clock's "
            "projective C4, the two missing Pass10954 C8 characters k=2,6 are "
            "exactly the two mu4 characters taking the clock generator to +i and "
            "-i and squaring to permutation sign."
        ),
        "boundary": (
            "This is a finite group-cohomology and projective-representation theorem. "
            "It does not make the two 48-element groups isomorphic, identify the "
            "Pass10954 missing modes with an Albert physical degree of freedom, or "
            "construct a full matrix map from the order-eight clock into Spin(9)."
        ),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(json.dumps({
        "status": out["status"],
        "plus_involutions": plus_orders[2],
        "minus_involutions": minus_orders[2],
        "mu4_checks": mu4_checks,
        "clock_square_roots": out["clock_C4_square_root"]["pass10954_missing_phase_values"],
    }, indent=2))


if __name__ == "__main__":
    main()
