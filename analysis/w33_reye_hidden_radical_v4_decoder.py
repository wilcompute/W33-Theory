#!/usr/bin/env python3
"""Reye/Klein Latin geometry as the addition table of the hidden Pauli radical.

The E8-selected D4/Reye sector has already been put in the standard
three-qubit Pauli normal form

    selected = W \\ Rad(W),
    W = <X1,Z1,Z2,X3>,
    R = Rad(W) = <Z2,X3> ~= F2^2.

This certificate resolves the remaining Latin-square ambiguity objectwise.
The three nonzero cosets of R are

    A = X1 + R,  B = Z1 + R,  C = Y1 + R,

and every Reye block is uniquely

    T(r,s) = { X1+r, Z1+s, Y1+r+s },   (r,s) in R^2.

Hence the 16 Reye blocks are literally R x R and their row/column/symbol law
is addition in the hidden radical V4.  We also reconstruct the exact point
ordering used by Pass8909-8916 and verify its stored Latin square through
explicit row/column/symbol coordinate maps to R.  Separately, the numeric
Pass8909 table happens to be the affine table i xor j xor 3 in its stored
0..3 labels.

Information statements below are finite counting statements under an explicit
uniform prior on radical offsets; they are not cryptographic or quantum
randomness claims.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations, product
import json
from math import log2
from pathlib import Path
import sys

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "analysis"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ANALYSIS) not in sys.path:
    sys.path.insert(0, str(ANALYSIS))

from w33_e7_d4_presymplectic_reye_normal_form import (  # noqa: E402
    complementary_d4_pairs,
)
from w33_schur64_e7_threequbit_pauli_objectwise_bridge import (  # noqa: E402
    JSTD,
    build_result as build_pauli_bridge,
    omega,
    pauli_word,
)

OUT = ROOT / "data" / "w33_reye_hidden_radical_v4_decoder.json"
OLD = ROOT / "data" / "PART_W33_PASS8909_8916_E7_E8_D4_REYE_LATIN_SELECTOR.json"
ZERO = (0, 0, 0, 0, 0, 0)


def vxor(a, b):
    return tuple(x ^ y for x, y in zip(a, b))


def bits(word: str):
    lut = {"I": (0, 0), "X": (1, 0), "Z": (0, 1), "Y": (1, 1)}
    out = []
    for ch in word:
        out.extend(lut[ch])
    return tuple(out)


def span(gens):
    S = {ZERO}
    for g in gens:
        S |= {vxor(x, g) for x in tuple(S)}
    return S


X1, Z1, Y1 = bits("XII"), bits("ZII"), bits("YII")
Z2, X3 = bits("IZI"), bits("IIX")
R = span((Z2, X3))
assert len(R) == 4

# Canonical F2^2 coordinate on the radical: index = x3 + 2*z2.
def rindex(v):
    assert v in R
    return int(v[4]) + 2 * int(v[3])


def rvec(i: int):
    assert 0 <= i < 4
    return vxor(X3 if (i & 1) else ZERO, Z2 if (i & 2) else ZERO)


def radical_component(v):
    # Strip the first-qubit Pauli coset representative.
    w = pauli_word(v)
    base = {"X": X1, "Z": Z1, "Y": Y1}[w[0]]
    r = vxor(v, base)
    assert r in R
    return r


def build_result():
    bridge = build_pauli_bridge()
    assert bridge["status"] == "PASS"
    root_to_bits = {
        tuple(row["e7_antipodal_root_pair_representative"]):
        tuple(row["standard_bits_x1z1x2z2x3z3"])
        for row in bridge["dictionary"]
    }

    # Reproduce the exact 12-point ordering used in Pass8909.
    pts = sorted(complementary_d4_pairs())
    selected = [root_to_bits[p] for p in pts]
    assert len(selected) == 12
    assert {pauli_word(v)[0] for v in selected} == {"X", "Y", "Z"}

    # All closed anticommuting XOR triangles on the selected carrier.
    triangles = set()
    for a, b in combinations(selected, 2):
        if omega(a, b, JSTD) != 1:
            continue
        c = vxor(a, b)
        assert c in selected
        triangles.add(frozenset((a, b, c)))
    assert len(triangles) == 16

    # Canonical radical decoder: R^2 -> 16 Reye blocks.
    decoded = {}
    for i, j in product(range(4), repeat=2):
        r, s = rvec(i), rvec(j)
        t = vxor(r, s)
        B = frozenset((vxor(X1, r), vxor(Z1, s), vxor(Y1, t)))
        assert len(B) == 3
        assert all(v in selected for v in B)
        assert sum(omega(a, b, JSTD) for a, b in combinations(B, 2)) == 3
        assert vxor(vxor(*tuple(B)[:2]), tuple(B)[2]) == ZERO
        decoded[(i, j)] = B
    assert len(set(decoded.values())) == 16
    assert set(decoded.values()) == triangles

    # Reconstruct Pass8909's K4+K4+K4 parts and exact Latin table ordering.
    Gcomm = nx.Graph()
    Gcomm.add_nodes_from(range(12))
    for i, j in combinations(range(12), 2):
        if omega(selected[i], selected[j], JSTD) == 0:
            Gcomm.add_edge(i, j)
    parts = [sorted(C) for C in nx.connected_components(Gcomm)]
    assert sorted(map(len, parts)) == [4, 4, 4]
    # NetworkX sees exactly three K4 commuting components.
    assert all(nx.is_isomorphic(Gcomm.subgraph(C), nx.complete_graph(4)) for C in parts)

    rows, cols, syms = parts
    rpos = {x: i for i, x in enumerate(rows)}
    cpos = {x: i for i, x in enumerate(cols)}
    spos = {x: i for i, x in enumerate(syms)}
    L = [[-1] * 4 for _ in range(4)]
    for T in triangles:
        ids = {selected.index(v) for v in T}
        rr = next(x for x in ids if x in rpos)
        cc = next(x for x in ids if x in cpos)
        ss = next(x for x in ids if x in spos)
        L[rpos[rr]][cpos[cc]] = spos[ss]
    assert all(sorted(row) == [0, 1, 2, 3] for row in L)

    old = json.loads(OLD.read_text(encoding="utf-8"))
    old_L = old["latin_square"]
    assert L == old_L

    # Explicit semantic maps from Pass8909's position labels to hidden radical labels.
    position_maps = []
    part_letters = []
    for part in parts:
        letters = {pauli_word(selected[p])[0] for p in part}
        assert len(letters) == 1
        part_letters.append(next(iter(letters)))
        position_maps.append([
            rindex(radical_component(selected[p]))
            for p in part
        ])
    assert set(part_letters) == {"X", "Y", "Z"}
    phi_r, phi_c, phi_s = position_maps

    # The stored Latin incidence is exactly radical addition after those three
    # explicit coordinate maps: phi_s(L(i,j)) = phi_r(i) xor phi_c(j).
    for i, j in product(range(4), repeat=2):
        assert phi_s[L[i][j]] == (phi_r[i] ^ phi_c[j])

    # In the stored *numeric* 0..3 table, a still simpler affine formula holds.
    offsets = {
        L[i][j] ^ i ^ j
        for i, j in product(range(4), repeat=2)
    }
    assert len(offsets) == 1
    affine_offset = next(iter(offsets))
    assert affine_offset == 3

    # Block-intersection graph follows directly from the R^2 labels.
    BG = nx.Graph()
    labels = sorted(decoded)
    BG.add_nodes_from(labels)
    for u, v in combinations(labels, 2):
        if decoded[u] & decoded[v]:
            BG.add_edge(u, v)
    assert set(dict(BG.degree()).values()) == {9}
    lam, mu = set(), set()
    for u, v in combinations(labels, 2):
        common = len(set(BG[u]) & set(BG[v]))
        (lam if BG.has_edge(u, v) else mu).add(common)
    assert lam == {4} and mu == {6}

    # Exact intersection criterion in decoder coordinates.
    for (r, s), (rp, sp) in combinations(labels, 2):
        predicted = (r == rp) or (s == sp) or ((r ^ s) == (rp ^ sp))
        assert bool(decoded[(r, s)] & decoded[(rp, sp)]) == predicted

    # Uniform finite side-information accounting.  No physical randomness claim.
    point_fibre = len(R)
    block_fibre = len(decoded)
    point_bits = log2(point_fibre)
    block_bits = log2(block_fibre)
    assert point_bits == 2.0 and block_bits == 4.0

    checks = {
        "hidden_radical_is_V4": len(R) == 4,
        "decoder_R2_has_16_unique_blocks": len(set(decoded.values())) == 16,
        "decoder_blocks_equal_all_Reye_XOR_triangles": set(decoded.values()) == triangles,
        "Pass8909_exact_Latin_table_reconstructed": L == old_L,
        "explicit_position_maps_turn_Latin_rule_into_radical_XOR": all(
            phi_s[L[i][j]] == (phi_r[i] ^ phi_c[j])
            for i, j in product(range(4), repeat=2)
        ),
        "stored_numeric_Latin_table_is_i_xor_j_xor_3": affine_offset == 3,
        "block_graph_is_SRG_16_9_4_6": set(dict(BG.degree()).values()) == {9} and lam == {4} and mu == {6},
        "block_intersection_has_row_column_symbol_criterion": all(
            bool(decoded[u] & decoded[v]) == ((u[0] == v[0]) or (u[1] == v[1]) or ((u[0] ^ u[1]) == (v[0] ^ v[1])))
            for u, v in combinations(labels, 2)
        ),
        "uniform_point_fibre_side_information_is_2_bits": point_bits == 2.0,
        "uniform_block_choice_side_information_is_4_bits": block_bits == 4.0,
    }

    decoder_rows = []
    for i, j in labels:
        B = decoded[(i, j)]
        decoder_rows.append({
            "row_radical_index": i,
            "column_radical_index": j,
            "symbol_radical_index": i ^ j,
            "block_pauli_words": sorted(pauli_word(v) for v in B),
        })

    return {
        "schema": "w33.reye-hidden-radical-v4-decoder.v1",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "radical": {
            "group": "R = <Z2,X3> ~= F2^2 ~= V4",
            "index_convention": "index = x3 + 2*z2",
            "index_to_pauli_word": {str(i): pauli_word(rvec(i)) for i in range(4)},
            "order": 4,
        },
        "three_nonzero_cosets": {
            "A": "X1 + R",
            "B": "Z1 + R",
            "C": "Y1 + R",
        },
        "decoder": {
            "formula": "T(r,s)={X1+r, Z1+s, Y1+r+s}",
            "domain": "R x R",
            "blocks": 16,
            "rows": decoder_rows,
        },
        "Pass8909_Latin_resolution": {
            "stored_table": L,
            "part_first_qubit_letters_in_stored_component_order": part_letters,
            "position_to_radical_index": {
                "row": phi_r,
                "column": phi_c,
                "symbol": phi_s,
            },
            "semantic_law": "phi_symbol(L(i,j)) = phi_row(i) XOR phi_column(j)",
            "stored_numeric_affine_law": f"L(i,j) = i XOR j XOR {affine_offset}",
            "affine_offset": affine_offset,
        },
        "block_graph": {
            "parameters": [16, 9, 4, 6],
            "intersection_rule": "same r OR same s OR same r+s",
        },
        "uniform_finite_information_model": {
            "qualification": "counting/min-entropy statement only under a uniform prior on radical offsets; no ontic-randomness claim",
            "states_per_coarse_nonzero_coset": point_fibre,
            "hidden_bits_per_point_fibre": point_bits,
            "possible_blocks_for_fixed three_coset_roles": block_fibre,
            "independent_radical_offsets_per_block": 2,
            "hidden_bits_to_select_exact_block": block_bits,
            "third_offset_rule": "t = r XOR s",
        },
        "theorem": (
            "The E8-selected D4/Reye configuration is the V4 radical decoder of the presymplectic Pauli flat: its 16 blocks are canonically R^2 via T(r,s)={X1+r,Z1+s,Y1+r+s}. Pass8909's Latin square becomes the exact addition law of R under explicit point-coordinate maps; its stored numeric table is the affine gauge L(i,j)=i XOR j XOR 3."
        ),
        "claim_boundary": (
            "Exact finite symplectic/incidence theorem. The 2-bit and 4-bit statements are uniform finite side-information counts, not a claim that physical quantum randomness is hidden classical information."
        ),
        "checks": checks,
    }


def main():
    result = build_result()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "radical": result["radical"]["order"],
        "blocks": result["decoder"]["blocks"],
        "affine_offset": result["Pass8909_Latin_resolution"]["affine_offset"],
        "block_graph": result["block_graph"]["parameters"],
    }, sort_keys=True))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
