#!/usr/bin/env python3
"""Passes 5832--5839: close the q=5 M2(F2) carrier through eight exact probes.

This packet deliberately mixes one mainline closure (normalizer/code/Pauli/all-field
Fourier geometry) with three outside-the-box structural probes.  Every finite claim is
replayed from definitions here; external two-qubit prior art supplies only the published
choice of the 15 Pauli labels and its 9+6 partition.

Pass 5832  Full S16 normalizer of the 576 affine left/right group.
Pass 5833  The Reye [12,4,6] kernel: its 12 minimum words are exactly heavy blocks.
Pass 5834  Explicit quadratic/symplectic isometry from matrix-rank 9+6 to the published
           two-qubit Mermin 9+6.
Pass 5835  M2(F_r) all-field Fourier/Radon rank-orbit theorem, prime anchors 2,3,5,7.
Pass 5836  Publication-front-door audit payload for the five new matrix-frontier cards.
Pass 5837  Determinant is a self-dual bent quadratic on M2(F2).
Pass 5838  The unit-difference Cayley graph is the 4x4 rook graph; its full 1152
           automorphism group is exactly the affine normalizer.
Pass 5839  The Reye [12,4,6] code is the three-coordinate projective-line puncture of
           the binary simplex [15,4,8] code.

No physical state, particle, coupling, or continuum identification is asserted.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "PART_W33_PASS5832_5839_NORMALIZER_CODE_PAULI_ALLQ.json"
SNF_SOURCE = ROOT / "data" / "PART_W33_PASS5824_5831_INTEGRAL_W9_LATTICES.json"

# Binary vector convention throughout: integer bits (a,b,c,d), least-significant first.
BASIS = (1, 2, 4, 8)


def bits4(x: int) -> tuple[int, int, int, int]:
    return tuple((x >> i) & 1 for i in range(4))  # type: ignore[return-value]


def parity(x: int) -> int:
    return x.bit_count() & 1


def mdet2(x: int) -> int:
    a, b, c, d = bits4(x)
    return (a & d) ^ (b & c)


def mmul2(x: int, y: int) -> int:
    a, b, c, d = bits4(x)
    e, f, g, h = bits4(y)
    out = (
        (a & e) ^ (b & g),
        (a & f) ^ (b & h),
        (c & e) ^ (d & g),
        (c & f) ^ (d & h),
    )
    return sum(bit << i for i, bit in enumerate(out))


def mt2(x: int) -> int:
    a, b, c, d = bits4(x)
    out = (a, c, b, d)
    return sum(bit << i for i, bit in enumerate(out))


def minv2(x: int) -> int:
    assert mdet2(x) == 1
    a, b, c, d = bits4(x)
    out = (d, b, c, a)
    return sum(bit << i for i, bit in enumerate(out))


GL2 = tuple(x for x in range(16) if mdet2(x) == 1)
assert len(GL2) == 6


def lin_perm_from_cols(cols: tuple[int, int, int, int]) -> tuple[int, ...]:
    return tuple(
        cols[0] * ((x >> 0) & 1)
        ^ cols[1] * ((x >> 1) & 1)
        ^ cols[2] * ((x >> 2) & 1)
        ^ cols[3] * ((x >> 3) & 1)
        for x in range(16)
    )


def rank4_cols(cols: tuple[int, int, int, int]) -> int:
    span = {0}
    rank = 0
    for v in cols:
        new = span | {x ^ v for x in span}
        if len(new) > len(span):
            rank += 1
            span = new
    return rank


def gl4_perms() -> list[tuple[int, ...]]:
    out = []
    for cols in itertools.permutations(range(1, 16), 4):
        if rank4_cols(cols) == 4:
            out.append(lin_perm_from_cols(cols))
    assert len(out) == 20160 and len(set(out)) == 20160
    return out


def pcompose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    """p after q."""
    return tuple(p[q[x]] for x in range(len(q)))


def pinv(p: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * len(p)
    for i, j in enumerate(p):
        out[j] = i
    return tuple(out)


def left_right_perm(A: int, B: int) -> tuple[int, ...]:
    Bi = minv2(B)
    return tuple(mmul2(mmul2(A, M), Bi) for M in range(16))


def affine_perm(X: int, lin: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(lin[M] ^ X for M in range(16))


def normalizer_packet(gl4: list[tuple[int, ...]]) -> dict:
    H = {left_right_perm(A, B) for A in GL2 for B in GL2}
    assert len(H) == 36
    normal = []
    central = []
    for L in gl4:
        Li = pinv(L)
        conj = {pcompose(pcompose(L, h), Li) for h in H}
        if conj == H:
            normal.append(L)
        if all(pcompose(L, h) == pcompose(h, L) for h in H):
            central.append(L)
    transpose = tuple(mt2(M) for M in range(16))
    assert len(normal) == 72
    assert len(central) == 1
    assert transpose in normal and transpose not in H

    Naff = {affine_perm(X, L) for X in range(16) for L in normal}
    Gaff = {affine_perm(X, L) for X in range(16) for L in H}
    assert len(Gaff) == 576 and len(Naff) == 1152 and Gaff < Naff
    return {
        "linear_left_right_order": 36,
        "linear_normalizer_order": len(normal),
        "linear_centralizer_order": len(central),
        "transpose_in_normalizer_not_group": True,
        "affine_group_order": len(Gaff),
        "full_S16_normalizer_order": len(Naff),
        "normalizer_quotient": "C2",
        "proof_of_S16_exhaustion": (
            "The regular translation subgroup T=C2^4 is O_2(G): the quotient "
            "G/T=S3xS3 has trivial O_2. Hence T is characteristic in G. Every "
            "S16-normalizer of G normalizes T and therefore lies in "
            "N_S16(T)=AGL(4,2). The exhaustive GL4(2) computation gives "
            "|N_GL4(H)|=72, so |N_S16(G)|=16*72=1152."
        ),
        "_normalizer_affine_perms": Naff,
    }


def mv2(M: int, w: int) -> int:
    a, b, c, d = bits4(M)
    w0, w1 = w & 1, (w >> 1) & 1
    return ((a & w0) ^ (b & w1)) | (((c & w0) ^ (d & w1)) << 1)


def dot2(u: int, v: int) -> int:
    return parity(u & v)


POINTS = tuple((w, x) for w in (1, 2, 3) for x in range(4))


def reye_lines() -> tuple[frozenset[int], ...]:
    return tuple(
        frozenset(i for i, (w, x) in enumerate(POINTS) if x == mv2(M, w))
        for M in range(16)
    )


def reye_kernel_words() -> list[tuple[int, ...]]:
    lines = reye_lines()
    words = []
    for mask in range(1 << 12):
        word = tuple((mask >> i) & 1 for i in range(12))
        if all(sum(word[i] for i in L) % 2 == 0 for L in lines):
            words.append(word)
    return words


def support_word(phi: int, psi: int) -> tuple[int, ...]:
    return tuple(dot2(phi, x) ^ dot2(psi, w) for w, x in POINTS)


def code_packet() -> dict:
    words = reye_kernel_words()
    weights = {}
    for word in words:
        weights[sum(word)] = weights.get(sum(word), 0) + 1
    assert len(words) == 16 and weights == {0: 1, 6: 12, 8: 3}

    heavy = {support_word(phi, psi) for phi in (1, 2, 3) for psi in range(4)}
    wt6 = {w for w in words if sum(w) == 6}
    assert wt6 == heavy
    wt8 = {w for w in words if sum(w) == 8}
    expected_wt8 = {support_word(0, psi) for psi in (1, 2, 3)}
    assert wt8 == expected_wt8

    snf = json.loads(SNF_SOURCE.read_text())
    r_snf = snf["pass_5827_saturated_radon_snf"]["R_transpose_A3cubed_to_A3tensorA3"]
    h_snf = snf["pass_5827_saturated_radon_snf"]["H_transpose_A3cubed_to_A3cubed"]
    r_even = sum(d % 2 == 0 for d in r_snf)
    r_v2 = sum((d.bit_length() - 1) for d in r_snf)
    h_even = sum(d % 2 == 0 for d in h_snf)
    h_v2 = sum((d.bit_length() - 1) for d in h_snf)
    assert (r_even, r_v2) == (4, 6)
    assert (h_even, h_v2) == (7, 9)

    return {
        "reye_binary_code": [12, 4, 6],
        "weight_enumerator": {"0": 1, "6": 12, "8": 3},
        "minimum_weight_words_equal_heavy_six_sets": True,
        "weight8_words": "the three phi=0, psi!=0 fiber-pair words",
        "saturated_R_transpose_snf": r_snf,
        "saturated_R_mod2_nullity": r_even,
        "saturated_R_2adic_cokernel_valuation": r_v2,
        "same_four_dimensional_binary_defect": True,
        "saturated_H_transpose_snf": h_snf,
        "saturated_H_mod2_nullity": h_even,
        "saturated_H_2adic_cokernel_valuation": h_v2,
        "firewall": (
            "The local 12-coordinate Reye code is not identified with the global "
            "q=5 [[156,26,6]]_2 W(3,5) CSS point code. Their common distance 6 is "
            "not by itself an equivalence."
        ),
    }


# Pauli vectors in bit order (x1,z1,x2,z2).
PAULI = {
    "II": 0, "XI": 1, "ZI": 2, "YI": 3, "IX": 4, "IY": 12, "IZ": 8,
    "XX": 5, "XY": 13, "XZ": 9, "YX": 7, "YY": 15, "YZ": 11,
    "ZX": 6, "ZY": 14, "ZZ": 10,
}
# Saniga--Planat--Pracna, arXiv:quant-ph/0611063, Eq. (6)--(8).
C_PAULI = {
    1: PAULI["ZX"], 2: PAULI["YY"], 3: PAULI["IX"],
    4: PAULI["YZ"], 5: PAULI["YI"], 6: PAULI["XX"],
    7: PAULI["XZ"], 8: PAULI["YX"], 9: PAULI["ZY"],
    10: PAULI["XI"], 11: PAULI["XY"], 12: PAULI["IY"],
    13: PAULI["IZ"], 14: PAULI["ZZ"], 15: PAULI["ZI"],
}
PAULI_TO_C = {v: k for k, v in C_PAULI.items()}
assert len(PAULI_TO_C) == 15


def q_spp(v: int) -> int:
    x1, z1, x2, z2 = bits4(v)
    return (x1 & z1) ^ (x2 & z2) ^ x2


def b_spp(u: int, v: int) -> int:
    ux1, uz1, ux2, uz2 = bits4(u)
    vx1, vz1, vx2, vz2 = bits4(v)
    return (ux1 & vz1) ^ (uz1 & vx1) ^ (ux2 & vz2) ^ (uz2 & vx2)


def frob_pair(Y: int, Z: int) -> int:
    return parity(Y & Z)


def pauli_packet(gl4: list[tuple[int, ...]]) -> dict:
    assert {PAULI_TO_C[v] for v in range(1, 16) if q_spp(v) == 0} == set(range(7, 16))
    assert {PAULI_TO_C[v] for v in range(1, 16) if q_spp(v) == 1} == set(range(1, 7))

    isometries = [L for L in gl4 if all(q_spp(L[Y]) == mdet2(Y) for Y in range(16))]
    assert len(isometries) == 72
    L = next(L for L in isometries if tuple(L[e] for e in BASIS) == (1, 8, 12, 2))
    for Y in range(16):
        for Z in range(16):
            det_polar = mdet2(Y) ^ mdet2(Z) ^ mdet2(Y ^ Z)
            assert det_polar == b_spp(L[Y], L[Z])

    label_to_C = {str(Y): PAULI_TO_C[L[Y]] for Y in range(1, 16)}
    rank1 = {Y for Y in range(1, 16) if mdet2(Y) == 0}
    rank2 = {Y for Y in range(1, 16) if mdet2(Y) == 1}
    assert {PAULI_TO_C[L[Y]] for Y in rank1} == set(range(7, 16))
    assert {PAULI_TO_C[L[Y]] for Y in rank2} == set(range(1, 7))

    factors = (1, 2, 3)
    grid = []
    for u in factors:
        row = []
        u0, u1 = u & 1, (u >> 1) & 1
        for v in factors:
            v0, v1 = v & 1, (v >> 1) & 1
            Ybits = (u0 & v0, u0 & v1, u1 & v0, u1 & v1)
            Y = sum(bit << i for i, bit in enumerate(Ybits))
            assert Y in rank1
            row.append(PAULI_TO_C[L[Y]])
        grid.append(row)
    # Every row and every column is a commuting triple (phases/sign-products omitted).
    for triple in grid + [[grid[i][j] for i in range(3)] for j in range(3)]:
        vals = [C_PAULI[c] for c in triple]
        assert all(b_spp(vals[i], vals[j]) == 0 for i in range(3) for j in range(i + 1, 3))

    return {
        "published_partition": {"C1_C6": "six-point complement", "C7_C15": "Mermin nine"},
        "quadratic_form_on_Pauli_bits": "q_SPP=x1*z1+x2*z2+x2",
        "matrix_quadratic_form": "det([[a,b],[c,d]])=a*d+b*c",
        "number_of_linear_quadratic_isometries": len(isometries),
        "chosen_isometry_basis_images_Pauli_ints": [1, 8, 12, 2],
        "chosen_isometry_basis_images": ["XI", "IZ", "IY", "ZI"],
        "matrix_label_to_C_label": label_to_C,
        "rank_one_grid_C_labels": grid,
        "rank_one_grid_rows_and_columns_commute": True,
        "rank_one_maps_exactly_to_C7_C15": True,
        "units_map_exactly_to_C1_C6": True,
        "all_105_polar_commutation_pairs_preserved": True,
        "interpretation": (
            "This is an object-level isomorphism between the nonzero dual Fourier "
            "labels Y in M2(F2) and the 15 two-qubit Pauli points. It does not "
            "identify the q=5 cover points with qubit states or observables."
        ),
    }


def rank2_modp(M: tuple[int, int, int, int], p: int) -> int:
    a, b, c, d = M
    if all(x % p == 0 for x in M):
        return 0
    if (a * d - b * c) % p:
        return 2
    return 1


def allq_packet() -> dict:
    anchors = {}
    for p in (2, 3, 5, 7):
        mats = list(itertools.product(range(p), repeat=4))
        ranks = [rank2_modp(M, p) for M in mats]
        counts = {r: ranks.count(r) for r in (0, 1, 2)}
        N1 = (p - 1) * (p + 1) ** 2
        N2 = p * (p - 1) ** 2 * (p + 1)
        assert counts == {0: 1, 1: N1, 2: N2}
        kernel_weights = [(p * p - 1) if r == 0 else (p - 1 if r == 1 else 0) for r in ranks]
        spectra = {0: set(), 1: set(), 2: set()}
        for Y, yrank in zip(mats, ranks):
            bins = [0] * p
            for D, k in zip(mats, kernel_weights):
                if not k:
                    continue
                exponent = sum(y * d for y, d in zip(Y, D)) % p
                bins[exponent] += k
            assert len(set(bins[1:])) == 1
            eig = bins[0] - bins[1]
            spectra[yrank].add(eig)
        expected = {0: p * p * (p * p - 1), 1: p * p * (p - 1), 2: 0}
        assert {r: next(iter(v)) for r, v in spectra.items()} == expected
        anchors[str(p)] = {
            "rank_label_counts": counts,
            "R_rank": 1 + N1,
            "R_kernel_dimension": N2,
            "RRT_nonzero_singular_values_squared": {"constant": expected[0], "rank1": expected[1]},
            "extra_point_rank1_preimage_kernel_dimension": (p - 2) * N1,
        }

    return {
        "field_statement": (
            "For every finite field F_r, additive characters of M2(F_r) split by "
            "dual matrix rank 0/1/2. For evaluation incidence R[(w,x),M]=1 iff x=Mw, "
            "im(R^T)=1 plus the rank-one Fourier sector and ker(R)=the rank-two sector."
        ),
        "rank1_dimension_formula": "(r-1)(r+1)^2",
        "rank2_dimension_formula": "r(r-1)^2(r+1)=|GL2(r)|",
        "R_rank_formula": "1+(r-1)(r+1)^2",
        "singular_square_constant": "r^2(r^2-1)",
        "singular_square_rank1": "r^2(r-1)",
        "D_disjointness_formula": "D[M,(phi,psi)]=1 iff psi=-phi*M",
        "q2_tightness": (
            "At r=2 every rank-one label has a unique factorization phi^T w^T. "
            "For r>2 it has r-1 factorizations, producing an additional "
            "(r-2)(r-1)(r+1)^2 point-side kernel."
        ),
        "prime_anchor_exact_replays": anchors,
        "prime_power_extension": (
            "The proof uses only finite-field linear algebra and additive characters; "
            "for prime powers use a nontrivial character composed with the field trace."
        ),
    }


def bent_packet() -> dict:
    walsh = {}
    for Z in range(16):
        s = sum((-1 if (mdet2(Y) ^ frob_pair(Z, Y)) else 1) for Y in range(16))
        walsh[Z] = s
        assert s == 4 * (-1 if mdet2(Z) else 1)
    assert set(abs(v) for v in walsh.values()) == {4}
    return {
        "identity": "Walsh((-1)^det)(Z)=4*(-1)^det(Z)",
        "is_bent": True,
        "is_self_dual": True,
        "walsh_distribution": {"+4": 10, "-4": 6},
        "boundary": "Boolean/Fourier identity only; no quantum-state claim.",
    }


def rook_packet(normalizer_affine_perms: set[tuple[int, ...]]) -> dict:
    units = {x for x in range(16) if mdet2(x) == 1}
    adj = [[False] * 16 for _ in range(16)]
    for x in range(16):
        for y in range(16):
            if x != y and (x ^ y) in units:
                adj[x][y] = True
    assert {sum(row) for row in adj} == {6}
    lam_mu = {}
    for x in range(16):
        for y in range(x + 1, 16):
            common = sum(adj[x][z] and adj[y][z] for z in range(16))
            lam_mu.setdefault(adj[x][y], set()).add(common)
    assert lam_mu == {True: {2}, False: {2}}

    cliques = []
    for C in itertools.combinations(range(16), 4):
        if all(adj[x][y] for x, y in itertools.combinations(C, 2)):
            cliques.append(C)
    assert len(cliques) == 8
    parallel = []
    for fam in itertools.combinations(range(8), 4):
        chosen = [set(cliques[i]) for i in fam]
        if sum(len(s) for s in chosen) == 16 and len(set().union(*chosen)) == 16:
            parallel.append(fam)
    assert len(parallel) == 2
    rows = [cliques[i] for i in parallel[0]]
    cols = [cliques[i] for i in parallel[1]]
    coord = {}
    for ri, R in enumerate(rows):
        for ci, C in enumerate(cols):
            inter = set(R) & set(C)
            assert len(inter) == 1
            coord[next(iter(inter))] = (ri, ci)

    inverse_coord = {rc: v for v, rc in coord.items()}
    rook_aut = set()
    for rp in itertools.permutations(range(4)):
        for cp in itertools.permutations(range(4)):
            for swap in (0, 1):
                perm = [None] * 16
                for x, (r, c) in coord.items():
                    rr, cc = rp[r], cp[c]
                    if swap:
                        rr, cc = cc, rr
                    perm[x] = inverse_coord[(rr, cc)]
                rook_aut.add(tuple(perm))  # type: ignore[arg-type]
    assert len(rook_aut) == 1152
    assert rook_aut == normalizer_affine_perms
    return {
        "cayley_connection_set": "six invertible 2x2 binary matrices",
        "srg_parameters": [16, 6, 2, 2],
        "K4_count": len(cliques),
        "parallel_K4_partitions": len(parallel),
        "identified_graph": "4x4 rook/lattice graph L2(4)",
        "full_automorphism_order": len(rook_aut),
        "full_automorphism_group": "S4 wr C2",
        "equals_affine_normalizer_from_pass5832": True,
        "resolution": (
            "This supplies the previously missing source of the order-1152 S4 wr C2: "
            "it is the full automorphism group of the unit-difference Cayley graph, "
            "not a Delsarte graph of the [12,4,6] code."
        ),
    }


def simplex_packet() -> dict:
    full_coords = tuple(z for z in range(1, 16))
    deleted_line = {4, 8, 12}  # w=0, x!=0 under z=(w0,w1,x0,x1)
    kept = tuple(z for z in full_coords if z not in deleted_line)
    pcoords = tuple(w | (x << 2) for w, x in POINTS)
    assert set(kept) == set(pcoords) and len(kept) == 12

    restricted = {}
    fullweights = {}
    for coeff in range(16):
        fullword = tuple(parity(coeff & z) for z in full_coords)
        fullweights[coeff] = sum(fullword)
        restricted[coeff] = tuple(parity(coeff & z) for z in pcoords)
    assert {fullweights[c] for c in range(1, 16)} == {8}
    assert set(restricted.values()) == set(reye_kernel_words())

    weight_by_phi = {}
    for coeff in range(1, 16):
        phi = coeff >> 2
        wt = sum(restricted[coeff])
        weight_by_phi.setdefault(phi == 0, set()).add(wt)
    assert weight_by_phi == {True: {8}, False: {6}}

    return {
        "parent_code": "[15,4,8] binary simplex code on PG(3,2)",
        "deleted_coordinates": "projective line {(w,x): w=0, x!=0}, three points",
        "punctured_code": "[12,4,6] Reye kernel",
        "punctured_code_equal_reye_kernel_objectwise": True,
        "twelve_weight6_words": "linear forms with phi!=0; the deleted line contains exactly two 1s",
        "three_weight8_words": "linear forms with phi=0, psi!=0; the deleted line contains only 0s",
        "conceptual_enumerator": "1 + 12 z^6 + 3 z^8",
    }


def publication_packet() -> dict:
    return {
        "canonical_public_index": "docs/index.html",
        "cards_to_register_and_materialize": [
            ["pass-5776-5783-reye-latin-common-core", "analysis/PASS5776_5783_index_insert.html"],
            ["pass-5792-5799-matrix-ring-transpose-outer", "analysis/PASS5792_5799_index_insert.html"],
            ["pass-5816-5823-matrix-fourier-rank", "analysis/PASS5816_5823_index_insert.html"],
            ["pass-5824-5831-integral-w9-lattices", "analysis/PASS5824_5831_index_insert.html"],
            ["pass-5832-5839-normalizer-code-pauli-allq", "analysis/PASS5832_5839_index_insert.html"],
        ],
        "materialization_rule": (
            "Insert each missing card independently into docs/index.html and index.html "
            "before </main> (fallback </body>), rejecting duplicates but not requiring "
            "the two surfaces to be byte-identical."
        ),
        "manuscript_rule": (
            "One new include in analysis/W33_CURRENT_FRONTIER_MANIFEST.tex propagates "
            "to w33_paper.tex, photonic_holonet.tex, and holonet_machine_blueprint.tex."
        ),
    }


def main() -> None:
    gl4 = gl4_perms()
    p5832 = normalizer_packet(gl4)
    Naff = p5832.pop("_normalizer_affine_perms")
    out = {
        "schema": "w33.pass5832_5839.normalizer_code_pauli_allq.v1",
        "status": "PASS",
        "pass_5832_full_normalizer": p5832,
        "pass_5833_code_snf_interface": code_packet(),
        "pass_5834_two_qubit_object_isometry": pauli_packet(gl4),
        "pass_5835_all_field_matrix_fourier_radon": allq_packet(),
        "pass_5836_publication_front_doors": publication_packet(),
        "pass_5837_determinant_bent_chirp": bent_packet(),
        "pass_5838_unit_cayley_rook_graph": rook_packet(Naff),
        "pass_5839_simplex_line_puncture": simplex_packet(),
        "boundary": (
            "Exact finite algebra, coding, Fourier analysis, graph theory and publication "
            "plumbing. The two-qubit bridge is an isomorphism of the nonzero dual Fourier "
            "label geometry to the Pauli-point geometry; it is not a q=5 physical-state "
            "embedding. The all-field theorem is mathematical and does not assign dynamics."
        ),
    }
    OUTPUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
