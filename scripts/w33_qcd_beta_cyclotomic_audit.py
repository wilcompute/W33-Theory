"""QCD β-function cyclotomic audit for W(3,3).

Finding (new, May 2026 sprint):

    At the physical Standard-Model content (Nc = 3, Nf = 6 above m_t),
    the first three MS-bar QCD β-coefficients are exact W(3,3)
    cyclotomic rationals at q = 3:

        β₀ = Φ₆(q)        = q² − q + 1        = 7
        β₁ = 2·Φ₃(q)      = 2(q² + q + 1)     = 26
        β₂ = −(5/2)·Φ₃(q) = −(5/2)(q² + q + 1) = −65/2

This is strictly stronger than the previously catalogued
β₀ = Φ₆(q=3) = 7 identity, and it is scheme-restricted: β₀ and β₁
are scheme-independent (MS-bar, on-shell, and most standard schemes
agree); β₂ is MS-bar specific. From β₃ onward MS-bar coefficients
contain transcendental ζ(3), ζ(5), … and cannot be expressed as
cyclotomic rationals, so the identity tower *must* stop at three
loops in MS-bar.

Group-theoretically the identity reads, in Eisenstein-integer norms,

        β₀ = |q + ω|²          (ω = primitive cube root of unity)
        β₁ = 2·|q − ω|²
        β₂ = −(5/2)·|q − ω|²

so β₀, β₁ come from conjugate Eisenstein primes lying over q = 3.

Tier: exact finite arithmetic identity
(on the structural side — the coefficients are fixed by Nc, Nf and
group-theoretic Casimirs; the W(3,3) claim is that the q = 3 / Nc = 3 /
Nf = 6 slice projects those coefficients onto the Φ_n(q) ring).
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from typing import Dict

Q = 3
PHI3 = Q * Q + Q + 1  # 13
PHI4 = Q * Q + 1  # 10
PHI6 = Q * Q - Q + 1  # 7


def _Cf(Nc: int) -> Fraction:
    """SU(Nc) fundamental Casimir."""
    return Fraction(Nc * Nc - 1, 2 * Nc)


def msbar_beta_coefficients(Nc: int, Nf: int) -> Dict[str, Fraction]:
    """Exact MS-bar QCD β-coefficients β₀, β₁, β₂ for SU(Nc), Nf flavors.

    Normalization: μ² dg²/dμ² = −β₀/(4π)² · g⁴ − β₁/(4π)⁴ · g⁶
    − β₂/(4π)⁶ · g⁸ − ... as in standard textbooks (Peskin-Schroeder,
    Vermaseren-Larin-Tkachov).
    """
    Cf = _Cf(Nc)
    Ca = Fraction(Nc)
    b0 = Fraction(11 * Nc, 3) - Fraction(2 * Nf, 3)
    b1 = Fraction(34 * Nc * Nc, 3) - Fraction(10 * Nc * Nf, 3) - 2 * Cf * Nf
    # Closed-form β₂ for SU(3) MS-bar (Tarasov-Vladimirov-Zharkov 1980).
    # For general Nc the formula is more involved; we only need SU(3) here.
    if Nc == 3:
        b2 = (
            Fraction(2857, 2)
            - Fraction(5033, 18) * Nf
            + Fraction(325, 54) * Nf * Nf
        )
    else:
        b2 = None
    return {"beta0": b0, "beta1": b1, "beta2": b2}


@lru_cache(maxsize=1)
def w33_qcd_beta_cyclotomic_audit() -> Dict[str, object]:
    """Return the exact audit packet for QCD β-coefficients at SM content."""
    standard_model = msbar_beta_coefficients(Nc=3, Nf=6)
    b0, b1, b2 = (
        standard_model["beta0"],
        standard_model["beta1"],
        standard_model["beta2"],
    )

    phi3 = Fraction(PHI3)
    phi6 = Fraction(PHI6)

    return {
        "source": "scripts/w33_qcd_beta_cyclotomic_audit.py",
        "scheme": "MS-bar",
        "gauge": "SU(3)_c",
        "matter": "Nf=6 active flavors (above m_t threshold)",
        "w33_constants": {
            "q": Q,
            "Phi3": PHI3,
            "Phi4": PHI4,
            "Phi6": PHI6,
        },
        "identity": {
            "beta0": {
                "value": str(b0),
                "cyclotomic": "Phi_6(q)",
                "equal_Phi6": b0 == phi6,
                "scheme_independent": True,
            },
            "beta1": {
                "value": str(b1),
                "cyclotomic": "2 * Phi_3(q)",
                "equal_2Phi3": b1 == 2 * phi3,
                "scheme_independent": True,
            },
            "beta2": {
                "value": str(b2),
                "cyclotomic": "-(5/2) * Phi_3(q)",
                "equal_minus_5_over_2_Phi3": b2 == -Fraction(5, 2) * phi3,
                "scheme_independent": False,
            },
        },
        "cross_ratios": {
            "beta1_over_beta0": str(b1 / b0),
            "beta1_over_beta2": str(b1 / b2),  # -4/5 at SM content
            "beta0_beta1_product": str(b0 * b1),  # 14 * Phi3 = 182
        },
        "eisenstein_interpretation": {
            "omega_order": 3,
            "phi6_as_norm": "|q + omega|^2 = q^2 - q + 1",
            "phi3_as_norm": "|q - omega|^2 = q^2 + q + 1",
            "note": (
                "beta0 and beta1/2 are exact Eisenstein-integer norms at q=3; "
                "they realize the conjugate primes of ring Z[omega] above q=3."
            ),
        },
        "tier_note": (
            "exact finite arithmetic identity, MS-bar QCD; "
            "extends the previously catalogued beta0 = Phi6(3) identity "
            "to beta0, beta1 (scheme-independent) and beta2 (MS-bar specific)."
        ),
        "termination": (
            "From beta3 onward, MS-bar coefficients contain transcendental "
            "zeta(3), zeta(5), ..., so the cyclotomic-rational tower is "
            "exactly three loops long at SM content in MS-bar."
        ),
    }


def assert_all_identities_hold() -> None:
    """Raise AssertionError if any exact identity fails."""
    packet = w33_qcd_beta_cyclotomic_audit()
    for coeff, info in packet["identity"].items():
        flag_key = next(k for k in info if k.startswith("equal"))
        if not info[flag_key]:
            raise AssertionError(
                f"QCD cyclotomic identity failed for {coeff}: {info}"
            )
    b0 = Fraction(packet["identity"]["beta0"]["value"])
    b1 = Fraction(packet["identity"]["beta1"]["value"])
    assert b0 == Fraction(PHI6), "beta0 must equal Phi6(3)=7"
    assert b1 == 2 * Fraction(PHI3), "beta1 must equal 2*Phi3(3)=26"


if __name__ == "__main__":
    import json

    assert_all_identities_hold()
    print(json.dumps(w33_qcd_beta_cyclotomic_audit(), indent=2))
