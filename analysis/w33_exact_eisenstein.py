#!/usr/bin/env python3
"""Small exact-linear-algebra kernel for Q(omega).

Elements are stored as Fraction pairs ``a + b*omega`` with
``omega**2 + omega + 1 = 0``.  This module intentionally implements only the
operations needed by the W33 qutrit certificates: exact field arithmetic,
matrix products, adjoints, Kronecker products, and Gaussian rank.
"""
from __future__ import annotations

from fractions import Fraction
from typing import Iterable, Sequence


class Eisenstein:
    """An exact element of Q(omega), represented by the pair (a, b)."""

    __slots__ = ("a", "b")

    def __init__(self, a: int | Fraction = 0, b: int | Fraction = 0) -> None:
        self.a = Fraction(a)
        self.b = Fraction(b)

    def __add__(self, other: object) -> "Eisenstein":
        right = coerce(other)
        return Eisenstein(self.a + right.a, self.b + right.b)

    __radd__ = __add__

    def __neg__(self) -> "Eisenstein":
        return Eisenstein(-self.a, -self.b)

    def __sub__(self, other: object) -> "Eisenstein":
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> "Eisenstein":
        return coerce(other) - self

    def __mul__(self, other: object) -> "Eisenstein":
        right = coerce(other)
        return Eisenstein(
            self.a * right.a - self.b * right.b,
            self.a * right.b + self.b * right.a - self.b * right.b,
        )

    __rmul__ = __mul__

    def conjugate(self) -> "Eisenstein":
        # omega_bar = omega**2 = -1 - omega.
        return Eisenstein(self.a - self.b, -self.b)

    def norm(self) -> Fraction:
        return self.a * self.a - self.a * self.b + self.b * self.b

    def __truediv__(self, other: object) -> "Eisenstein":
        right = coerce(other)
        denominator = right.norm()
        if denominator == 0:
            raise ZeroDivisionError("division by zero in Q(omega)")
        return self * Eisenstein(
            right.conjugate().a / denominator,
            right.conjugate().b / denominator,
        )

    def __eq__(self, other: object) -> bool:
        try:
            right = coerce(other)
        except TypeError:
            return False
        return self.a == right.a and self.b == right.b

    def __hash__(self) -> int:
        return hash((self.a, self.b))

    def __bool__(self) -> bool:
        return self.a != 0 or self.b != 0

    def as_pair(self) -> tuple[Fraction, Fraction]:
        return self.a, self.b

    def __repr__(self) -> str:
        return f"Eisenstein({self.a!r}, {self.b!r})"


def coerce(value: object) -> Eisenstein:
    if isinstance(value, Eisenstein):
        return value
    if isinstance(value, (int, Fraction)):
        return Eisenstein(value)
    raise TypeError(f"cannot coerce {type(value).__name__} to Q(omega)")


ZERO = Eisenstein()
ONE = Eisenstein(1)
OMEGA = Eisenstein(0, 1)
OMEGA_POWERS = (ONE, OMEGA, Eisenstein(-1, -1))

Matrix = list[list[Eisenstein]]


def omega_power(exponent: int) -> Eisenstein:
    return OMEGA_POWERS[int(exponent) % 3]


def zero_matrix(rows: int, columns: int) -> Matrix:
    return [[ZERO for _ in range(columns)] for _ in range(rows)]


def identity_matrix(dimension: int) -> Matrix:
    return [
        [ONE if row == column else ZERO for column in range(dimension)]
        for row in range(dimension)
    ]


def matrix_add(*matrices: Sequence[Sequence[Eisenstein]]) -> Matrix:
    if not matrices:
        raise ValueError("matrix_add needs at least one matrix")
    rows, columns = len(matrices[0]), len(matrices[0][0])
    return [
        [sum((matrix[i][j] for matrix in matrices), ZERO) for j in range(columns)]
        for i in range(rows)
    ]


def matrix_scale(scalar: object, matrix: Sequence[Sequence[Eisenstein]]) -> Matrix:
    factor = coerce(scalar)
    return [[factor * value for value in row] for row in matrix]


def matrix_multiply(
    left: Sequence[Sequence[Eisenstein]],
    right: Sequence[Sequence[Eisenstein]],
) -> Matrix:
    rows, middle, columns = len(left), len(right), len(right[0])
    if not left or len(left[0]) != middle:
        raise ValueError("incompatible matrix dimensions")
    result = zero_matrix(rows, columns)
    for i in range(rows):
        for k in range(middle):
            if not left[i][k]:
                continue
            for j in range(columns):
                if right[k][j]:
                    result[i][j] = result[i][j] + left[i][k] * right[k][j]
    return result


def matrix_dagger(matrix: Sequence[Sequence[Eisenstein]]) -> Matrix:
    return [
        [matrix[j][i].conjugate() for j in range(len(matrix))]
        for i in range(len(matrix[0]))
    ]


def kronecker(
    left: Sequence[Sequence[Eisenstein]],
    right: Sequence[Sequence[Eisenstein]],
) -> Matrix:
    return [
        [
            left[i][j] * right[k][ell]
            for j in range(len(left[0]))
            for ell in range(len(right[0]))
        ]
        for i in range(len(left))
        for k in range(len(right))
    ]


def matrix_rank(matrix: Iterable[Iterable[object]]) -> int:
    """Return the exact row rank over Q(omega) by Gaussian elimination."""

    reduced = [[coerce(value) for value in row] for row in matrix]
    if not reduced:
        return 0
    columns = len(reduced[0])
    if any(len(row) != columns for row in reduced):
        raise ValueError("ragged matrix")
    pivot_row = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(pivot_row, len(reduced)) if reduced[row][column]),
            None,
        )
        if pivot is None:
            continue
        reduced[pivot_row], reduced[pivot] = reduced[pivot], reduced[pivot_row]
        inverse = ONE / reduced[pivot_row][column]
        reduced[pivot_row] = [value * inverse for value in reduced[pivot_row]]
        for row in range(pivot_row + 1, len(reduced)):
            factor = reduced[row][column]
            if factor:
                reduced[row] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(reduced[row], reduced[pivot_row])
                ]
        pivot_row += 1
        if pivot_row == len(reduced):
            break
    return pivot_row
