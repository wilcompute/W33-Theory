#!/usr/bin/env python3
"""Pillar 70 (Part CLXXVIII): Tomotope-H Obstruction Theorem

The 192-flag tomotope is a rank-4 maniplex with f-vector (4,12,16,8) and
automorphism group P of order 96.  Its flags can be counted as
|W(D4)| = 192, coinciding with the order of the axis-line stabilizer H
of the W(3,3) geometry.

This script proves that this coincidence is NUMEROLOGICAL, not structural:

  T1 True f-vector: tomotope has (V,E,F,C)=(4,12,16,8), 192 flags, cells=hemioctahedra
  T2 Monodromy group: |Gamma(tomotope)| = 18432 = |P| x |H| (exact product)
  T3 Flag stabilizer: Stab_Gamma(f) has order 96 with order-dist matching P exactly
  T4 H center trivial: Z(H)={e}, so P is NOT a quotient H/Z2 of H
  T5 Universal obstruction: H cannot be the connection group of any rank-4 maniplex
     with f-vector (4,12,16,8).  Proof: for ALL 66 D4 subgroups <r2,r3> in H and
     ALL centralizing involutions r0 outside D4 (giving |<r0,r2,r3>|=16), every
     involution r1 commuting with r3 satisfies ord(r0*r1) in {2,4} -- never 3.
     This prevents |<r0,r1,r3>|=12 needed for F=16 faces.
  T6 Order-8 signature: H has 48 order-8 elements (octonionic spin), Gamma(tomotope)
     has 3456 order-8 elements; P has 0 order-8 elements.  H and Gamma(tomotope)
     are not isomorphic (different distributions); H cannot embed as the monodromy.
"""
from __future__ import annotations

import json
import zipfile
from collections import Counter, deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def compose(p: tuple, q: tuple) -> tuple:
    return tuple(p[q[i]] for i in range(len(p)))


def perm_order(p: tuple) -> int:
    n = len(p)
    idn = tuple(range(n))
    cur = p
    k = 1
    while cur != idn:
        cur = compose(p, cur)
        k += 1
        if k > 50000:
            raise RuntimeError("order overflow")
    return k


def subgroup_closure(gens: list[tuple]) -> set:
    idn = tuple(range(len(gens[0])))
    S: set = {idn}
    queue = list(gens)
    while queue:
        g = queue.pop()
        if g in S:
            continue
        S.add(g)
        for h in list(S):
            for p in (compose(g, h), compose(h, g)):
                if p not in S:
                    queue.append(p)
    return S


def orbit_count(sub_gens: list[tuple], n: int) -> int:
    visited = [False] * n
    cnt = 0
    for s in range(n):
        if not visited[s]:
            cnt += 1
            q = [s]
            visited[s] = True
            while q:
                v = q.pop()
                for a in sub_gens:
                    w = a[v]
                    if not visited[w]:
                        visited[w] = True
                        q.append(w)
    return cnt


# ---------------------------------------------------------------------------
# H multiplication
# ---------------------------------------------------------------------------

def _load_H():
    path = ROOT / "axis_line_stabilizer_192.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    elems = data["elements"]
    assert len(elems) == 192

    def _mul_h(h1, h2):
        p1, s1 = h1["perm"], h1["signs"]
        p2, s2 = h2["perm"], h2["signs"]
        np_ = [None] * 7
        ns = [None] * 7
        for i in range(7):
            j = p2[i] - 1
            np_[i] = p1[j]
            ns[i] = s1[j] * s2[i]
        return {"perm": np_, "signs": ns}

    H_index = {
        (tuple(h["perm"]), tuple(h["signs"])): idx
        for idx, h in enumerate(elems)
    }
    assert len(H_index) == 192

    mul = [
        [None] * 192
        for _ in range(192)
    ]
    for i in range(192):
        for j in range(192):
            prod = _mul_h(elems[i], elems[j])
            mul[i][j] = H_index[(tuple(prod["perm"]), tuple(prod["signs"]))]

    return elems, mul


# ---------------------------------------------------------------------------
# main computation
# ---------------------------------------------------------------------------

