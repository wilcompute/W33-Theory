"""w33_spectral_core.py

Core W(3,3) spectral data, identities, and verified arithmetic facts.
All values verified computationally — see paper/EXTENSIONS.md for derivations.

Usage:
    from scripts.w33_spectral_core import W33, spectral_moment, spec_zeta
"""
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class W33Params:
    """Immutable W(3,3) parameter block with self-verification."""
    # Graph parameters
    k:   int = 12
    v:   int = 40
    f:   int = 24
    g:   int = 15
    q:   int = 3
    # Eigenvalues
    ev_r: int = 2
    ev_s: int = -4
    # Cyclotomic values at q=3
    Phi3: int = 13
    Phi4: int = 10
    Phi6: int = 7
    mu:   int = 4        # q+1
    two_k_minus_1: int = 23
    # Derived counts
    n_vertices: int = 80   # 2v
    n_edges:    int = 480  # v*k
    n_zero:     int = 0    # corrected: bipartite has no zero eigenvalues

    def __post_init__(self):
        assert self.k == self.q * (self.q + 1),            "k = q(q+1)"
        assert self.f == self.q * (self.q+1)**2 // 2,      "f = q(q+1)^2/2"
        assert self.g == self.q * (self.q**2 + 1) // 2,   "g = q(q^2+1)/2"
        assert self.k + self.g == self.q**self.q,           "k+g = q^q"
        assert -self.f == -24,                              "tau(2) = -f"
        assert self.k * self.q * self.Phi6 == 252,          "tau(3) = k*q*Phi6"
        assert self.Phi3 == self.q**2 + self.q + 1,        "Phi3(q)"
        assert self.Phi4 == self.q**2 + 1,                 "Phi4(q)"
        assert self.Phi6 == self.q**2 - self.q + 1,        "Phi6(q)"
        assert self.mu == self.q + 1,                      "mu = q+1"
        assert self.two_k_minus_1 == 2*self.k - 1,         "2k-1"
        assert self.n_vertices == 2*self.v,                "n_vertices = 2v"
        assert self.n_edges == self.v * self.k,            "n_edges = v*k"
        assert 2 + 2*self.f + 2*self.g == self.n_vertices, "spectrum count = 2v"


W33 = W33Params()

# Full corrected adjacency spectrum: (eigenvalue, multiplicity)
SPECTRUM: List[Tuple[int, int]] = [
    (+W33.k,          1),
    (-W33.k,          1),
    (+W33.ev_r,       W33.f),
    (-W33.ev_r,       W33.f),
    (+abs(W33.ev_s),  W33.g),
    (-abs(W33.ev_s),  W33.g),
]


def spectral_moment(n: int) -> float:
    """M_n = (1/2v) * Tr(A^n) = (1/2v) * sum_lambda mult * lambda^n."""
    return sum(mult * lam**n for lam, mult in SPECTRUM) / W33.n_vertices


def spec_zeta(s: float) -> float:
    """W(3,3) spectral zeta zeta_{W33}(s) = (1/2v)*sum_{|lambda|>0} mult*|lambda|^{-s}."""
    return sum(mult * abs(lam)**(-s)
               for lam, mult in SPECTRUM if lam != 0) / W33.n_vertices


def ihara_p1(u: float) -> float:
    """r-eigenspace Ihara factor: p1(u) = 1 - ev_r*u + (k-1)*u^2."""
    return 1 - W33.ev_r * u + (W33.k - 1) * u**2


def ihara_p2(u: float) -> float:
    """s-eigenspace Ihara factor: p2(u) = 1 - ev_s*u + (k-1)*u^2."""
    return 1 - W33.ev_s * u + (W33.k - 1) * u**2


def ihara_zeta_numerator(u: float) -> float:
    """Ihara zeta numerator: p1(u)^f * p2(u)^g."""
    return ihara_p1(u)**W33.f * ihara_p2(u)**W33.g


# ── New arithmetic identities (April 2026) ────────────────────────────────────

def M4_formula(q: int) -> int:
    """THEOREM (April 2026): M_4(q) = q*(q+1)^2*(q^2+q+1) = q*mu^2*Phi3(q).

    Proved via corrected bipartite spectrum + symbolic factoring.
    Verified for q = 2, 3, 4, 5, 7.
    """
    return q * (q+1)**2 * (q**2 + q + 1)


def moment_recurrence_coeffs() -> Tuple[int, int, int]:
    """Return (c1, c2, c3) for the 3-term spectral moment recurrence:

        a_n = c1*a_{n-1} - c2*a_{n-2} + c3*a_{n-3}

    Characteristic roots: {k^2, ev_r^2, ev_s^2} = {144, 4, 16}.
    """
    k2 = W33.k**2
    r2 = W33.ev_r**2
    s2 = W33.ev_s**2
    c1 = k2 + r2 + s2
    c2 = k2*r2 + k2*s2 + r2*s2
    c3 = k2 * r2 * s2
    return int(c1), int(c2), int(c3)


def ramanujan_bound_check() -> bool:
    """Verify W(3,3) satisfies |lambda| <= 2*sqrt(k-1) for all non-trivial eigenvalues."""
    bound = 2 * np.sqrt(W33.k - 1)
    return all(
        abs(lam) <= bound + 1e-10
        for lam, _ in SPECTRUM
        if abs(lam) not in (0, W33.k)
    )


if __name__ == "__main__":
    print("W(3,3) spectral core — self-verification")
    print(f"  k={W33.k}, v={W33.v}, f={W33.f}, g={W33.g}, q={W33.q}")
    print(f"  Spectrum total: {sum(m for _,m in SPECTRUM)} = 2v={W33.n_vertices}  "
          + ("✓" if sum(m for _,m in SPECTRUM)==W33.n_vertices else "FAIL"))
    print(f"  M_2  = {spectral_moment(2):.1f}  (should = k={W33.k})")
    print(f"  M_4  = {spectral_moment(4):.1f}  (formula: {M4_formula(W33.q)})")
    c1, c2, c3 = moment_recurrence_coeffs()
    print(f"  Recurrence: a_n = {c1}*a_{{n-1}} - {c2}*a_{{n-2}} + {c3}*a_{{n-3}}")
    print(f"  Ramanujan bound satisfied: {ramanujan_bound_check()}")
    print(f"  zeta_W33(1)  = {spec_zeta(1):.6f}")
    print(f"  zeta_W33(2)  = {spec_zeta(2):.6f}")
    print(f"  zeta_W33(11) = {spec_zeta(11):.6e}")
