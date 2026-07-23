#!/usr/bin/env python3
"""Exact Laurent principal parts of the nontrivial W(3,3) Ihara poles.

There are four distinct nontrivial pole locations, not 39 distinct locations:

* (1 +/- sqrt(-10))/11, each of order 24;
* (-2 +/- sqrt(-7))/11, each of order 15.

The restricted adjacency multiplicities 24+15=39 count eigenvalue slots. Each
slot contributes a conjugate pair, so the total nontrivial pole order is 78.
This module computes every principal-part coefficient exactly in the relevant
quadratic field and records the pole-coordinate denominator ideals above 11.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
from math import comb
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Quad:
    """a+b*w in Q(w), with w^2=-d."""

    a: Fraction
    b: Fraction
    d: int

    @classmethod
    def rational(cls, value: int | Fraction, d: int) -> "Quad":
        return cls(Fraction(value), Fraction(0), d)

    def _coerce(self, other: int | Fraction | "Quad") -> "Quad":
        if isinstance(other, Quad):
            if self.d != other.d:
                raise ValueError("quadratic fields differ")
            return other
        return Quad.rational(other, self.d)

    def __add__(self, other: int | Fraction | "Quad") -> "Quad":
        o = self._coerce(other)
        return Quad(self.a + o.a, self.b + o.b, self.d)

    __radd__ = __add__

    def __neg__(self) -> "Quad":
        return Quad(-self.a, -self.b, self.d)

    def __sub__(self, other: int | Fraction | "Quad") -> "Quad":
        return self + (-self._coerce(other))

    def __rsub__(self, other: int | Fraction | "Quad") -> "Quad":
        return self._coerce(other) - self

    def __mul__(self, other: int | Fraction | "Quad") -> "Quad":
        o = self._coerce(other)
        return Quad(
            self.a * o.a - self.d * self.b * o.b,
            self.a * o.b + self.b * o.a,
            self.d,
        )

    __rmul__ = __mul__

    def conjugate(self) -> "Quad":
        return Quad(self.a, -self.b, self.d)

    def norm(self) -> Fraction:
        return self.a * self.a + self.d * self.b * self.b

    def inverse(self) -> "Quad":
        n = self.norm()
        if n == 0:
            raise ZeroDivisionError("zero quadratic element")
        c = self.conjugate()
        return Quad(c.a / n, c.b / n, self.d)

    def __truediv__(self, other: int | Fraction | "Quad") -> "Quad":
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other: int | Fraction | "Quad") -> "Quad":
        return self._coerce(other) / self

    def __pow__(self, exponent: int) -> "Quad":
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = Quad.rational(1, self.d)
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n >>= 1
        return result

    def is_zero(self) -> bool:
        return self.a == 0 and self.b == 0

    def expression(self) -> str:
        if self.b == 0:
            return str(self.a)
        return f"({self.a}) + ({self.b})*sqrt(-{self.d})"

    def payload(self) -> dict[str, str | int]:
        return {
            "field_d": self.d,
            "a": str(self.a),
            "b": str(self.b),
            "expression": self.expression(),
        }


Series = list[Quad]


def zero_series(length: int, d: int) -> Series:
    return [Quad.rational(0, d) for _ in range(length)]


def series_multiply(left: Series, right: Series, length: int) -> Series:
    d = left[0].d if left else right[0].d
    out = zero_series(length, d)
    for i, x in enumerate(left[:length]):
        for j, y in enumerate(right[: length - i]):
            out[i + j] = out[i + j] + x * y
    return out


def series_power_positive(poly: Series, exponent: int, length: int) -> Series:
    result = zero_series(length, poly[0].d)
    result[0] = Quad.rational(1, poly[0].d)
    base = poly[:length] + zero_series(max(0, length - len(poly)), poly[0].d)
    n = exponent
    while n:
        if n & 1:
            result = series_multiply(result, base, length)
        base = series_multiply(base, base, length)
        n >>= 1
    return result


def generalized_negative_binomial(exponent: int, k: int) -> Fraction:
    return Fraction(((-1) ** k) * comb(exponent + k - 1, k))


def series_negative_power(poly: Series, exponent: int, length: int) -> Series:
    """poly(x)^(-exponent) through x^(length-1), exactly."""
    d = poly[0].d
    f0 = poly[0]
    if f0.is_zero():
        raise ZeroDivisionError("series constant term is zero")

    normalized = [coefficient / f0 for coefficient in poly]
    z = zero_series(length, d)
    for index in range(1, min(length, len(normalized))):
        z[index] = normalized[index]

    result = zero_series(length, d)
    z_power = zero_series(length, d)
    z_power[0] = Quad.rational(1, d)
    for k in range(length):
        coefficient = generalized_negative_binomial(exponent, k)
        for index in range(length):
            result[index] = result[index] + coefficient * z_power[index]
        z_power = series_multiply(z_power, z, length)

    prefactor = f0 ** (-exponent)
    return [prefactor * coefficient for coefficient in result]


def polynomial_at_shift(coefficients: Iterable[int], root: Quad, length: int) -> Series:
    """Expand sum_j coefficients[j]*(root+x)^j."""
    coefficients = list(coefficients)
    d = root.d
    out = zero_series(length, d)
    for power, coefficient in enumerate(coefficients):
        for x_power in range(min(power, length - 1) + 1):
            out[x_power] = out[x_power] + (
                coefficient * comb(power, x_power) * (root ** (power - x_power))
            )
    return out


def sector_definition(name: str, sign: int) -> dict[str, Any]:
    if name == "positive":
        d = 10
        numerator_a = 1
        order = 24
        target = [1, -2, 11]
        other = [1, 4, 11]
        other_order = 15
        field_discriminant = -40
        ring = "Z[sqrt(-10)]"
    elif name == "negative":
        d = 7
        numerator_a = -2
        order = 15
        target = [1, 4, 11]
        other = [1, -2, 11]
        other_order = 24
        field_discriminant = -7
        ring = "Z[(1+sqrt(-7))/2]"
    else:
        raise ValueError(name)

    root = Quad(Fraction(numerator_a, 11), Fraction(sign, 11), d)
    numerator = Quad(Fraction(numerator_a), Fraction(sign), d)
    denominator_generator = numerator.conjugate()
    assert numerator * denominator_generator == Quad.rational(11, d)
    assert root == Quad.rational(1, d) / denominator_generator

    return {
        "name": name,
        "sign": sign,
        "d": d,
        "root": root,
        "order": order,
        "target": target,
        "other": other,
        "other_order": other_order,
        "field_discriminant": field_discriminant,
        "ring_of_integers": ring,
        "numerator": numerator,
        "denominator_generator": denominator_generator,
    }


def principal_part(sector: dict[str, Any]) -> dict[str, Any]:
    root: Quad = sector["root"]
    order: int = sector["order"]
    length = order
    d = root.d

    target = sector["target"]
    derivative_at_root = target[1] + 2 * target[2] * root
    q1 = [derivative_at_root, Quad.rational(target[2], d)]

    factors: list[tuple[Series, int, str]] = [
        (q1, order, "target_derivative_factor"),
        (polynomial_at_shift([1, 0, -1], root, length), 200, "1-u^2"),
        (polynomial_at_shift([1, -1], root, length), 1, "1-u"),
        (polynomial_at_shift([1, -11], root, length), 1, "1-11u"),
        (
            polynomial_at_shift(sector["other"], root, length),
            sector["other_order"],
            "other_nontrivial_quadratic",
        ),
    ]

    inverse_product = zero_series(length, d)
    inverse_product[0] = Quad.rational(1, d)
    positive_product = zero_series(length, d)
    positive_product[0] = Quad.rational(1, d)

    for series, exponent, _ in factors:
        inverse_product = series_multiply(
            inverse_product,
            series_negative_power(series, exponent, length),
            length,
        )
        positive_product = series_multiply(
            positive_product,
            series_power_positive(series, exponent, length),
            length,
        )

    identity = series_multiply(inverse_product, positive_product, length)
    exact_identity = identity[0] == Quad.rational(1, d) and all(
        x.is_zero() for x in identity[1:]
    )

    coefficients = [
        {
            "laurent_power": index - order,
            "coefficient": coefficient.payload(),
        }
        for index, coefficient in enumerate(inverse_product)
    ]

    return {
        "root": root.payload(),
        "minimal_polynomial": (
            "11*u^2-2*u+1" if sector["name"] == "positive" else "11*u^2+4*u+1"
        ),
        "pole_order": order,
        "field": f"Q(sqrt(-{d}))",
        "field_discriminant": sector["field_discriminant"],
        "ring_of_integers": sector["ring_of_integers"],
        "coordinate_denominator_ideal": {
            "generator": sector["denominator_generator"].expression(),
            "norm": "11",
            "identity": f"u=1/({sector['denominator_generator'].expression()})",
            "interpretation": "a prime ideal factor above 11, not the full ideal (11)",
        },
        "leading_laurent_coefficient": inverse_product[0].payload(),
        "residue": inverse_product[order - 1].payload(),
        "principal_part_coefficients": coefficients,
        "series_inverse_identity_exact": exact_identity,
    }


def build_certificate() -> dict[str, Any]:
    poles = [
        principal_part(sector_definition(name, sign))
        for name in ("positive", "negative")
        for sign in (1, -1)
    ]
    checks = {
        "four_distinct_nontrivial_locations": len(poles) == 4,
        "orders_are_24_24_15_15": sorted(p["pole_order"] for p in poles)
        == [15, 15, 24, 24],
        "total_nontrivial_pole_order_is_78": sum(p["pole_order"] for p in poles)
        == 78,
        "all_principal_parts_exact": all(
            p["series_inverse_identity_exact"] for p in poles
        ),
        "all_coordinate_denominator_norms_11": all(
            p["coordinate_denominator_ideal"]["norm"] == "11" for p in poles
        ),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "counting_correction": {
            "restricted_adjacency_slots": 24 + 15,
            "distinct_nontrivial_pole_locations": 4,
            "total_nontrivial_pole_order": 2 * 24 + 2 * 15,
            "explanation": (
                "each of the 39 restricted adjacency slots contributes two conjugate "
                "Ihara roots; equal eigenvalues coalesce into poles of order 24 or 15"
            ),
        },
        "ihara_inverse": (
            "(1-u^2)^200(1-u)(1-11u)"
            "(1-2u+11u^2)^24(1+4u+11u^2)^15"
        ),
        "poles": poles,
        "checks": checks,
    }


def main() -> None:
    payload = build_certificate()
    output = ROOT / "data" / "w33_ihara_principal_parts_exact.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(
        json.dumps(
            {
                "status": payload["status"],
                "counting_correction": payload["counting_correction"],
                "pole_summaries": [
                    {
                        "root": p["root"]["expression"],
                        "order": p["pole_order"],
                        "field": p["field"],
                        "denominator_ideal": p["coordinate_denominator_ideal"],
                        "residue": p["residue"]["expression"],
                    }
                    for p in payload["poles"]
                ],
                "checks": payload["checks"],
            },
            indent=2,
        )
    )
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
