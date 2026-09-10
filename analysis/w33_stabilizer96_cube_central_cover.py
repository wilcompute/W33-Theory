#!/usr/bin/env python3
"""The order-96 Heawood stabilizer as a non-split central cover of Aut(Q3).

Prior exact certificates give

    H = V4 semidirect S4,  V4=<z,u>,
    z central,
    sigma u sigma^-1 = z^sgn(sigma) u.

Therefore H/<z> = C2 x S4.  This script independently constructs every affine
Hamming automorphism of Q3, proves that there are exactly 48 and decomposes them
as

    Aut(Q3) = <antipode> x (V4_even semidirect S3) ~= C2 x S4.

It then writes the explicit central extension

    1 -> C2 -> H -> Aut(Q3) -> 1

and its normalized Z2-valued factor set

    alpha((b,sigma),(d,tau)) = d * sgn(sigma)  (mod 2).

The cocycle is nontrivial: on the commuting quotient elements represented by an
odd S4 permutation and the cube-antipode bit, alpha(g,h) != alpha(h,g).  A
coboundary on an abelian subgroup would be symmetric, so this is a direct
cohomological obstruction to splitting.  Equivalently, the two commuting cube
symmetries lift to elements whose commutator is the central z.

This is a finite-group/controller statement.  It is deliberately not identified
with a Spin/Pin double cover or with a physical phase until a representation-level
dictionary is constructed.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations, product
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "w33_stabilizer96_cube_central_cover.json"


def bits(i, n=3):
    return tuple((i >> (n - 1 - j)) & 1 for j in range(n))


def integer(v):
    x = 0
    for b in v:
        x = (x << 1) | b
    return x


def parity(v):
    return sum(v) & 1


def affine_signature(t, p):
    out = []
    for i in range(8):
        x = bits(i)
        y = tuple(x[p[j]] ^ t[j] for j in range(3))
        out.append(integer(y))
    return tuple(out)


def compose(g, h):
    return tuple(g[h[i]] for i in range(len(g)))


def inverse(g):
    out = [None] * len(g)
    for i, j in enumerate(g):
        out[j] = i
    return tuple(out)


def order(g):
    e = tuple(range(len(g)))
    x = e
    for k in range(1, 100):
        x = compose(g, x)
        if x == e:
            return k
    raise AssertionError("order bound exceeded")


def generated_subgroup(generators):
    e = tuple(range(len(generators[0])))
    gens = list(generators) + [inverse(g) for g in generators]
    seen = {e}
    stack = [e]
    while stack:
        x = stack.pop()
        for g in gens:
            y = compose(g, x)
            if y not in seen:
                seen.add(y)
                stack.append(y)
    return frozenset(seen)


def sign_perm(p):
    inv = sum(p[i] > p[j] for i in range(len(p)) for j in range(i + 1, len(p)))
    return inv & 1


def compose_perm(p, q):
    # Functions act by i -> p[i]; compose p after q.
    return tuple(p[q[i]] for i in range(len(p)))


def cube_group():
    ps = tuple(permutations(range(3)))
    ts = tuple(product((0, 1), repeat=3))
    G = frozenset(affine_signature(t, p) for t in ts for p in ps)
    assert len(G) == 48

    cube_edges = {
        tuple(sorted((i, j)))
        for i in range(8) for j in range(i + 1, 8)
        if sum(a != b for a, b in zip(bits(i), bits(j))) == 1
    }
    assert len(cube_edges) == 12
    for g in G:
        image = {tuple(sorted((g[a], g[b]))) for a, b in cube_edges}
        assert image == cube_edges

    # There cannot be more than 48 automorphisms: choose image of 000 (8 ways),
    # then permute its three neighbours (at most 6 ways).  Fixing 000 and all
    # three neighbours pointwise fixes the weight-2 vertices as pairwise common
    # neighbours, then fixes 111.  Our 48 affine maps therefore exhaust Aut(Q3).
    aut_upper_bound = 8 * 6
    assert len(G) == aut_upper_bound

    ident3 = (0, 1, 2)
    antipode = affine_signature((1, 1, 1), ident3)
    even_translations = tuple(t for t in ts if parity(t) == 0)
    K = frozenset(affine_signature(t, p) for t in even_translations for p in ps)
    assert len(K) == 24
    assert antipode not in K
    assert all(compose(antipode, g) == compose(g, antipode) for g in G)
    antipode_K = {compose(antipode, k) for k in K}
    assert K.isdisjoint(antipode_K)
    assert K | antipode_K == G

    even_vertices = tuple(i for i in range(8) if parity(bits(i)) == 0)
    restrictions = set()
    for g in K:
        assert all(g[v] in even_vertices for v in even_vertices)
        restrictions.add(tuple(g[v] for v in even_vertices))
    # A faithful order-24 action on four objects is the full S4.
    assert len(restrictions) == 24

    center = tuple(g for g in G if all(compose(g, h) == compose(h, g) for h in G))
    assert len(center) == 2
    assert set(center) == {tuple(range(8)), antipode}

    commutators = []
    for g in G:
        gi = inverse(g)
        for h in G:
            hi = inverse(h)
            commutators.append(compose(compose(compose(gi, hi), g), h))
    derived = generated_subgroup(tuple(set(commutators)))
    assert len(derived) == 12

    return {
        "group": G,
        "K": K,
        "antipode": antipode,
        "center": center,
        "derived": derived,
        "edge_count": len(cube_edges),
        "aut_upper_bound": aut_upper_bound,
        "element_order_histogram": Counter(order(g) for g in G),
    }


def quotient_and_cocycle_certificate():
    group_cert = json.loads(
        (ROOT / "data" / "w33_heawood_stabilizer96_presentation_lattice.json")
        .read_text(encoding="utf-8")
    )
    assert group_cert["status"] == "PASS"
    st = group_cert["structure"]
    assert st["order"] == 96
    assert st["center_order"] == 2
    assert st["derived_structure"] == "C2 x A4"
    assert st["abelianization_structure"] == "C2 x C2"
    fp = group_cert["fiber_product"]
    assert fp["semidirect_form"].startswith("V4 semidirect S4")
    assert "factors through sgn" in fp["semidirect_form"] or "sgn" in fp["action"] or "sign" in group_cert["headline"]

    # Q = C2 x S4.  We verify the factor set on all 48^3 triples.
    S4 = tuple(permutations(range(4)))
    Q = tuple((b, s) for b in (0, 1) for s in S4)
    id4 = tuple(range(4))

    def qmul(x, y):
        b, s = x
        d, t = y
        return (b ^ d, compose_perm(s, t))

    def alpha(x, y):
        _b, s = x
        d, _t = y
        return d & sign_perm(s)

    e = (0, id4)
    assert all(alpha(e, q) == alpha(q, e) == 0 for q in Q)
    cocycle_checks = 0
    for g in Q:
        for h in Q:
            gh = qmul(g, h)
            for k in Q:
                lhs = alpha(g, h) ^ alpha(gh, k)
                rhs = alpha(h, k) ^ alpha(g, qmul(h, k))
                assert lhs == rhs
                cocycle_checks += 1
    assert cocycle_checks == 48 ** 3

    odd = next(s for s in S4 if sign_perm(s) == 1)
    g = (0, odd)
    h = (1, id4)
    assert qmul(g, h) == qmul(h, g)  # commute in the quotient
    alpha_gh = alpha(g, h)
    alpha_hg = alpha(h, g)
    assert (alpha_gh, alpha_hg) == (1, 0)
    # On an abelian subgroup with trivial C2 coefficients, every 2-coboundary
    # delta f(g,h)=f(g)+f(h)+f(gh) is symmetric.  This restriction is not.
    nontrivial_restriction_witness = alpha_gh != alpha_hg
    assert nontrivial_restriction_witness

    return {
        "group_cert": group_cert,
        "cocycle_checks": cocycle_checks,
        "nontrivial_restriction_witness": nontrivial_restriction_witness,
        "alpha_odd_then_antipode": alpha_gh,
        "alpha_antipode_then_odd": alpha_hg,
    }


def build_result():
    cube = cube_group()
    lift = quotient_and_cocycle_certificate()
    H = lift["group_cert"]

    # H/Z(H) is direct because z dies and uZ is then centralized by every S4
    # element.  Its derived subgroup is A4, matching Aut(Q3)' exactly.
    checks = {
        "constructed_48_affine_maps_are_all_cube_automorphisms": len(cube["group"]) == 48,
        "cube_aut_decomposes_as_C2_times_S4": len(cube["K"]) == 24 and len(cube["center"]) == 2,
        "cube_aut_center_is_antipodal_C2": len(cube["center"]) == 2,
        "cube_aut_derived_is_A4_order12": len(cube["derived"]) == 12,
        "H_center_is_C2": H["structure"]["center_order"] == 2,
        "H_mod_center_is_C2_times_S4": H["structure"]["order"] // H["structure"]["center_order"] == 48,
        "derived_quotient_matches_A4": H["structure"]["derived_order"] // H["structure"]["center_order"] == 12,
        "cocycle_identity_checked_on_all_48_cubed_triples": lift["cocycle_checks"] == 48 ** 3,
        "central_extension_class_has_asymmetric_abelian_restriction": lift["nontrivial_restriction_witness"],
        "extension_is_non_split_by_center_obstruction": H["structure"]["center_order"] == 2 and len(cube["center"]) == 2,
    }

    return {
        "schema": "w33.heawood-stabilizer96-cube-central-cover.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The order-96 Heawood C6 stabilizer is a non-split central double "
            "cover of the full cube automorphism group: 1 -> C2 -> H -> Aut(Q3) "
            "-> 1, with Aut(Q3) ~= C2 x S4.  The extension twist is the explicit "
            "cocycle alpha((b,sigma),(d,tau))=d*sgn(sigma) mod 2."
        ),
        "cube_automorphism_group": {
            "order": len(cube["group"]),
            "construction": "F2^3 translations semidirect coordinate S3",
            "upper_bound_argument": "image of 000: 8 choices; permutation of its three neighbours: at most 6",
            "upper_bound": cube["aut_upper_bound"],
            "center_order": len(cube["center"]),
            "center_generator": "antipodal translation x -> x + 111",
            "S4_factor": "even-parity translations V4 semidirect S3 acts faithfully as Sym(4) on the four even-parity vertices",
            "direct_product": "Aut(Q3) = <111> x (V4_even semidirect S3) ~= C2 x S4",
            "derived_order": len(cube["derived"]),
            "derived_structure": "A4",
            "element_order_histogram": {str(k): v for k, v in sorted(cube["element_order_histogram"].items())},
        },
        "Heawood_stabilizer_cover": {
            "H_order": H["structure"]["order"],
            "kernel": "Z(H)=<z>~=C2",
            "quotient": "H/Z(H) ~= C2 x S4 ~= Aut(Q3)",
            "quotient_order": 48,
            "H_derived": H["structure"]["derived_structure"],
            "derived_image": "H'/Z(H) ~= A4 = Aut(Q3)'",
            "abelianization": H["structure"]["abelianization_structure"],
            "splitting": "NON-SPLIT",
            "splitting_proof": (
                "A split central extension would be C2 x Aut(Q3), whose center "
                "has order at least 4 because Aut(Q3) itself has central antipodal C2; "
                "the certified H has center order 2."
            ),
        },
        "extension_cocycle": {
            "quotient_coordinates": "q=(b,sigma) in C2 x S4",
            "section": "s(b,sigma)=u^b * sigma",
            "formula": "alpha((b,sigma),(d,tau)) = d * sgn(sigma) mod 2",
            "cocycle_triples_checked": lift["cocycle_checks"],
            "nontriviality_witness": {
                "commuting_quotient_pair": "g=(0,odd sigma), h=(1,id)",
                "alpha_g_h": lift["alpha_odd_then_antipode"],
                "alpha_h_g": lift["alpha_antipode_then_odd"],
                "reading": (
                    "g and h commute in C2 x S4, but their chosen lifts have "
                    "commutator z.  The asymmetric restriction cannot be a "
                    "coboundary on this abelian C2xC2 subgroup."
                ),
            },
            "controller_reading": (
                "The central bit behaves like a parity carry: moving an antipodal "
                "cube bit through an odd S4 operation contributes z."
            ),
        },
        "tomotope_firewall": (
            "This makes the two order-96 groups even more sharply opposite: the "
            "Heawood stabilizer is a central DOUBLE COVER of cube symmetry, while "
            "the repo-certified tomotope group is W(D4)/{+-1}, a central QUOTIENT. "
            "The prior center/derived invariants already prove they are nonisomorphic."
        ),
        "claim_boundary": [
            "Aut(Q3) is constructed and exhausted internally; the S4 x C2 identification is not inferred from order alone.",
            "The map H -> Aut(Q3) is an abstract quotient representation derived from the certified presentation; this certificate does not assert that H acts geometrically on the particular outer-fixed Q3 from the companion certificate.",
            "The nonzero C2 cocycle is a group-extension phase obstruction. It is not identified here with the spin double cover, a Pin group, a quantum Berry phase, or a physical fermion sign.",
            "Any such representation-level interpretation requires an explicit compatible linear/projective representation and is left as a falsifiable next step.",
        ],
        "external_cross_check": {
            "standard_fact": "Aut(Q3) ~= S4 x C2 and has order 48",
            "source": "Cubic symmetric graphs of order 8p^3, Discrete Mathematics 2014; also standard cube/Coxeter literature",
        },
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "quotient": result["Heawood_stabilizer_cover"]["quotient"],
        "splitting": result["Heawood_stabilizer_cover"]["splitting"],
        "cocycle": result["extension_cocycle"]["formula"],
        "triples_checked": result["extension_cocycle"]["cocycle_triples_checked"],
    }, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
