#!/usr/bin/env python3
"""Verified spectral core for the exact W(3,3) kernel.

This module packages the strongest already-exact spectral data for the live
W33 kernel into one reusable surface:

1. The SRG(40,12,2,4) adjacency spectrum 12^1, 2^24, (-4)^15.
2. The corrected 80-mode bipartite lift spectrum with no zero modes:
   +/-12 (x1), +/-2 (x24), +/-4 (x15).
3. The exact even-moment recurrence coming from the squared roots
   {144, 16, 4}.
4. The canonical Hamiltonian zeta packet for H_can = 12 I - A.
5. The Ihara determinant factorization for W(3,3).

The module also preserves the older `W33` / `spectral_moment` / `spec_zeta`
surface so the April 2026 scripts keep running after the spectral-core
refactor.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from functools import lru_cache
import json
import math
from pathlib import Path
import sys
from typing import Dict, Tuple

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.w33_qutrit_operator_algebra import summarize_canonical_projective_hamiltonian
from scripts.w3q_scaling_family import w3q_parameters

Eigenpair = Tuple[int, int]


def family_fourth_moment_per_vertex(q_value: int) -> int:
    """Exact per-vertex fourth adjacency moment for W(3,q)."""
    vertex_count, degree, lam, mu = w3q_parameters(q_value)
    return degree * degree + degree * lam * lam + (vertex_count - degree - 1) * mu * mu


def family_fourth_moment_formula(q_value: int) -> int:
    """Closed form of the per-vertex fourth adjacency moment for W(3,q)."""
    return q_value * (q_value + 1) * (q_value**3 + 3 * q_value * q_value - q_value + 1)


def q3_special_fourth_moment_factorization(q_value: int) -> int:
    """The special q=3 factorization highlighted by the live W33 kernel."""
    return q_value * (q_value + 1) ** 2 * (q_value**2 + q_value + 1)


def _fraction_payload(value: Fraction) -> Dict[str, object]:
    return {"exact": str(value), "float": float(value)}


@dataclass(frozen=True)
class LegacyW33Params:
    """Backward-compatible W(3,3) packet used by older scripts."""

    k: int = 12
    v: int = 40
    f: int = 24
    g: int = 15
    q: int = 3
    ev_r: int = 2
    ev_s: int = -4
    Phi3: int = 13
    Phi4: int = 10
    Phi6: int = 7
    mu: int = 4
    two_k_minus_1: int = 23
    n_vertices: int = 80
    n_edges: int = 480
    n_zero: int = 0


W33 = LegacyW33Params()
SPECTRUM: Tuple[Eigenpair, ...] = (
    (+W33.k, 1),
    (-W33.k, 1),
    (+W33.ev_r, W33.f),
    (-W33.ev_r, W33.f),
    (+abs(W33.ev_s), W33.g),
    (-abs(W33.ev_s), W33.g),
)


def spectral_moment(n: int) -> Fraction:
    """Legacy bipartite-lift moment normalized by 2v."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    return Fraction(sum(mult * (lam**n) for lam, mult in SPECTRUM), W33.n_vertices)


def spec_zeta(s: int | float) -> float:
    """Legacy adjacency-absolute spectral zeta on the corrected 80-mode lift."""
    return sum(mult * abs(lam) ** (-s) for lam, mult in SPECTRUM if lam != 0) / W33.n_vertices


def ihara_p1(u: float) -> float:
    """Legacy r-eigenspace Ihara factor."""
    return 1 - W33.ev_r * u + (W33.k - 1) * u**2


def ihara_p2(u: float) -> float:
    """Legacy s-eigenspace Ihara factor."""
    return 1 - W33.ev_s * u + (W33.k - 1) * u**2


def ihara_zeta_numerator(u: float) -> float:
    """Legacy Ihara numerator p_r(u)^f p_s(u)^g."""
    return ihara_p1(u) ** W33.f * ihara_p2(u) ** W33.g


def M4_formula(q_value: int) -> int:
    """Legacy closed form for the fourth moment family."""
    return family_fourth_moment_formula(q_value)


def moment_recurrence_coeffs() -> Tuple[int, int, int]:
    """Legacy signless recurrence coefficients."""
    coeff_1, coeff_2, coeff_3 = get_w33_spectral_core().even_moment_recurrence_coefficients
    return (coeff_1, abs(coeff_2), coeff_3)


def ramanujan_bound_check() -> bool:
    """Legacy Ramanujan bound verifier for the nontrivial adjacency eigenvalues."""
    bound = 2 * math.sqrt(W33.k - 1)
    return all(
        abs(lam) <= bound + 1e-10
        for lam, _ in SPECTRUM
        if abs(lam) not in (0, W33.k)
    )


