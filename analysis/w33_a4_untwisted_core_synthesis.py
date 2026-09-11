#!/usr/bin/env python3
"""A4 untwisted-core synthesis across the 84 codec and order-96 cover.

Three independently derived objects meet on the same four-label permutation
representation:

1. The boundary-Singer 84 bridge has local quotient

       (PG(2,4) x GF(4))/C7 ~= GF(4) x GF(4)^*,

   acting as AGL(1,4) on the four GF(4) labels.  Its 12 maps are exactly the 12
   even permutations, hence the standard A4 < S4.

2. The order-96 stabilizer presentation contains an explicit normal A4 section
   of order 12, with H'=C2 x A4 and preimage_A4=V4 x A4.

3. The cube-cover cocycle alpha((b,sigma),(d,tau))=d*sgn(sigma) vanishes whenever
   sigma is even.  Therefore the restriction to C2 x A4 is cohomologically
   trivial in the chosen section: the entire local A4 codec sits inside the
   untwisted parity firewall.  The central obstruction turns on only on extending
   from A4 to the odd S4 coset and coupling that parity to the antipodal C2 bit.

Thus the local 12-phase tetrahedral codec is not merely another order-12 object:
after the declared GF(4)/K4 labeling it is literally the even-permutation A4
appearing in the quotient cube symmetry and stabilizer normal lattice.
"""
from __future__ import annotations

from collections import Counter
from itertools import permutations
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_marcelis_gf4_trace_gauge import gf4_add, gf4_mul  # noqa: E402
from w33_stabilizer96_cube_central_cover import sign_perm  # noqa: E402

OUT = ROOT / "data" / "w33_a4_untwisted_core_synthesis.json"


def perm_order(p):
    cur = tuple(range(len(p)))
    ident = cur
    for n in range(1, 20):
        cur = tuple(p[cur[i]] for i in range(len(p)))
        if cur == ident:
            return n
    raise AssertionError("order bound")


def agl14():
    return {
        (a, d): tuple(gf4_add(gf4_mul(d, x), a) for x in range(4))
        for a in range(4) for d in (1, 2, 3)
    }


