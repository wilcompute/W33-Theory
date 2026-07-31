from __future__ import annotations

import hashlib
import itertools

import numpy as np

from pass1370_1374 import modular_radicals

from .bridge_classification import MASKS, bridge, build_all_sheets, dense_sheet
from .common import GOOD, rank_mod, sha


class DenseBasis:
    def __init__(self, p, shape):
        self.p = p
        self.shape = shape
        self.pivots = {}
        self.matrices = []

    def add(self, M):
        p = self.p
        x = np.asarray(M, dtype=np.int64).reshape(-1).copy() % p
        while np.any(x):
            c = int(np.flatnonzero(x)[0])
            if c not in self.pivots:
                x = x * pow(int(x[c]), -1, p) % p
                self.pivots[c] = x
                self.matrices.append(x.reshape(self.shape).copy())
                return True
            x = (x - int(x[c]) * self.pivots[c]) % p
        return False

    def contains(self, M):
        p = self.p
        x = np.asarray(M, dtype=np.int64).reshape(-1).copy() % p
        while np.any(x):
            c = int(np.flatnonzero(x)[0])
            if c not in self.pivots:
                return False
            x = (x - int(x[c]) * self.pivots[c]) % p
        return True

    @property
    def dimension(self):
        return len(self.pivots)


def reduce_matrices(mats, p, shape):
    basis = DenseBasis(p, shape)
    for M in mats:
        basis.add(M)
    return basis


def algebra_closure(generators, p, n):
    basis = reduce_matrices(generators, p, (n, n))
    generator_basis = list(basis.matrices)
    queue = list(basis.matrices)
    seen = 0
    while seen < len(queue):
        X = queue[seen]
        seen += 1
        for G in generator_basis:
            for product in (X @ G % p, G @ X % p):
                if basis.add(product):
                    queue.append(basis.matrices[-1])
    return basis, generator_basis


def bimodule_closure(seed, left_generators, right_generators, p):
    basis = reduce_matrices(seed, p, seed[0].shape)
    queue = list(basis.matrices)
    seen = 0
    while seen < len(queue):
        X = queue[seen]
        seen += 1
        for A in left_generators:
            Y = A @ X % p
            if basis.add(Y):
                queue.append(basis.matrices[-1])
        for C in right_generators:
            Y = X @ C % p
            if basis.add(Y):
                queue.append(basis.matrices[-1])
    return basis


def analyze():
    p = GOOD
    sheet_rows, rectangles, _flag_index = build_all_sheets()
    Sref = dense_sheet(sheet_rows[((1, 1, 1, 0), 0)]) % p
    R = modular_radicals.rowbasis(Sref, p, 160)
    assert R.shape == (81, 160)
    _RR, pivots = modular_radicals.rref(R, p)
    pivots = pivots[:81]
    RP = R[:, pivots] % p
    RPinv = modular_radicals.invmat(RP, p)

    raw_bridges = []
    labels = []
    attempted = 0
    rejected_ranks = {}
    for mask in MASKS:
        for residual in range(3):
            S = dense_sheet(sheet_rows[(mask, residual)])
            if rank_mod(S) != 81:
                continue
            for side_char, edge_char in itertools.product((0, 1), repeat=2):
                attempted += 1
                B = bridge(S, rectangles, side_char, edge_char) % p
                brank = rank_mod(B)
                if brank != 81:
                    rejected_ranks[str(brank)] = rejected_ranks.get(str(brank), 0) + 1
                    continue
                T = B[:, pivots] @ RPinv % p
                assert np.array_equal(T @ R % p, B % p)
                raw_bridges.append(T)
                labels.append(f"{''.join(map(str, mask))}_r{residual}_s{side_char}_e{edge_char}")

    offdiag = reduce_matrices(raw_bridges, p, (120, 81))
    Tbasis = list(offdiag.matrices)
    assert Tbasis

    left_pairings = []
    right_pairings = []
    for X in Tbasis:
        for Y in Tbasis:
            left_pairings.append(X @ Y.T % p)
            right_pairings.append(X.T @ Y % p)
    left_raw = reduce_matrices(left_pairings, p, (120, 120))
    right_raw = reduce_matrices(right_pairings, p, (81, 81))

    left_alg, left_gens = algebra_closure(left_raw.matrices, p, 120)
    right_alg, right_gens = algebra_closure(right_raw.matrices, p, 81)
    module = bimodule_closure(Tbasis, left_gens, right_gens, p)

    IV = np.eye(120, dtype=np.int64)
    IW = np.eye(81, dtype=np.int64)
    collective_image = np.hstack(Tbasis)
    collective_transpose = np.vstack([T.T for T in Tbasis])

    result = {
        "theorem": "Pass 1414 Full 2160-Apartment Linking Algebra",
        "field_of_exact_rank_computation": p,
        "candidate_bridges_attempted": attempted,
        "rank81_gauge_bridges_input": len(raw_bridges),
        "rejected_bridge_rank_census": rejected_ranks,
        "independent_offdiagonal_bridge_dimension": offdiag.dimension,
        "collective_selector_image_rank": rank_mod(collective_image, p),
        "collective_cycle_detection_rank": rank_mod(collective_transpose, p),
        "left_pairing_span_dimension": left_raw.dimension,
        "right_pairing_span_dimension": right_raw.dimension,
        "left_generated_algebra_dimension": left_alg.dimension,
        "right_generated_algebra_dimension": right_alg.dimension,
        "closed_bridge_bimodule_dimension": module.dimension,
        "selector_identity_in_left_algebra": left_alg.contains(IV),
        "cycle_identity_in_right_algebra": right_alg.contains(IW),
        "left_algebra_is_full_endomorphism_algebra": left_alg.dimension == 120 * 120,
        "right_algebra_is_full_endomorphism_algebra": right_alg.dimension == 81 * 81,
        "linking_envelope_dimension": left_alg.dimension + right_alg.dimension + 2 * module.dimension,
        "strict_morita_context": left_alg.contains(IV) and right_alg.contains(IW),
        "bridge_coordinate_basis": {
            "cycle_basis_rank": 81,
            "pivot_columns": [int(x) for x in pivots],
            "basis_sha256": hashlib.sha256(R.astype(np.int64).tobytes()).hexdigest(),
        },
        "input_labels": labels,
        "conclusion": "The complete full-rank apartment-gauge family is compressed to its independent selector/Steinberg bimodule, and both pairing corners are closed under multiplication. Identity-corner tests decide whether the resulting linking envelope is a strict Morita context.",
        "boundary": "Only bridges independently verified to have rank 81 enter the linking algebra. All dimensions are exact over the good prime 1000003; characteristic-zero equality is not inferred without the frozen integer generators.",
    }
    result["sha256"] = sha(result)
    return result
