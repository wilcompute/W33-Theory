#!/usr/bin/env python3
from __future__ import annotations

from collections import deque
import hashlib
import json
from pathlib import Path
from typing import Iterable

import numpy as np


def canonical_json(payload: object) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def certificate(payload: dict) -> str:
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")


class FiniteField:
    """Small polynomial-basis finite field used by the executable witnesses.

    modulus coefficients are constant-first and monic. Degree-one fields use
    modulus=(0, 1). The implementation is deliberately compact and exact.
    """

    def __init__(self, p: int, modulus: tuple[int, ...]):
        self.p = int(p)
        self.modulus = tuple(int(x) % p for x in modulus)
        if self.modulus[-1] != 1:
            raise ValueError("modulus must be monic")
        self.f = len(modulus) - 1
        self.q = p**self.f
        self.elements = tuple(range(self.q))

    def digits(self, a: int) -> list[int]:
        out = []
        for _ in range(self.f):
            out.append(a % self.p)
            a //= self.p
        return out

    def encode(self, coeffs: Iterable[int]) -> int:
        value = 0
        scale = 1
        for c in coeffs:
            value += (int(c) % self.p) * scale
            scale *= self.p
        return value

    def add(self, a: int, b: int) -> int:
        return self.encode((x + y for x, y in zip(self.digits(a), self.digits(b))))

    def neg(self, a: int) -> int:
        return self.encode((-x for x in self.digits(a)))

    def sub(self, a: int, b: int) -> int:
        return self.add(a, self.neg(b))

    def mul(self, a: int, b: int) -> int:
        if self.f == 1:
            return (a * b) % self.p
        aa = self.digits(a)
        bb = self.digits(b)
        coeff = [0] * (2 * self.f - 1)
        for i, x in enumerate(aa):
            for j, y in enumerate(bb):
                coeff[i + j] = (coeff[i + j] + x * y) % self.p
        for degree in range(len(coeff) - 1, self.f - 1, -1):
            lead = coeff[degree] % self.p
            if not lead:
                continue
            shift = degree - self.f
            for j in range(self.f):
                coeff[shift + j] = (coeff[shift + j] - lead * self.modulus[j]) % self.p
        return self.encode(coeff[: self.f])

    def pow(self, a: int, n: int) -> int:
        result = 1
        while n:
            if n & 1:
                result = self.mul(result, a)
            a = self.mul(a, a)
            n >>= 1
        return result

    def inv(self, a: int) -> int:
        if a == 0:
            raise ZeroDivisionError
        return self.pow(a, self.q - 2)

    def validate(self) -> bool:
        if self.q > 125:
            return True
        for a in self.elements:
            if self.add(a, 0) != a or self.mul(a, 1) != a:
                return False
            if a and self.mul(a, self.inv(a)) != 1:
                return False
        return True


def heisenberg_vertices(field: FiniteField) -> list[tuple[int, int, int]]:
    return [(x, y, z) for x in field.elements for y in field.elements for z in field.elements]


def heisenberg_laplacian(field: FiniteField, reduced: bool = True) -> np.ndarray:
    vertices = heisenberg_vertices(field)
    index = {v: i for i, v in enumerate(vertices)}
    n_full = len(vertices)
    n = n_full - 1 if reduced else n_full
    degree = field.q * field.q - 1
    lap = np.zeros((n, n), dtype=np.int64)
    np.fill_diagonal(lap, degree)
    for i, (x, y, z) in enumerate(vertices[:n]):
        for xp in field.elements:
            for yp in field.elements:
                if xp == x and yp == y:
                    continue
                voltage = field.sub(field.mul(y, xp), field.mul(x, yp))
                zp = field.add(z, voltage)
                j = index[(xp, yp, zp)]
                if j < n:
                    lap[i, j] -= 1
    return lap


def padic_smith_exact_valuations(matrix: np.ndarray, p: int, max_exponent: int) -> list[int]:
    """Exact elementary-divisor valuation counts over Z_p.

    Unit pivots are extracted over Z/(p^K). After all unit pivots are removed,
    the residual block is divisible by p; division advances one Bockstein page.
    The returned list gives the number of invariant factors of exact valuation k.
    """
    modulus = p**max_exponent
    work = np.asarray(matrix, dtype=np.int64) % modulus
    exact: list[int] = []
    for _level in range(max_exponent):
        count = 0
        while work.size:
            locations = np.argwhere((work % p) != 0)
            if not locations.size:
                break
            row, col = map(int, locations[0])
            if row:
                work[[0, row], :] = work[[row, 0], :]
            if col:
                work[:, [0, col]] = work[:, [col, 0]]
            inverse = pow(int(work[0, 0]), -1, modulus)
            work[0, :] = (work[0, :] * inverse) % modulus
            if work.shape[0] > 1:
                coefficients = work[1:, 0].copy()
                work[1:, :] = (work[1:, :] - coefficients[:, None] * work[0:1, :]) % modulus
            work = work[1:, 1:].copy()
            count += 1
        exact.append(count)
        if not work.size:
            break
        if np.any(work % p):
            raise AssertionError("residual block is not p-divisible")
        work //= p
        modulus //= p
    if work.size:
        raise AssertionError("max_exponent was too small")
    return exact


def qutrit_matrices() -> dict[str, np.ndarray]:
    omega = np.exp(2j * np.pi / 3)
    x = np.roll(np.eye(3, dtype=complex), 1, axis=0)
    z = np.diag([1, omega, omega**2])
    fourier = np.array([[omega ** (j * k) for k in range(3)] for j in range(3)], dtype=complex) / np.sqrt(3)
    phase = np.diag([1, 1, omega])
    return {"X": x, "Z": z, "F": fourier, "P": phase}


def projective_key(matrix: np.ndarray, decimals: int = 10) -> tuple[float, ...]:
    flat = matrix.reshape(-1)
    nonzero = np.where(np.abs(flat) > 10 ** (-(decimals - 2)))[0]
    if not len(nonzero):
        raise ValueError("zero matrix")
    phase = flat[nonzero[0]] / abs(flat[nonzero[0]])
    normalized = matrix / phase
    return tuple(np.round(np.r_[normalized.real.reshape(-1), normalized.imag.reshape(-1)], decimals))


def qutrit_clifford_words() -> dict[tuple[float, ...], tuple[str, np.ndarray]]:
    generators = qutrit_matrices()
    identity = np.eye(3, dtype=complex)
    words = {projective_key(identity): ("", identity)}
    queue = deque([("", identity)])
    while queue:
        word, current = queue.popleft()
        for name, generator in generators.items():
            candidate = current @ generator
            key = projective_key(candidate)
            if key not in words:
                words[key] = (word + name, candidate)
                queue.append((word + name, candidate))
    return words


def torus_residue(value: int, modulus: int) -> int:
    value %= modulus
    return min(value, modulus - value)