def build_result() -> dict:
    bridge = json.loads((ROOT / "data" / "w33_boundary_singer_toroidal_84_bridge.json").read_text(encoding="utf-8"))
    cocycle = json.loads((ROOT / "data" / "w33_cocycle_rank1_576_parity_firewall.json").read_text(encoding="utf-8"))
    group = json.loads((ROOT / "data" / "w33_heawood_stabilizer96_presentation_lattice.json").read_text(encoding="utf-8"))
    cover = json.loads((ROOT / "data" / "w33_stabilizer96_cube_central_cover.json").read_text(encoding="utf-8"))
    assert all(x["status"] == "PASS" for x in (bridge, cocycle, group, cover))

    maps = agl14()
    image = set(maps.values())
    even = {p for p in permutations(range(4)) if sign_perm(p) == 0}
    assert len(image) == len(even) == 12
    assert image == even
    assert Counter(perm_order(p) for p in image) == {1: 1, 2: 3, 3: 8}

    nodes = {n.get("name"): n for n in group["normal_subgroup_lattice"]["nodes"] if n.get("name")}
    A4node = nodes["A4_section"]
    Hprime = nodes["H_prime=C2_x_A4"]
    preA4 = nodes["preimage_A4=V4_x_A4"]
    assert A4node["order"] == 12
    assert A4node["element_order_histogram"] == {"1": 1, "2": 3, "3": 8}
    assert Hprime["order"] == 24
    assert preA4["order"] == 48

    assert bridge["local12"]["AGL14_order"] == 12
    assert bridge["local12"]["AGL14_element_order_histogram"] == {"1": 1, "2": 3, "3": 8}
    assert cocycle["parity_firewall"]["A4_size"] == 12
    assert cocycle["parity_firewall"]["C2_times_A4_size"] == 24
    assert cover["Heawood_stabilizer_cover"]["derived_image"] == "H'/Z(H) ~= A4 = Aut(Q3)'"

    # The local quotient acts sharply transitively on directed K4 edges; record
    # the regular A4 torsor structure explicitly.
    directed = {(u, v) for u in range(4) for v in range(4) if u != v}
    reference = (0, 1)
    orbit = {p: (p[0], p[1]) for p in image}
    assert set(orbit.values()) == directed and len(set(orbit.values())) == 12

    checks = {
        "AGL14_equals_even_permutation_A4_on_four_labels": image == even,
        "local12_order_spectrum_matches_A4_section": A4node["element_order_histogram"] == {"1": 1, "2": 3, "3": 8},
        "A4_section_is_order12_normal_lattice_node": A4node["order"] == 12,
        "derived_is_C2_times_A4_order24": Hprime["order"] == 24,
        "preimage_A4_is_V4_times_A4_order48": preA4["order"] == 48,
        "cocycle_firewall_contains_C2_times_A4": cocycle["parity_firewall"]["C2_times_A4_size"] == 24,
        "local_A4_is_sharply_transitive_on_12_directed_K4_edges": len(set(orbit.values())) == 12,
        "cube_cover_derived_image_is_A4": "A4" in cover["Heawood_stabilizer_cover"]["derived_image"],
        "boundary_bridge_local_group_is_AGL14": bridge["local12"]["AGL14_order"] == 12,
    }

    return {
        "schema": "w33.a4-untwisted-core-synthesis.v1",
        "status": "PASS" if all(checks.values()) else "PARTIAL",
        "headline": (
            "The 12 local phases of the C7-equivariant boundary/toroidal 84 codec are literally "
            "AGL(1,4)=A4 as the even permutations of the four affine labels.  This is the same "
            "A4 section appearing in the order-96 stabilizer and it lies completely inside the "
            "cocycle's untwisted parity firewall; the central twist begins only in the odd S4 coset."
        ),
        "same_four_label_A4": {
            "GF4_affine_maps": 12,
            "even_permutations_of_four_labels": 12,
            "sets_equal": image == even,
            "element_order_histogram": {str(k): v for k, v in sorted(Counter(perm_order(p) for p in image).items())},
            "directed_K4_edge_torsor": "A4 acts sharply transitively on the 12 ordered pairs u->v with u!=v",
        },
        "stabilizer_ladder": {
            "A4_section": {"order": A4node["order"], "node": A4node["id"]},
            "H_prime": {"order": Hprime["order"], "structure": "C2 x A4", "node": Hprime["id"]},
            "preimage_A4": {"order": preA4["order"], "structure": "V4 x A4", "node": preA4["id"]},
            "full_H": {"order": 96, "structure": "V4 semidirect S4"},
        },
        "twist_boundary": {
            "untwisted": "A4 and C2_antipode x A4: first S4 parity even implies alpha=0 against every second argument",
            "twisted_extension": "odd S4 parity couples to the second antipodal bit through alpha=d*sgn(sigma)",
            "reading": "The local tetrahedral codec is an exact untwisted core; the nontrivial central phase is an orientation-parity extension effect, not an intrinsic A4 effect.",
        },
        "codec_chain": "PG(2,4)xGF(4) --/C7--> AGL(1,4)=A4 --regularly--> 12 directed K4 edges --C7 lift--> 84 toroidal flags",
        "claim_boundary": [
            "Equality with the standard A4 is literal after the declared four-label GF(4) coordinate gauge: both are the same set of even permutations of {0,1,2,3}.",
            "The choice of that four-label gauge and Singer phase origin is not claimed canonical under the full ambient geometry.",
            "Untwisted refers to the certified Z2 group-extension cocycle; it is not a statement about absence of physical quantum phase.",
        ],
        "checks": checks,
    }


def main() -> int:
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "same_A4": result["same_four_label_A4"]["sets_equal"],
        "codec_chain": result["codec_chain"],
        "twist_boundary": result["twist_boundary"]["twisted_extension"],
    }, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