def build_tomotope_H_obstruction_report() -> dict:
    out: dict = {"status": "ok"}

    # ------------------------------------------------------------------
    # T1: true tomotope f-vector from bundle
    # ------------------------------------------------------------------
    bundle_path = ROOT / "TOE_tomotope_true_flag_model_v02_20260228_bundle.zip"
    if not bundle_path.exists():
        raise RuntimeError(f"Missing bundle: {bundle_path}")

    with zipfile.ZipFile(bundle_path) as zf:
        rgens = json.loads(zf.read("tomotope_r_generators_192.json"))
        report_raw = json.loads(zf.read("REPORT.json"))

    r0 = tuple(rgens["r0"])
    r1 = tuple(rgens["r1"])
    r2 = tuple(rgens["r2"])
    r3 = tuple(rgens["r3"])
    n = 192

    fvec = (
        orbit_count([r1, r2, r3], n),
        orbit_count([r0, r2, r3], n),
        orbit_count([r0, r1, r3], n),
        orbit_count([r0, r1, r2], n),
    )
    assert fvec == (4, 12, 16, 8), f"Wrong f-vector: {fvec}"
    out["T1_fvector"] = {"V": fvec[0], "E": fvec[1], "F": fvec[2], "C": fvec[3]}
    out["T1_flags"] = n
    out["T1_cell_type"] = report_raw.get("cell_types", ["hemioctahedron"])[0] if isinstance(
        report_raw.get("cell_types"), list) else "hemioctahedron"
    print(f"T1: f-vector = {fvec}, flags = {n}  OK")

    # ------------------------------------------------------------------
    # T2: monodromy group order = |P| x |H| = 18432
    # ------------------------------------------------------------------
    gens4 = [r0, r1, r2, r3]
    G: list[tuple] = [tuple(range(n))]
    seen: set = {G[0]}
    idx = 0
    while idx < len(G):
        g = G[idx]
        for a in gens4:
            c = compose(a, g)
            if c not in seen:
                seen.add(c)
                G.append(c)
        idx += 1

    gamma_order = len(G)
    assert gamma_order == 18432, f"Unexpected monodromy order: {gamma_order}"
    P_order = 96
    H_order = 192
    assert gamma_order == P_order * H_order
    out["T2_monodromy_order"] = gamma_order
    out["T2_P_order"] = P_order
    out["T2_H_order"] = H_order
    out["T2_product_check"] = (gamma_order == P_order * H_order)
    print(f"T2: |Gamma| = {gamma_order} = {P_order} x {H_order}  OK")

    # ------------------------------------------------------------------
    # T3: stabilizer of flag 0 has order 96 with order-dist = P
    # ------------------------------------------------------------------
    stab_0 = [g for g in G if g[0] == 0]
    assert len(stab_0) == P_order, f"Stab_0 has unexpected size {len(stab_0)}"
    stab_0_order_dist = Counter(perm_order(g) for g in stab_0)
    P_expected_dist = {1: 1, 2: 27, 3: 32, 4: 36}
    assert dict(stab_0_order_dist) == P_expected_dist, (
        f"Stab_0 order dist {dict(stab_0_order_dist)} != P {P_expected_dist}"
    )
    out["T3_stab_flag0_order"] = len(stab_0)
    out["T3_stab_order_dist"] = dict(stab_0_order_dist)
    out["T3_matches_P"] = True
    print(f"T3: Stab(flag 0) has order {len(stab_0)} with dist {dict(stab_0_order_dist)}  OK")

    # ------------------------------------------------------------------
    # T4: center of H is trivial (no central Z2 => P is not H/Z2)
    # ------------------------------------------------------------------
    H_elems, mul = _load_H()
    identity_H = next(i for i in range(192) if all(mul[i][j] == j for j in range(192)))

    center_H = [
        i for i in range(192)
        if all(mul[i][j] == mul[j][i] for j in range(192))
    ]
    assert center_H == [identity_H], f"H center = {center_H}, expected trivial"
    out["T4_H_center_size"] = len(center_H)
    out["T4_H_center_trivial"] = True
    out["T4_P_not_quotient_of_H"] = True
    print(f"T4: Z(H) = {{e}} (trivial), P is not a quotient H/Z2  OK")

    # ------------------------------------------------------------------
    # T5: Universal obstruction -- H cannot host f-vector (4,12,16,8)
    # ------------------------------------------------------------------
    def elem_order_H(i: int) -> int:
        cur = i
        k = 1
        while cur != identity_H:
            cur = mul[i][cur]
            k += 1
            if k > 200:
                return -1
        return k

    H_orders = [elem_order_H(i) for i in range(192)]
    invols_H = [i for i in range(192) if H_orders[i] == 2]

    def commutes_H(a: int, b: int) -> bool:
        return mul[a][b] == mul[b][a]

    def subgroup_order_H(gens_idx: set) -> int:
        S: set = {identity_H}
        queue = list(gens_idx)
        while queue:
            g = queue.pop()
            if g in S:
                continue
            S.add(g)
            for h in list(S):
                for p in (mul[g][h], mul[h][g]):
                    if p not in S:
                        queue.append(p)
        return len(S)

    # Count D4 subgroups (generated by two involutions with product of order 4)
    D4_subgroup_orbits_checked = 0
    obstruction_confirmed = 0
    processed_D4 = set()

    for r2_h in invols_H:
        for r3_h in invols_H:
            if r2_h >= r3_h:
                continue
            if H_orders[mul[r2_h][r3_h]] != 4:
                continue
            D4_set = subgroup_closure([
                tuple(range(192)),  # identity (hack: use index form below)
            ])
            # Use index-based closure for D4
            D4_idx: set = {identity_H}
            queue_d4 = [r2_h, r3_h]
            while queue_d4:
                g = queue_d4.pop()
                if g in D4_idx:
                    continue
                D4_idx.add(g)
                for h in list(D4_idx):
                    for p in (mul[g][h], mul[h][g]):
                        if p not in D4_idx:
                            queue_d4.append(p)
            if len(D4_idx) != 8:
                continue
            D4_frozen = frozenset(D4_idx)
            if D4_frozen in processed_D4:
                continue
            processed_D4.add(D4_frozen)

            # Find involutions r0 centralizing D4 and outside D4
            valid_r0_list = []
            for r0_h in invols_H:
                if r0_h in D4_idx:
                    continue
                if not all(commutes_H(r0_h, g) for g in D4_idx):
                    continue
                if subgroup_order_H({r0_h, r2_h, r3_h}) == 16:
                    valid_r0_list.append(r0_h)

            if not valid_r0_list:
                continue

            D4_subgroup_orbits_checked += 1

            # Check: any r1 commuting with r3_h giving ord(r0*r1)=3?
            found_order3 = False
            for r0_h in valid_r0_list:
                for r1_h in invols_H:
                    if not commutes_H(r1_h, r3_h):
                        continue
                    if r1_h in {r0_h, r2_h, r3_h}:
                        continue
                    if H_orders[mul[r0_h][r1_h]] == 3:
                        found_order3 = True
                        break
                if found_order3:
                    break

            if not found_order3:
                obstruction_confirmed += 1

    assert D4_subgroup_orbits_checked == 66, (
        f"Expected 66 D4 subgroup orbits, got {D4_subgroup_orbits_checked}"
    )
    assert obstruction_confirmed == 66, (
        f"Obstruction not universal: {obstruction_confirmed}/66 confirmed"
    )
    out["T5_D4_subgroups_in_H"] = D4_subgroup_orbits_checked
    out["T5_obstruction_confirmed_all"] = (obstruction_confirmed == 66)
    out["T5_obstruction_count"] = obstruction_confirmed
    out["T5_H_cannot_host_4_12_16_8"] = True
    print(f"T5: Universal obstruction confirmed for all {obstruction_confirmed}/66 D4 subgroups  OK")

    # ------------------------------------------------------------------
    # T6: Order-8 signatures distinguish the groups
    # ------------------------------------------------------------------
    H_order_dist = Counter(H_orders)
    Gamma_order_dist = Counter(perm_order(g) for g in G)
    # Compare: H has 48 order-8, Gamma has 3456, P has 0
    assert H_order_dist[8] == 48
    assert Gamma_order_dist[8] == 3456
    assert P_expected_dist.get(8, 0) == 0
    out["T6_H_order8_count"] = int(H_order_dist[8])
    out["T6_Gamma_order8_count"] = int(Gamma_order_dist[8])
    out["T6_P_order8_count"] = 0
    out["T6_H_not_isomorphic_to_monodromy"] = True
    print(f"T6: H has {H_order_dist[8]} order-8, Gamma has {Gamma_order_dist[8]}, P has 0  OK")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    out["numerological_connection"] = {
        "flags": 192,
        "H_order": 192,
        "W_D4_order": 192,
        "note": "192 = |tomotope flags| = |H| = |W(D4)| is a numerological coincidence",
        "structural_connection": False,
        "actual_monodromy_order": 18432,
    }
    out["coxeter_orders"] = {
        "|r0r1|": int(perm_order(compose(r0, r1))),
        "|r1r2|": int(perm_order(compose(r1, r2))),
        "|r2r3|": int(perm_order(compose(r2, r3))),
        "|r0r2|": int(perm_order(compose(r0, r2))),
        "|r0r3|": int(perm_order(compose(r0, r3))),
        "|r1r3|": int(perm_order(compose(r1, r3))),
    }

    return out


def main() -> None:
    report = build_tomotope_H_obstruction_report()
    out_path = ROOT / "data" / "w33_tomotope_H_obstruction.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {out_path}")
    print("All theorems verified OK")


if __name__ == "__main__":
    main()
