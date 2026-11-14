"""Kernel constraints for full one-versus-two PPT on the F8 code."""
import json
from fractions import Fraction
from itertools import combinations_with_replacement, product
from pathlib import Path

import numpy as np

from toe_20261114_regulus_three_copy import logical_terms

OUT = Path(__file__).resolve().parents[1] / "data/toe_20261114_regulus_full_ppt.json"


def constraints(triples, columns, terms, dimension):
    index = {t: i for i, t in enumerate(triples)}
    rows = []
    for x, z, _ in terms:
        for a, b in product(range(dimension), repeat=2):
            c = a ^ b
            if b > c:
                continue
            row = np.zeros(len(columns), dtype=np.int64)
            for t in range(dimension):
                shift = t ^ a
                i = index[tuple(sorted((a, b ^ shift, c ^ shift)))]
                j = index[tuple(sorted((t, a ^ x, x ^ shift)))]
                row[columns[min(i,j), max(i,j)]] += (-1)**((z & t).bit_count())
            rows.append(row)
    return np.array(rows)


def rank_mod(matrix, prime):
    matrix = matrix % prime
    rank = 0
    for j in range(matrix.shape[1]):
        rows = np.flatnonzero(matrix[rank:, j])
        if not len(rows):
            continue
        pivot = rank + rows[0]
        matrix[[rank,pivot]] = matrix[[pivot,rank]]
        row = matrix[rank, j:]*pow(int(matrix[rank,j]), -1, prime) % prime
        remaining = np.flatnonzero(matrix[rank+1:,j]) + rank + 1
        matrix[remaining,j:] = (matrix[remaining,j:] - matrix[remaining,j,None]*row) % prime
        rank += 1
    return rank


def check_indexing():
    dimension = 4
    triples = [u for u in combinations_with_replacement(range(dimension), 3)
               if u[0] ^ u[1] ^ u[2] == 0]
    columns = {pair: j for j, pair in enumerate(
        combinations_with_replacement(range(len(triples)), 2))}
    coefficients = np.arange(1, len(columns)+1)
    matrix = np.array([[coefficients[columns[min(i, j), max(i, j)]]
                        for j in range(len(triples))] for i in range(len(triples))])
    labels = list(product(range(dimension), repeat=3))
    index = {u: i for i, u in enumerate(triples)}
    # Explicitly build the Pauli-translation twirl before transposing.
    full = np.zeros((dimension**3, dimension**3), dtype=np.int64)
    for i, u in enumerate(labels):
        shift = u[0] ^ u[1] ^ u[2]
        for j, v in enumerate(labels):
            if shift == v[0] ^ v[1] ^ v[2]:
                a = index[tuple(sorted(x ^ shift for x in u))]
                b = index[tuple(sorted(x ^ shift for x in v))]
                full[i, j] = matrix[a, b]
    pt = full.reshape((dimension,)*6).swapaxes(0, 3)
    for x, z in product(range(dimension), repeat=2):
        direct = [sum((-1)**((z&t).bit_count())*pt[a,b,a^b,t,t^x,x]
                      for t in range(dimension))
                  for a,b in product(range(dimension),repeat=2) if b <= a^b]
        np.testing.assert_array_equal(
            constraints(triples, columns, [(x,z,1)], dimension) @ coefficients, direct)


def certify_gram(rows):
    # Binary64 products and intermediate sums are exact for these integer
    # matrices. A row-norm bound controls every partial dot product.
    matrix = rows.astype(np.float64)
    assert len(rows)*int(np.max(abs(rows)))**2 < 2**53
    gram = matrix.T @ matrix
    identity = np.eye(gram.shape[0])
    scale = 2**16
    lower = np.rint(scale*np.linalg.cholesky(gram-1.5*identity))
    assert lower.shape[0]*int(np.max(abs(lower)))**2 < 2**53
    assert int(np.max(abs(gram)))*scale**2 < 2**51
    residual = (gram-identity)*scale**2 - lower @ lower.T
    assert residual.shape[0]*int(np.max(abs(residual))) < 2**53
    margin = np.diag(residual)-(abs(residual).sum(axis=1)-abs(np.diag(residual)))
    assert min(margin) > 0
    return Fraction(int(min(margin)), scale**2)


def calculate():
    triples = [t for t in combinations_with_replacement(range(16), 3) if t[0]^t[1]^t[2] == 0]
    columns = {pair: j for j, pair in enumerate(combinations_with_replacement(range(len(triples)), 2))}
    check_indexing()
    rows = constraints(triples, columns, logical_terms(), 16)
    rank = rank_mod(rows, 101)
    assert rank == len(columns)
    margin = certify_gram(rows)
    sizes = [1 if len(set(t)) == 1 else 3 if len(set(t)) == 2 else 6 for t in triples]
    # There are 16 identical blocks for the normalized Pauli twirl.
    bound = (1+margin)/sum(s*s for s in sizes)
    print(rows.shape, rank, margin, bound, float(bound), flush=True)
    return dict(status="PASS", variables=len(columns), constraints=len(rows), prime=101, modular_rank=rank, zero_objective_feasible=False,
                gram_gershgorin_margin=str(margin), full_ppt_objective_lower_bound=str(bound),
                decimal_lower_bound=float(bound))


if __name__ == "__main__":
    result = calculate()
    OUT.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
