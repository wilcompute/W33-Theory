#!/usr/bin/env python3
"""Exact split-swap realization of the W33 order-576 stabilizer.

Let K=(2T x 2T)/diag(C2), where 2T=SL(2,3).  K acts faithfully on the
24 elements of 2T by left-right multiplication x -> a x b^{-1}; the diagonal
central pair is exactly the kernel.  Factor exchange (a,b)<->(b,a) is realized
on this 24-point carrier by inversion x -> x^{-1}.

This script adjoins that honest involution to K, obtaining K:C2 of order 576,
and constructs an explicit isomorphism from the W33 minimum-vector stabilizer
onto it.  The map carries the W33 oriented subgroup H+ exactly onto K and one
outer W33 involution exactly onto the inversion/factor-swap permutation.
All 576^2 multiplication identities are checked.
"""
from __future__ import annotations

import itertools
import json
from collections import Counter, deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = Path(__file__).resolve().parent
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_threeway_576_provenance_closure import (  # noqa: E402
    action_mats,
    compose,
    derived_subgroup,
    find_GL4_conjugator,
    find_complement_generators,
    generated_group,
    mapply,
    mcomp,
    minv,
    normal_form,
    pinv,
    porder,
    psp_minimum_stabilizer,
    quotient_E_coords,
    sha,
)
from w33_oriented288_binary_tetrahedral_bridge import (  # noqa: E402
    SL23,
    mmul,
    minv3,
)

OUT = ROOT / "data" / "w33_binary_tetrahedral_split_swap_completion.json"


def binary_tetrahedral_left_right_action():
    idx = {x: i for i, x in enumerate(SL23)}
    local = set()
    for a in SL23:
        for b in SL23:
            bi = minv3(b)
            local.add(tuple(idx[mmul(mmul(a, x), bi)] for x in SL23))
    assert len(local) == 288
    swap = tuple(idx[minv3(x)] for x in SL23)
    assert porder(swap) == 2
    full = generated_group(tuple(local) + (swap,), 24)
    assert len(full) == 576
    return local, swap, full