@dataclass(frozen=True)
class W33SpectralCore:
    q: int = 3
    v: int = 40
    k: int = 12
    lam: int = 2
    mu: int = 4
    adjacency_positive_eigenvalue: int = 2
    adjacency_positive_multiplicity: int = 24
    adjacency_negative_eigenvalue: int = -4
    adjacency_negative_multiplicity: int = 15
    self_verified: bool = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "self_verified", self._run_self_checks())

    @property
    def adjacency_eigenpairs(self) -> Tuple[Eigenpair, ...]:
        return (
            (self.k, 1),
            (self.adjacency_positive_eigenvalue, self.adjacency_positive_multiplicity),
            (self.adjacency_negative_eigenvalue, self.adjacency_negative_multiplicity),
        )

    @property
    def bipartite_lift_positive_eigenpairs(self) -> Tuple[Eigenpair, ...]:
        return (
            (12, 1),
            (4, 15),
            (2, 24),
        )

    @property
    def bipartite_lift_negative_eigenpairs(self) -> Tuple[Eigenpair, ...]:
        return (
            (-2, 24),
            (-4, 15),
            (-12, 1),
        )

    @property
    def bipartite_lift_zero_mode_count(self) -> int:
        return 0

    @property
    def bipartite_lift_mode_count(self) -> int:
        return 2 * self.v

    @property
    def canonical_hamiltonian_eigenpairs(self) -> Tuple[Eigenpair, ...]:
        return (
            (0, 1),
            (self.k - self.adjacency_positive_eigenvalue, self.adjacency_positive_multiplicity),
            (self.k - self.adjacency_negative_eigenvalue, self.adjacency_negative_multiplicity),
        )

    @property
    def even_moment_characteristic_roots(self) -> Tuple[int, int, int]:
        return (self.k * self.k, 16, 4)

    @property
    def even_moment_recurrence_coefficients(self) -> Tuple[int, int, int]:
        root_a, root_b, root_c = self.even_moment_characteristic_roots
        pairwise_sum = root_a * root_b + root_a * root_c + root_b * root_c
        return (root_a + root_b + root_c, -pairwise_sum, root_a * root_b * root_c)

    @property
    def even_moment_recurrence_formula(self) -> str:
        coeff_1, coeff_2, coeff_3 = self.even_moment_recurrence_coefficients
        return f"a_n = {coeff_1}*a_(n-1) - {abs(coeff_2)}*a_(n-2) + {coeff_3}*a_(n-3)"

    def adjacency_moment(self, power: int) -> int:
        if power < 0:
            raise ValueError("power must be nonnegative")
        return sum(eigenvalue**power * multiplicity for eigenvalue, multiplicity in self.adjacency_eigenpairs)

    def adjacency_moment_per_vertex(self, power: int) -> Fraction:
        return Fraction(self.adjacency_moment(power), self.v)

    def even_adjacency_moment(self, index: int) -> int:
        if index < 0:
            raise ValueError("index must be nonnegative")
        return self.adjacency_moment(2 * index)

    def verify_even_moment_recurrence(self, max_index: int = 8) -> bool:
        coeff_1, coeff_2, coeff_3 = self.even_moment_recurrence_coefficients
        for index in range(3, max_index + 1):
            lhs = self.even_adjacency_moment(index)
            rhs = (
                coeff_1 * self.even_adjacency_moment(index - 1)
                + coeff_2 * self.even_adjacency_moment(index - 2)
                + coeff_3 * self.even_adjacency_moment(index - 3)
            )
            if lhs != rhs:
                return False
        return True

    def canonical_hamiltonian_zeta(self, s_value: int) -> Fraction:
        if not isinstance(s_value, int):
            raise TypeError("s_value must be an integer")
        if s_value >= 0:
            return Fraction(24, 10**s_value) + Fraction(15, 16**s_value)
        return Fraction(24 * 10 ** (-s_value) + 15 * 16 ** (-s_value), 1)

    @property
    def zeta_regularised_determinant(self) -> int:
        return 10**24 * 16**15

    @property
    def ihara_cycle_rank(self) -> int:
        edge_count = self.v * self.k // 2
        return edge_count - self.v

    @property
    def ihara_k_minus_1(self) -> int:
        return self.k - 1

    @property
    def ihara_trivial_factor_roots(self) -> Tuple[Fraction, Fraction]:
        return (Fraction(1, 11), Fraction(1, 1))

    @property
    def ihara_nontrivial_discriminants(self) -> Tuple[int, int]:
        u = sp.symbols("u")
        factor_r = sp.expand(1 - self.adjacency_positive_eigenvalue * u + self.ihara_k_minus_1 * u * u)
        factor_s = sp.expand(1 - self.adjacency_negative_eigenvalue * u + self.ihara_k_minus_1 * u * u)
        return (
            int(sp.discriminant(factor_r, u)),
            int(sp.discriminant(factor_s, u)),
        )

    def to_dict(self) -> Dict[str, object]:
        return {
            "status": "ok",
            "srg_parameters": (self.v, self.k, self.lam, self.mu),
            "adjacency_eigenpairs": self.adjacency_eigenpairs,
            "bipartite_lift_spectrum": {
                "positive": self.bipartite_lift_positive_eigenpairs,
                "negative": self.bipartite_lift_negative_eigenpairs,
                "zero_mode_count": self.bipartite_lift_zero_mode_count,
                "total_mode_count": self.bipartite_lift_mode_count,
            },
            "canonical_hamiltonian_eigenpairs": self.canonical_hamiltonian_eigenpairs,
            "fourth_moment": {
                "family_formula": "q*(q+1)*(q**3 + 3*q**2 - q + 1)",
                "q3_special_factorization": "q*(q+1)**2*(q**2 + q + 1)",
                "q3_per_vertex": int(self.adjacency_moment_per_vertex(4)),
                "sample_values": {
                    q_value: family_fourth_moment_per_vertex(q_value)
                    for q_value in (2, 3, 4, 5, 7)
                },
            },
            "even_moment_recurrence": {
                "characteristic_roots": self.even_moment_characteristic_roots,
                "formula": self.even_moment_recurrence_formula,
                "coefficients": self.even_moment_recurrence_coefficients,
            },
            "canonical_hamiltonian_zeta": {
                "zeta_1": _fraction_payload(self.canonical_hamiltonian_zeta(1)),
                "zeta_2": _fraction_payload(self.canonical_hamiltonian_zeta(2)),
                "zeta_minus_1": _fraction_payload(self.canonical_hamiltonian_zeta(-1)),
                "zeta_regularised_determinant": str(self.zeta_regularised_determinant),
            },
            "ihara_determinant": {
                "cycle_rank": self.ihara_cycle_rank,
                "k_minus_1": self.ihara_k_minus_1,
                "trivial_factor_roots": tuple(str(root) for root in self.ihara_trivial_factor_roots),
                "nontrivial_discriminants": self.ihara_nontrivial_discriminants,
            },
            "legacy_api": {
                "spectral_moment_2": str(spectral_moment(2)),
                "spectral_moment_4": str(spectral_moment(4)),
                "spec_zeta_1": spec_zeta(1),
                "spec_zeta_2": spec_zeta(2),
                "spec_zeta_11": spec_zeta(11),
            },
            "self_verified": self.self_verified,
        }

    def _run_self_checks(self) -> bool:
        if w3q_parameters(self.q) != (self.v, self.k, self.lam, self.mu):
            raise ValueError("W(3,3) family parameters drifted")

        canonical = summarize_canonical_projective_hamiltonian()
        if canonical["laplacian_eigenpairs"] != self.canonical_hamiltonian_eigenpairs:
            raise ValueError("canonical Hamiltonian spectrum drifted")

        if self.bipartite_lift_mode_count != 80 or self.bipartite_lift_zero_mode_count != 0:
            raise ValueError("bipartite lift spectrum no longer has 80 nonzero modes")

        sample_q_values = (2, 3, 4, 5, 7)
        for q_value in sample_q_values:
            if family_fourth_moment_per_vertex(q_value) != family_fourth_moment_formula(q_value):
                raise ValueError(f"fourth moment family formula drifted at q={q_value}")

        if family_fourth_moment_per_vertex(self.q) != q3_special_fourth_moment_factorization(self.q):
            raise ValueError("q=3 special fourth moment factorization drifted")

        if int(self.adjacency_moment_per_vertex(4)) != family_fourth_moment_per_vertex(self.q):
            raise ValueError("q=3 fourth moment no longer matches the live adjacency spectrum")

        if not self.verify_even_moment_recurrence():
            raise ValueError("even-moment recurrence drifted")

        if self.canonical_hamiltonian_zeta(1) != Fraction(267, 80):
            raise ValueError("zeta(1) drifted")
        if self.canonical_hamiltonian_zeta(2) != Fraction(1911, 6400):
            raise ValueError("zeta(2) drifted")
        if self.canonical_hamiltonian_zeta(-1) != Fraction(480, 1):
            raise ValueError("zeta(-1) drifted")

        if self.zeta_regularised_determinant != 10**24 * 16**15:
            raise ValueError("zeta-regularised determinant drifted")

        if self.ihara_cycle_rank != 200 or self.ihara_k_minus_1 != 11:
            raise ValueError("Ihara rank packet drifted")
        if self.ihara_nontrivial_discriminants != (-40, -28):
            raise ValueError("Ihara nontrivial discriminants drifted")

        if spectral_moment(2) != Fraction(12, 1):
            raise ValueError("legacy spectral moment M2 drifted")
        if spectral_moment(4) != Fraction(624, 1):
            raise ValueError("legacy spectral moment M4 drifted")
        if (self.even_moment_recurrence_coefficients[0], abs(self.even_moment_recurrence_coefficients[1]), self.even_moment_recurrence_coefficients[2]) != (164, 2944, 9216):
            raise ValueError("legacy recurrence coefficients drifted")

        return True


@lru_cache(maxsize=1)
def get_w33_spectral_core() -> W33SpectralCore:
    return W33SpectralCore()


def main() -> None:
    print(json.dumps(get_w33_spectral_core().to_dict(), indent=2))


if __name__ == "__main__":
    main()
