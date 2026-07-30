#!/usr/bin/env python3
from __future__ import annotations
from fractions import Fraction
from functools import reduce
from math import gcd
import math
import numpy as np
import sympy as sp
import w33_pass1315_1319_exact_frontiers as prior
GROUP_ORDER=prior.GROUP_ORDER
COMMON_SPECIES=("1","15a","20","60a")
NONCOMMUTATIVE_BLOCKS=("6","20","30","64")
def fstr(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def fractions_to_json(values):
    if isinstance(values, Fraction):
        return fstr(values)
    if isinstance(values, list):
        return [fractions_to_json(x) for x in values]
    if isinstance(values, tuple):
        return [fractions_to_json(x) for x in values]
    if isinstance(values, dict):
        return {str(k): fractions_to_json(v) for k, v in values.items()}
    return values


def lcm_many(values):
    answer = 1
    for value in values:
        answer = math.lcm(answer, value)
    return answer


def primitive_integer_vector(vector: list[Fraction]) -> list[Fraction]:
    """Scale a rational vector to primitive integral coordinates."""
    den = lcm_many(x.denominator for x in vector)
    ints = [int(x * den) for x in vector]
    nonzero = [abs(x) for x in ints if x]
    if not nonzero:
        return [Fraction(0) for _ in vector]
    common = reduce(gcd, nonzero)
    ints = [x // common for x in ints]
    first = next(x for x in ints if x)
    if first < 0:
        ints = [-x for x in ints]
    return [Fraction(x) for x in ints]


class RelationAlgebra:
    def __init__(self, hecke: dict):
        self.p = hecke["p"]
        self.R = hecke["R"]
        self.r = self.p.shape[0]
        self.central = hecke["idempotents"]
        self.zero = [Fraction(0) for _ in range(self.r)]
        self.std = [
            [Fraction(int(i == j)) for i in range(self.r)]
            for j in range(self.r)
        ]
        self.diag_label = int(self.R[0, 0])
        self.star_map = self._star_map()

    def _star_map(self) -> list[int]:
        out = []
        for i in range(self.r):
            x, y = np.argwhere(self.R == i)[0]
            out.append(int(self.R[y, x]))
        assert sorted(out) == list(range(self.r))
        return out

    def add(self, a, b):
        return [x + y for x, y in zip(a, b)]

    def sub(self, a, b):
        return [x - y for x, y in zip(a, b)]

    def scale(self, a, scalar):
        scalar = Fraction(scalar)
        return [scalar * x for x in a]

    def mul(self, a, b):
        out = [Fraction(0) for _ in range(self.r)]
        for i, ai in enumerate(a):
            if not ai:
                continue
            for j, bj in enumerate(b):
                if not bj:
                    continue
                for k, value in enumerate(self.p[i, j]):
                    if value:
                        out[k] += ai * bj * int(value)
        return out

    def star(self, a):
        out = [Fraction(0) for _ in range(self.r)]
        for i, value in enumerate(a):
            out[self.star_map[i]] += value
        return out

    @staticmethod
    def to_sympy(vector):
        return sp.Matrix([sp.Rational(x.numerator, x.denominator) for x in vector])

    @staticmethod
    def from_sympy(vector):
        return [Fraction(int(x.p), int(x.q)) for x in vector]

    def independent_basis(self, vectors):
        matrix = sp.Matrix.hstack(*(self.to_sympy(x) for x in vectors))
        pivots = matrix.rref()[1]
        return [vectors[i] for i in pivots]

    def coordinate_solver(self, basis):
        matrix = sp.Matrix.hstack(*(self.to_sympy(x) for x in basis))
        pivot_rows = list(matrix.T.rref()[1])
        assert len(pivot_rows) == len(basis)
        square = matrix.extract(pivot_rows, range(len(basis)))
        inverse = square.inv()

        def coordinates(vector):
            restricted = self.to_sympy(vector).extract(pivot_rows, [0])
            return self.from_sympy(inverse * restricted)

        return coordinates

    def left_matrix(self, element, basis, coordinates):
        columns = [coordinates(self.mul(element, b)) for b in basis]
        return sp.Matrix.hstack(*(self.to_sympy(x) for x in columns))