def build_result():
    local, swap, target = binary_tetrahedral_left_right_action()
    target_hist = dict(sorted(Counter(porder(g) for g in target).items()))
    expected = {1: 1, 2: 43, 3: 80, 4: 84, 6: 272, 12: 96}
    assert target_hist == expected

    H = psp_minimum_stabilizer()
    H1 = derived_subgroup(H, 40)
    H2 = derived_subgroup(H1, 40)
    assert len(H) == 576 and len(H1) == 96 and len(H2) == 32
    assert dict(sorted(Counter(porder(g) for g in H).items())) == expected

    T1 = derived_subgroup(target, 24)
    T2 = derived_subgroup(T1, 24)
    assert len(T1) == 96 and len(T2) == 32

    EH = quotient_E_coords(H2, 40)
    ET = quotient_E_coords(T2, 24)
    AH = action_mats(H, EH)
    AT = action_mats(target, ET)
    assert len(set(AH.values())) == len(set(AT.values())) == 18
    P = find_GL4_conjugator(set(AH.values()), set(AT.values()), EH["q"], ET["q"])
    assert P == (5, 10, 7, 9)

    relH, hgens, HC = find_complement_generators(H, AH, H2, 40)
    Pi = minv(P)
    targetM = tuple(mcomp(mcomp(P, A), Pi) for A in relH)
    opts = []
    for M, o in zip(targetM, (2, 3, 3)):
        opts.append([g for g, A in AT.items() if A == M and porder(g) == o])

    _, Hnf = normal_form(EH, H2, 40)
    target_cosets = [ET["invcoord"][mapply(P, 1 << i)] for i in range(4)]
    zT = ET["z"]
    eT = tuple(range(24))
    eH = tuple(range(40))
    phiE = None
    for toggles in itertools.product((0, 1), repeat=4):
        tb = []
        for i, c in enumerate(target_cosets):
            base = ET["cosets"][c][0]
            tb.append(compose(zT, base) if toggles[i] else base)
        tprod = {}
        for v in range(16):
            x = eT
            for i in range(4):
                if v & (1 << i):
                    x = compose(x, tb[i])
            tprod[v] = x
        phi = {}
        for h, (eps, v) in Hnf.items():
            phi[h] = compose(zT, tprod[v]) if eps else tprod[v]
        if len(set(phi.values())) < 32:
            continue
        if all(phi[compose(a, b)] == compose(phi[a], phi[b]) for a in H2 for b in H2):
            phiE = phi
            break
    assert phiE is not None

    def conj(g, x):
        return compose(compose(g, x), pinv(g))

    good_lists = []
    for hg, candidates in zip(hgens, opts):
        good = [tg for tg in candidates if all(phiE[conj(hg, x)] == conj(tg, phiE[x]) for x in H2)]
        assert good
        good_lists.append(good)

    tgens = None
    for s in good_lists[0]:
        for a in good_lists[1]:
            if compose(compose(s, a), s) != pinv(a):
                continue
            if len(generated_group((s, a), 24)) != 6:
                continue
            for b in good_lists[2]:
                if compose(b, s) != compose(s, b) or compose(b, a) != compose(a, b):
                    continue
                C = generated_group((s, a, b), 24)
                if len(C) == 18 and len(C & T2) == 1:
                    tgens = (s, a, b)
                    TC = C
                    break
            if tgens:
                break
        if tgens:
            break
    assert tgens is not None

    cmap = {eH: eT}
    queue = deque([eH])
    gpairs = []
    for a, b in zip(hgens, tgens):
        gpairs.extend(((a, b), (pinv(a), pinv(b))))
    while queue:
        h = queue.popleft()
        t = cmap[h]
        for a, b in gpairs:
            nh = compose(a, h)
            nt = compose(b, t)
            if nh not in cmap:
                cmap[nh] = nt
                queue.append(nh)
            else:
                assert cmap[nh] == nt
    assert len(cmap) == 18

    decomp = {}
    for ee in H2:
        for c in HC:
            x = compose(ee, c)
            assert x not in decomp
            decomp[x] = (ee, c)
    assert set(decomp) == H
    phi = {h: compose(phiE[ee], cmap[c]) for h, (ee, c) in decomp.items()}
    assert len(set(phi.values())) == 576 and set(phi.values()) == target
    assert all(phi[compose(a, b)] == compose(phi[a], phi[b]) for a in H for b in H)

    Hplus = generated_group(tuple(H1) + tuple(g for g in H if porder(g) == 3), 40)
    assert len(Hplus) == 288
    assert {phi[h] for h in Hplus} == local
    swap_preimage = [h for h in H if phi[h] == swap]
    assert len(swap_preimage) == 1 and porder(swap_preimage[0]) == 2

    # Directly verify the carrier model really implements factor exchange.
    for a in SL23:
        for b in SL23:
            bi = minv3(b)
            ai = minv3(a)
            left_right = tuple(
                {x: i for i, x in enumerate(SL23)}[mmul(mmul(a, x), bi)]
                for x in SL23
            )
            exchanged = tuple(
                {x: i for i, x in enumerate(SL23)}[mmul(mmul(b, x), ai)]
                for x in SL23
            )
            assert compose(compose(swap, left_right), swap) == exchanged

    checks = {
        "local_binary_tetrahedral_group_order_288": len(local) == 288,
        "factor_exchange_is_inversion_order2": porder(swap) == 2,
        "split_swap_completion_order_576": len(target) == 576,
        "split_swap_spectrum_equals_W33": target_hist == expected,
        "characteristic_extraspecial_kernels_order32": len(H2) == len(T2) == 32,
        "quotient_actions_order18": len(set(AH.values())) == len(set(AT.values())) == 18,
        "explicit_GL4_conjugator": P == (5, 10, 7, 9),
        "full_map_bijective": len(set(phi.values())) == 576,
        "all_576_squared_products_checked": True,
        "W33_oriented_288_maps_exactly_to_local_group": {phi[h] for h in Hplus} == local,
        "W33_outer_involution_maps_exactly_to_factor_swap": len(swap_preimage) == 1,
    }

    return {
        "schema": "w33.binary-tetrahedral-split-swap-completion.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "common_interior": {
            "group": "K_288 = (2T x 2T)/diag(C2)",
            "order": len(local),
            "carrier": "24 elements of 2T = SL(2,3)",
            "action": "(a,b): x -> a x b^{-1}",
        },
        "outer_swap": {
            "carrier_map": "x -> x^{-1}",
            "order": porder(swap),
            "conjugation": "inversion conjugates (a,b) to (b,a)",
        },
        "W33_completion": {
            "structure": "K_288 : C2 with honest factor swap",
            "order": len(target),
            "element_orders": target_hist,
            "oriented_subgroup_maps_to_K_288": True,
            "outer_swap_preimage_is_involution": True,
        },
        "explicit_isomorphism": {
            "GL4_conjugator_columns": list(P),
            "extraspecial_map_sha256": sha(sorted((str(k), str(v)) for k, v in phiE.items())),
            "full_map_sha256": sha(sorted((str(k), str(v)) for k, v in phi.items())),
            "full_576_squared_homomorphism_check": True,
        },
        "theorem": (
            "The W33 minimum-vector stabilizer is exactly the split factor-exchange completion "
            "of its binary-tetrahedral oriented subgroup: H_576 ~= ((2T x 2T)/diag(C2)) : C2, "
            "where the outer C2 is represented by inversion on the 24-element 2T carrier."
        ),
        "boundary": (
            "This is an exact finite-group theorem. It does not identify the outer involution with a "
            "physical SWAP gate until a Hilbert-space representation is specified."
        ),
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "order": result["W33_completion"]["order"],
        "GL4": result["explicit_isomorphism"]["GL4_conjugator_columns"],
        "oriented_exact": result["W33_completion"]["oriented_subgroup_maps_to_K_288"],
        "swap_exact": result["W33_completion"]["outer_swap_preimage_is_involution"],
    }, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
